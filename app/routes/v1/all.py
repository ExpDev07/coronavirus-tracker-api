from flask import jsonify
from .recovered import dummy
from ...routes import api_v1 as api
from ...services.location.jhu import get_category

@api.route('/all')
def all():
    # Get all the categories.
    confirmed = get_category('confirmed')
    deaths    = get_category('deaths')

    return jsonify({
        # Data.
        'confirmed': confirmed,
        'deaths':    deaths,
        'recovered': dummy,

        # Latest.
        'latest': {
            'confirmed': confirmed['latest'],
            'deaths':    deaths['latest'],
            'recovered': 0,
        }
    })
