from flask import Flask
from flask_cors import CORS

def create_app():
    """
    Construct the core application.
    """

    # Create flask app with CORS enabled.
    app = Flask(__name__)
    CORS(app)

    # Set app config from settings.
    app.config.from_pyfile('config/settings.py');

    with app.app_context():
        # Import routes.
        from . import routes

        # Return created app.
        return app