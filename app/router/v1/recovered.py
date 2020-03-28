# from flask import jsonify

# from ...routes import api_v1 as api
from ...services.location.jhu import get_category
from . import router


@router.get("/recovered")
def recovered():
    return {
        get_category("recovered")
    }
