from fastapi import APIRouter, HTTPException, Depends
from backend.v1.shared.firebase_manager import FirebaseManager
from backend.v1.shared.token_manager import TokenManager

router = APIRouter()
firebase_manager = FirebaseManager()

# Save application
@router.post("/save/{job_id}")
async def save_application(job_id: str, user: dict = Depends(TokenManager.get_current_user)):
    """Save a job listing"""
    user_id = user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized user.")
    return await firebase_manager.save_application(user_id, job_id)

# Update application status
@router.put("/update/{application_id}")
async def update_application_status(application_id: str, new_status: str, comments: str, user: dict = Depends(TokenManager.get_current_user)):
    """Update the status of an application"""
    user_id = user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized user.")
    return await firebase_manager.update_application_status(application_id, new_status, comments)

# Get application status
@router.get("/details/{application_id}")
async def view_application_details(application_id: str, user: dict = Depends(TokenManager.get_current_user)):
    """Get application details."""
    user_id = user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized user.")
    
    application_doc, job_doc = await firebase_manager.get_application_details(application_id)
    return {
        "application": application_doc,
        "job": job_doc
    }

# Delete application
@router.get("/delete/{application_id}")
async def delete_application(application_id: str, user: dict = Depends(TokenManager.get_current_user)):
    """Delete application"""
    user_id = user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized user.")
    return await firebase_manager.delete_application(application_id)

# Retrieve all applications for a user
@router.get("/user/{user_id}")
async def view_user_applications(user_id: str, user: dict = Depends(TokenManager.get_current_user)):
    """Retrieve all applications for a user."""
    user_id = user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized user.")
    return await firebase_manager.get_user_applications(user_id)