import pytest
from v1.shared.firebase_manager import FirebaseManager

@pytest.fixture
def firebase_manager(mocker):
    """
    Fixture: Mock Firestore client instance
    """
    mock_db = mocker.patch("v1.shared.firebase_manager.FirebaseClient.get_instance")
    return FirebaseManager()

def test_store_data(firebase_manager, mocker):
    """
    Test: Store data in Firestore
    """
    # Mock Firestore document.set method
    mock_doc = mocker.Mock()
    firebase_manager.db.collection.return_value.document.return_value = mock_doc
    
    # Call store_data with params
    result = firebase_manager.store_data("test", "doc1", {"key": "value"})
    
    # Assertions
    mock_doc.set.assert_called_once_with({"key": "value"})
    assert result["message"] == "Data successfully stored"

def test_get_data(firebase_manager, mocker):
    """
    Test: Retrieve data from Firestore
    """
    # Mock Firestore's document.get method
    mock_doc = mocker.Mock()
    mock_doc.get.return_value.to_dict.return_value = {"key": "value"}
    firebase_manager.db.collection.return_value.document.return_value = mock_doc

    # Call get_data with params
    result = firebase_manager.get_data("test", "doc1")

    # Assertions
    assert result == {"key": "value"}