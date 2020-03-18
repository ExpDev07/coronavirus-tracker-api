from flask import jsonify
from flask import current_app as app
from ...services.location.jhu import get_category

@app.route('/deaths')
def deaths():
    return jsonify(get_category('deaths'))