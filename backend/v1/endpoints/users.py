from fastapi import APIRouter, HTTPException, Depends
from backend.v1.shared.user_manager import UserManager
from backend.v1.shared.firebase_manager import FirebaseManager
from backend.v1.shared.models import UserRegister, AddAPIKey
from backend.v1.shared.token_manager import TokenManager
from backend.v1.shared.rbac_manager import RBACManager
from fastapi import Form


router = APIRouter()
firebase_manager = FirebaseManager()
user_manager = UserManager(firebase_manager)

@router.post("/register")
async def register_user(user: UserRegister):
    """
    Register new user.
    """
    return user_manager.register(
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
    return user_manager.login(username=username, password=password)

@router.put("/apikey")
async def add_apikey(apikey_request: AddAPIKey, user: dict = Depends(TokenManager.get_current_user)):
    """
    Add User's API key; includes auth and rbac.
    """
    # Check roles
    RBACManager.require_role(user, ["user", "admin"])

    user_id = user.get("user_id")

    return user_manager.add_apikey(user_id=user_id, apikey=apikey_request.apikey)
