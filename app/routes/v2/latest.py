from flask import request, jsonify
from ...routes import api_v2 as api

@api.route('/latest')
def latest():
    # Get the serialized version of all the locations.
    locations = request.source.get_all()

    # All the latest information.
    # latest = list(map(lambda location: location['latest'], locations))

    return jsonify({
        'latest': {
            'confirmed': sum(map(lambda location: location.confirmed, locations)),
            'deaths'   : sum(map(lambda location: location.deaths, locations)),
            'recovered': sum(map(lambda location: location.recovered, locations)),
        }
    })
