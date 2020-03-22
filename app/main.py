"""
app.main.py
"""
import os
import datetime as dt
from typing import Dict, List

import fastapi
import pydantic
import uvicorn


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
    timelines: TimelinedLocation


class AllLocations(pydantic.BaseModel):
    latest: Totals
    locations: List[Country]


class Location(pydantic.BaseModel):
    location: Country


APP = fastapi.FastAPI(
    title="Coronavirus Tracker",
    description="API for tracking the global coronavirus (COVID-19, SARS-CoV-2) outbreak.",
    version="3.0.0",
    prefix="/v3",
    docs_url="/v3",
    redoc_url="/docs",
)


@APP.get("/latest", response_model=Latest)
def get_latest():
    sample_data = {"latest": {"confirmed": 197146, "deaths": 7905, "recovered": 80840}}
    return sample_data


@APP.get("/locations")
def get_all_locations(country_code: str = None, timelines: int = None):
    return


@APP.get("/locations/{id}")
def get_location_by_id(id: int):
    return


if __name__ == "__main__":
    uvicorn.run(
        "app.main:APP",
        host="127.0.0.1",
        port=int(os.getenv("PORT", 5000)),
        log_level="info",
    )
