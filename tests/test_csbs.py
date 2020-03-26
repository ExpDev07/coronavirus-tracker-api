import datetime
from unittest import mock

import pytest

import app
from app.services.location import csbs


def mocked_csbs_requests_get(*args, **kwargs):
    class FakeRequestsGetResponse:
        """
        Returns instance of `FakeRequestsGetResponse`
        when calling `app.services.location.csbs.requests.get()
        """

        def __init__(self):
            self.text = self.read_file()

        def read_file(self):
            """
            Mock HTTP GET-method and return text from file
            """
            filepath = "tests/example_data/sample_covid19_county.csv"
            print("Try to read {}".format(filepath))
            with open(filepath, "r") as file:
                return file.read()

    return FakeRequestsGetResponse()


@mock.patch("app.services.location.csbs.requests.get", side_effect=mocked_csbs_requests_get)
def test_get_locations(mock_request_get):
    data = csbs.get_locations()
    assert isinstance(data, list)

    # check to see that Unknown/Unassigned has been filtered
    for d in data:
        assert d.county != "Unknown"
        assert d.county != "Unassigned"
