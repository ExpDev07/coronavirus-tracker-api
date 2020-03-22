"""
app.main.py
"""
import datetime as dt
import logging
import os
import reprlib
from typing import Dict, List

import fastapi
import pydantic
import uvicorn
from fastapi.middleware.wsgi import WSGIMiddleware

from .data import data_source
from .core import create_app

# #################################
# Models
# #################################


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


# ################
# Dependencies
# ################


# ############
# FastAPI App
# ############
LOGGER = logging.getLogger("api")

APP = fastapi.FastAPI(
    title="Coronavirus Tracker",
    description="API for tracking the global coronavirus (COVID-19, SARS-CoV-2) outbreak.",
    version="2.1.0",
    prefix="/v2-1",
    docs_url="/v2-1",
    redoc_url="/docs",
)

# #####################
# Middleware
#######################


# TODO this could probably just be a FastAPI dependency
@APP.middleware("http")
async def add_datasource(request: fastapi.Request, call_next):
    """Attach the data source to the request.state."""
    source = request.query_params.get("source", default="jhu")
    request.state.source = data_source(source)
    LOGGER.info(f"source: {request.state.source.__class__.__name__}")
    response = await call_next(request)
    return response


# ################
# Exception Handler
# ################


@APP.exception_handler(pydantic.error_wrappers.ValidationError)
async def handle_validation_error(
    request: fastapi.Request, exc: pydantic.error_wrappers.ValidationError
):
    return fastapi.responses.JSONResponse({"message": exc.errors()}, status_code=422)


# ################
# Routes
# ################


@APP.get("/latest", response_model=Latest)
def get_latest(request: fastapi.Request):
    """Getting latest amount of total confirmed cases, deaths, and recoveries."""
    locations = request.state.source.get_all()
    return {
        "latest": {
            "confirmed": sum(map(lambda location: location.confirmed, locations)),
            "deaths": sum(map(lambda location: location.deaths, locations)),
            "recovered": sum(map(lambda location: location.recovered, locations)),
        }
    }


@APP.get("/locations", response_model=AllLocations)
def get_all_locations(
    request: fastapi.Request, country_code: str = None, timelines: int = 0
):
    # Retrieve all the locations.
    locations = request.state.source.get_all()

    # Filtering my country code if provided.
    if country_code:
        locations = list(
            filter(
                lambda location: location.country_code == country_code.upper(),
                locations,
            )
        )
    return {
        "latest": {
            "confirmed": sum(map(lambda location: location.confirmed, locations)),
            "deaths": sum(map(lambda location: location.deaths, locations)),
            "recovered": sum(map(lambda location: location.recovered, locations)),
        },
        "locations": [location.serialize(timelines) for location in locations],
    }


@APP.get("/locations/{id}", response_model=Location)
def get_location_by_id(request: fastapi.Request, id: int, timelines: int = 1):
    return {"location": request.state.source.get(id).serialize(timelines)}

# mount the existing Flask app to /v2
APP.mount("/v2", WSGIMiddleware(create_app()))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:APP",
        host="127.0.0.1",
        port=int(os.getenv("PORT", 5000)),
        log_level="info",
    )
