"""app.locations.nyt.py"""
from . import Director, TimelinedLocationBuilder, BaseInfo, GeoInfo, Statistic


class NYTLocation(TimelinedLocation):
    """
    A NYT (county) Timelinedlocation.
    """

    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, state, county, coordinates, last_updated, timelines):

        director = Director()
        baseinfo = BaseInfo(id=id,last_updated=last_updated)
        geoinfo = GeoInfo(county="US", province=state, coordinates=coordinates)
        locationBuilder = TimelinedLocationBuilder(baseinfo=baseinfo, geoinfo=geoinfo, timelines=timelines)
        director.set_builder(TimelinedLocationBuilder)
        nyt = director.build_location()

    def serialize(self, timelines=False):  # pylint: disable=arguments-differ,unused-argument
        """
        Serializes the location into a dict.

        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize(timelines)

        # Update with new fields.
        serialized.update(
            {"state": self.state, "county": self.county,}
        )

        # Return the serialized location.
        return serialized
