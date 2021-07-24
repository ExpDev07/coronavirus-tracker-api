"""app.services.location"""
from abc import ABC, abstractmethod


class LocationService(ABC):
    """
    Service for retrieving locations.
    """

    @abstractmethod
    async def get_all(self):
        """
        Gets and returns all of the locations.

        :returns: The locations.
        :rtype: List[Location]
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, id):  # pylint: disable=redefined-builtin,invalid-name
        """
        Gets and returns location with the provided id.

        :returns: The location.
        :rtype: Location
        """
        raise NotImplementedError

class BASE_URLs(str):
    csbs = "https://facts.csbs.org/covid-19/covid19_county.csv"
    jhu = "https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/"
    nyt = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"


