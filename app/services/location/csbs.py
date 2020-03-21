from . import LocationService
from ...location import CSBSLocation
from ...coordinates import Coordinates

class CSBSLocationService(LocationService):
    """
    Servive for retrieving locations from csbs
    """

    def get_all(self):
        # Get the locations
        return get_locations()
    
    def get(self, id):
        return self.get_all()[id]

import requests
import csv
from datetime import datetime
from cachetools import cached, TTLCache

# Base URL for fetching data
base_url = 'https://facts.csbs.org/covid-19/covid19_county.csv'

@cached(cache=TTLCache(maxsize=1, ttl=3600))
def get_locations():
    """
    Retrieves county locations; locations are cached for 1 hour

    :returns: The locations.
    :rtype: dict
    """
    request = requests.get(base_url)
    text = request.text

    data = list(csv.DictReader(text.splitlines()))
    
    locations = []

    for i, item in enumerate(data):
        state = item['State Name']
        county = item['County Name']
        if county == "Unassigned" or county == "Unknown":
            continue

        confirmed = int(item['Confirmed'] or 0)
        death = int(item['Death'] or 0)
        coordinates = Coordinates(float(item['Latitude']), float(item['Longitude']))
        last_update = item['Last Update']
        locations.append(CSBSLocation(i, state, county, coordinates, last_update, confirmed, death))

    return locations
