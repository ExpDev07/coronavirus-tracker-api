from flask import jsonify
from app import app
from app.data import get_data

@app.route('/confirmed')
def confirmed():
    return jsonify(get_data('confirmed'))