from fastapi import APIRouter, HTTPException, Depends, Form
from backend.v1.shared.user_manager import UserManager
from backend.v1.shared.firebase_manager import FirebaseManager
from backend.v1.shared.models import UserRegister, AddAPIKey
from backend.v1.shared.token_manager import TokenManager
from backend.v1.shared.rbac_manager import RBACManager
import asyncio



router = APIRouter()
firebase_manager = FirebaseManager()
user_manager = UserManager(firebase_manager)

@router.get("/{user_id}")
async def get_user(user_id: str):
    """
    Retrieve user details by user_id (with async timeout).
    """
    try:
        user_data = await asyncio.wait_for(
            user_manager.get_user_by_id(user_id),
            timeout=10.0  # Allow longer timeout
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Firebase request timed out")

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    user_data.pop("password_hash", None)
    user_data.pop("serp_api_key", None)

    return user_data

@router.post("/register")
async def register_user(user: UserRegister):
    """
    Register new user.
    """
    return await user_manager.register(
        username=user.username, 
        email=user.email, 
        password=user.password,
        role=user.role
    )

@router.post("/login")
async def login_user(username: str = Form(...), password: str = Form(...)):
    """
    Login and return a token.
    """
    return await user_manager.login(username=username, password=password)
