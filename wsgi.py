from settings import *
from app import app

# Run the application (server).
if __name__ == 'main':
    app.run(port=PORT, threaded=True)