"""
app.main.py
"""
import datetime as dt
import logging
import os
import reprlib

import pydantic
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import JSONResponse

from .core import create_app
from .data import data_source
from .models.latest import LatestResponse as Latest
from .models.location import LocationResponse as Location
from .models.location import LocationsResponse as Locations
from .router.v2 import router as v2router

# ############
# FastAPI App
# ############
LOGGER = logging.getLogger("api")

APP = FastAPI(
    title="Coronavirus Tracker",
    description="API for tracking the global coronavirus (COVID-19, SARS-CoV-2) outbreak. Project page: https://github.com/ExpDev07/coronavirus-tracker-api.",
    version="2.0.1",
    docs_url="/",
    redoc_url="/docs",
)

# #####################
# Middleware
#######################

# Enable CORS.
APP.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# TODO this could probably just be a FastAPI dependency.
@APP.middleware("http")
async def add_datasource(request: Request, call_next):
    """
    Attach the data source to the request.state.
    """
    # Retrieve the datas ource from query param.
    source = data_source(request.query_params.get("source", default="jhu"))

    # Abort with 404 if source cannot be found.
    if not source:
        return Response("The provided data-source was not found.", status_code=404)

    # Attach source to request.
    request.state.source = source

    # Move on...
    LOGGER.info(f"source provided: {source.__class__.__name__}")
    response = await call_next(request)
    return response


# ################
# Exception Handler
# ################


@APP.exception_handler(pydantic.error_wrappers.ValidationError)
async def handle_validation_error(request: Request, exc: pydantic.error_wrappers.ValidationError):
    """
    Handles validation errors.
    """
    return JSONResponse({"message": exc.errors()}, status_code=422)


# ################
# Routing
# ################


# Include routers.
# APP.include_router(router, prefix="/", tags=["v1"])
APP.include_router(v2router, prefix="/v2", tags=["v2"])

# mount the existing Flask app
# v1 @ /
APP.mount("/", WSGIMiddleware(create_app()))


# Running of app.
if __name__ == "__main__":
    uvicorn.run(
        "app.main:APP", host="127.0.0.1", port=int(os.getenv("PORT", 5000)), log_level="info",
    )
