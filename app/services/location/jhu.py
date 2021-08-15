import csv
import logging
import os
from datetime import datetime
from pprint import pformat as pf

from asyncache import cached
from cachetools import TTLCache

from ...caches import check_cache, load_cache
from ...coordinates import Coordinates
from ...location import TimelinedLocation
from ...models import Timeline
from ...utils import countries
from ...utils import date as date_util
from ...utils import httputils
from . import DataSourcesInterface

# Base URL for fetching category.
BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/"
LOGGER = logging.getLogger("services.location.jhu")
PID = os.getpid()

class JHULocations(DataSourcesInterface):
    @cached(cache=TTLCache(maxsize=1, ttl=1800))
    async def get_locations():
        """
        Retrieves the locations from the categories. The locations are cached for 1 hour.
        :returns: The locations.
        :rtype: List[Location]
        """
        data_id = "jhu.locations"
        LOGGER.info(f"pid:{PID}: {data_id} Requesting data...")
        # Get all of the data categories locations.
        confirmed = await get_category("confirmed")
        deaths = await get_category("deaths")
        recovered = await get_category("recovered")

        locations_confirmed = confirmed["locations"]
        locations_deaths = deaths["locations"]
        locations_recovered = recovered["locations"]

        # Final locations to return.
        locations = []
        # ***************************************************************************
        # TODO: This iteration approach assumes the indexes remain the same
        #       and opens us to a CRITICAL ERROR. The removal of a column in the data source
        #       would break the API or SHIFT all the data confirmed, deaths, recovery producting
        #       incorrect data to consumers.
        # ***************************************************************************
        # Go through locations.
        for index, location in enumerate(locations_confirmed):
            # Get the timelines.

            # TEMP: Fix for merging recovery data. See TODO above for more details.
            key = (location["country"], location["province"])

            timelines = {
                "confirmed": location["history"],
                "deaths": parse_history(key, locations_deaths, index),
                "recovered": parse_history(key, locations_recovered, index),
            }

            # Grab coordinates.
            coordinates = location["coordinates"]

            # Create location (supporting timelines) and append.
            locations.append(
                TimelinedLocation(
                    # General info.
                    index,
                    location["country"],
                    location["province"],
                    # Coordinates.
                    Coordinates(latitude=coordinates["lat"], longitude=coordinates["long"]),
                    # Last update.
                    datetime.utcnow().isoformat() + "Z",
                    # Timelines (parse dates as ISO).
                    {
                        "confirmed": Timeline(
                            timeline={
                                datetime.strptime(date, "%m/%d/%y").isoformat() + "Z": amount
                                for date, amount in timelines["confirmed"].items()
                            }
                        ),
                        "deaths": Timeline(
                            timeline={
                                datetime.strptime(date, "%m/%d/%y").isoformat() + "Z": amount
                                for date, amount in timelines["deaths"].items()
                            }
                        ),
                        "recovered": Timeline(
                            timeline={
                                datetime.strptime(date, "%m/%d/%y").isoformat() + "Z": amount
                                for date, amount in timelines["recovered"].items()
                            }
                        ),
                    },
                )
            )
        LOGGER.info(f"{data_id} Data normalized")

        # Finally, return the locations.
        return locations
 

    
def parse_history(key: tuple, locations: list, index: int):
    """
    Helper for validating and extracting history content from
    locations data based on index. Validates with the current country/province
    key to make sure no index/column issue.
    TEMP: solution because implement a more efficient and better approach in the refactor.
    """
    location_history = {}
    try:
        if key == (locations[index]["country"], locations[index]["province"]):
            location_history = locations[index]["history"]
    except (IndexError, KeyError):
        LOGGER.debug(f"iteration data merge error: {index} {key}")

    return location_history




@cached(cache=TTLCache(maxsize=4, ttl=1800))
async def get_category(category):
    """
    Retrieves the data for the provided category. The data is cached for 30 minutes locally, 1 hour via shared Redis.
    :returns: The data for category.
    :rtype: dict
    """
    # Adhere to category naming standard.
    category = category.lower()
    data_id = f"jhu.{category}"

    # check shared cache
    cache_results = await check_cache(data_id)
    if cache_results:
        LOGGER.info(f"{data_id} using shared cache results")
        results = cache_results
    else:
        LOGGER.info(f"{data_id} shared cache empty")
        # URL to request data from.
        url = BASE_URL + "time_series_covid19_%s_global.csv" % category

        # Request the data
        LOGGER.info(f"{data_id} Requesting data...")
        async with httputils.CLIENT_SESSION.get(url) as response:
            text = await response.text()

        LOGGER.debug(f"{data_id} Data received")

        # Parse the CSV.
        data = list(csv.DictReader(text.splitlines()))
        LOGGER.debug(f"{data_id} CSV parsed")

        # The normalized locations.
        locations = []

        for item in data:
            # Filter out all the dates.
            dates = dict(filter(lambda element: date_util.is_date(element[0]), item.items()))

            # Make location history from dates.
            history = {date: int(float(amount or 0)) for date, amount in dates.items()}

            # Country for this location.
            country = item["Country/Region"]

            # Latest data insert value.
            latest = list(history.values())[-1]

            # Normalize the item and append to locations.
            locations.append(
                {
                    # General info.
                    "country": country,
                    "country_code": countries.country_code(country),
                    "province": item["Province/State"],
                    # Coordinates.
                    "coordinates": {"lat": item["Lat"], "long": item["Long"],},
                    # History.
                    "history": history,
                    # Latest statistic.
                    "latest": int(latest or 0),
                }
            )
        LOGGER.debug(f"{data_id} Data normalized")

        # Latest total.
        latest = sum(map(lambda location: location["latest"], locations))

        # Return the final data.
        results = {
            "locations": locations,
            "latest": latest,
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "source": "https://github.com/ExpDev07/coronavirus-tracker-api",
        }
        # save the results to distributed cache
        await load_cache(data_id, results)

    LOGGER.info(f"{data_id} results:\n{pf(results, depth=1)}")
    return results

