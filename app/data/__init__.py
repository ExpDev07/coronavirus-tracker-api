import requests
import csv
from datetime import datetime
from cachetools import cached, TTLCache
from ..utils import countrycodes, date as date_util

"""
Base URL for fetching data.
"""
base_url = 'https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-%s.csv';

@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_data(category):
    """
    Retrieves the data for the provided type. The data is cached for 1 hour.
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
    keys = []
    for item in data:
        # Filter out all the dates.
        dates = dict(filter(lambda element: date_util.is_date(element[0]), item.items()))

        # Make location history from dates.
        history = { date: int(amount or 0) for date, amount in dates.items() };

        # Country for this location.
        country = item['Country/Region']

        # Latest data insert value.
        latest = list(history.values())[-1];
        if item['Province/State'] == "":
            keys.append(country)
        else:
            keys.append(item['Province/State'])
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
        'locations': dict(zip(keys, locations)),
        'latest': latest,
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'source': 'https://github.com/ExpDev07/coronavirus-tracker-api',
    }
