import app
import datetime
import pytest
from unittest import mock
from app.utils import date
from app import location
from app.services.location import jhu

DATETIME_STRING = "2020-03-17T10:23:22.505550"

def mocked_requests_get(*args, **kwargs):
    class FakeRequestsGetResponse:
        """
        Returns instance of `FakeRequestsGetResponse`
        when calling `app.services.location.jhu.requests.get()`
        """
        def __init__(self, url, filename, state):
            self.url = url
            self.filename = filename
            self.state = state
            self.text = self.read_file(self.state)

        def read_file(self, state):
            """
            Mock HTTP GET-method and return text from file
            """
            state = state.lower()

            # Determine filepath.
            filepath = "tests/example_data/time_series_covid19_{}_global".format(state)

            if state == 'recovered':
                filepath = 'tests/example_data/time_series_19-covid-Recovered.csv'

            # Return fake response.
            print("Try to read {}".format(filepath))
            with open(filepath, "r") as file:
                return file.read()

    #get url from `request.get`
    url = args[0]

    #get filename from url
    filename = url.split("/")[-1]

    #clean up for id token (e.g. Deaths)
    state = filename.split("-")[-1].replace(".csv", "").lower().capitalize()

    return FakeRequestsGetResponse(url, filename, state)

def mocked_strptime_isoformat(*args, **kwargs):
    class DateTimeStrpTime:
        """
        Returns instance of `DateTimeStrpTime`
        when calling `app.services.location.jhu.datetime.trptime(date, '%m/%d/%y').isoformat()`
        """
        def __init__(self, date, strformat):
            self.date = date
            self.strformat = strformat

        def isoformat(self):
            return datetime.datetime.strptime(self.date, self.strformat).isoformat()

    date = args[0]
    strformat = args[1]

    return DateTimeStrpTime(date, strformat)

@mock.patch('app.services.location.jhu.datetime')
@mock.patch('app.services.location.jhu.requests.get', side_effect=mocked_requests_get)
def test_get_locations(mock_request_get, mock_datetime):
    #mock app.services.location.jhu.datetime.utcnow().isoformat()
    mock_datetime.utcnow.return_value.isoformat.return_value = DATETIME_STRING
    mock_datetime.strptime.side_effect = mocked_strptime_isoformat

    output = jhu.get_locations()
    assert isinstance(output, list)
    assert isinstance(output[0], location.Location)

    #`jhu.get_locations()` creates id based on confirmed list
    location_confirmed = jhu.get_category("confirmed")
    assert len(output) == len(location_confirmed["locations"])
