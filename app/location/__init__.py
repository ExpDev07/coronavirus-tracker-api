"""app.location"""
from ..coordinates import Coordinates
from ..utils import countries
from ..utils.populations import country_population

# put confirmed cases, deaths cases, recovered cases into one class
# Inseated of using confirmed cases, deaths cases, recovered cases as attributes, we can use CaseNumbers class instance as attribute
class CaseNumbers:
    def __init__(self, id, confirmed = 0, deaths = 0, recovered = 0):
        self.id = id
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered


#put all location information into one class
#CaseNumbers, Locationinfo, coordinates and Location forms one aggregate
class Locationinfo:
    def __init__(self, id, country, province, coordinates):
        self.id = id
        self.country = country.strip()
        self.province = province.strip()
        self.coordinates = coordinates




# pylint: disable=redefined-builtin,invalid-name
class Location:  # pylint: disable=too-many-instance-attributes
    """
    A location in the world affected by the coronavirus.
    """

    # Use instance of class CaseNumbers as attribute
    def __init__(
        self, id, locationinfo, last_updated, casenumbers
    ):  # pylint: disable=too-many-arguments
        # General info.
        self.locationinfo = locationinfo

        # Last update.
        self.last_updated = last_updated

        # Statistics.
        self.casenumbers = casenumbers

    @property
    def country_code(self):
        """
        Gets the alpha-2 code represention of the country. Returns 'XX' if none is found.

        :returns: The country code.
        :rtype: str
        """
        return (countries.country_code(self.locationinfo.country) or countries.DEFAULT_COUNTRY_CODE).upper()

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
            "id": self.locationinfo.id,
            "country": self.locationinfo.country,
            "country_code": self.country_code,
            "country_population": self.country_population,
            "province": self.locationinfo.province,
            # Coordinates.
            "coordinates": self.locationinfo.coordinates.serialize(),
            # Last updated.
            "last_updated": self.last_updated,
            # Latest data (statistics).
            "latest": {
                "confirmed": self.casenumbers.confirmed,
                "deaths": self.casenumbers.deaths,
                "recovered": self.casenumbers.recovered,
            },
        }


class TimelinedLocation(Location):
    """
    A location with timelines.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, locationinfo, last_updated, timelines, casenumbers):
        super().__init__(
            # General info.
            locationinfo,
            last_updated,
            # Statistics (retrieve latest from timelines).
            casenumbers
            #confirmed=timelines.get("confirmed").latest or 0,
            #deaths=timelines.get("deaths").latest or 0,
            #recovered=timelines.get("recovered").latest or 0,
        )
        #set case numbers
        self.casenumbers.confirmed=timelines.get("confirmed").latest or 0
        self.casenumbers.deaths=timelines.get("deaths").latest or 0
        self.casenumbers.recovered=timelines.get("recovered").latest or 0
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
