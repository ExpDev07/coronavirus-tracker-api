"""app.router.v1.recovered.py"""
from ...services.location.jhu import get_category
from . import V1


@V1.get("/recovered")
def recovered():
    """Recovered cases."""
    return get_category("recovered")
