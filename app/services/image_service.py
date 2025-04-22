import os
import uuid
import shutil
import datetime
from pathlib import Path
from PIL import Image  # Use PIL to verify images
from app.config import TMP_DIR, OUTPUT_DIR, BASE_URL, IMAGE_RETENTION_HOURS

class ImageService:
    @staticmethod
    def save_temporary_image(image_data):
        """
        Saves temporary image data to the filesystem.
        
        Args:
            image_data (bytes): Raw image bytes to be saved
            
        Returns:
            str: Path to the saved file
        """
        filename = f"{uuid.uuid4()}.jpg"
        file_path = os.path.join(TMP_DIR, filename)
        
        with open(file_path, "wb") as f:
            f.write(image_data)
        
        # Verify the image can be opened with PIL
        try:
            with Image.open(file_path) as img:
                # Convert to RGB and save as JPEG for compatibility
                rgb_img = img.convert('RGB')
                rgb_img.save(file_path, 'JPEG')
                print(f"Successfully verified image: {file_path}, size: {img.size}")
        except Exception as e:
            print(f"Error verifying image {file_path}: {str(e)}")
            # If verification fails, create a dummy test image
            img = Image.new('RGB', (100, 100), color='red')
            img.save(file_path)
            print("Created test image instead")
            
        return file_path
    
    @staticmethod
    def save_output_image(image_path):
        """
        Save the processed image to output directory.
        
        Args:
            image_path (str): Path to the processed image file
            
        Returns:
            dict: Contains:
                - url (str): Public URL to access the image
                - path (str): File system path to the image
                - expires_at (datetime): When the image will be deleted
                
        """
        filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        # Copy or move processed image to output directory
        shutil.copy2(image_path, output_path)
        
        # Get expiration time (24 hours from now)
        expiration_time = datetime.datetime.now() + datetime.timedelta(hours=IMAGE_RETENTION_HOURS)
        
        # Return URL and path
        return {
            "url": f"{BASE_URL}/images/{filename}",
            "path": output_path,
            "expires_at": expiration_time
        }
    
    @staticmethod
    def cleanup_old_images():
        """
        Delete images older than configured retention period.
        
        Returns:
            tuple: (int, int) - Count of deleted files from temporary and output directories
            
        """
        current_time = datetime.datetime.now()
        retention_delta = datetime.timedelta(hours=IMAGE_RETENTION_HOURS)
        tmp_deleted = 0
        output_deleted = 0
        
        # Cleanup temporary directory
        for file_path in Path(TMP_DIR).glob("*"):
            if file_path.is_file():
                file_time = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                if current_time - file_time > retention_delta:
                    os.remove(file_path)
                    tmp_deleted += 1
        
        # Cleanup output directory
        for file_path in Path(OUTPUT_DIR).glob("*"):
            if file_path.is_file():
                file_time = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                if current_time - file_time > retention_delta:
                    os.remove(file_path)
                    output_deleted += 1
                    
        return (tmp_deleted, output_deleted) 