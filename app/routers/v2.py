"""app.routers.v2"""
from typing import Any
from app.services.repo.metricsprovider import MetricsProvider
import enum

from fastapi import APIRouter, HTTPException, Request

from ..data import DATA_SOURCES
from ..models import LatestResponse, LocationResponse, LocationsResponse

V2 = APIRouter()
metrics_provider = MetricsProvider()


class Sources(str, enum.Enum):
    """
    A source available for retrieving data.
    """

    JHU = "jhu"
    CSBS = "csbs"
    NYT = "nyt"


@V2.get("/latest", response_model=LatestResponse)
async def get_latest(
    request: Request, source: Sources = Sources.JHU
):  # pylint: disable=unused-argument
    """
    Getting latest amount of total confirmed cases, deaths, and recoveries.
    """
    return await metrics_provider.get_latest_global(request.state.source)


# pylint: disable=unused-argument,too-many-arguments,redefined-builtin
@V2.get("/locations", response_model=LocationsResponse, response_model_exclude_unset=True)
async def get_locations(
    request: Request,
    source: Sources = "jhu",
    country_code: str = None,
    province: str = None,
    county: str = None,
    timelines: bool = False,
):
    """
    Getting the locations.
    """
    # All query paramameters.
    params = dict(request.query_params)

    # Remove reserved params.
    params.pop("source", None)
    params.pop("timelines", None)

    # # Retrieve all the locations.
    try:
        return await metrics_provider.get_available_locations(request.state.source, params, timelines)
    except Exception as err:
        raise HTTPException(404, str(err))




# pylint: disable=invalid-name
@V2.get("/locations/{id}", response_model=LocationResponse)
async def get_location_by_id(
    request: Request, id: int, source: Sources = Sources.JHU, timelines: bool = True
):
    """
    Getting specific location by id.
    """
    return await metrics_provider.get_location_by_id(request.state.source, id, timelines)


@V2.get("/sources")
async def sources():
    """
    Retrieves a list of data-sources that are availble to use.
    """
    return {"sources": list(DATA_SOURCES.keys())}
