import os
import uvicorn
from fastapi import FastAPI

# Importing route handlers
from backend.v1.endpoints.users import router as users_router
from backend.v1.endpoints.search import router as search_router

# Initialize the FastAPI app
app = FastAPI(
    title="Job Search Gamification API",
    description="MVP version support",
    version="1.0.0",
)

# Include V1 API routers
app.include_router(users_router, prefix="/v1/user", tags=["users"])
app.include_router(search_router, prefix="/v1/search", tags=["search"])

# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    """
    Root endpoint to confirm API is running.
    """
    return {
        "message": "Welcome to the Job Search Gamification API!",
        "available_versions": ["v1"],
        "documentation_url": "/docs",
    }

# Explicitly handle HEAD requests to avoid 405 errors
@app.head("/")
async def head_root():
    """
    Handles HEAD requests for the root endpoint.
    """
    return {}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render provides PORT env variable
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="debug")
