"""app.services.location.csbs.py"""
import csv
import logging
from datetime import datetime

from asyncache import cached
from cachetools import TTLCache

from ...coordinates import Coordinates
from ...location.csbs import CSBSLocation
from ...utils import httputils
from . import LocationService


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


@cached(cache=TTLCache(maxsize=1, ttl=3600))
async def get_locations():
    """
    Retrieves county locations; locations are cached for 1 hour

    :returns: The locations.
    :rtype: dict
    """
    logger = logging.getLogger("services.location.csbs")
    logger.info("Requesting data...")
    async with httputils.CLIENT_SESSION.get(BASE_URL) as response:
        text = await response.text()

    logger.info("Data received")

    data = list(csv.DictReader(text.splitlines()))
    logger.info("CSV parsed")

    locations = []

    for i, item in enumerate(data):
        # General info.
        state = item["State Name"]
        county = item["County Name"]

        # Ensure country is specified.
        if county in {"Unassigned", "Unknown"}:
            continue

        # Coordinates.
        coordinates = Coordinates(item["Latitude"], item["Longitude"])  # pylint: disable=unused-variable

        # Date string without "EDT" at end.
        last_update = " ".join(item["Last Update"].split(" ")[0:2])

        # Append to locations.
        locations.append(
            CSBSLocation(
                # General info.
                i,
                state,
                county,
                # Coordinates.
                Coordinates(item["Latitude"], item["Longitude"]),
                # Last update (parse as ISO).
                datetime.strptime(last_update, "%Y-%m-%d %H:%M").isoformat() + "Z",
                # Statistics.
                int(item["Confirmed"] or 0),
                int(item["Death"] or 0),
            )
        )
    logger.info("Data normalized")

    # Return the locations.
    return locations
