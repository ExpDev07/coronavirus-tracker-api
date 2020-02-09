import requests
import functools
from flask import jsonify
from app import app
from app.location import get_locations

@app.route('/latest')
def latest():
    # Get all the locations.
    locations = list(map(lambda loc: loc.serialize(), get_locations()))

    # Make some simple statistic calculations.
    confirmed = sum(map(lambda loc: loc['confirmed'], locations))
    deaths    = sum(map(lambda loc: loc['deaths'], locations))
    recovered = sum(map(lambda loc: loc['recovered'], locations))

    # Return the stats and data as json.
    return {
        # Stats
        'confirmed': confirmed,
        'deaths':    deaths,
        'recovered': recovered,

        # Data
        'locations': locations,
    }