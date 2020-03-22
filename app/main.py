"""
app.main.py
"""
import os
import datetime as dt
from typing import Dict

import fastapi
import pydantic
import uvicorn


class Stats(pydantic.BaseModel):
    confirmed: int
    deaths: int
    recovered: int


class Latest(pydantic.BaseModel):
    latest: Stats


class Country(pydantic.BaseModel):
    id: int
    country: str
    country_code: str
    province: str = None
    last_updated: dt.datetime = None
    coordinates: Dict = None
    latest: Stats = None
    timelines: Dict = None


APP = fastapi.FastAPI(
    title="Coronavirus Tracker",
    description="API for tracking the global coronavirus (COVID-19, SARS-CoV-2) outbreak.",
    version="3.0.0",
    prefix="/v3",
    docs_url="/v3",
    redoc_url="/docs",
)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:APP",
        host="127.0.0.1",
        port=int(os.getenv("PORT", 5000)),
        log_level="info",
    )
