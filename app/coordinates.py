"""app.coordinates.py"""


class Coordinates:
    """
    A position on earth using decimal coordinates (latitude and longitude).
    """

    def __init__(self, latitude, longitude):
        self._latitude = latitude
        self._longitude = longitude

    def serialize(self):
        """
        Serializes the coordinates into a dict.

        :returns: The serialized coordinates.
        :rtype: dict
        """
        return {"latitude": self._latitude, "longitude": self._longitude}

    def __str__(self):
        return "lat: %s, long: %s" % (self._latitude, self._longitude)
