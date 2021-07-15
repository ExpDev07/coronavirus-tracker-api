"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService
from ..services.location import LocationService

class DataSource:
    __DATA_SOURCES = {}

    def __init__(self):
        self.__DATA_SOURCES['jhu'] = JhuLocationService()
        self.__DATA_SOURCES['csbs'] = CSBSLocationService()
        self.__DATA_SOURCES['nyt'] = NYTLocationService()

    # Mapping of services to data-sources.
    @classmethod
    def get_data_source(self, source: str) -> LocationService:
        return self.__DATA_SOURCES.get(source.lower())

    @classmethod
    def add_data_source(self, source: str, reference_to_source: LocationService) -> None:
        self.__DATA_SOURCES[source] = reference_to_source
    
    @classmethod
    def get_all_sources(self) -> dict:
        return self.__DATA_SOURCES