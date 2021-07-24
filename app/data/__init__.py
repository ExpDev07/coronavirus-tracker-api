"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService
from ..utils.source_enum import SourceEnum

# Mapping of services to data-sources.
DATA_SOURCES = {
    SourceEnum.JHU: JhuLocationService(),
    SourceEnum.CSBS: CSBSLocationService(),
    SourceEnum.NYT: NYTLocationService(),
}


def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return DATA_SOURCES.get(source.lower())
