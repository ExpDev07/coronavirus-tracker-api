from ..services.location.jhu import JhuLocationService
from ..services.location.csbs import CSBSLocationService

# Mapping of services to data-sources.
data_sources = {
    'jhu': JhuLocationService(),
    'csbs': CSBSLocationService()
}

def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return data_sources.get(source.lower())