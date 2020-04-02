"""app.router.v1.confirmed.py"""
from ...services.location.jhu import get_category
from . import V1


@V1.get("/confirmed")
def confirmed():
    """Confirmed cases."""
    return get_category("confirmed")
