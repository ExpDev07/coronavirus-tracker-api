import csv
import logging
from datetime import datetime

from asyncache import cached
from cachetools import TTLCache

from ...caches import check_cache, load_cache
from ...coordinates import Coordinates
from ...location.csbs import CSBSLocation
from ...utils import httputils
from . import DataSourcesInterface

LOGGER = logging.getLogger("services.location.csbs")
 # Base URL for fetching data
BASE_URL = "https://facts.csbs.org/covid-19/covid19_county.csv"

class CSBSLocations(DataSourcesInterface):
   
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
            LOGGER.info(f"{data_id} Data normalized")
            # save the results to distributed cache
            # TODO: fix json serialization
            try:
                await load_cache(data_id, locations)
            except TypeError as type_err:
                LOGGER.error(type_err)

        # Return the locations.
        return locations