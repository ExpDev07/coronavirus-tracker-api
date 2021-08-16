"""app.locations.csbs.py"""
from . import Location
from . import serialize

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

        self.state = state
        self.county = county

   
        


