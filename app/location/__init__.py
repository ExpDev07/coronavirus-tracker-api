"""app.location"""
from ..coordinates import Coordinates
from ..utils import countries
from ..utils.populations import country_population

class Statistics:
    def __init__(self, confirmed=0, deaths=0, recovered=0):
        self.__confirmed = confirmed
        self.__deaths = deaths
        self.__recovered = recovered

    @property()
    def confirmed(self):
        return self.__confirmed
    
    @confirmed.setter
    def confirmed(self, value):
        self.__confirmed = value

    @property()
    def deaths(self):
        return self.__deaths

    @deaths.setter
    def deaths(self, value):
        self.__deaths = value

    @property()
    def recovered(self):
        return self.__recovered

    @recovered.setter
    def recovered(self, value):
        self.__recovered = value

# pylint: disable=redefined-builtin,invalid-name
class Location:  # pylint: disable=too-many-instance-attributes
    """
    A location in the world affected by the coronavirus.
    """

    def __init__(
        self, id, country, province, coordinates, last_updated, statistics
    ):  # pylint: disable=too-many-arguments
        # General info.
        self.id = id
        self.country = country.strip()
        self.province = province.strip()
        self.coordinates = coordinates

        # Last update.
        self.last_updated = last_updated

        # Statistics.
        self.statistics = statistics

    @property
    def country_code(self):
        """
        Gets the alpha-2 code represention of the country. Returns 'XX' if none is found.

        :returns: The country code.
        :rtype: str
        """
        return (countries.country_code(self.country) or countries.DEFAULT_COUNTRY_CODE).upper()

    @property
    def country_population(self):
        """
        Gets the population of this location.

        :returns: The population.
        :rtype: int
        """
        return country_population(self.country_code)

    def serialize(self):
        """
        Serializes the location into a dict.

        :returns: The serialized location.
        :rtype: dict
        """
        return {
            # General info.
            "id": self.id,
            "country": self.country,
            "country_code": self.country_code,
            "country_population": self.country_population,
            "province": self.province,
            # Coordinates.
            "coordinates": self.coordinates.serialize(),
            # Last updated.
            "last_updated": self.last_updated,
            # Latest data (statistics).
            "latest": {
                "confirmed": self.statistics.confirmed,
                "deaths": self.statistics.deaths,
                "recovered": self.statistics.recovered,
            },
        }


class TimelinedLocation(Location):
    """
    A location with timelines.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, id, country, province, coordinates, last_updated, statistics, timelines):
        super().__init__(
            # General info.
            id,
            country,
            province,
            coordinates,
            last_updated,
            # Statistics (retrieve latest from timelines).
            statistics
        )
        self.statistics.confirmed = timelines.get("confirmed").latest or 0
        self.statistics.deaths = timelines.get("deaths").latest or 0
        self.statistics.recovered = timelines.get("recovered").latest or 0
        # Set timelines.
        self.timelines = timelines

    # pylint: disable=arguments-differ
    def serialize(self, timelines=False):
        """
        Serializes the location into a dict.

        :param timelines: Whether to include the timelines.
        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize()

        # Whether to include the timelines or not.
        if timelines:
            serialized.update(
                {
                    "timelines": {
                        # Serialize all the timelines.
                        key: value.serialize()
                        for (key, value) in self.timelines.items()
                    }
                }
            )

        # Return the serialized location.
        return serialized
