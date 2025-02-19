import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


# Importing route handlers
from backend.v1.endpoints.users import router as users_router
from backend.v1.endpoints.search import router as search_router
from backend.v1.endpoints.test_routes import router as test_router
from backend.v1.endpoints.application import router as application_router

# Initialize the FastAPI app
app = FastAPI(
    title="Job Search Gamification API",
    description="MVP version support",
    version="1.0.0",
)

# Setting Favicon 
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Include V1 API routers
app.include_router(users_router, prefix="/v1/user", tags=["users"])
app.include_router(search_router, prefix="/v1/search", tags=["search"])
app.include_router(test_router, prefix="/v1/test", tags=["test"])
app.include_router(application_router, prefix="/v1/application", tags=["application"])

# Enable CORS (important if frontend calls the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://asp-final-project.onrender.com/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 in case PORT is missing
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


