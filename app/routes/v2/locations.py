from flask import jsonify, request
from distutils.util import strtobool
from ...routes import api_v2 as api
from ...data import data_source

@api.route('/locations')
def locations():
    # Query parameters.
    timelines    = strtobool(request.args.get('timelines', default='0'))
    country_code = request.args.get('country_code', type=str)

    # Retrieve all the locations.
    locations = request.source.get_all()

    # Filtering my country code if provided.
    if not country_code is None:
        locations = list(filter(lambda location: location.country_code == country_code.upper(), locations))

    # Serialize each location and return.
    return jsonify({
        'locations': [
            location.serialize(timelines) for location in locations
        ]
    })

@api.route('/locations/<int:id>')
def location(id):
    # Query parameters.
    timelines = strtobool(request.args.get('timelines', default='1'))

    # Return serialized location.
    return jsonify({
        'location': request.source.get(id).serialize(timelines)
    })
