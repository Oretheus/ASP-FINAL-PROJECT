def test_search_jobs_endpoint(test_client):
    """
    Test the search jobs endpoint with actual test user.
    """
    # Log in to get an access token
    login_response = test_client.post("/v1/user/login", json={
        "email": "email@email.com",
        "password": "password123"
    })
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    token = login_data["access_token"]
    
    # Search for jobs using the token
    headers = {"Authorization": f"Bearer {token}"}
    search_response = test_client.post("/v1/search/jobs", json={
        "query": "Software Engineer",
        "location": "New York"
    }, headers=headers)
    
    # Assertions
    assert search_response.status_code == 200

def test_paginate_jobs_endpoint(test_client):
    """
    Test the pagination search jobs endpoint with actual search record id
    """
    # Log in to get an access token
    login_response = test_client.post("/v1/user/login", json={
        "email": "email@email.com",
        "password": "password123"
    })
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    token = login_data["access_token"]
    
    # Search pagination
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.post("/v1/search/jobs", json={"search_id": "03f88f03-b3d9-464d-9091-b1d3da589956"}, headers=headers)
    
    # Assertions
    assert response.status_code == 200