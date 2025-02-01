from fastapi import APIRouter, HTTPException, Depends
from v1.shared.firebase_manager import FirebaseManager
from v1.shared.api_manager import APIManager
from v1.shared.search_manager import SearchManager
from v1.shared.models import JobSearchRequest
from v1.shared.token_manager import TokenManager
from v1.shared.rbac_manager import RBACManager

router = APIRouter()
firebase_manager = FirebaseManager()
api_manager = APIManager()
search_manager = SearchManager(firebase_manager, api_manager)

@router.post("/jobs")
async def search_jobs(search_request: JobSearchRequest, user: dict = Depends(TokenManager.get_current_user)):
    """
    Search jobs endpoints; includes auth and rbac.
    """
    # Get user_id from the token
    user_id = user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid user data")

    # Check roles
    RBACManager.require_role(user, ["user", "admin"])

    if search_request.search_id:
        # Handle pagination
        return search_manager.paginate_search(user_id, search_request.search_id)
    else:
        # Handle initial search
        return search_manager.start_search(
            user_id,
            search_request.query,
            search_request.location,
        )