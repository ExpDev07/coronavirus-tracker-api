from flask import jsonify, current_app as app
from ...services import jhu

@app.route('/v2/latest')
def latest():
    # Get the serialized version of all the locations.
    locations = [ location.serialize() for location in jhu.get_all() ]

    # All the latest information.
    latest = list(map(lambda location: location['latest'], locations))

    return jsonify({
        'latest': {
            'confirmed': sum(map(lambda latest: latest['confirmed'], latest)),
            'deaths'   : sum(map(lambda latest: latest['deaths'], latest)),
            'recovered': sum(map(lambda latest: latest['recovered'], latest)),
        }
    })