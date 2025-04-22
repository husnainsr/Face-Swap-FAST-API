import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB settings
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "FaceSwap")

# Token settings
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "admin-secret-key")
TOKEN_EXPIRY_DAYS = int(os.getenv("TOKEN_EXPIRY_DAYS", "30"))

# Image storage settings
TMP_DIR = os.getenv("TMP_DIR", "tmp")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
IMAGE_RETENTION_HOURS = int(os.getenv("IMAGE_RETENTION_HOURS", "24"))
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000") 