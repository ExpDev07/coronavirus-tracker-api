from flask import jsonify
from flask import current_app as app
from ..data import get_data

@app.route('/all')
def all():
    # Get all the categories.
    confirmed = get_data('confirmed')
    deaths    = get_data('deaths')
    recovered = get_data('recovered')

    return jsonify({
        # Data.
        'confirmed': confirmed,
        'deaths':    deaths,
        'recovered': recovered,

        # Latest.
        'latest': {
            'confirmed': confirmed['latest'],
            'deaths':    deaths['latest'],
            'recovered': recovered['latest'],
        }
    })