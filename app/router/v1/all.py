"""app.router.v1.all.py"""
from ...services.location.jhu import get_category
from . import V1


@V1.get("/all")
async def all():  # pylint: disable=redefined-builtin
    """Get all the categories."""
    confirmed = await get_category("confirmed")
    deaths = await get_category("deaths")
    recovered = await get_category("recovered")

    return {
        # Data.
        "confirmed": confirmed,
        "deaths": deaths,
        "recovered": recovered,
        # Latest.
        "latest": {"confirmed": confirmed["latest"], "deaths": deaths["latest"], "recovered": recovered["latest"],},
    }
