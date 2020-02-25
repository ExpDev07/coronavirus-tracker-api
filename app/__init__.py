from flask import Flask
from flask import json
from flask_cors import CORS
from app.settings import *

# Create the flask application.
app = Flask(__name__)
CORS(app)

# Import assets, models, routes, etc. 
from . import routes

@app.after_request
def set_source(response):
    """
    Attaches the source to the response.
    """
    body = response.get_json()

    # Attach only if we're dealing with a dict.
    if type(body) is dict:
        body['source'] = 'https://github.com/ExpDev07/coronavirus-tracker-api'
        response.data = json.dumps(body)
    
    # Finally, return the modified response.
    return response

# Run the application (server).
if __name__ == 'main':
    app.run(port=PORT, threaded=True)