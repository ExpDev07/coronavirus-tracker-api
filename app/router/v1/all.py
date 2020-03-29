from ...services.location.jhu import get_category
from . import router


@router.get("/all")
def all():
    # Get all the categories.
    confirmed = get_category("confirmed")
    deaths = get_category("deaths")
    recovered = get_category("recovered")

    return {
        # Data.
        "confirmed": confirmed,
        "deaths": deaths,
        "recovered": recovered,
        # Latest.
        "latest": {"confirmed": confirmed["latest"], "deaths": deaths["latest"], "recovered": recovered["latest"],},
    }
