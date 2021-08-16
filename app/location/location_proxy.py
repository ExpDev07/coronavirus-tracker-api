from .csbs import CSBSLocation
from .nyt import NYTLocation
from datetime import datetime
from datetime import timedelta



class CSBSLocationProxy:

    def __init__(self, id, state, county, coordinates, last_updated, confirmed, deaths):
        if confirmed >= 0 and deaths >= 0 and coordinates not None and last_updated > datetime.now() - timedelta(days=30):
            self.location = CSBSLocation(
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
        else:
            self.location = "Invalid information"


    def getInfo(self):
        return self.location


class NYTLocationProxy:

    def __init__(self, id, state, county, coordinates, last_updated, timelines):
        if coordinates not None and last_updated > datetime.now() - timedelta(days=30):
            self.location = NYTLocation(
                id, state, county, coordinates, last_updated, timelines
            )

        else:
            self.location = "Invalid Information"


    def getInfo(self):
        return self.location
