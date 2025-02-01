import pytest
from passlib.hash import bcrypt
from v1.shared.user_manager import UserManager

@pytest.fixture
def mock_user_manager(mocker):
    """
    Fixture: Mock FirebaseManager and inject into UserManager
    """
    mock_firebase = mocker.Mock()
    return UserManager(mock_firebase)

def test_register_user(mock_user_manager, mocker):
    """
    Test: User registration
    """
    mock_user_manager.firebase_manager.store_data.return_value = {"message": "success"}
    
    # Call register method
    response = mock_user_manager.register("testuser", "test@example.com", "password123")
    
    # Assertions
    assert response["message"] == "User registered successfully"


def test_login_user(mock_user_manager, mocker):
    """
    Test: User login with valid credentials
    """
    hashed_password = bcrypt.hash("password123")
    mock_user_manager.firebase_manager.get_user_data.return_value = {
        "user_id": "123",
        "email": "test@example.com",
        "password_hash": hashed_password,
        "role": "user"
    }

    # Mock token creation
    mocker.patch("v1.shared.token_manager.TokenManager.create_access_token", return_value="mocked_token")
    
    # Call the login method
    response = mock_user_manager.login("test@example.com", "password123")
    
    # Assertions
    assert "access_token" in response
    assert response["access_token"] == "mocked_token"
    assert response["message"] == "Login successful"
    assert response["token_type"] == "bearer"