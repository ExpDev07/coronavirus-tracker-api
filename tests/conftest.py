"""
tests.conftest.py

Global conftest file for shared pytest fixtures
"""
import pytest
from fastapi.testclient import TestClient


from app.main import APP


@pytest.fixture
def api_client():
    """
    Returns a TestClient.
    The test client uses the requests library for making http requests.
    """
    return TestClient(APP)
