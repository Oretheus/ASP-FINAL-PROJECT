import jwt
from datetime import datetime, timezone, timedelta
import os
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/login")

class TokenManager:
    @staticmethod
    def create_access_token(data: dict) -> str:
        """
        Create a JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_access_token(token: str) -> dict:
        """
        Verify and decode a JWT access token.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.JWTError:
            raise ValueError("Invalid token")

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
        """
        Extract user data from the JWT token.
        """
        try:
            payload = TokenManager.verify_access_token(token)
            return payload
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))
