"""app.locations.csbs.py"""
from . import Director, LocationBuilder, BaseInfo, GeoInfo, Statistic


class CSBSLocation:
    """
    A CSBS (county) location.
    """
    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, state, county, coordinates, last_updated, confirmed, deaths):
        director = Director()
        baseinfo = BaseInfo(id=id,last_updated=last_updated)
        geoinfo = GeoInfo(county="US", province=state, coordinates=coordinates)
        statistic = Statistic(confirmed=confirmed, deaths=deaths, recovered=0)
        locationBuilder = LocationBuilder(baseinfo=baseinfo, statistic=statistic, geoinfo=geoinfo)
        director.set_builder(LocationBuilder)
        csbs = director.build_location()

    def serialize(self, timelines=False):  # pylint: disable=arguments-differ,unused-argument
        """
        Serializes the location into a dict.

        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize()

        # Update with new fields.
        serialized.update(
            {"state": self.state, "county": self.county,}
        )

        # Return the serialized location.
        return serialized
