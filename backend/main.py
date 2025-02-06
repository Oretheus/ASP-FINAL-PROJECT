from fastapi import FastAPI

# Attempting absolute imports
from backend.v1.endpoints.users import users
from backend.v1.endpoints.search import search

# Initialize the app
app = FastAPI(
    title="Job Search Gamification API",
    description="MVP version support",
    version="1.0.0",
)

# V1 routes
app.include_router(users, prefix="/v1/user", tags=["users"])
app.include_router(search, prefix="/v1/search", tags=["search"])

# Root endpoint
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
