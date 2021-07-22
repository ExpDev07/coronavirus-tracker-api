"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService
from ..services.location import LocationService

# Mapping of services to data-sources.
class DATA_SOURCES:
    DATA_SOURCES = {}

    def data(self)
    self.DATA_SOURCES['jhu'] = JhuLocationService()
    self.DATA_SOURCES['csbs'] = CSBSLocationService()
    self.DATA_SOURCES['nyt'] = NYTLocationService()

    def data_source(self, source : str)-> LocationService:
         return self.DATA_SOURCES.get(source.lower())
