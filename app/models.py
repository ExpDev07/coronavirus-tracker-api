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


class Timeline(basemodel):  

  def __init__(self, timeline):  

   self.timeline = timeline  

 

class Timelines(basemodel):  

  def __init__(self, confirmed, deaths, recovered):  

   self.confirmed = confirmed  

   self.deaths = deaths  

   self.recovered = recovered  

 

  if __name__ == "__main__":  

   confirm = Timeline({'Sat':10, 'Wed':20})  

   death = Timeline({'Sat':10, 'Wed':20}) 

   recovered = Timeline({'Sat':10, 'Wed':20})  

   timelines_1 = Timelines(confirm, death, recovered) 


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
