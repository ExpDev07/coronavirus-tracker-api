"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService
from ..services.location import LocationService

# Mapping of services to data-sources.
class DATA_SOURCES:
    DATA_SOURCES = {}

    def data(self)
    self.data_Sources['jhu'] = JhuLocationService()
    self.data_Sources['csbs'] = CSBSLocationService()
    self.data_Sources['nyt'] = NYTLocationService()

    def data_source(self, source : str)-> LocationService:
         return self.dataSource.get(source.lower())
