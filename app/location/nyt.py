"""app.locations.nyt.py"""
from . import TimelinedLocation

class Serialize():  # pylint: disable=arguments-differ,unused-argument

    def super_serialized(self, timelines):
        serialized = super().serialize(timelines)
        return serialized

# Update with new fields.
    def serialized_update(self, serialized):
        serialized.update(
            {"state": self.state, "county": self.county,}
            )
        return serialized

# Return the serialized location.
    def get_serialized(self, serialized):
        return serialized


class Serialize_Builder:
    ser = Serialize()

    def Run_super_serialized(self):
        pass

    def Run_serialized_update(self, serialized):
        pass

    def Run_get_serialized(self, serialized):
        pass


class nyt_Serialize_Builder(Serialize_Builder):
    def __init__(self, timelines):
        self.name = "nyt_ser"
        self.nyt_ser = Serialize()
        self.timelines = timelines

    def Run_super_serialized(self):
        return self.nyt_ser.super_serialized(self.timelines)

    def Run_serialized_update(self, serialized):
        return self.nyt_ser.serialized_update(serialized)

    def Run_get_serialized(self, serialized):
        return self.nyt_ser.get_serialized()


class csbs_Serialize_Builder(Serialize_Builder):
        def __init__(self):
            self.name = "csbs_ser"
            self.csbs_ser = Serialize()

        def Run_super_serialized(self):
            return self.csbs_ser.super_serialized()

        def Run_serialized_update(self, serialized):
            return self.csbs_ser.serialized_update(serialized)

        def Run_get_serialized(self, serialized):
            return self.csbs_ser.get_serialized()

class Director:
    def __init__(self, bld):
        self.builder = bld

    def build_product(self):

        if self.builder.name == "nyt_ser":
            serialized = self.builder.Run_super_serialized()
            update_serialized = self.builder.Run_serialized_update(serialized)
            self.builder.Run_get_serialized(update_serialized)
'''
        if self.builder.name == "csbs_ser":
            self.builder.Run_super_serialized()
            self.builder.Run_serialized_update()
            self.builder.Run_get_serialized()
'''


class NYTLocation(TimelinedLocation):
    """
    A NYT (county) Timelinedlocation.
    """

    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, state, county, coordinates, last_updated, timelines):
        super().__init__(id, "US", state, coordinates, last_updated, timelines)

        self.state = state
        self.county = county

    def serialize(self, timelines=False):  # pylint: disable=arguments-differ,unused-argument
        bld = nyt_Serialize_Builder(timelines)
        director = Director(bld)
        return director.build_product()







'''

--------------------------

class NYTLocation(TimelinedLocation):
    """
    A NYT (county) Timelinedlocation.
    """

    # pylint: disable=too-many-arguments,redefined-builtin
    def __init__(self, id, state, county, coordinates, last_updated, timelines):
        super().__init__(id, "US", state, coordinates, last_updated, timelines)

        self.state = state
        self.county = county

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
'''