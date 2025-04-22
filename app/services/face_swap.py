import os
import cv2
import numpy as np
import datetime
import insightface
from insightface.app import FaceAnalysis
import urllib.request

# Ensure directories exist
os.makedirs("tmp", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Ensure model directory exists
model_dir = os.path.expanduser('~/.insightface/models')
os.makedirs(model_dir, exist_ok=True)

# Model path
model_path = os.path.join(model_dir, 'inswapper_128.onnx')

# Download model if it doesn't exist
if not os.path.exists(model_path):
    print(f"Downloading model to {model_path}...")
    url = "https://huggingface.co/deepinsight/insightface/resolve/main/inswapper_128.onnx"
    urllib.request.urlretrieve(url, model_path)
    print("Model download complete!")

# Initialize face detector
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=-1, det_size=(640, 640))

# Load swapper
swapper = insightface.model_zoo.get_model(model_path, providers=['CPUExecutionProvider'])

class FaceSwapService:
    @staticmethod
    def swap_faces(source_image_data, target_image_data):
        """
        Performs face swapping between source and target images using InsightFace.
        
        Args:
            source_image_data (bytes): Raw image data containing source face
            target_image_data (bytes): Raw image data containing target face(s)
            
        Returns:
            dict: Contains result information including URL path and expiration
            
        Raises:
            ValueError: If face detection fails or image processing error occurs
        """
        # Create temporary file paths
        source_path = os.path.join("tmp", f"source_{os.urandom(4).hex()}.jpg")
        target_path = os.path.join("tmp", f"target_{os.urandom(4).hex()}.jpg")
        
        # Save uploaded images
        with open(source_path, "wb") as f:
            f.write(source_image_data)
        with open(target_path, "wb") as f:
            f.write(target_image_data)
        
        try:
            # Load images
            source_img = cv2.imread(source_path)
            target_img = cv2.imread(target_path)
            
            if source_img is None or target_img is None:
                raise ValueError("Failed to load images")
            
            # Detect faces
            src_faces = app.get(source_img)
            dst_faces = app.get(target_img)
            
            if len(src_faces) == 0 or len(dst_faces) == 0:
                raise ValueError("No faces detected in one or both images")
            
            # Get the source face
            src_face = src_faces[0]
            
            # Process result
            result_img = target_img.copy()
            
            # Swap each face in the target image
            for dst_face in dst_faces:
                result_img = swapper.get(result_img, dst_face, src_face, paste_back=True)
            
            # Save result
            output_path = os.path.join("output", f"swapped_{os.urandom(4).hex()}.jpg")
            cv2.imwrite(output_path, result_img)
            
            # Return result information
            expiration_time = datetime.datetime.now() + datetime.timedelta(hours=24)
            result_info = {
                "url": f"http://localhost:8000/images/{os.path.basename(output_path)}",
                "path": output_path,
                "expires_at": expiration_time
            }
            
            return result_info
            
        except Exception as e:
            raise ValueError(f"Face swap failed: {str(e)}")
            
        finally:
            # Clean up temporary files
            for path in [source_path, target_path]:
                if os.path.exists(path):
                    os.remove(path)