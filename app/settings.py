import os

# Load enviroment variables from .env file.
from dotenv import load_dotenv
load_dotenv()

"""
The port to serve the app application on.
"""
PORT = int(os.getenv('port', 5000))

"""
The id found in the URL of the Google Spreadsheet.
"""
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', '1wQVypefm946ch4XDp37uZ-wartW4V7ILdg-qYiDXUHM')

"""
The API key for your Google Cloud that has the Google Sheets API enabled (https://developers.google.com/sheets/api).
"""
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')