import csv
import logging
from datetime import datetime

from asyncache import cached
from cachetools import TTLCache

from ...caches import check_cache, load_cache
from ...coordinates import Coordinates
from ...location.nyt import NYTLocation
from ...models import Timeline
from ...utils import httputils
from . import DataSourcesInterface

LOGGER = logging.getLogger("services.location.nyt")
 # Base URL for fetching category.
BASE_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"


class NYTLocations(DataSourcesInterface):

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
                                timeline={
                                    datetime.strptime(date, "%Y-%m-%d").isoformat() + "Z": amount
                                    for date, amount in confirmed_history.items()
                                }
                            ),
                            "deaths": Timeline(
                                timeline={
                                    datetime.strptime(date, "%Y-%m-%d").isoformat() + "Z": amount
                                    for date, amount in deaths_history.items()
                                }
                            ),
                            "recovered": Timeline(),
                        },
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
