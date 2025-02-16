import uuid
from fastapi import HTTPException
from datetime import datetime, timezone
from passlib.context import CryptContext
from backend.v1.shared.firebase_manager import FirebaseManager
from backend.v1.shared.token_manager import TokenManager

class UserManager:
    def __init__(self, firebase_manager: FirebaseManager):
        self.firebase_manager = firebase_manager
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def register(self, username: str, email: str, password: str, role: str = "user"):
        """
        Register a new user.
        """
        user_id = str(uuid.uuid4())
        hashed_password = self.pwd_context.hash(password)
        user_data = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "password_hash": hashed_password,
            "level": "Beginner",
            "points": 0,
            "role": role,
            "date_joined": datetime.now(timezone.utc),
        }

        result = self.firebase_manager.store_data("users", user_id, user_data)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return {"message": "User registered successfully", "user_id": user_id}

    def login(self, username: str, password: str):
        """
        Authenticate a user.
        """
        # Identify whether username is an email or username
        if "@" in username:
            # Search by email
            user_data = self.firebase_manager.get_user_data("users", username)
        else:
            # Search by username
            user_docs = self.firebase_manager.db.collection("users").where("username", "==", username).stream()
            user_data = None
            for doc in user_docs:
                user_data = doc.to_dict()
                break
            
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        if not self.pwd_context.verify(password, user_data["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generate a JWT token with user_id and role
        token_data = {
            "user_id": user_data["user_id"],
            "role": user_data["role"]
        }
        access_token = TokenManager.create_access_token(data=token_data)

        return {
            "message": "Login successful", 
            "access_token": access_token,
            "token_type": "bearer"
        }

    def add_apikey(self, user_id: str, apikey: str):
        """
        Add or update user's SERP API key.
        """
        user_data = self.firebase_manager.get_data("users", user_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        user_data["serp_api_key"] = apikey
        result = self.firebase_manager.store_data("users", user_id, user_data)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return {"message": "API key added successfully"}
