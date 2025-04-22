from fastapi import APIRouter, Depends, HTTPException
from app.auth.token import get_admin_auth
from app.services.token_service import TokenService
from pydantic import BaseModel

router = APIRouter(prefix="/token", tags=["Token Management"])

class TokenResponse(BaseModel):
    token_id: str

@router.post("", response_model=TokenResponse)
async def create_token(admin_key: str = Depends(get_admin_auth)):
    """
    Admin endpoint to create a new API token.
    
    Args:
        admin_key: Validated admin key from request header
        
    Returns:
        TokenResponse: Newly created token details
    """
    token_id = TokenService.create_token()
    return {"token_id": token_id}

@router.get("/{token_id}")
async def get_token(token_id: str, admin_key: str = Depends(get_admin_auth)):
    """
    Admin endpoint to retrieve token information.
    
    Args:
        token_id: ID of the token to retrieve
        admin_key: Validated admin key from request header
        
    Returns:
        TokenResponse: Token details
        
    Raises:
        HTTPException: If token not found
    """
    token = TokenService.get_token(token_id)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    return token

@router.delete("/{token_id}")
async def delete_token(token_id: str, admin_key: str = Depends(get_admin_auth)):
    """
    Admin endpoint to delete a token.
    
    Args:
        token_id: ID of the token to delete
        admin_key: Validated admin key from request header
        
    Returns:
        TokenResponse: Deleted token details
        
    Raises:
        HTTPException: If token not found
    """
    success = TokenService.delete_token(token_id)
    if not success:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"message": "Token deleted successfully"} 