"""app.routers.v2"""
import enum

from fastapi import APIRouter, HTTPException, Request

from ..data import DATA_SOURCES
from ..models import LatestResponse, LocationResponse, LocationsResponse

V2 = APIRouter()


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
    locations = await request.state.source.get_all()
    return {
        "latest": {
            "confirmed": sum(map(lambda location: location.confirmed, locations)),
            "deaths": sum(map(lambda location: location.deaths, locations)),
            "recovered": sum(map(lambda location: location.recovered, locations)),
        }
    }


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

    # Retrieve all the locations.
    locations = await request.state.source.get_all()

    # Attempt to filter out locations with properties matching the provided query params.
    for key, value in params.items():
        # Clean keys for security purposes.
        key = key.lower()
        value = value.lower().strip("__")

        # Do filtering.
        try:
            locations = [
                location
                for location in locations
                if str(getattr(location, key)).lower() == str(value)
            ]
        except AttributeError:
            pass
        if not locations:
            raise HTTPException(
                404, detail=f"Source `{source}` does not have the desired location data.",
            )

    # Return final serialized data.
    return {
        "latest": {
            "confirmed": sum(map(lambda location: location.confirmed, locations)),
            "deaths": sum(map(lambda location: location.deaths, locations)),
            "recovered": sum(map(lambda location: location.recovered, locations)),
        },
        "locations": [location.serialize(timelines) for location in locations],
    }


# pylint: disable=invalid-name
@V2.get("/locations/{id}", response_model=LocationResponse)
async def get_location_by_id(
    request: Request, id: int, source: Sources = Sources.JHU, timelines: bool = True
):
    """
    Getting specific location by id.
    """
    location = await request.state.source.get(id)
    
    return {"location": location.serialize(timelines)}


@V2.get("/sources")
async def sources():
    """
    Retrieves a list of data-sources that are availble to use.
    """
    return {"sources": list(DATA_SOURCES.keys())}
