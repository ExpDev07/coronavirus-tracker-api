import requests
import csv
from cachetools import cached, TTLCache
from app.utils import date as date_util

"""
Base URL for fetching data.
"""
base_url = 'https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/time_series/time_series_2019-ncov-%s.csv';

@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_data(type):
    """
    Retrieves the data for the provided type.
    """

    # Adhere to type naming standard.
    type = type.lower().capitalize();
    
    # Request the data 
    request = requests.get(base_url % type)
    text    = request.text

    # Parse the CSV.
    data = list(csv.DictReader(text.splitlines()))

    # The normalized locations.
    locations = []

    for item in data:

        # Normalize the item and append to locations.
        locations.append({
            # General info.
            'country':  item['Country/Region'],
            'province': item['Province/State'],

            # Coordinates.
            'coordinates': {
                'lat':  item['Lat'],
                'long': item['Long'],
            },

            # History.
            'history': dict(filter(lambda element: date_util.is_date(element[0]), item.items())),

            # TODO: Total.
            'total': 0
        })

    # Return the final data.
    return locations






    

