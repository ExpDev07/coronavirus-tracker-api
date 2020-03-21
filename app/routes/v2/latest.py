from flask import request, jsonify
from ...routes import api_v2 as api

@api.route('/latest')
def latest():
    # Get the serialized version of all the locations.
    locations = [ location.serialize() for location in request.source.get_all() ]

    # All the latest information.
    latest = list(map(lambda location: location['latest'], locations))

    return jsonify({
        'latest': {
            'confirmed': sum(map(lambda latest: latest['confirmed'], latest)),
            'deaths'   : sum(map(lambda latest: latest['deaths'], latest)),
            'recovered': sum(map(lambda latest: latest['recovered'], latest)),
        }
    })
