from flask import jsonify, request
from distutils.util import strtobool
from ...routes import api_v2 as api

@api.route('/locations')
def locations():
    # Query parameters.
    args         = request.args
    timelines    = strtobool(args.get('timelines', default='0'))

    # Retrieve all the locations.
    locations = request.source.get_all()

    # Filtering by args if provided.
    for i in args:
        if i != 'timelines' and i[:2] != '__':
            try:
                locations = [j for j in locations if getattr(j, i) == args.get(i, type=str)]
            except AttributeError:
                print('Location does not have attribute {}.'.format(i))

    # Serialize each location and return.
    return jsonify({
        'latest': {
            'confirmed': sum(map(lambda location: location.confirmed, locations)),
            'deaths'   : sum(map(lambda location: location.deaths, locations)),
            'recovered': sum(map(lambda location: location.recovered, locations)),
        },
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
