from flask import jsonify
from app import app
from app.data import get_data

@app.route('/recovered')
def recovered():
    return jsonify(get_data('recovered'))