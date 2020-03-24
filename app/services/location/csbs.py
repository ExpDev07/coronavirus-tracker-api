from . import LocationService
from ...coordinates import Coordinates
from ...location.csbs import CSBSLocation

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
        # General info.
        state = item['State Name']
        county = item['County Name']

        # Ensure country is specified.
        if county == "Unassigned" or county == "Unknown":
            continue

        # Coordinates.
        coordinates = Coordinates(
            item['Latitude'], 
            item['Longitude']
        )
        
        # Date string without "EDT" at end.
        last_update = ' '.join(item['Last Update'].split(' ')[0:2])
        
        # Append to locations.
        locations.append(CSBSLocation(
            # General info.
            i, state, county,
            
            # Coordinates.
            Coordinates(
                item['Latitude'], 
                item['Longitude']
            ),

            # Last update (parse as ISO).
            datetime.strptime(last_update, '%Y-%m-%d %H:%M').isoformat() + 'Z', 
            
            # Statistics.
            int(item['Confirmed'] or 0),
            int(item['Death'] or 0)
        ))

    # Return the locations.
    return locations
