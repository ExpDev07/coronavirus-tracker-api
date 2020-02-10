import os

# Load enviroment variables from .env file.
from dotenv import load_dotenv
load_dotenv()

"""
The port to serve the app application on.
"""
PORT = int(os.getenv('port', 5000))