"""app.location"""
from ..coordinates import Coordinates
from ..utils import countries
from ..utils.populations import country_population
from abc import abstractmethod
class Builder:
    def build_base(self) -> None:
        pass
    def build_stat(self) -> None:
        pass
    def build_geo(self) -> None:
        pass
    def build_timelines(self) -> None:
        pass

class Location_Builder(Builder):
    def __init__(self, basinfo, statistic, geoinfo) -> None:
        self.reset()
    
    def reset(self) -> None:
        self._location = Location()
    
    def locate(self) -> Location:
        location = self._location
        self.reset()
        return location
    
    def build_base(self, baseinfo) -> None:
        self.baseinfo = baseinfo
    def build_stat(self, statistic) -> None:
        self.statistic = statistic
    def build_geo(self, geoinfo) -> None:
        self.geoinfo = geoinfo
        
class TimelinedLocation_Builder(Builder):
    def __init__(self, baseinfo, statistic, geoinfo, timelines) -> None:
        self.reset()
    
    def reset(self) -> None:
        self._location = TimelinedLocation()
    
    def locate(self) -> TimelinedLocation:
        timelined_location = self._timelined_location
        self.reset()
        return timelined_location

    def build_base(self, baseinfo) -> None:
        self.baseinfo = baseinfo
    def build_stat(self, statistic) -> None:
        self.statistic = statistic
    def build_geo(self, geoinfo) -> None:
        self.geoinfo = geoinfo
    def build_timelines(self, timelines) -> None:
        self.timelines = timelines
        
class Location:

    def __init__(self):
        self.id = None
        self.last_updated = None
        self.country_code = None
        self.country_population = None
        self.serialize = None
        self.geoinfo = None
        self.last_updated = None
        self.statistic = None

    def set_base(self, id, last_updated, serialize) -> None:
        self.id = id
        self.last_updated = last_updated
        self.serialize = serialize
    def set_geoinfo(self, geoinfo):
        self._geoinfo = geoinfo
    def set_statistic(self, statistic):
        self._statistic = statistic

class TimelinedLocation:

    def set_base(self, id, last_updated, serialize) -> None:
        self.id = id
        self.last_updated = last_updated
        self.serialize = serialize
    def set_geoinfo(self, geoinfo):
        self._geoinfo = geoinfo
    def set_timelines(self, timelines):
        self._timelines = timelines

class Director:
    def __init__(self) -> None:
        self._builder = None
    
    def set_builder(self, builder: Builder) -> None:
        self._builder = builder
    
    def build_location(self) -> None:
        location = Location()
        self.builder.build_location()
        self.builder.build_base()
        self.builder.build_stat()
        self.builder.build_geo()

    def build_timelinedlocation(self) -> None:
        self.builder.build_location()
        self.builder.build_base()
        self.builder.build_stat()
        self.builder.build_geo()
        self.builder.build_timelines()

class Stastistic:
    def __init__(self, confirmed, deaths, recovered):
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered

class GeoInfo:
    def __init__(self, country, province, coorinates):
        self.country = country
        self.province = province
        self.coordinates = coorinates
        self.country_code = (countries.country_code(self.geoinfo.country) or countries.DEFAULT_COUNTRY_CODE).upper()
        self.country_population = country_population(self.country_code)

class BaseInfo:
    def __init__(self, id, last_updated, serialize):
        self.id = id
        self.last_updated = last_updated
        self.serialize = {
            # General info.
            "id": self.id,
            "country": self.geoinfo.country,
            "country_code": self.country_code,
            "country_population": self.country_population,
            "province": self.geoinfo.province,
            # Coordinates.
            "coordinates": self.geoinfo.coordinates.serialize(),
            # Last updated.
            "last_updated": self.last_updated,
            # Latest data (statistics).
            "latest": {
                "confirmed": self.statistic.confirmed,
                "deaths": self.statistic.deaths,
                "recovered": self.statistic.recovered,
            },
        }
# pylint: disable=redefined-builtin,invalid-name
'''class Location:  # pylint: disable=too-many-instance-attributes
    """
    A location in the world affected by the coronavirus.
    """

    def __init__(
        self, id, geoinfo, last_updated, statistic
    ):  # pylint: disable=too-many-arguments
        # General info.
        self.id = id
        self.geoinfo = geoinfo
        # Last update.
        self.last_updated = last_updated

        # Statistics.
        self.statistic = statistic

    @property
    def country_code(self):
        """
        Gets the alpha-2 code represention of the country. Returns 'XX' if none is found.

        :returns: The country code.
        :rtype: str
        """
        return (countries.country_code(self.geoinfo.country) or countries.DEFAULT_COUNTRY_CODE).upper()

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
            "country": self.geoinfo.country,
            "country_code": self.country_code,
            "country_population": self.country_population,
            "province": self.geoinfo.province,
            # Coordinates.
            "coordinates": self.geoinfo.coordinates.serialize(),
            # Last updated.
            "last_updated": self.last_updated,
            # Latest data (statistics).
            "latest": {
                "confirmed": self.statistic.confirmed,
                "deaths": self.statistic.deaths,
                "recovered": self.statistic.recovered,
            },
        }


class TimelinedLocation(Location):
    """
    A location with timelines.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, id, geoinfo, last_updated, timelines):
        super().__init__(
            # General info.
            id,
            geoinfo,
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
'''