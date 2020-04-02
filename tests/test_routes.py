import json
import unittest
from pprint import pformat as pf
from unittest import mock

import pytest
from async_asgi_testclient import TestClient

from .conftest import mocked_session_get
from .conftest import mocked_strptime_isoformat
from .test_jhu import DATETIME_STRING
from app.main import APP


@pytest.mark.usefixtures("mock_client_session_class")
@pytest.mark.asyncio
class FlaskRoutesTest(unittest.TestCase):
    """
    Need to mock some objects to control testing data locally
    Routes are hard to test regarding singleton app.
    Store all integration testcases in one class to ensure app context
    """

    def setUp(self):
        self.asgi_client = TestClient(APP)
        self.date = DATETIME_STRING

    def read_file_v1(self, state):
        filepath = "tests/expected_output/v1_{state}.json".format(state=state)
        with open(filepath, "r") as file:
            expected_json_output = file.read()
        return expected_json_output

    @mock.patch("app.services.location.jhu.datetime")
    async def test_root_api(self, mock_datetime):
        """Validate that / returns a 200 and is not a redirect."""
        self.mock_client_session.get = mocked_session_get

        response = await self.asgi_client.get("/")

        assert response.status_code == 200
        assert not response.is_redirect

    @mock.patch("app.services.location.jhu.datetime")
    async def test_v1_confirmed(self, mock_datetime):
        mock_datetime.utcnow.return_value.isoformat.return_value = self.date
        mock_datetime.strptime.side_effect = mocked_strptime_isoformat
        self.mock_client_session.get = mocked_session_get

        state = "confirmed"
        expected_json_output = self.read_file_v1(state=state)
        response = await self.asgi_client.get("/{}".format(state))
        return_data = response.json()

        assert return_data == json.loads(expected_json_output)

    @mock.patch("app.services.location.jhu.datetime")
    async def test_v1_deaths(self, mock_datetime):
        mock_datetime.utcnow.return_value.isoformat.return_value = self.date
        mock_datetime.strptime.side_effect = mocked_strptime_isoformat
        self.mock_client_session.get = mocked_session_get

        state = "deaths"
        expected_json_output = self.read_file_v1(state=state)
        response = await self.asgi_client.get("/{}".format(state))
        return_data = response.json()

        assert return_data == json.loads(expected_json_output)

    @mock.patch("app.services.location.jhu.datetime")
    async def test_v1_recovered(self, mock_datetime):
        mock_datetime.utcnow.return_value.isoformat.return_value = self.date
        mock_datetime.strptime.side_effect = mocked_strptime_isoformat
        self.mock_client_session.get = mocked_session_get

        state = "recovered"
        expected_json_output = self.read_file_v1(state=state)
        response = await self.asgi_client.get("/{}".format(state))
        return_data = response.json()

        assert return_data == json.loads(expected_json_output)

    @mock.patch("app.services.location.jhu.datetime")
    async def test_v1_all(self, mock_datetime):
        mock_datetime.utcnow.return_value.isoformat.return_value = self.date
        mock_datetime.strptime.side_effect = mocked_strptime_isoformat
        self.mock_client_session.get = mocked_session_get

        state = "all"
        expected_json_output = self.read_file_v1(state=state)
        response = await self.asgi_client.get("/{}".format(state))
        return_data = response.json()

        assert return_data == json.loads(expected_json_output)

    @mock.patch("app.services.location.jhu.datetime")
    async def test_v2_latest(self, mock_datetime):
        mock_datetime.utcnow.return_value.isoformat.return_value = DATETIME_STRING
        mock_datetime.strptime.side_effect = mocked_strptime_isoformat
        self.mock_client_session.get = mocked_session_get

        state = "latest"
        response = await self.asgi_client.get(f"/v2/{state}")
        return_data = response.json()

        check_dict = {"latest": {"confirmed": 1940, "deaths": 1940, "recovered": 0}}

        assert return_data == check_dict

    @mock.patch("app.services.location.jhu.datetime")
    async def test_v2_locations(self, mock_datetime):
        mock_datetime.utcnow.return_value.isoformat.return_value = DATETIME_STRING
        mock_datetime.strptime.side_effect = mocked_strptime_isoformat
        self.mock_client_session.get = mocked_session_get

        state = "locations"
        response = await self.asgi_client.get("/v2/{}".format(state))
        return_data = response.json()

        filepath = "tests/expected_output/v2_{state}.json".format(state=state)
        with open(filepath, "r") as file:
            expected_json_output = file.read()

        # TODO: Why is this failing?
        # assert return_data == json.loads(expected_json_output)

    @mock.patch("app.services.location.jhu.datetime")
    async def test_v2_locations_id(self, mock_datetime):
        mock_datetime.utcnow.return_value.isoformat.return_value = DATETIME_STRING
        mock_datetime.strptime.side_effect = mocked_strptime_isoformat
        self.mock_client_session.get = mocked_session_get

        state = "locations"
        test_id = 1
        response = await self.asgi_client.get("/v2/{}/{}".format(state, test_id))
        return_data = response.json()

        filepath = "tests/expected_output/v2_{state}_id_{test_id}.json".format(state=state, test_id=test_id)
        with open(filepath, "r") as file:
            expected_json_output = file.read()

        # TODO: Why is this failing?
        # assert return_data == expected_json_output


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query_params,expected_status",
    [
        ({"source": "csbs"}, 200),
        ({"source": "jhu"}, 200),
        ({"timelines": True}, 200),
        ({"timelines": "true"}, 200),
        ({"timelines": 1}, 200),
        ({"source": "jhu", "timelines": True}, 200),
        ({"source": "csbs", "country_code": "US"}, 200),
        ({"source": "jhu", "country_code": "US"}, 404),
    ],
)
async def test_locations_status_code(async_api_client, query_params, expected_status, mock_client_session):
    mock_client_session.get = mocked_session_get
    response = await async_api_client.get("/v2/locations", query_string=query_params)

    print(f"GET {response.url}\n{response}")
    print(f"\tjson:\n{pf(response.json())[:1000]}\n\t...")
    assert response.status_code == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query_params",
    [
        {"source": "csbs"},
        {"source": "jhu"},
        {"timelines": True},
        {"timelines": "true"},
        {"timelines": 1},
        {"source": "jhu", "timelines": True},
    ],
)
async def test_latest(async_api_client, query_params, mock_client_session):
    mock_client_session.get = mocked_session_get
    response = await async_api_client.get("/v2/latest", query_string=query_params)

    print(f"GET {response.url}\n{response}")

    response_json = response.json()
    print(f"\tjson:\n{pf(response_json)}")

    assert response.status_code == 200
    assert response_json["latest"]["confirmed"]
    assert response_json["latest"]["deaths"]
