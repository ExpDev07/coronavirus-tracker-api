from flask import jsonify
from app import app
from app.data import get_data

@app.route('/deaths')
def deaths():
    return jsonify(get_data('deaths'))