"""
app.models.py
~~~~~~~~~~~~~
Reponse data models.
"""
import datetime as dt
from typing import Dict, List

import pydantic


class Totals(pydantic.BaseModel):
    confirmed: int
    deaths: int
    recovered: int


class Latest(pydantic.BaseModel):
    latest: Totals


class TimelineStats(pydantic.BaseModel):
    latest: int
    timeline: Dict[str, int]


class TimelinedLocation(pydantic.BaseModel):
    confirmed: TimelineStats
    deaths: TimelineStats
    recovered: TimelineStats


class Country(pydantic.BaseModel):
    coordinates: Dict
    country: str
    country_code: str
    id: int
    last_updated: dt.datetime
    latest: Totals
    province: str = ""
    timelines: TimelinedLocation = None  # FIXME


class AllLocations(pydantic.BaseModel):
    latest: Totals
    locations: List[Country]


class Location(pydantic.BaseModel):
    location: Country
