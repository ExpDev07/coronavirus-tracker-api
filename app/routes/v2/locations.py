from flask import jsonify, request
from distutils.util import strtobool
from ...routes import api_v2 as api
from ...services import jhu, csbs

@api.route('/locations')
def locations():
    # Query parameter -> data source.
    source = request.args.get('source', default='jhu')

    if source == 'csbs':
        # Query parameters
        state = request.args.get('state', type=str, default='')
        
        # Retrieve all locations.
        data = csbs.get_all()
        locations = data.copy()

        # Filter by state if applicable
        if state in locations:
            locations = locations[state]
            return jsonify({
                state: [
                    location.serialize() for location in locations
                ]
            })
        
        # serialize everything
        for state in locations:
            locations[state] = [county.serialize() for county in locations[state]]
        
        return jsonify(locations)
    else:
        # Query parameters
        timelines    = strtobool(request.args.get('timelines', default='0'))
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

    

@api.route('/locations/<int:id>')
def location(id):
    # Query parameters.
    timelines = strtobool(request.args.get('timelines', default='1'))

    # Return serialized location.
    return jsonify({
        'location': jhu.get(id).serialize(timelines)
    })
