"""
app.main.py
"""
import datetime as dt
import enum
import logging
import os
import reprlib
from typing import Dict, List

import fastapi
import pydantic
import uvicorn
from fastapi.middleware.wsgi import WSGIMiddleware

from . import models
from .core import create_app
from .data import data_source, data_sources

# ################
# Dependencies
# ################


class Sources(str, enum.Enum):
    jhu = "jhu"
    csbs = "csbs"


# ############
# FastAPI App
# ############
LOGGER = logging.getLogger("api")

APP = fastapi.FastAPI(
    title="Coronavirus Tracker",
    description="API for tracking the global coronavirus (COVID-19, SARS-CoV-2) outbreak.",
    version="2.0.1",
    docs_url="/",
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

V2 = fastapi.APIRouter()


@V2.get("/latest", response_model=models.Latest)
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


@V2.get(
    "/locations", response_model=models.AllLocations, response_model_exclude_unset=True
)
def get_all_locations(
    request: fastapi.Request,
    country_code: str = None,
    timelines: int = 0,
    source: Sources = "jhu",
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
    # FIXME: timelines are not showing up
    return {
        "latest": {
            "confirmed": sum(map(lambda location: location.confirmed, locations)),
            "deaths": sum(map(lambda location: location.deaths, locations)),
            "recovered": sum(map(lambda location: location.recovered, locations)),
        },
        "locations": [location.serialize(timelines) for location in locations],
    }


@V2.get("/locations/{id}", response_model=models.Location)
def get_location_by_id(request: fastapi.Request, id: int, timelines: int = 1):
    return {"location": request.state.source.get(id).serialize(timelines)}


@V2.get('/sources')
async def sources():
    """
    Retrieves a list of data-sources that are availble to use.
    """
    return {
        'sources': list(data_sources.keys())
    }


APP.include_router(V2, prefix="/v2-beta", tags=["v2"])
# mount the existing Flask app
# v1 @ /
# v2 @ /v2
APP.mount("/", WSGIMiddleware(create_app()))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:APP",
        host="127.0.0.1",
        port=int(os.getenv("PORT", 5000)),
        log_level="info",
    )
