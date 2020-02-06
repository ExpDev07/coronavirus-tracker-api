import requests
import functools
from datetime import datetime
from app import app
from ..settings import *

@app.route('/latest')
def latest():
    # Fetch the latest data.
    data = fetch()

    # Make some simple statistic calculations.
    confirmed = sum(map(lambda value: value['confirmed'], data))
    deaths    = sum(map(lambda value: value['deaths'], data))
    recovered = sum(map(lambda value: value['recovered'], data))

    # Return the stats and data as json.
    return {
        # Stats
        'confirmed': confirmed,
        'deaths':    deaths,
        'recovered': recovered,

        # Data
        'data': data
    }

def fetch():
    """
    Fetches the latest data.
    """

    # Request latest data and parse the json
    response = requests.get('https://sheets.googleapis.com/v4/spreadsheets/' + SPREADSHEET_ID + '/values/A:F?key=' + GOOGLE_API_KEY).json()

    # Extract the values and remove header
    items = response['values']
    items.pop(0)

    # Normalize the values
    return normalizeItems(items)

def normalizeItems(items):
    """
    Normalizes the items into a format that can be returned.
    """

    # The list of items normalized.
    normalized = []

    # Normalize each item and add them to the list.
    for item in items:
        normalized.append(normalize(item))

    # Return the normalized items.
    return normalized

def normalize(item):
    """
    Normalizes the provided item.
    """

    # Return the normalized item.
    return {
        'province':     item[0],
        'country':      item[1],
        'last_updated': datetime.strptime(item[2], '%m/%d/%y %H:%M'),
        'confirmed':    int(item[3]),
        'deaths':       int(item[4]),
        'recovered':    int(item[5]),
    }