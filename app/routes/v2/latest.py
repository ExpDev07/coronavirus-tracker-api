from flask import jsonify, request
from ...routes import api_v2 as api
from ...services import jhu

@api.route('/latest')
def latest():
    #Query parameters.
    country_code = request.args.get('country_code', type=str)

    # Get the serialized version of all the locations.
    locations = [ location.serialize() for location in jhu.get_all() ]

    # Return aggregate data for country if provided.
    if not country_code is None:
        locations = list(filter(lambda location: location['country_code'] == country_code.upper(), locations))

    # All the latest information.
    latest = list(map(lambda location: location['latest'], locations))

    return jsonify({
        'latest': {
            'confirmed': sum(map(lambda latest: latest['confirmed'], latest)),
            'deaths'   : sum(map(lambda latest: latest['deaths'], latest)),
            'recovered': sum(map(lambda latest: latest['recovered'], latest)),
        }
    })
