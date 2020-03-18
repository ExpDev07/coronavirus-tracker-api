from flask import redirect, current_app as app

# API version 1.
from .v1 import confirmed, deaths, recovered, all

# API version 2.
from .v2 import locations, latest

# Redirect to project page on index.
@app.route('/')
def index():
    return redirect('https://github.com/ExpDev07/coronavirus-tracker-api', 302)