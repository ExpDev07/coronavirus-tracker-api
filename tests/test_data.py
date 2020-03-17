from unittest import mock
import pytest

from app import data
from app.utils import date

"""
Todo:
    * More separation of test case `test_data_parsing`
"""

def mocked_requests_get(*args, **kwargs):
    class TestResponse:
        def __init__(self, state):
            self.text = self.read_file(state)

        def read_file(self, state):
            """
            Mock HTTP GET-method and return text from file
            """
            filepath = "tests/example_data/time_series_19-covid-{}.csv".format(state)
            print("Try to read {}".format(filepath))
            with open(filepath, "r") as file:
                return file.read()

    filename = args[0].split("/")[-1]
    #clean up for token (e.g. Deaths)
    filename = filename.split("-")[-1].replace(".csv", "")

    return TestResponse(filename)

@pytest.mark.parametrize("state, datetime_str",
                         [("recovered", "2020-03-17T10:02:01.285418"),
                          ("deaths", "2020-03-17T10:23:22.505550"),
                          ("confirmed", "2020-03-17T10:02:01.285418")])
@mock.patch('app.data.requests.get', side_effect=mocked_requests_get)
@mock.patch('app.data.datetime')
def test_data_parsing(mock_datetime, mock_get, state, datetime_str):
    """`data.get_data` sets current datentime via `utcnow()`
        Control datetime for testing
        Mocked datetime based on `last_updated` of expected_output/data_{state}.json
        #datetime value need to be equal due to caching
    """
    mock_datetime.utcnow.return_value.isoformat.return_value = datetime_str
    output = data.get_data(state)

    #simple schema validation
    assert output["source"] == "https://github.com/ExpDev07/coronavirus-tracker-api"
    assert isinstance(output["latest"], int)
    #check for valid datestring
    assert date.is_date(output["last_updated"]) is True
    #ensure date formating
    assert output["last_updated"] == datetime_str + "Z"
    #validate location schema
    location_entry = output["locations"][0]

    assert isinstance(location_entry["country"], str)
    assert isinstance(location_entry["country_code"], str)
    assert len(location_entry["country_code"]) == 2
    assert isinstance(location_entry["province"], str)
    assert isinstance(location_entry["latest"], int)

    #validate coordinates in location
    coordinates = location_entry["coordinates"]
    assert isinstance(coordinates["lat"], str)
    assert isinstance(coordinates["long"], str)

    #validate history in location
    history = location_entry["history"]
    assert date.is_date(list(history.keys())[0]) is True
    assert isinstance(list(history.values())[0], int)
