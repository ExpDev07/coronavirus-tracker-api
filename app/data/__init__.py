from ..services.location.jhu import JhuLocationService

# Mapping of services to data-sources.
data_sources = {
    'jhu': JhuLocationService(),
}

def data_source(source: str):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return data_sources.get(source.lower())