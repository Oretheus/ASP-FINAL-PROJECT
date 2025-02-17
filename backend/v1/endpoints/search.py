from fastapi import APIRouter, HTTPException, Depends
from backend.v1.shared.firebase_manager import FirebaseManager
from backend.v1.shared.api_manager import APIManager
from backend.v1.shared.search_manager import SearchManager
from backend.v1.shared.models import JobSearchRequest
from backend.v1.shared.token_manager import TokenManager
from backend.v1.shared.rbac_manager import RBACManager

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

@router.get("/job/{job_id}")
async def get_job_details(job_id: str, user: dict = Depends(TokenManager.get_current_user)):
    """
    Fetch job details by job_id.
    """
    # Check roles
    RBACManager.require_role(user, ["user", "admin"])

    # Fetch job from Firebase
    job_data = firebase_manager.fetch_job(job_id)
    if "error" in job_data:
        raise HTTPException(status_code=404, detail=job_data["error"])

    return {"job_id": job_id, "job_details": job_data}