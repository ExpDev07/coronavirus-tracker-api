"""app.location"""
from ..coordinates import Coordinates
from ..utils import countries
from ..utils.populations import country_population
from creationalBP import DataLocation


# pylint: disable=redefined-builtin,invalid-name
class Location(creationalBP):  # pylint: disable=too-many-instance-attributes
    """
    A location in the world affected by the coronavirus.
    """

    @property
    def country_code(DataLocation):
        """
        Gets the alpha-2 code represention of the country. Returns 'XX' if none is found.

        :returns: The country code.
        :rtype: str
        """
        return (countries.country_code(super().__init__.country) or countries.DEFAULT_COUNTRY_CODE).upper()

    @property
    def country_population(DataLocation):
        """
        Gets the population of this location.

        :returns: The population.
        :rtype: int
        """
        return country_population(super().__init__.country_code)

class TimelinedLocation(DataLocation):
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
