"""app.location"""
from ..coordinates import Coordinates
from ..utils.countries import CountryCodeUtil
from ..utils.populations import country_population
from abc import ABC, abstractmethod

class LocationBuilder(ABC):
    """
        An Abstract class to inherit to build coordinates of a location. 
    """
    @abstractmethod
    def country_code(self):
        pass
    
    @abstractmethod
    def country_population(self):
        pass
    
    @abstractmethod
    def serialize(self):
        pass

# pylint: disable=redefined-builtin,invalid-name
class Location(LocationBuilder):  # pylint: disable=too-many-instance-attributes
    """
    A location in the world affected by the coronavirus.
    """
    def __init__(
        self, locationDict
    ):  # pylint: disable=too-many-arguments
        # General info.
        #if all True, then location would be constructed of all the params passed.
        pass

    def build_location_dict(self,locationDict):
        self.country_code_util = CountryCodeUtil()

        self.location_dict = locationDict.fromkeys([list(locationDict.keys())])
        for key, value in locationDict.items():
            if value:
                if key == "country":
                    self.location_dict[key] = self.format_country(value)
                elif key == "province":
                    self.location_dict[key] = self.format_province(value)
                elif key == "coordinates":
                    self.location_dict[key] = self.format_coordinates(value)
                else:
                    self.location_dict[key] = value

        self.location_dict["country_population"] = self.country_population
            
    @property
    def country_code(self):
        """
        Gets the alpha-2 code represention of the country. Returns 'XX' if none is found.
        :returns: The country code.
        :rtype: str
        """
        return (self.country_code_util.get_country_code(self.location_dict["country"]) or self.country_code_util.DEFAULT_COUNTRY_CODE).upper()

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
            "id": self.location_dict["id"],
            "country": self.location_dict["country"],
            "country_code": self.location_dict["country_code"],
            "country_population":  self.location_dict["country_population"],
            "province": self.location_dict["province"],
            # Coordinates.
            "coordinates": self.location_dict["coordinates"],
            # Last updated.
            "last_updated":  self.location_dict["last_updated"],
            # Latest data (statistics).
            "latest": {
                "confirmed": self.location_dict["confirmed"],
                "deaths": self.location_dict["deaths"],
                "recovered": self.location_dict["recovered"],
            },
        }
    

    def format_country(self,country):
        return country.strip()

    def format_province(self,province):
        return province.strip()

    def format_coordinates(self, coordinates):
        return coordinates.serialize()
