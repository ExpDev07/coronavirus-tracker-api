"""app.router.v2.latest.py"""
from fastapi import Request

from ...enums.sources import Sources
from ...models.latest import LatestResponse as Latest
from . import V2


@V2.get("/latest", response_model=Latest)
async def get_latest(request: Request, source: Sources = "jhu"):  # pylint: disable=unused-argument
    """
    Getting latest amount of total confirmed cases, deaths, and recoveries.
    """
    locations = await request.state.source.get_all()
    return {
        "latest": {
            "confirmed": sum(map(lambda location: location.confirmed, locations)),
            "deaths": sum(map(lambda location: location.deaths, locations)),
            "recovered": sum(map(lambda location: location.recovered, locations)),
        }
    }
