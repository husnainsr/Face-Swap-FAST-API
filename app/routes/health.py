from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    """
    Public endpoint to check API health.
    
    Returns:
        dict: {"status": "ok"}
    """    
    return {"status": "ok"} 