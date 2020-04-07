"""app.services.location.nyt.py"""
import csv
from datetime import datetime

from asyncache import cached
from cachetools import TTLCache

from . import LocationService


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


@cached(cache=TTLCache(maxsize=1024, ttl=3600))  # TODO
async def get_category(category):
    pass


@cached(cache=TTLCache(maxsize=1024, ttl=3600))
async def get_locations():
    pass
