from flask import jsonify
from flask import current_app as app
from ...services.location.jhu import get_category

@app.route('/recovered')
def recovered():
    return jsonify(get_category('recovered'))