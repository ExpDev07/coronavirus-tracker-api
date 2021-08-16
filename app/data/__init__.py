"""app.data"""
from ..services.location.location_factory import LocationFactory

def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return LocationFactory.get_location(source)
