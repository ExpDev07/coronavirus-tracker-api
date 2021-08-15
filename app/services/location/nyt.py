"""app.services.location.nyt.py"""
import csv
import logging

from asyncache import cached
from cachetools import TTLCache

from ...caches import check_cache, load_cache
from ...utils import httputils
from . import LocationService
from ...import factorylocation

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


@cached(cache=TTLCache(maxsize=1, ttl=1800))
async def get_locations():
    """
    Returns a list containing parsed NYT data by US county. The data is cached for 1 hour.

    :returns: The complete data for US Counties.
    :rtype: dict
    """
    data_id = "nyt.locations"
    # Request the data.
    LOGGER.info(f"{data_id} Requesting data...")
    # check shared cache
    cache_results = await check_cache(data_id)
    if cache_results:
        LOGGER.info(f"{data_id} using shared cache results")
        locations = cache_results
    else:
        LOGGER.info(f"{data_id} shared cache empty")
        async with httputils.CLIENT_SESSION.get(BASE_URL) as response:
            text = await response.text()

        LOGGER.debug(f"{data_id} Data received")

        # Parse the CSV.
        data = list(csv.DictReader(text.splitlines()))
        LOGGER.debug(f"{data_id} CSV parsed")

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
            params = {'index': idx, 'county_state': county_state, 'confirmed_history': confirmed_history,'deaths_history': deaths_history}
            locations.append(locationfactory.create_location('NYT', params))

        LOGGER.info(f"{data_id} Data normalized")

        try:
            await load_cache(data_id, locations)
        except TypeError as type_err:
            LOGGER.error(type_err)

    return locations
