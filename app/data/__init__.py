"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService

class Source:
    def __init__(self, source) -> None:
        self._sources = {"jhu","csbs","nyt"}

        if source == "csbs":
            self._service = CSBSLocationService()
        elif source == "nyt":
            self._service = NYTLocationService()
        else:
            self._service = JhuLocationService()

        if source not in self._sources:
            self._service = None
    
    def get_sources(self):
        """
        Return the list of available sources.
        """
        return self._sources

    def get_service(self):
        """
        Retrieves the provided data-source service.

        :returns: The service.
        :rtype: LocationService
        """
        return self._service
    
    