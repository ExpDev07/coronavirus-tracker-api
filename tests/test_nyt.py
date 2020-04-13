import json
from unittest import mock

import pytest

from app.location import TimelinedLocation
from app.location.nyt import NYTLocation
from app.services.location import nyt
from tests.conftest import mocked_strptime_isoformat

DATETIME_STRING = "2020-04-12T19:14:59.638001"


@pytest.mark.asyncio
async def test_get_locations(mock_client_session):
    with mock.patch("app.services.location.nyt.datetime") as mock_datetime:
        mock_datetime.utcnow.return_value.isoformat.return_value = DATETIME_STRING
        mock_datetime.strptime.side_effect = mocked_strptime_isoformat
        locations = await nyt.get_locations()

    assert isinstance(locations, list)

    serialized_locations = []
    for location in locations:
        assert isinstance(location, NYTLocation)
        assert isinstance(location, TimelinedLocation)

        # Making sure country population is a non-zero value
        assert location.country_population != 0
        serialized_location = location.serialize(timelines=True)
        # Not checking for exact value of country population
        del serialized_location["country_population"]

        serialized_locations.append(serialized_location)

    produced_json_output = json.dumps(serialized_locations)

    with open("tests/expected_output/nyt_locations.json", "r") as file:
        expected_json_output = file.read()

    # translate them into python lists for ordering
    assert json.loads(expected_json_output) == json.loads(produced_json_output)
