"""app.services.location.jhu.py"""
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
from . import LocationService

LOGGER = logging.getLogger("services.location.jhu")
PID = os.getpid()

class JhuLocationService(LocationService):
    """
    Service for retrieving locations from Johns Hopkins CSSE (https://github.com/CSSEGISandData/COVID-19).
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
BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/"


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

            # Latest data insert value.
            latest = list(history.values())[-1]

            # Country for this location.
            country = item["Country/Region"]

            # Normalize the item and append to locations.
            locations.append({
                "country": country,
                "country_code": countries.country_code(country),
                "province": item["Province/State"],
                "coordinates": {
                    "lat": item["Lat"], 
                    "long": item["Long"],
                },
                "history": history,
                "latest": int(latest or 0),
            })
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
            "deaths": parse_history(key, locations_deaths),
            "recovered": parse_history(key, locations_recovered),
        }

        # Grab coordinates.
        coordinates = location["coordinates"]

        # Create location (supporting timelines) and append.
        locations.append(
            TimelinedLocation(
                id=index,
                country=location["country"],
                province=location["province"],
                coordinates=Coordinates(latitude=coordinates["lat"], longitude=coordinates["long"]),
                last_updated=datetime.utcnow().isoformat() + "Z",
                timelines={
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

    return locations


def parse_history(key: tuple, locations: list):
    """
    Helper for validating and extracting history content from
    locations data based on key. Validates with the current country/province
    key to make sure no index/column issue.
    """

    for i, location in enumerate(locations):
        if (location["country"], location["province"]) == key:
            return location["history"]

    LOGGER.debug(f"iteration data merge error: {key}")

    return {}
