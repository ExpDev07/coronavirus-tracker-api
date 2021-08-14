from ..coordinates import Coordinates
from ..utils import countries
from ..utils.populations import country_population
from ..__init__.py import country_code, country_population 

class DataLocation: 

	def __init__ (self, id, country, province, coordinates, last_updated, confirmed, deaths, recovered,
    ):

	self.id = id
        self.country = country.strip()
        self.province = province.strip()
        self.coordinates = coordinates

       
        self.last_updated = last_updated

      
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered

def serialize(self):
        """
        Serializes the location into a dict.
        :returns: The serialized location.
        :rtype: dict
        """
        return {
            
            "id": self.id,
            "country": self.country,
            "country_code": self.country_code,
            "country_population": self.country_population,
            "province": self.province,
          
            "coordinates": self.coordinates.serialize(),
            
            "last_updated": self.last_updated,
            "latest": {
                "confirmed": self.confirmed,
                "deaths": self.deaths,
                "recovered": self.recovered,
            },
        }
}
