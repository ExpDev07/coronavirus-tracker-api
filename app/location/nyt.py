"""app.locations.nyt.py"""
from . import TimelinedLocation


class NYTLocation(TimelinedLocation):
    """
    A NYT (county) Timelinedlocation.
    """

    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, state, county, coordinates, last_updated, timelines):
        super().__init__(id, "US", state, coordinates, last_updated, timelines)

        self.state = state
        self.county = county

    @decoratedSerialize(timelines=self.timelines, state=self.state, county=self.county)
    def serialize(self, inc_timelines=False):  # pylint: disable=arguments-differ,unused-argument
        """
        Serializes the location into a dict.
        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize(inc_timelines)

        # Return the serialized location.
        return serialized
