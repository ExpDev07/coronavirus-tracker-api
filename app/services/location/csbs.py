"""app.services.location.csbs.py"""
import csv
from datetime import datetime

import requests
from cachetools import TTLCache, cached

from ...coordinates import Coordinates
from ...location.csbs import CSBSLocation
from . import LocationService


class CSBSLocationService(LocationService):
    """
    Servive for retrieving locations from csbs
    """

    def get_all(self):
        # Get the locations
        return get_locations()

    def get(self, loc_id):  # pylint: disable=arguments-differ
        return self.get_all()[loc_id]


# Base URL for fetching data
BASE_URL = "https://facts.csbs.org/covid-19/covid19_county.csv"


@cached(cache=TTLCache(maxsize=1, ttl=3600))
def get_locations():
    """
    Retrieves county locations; locations are cached for 1 hour

    :returns: The locations.
    :rtype: dict
    """
    request = requests.get(BASE_URL)
    text = request.text

    data = list(csv.DictReader(text.splitlines()))

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

    # Return the locations.
    return locations
