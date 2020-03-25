"""
app.models.py
~~~~~~~~~~~~~
Reponse data models.
"""
from pydantic import BaseModel
from typing import Dict, List

class Totals(BaseModel):
    confirmed: int
    deaths: int
    recovered: int


class Latest(BaseModel):
    latest: Totals


class TimelineStats(BaseModel):
    latest: int
    timeline: Dict[str, int] = {}


class TimelinedLocation(BaseModel):
    confirmed: TimelineStats
    deaths: TimelineStats
    recovered: TimelineStats


class Country(BaseModel):
    id: int
    country: str
    country_code: str
    county: str = None
    province: str = ''
    last_updated: str # TODO use datetime.datetime type.
    coordinates: Dict
    latest: Totals
    timelines: TimelinedLocation = {}


class Locations(BaseModel):
    latest: Totals
    locations: List[Country] = []


class Location(BaseModel):
    location: Country
