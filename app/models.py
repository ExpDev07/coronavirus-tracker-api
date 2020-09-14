"""app.models.py"""
from typing import Dict, List

from pydantic import BaseModel, validator


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

    timeline: Dict[str, int] = {}

    @validator("timeline")
    @classmethod
    def sort_timeline(cls, value):
        """Sort the timeline history before inserting into the model"""
        return dict(sorted(value.items()))

    @property
    def latest(self):
        """Get latest available history value."""
        return list(self.timeline.values())[-1] if self.timeline else 0

    def serialize(self):
        """
        Serialize the model into dict
        TODO: override dict() instead of using serialize
        """
        return {**self.dict(), "latest": self.latest}


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
