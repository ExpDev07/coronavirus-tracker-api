from flask import Blueprint, redirect, current_app as app

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
