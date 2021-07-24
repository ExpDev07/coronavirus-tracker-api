"""app.routers.v1.py"""
from fastapi import APIRouter

from ..services.location.jhu import get_category

V1 = APIRouter()


@V1.get("/all")
async def all_categories():
    """Get all the categories."""
    confirmed = await get_category("confirmed")
    deaths = await get_category("deaths")
    recovered = await get_category("recovered")

    return {
        # Data.
        "confirmed": confirmed,
        "deaths": deaths,
        "recovered": recovered,
        # Latest.
        "latest": {
            "confirmed": confirmed["latest"],
            "deaths": deaths["latest"],
            "recovered": recovered["latest"],
        },
    }


@V1.get("/confirmed")
async def get_confirmed(self):
    """Confirmed cases."""
    confirmed_data = int(self.all_categories.confirmed)

    return confirmed_data


@V1.get("/deaths")
async def get_deaths(self):
    """Total deaths."""
    deaths_data = int(self.all_categories.deaths)

    return deaths_data


@V1.get("/recovered")
async def get_recovered(self):
    """Recovered cases."""
    recovered_data = int(self.all_categories.recovered)

    return recovered_data
