from flask import jsonify
from flask import current_app as app
from ..data import get_data

@app.route('/recovered')
def recovered():
    return jsonify(get_data('recovered'))