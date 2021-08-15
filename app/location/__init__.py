"""app.location"""
from ..coordinates import Coordinates
from ..utils import countries
from ..utils.populations import country_population


class Location:
    def __init__(
            self, id, country, province, coordinates, last_updated, confirmed, deaths, recovered,
        ):  # pylint: disable=too-many-arguments
            # General info.
            self.id = id
            self.country = country.strip()
            self.province = province.strip()
            self.coordinates = coordinates

            # Last update.
            self.last_updated = last_updated

            # Statistics.
            self.confirmed = confirmed
            self.deaths = deaths
            self.recovered = recovered

    def add(self, location):
        pass

    def remove(self, location):
        pass

    def country_code(self):
        pass

    def country_population(self):
        pass

    def serialize(self):
        pass


class Province(Location):
    countries = None

    def __init__(
                self, id, country, province, coordinates, last_updated, confirmed, deaths, recovered,
            ):  # pylint: disable=too-many-arguments
                # General info.
                self.id = id
                self.country = country.strip()
                self.province = None
                self.coordinates = coordinates

                # Last update.
                self.last_updated = last_updated

                # Statistics.
                self.confirmed = confirmed
                self.deaths = deaths
                self.recovered = recovered
                self.countries = []

    def add(self, location):
        self.countries.append(location)

    def remove(self, location):
        self.countries.remove(location)

    def country_code(self):
        countries_code = []
        for i in countries
            countries_code.append(countries.country_code(i))
        return countries_code

    def country_population(self):
        countries_population = 0
        for i in countries
            countries_population=countries_population+ country_population(i)
        return countries_population

    def serialize(self):
        for i in countries
            i.serialize()




# pylint: disable=redefined-builtin,invalid-name
class Country(Location):  # pylint: disable=too-many-instance-attributes
    """
    A location in the world affected by the coronavirus.
    """

    def __init__(
        self, id, country, province, coordinates, last_updated, confirmed, deaths, recovered,
    ):  # pylint: disable=too-many-arguments
        # General info.
        self.id = id
        self.country = country.strip()
        self.province = province.strip()
        self.coordinates = coordinates

        # Last update.
        self.last_updated = last_updated

        # Statistics.
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered

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
                "confirmed": self.confirmed,
                "deaths": self.deaths,
                "recovered": self.recovered,
            },
        }


class TimelinedLocation(Location):
    """
    A location with timelines.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, id, country, province, coordinates, last_updated, timelines):
        super().__init__(
            # General info.
            id,
            country,
            province,
            coordinates,
            last_updated,
            # Statistics (retrieve latest from timelines).
            confirmed=timelines.get("confirmed").latest or 0,
            deaths=timelines.get("deaths").latest or 0,
            recovered=timelines.get("recovered").latest or 0,
        )

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
