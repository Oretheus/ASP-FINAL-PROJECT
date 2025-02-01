import pytest
from v1.shared.api_manager import APIManager

@pytest.fixture
def api_manager():
    """
    Fixture: Mock APIManager instance
    """
    return APIManager()

def test_fetch_jobs(api_manager, mocker):
    """
    Test: fetch_jobs with mock API response
    """
    # Mock response returned by requests.get
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "jobs_results": [{"job_id": "1"}],
        "serpapi_pagination": {"next_page_token": "page_token_abc"}
    }
   
    # Patch requests.get method to return the mocked response
    mocker.patch("requests.get", return_value=mock_response)
    
    # Call fetch_jobs with mock parameters
    result = api_manager.fetch_jobs("dummy_key", "query", "location")
    
    # Assertions
    assert result["jobs"] == [{"job_id": "1"}]
    assert result["next_page_token"] == "page_token_abc"