# from flask import jsonify

# from ...routes import api_v1 as api
from ...services.location.jhu import get_category
from . import router


@router.get("/confirmed")
def confirmed():
    
    return {
        get_category("confirmed")
    }
