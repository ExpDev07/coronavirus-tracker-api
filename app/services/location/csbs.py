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

class CSBSLocationService(LocationService):
    """
    Service for retrieving locations from csbs
    """

    async def get_all(self):
        # Get the locations.
        locations = await get_locations()

        return locations

    async def get(self, loc_id):  # pylint: disable=arguments-differ
        # Get location at the index equal to the provided id.
        locations = await self.get_all()

        return locations[loc_id]

# Base URL for fetching data
BASE_URL = "https://facts.csbs.org/covid-19/covid19_county.csv"

@cached(cache=TTLCache(maxsize=1, ttl=1800))
async def get_locations():
    """
    Retrieves county locations; locations are cached for 1 hour

    :returns: The locations.
    :rtype: dict
    """

    data_id = "csbs.locations"
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

        data = list(csv.DictReader(text.splitlines()))
        LOGGER.debug(f"{data_id} CSV parsed")

        locations = []

        for i, item in enumerate(data):
            # General info.
            state = item["State Name"]
            county = item["County Name"]

            # Ensure country is specified.
            if county in {"Unassigned", "Unknown"}:
                continue

            # Date string without "EDT" at end.
            last_update = " ".join(item["Last Update"].split(" ")[0:2])

            # Append to locations.
            locations.append(
                CSBSLocation(
                    id=i,
                    state=state,
                    county=county,
                    coordinates=Coordinates(item["Latitude"], item["Longitude"]),
                    last_updated=datetime.strptime(last_update, "%Y-%m-%d %H:%M").isoformat() + "Z",
                    confirmed=int(item["Confirmed"] or 0),
                    deaths=int(item["Death"] or 0),
                )
            )
        
        LOGGER.info(f"{data_id} Data normalized")
        # save the results to distributed cache
        # TODO: fix json serialization
        try:
            await load_cache(data_id, locations)
        except TypeError as type_err:
            LOGGER.error(type_err)

    return locations
