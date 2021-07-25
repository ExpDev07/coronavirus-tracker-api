"""app.data"""
from sys import int_info
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService


def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """

    jhuLocationService = JhuLocationService()
    csbsLocationService: CSBSLocationService()
    nytLocationService = NYTLocationService()

    return DataSource(jhuLocationService, csbsLocationService, nytLocationService).get(source.lower())

# Mapping of services to data-sources.


class DataSource:
    def __init__(self, jhuLocationService, csbsLocationService, nytLocationService):
        self.jhuLocationService = jhuLocationService
        self.csbsLocationService = csbsLocationService
        self.nytLocationService = nytLocationService

    def get(self, sourceName):
        if(sourceName == "jhu"):
            return self.jhuLocationService

        if(sourceName == "csbs"):
            return self.csbsLocationService

        return self.nytLocationService
