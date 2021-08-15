"""app.data"""
from ..services.location import LocationService
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService

class dataSourceFactory():
    def getDataSource():
        return LocationService()

class JhuFactory(dataSourceFactory):
    def getDataSource():
        return JhuLocationService()

class CSBSFactory(dataSourceFactory):
    def getDataSource():
        return CSBSLocationService()

class NYTFactory(dataSourceFactory):
    def getDataSource():
        return NYTLocationService()


# Mapping of factories to data-sources.
DATA_SOURCES = {
    "jhu": JhuFactory(),
    "csbs": CSBSFactory(),
    "nyt": NYTFactory(),
}

def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return DATA_SOURCES.get(source.lower()).getDataSource()
