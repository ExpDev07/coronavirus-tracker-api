"""app.models.py"""
from typing import Dict, List

from pydantic import BaseModel


class Latest(BaseModel):
    """
    Latest model.
    """

    confirmed: int
    deaths: int
    recovered: int


class LatestResponse(BaseModel):
    """
    Response for latest.
    """

    latest: Latest


class Timeline(BaseModel):
    """
    Timeline model.
    """

    latest: int
    timeline: Dict[str, int] = {}


class Timelines(BaseModel):
    """
    Timelines model.
    """

    confirmed: Timeline
    deaths: Timeline
    recovered: Timeline


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
