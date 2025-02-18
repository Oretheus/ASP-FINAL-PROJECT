import requests

class APIManager:
    def __init__(self):
        # Retrieve API key from render env secrets variable
        self.api_key = os.getenv("SERP_API_KEY")
        if not self.api_key:
            raise ValueError("Missing SERP_API_KEY in Render env variable.")

    def fetch_jobs(self, query, location, next_page_token=None):
        """
        Fetch job listings from SerpApi - Google Jobs Api
        """
        try:
            # Endpoints URL with parameters
            url = "https://serpapi.com/search"
            params = {
                "engine": "google_jobs",
                "q": query,
                "location": location,
                "api_key": self.apikey,
                "hl": "en",
                "gl": "ca",
            }

            # Add pagination token if provided
            if next_page_token:
                params["next_page_token"] = next_page_token

            # Make API request
            response = requests.get(url, params=params)
            response.raise_for_status()

            # Parse response JSON
            data = response.json()
            next_page_token = data.get("serpapi_pagination", {}).get("next_page_token")
            jobs = data.get("jobs_results", [])

            return {
                "jobs": jobs,
                "next_page_token": next_page_token,
                "status": "success" if jobs else "no_results",
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}