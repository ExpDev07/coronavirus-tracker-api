"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService


class DataSources:
    """
    Class to represent the root of the aggregate containing the location services.
    """

    # Mapping of services to data-sources.
    __DATA_SOURCES_MAP = {
        "jhu": JhuLocationService(),
        "csbs": CSBSLocationService(),
        "nyt": NYTLocationService(),
    }

    def __init__(self):
        pass

    def get_data_source(self, source):
        """
        Retrieves the provided data-source service.

        :returns: The service.
        :rtype: LocationService
        """
        return self.__DATA_SOURCES_MAP.get(source.lower())

    def get_data_sources(self):
        """
            Retrieves a dict of all data sources.

            :returns: The dictionary of data sources.
            :rtype: dict
        """
        return self.__DATA_SOURCES_MAP
