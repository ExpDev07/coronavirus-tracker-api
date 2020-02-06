from flask import Flask

# Create the flask application.
app = Flask(__name__)

# Import assets, models, routes, etc. 
from . import routes