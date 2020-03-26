from fastapi import HTTPException, Request

from ..enums.sources import Sources
from ..models.location import LocationResponse as Location
from ..models.location import LocationsResponse as Locations
from . import router


@router.get("/locations", response_model=Locations, response_model_exclude_unset=True)
def get_locations(
    request: Request,
    source: Sources = "jhu",
    country_code: str = None,
    province: str = None,
    county: str = None,
    timelines: bool = False,
):
    """
    Getting the locations.
    """
    # All query paramameters.
    params = dict(request.query_params)

    # Remove reserved params.
    params.pop("source", None)
    params.pop("timelines", None)

    # Retrieve all the locations.
    locations = request.state.source.get_all()

    # Attempt to filter out locations with properties matching the provided query params.
    for key, value in params.items():
        # Clean keys for security purposes.
        key = key.lower()
        value = value.lower().strip("__")

        # Do filtering.
        try:
            locations = [location for location in locations if str(getattr(location, key)).lower() == str(value)]
        except AttributeError:
            pass
        if not locations:
            raise HTTPException(404, detail=f"Source `{source}` does not have the desired location data.")

    # Return final serialized data.
    return {
        "latest": {
            "confirmed": sum(map(lambda location: location.confirmed, locations)),
            "deaths": sum(map(lambda location: location.deaths, locations)),
            "recovered": sum(map(lambda location: location.recovered, locations)),
        },
        "locations": [location.serialize(timelines) for location in locations],
    }


@router.get("/locations/{id}", response_model=Location)
def get_location_by_id(request: Request, id: int, source: Sources = "jhu", timelines: bool = True):
    """
    Getting specific location by id.
    """
    return {"location": request.state.source.get(id).serialize(timelines)}
