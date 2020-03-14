from flask import jsonify
from flask import current_app as app
from ..data import get_data

@app.route('/deaths')
def deaths():
    return jsonify(get_data('deaths'))