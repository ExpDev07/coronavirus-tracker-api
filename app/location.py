import requests
from datetime import datetime
from cachetools import cached, TTLCache
from geopy.geocoders import Nominatim
from app.settings import * 

class Location(object):
    """A location with data about the coronavirus."""    

    def __init__(self, last_updated, country, province, coordinates, confirmed, deaths, recovered):
        self.last_updated = last_updated
        self.country = country
        self.province = province
        self.coordinates = coordinates
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered

    def serialize(self):
        """Serializes the location."""
        return {
            'last_updated': self.last_updated, 
            'country':      self.country,
            'province':     self.province,
            'coordinates':  self.coordinates,
            'confirmed':    self.confirmed,
            'deaths':       self.deaths,
            'recovered':    self.recovered,
        }

import pprint

@cached(cache=TTLCache(maxsize=100, ttl=1800))
def get_locations():
    """Gets all the locations."""

    # Request latest data and parse the json.
    response = requests.get('https://sheets.googleapis.com/v4/spreadsheets/' + SPREADSHEET_ID + '/values/A:F?key=' + GOOGLE_API_KEY).json()

    # Extract the values and remove header.
    items = response['values']
    items.pop(0)

    # The locations.
    locations = [];

    # Go through all the items and make a location for them all.
    for item in items:
        locations.append(Location(
            # Date when location was last updated.
            last_updated = datetime.strptime(item[2], '%m/%d/%y %H:%M'),

            # Country and province.
            country  = item[1],
            province = item[0],

            # Coordinates.
            coordinates = get_coordinates(item[0] or item[1]),

            # Statistics.
            confirmed = int(item[3]),
            deaths    = int(item[4]),
            recovered = int(item[5]),
        ))

    # Return the locations!
    return locations

# Create the geo locator.
geolocator = Nominatim(user_agent='coronavirus-tracker-api', timeout=50)

@cached(cache={})
def get_coordinates(query):
    """Gets the coordinates from the query provided."""

    # Geo-code the query.
    geo_location = geolocator.geocode(query)
    
    # Make sure to return empty if we cannot geo-locate.
    if not geo_location:
        print('Could not geo-code ' + query)
        return None

    # Return the coordinates.
    print('Successfully geo-coded ' + query + '!')
    return {
        'latitude':  geo_location.latitude,
        'longitude': geo_location.longitude,
    }
        
    