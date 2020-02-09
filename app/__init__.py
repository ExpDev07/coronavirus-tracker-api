from flask import Flask
from flask_cors import CORS
from app.settings import *
from app.location import get_locations

# Create the flask application.
app = Flask(__name__)
CORS(app)

# Import assets, models, routes, etc. 
from . import routes

# Run the application (server).
if __name__ == 'main':
    app.run(port=PORT, threaded=True)