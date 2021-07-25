"""app.data"""
from ..services.location.csbs import CSBSGateway
from ..services.location.jhu import JHUGateway
from ..services.location.nyt import NYTGateway

from ..services.location import LocationGateway, LocationService



class ServiceFactory:

    def create_service(self, source_name: str):
        source_name = source_name.lower()

        gateway: LocationGateway

        if source_name == 'jhu':
            gateway = JHUGateway("https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/")
        elif source_name == 'csbs':
            gateway = CSBSGateway("https://facts.csbs.org/covid-19/covid19_county.csv")
        elif source_name == 'nyt':
            gateway = NYTGateway("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")

        service: LocationService = LocationService(gateway)


# Mapping of services to data-sources.
DATA_SOURCES = {
    "jhu": ServiceFactory().create_service("jhu"),
    "csbs": ServiceFactory().create_service("csbs"),
    "nyt": ServiceFactory().create_service("nyt"),
}


def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return DATA_SOURCES.get(source.lower())




