from flask import jsonify, request
from ...routes import api_v2 as api
from ...services import jhu

@api.route('/country')
def country():

    # Retrieve all the locations.
    locations = jhu.get_all()

    # accepts either country or country_code as a parameter, but only one is required
    country_code = request.args.get('country_code', type=str)
    country = request.args.get('country', type=str)

    # sort by given country or country_code. Country_code will always override country
    if country_code:
        country_locations = list(filter(lambda location: location.country_code == country_code.upper(), locations))
    elif country:
        country_locations = list(filter(lambda location: location.country.lower() == country.lower(), locations))

    # serialize location objects
    country_locations = [location.serialize() for location in country_locations]

    # check for errors in query
    if not country_locations:
        return jsonify({'error': 'parameter country_code or country required'})

    # return as a singe dictionary
    return jsonify({
        'country_code': country_locations[0]['country_code'],
        'country'     : country_locations[0]['country'],

        'latest': {
            'confirmed': sum(location['latest']['confirmed'] for location in country_locations),
            'deaths'   : sum(location['latest']['deaths'] for location in country_locations),
            'recovered': sum(location['latest']['recovered'] for location in country_locations),
        }
    })
