"""app.locations.nyt.py"""
from app.location import Location


class JHULocation(Location):
    """
    A JHU (county) Location.
    """

    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, country, state, coordinates, last_updated, timelines):
        super().__init__(
            # General info.
            id,
            country,
            state,
            coordinates,
            last_updated,
            confirmed=timelines.get("confirmed").latest or 0,
            deaths=timelines.get("deaths").latest or 0,
            recovered=timelines.get("recovered").latest or 0,
            timelines=timelines
        )
