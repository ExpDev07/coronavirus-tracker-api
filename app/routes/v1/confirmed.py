from flask import jsonify
from flask import current_app as app
from ...services.location.jhu import get_category

@app.route('/confirmed')
def confirmed():
    return jsonify(get_category('confirmed'))