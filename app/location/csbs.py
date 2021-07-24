"""app.locations.csbs.py"""
from . import Location
from ..utils import Country

class CSBSLocation(Location):
    """
    A CSBS (county) location.
    """

    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, country, coordinates, last_updated, confirmed, deaths):
        super().__init__(
            # General info.
            id,
            country,
            coordinates,
            last_updated,
            # Statistics.
            confirmed=confirmed,
            deaths=deaths,
            recovered=0,
        )

        self.state = country.state
        self.county = country.county

    def serialize(self, timelines=False):  # pylint: disable=arguments-differ,unused-argument
        """
        Serializes the location into a dict.

        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize()

        # Update with new fields.
        serialized.update(
            {"state": self.country.state, "county": self.country.county,}
        )

        # Return the serialized location.
        return serialized
