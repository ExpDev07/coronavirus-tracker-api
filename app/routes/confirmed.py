from flask import jsonify
from flask import current_app as app
from ..data import get_data

@app.route('/confirmed')
def confirmed():
    return jsonify(get_data('confirmed'))