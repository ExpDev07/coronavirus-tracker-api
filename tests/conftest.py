"""
tests.conftest.py

Global conftest file for shared pytest fixtures
"""
import pytest
from fastapi.testclient import TestClient
from async_asgi_testclient import TestClient as AsyncTestClient

from app.main import APP


@pytest.fixture
def api_client():
    """
    Returns a fastapi.testclient.TestClient.
    The test client uses the requests library for making http requests.
    """
    return TestClient(APP)


@pytest.fixture
async def async_api_client():
    """
    Returns an async_asgi_testclient.TestClient.
    """
    return AsyncTestClient(APP)
