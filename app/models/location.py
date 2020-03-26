from typing import Dict, List

from pydantic import BaseModel

from .latest import Latest
from .timeline import Timelines


class Location(BaseModel):
    """
    Location model.
    """

    id: int
    country: str
    country_code: str
    country_population: int = None
    province: str = ""
    county: str = ""
    last_updated: str  # TODO use datetime.datetime type.
    coordinates: Dict
    latest: Latest
    timelines: Timelines = {}


class LocationResponse(BaseModel):
    """
    Response for location.
    """

    location: Location


class LocationsResponse(BaseModel):
    """
    Response for locations.
    """

    latest: Latest
    locations: List[Location] = []
