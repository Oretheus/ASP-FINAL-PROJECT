import jwt
import pytest
from datetime import datetime, timezone, timedelta
from v1.shared.token_manager import TokenManager
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def test_create_access_token():
    """
    Test: Create access token
    """
    data = {"user_id": "user123", "role": "user"}
    token = TokenManager.create_access_token(data)
    assert isinstance(token, str)

def test_verify_access_token():
    """
    Test: Verify access token
    """
    data = {"user_id": "123", "role": "user"}
    token = TokenManager.create_access_token(data)
    payload = TokenManager.verify_access_token(token)
    assert payload["user_id"] == "123"
    assert payload["role"] == "user"

def test_expired_token():
    """
    Test: Expired token validation
    """
    data = {"user_id": "123", "role": "user"}
    token = jwt.encode(
        {**data, "exp": datetime.now(timezone.utc) - timedelta(seconds=1)}, 
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    with pytest.raises(ValueError, match="Token has expired"):
        TokenManager.verify_access_token(token)
