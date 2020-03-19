from flask import redirect, current_app as app

#follow the import order to avoid circular dependency
from flask import Blueprint
rest_api_v1 = Blueprint("rest_api_v1", __name__, url_prefix="")
rest_api_v2 = Blueprint("rest_api_v2", __name__, url_prefix="/v2")

# API version 2.
from .v2 import locations, latest

# API version 1.
from .v1 import confirmed, deaths, recovered, all

# Redirect to project page on index.
@app.route('/')
def index():
    return redirect('https://github.com/ExpDev07/coronavirus-tracker-api', 302)
