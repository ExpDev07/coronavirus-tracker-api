import json
import unittest
from pprint import pformat as pf
from unittest import mock

import pytest
from fastapi.testclient import TestClient

# import app
# from app import services
from app.main import APP

from .test_jhu import DATETIME_STRING, mocked_requests_get, mocked_strptime_isoformat


def format_json(s):
    return json.dumps(json.loads(s), indent=4, sort_keys=True)

def do_test_v1(obj, state, mock_request_get, mock_datetime):
    "Formatted json-strings make debugging easier"
    mock_datetime.utcnow.return_value.isoformat.return_value = obj.date
    mock_datetime.strptime.side_effect = mocked_strptime_isoformat

    json_ret = obj.asgi_client.get("/{}".format(state)).json()
    ret = str(json_ret).replace("\'", "\"")

    filepath = "tests/expected_output/v1_{state}.json".format(state=state)
    with open(filepath, "r") as file:
        exp = file.read()

    assert format_json(ret) == format_json(exp)


@mock.patch("app.services.location.jhu.datetime")
@mock.patch("app.services.location.jhu.requests.get", side_effect=mocked_requests_get)
class FlaskRoutesTest(unittest.TestCase):
    """
    Need to mock some objects to control testing data locally
    Routes are hard to test regarding singleton app.
    Store all integration testcases in one class to ensure app context
    """

    def setUp(self):
        self.asgi_client = TestClient(APP)
        self.date = DATETIME_STRING

    def test_root_api(self, mock_request_get, mock_datetime):
        """Validate that / returns a 200 and is not a redirect."""
        response = self.asgi_client.get("/")

        assert response.status_code == 200
        assert not response.is_redirect

    def test_v1_confirmed(self, mock_request_get, mock_datetime):
        do_test_v1(self, "confirmed", mock_request_get, mock_datetime)

    def test_v1_deaths(self, mock_request_get, mock_datetime):
        do_test_v1(self, "deaths", mock_request_get, mock_datetime)

    def test_v1_recovered(self, mock_request_get, mock_datetime):
        do_test_v1(self, "recovered", mock_request_get, mock_datetime)

    def test_v1_all(self, mock_request_get, mock_datetime):
        do_test_v1(self, "all", mock_request_get, mock_datetime)

    def test_v2_latest(self, mock_request_get, mock_datetime):
        mock_datetime.utcnow.return_value.isoformat.return_value = DATETIME_STRING
        mock_datetime.strptime.side_effect = mocked_strptime_isoformat
        state = "latest"
        return_data = self.asgi_client.get(f"/v2/{state}").json()
        check_dict = {"latest": {"confirmed": 1940, "deaths": 1940, "recovered": 0}}
        assert return_data == check_dict

    def test_v2_locations(self, mock_request_get, mock_datetime):
        mock_datetime.utcnow.return_value.isoformat.return_value = DATETIME_STRING
        mock_datetime.strptime.side_effect = mocked_strptime_isoformat
        state = "locations"
        return_data = self.asgi_client.get("/v2/{}".format(state)).json()

        filepath = "tests/expected_output/v2_{state}.json".format(state=state)
        with open(filepath, "r") as file:
            data_read = file.read()

    def test_v2_locations_id(self, mock_request_get, mock_datetime):
        mock_datetime.utcnow.return_value.isoformat.return_value = DATETIME_STRING
        mock_datetime.strptime.side_effect = mocked_strptime_isoformat

        state = "locations"
        test_id = 1
        return_data = self.asgi_client.get("/v2/{}/{}".format(state, test_id)).json()

        filepath = "tests/expected_output/v2_{state}_id_{test_id}.json".format(state=state, test_id=test_id)
        with open(filepath, "r") as file:
            data_read = file.read()

    def tearDown(self):
        pass


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
def test_locations_status_code(api_client, query_params, expected_status):
    response = api_client.get("/v2/locations", params=query_params)
    print(f"GET {response.url}\n{response}")
    print(f"\tjson:\n{pf(response.json())[:1000]}\n\t...")
    assert response.status_code == expected_status


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
def test_latest(api_client, query_params):
    response = api_client.get("/v2/latest", params=query_params)
    print(f"GET {response.url}\n{response}")

    response_json = response.json()
    print(f"\tjson:\n{pf(response_json)}")

    assert response.status_code == 200
    assert response_json["latest"]["confirmed"]
    assert response_json["latest"]["deaths"]
