"""app.services.location.nyt.py"""
import csv
import logging
from datetime import datetime

from asyncache import cached
from cachetools import TTLCache

from ...coordinates import Coordinates
from ...location.nyt import NYTLocation
from ...timeline import Timeline
from ...utils import httputils
from . import LocationService

LOGGER = logging.getLogger("services.location.nyt")


class NYTLocationService(LocationService):
    """
    Service for retrieving locations from New York Times (https://github.com/nytimes/covid-19-data).
    """

    async def get_all(self):
        # Get the locations.
        locations = await get_locations()
        return locations

    async def get(self, loc_id):  # pylint: disable=arguments-differ
        # Get location at the index equal to provided id.
        locations = await self.get_all()
        return locations[loc_id]


# ---------------------------------------------------------------


# Base URL for fetching category.
BASE_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"


def get_grouped_locations_dict(data):
    """
    Helper function to group history for locations into one dict.

    :returns: The complete data for each unique US county
    :rdata: dict
    """
    grouped_locations = {}

    # in increasing order of dates
    for row in data:
        county_state = (row["county"], row["state"])
        date = row["date"]
        confirmed = row["cases"]
        deaths = row["deaths"]

        # initialize if not existing
        if county_state not in grouped_locations:
            grouped_locations[county_state] = {"confirmed": [], "deaths": []}

        # append confirmed tuple to county_state (date, # confirmed)
        grouped_locations[county_state]["confirmed"].append((date, confirmed))
        # append deaths tuple to county_state (date, # deaths)
        grouped_locations[county_state]["deaths"].append((date, deaths))

    return grouped_locations


@cached(cache=TTLCache(maxsize=1024, ttl=3600))
async def get_locations():
    """
    Returns a list containing parsed NYT data by US county. The data is cached for 1 hour.

    :returns: The complete data for US Counties.
    :rtype: dict
    """
    # Request the data.
    LOGGER.info("nyt Requesting data...")
    async with httputils.CLIENT_SESSION.get(BASE_URL) as response:
        text = await response.text()

    LOGGER.info("Data received")

    # Parse the CSV.
    data = list(csv.DictReader(text.splitlines()))
    LOGGER.info("nyt CSV parsed")

    # Group together locations (NYT data ordered by dates not location).
    grouped_locations = get_grouped_locations_dict(data)

    # The normalized locations.
    locations = []

    for idx, (county_state, histories) in enumerate(grouped_locations.items()):
        # Make location history for confirmed and deaths from dates.
        # List is tuples of (date, amount) in order of increasing dates.
        confirmed_list = histories["confirmed"]
        confirmed_history = {date: int(amount or 0) for date, amount in confirmed_list}

        deaths_list = histories["deaths"]
        deaths_history = {date: int(amount or 0) for date, amount in deaths_list}

        # Normalize the item and append to locations.
        locations.append(
            NYTLocation(
                id=idx,
                state=county_state[1],
                county=county_state[0],
                coordinates=Coordinates(None, None),  # NYT does not provide coordinates
                last_updated=datetime.utcnow().isoformat() + "Z",  # since last request
                timelines={
                    "confirmed": Timeline(
                        {
                            datetime.strptime(date, "%Y-%m-%d").isoformat() + "Z": amount
                            for date, amount in confirmed_history.items()
                        }
                    ),
                    "deaths": Timeline(
                        {
                            datetime.strptime(date, "%Y-%m-%d").isoformat() + "Z": amount
                            for date, amount in deaths_history.items()
                        }
                    ),
                    "recovered": Timeline({}),
                },
            )
        )
    LOGGER.info("nyt Data normalized")

    return locations
