from fastapi import HTTPException
from backend.v1.shared.api_manager import APIManager

class SearchManager:
    def __init__(self, firebase_manager, api_manager):
        self.firebase_manager = firebase_manager
        self.api_manager = api_manager

    async def start_search(self, user_id: str, query: str, location: str):
        """
        Perform the initial job search.
        """
        user_data = await self.firebase_manager.get_data("users", user_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        # Fetch the first page of results
        result = await self.api_manager.fetch_jobs(
            query=query,
            location=location,
        )

        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result["error"])

        jobs = result.get("jobs", [])
        next_page_token = result.get("next_page_token")

        if not jobs:
            raise HTTPException(status_code=404, detail="No jobs found.")

        # Store jobs
        job_ids = []
        for job in jobs:
            job_id = job.get('job_id')
            if not job_id:
                raise HTTPException(status_code=500, detail="Missing job_id in result data.")
            await self.firebase_manager.store_job(job_id, job)
            job_ids.append(job_id)

        # Log search and save next_page_token
        search_id = await self.firebase_manager.store_user_search(
            user_id=user_id,
            query=query,
            location=location,
            job_ids=job_ids,
            next_page_token=next_page_token,
        )

        return {
            "message": "Initial Search - Search results retrieved successfully.",
            "search_id": search_id,
            "results": job_ids,
            "next_page_token": next_page_token,
        }

    async def paginate_search(self, user_id: str, search_id: str):
        """
        Handle pagination for an existing search.
        """
        search_data = await self.firebase_manager.get_data("user_searches", search_id)
        if not search_data:
            raise HTTPException(status_code=404, detail="Search ID not found")

        next_page_token = search_data.get("next_page_token")
        if not next_page_token:
            raise HTTPException(status_code=400, detail="No more results available")

        user_data = await self.firebase_manager.get_data("users", user_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        # Fetch next page of results
        result = await self.api_manager.fetch_jobs(
            query=search_data["query"],
            location=search_data["location"],
            next_page_token=next_page_token,
        )

        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result["error"])

        # Store each job
        jobs = result.get("jobs", [])
        job_ids = []
        for job in jobs:
            job_id = job.get('job_id')
            if not job_id:
                raise HTTPException(status_code=500, detail="Missing job_id in result data.")
            await self.firebase_manager.store_job(job_id, job)
            job_ids.append(job_id)

        # Update search record with new job_ids
        search_data["job_ids"].extend(job_ids)
        new_token = result.get("next_page_token")
        search_data["next_page_token"] = new_token
        await self.firebase_manager.store_data("user_searches", search_id, search_data)

        return {
            "message": "Pagination results retrieved successfully.",
            "search_id": search_id,
            "results": job_ids,
            "next_page_token": new_token,
        }
