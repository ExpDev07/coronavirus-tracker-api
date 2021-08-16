"""app.location"""
from ..coordinates import Coordinates
from ..utils import countries
from ..utils.populations import country_population


# pylint: disable=redefined-builtin,invalid-name
class BuilderLocation:  # pylint: disable=too-many-instance-attributes
    """
    A location in the world affected by the coronavirus.
    """

    def __init__(self):  
        self.id = 0
        self.country = ""
        self.province = ""
        self.coordinates = 0.0
        self.last_updated = ""
        self.confirmed = 0
        self.deaths = 0
        self.recovered = 0
        
    @staticmethod
    def item():
        return BuilderLocation()
        
    @property
    def withCountry_code(self):
        """
        Gets the alpha-2 code represention of the country. Returns 'XX' if none is found.
        :returns: The country code.
        :rtype: str
        """
        return (countries.withCountry_code(self.country) or countries.DEFAULT_COUNTRY_CODE).upper()

    @property
    def withCountry_population(self):
        """
        Gets the population of this location.
        :returns: The population.
        :rtype: int
        """
        return withCountry_population(self.withCountry_code)
        
    def withProvince(self,province):
        self.province = province
        return self
        
    def withCoordinates(self,coordinates):
        self.coordinates = coordinates
        return self
        
    def withlast_updated(self,last_updated):
        self.last_updated = last_updated
        return self
    
     def withConfirmed(self,confirmed):
        self.confirmed = confirmed
        return self
    
     def withDeaths(self,deaths):
        self.deaths = deaths
        return self
    
     def withRecovered(self,recovered):
        self.recovered = recovered
        return self

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
