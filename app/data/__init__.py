"""app.data"""
from ..services.location.basiclocationservice import BasicLocationService
from ..services.location.csbs import CSBSLocations
from ..services.location.jhu import JHULocations
from ..services.location.nyt import NYTLocations

# Mapping of services to data-sources.
DATA_SOURCES = {
    "jhu": BasicLocationService(JHULocations()),
    "csbs": BasicLocationService(CSBSLocations()),
    "nyt": BasicLocationService(NYTLocations()),
}


def data_source(source):
    """
    Retrieves the provided data-source service.
    :returns: The service.
    :rtype: LocationService
    """
    return DATA_SOURCES.get(source.lower())