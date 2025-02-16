from pydantic import BaseModel, Field, model_validator
from typing import Optional

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[str] = "user" # Default role

class AddAPIKey(BaseModel):
    apikey: str

class JobSearchRequest(BaseModel):
    query: Optional[str] = Field(default=None, description="Search query for jobs")
    location: Optional[str] = Field(default=None, description="Location for the search")
    search_id: Optional[str] = Field(default=None, description="Search ID for pagination.")

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, values):
        """
        Validation for job search requests.

        Rules:
        - New Search: `query` and `location` are required if `search_id` is missing.
        - Pagination: Only `search_id` is allowed when fetching additional results.

        Examples:
        - New Search: {"query": "Software Engineer", "location": "New York"}
        - Pagination: {"search_id": "abc123"}
        """

        query, location, search_id = values.get("query"), values.get("location"), values.get("search_id")

        if not search_id and (not query or not location):
            raise ValueError("Query and location are required for a new search when search_id is not provided.")

        if search_id and (query or location):
            raise ValueError("Query and location must not be provided when search_id is present.")

        return values