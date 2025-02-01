import sys
import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

# Add the backend dir to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from main import app
from v1.shared.token_manager import TokenManager

# Load the test env variables
load_dotenv(dotenv_path="v1/tests/.env.test")

@pytest.fixture
def test_client():
    return TestClient(app)