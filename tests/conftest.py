"""
tests.conftest.py

Global conftest file for shared pytest fixtures
"""
import pytest

from app.main import APP
from fastapi.testclient import TestClient


@pytest.fixture
def api_client():
    """
    Returns a TestClient.
    The test client uses the requests library for making http requests.
    """
    return TestClient(APP)
