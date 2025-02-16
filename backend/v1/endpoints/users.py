from fastapi import APIRouter, HTTPException, Depends
from backend.v1.shared.user_manager import UserManager
from backend.v1.shared.firebase_manager import FirebaseManager
from backend.v1.shared.models import UserRegister, UserLogin, AddAPIKey
from backend.v1.shared.token_manager import TokenManager
from backend.v1.shared.rbac_manager import RBACManager



router = APIRouter()
firebase_manager = FirebaseManager()
user_manager = UserManager(firebase_manager)

@router.get("/{user_id}")
async def get_user(user_id: str, user: dict = Depends(TokenManager.get_current_user)):
    """
    Retrieve user information by user_id (requires auth).
    Only admin or the user themselves can view user details.
    """
    # Authorization Check
    if user.get("user_id") != user_id and not RBACManager.has_role(user, "admin"):
        raise HTTPException(status_code=403, detail="Permission denied")

    user_data = user_manager.get_user_by_id(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Hide sensitive fields before returning
    user_data.pop("password_hash", None)
    user_data.pop("serp_api_key", None)
    
    return user_data

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
async def login_user(user: UserLogin):
    """
    Login and return a token.
    """
    return user_manager.login(email=user.email, password=user.password)

@router.put("/apikey")
async def add_apikey(apikey_request: AddAPIKey, user: dict = Depends(TokenManager.get_current_user)):
    """
    Add User's API key; includes auth and rbac.
    """
    # Check roles
    RBACManager.require_role(user, ["user", "admin"])

    user_id = user.get("user_id")

    return user_manager.add_apikey(user_id=user_id, apikey=apikey_request.apikey)
