"""app.routers.v3"""
import enum

from fastapi import APIRouter, HTTPException, Request

from ..data import DATA_SOURCES
from ..models import LatestResponse, LocationResponse, LocationsResponse
from ..location import Location

V3 = APIRouter()


class Sources(str, enum.Enum):
    """
    A source available for retrieving data.
    """

    JHU = "jhu"
    CSBS = "csbs"
    NYT = "nyt"


class Source():
    """
    A datasource and its location data.
    """

    def __init__(self, name: str, locations: list[Location]):
        self.name = name
        self.locations = locations


@V3.get("/sources")
async def sources():
    """
    Retrieves a list of data-sources that are availble to use.
    """
    return {"sources": list(DATA_SOURCES.keys())}


@V3.get("/sources/{name}")
async def data_source(
    request: Request,
    source: Sources,
    country_code: str = None,
    province: str = None,
    county: str = None,
    timelines: bool = False,
):
    # All query paramameters.
    params = dict(request.query_params)

    # Remove reserved params.
    params.pop("source", None)
    params.pop("timelines", None)

    source = Sources(source)

    locations = await source.get_all()

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

    data_source = Source(source, locations)

    return {
        "name": data_source.name,
        "locations": [location.serialize(timelines) for location in data_source.locations],
    }
