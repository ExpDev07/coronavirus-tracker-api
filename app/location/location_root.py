from csbs import CSBSLocation
from nyt import NYTLocation

class LocationRoot:


    def __init__(self, location):
        location = NYTLocationService


    def set_csbs(self, id, state, county, coordinates, last_updated, confirmed, deaths):
        self.location = CSBSLocation(id, state, county, coordinates, last_updated, confirmed, deaths)



    def set_nyt(self, id, state, county, coordinates, last_updated, timelines):
        self.location = NYTLocation( id, state, county, coordinates, last_updated, timelines)
