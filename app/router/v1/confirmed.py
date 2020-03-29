# from flask import jsonify
import json

# from ...routes import api_v1 as api
from ...services.location.jhu import get_category
from . import router


@router.get("/confirmed")
def confirmed():
    confirmed = get_category("confirmed")

    return confirmed
