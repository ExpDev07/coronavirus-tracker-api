from flask import jsonify, request, current_app as app
from ...services import jhu
from ...routes import rest_api_v2

@rest_api_v2.route('/locations')
def locations():
    # Query parameters.
    timelines    = request.args.get('timelines', type=bool, default=False)
    country_code = request.args.get('country_code', type=str)

    # Retrieve all the locations.
    locations = jhu.get_all()

    # Filtering my country code if provided.
    if not country_code is None:
        locations = list(filter(lambda location: location.country_code == country_code.upper(), locations))

    # Serialize each location and return.
    return jsonify({
        'locations': [
            location.serialize(timelines) for location in locations
        ]
    })

@rest_api_v2.route('/locations/<int:id>')
def location(id):
    # Serialize the location with timelines.
    return jsonify({
        'location': jhu.get(id).serialize(True)
    })
