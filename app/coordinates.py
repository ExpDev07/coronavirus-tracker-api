"""app.coordinates.py"""

class Position(object):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Coordinates(Position):
    """
    A position on earth using decimal coordinates (latitude and longitude).
    """
    def serialize(self, position):
        self.position = {"latitude": self.latitude, "longitude": self.longitude}
        """
        Serializes the coordinates into a dict.

        :returns: The serialized coordinates.
        :rtype: dict
        """
        return self.postion

    def __str__(self):
        return "lat: %s, long: %s" % (self.latitude, self.longitude)
