"""app.services.location.csbs.py"""
import csv
import logging
from datetime import datetime

from asyncache import cached
from cachetools import TTLCache

from ...caches import check_cache, load_cache
from ...coordinates import Coordinates
from ...location.csbs import CSBSLocation
from ...utils import httputils
from . import LocationService

LOGGER = logging.getLogger("services.location.csbs")


class BasicLocationService(LocationService):
    """
    Service for retrieving locations from csbs
    """

    async def get_all(self):
        # Get the locations.
        locations = await self.dataSource.get_locations()
        return locations

    async def get(self, loc_id):  # pylint: disable=arguments-differ
        # Get location at the index equal to the provided id.
        locations = await self.get_all()
        return locations[loc_id]


