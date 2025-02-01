def test_register_endpoint(test_client):
    """
    Test: User register endpoint.
    """
    response = test_client.post("/v1/user/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User registered successfully"
    assert "user_id" in data

def test_login_endpoint(test_client):
    """
    Test: User login endpoint.
    """
    response = test_client.post("/v1/user/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert "access_token" in data