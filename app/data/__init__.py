"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService

def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    s = source.lower()
    # return the singleton instance of the required service
    if s == 'jhu': 
        return JhuLocationService.getInstance()
    elif s == 'csbs': 
        return CSBSLocationService.getInstance()
    elif s == 'nyt': 
        return NYTLocationService.getInstance()
    else:
        return None
