import os
import uvicorn
from fastapi import FastAPI

# Attempting to correct imports
from backend.v1.endpoints.users import router as users_router
from backend.v1.endpoints.search import router as search_router

# Initialize the app
app = FastAPI(
    title="Job Search Gamification API",
    description="MVP version support",
    version="1.0.0",
)

# V1 routes
app.include_router(users_router, prefix="/v1/user", tags=["users"])
app.include_router(search_router, prefix="/v1/search", tags=["search"])

# Root endpoint (Added methods)
@app.get("/") 
async def root():
    """
    Root endpoint to confirm API is running.
    """
    return {
        "message": "Welcome to the Job Search Gamification API!",
        "available_versions": ["v1"], #["v1", "v2"],
        "documentation_url": "/docs",
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render provides PORT env variable
    uvicorn.run(app, host="0.0.0.0", port=port)
