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
            filepath = "tests/example_data/time_series_19-covid-Time_series_covid19_{}_global.csv".format(state.lower())

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

@pytest.mark.parametrize("category, capitalize_category", [
                            ("deaths", "Deaths"),
                            ("recovered", "Recovered"),
                            ("confirmed", "Confirmed")])
@mock.patch('app.services.location.jhu.requests.get', side_effect=mocked_requests_get)
def test_validate_category(mock_request_get, category, capitalize_category):
    base_url = 'https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-%s.csv'
    request = app.services.location.jhu.requests.get(base_url % category)
    
    assert request.state == capitalize_category

@pytest.mark.parametrize("category, datetime_str, latest_value, country_name, \
                          country_code, province, latest_country_value, \
                          coordinate_lat, coordinate_long",
                         [("deaths", DATETIME_STRING, 1940, "Thailand", "TH", "",
                           114, "15", "101"),
                          ("recovered", DATETIME_STRING, 1940, "Thailand", "TH", "",
                           114, "15", "101"),
                          ("confirmed", DATETIME_STRING, 1940, "Thailand", "TH", "",
                           114, "15", "101")])
@mock.patch('app.services.location.jhu.datetime')
@mock.patch('app.services.location.jhu.requests.get', side_effect=mocked_requests_get)
def test_get_category(mock_request_get, mock_datetime, category, datetime_str,
                      latest_value, country_name, country_code, province, latest_country_value,
                      coordinate_lat, coordinate_long):
    #mock app.services.location.jhu.datetime.utcnow().isoformat()
    mock_datetime.utcnow.return_value.isoformat.return_value = datetime_str
    output = jhu.get_category(category)

    #simple schema validation
    assert output["source"] == "https://github.com/ExpDev07/coronavirus-tracker-api"

    assert isinstance(output["latest"], int)
    assert output["latest"] == latest_value #based on example data

    #check for valid datestring
    assert date.is_date(output["last_updated"]) is True
    #ensure date formating
    assert output["last_updated"] == datetime_str + "Z" #based on example data

    #validate location schema
    location_entry = output["locations"][0]

    assert isinstance(location_entry["country"], str)
    assert location_entry["country"] == country_name #based on example data

    assert isinstance(location_entry["country_code"], str)
    assert len(location_entry["country_code"]) == 2
    assert location_entry["country_code"] == country_code #based on example data

    assert isinstance(location_entry["province"], str)
    assert location_entry["province"] == province #based on example data

    assert isinstance(location_entry["latest"], int)
    assert location_entry["latest"] == latest_country_value #based on example data

    #validate coordinates in location
    coordinates = location_entry["coordinates"]

    assert isinstance(coordinates["lat"], str)
    assert coordinates["lat"] == coordinate_lat

    assert isinstance(coordinates["long"], str)
    assert coordinates["long"] == coordinate_long

    #validate history in location
    history = location_entry["history"]
    assert date.is_date(list(history.keys())[0]) is True
    assert isinstance(list(history.values())[0], int)

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
