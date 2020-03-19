from flask import jsonify
from flask import current_app as app
from ...routes import api_v1 as api
from ...services.location.jhu import get_category

@api.route('/deaths')
def deaths():
    return jsonify(get_category('deaths'))
