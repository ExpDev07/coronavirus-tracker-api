from abc import ABC, abstractmethod
import csv
import logging
import os
from datetime import datetime
from pprint import pformat as pf

from asyncache import cached
from cachetools import TTLCache

from ...caches import check_cache, load_cache
from ...coordinates import Coordinates
from ...location.csbs import CSBSLocation
from ...location.nyt import NYTLocation
from ...location import TimelinedLocation
from ...utils import countries
from ...utils import date as date_util
from ...utils import httputils
from . import LocationService
from ...models import Timeline


class LocationService(ABC):
    """
    Service for retrieving locations.
    """

    @abstractmethod
    async def get_all(self):
        """
        Gets and returns all of the locations.

        :returns: The locations.
        :rtype: List[Location]
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, id):  # pylint: disable=redefined-builtin,invalid-name
        """
        Gets and returns location with the provided id.

        :returns: The location.
        :rtype: Location
        """
        raise NotImplementedError


class LocationService(object):
    def __init__(self, service):
        self.service = service


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

LOGGERJHU = logging.getLOGGERJHU("services.location.jhu")
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
        LOGGERJHU.info(f"{data_id} using shared cache results")
        results = cache_results
    else:
        LOGGERJHU.info(f"{data_id} shared cache empty")
        # URL to request data from.
        url = BASE_URL + "time_series_covid19_%s_global.csv" % category

        # Request the data
        LOGGERJHU.info(f"{data_id} Requesting data...")
        async with httputils.CLIENT_SESSION.get(url) as response:
            text = await response.text()

        LOGGERJHU.debug(f"{data_id} Data received")

        # Parse the CSV.
        data = list(csv.DictReader(text.splitlines()))
        LOGGERJHU.debug(f"{data_id} CSV parsed")

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
        LOGGERJHU.debug(f"{data_id} Data normalized")

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

    LOGGERJHU.info(f"{data_id} results:\n{pf(results, depth=1)}")
    return results


@cached(cache=TTLCache(maxsize=1, ttl=1800))
async def get_locations():
    """
    Retrieves the locations from the categories. The locations are cached for 1 hour.

    :returns: The locations.
    :rtype: List[Location]
    """
    data_id = "jhu.locations"
    LOGGERJHU.info(f"pid:{PID}: {data_id} Requesting data...")
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
    LOGGERJHU.info(f"{data_id} Data normalized")

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
        LOGGERJHU.debug(f"iteration data merge error: {index} {key}")

    return location_history

LOGGERNYT = logging.getLoggerNYT("services.location.nyt")


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
    LOGGERNYT.info(f"{data_id} Requesting data...")
    # check shared cache
    cache_results = await check_cache(data_id)
    if cache_results:
        LOGGERNYT.info(f"{data_id} using shared cache results")
        locations = cache_results
    else:
        LOGGERNYT.info(f"{data_id} shared cache empty")
        async with httputils.CLIENT_SESSION.get(BASE_URL) as response:
            text = await response.text()

        LOGGERNYT.debug(f"{data_id} Data received")

        # Parse the CSV.
        data = list(csv.DictReader(text.splitlines()))
        LOGGERNYT.debug(f"{data_id} CSV parsed")

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
        LOGGERNYT.info(f"{data_id} Data normalized")
        # save the results to distributed cache
        # TODO: fix json serialization
        try:
            await load_cache(data_id, locations)
        except TypeError as type_err:
            LOGGERNYT.error(type_err)

    return locations