"""app.router.v1.deaths.py"""
from ...services.location.jhu import get_category
from . import V1


@V1.get("/deaths")
def deaths():
    """Total deaths."""
    return get_category("deaths")
