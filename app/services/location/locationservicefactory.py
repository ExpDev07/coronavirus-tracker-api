

from ..location.csbs import CSBSLocationService
from ..location.jhu import JhuLocationService
from ..location.nyt import NYTLocationService


class LocationServiceFactory:
    def create(location_service_name):
        lowercase_service_name = location_service_name.lower()
        if lowercase_service_name == 'csbs':
            return CSBSLocationService()
        elif lowercase_service_name == 'jhu':
            return JhuLocationService()
        elif lowercase_service_name == 'nyt':
            return NYTLocationService()
