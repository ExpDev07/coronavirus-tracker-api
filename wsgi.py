from settings import *
from app import app

if __name__ == 'main':
    # Run the flask application on the specified port!
    app.run(port=PORT)