"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService

class Data
    def __init__(self.source)
    # Mapping of services to data-sources.
        DATA_SOURCES = {
            "jhu": JhuLocationService(),
            "csbs": CSBSLocationService(),
            "nyt": NYTLocationService(),
        }


    def data_source(self):
        """
        Retrieves the provided data-source service.

        :returns: The service.
        :rtype: LocationService
        """
        return self.DATA_SOURCES.get(source.lower())
