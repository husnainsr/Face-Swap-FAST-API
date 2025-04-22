import uuid
import datetime
from pymongo import MongoClient
from bson import ObjectId
from app.config import MONGO_URI, DB_NAME

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
tokens_collection = db["tokens"]
usage_collection = db["usage"]

class TokenService:
    @staticmethod
    def create_token():
        """
        Creates a new API access token.
        
        Returns:
            str: The generated token ID (UUID4 string)
            
        Notes:
            - Creates a token record in the database with zero request count
            - Token is stored with creation timestamp for tracking validity
        """
        token_id = str(uuid.uuid4())
        token_data = {
            "token_id": token_id,
            "created_at": datetime.datetime.utcnow(),
            "total_requests": 0
        }
        tokens_collection.insert_one(token_data)
        return token_id
    
    @staticmethod
    def get_token(token_id):
        """
        Get token details by token ID.
        
        Args:
            token_id (str): The token ID to retrieve
            
        Returns:
            dict: Token details including token_id, created_at, total_requests
                 Returns None if token does not exist
                 
        """
        token = tokens_collection.find_one({"token_id": token_id})
        if token:
            # Convert ObjectId to string to make it JSON serializable
            token["_id"] = str(token["_id"])
            # Ensure datetime is serializable
            token["created_at"] = token["created_at"].isoformat()
        return token
    
    @staticmethod
    def delete_token(token_id):
        """
        Delete a token by token ID.
        
        Args:
            token_id (str): The token ID to delete
            
        Returns:
            bool: True if token was deleted, False if token was not found

        """
        result = tokens_collection.delete_one({"token_id": token_id})
        return result.deleted_count > 0
    
    @staticmethod
    def validate_token(token_id):
        """
        Validate if a token exists and is valid.
        
        Args:
            token_id (str): The token ID to validate
            
        Returns:
            bool: True if token exists, False otherwise

        """
        token = tokens_collection.find_one({"token_id": token_id})
        return token is not None
    
    @staticmethod
    def log_token_usage(token_id):
        """
        Increment the usage count for a token and log the request.
        
        Args:
            token_id (str): The token ID that was used
            
        """
        tokens_collection.update_one(
            {"token_id": token_id},
            {"$inc": {"total_requests": 1}}
        )
        
        # Also log this usage for historical tracking
        usage_log = {
            "token_id": token_id,
            "timestamp": datetime.datetime.utcnow(),
            "endpoint": "faceswap"
        }
        usage_collection.insert_one(usage_log) 