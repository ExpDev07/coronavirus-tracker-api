"""app.data"""
from ..services.location import getDataSources

# Mapping of services to data-sources.
DATA_SOURCES = getDataSources()


def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return DATA_SOURCES.get(source.lower())
