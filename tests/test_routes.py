import unittest
from unittest import mock

import app

from .test_data import mocked_requests_get


@mock.patch('app.data.requests.get', side_effect=mocked_requests_get)
@mock.patch('app.data.datetime')
class FlaskRoutesTest(unittest.TestCase):
    """
    Need to mock some objects to control testing data locally
    """

    #load app context only once
    app = app.create_app()

    def setUp(self):
        self.client = FlaskRoutesTest.app.test_client()

    def test_app_route_recovered(self, mock_datetime, mock_get):
        """
        :param mock_datetime: mock.Mock, Mocking object for module path app.data.datetime
        :param mock_get: mock.Mock, Mocking object for module path app.data.requests.get
        """
        #mocked datetime based on `last_updated` of expected_output/data_{state}.json
        #datetime value need to be equal due to caching
        mock_datetime.utcnow.return_value.isoformat.return_value = "2020-03-17T10:02:01.285418"
        state = "recovered"
        filepath = "tests/expected_output/data_{state}.json".format(state=state)
        with open(filepath, "r") as file:
            expected_json_output = file.read()

        output_data = self.client.get("/{}".format(state)).data.decode()

        assert output_data == expected_json_output

    def test_app_route_deaths(self, mock_datetime, mock_get):
        #mocked datetime based on `last_updated` of expected_output/data_{state}.json
        #datetime value need to be equal due to caching
        mock_datetime.utcnow.return_value.isoformat.return_value = "2020-03-17T10:23:22.505550"
        state = "deaths"
        filepath = "tests/expected_output/data_{state}.json".format(state=state)
        with open(filepath, "r") as file:
            expected_json_output = file.read()

        output_data = self.client.get("/{}".format(state)).data.decode()

        assert output_data == expected_json_output

    def test_app_route_confirmed(self, mock_datetime, mock_get):
        #mocked datetime based on `last_updated` of expected_output/data_{state}.json
        #datetime value need to be equal due to caching
        mock_datetime.utcnow.return_value.isoformat.return_value = "2020-03-17T10:02:01.285418"
        state = "confirmed"
        filepath = "tests/expected_output/data_{state}.json".format(state=state)
        with open(filepath, "r") as file:
            expected_json_output = file.read()

        output_data = self.client.get("/{}".format(state)).data.decode()

        assert output_data == expected_json_output

    def tearDown(self):
        pass
