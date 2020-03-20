import app
import datetime
import pytest
from unittest import mock
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

@mock.patch('app.services.location.csbs.requests.get', side_effect=mocked_csbs_requests_get)
def test_get_locations(mock_request_get):
    data = csbs.get_locations()
    assert isinstance(data, dict)
    assert isinstance(data["Washington"], list)
    assert data.get("Wisconsin") == None

    # check to see that Unknown/Unassigned has been filtered
    for state in data:
        for county in data[state]:
            assert county.county != "Unknown"
            assert county.county != "Unassigned"