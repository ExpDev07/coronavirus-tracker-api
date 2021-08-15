"""app.data"""
from ..services.location.csbs import BasicLocationService
from ..services.location.csbslocations import CSBSLocations
from ..services.location.jhulocations import JHULocations
from ..services.location.nytlocations import NYTLocations

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