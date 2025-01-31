from fastapi import FastAPI
from v1.endpoints import users, search

# Initialize the app
app = FastAPI(
    title="Job Search Gamification API",
    description="MVP version support",
    version="1.0.0",
)

# V1 routes
app.include_router(users.router, prefix="/v1/user", tags=["users"])
app.include_router(search.router, prefix="/v1/search", tags=["search"])

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