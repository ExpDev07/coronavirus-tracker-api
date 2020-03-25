from fastapi import Request
from . import router
from ..enums.sources import Sources
from ..models.latest import LatestResponse as Latest


@router.get("/latest", response_model=Latest)
def get_latest(request: Request, source: Sources = "jhu"):
    """
    Getting latest amount of total confirmed cases, deaths, and recoveries.
    """
    locations = request.state.source.get_all()
    return {
        "latest": {
            "confirmed": sum(map(lambda location: location.confirmed, locations)),
            "deaths": sum(map(lambda location: location.deaths, locations)),
            "recovered": sum(map(lambda location: location.recovered, locations)),
        }
    }
