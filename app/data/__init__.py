"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService
from ..services.location import LocationService

# Mapping of services to data-sources.
class DATA_SOURCES:
    data_SOURCES = {}

    def data(self):
        self.data_SOURCES['jhu'] = JhuLocationService()
        self.data_SOURCES['csbs'] = CSBSLocationService()
        self.data_SOURCES['nyt'] = NYTLocationService()

    def data_source(self, source: str)-> LocationService:

         return self.data_SOURCES.get(source.lower())
