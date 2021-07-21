"""app.location"""
from ..coordinates import Coordinates
from ..utils import countries
from ..utils.populations import country_population


# pylint: disable=redefined-builtin,invalid-name
class Location:  # pylint: disable=too-many-instance-attributes
    """
    A location in the world affected by the coronavirus.
    """

    def __init__(
        self, id, country, province, coordinates, last_updated, confirmed, deaths, recovered,
    ):  # pylint: disable=too-many-arguments
        # General info.
        self._id = id
        self._country = country.strip()
        self._province = province.strip()
        self._coordinates = coordinates

        # Last update.
        self._last_updated = last_updated

        # Statistics.
        self._confirmed = confirmed
        self._deaths = deaths
        self._recovered = recovered

    @property
    def confirmed(self):
        """
        Gets the latest amount of total confirmed cases of this location.

        :returns: The latest amount of total confirmed cases.
        :rtype: int
        """
        return self._confirmed

    @property
    def deaths(self):
        """
        Gets the latest amount of total death cases of this location.

        :returns: The latest amount of total death cases.
        :rtype: int
        """
        return self._deaths

    @property
    def recovered(self):
        """
        Gets the latest amount of total recovered cases of this location.

        :returns: The latest amount of total recovered cases.
        :rtype: int
        """
        return self._recovered

    @property
    def country_code(self):
        """
        Gets the alpha-2 code represention of the country. Returns 'XX' if none is found.

        :returns: The country code.
        :rtype: str
        """
        return (countries.country_code(self._country) or countries.DEFAULT_COUNTRY_CODE).upper()

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
            "id": self._id,
            "country": self._country,
            "country_code": self.country_code,
            "country_population": self.country_population,
            "province": self._province,
            # Coordinates.
            "coordinates": self._coordinates.serialize(),
            # Last updated.
            "last_updated": self._last_updated,
            # Latest data (statistics).
            "latest": {
                "confirmed": self._confirmed,
                "deaths": self._deaths,
                "recovered": self._recovered,
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
        self._timelines = timelines

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
                        for (key, value) in self._timelines.items()
                    }
                }
            )

        # Return the serialized location.
        return serialized
