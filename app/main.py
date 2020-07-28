"""
app.main.py
"""
import logging

import pydantic
import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request, Response, openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from scout_apm.async_.starlette import ScoutMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from .config import get_settings
from .data import data_source
from .routers import V1, V2
from .utils.httputils import setup_client_session, teardown_client_session

# ############
# FastAPI App
# ############
LOGGER = logging.getLogger("api")

SETTINGS = get_settings()

if SETTINGS.sentry_dsn:  # pragma: no cover
    sentry_sdk.init(dsn=SETTINGS.sentry_dsn)

APP = FastAPI(
    title="Coronavirus Tracker",
    description=(
        "API for tracking the global coronavirus (COVID-19, SARS-CoV-2) outbreak."
        " Project page: https://github.com/ExpDev07/coronavirus-tracker-api."
    ),
    version="2.0.3",
    docs_url=None,
    redoc_url=None,
    on_startup=[setup_client_session],
    on_shutdown=[teardown_client_session],
)

# #####################
# Middleware
#######################

# Scout APM
if SETTINGS.scout_name:  # pragma: no cover
    LOGGER.info(f"Adding Scout APM middleware for `{SETTINGS.scout_name}`")
    APP.add_middleware(ScoutMiddleware)
else:
    LOGGER.debug("No SCOUT_NAME config")

# Sentry Error Tracking
if SETTINGS.sentry_dsn:  # pragma: no cover
    LOGGER.info("Adding Sentry middleware")
    APP.add_middleware(SentryAsgiMiddleware)

# Enable CORS.
APP.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)
APP.add_middleware(GZipMiddleware, minimum_size=1000)


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
    LOGGER.debug(f"source provided: {source.__class__.__name__}")
    response = await call_next(request)
    return response


# ################
# Exception Handler
# ################


@APP.exception_handler(pydantic.error_wrappers.ValidationError)
async def handle_validation_error(
    request: Request, exc: pydantic.error_wrappers.ValidationError
):  # pylint: disable=unused-argument
    """
    Handles validation errors.
    """
    return JSONResponse({"message": exc.errors()}, status_code=422)


# ################
# Routing
# ################


# Include routers.
APP.include_router(V1, prefix="", tags=["v1"])
APP.include_router(V2, prefix="/v2", tags=["v2"])
APP.mount("/static", StaticFiles(directory="static"), name="static")

# ##############
# Swagger/Redocs
# ##############


@APP.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    """Serve Swagger UI."""
    return openapi.docs.get_swagger_ui_html(
        openapi_url=APP.openapi_url,
        title=f"{APP.title} - Swagger UI",
        oauth2_redirect_url=APP.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@APP.get("/docs", include_in_schema=False)
async def redoc_html():
    """Serve ReDoc UI."""
    return openapi.docs.get_redoc_html(
        openapi_url=APP.openapi_url, title=f"{APP.title} - ReDoc", redoc_js_url="/static/redoc.standalone.js",
    )


# Running of app.
if __name__ == "__main__":
    uvicorn.run(
        "app.main:APP", host="127.0.0.1", port=SETTINGS.port, log_level="info",
    )
