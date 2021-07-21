"""app.locations.csbs.py"""
from . import Location


class CSBSLocation(Location):
    """
    A CSBS (county) location.
    """

    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, state, county, coordinates, last_updated, confirmed, deaths):
        super().__init__(
            # General info.
            id,
            "US",
            state,
            coordinates,
            last_updated,
            # Statistics.
            confirmed=confirmed,
            deaths=deaths,
            recovered=0,
        )

        self._state = state
        self._county = county

    @property
    def state(self):
        """
        Gets the name of the state.

        :returns: The name of the state.
        :rtype: str
        """
        return self._state

    @property
    def county(self):
        """
        Gets the name of the county.

        :returns: The name of the county.
        :rtype: str
        """
        return self._county

    def serialize(self, timelines=False):  # pylint: disable=arguments-differ,unused-argument
        """
        Serializes the location into a dict.

        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize()

        # Update with new fields.
        serialized.update(
            {"state": self._state, "county": self._county,}
        )

        # Return the serialized location.
        return serialized
