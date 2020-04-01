"""app.router.v1.deaths.py"""
from ...services.location.jhu import get_category
from . import V1


@V1.get("/deaths")
async def deaths():
    """Total deaths."""
    deaths = await get_category("deaths")

    return deaths
