

from ..location.csbs import CSBSLocationService
from ..location.jhu import JhuLocationService
from ..location.nyt import NYTLocationService


NEW_YORK_TIMES = 'nyt'
JOHNS_HOPKINS_UNIVERSITY = 'jhu'
CSBS = 'csbs'


class LocationServiceFactory:
    def create(location_service_name):
        lowercase_service_name = location_service_name.lower()
        if lowercase_service_name == CSBS:
            return CSBSLocationService()
        elif lowercase_service_name == JOHNS_HOPKINS_UNIVERSITY:
            return JhuLocationService()
        elif lowercase_service_name == NEW_YORK_TIMES:
            return NYTLocationService()
