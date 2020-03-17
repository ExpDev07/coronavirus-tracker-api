from . import LocationService
from ...location import Location
from ...coordinates import Coordinates
from ...timeline import Timeline

class JhuLocationService(LocationService):
    """
    Service for retrieving locations from Johns Hopkins CSSE (https://github.com/CSSEGISandData/COVID-19).
    """

    def get_all(self, **kwargs):
        # Get all of the data categories locations.
        confirmed = get_category('confirmed')['locations']
        deaths    = get_category('deaths')['locations']
        recovered = get_category('recovered')['locations']

        # Final locations to return.
        locations = []

        # Go through confirmed locations.
        for index, location in enumerate(confirmed):
            # Grab coordinates.
            coordinates = location['coordinates']

            # Create location and append.
            locations.append(Location(
                # General info.
                index, location['country'], location['province'], Coordinates(coordinates['lat'], coordinates['long']),

                # TODO: date key as ISO format.
                # { datetime.strptime(date, '%m/%d/%y').isoformat() + 'Z': int(amount or 0) for date, amount in history.items() }
            
                # Timelines.
                Timeline(confirmed[index]['history']),
                Timeline(deaths[index]['history']),
                Timeline(recovered[index]['history'])
            ))
        
        # Finally, return the locations.
        return locations
    
    def get(self, id):
        # Get location at the index equal to provided id.
        return self.get_all()[id]

import requests
import csv
from datetime import datetime
from cachetools import cached, TTLCache
from ...utils import countrycodes, date as date_util

"""
Base URL for fetching category.
"""
base_url = 'https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-%s.csv';

@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_category(category):
    """
    Retrieves the data for the provided category. The data is cached for 1 hour.
    """

    # Adhere to category naming standard.
    category = category.lower().capitalize();

    # Request the data
    request = requests.get(base_url % category)
    text    = request.text

    # Parse the CSV.
    data = list(csv.DictReader(text.splitlines()))

    # The normalized locations.
    locations = []

    for item in data:
        # Filter out all the dates.
        dates = dict(filter(lambda element: date_util.is_date(element[0]), item.items()))

        # Make location history from dates.
        history = { date: int(amount or 0) for date, amount in dates.items() };

        # Country for this location.
        country = item['Country/Region']

        # Latest data insert value.
        latest = list(sorted(history.values()))[-1];

        # Normalize the item and append to locations.
        locations.append({
            # General info.
            'country':  country,
            'country_code': countrycodes.country_code(country),
            'province': item['Province/State'],

            # Coordinates.
            'coordinates': {
                'lat':  item['Lat'],
                'long': item['Long'],
            },

            # History.
            'history': history,

            # Latest statistic.
            'latest': int(latest or 0),
        })

    # Latest total.
    latest = sum(map(lambda location: location['latest'], locations))

    # Return the final data.
    return {
        'locations': locations,
        'latest': latest,
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'source': 'https://github.com/ExpDev07/coronavirus-tracker-api',
    }