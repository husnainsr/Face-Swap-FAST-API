from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from app.auth.token import get_token_auth, api_key_header
from app.services.face_swap import FaceSwapService
from app.services.token_service import TokenService
import os
from app.config import OUTPUT_DIR

router = APIRouter(tags=["Face Swap"])

@router.post("/faceswap")
async def face_swap(
    source_image: UploadFile = File(...),
    target_image: UploadFile = File(...),
    token: str = None,
    api_key: str = Depends(api_key_header)
):
    """
    Swaps faces between source and target images.
    
    Args:
        source_image (UploadFile): The uploaded image containing the face to be used as source
        target_image (UploadFile): The uploaded image where the face will be swapped onto
        token (str, optional): Token provided directly in form data
        api_key (str, optional): Token provided via X-API-Key header
        
    Returns:
        dict: Contains:
            - image_url (str): URL to access the processed image
            - expires_at (str): ISO-formatted expiration timestamp
        
    Raises:
        HTTPException(401): If token is invalid or missing
        HTTPException(400): If face detection or image processing fails
        
    """
    # Use either token from form or from header
    token_id = token or api_key
    
    if not token_id or not TokenService.validate_token(token_id):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    try:
        # Read image data
        source_data = await source_image.read()
        target_data = await target_image.read()
        
        # Log token usage
        TokenService.log_token_usage(token_id)
        
        # Process face swap
        result = FaceSwapService.swap_faces(source_data, target_data)
        
        return {
            "image_url": result["url"],
            "expires_at": result["expires_at"].isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Face swap failed: {str(e)}")

@router.get("/images/{filename}")
async def get_image(filename: str):
    """
    Retrieves a processed image by filename.
    
    Args:
        filename (str): The name of the image file to retrieve
        
    Returns:
        FileResponse: The image file as a streaming response
        
    Raises:
        HTTPException(404): If the requested image is not found
        
    """
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(file_path)

@router.get("/images/debug/{filename}")
async def get_debug_image(filename: str):
    """
    Get a debug image from the debug directory.
    
    Args:
        filename (str): The name of the debug image file
        
    Returns:
        FileResponse: The debug image file as a streaming response
        
    Raises:
        HTTPException(404): If the requested debug image is not found
        
    """
    file_path = os.path.join("output", "debug", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Debug image not found")
    
    return FileResponse(file_path)

@router.post("/test-upload")
async def test_upload(
    image: UploadFile = File(...)
):
    """
    Test image upload functionality.
    
    Args:
        image (UploadFile): The image file to be uploaded
        
    Returns:
        dict: Contains:
            - filename (str): Original filename of the uploaded image
            - content_type (str): MIME type of the uploaded file
            - size (int): Size of the image in bytes
    """
    data = await image.read()
    return {
        "filename": image.filename,
        "content_type": image.content_type,
        "size": len(data)
    } 