from flask import jsonify
from flask import current_app as app
from ...services.location.jhu import get_category
from ...routes import rest_api_v1

@rest_api_v1.route('/recovered')
def recovered():
    return jsonify(get_category('recovered'))
