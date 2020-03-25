"""
app.models.py
~~~~~~~~~~~~~
Reponse data models.
"""
from pydantic import BaseModel
from typing import Dict, List

class Latest(BaseModel):
    confirmed: int
    deaths: int
    recovered: int

class LatestResponse(BaseModel):
    latest: Latest

class Timeline(BaseModel):
    latest: int
    timeline: Dict[str, int] = {}

class Timelines(BaseModel):
    confirmed: Timeline
    deaths: Timeline
    recovered: Timeline

class Location(BaseModel):
    id: int
    country: str
    country_code: str
    county: str = ''
    province: str = ''
    last_updated: str # TODO use datetime.datetime type.
    coordinates: Dict
    latest: Latest
    timelines: Timelines = {}


class LocationsResponse(BaseModel):
    latest: Latest
    locations: List[Location] = []


class LocationResponse(BaseModel):
    location: Location
