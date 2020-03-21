from flask import request, jsonify
from ...routes import api_v2 as api

@api.route('/latest')
def latest():
    # Query parameters.
    args = request.args

    # Get the serialized version of all the locations.
    locations = request.source.get_all()
    #print([i.country_code for i in locations])

    # Filter based on args.
    if len(args) > 0:
        locations = [i for i in locations for j in args if hasattr(i, j) and getattr(i, j) == args[j]]

    # All the latest information.
    # latest = list(map(lambda location: location['latest'], locations))

    return jsonify({
        'latest': {
            'confirmed': sum(map(lambda location: location.confirmed, locations)),
            'deaths'   : sum(map(lambda location: location.deaths, locations)),
            'recovered': sum(map(lambda location: location.recovered, locations)),
        }
    })
