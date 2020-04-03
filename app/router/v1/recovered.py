"""app.router.v1.recovered.py"""
from ...services.location.jhu import get_category
from . import V1


@V1.get("/recovered")
async def recovered():
    """Recovered cases."""
    recovered_data = await get_category("recovered")

    return recovered_data
