"""app.locations.nyt.py"""
from app.location import Location


class NYTLocation(Location):
    """
    A NYT (county) Location.
    """

    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, state, county, coordinates, last_updated, timelines):
        super().__init__(
            # General info.
            id,
            "US",
            state,
            coordinates,
            last_updated,
            confirmed=timelines.get("confirmed").latest or 0,
            deaths=timelines.get("deaths").latest or 0,
            recovered=timelines.get("recovered").latest or 0,
            timelines=timelines
        )

        self.state = state
        self.county = county

    def serialize(self, timelines=False):  # pylint: disable=arguments-differ,unused-argument
        """
        Serializes the location into a dict.

        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize(timelines)

        # Update with new fields.
        serialized.update(
            {"state": self.state, "county": self.county,}
        )

        # Return the serialized location.
        return serialized
