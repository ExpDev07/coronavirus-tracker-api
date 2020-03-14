from flask import Flask
from flask_cors import CORS
from . import settings

if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0')

def create_app():
    """
    Construct the core application.
    """

    # Create flask app with CORS enabled.
    app = Flask(__name__)
    CORS(app)

    # Set app config from settings.
    app.config.from_pyfile('settings.py');

    with app.app_context():
        # Import routes.
        from . import routes

        # Return created app.
        return app