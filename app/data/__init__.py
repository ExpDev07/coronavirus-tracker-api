"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService

# Mapping of services to data-sources.


class DataSources:

    def __init__(self):
        """
        Sets __data_source's key-value pairs to be the data-source (key) and data-source service (value) for the supported sources (jhu, csbs, nyt)
        """
        self.__data_source = {
            "jhu": JhuLocationService(),
            "csbs": CSBSLocationService(),
            "nyt": NYTLocationService(),
        }

    def get_data_source(self, source):
        """
        Retrieves the provided data-source service.

        :returns: The service.
        :rtype: LocationService
        """
        return self.__data_source.get(source.lower())
