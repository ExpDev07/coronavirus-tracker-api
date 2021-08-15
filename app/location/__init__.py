"""app.location"""

import copy

from ..utils import countries
from ..utils.populations import country_population

from abc import ABCMeta, abstractmethod


class PrototypeLocations(metaclass=ABCMeta):
    def __init__(self, id, country, province, coordinates, last_updated, confirmed, deaths, recovered, timelines):
        self.id = None
        self.country = None
        self.province = None
        self.coordinates = None

        # Last update.
        self.last_updated = None

        # Statistics.
        self.confirmed = None
        self.deaths = None
        self.recovered = None

        # Set timelines.
        self.timelines = None

    def set_id(self, id):
        self.id = id

    def set_country(self, country):
        self.country = country.strip()

    def set_province(self, province):
        self.province = province.strip()

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def set_last_update(self, last_updated):
        self.last_updated = last_updated

    def set_confirmed(self, confirmed):
        self.confirmed = confirmed

    def set_deaths(self, deaths):
        self.deaths = deaths

    def set_recovered(self, recovered):
        self.recovered = recovered

    def set_timelines(self, timelines):
        self.timelines = timelines

    def get_id(self):
        return self.id

    def get_country(self):
        return self.country.strip()

    def get_province(self):
        return self.province.strip()

    def get_coordinates(self):
        return self.coordinates

    def get_last_update(self):
        return self.last_updated

    def get_confirmed(self):
        return self.confirmed

    def get_deaths(self):
        return self.deaths

    def get_recovered(self):
        return self.recovered

    def get_timelines(self):
        return self.timelines

    def clone(self):
        return copy.copy(self)

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

    def __copy__(self):
        """
        Create a shallow copy. This method will be called whenever someone calls
        `copy.copy` with this object and the returned value is returned as the
        new shallow copy.
        """

        # First, let's create copies of the nested objects.
        id = copy.deepcopy(self.id)
        country = copy.copy(self.country)
        province = copy.copy(self.province)
        coordinates = copy.copy(self.coordinates)
        last_updated = copy.copy(self.last_updated)
        confirmed = copy.copy(self.confirmed)
        deaths = copy.copy(self.deaths)
        recovered = copy.copy(self.recovered)
        timelines = copy.copy(self.timelines)

        # Then, let's clone the object itself, using the prepared clones of the
        # nested objects.
        new = self.__class__(
            id, country, province, coordinates, last_updated, confirmed, deaths, recovered, timelines
        )
        new.__dict__.update(self.__dict__)

        return new

    def __deepcopy__(self, memo=None):
        """
        Create a deep copy. This method will be called whenever someone calls
        `copy.deepcopy` with this object and the returned value is returned as
        the new deep copy.

        What is the use of the argument `memo`? Memo is the dictionary that is
        used by the `deepcopy` library to prevent infinite recursive copies in
        instances of circular references. Pass it to all the `deepcopy` calls
        you make in the `__deepcopy__` implementation to prevent infinite
        recursions.
        """

        # First, let's create copies of the nested objects.
        if memo is None:
            memo = {}
        id = copy.deepcopy(self.id, memo)
        country = copy.deepcopy(self.country, memo)
        province = copy.deepcopy(self.province, memo)
        coordinates = copy.deepcopy(self.coordinates, memo)
        last_updated = copy.deepcopy(self.last_updated, memo)
        confirmed = copy.deepcopy(self.confirmed, memo)
        deaths = copy.deepcopy(self.deaths, memo)
        recovered = copy.deepcopy(self.recovered, memo)
        timelines = copy.deepcopy(self.timelines, memo)

        # Then, let's clone the object itself, using the prepared clones of the
        # nested objects.
        new = self.__class__(
            id, country, province, coordinates, last_updated, confirmed, deaths, recovered, timelines
        )
        new.__dict__ = copy.deepcopy(self.__dict__, memo)

        return new


class Location:  # pylint: disable=too-many-instance-attributes
    """
    A location in the world affected by the coronavirus.
    """

    def __init__(self):
        super().__init__()

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
    def __init__(self, timelines):
        super().__init__(
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
