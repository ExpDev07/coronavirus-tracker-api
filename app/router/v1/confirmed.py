"""app.router.v1.confirmed.py"""
from ...services.location.jhu import get_category
from . import V1


@V1.get("/confirmed")
async def confirmed():
    """Confirmed cases."""
    confirmed = await get_category("confirmed")

    return confirmed
