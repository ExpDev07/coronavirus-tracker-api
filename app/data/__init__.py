"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService

# Mapping of services to data-sources.
DATA_SOURCES = {"jhu": JhuLocationService(), "csbs": CSBSLocationService()}


def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return DATA_SOURCES.get(source.lower())
