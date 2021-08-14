"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService
from ..utils.singleton import Singleton


class DataSources(Singleton):
    """
    Class to represent the root of the aggregate containing the location services.
    """

    # Mapping of services to data-sources.
    __DATA_SOURCES_MAP = {
        "jhu": JhuLocationService(),
        "csbs": CSBSLocationService(),
        "nyt": NYTLocationService(),
    }

    __instance = None

    def __init__(self):
        pass

    def get_instance():
        if DataSources.__instance is None:
            DataSources.__instance = DataSources()
        return DataSources.__instance

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
