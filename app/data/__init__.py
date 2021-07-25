"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService

# Mapping of services to data-sources.
DATA_SOURCES = {
    "jhu": JhuLocationService(),
    "csbs": CSBSLocationService(),
    "nyt": NYTLocationService(),
}

class DataSourceRequest:
    def __init__(self, request): # request is of Obj reference of Reqeust from FastAPI
        self.request = request 
        
    def get_data_source(self):
        """
        Retrieves the provided data-source service.

        :returns: The service.
        :rtype: LocationService
        """
        request_source = self.request.query_params.get("source", default="jhu") # gets source parameters 
        return DATA_SOURCES.get(request_source.lower())
