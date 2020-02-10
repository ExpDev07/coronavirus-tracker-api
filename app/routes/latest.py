from app import app
from app.data import get_data

@app.route('/latest')
def latest():
    return { }