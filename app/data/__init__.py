"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService

# Mapping of services to data-sources.
DATA_SOURCES = [
    "jhu",
    "csbs",
    "nyt",
]
