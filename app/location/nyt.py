"""app.locations.nyt.py"""
from . import TimelinedLocation
from ..utils import Country

class NYTLocation(TimelinedLocation):
    """
    A NYT (county) Timelinedlocation.
    """

    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, country, coordinates, last_updated, timelines):
        super().__init__(id, country, coordinates, last_updated, timelines)

        self.state = country.state
        self.county = country.county

    def serialize(self, timelines=False):  # pylint: disable=arguments-differ,unused-argument
        """
        Serializes the location into a dict.

        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize(timelines)

        # Update with new fields.
        serialized.update(
            {"state": self.country.state, "county": self.country.county,}
        )

        # Return the serialized location.
        return serialized
