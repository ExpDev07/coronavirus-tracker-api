"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService

# Mapping of services to data-sources.
class DATASOURCES:
    __data_sources = {}
    def __init__(self):
        self.__date_sources = {
            "jhu": JhuLocationService(),
            "csbs": CSBSLocationService(),
            "nyt": NYTLocationService(),
        }


def get_data_sources(self, source: str):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return self.__data_sources.get(source.lower())
