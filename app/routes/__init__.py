from flask import Blueprint, redirect, request, current_app as app
from ..data import data_source

# Follow the import order to avoid circular dependency
api_v1 = Blueprint('api_v1', __name__, url_prefix='')
api_v2 = Blueprint('api_v2', __name__, url_prefix='/v2')

# API version 2.
from .v2 import locations, latest

# API version 1.
from .v1 import confirmed, deaths, recovered, all

# Redirect to project page on index.
@app.route('/')
def index():
    return redirect('https://github.com/ExpDev07/coronavirus-tracker-api', 302)

# Middleware for picking data source.
@api_v2.before_request
def datasource():
    """
    Attaches the datasource to the request.
    """
    # Retrieve the datas ource from query param.
    source = request.args.get('source', type=str, default='jhu')

    # Attach source to request and return it.
    request.source = data_source(source)
    pass
