from flask import jsonify
from ...data import data_sources
from ...routes import api_v2 as api

@api.route('/sources')
def sources():
    """
    Retrieves a list of data-sources that are availble to use.
    """
    return jsonify({
        'sources': list(data_sources.keys())
    })
