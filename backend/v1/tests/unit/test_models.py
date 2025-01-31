import pytest
from v1.shared.models import JobSearchRequest

"""
Parameterized Test: Validate JobSearchRequest Model
"""
@pytest.mark.parametrize("input_data, should_pass", [
    ({"query": "test", "location": "city"}, True), # Valid: query and location provided
    ({"search_id": "abc123"}, True),               # Valid: search_id provided
    ({}, False),                                   # Invalid: no query, location or search_id
    ({"query": "test"}, False),                    # Invalid: only query provided
    ({"location": "city"}, False),                 # Invalid: only location provided
    ({"query": "test", "location": "city", "search_id": "abc123"}, False),  # Invalid: query/location and search_id
])
def test_job_search_request_validation(input_data, should_pass):
    """
    Test: Valid and Invalid Inputs for JobSearchRequest
    """
    if should_pass:
         # Valid input should initialize successfully
        assert JobSearchRequest(**input_data)
    else:
        # Invalid input should raise ValueError
        with pytest.raises(ValueError):
            JobSearchRequest(**input_data)