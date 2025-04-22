from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, token, faceswap
import os
from app.config import TMP_DIR, OUTPUT_DIR
from app.utils.cleanup import setup_image_cleanup_scheduler
import uvicorn

app = FastAPI(title="Face Swap API")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
os.makedirs(TMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Include routers
app.include_router(health.router)
app.include_router(token.router)
app.include_router(faceswap.router)

# Setup cleanup scheduler
scheduler = setup_image_cleanup_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 