from flask import Blueprint, redirect, request, abort, current_app as app
from ..data import data_source

# Follow the import order to avoid circular dependency
api_v1 = Blueprint('api_v1', __name__, url_prefix='')

# API version 1.
from .v1 import confirmed, deaths, recovered, all

# Redirect to project page on index.
@app.route('/')
def index():
    return redirect('https://github.com/ExpDev07/coronavirus-tracker-api', 302)
