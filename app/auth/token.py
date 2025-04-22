from fastapi import Depends, HTTPException, Header
from fastapi.security import APIKeyHeader
from app.config import ADMIN_API_KEY
from app.services.token_service import TokenService

# Define API key header schemas
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
admin_key_header = APIKeyHeader(name="X-Admin-Key", auto_error=False)

async def get_token_auth(api_key: str = Depends(api_key_header)):
    """
    Validate the API token for protected endpoints.
    
    Args:
        api_key (str): The token provided in the X-API-Key header
        
    Returns:
        str: The validated token, passed to the endpoint handler
        
    Raises:
        HTTPException(401): When the API key is missing or invalid
        
    """
    if not api_key:
        raise HTTPException(status_code=401, detail="API Key is missing")
    
    if not TokenService.validate_token(api_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    return api_key

async def get_admin_auth(admin_key: str = Depends(admin_key_header)):
    """
    Validate the admin key for admin endpoints.
    
    Args:
        admin_key (str): The admin key provided in the X-Admin-Key header
        
    Returns:
        str: The validated admin key, passed to the endpoint handler
        
    Raises:
        HTTPException(401): When the admin key is missing or invalid
        
    """
    if not admin_key:
        raise HTTPException(status_code=401, detail="Admin Key is missing")
    
    if admin_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid Admin Key")
    
    return admin_key 