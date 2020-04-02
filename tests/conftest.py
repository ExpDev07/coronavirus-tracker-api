"""
tests.conftest.py

Global conftest file for shared pytest fixtures
"""
import datetime
import os
from contextlib import asynccontextmanager
from unittest import mock

import pytest
from async_asgi_testclient import TestClient as AsyncTestClient
from fastapi.testclient import TestClient

from app.main import APP
from app.utils import httputils


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


class DateTimeStrpTime:
    """Returns instance of `DateTimeStrpTime`
    when calling `app.services.location.jhu.datetime.trptime(date, '%m/%d/%y').isoformat()`.
    """

    def __init__(self, date, strformat):
        self.date = date
        self.strformat = strformat

    def isoformat(self):
        return datetime.datetime.strptime(self.date, self.strformat).isoformat()


class FakeRequestsGetResponse:
    """Fake instance of a response from `aiohttp.ClientSession.get`.
    """

    def __init__(self, url, filename, state):
        self.url = url
        self.filename = filename
        self.state = state

    async def text(self):
        return self.read_file(self.state)

    def read_file(self, state):
        """
        Mock HTTP GET-method and return text from file
        """
        state = state.lower()

        # Determine filepath.
        filepath = os.path.join(os.path.dirname(__file__), "example_data/{}.csv".format(state))

        # Return fake response.
        print("Try to read {}".format(filepath))
        with open(filepath, "r") as file:
            return file.read()


@asynccontextmanager
async def mock_client_session():
    """Context manager that replaces the global client_session with an AsyncMock instance.

    :Example:

    >>> async with mock_client_session() as mocked_client_session:
    >>>     mocked_client_session.get = mocked_session_get
    >>>     # test code...

    """

    httputils.client_session = mocked_client_session = mock.AsyncMock()
    try:
        yield mocked_client_session
    finally:
        del httputils.client_session


@asynccontextmanager
async def mocked_session_get(*args, **kwargs):
    """Mock response from client_session.get.
    """

    url = args[0]
    filename = url.split("/")[-1]

    # clean up for id token (e.g. Deaths)
    state = filename.split("-")[-1].replace(".csv", "").lower().capitalize()

    yield FakeRequestsGetResponse(url, filename, state)


def mocked_strptime_isoformat(*args, **kwargs):
    """Mock return value from datetime.strptime().isoformat().
    """

    date = args[0]
    strformat = args[1]

    return DateTimeStrpTime(date, strformat)
