"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService
from ..services.location import LocationServiceAbstractionImpl




# Mapping of services to data-sources.
DATA_SOURCES = {
    "jhu": LocationServiceAbstractionImpl(JhuLocationService()),
    "csbs": LocationServiceAbstractionImpl(CSBSLocationService()),
    "nyt": LocationServiceAbstractionImpl(NYTLocationService()),
}


def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return DATA_SOURCES.get(source.lower())
