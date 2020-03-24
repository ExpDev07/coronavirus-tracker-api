from flask import jsonify
from ...routes import api_v1 as api

# Dummy response.
dummy = {
    'source'      : 'https://github.com/ExpDev07/coronavirus-tracker-api',
    'last_updated': '2020-03-24T03:57:10.057450Z',
    'latest'      : 0,
    'locations'   : [],
}

@api.route('/recovered')
def recovered():
    # Dummy data.
    return jsonify(dummy)
