"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService



class Source:
    
    def __init__(self, source):
        # Mapping of services to data-sources.
        self.__DATA_SOURCES_LIST = {
            "jhu": JhuLocationService(),
            "csbs": CSBSLocationService(),
            "nyt": NYTLocationService(),
        }
    
    def all_data_source(self):
        return self.__DATA_SOURCES_LIST
        
    def single_data_source(self, source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return self.__DATA_SOURCES_LIST.get(source.lower())
