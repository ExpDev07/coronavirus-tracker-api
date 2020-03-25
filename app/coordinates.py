class Coordinates:
    """
    A position on earth using decimal coordinates (latitude and longitude).
    """

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def serialize(self):
        """
        Serializes the coordinates into a dict.

        :returns: The serialized coordinates.
        :rtype: dict
        """
        return {"latitude": self.latitude, "longitude": self.longitude}

    def __str__(self):
        return "lat: %s, long: %s" % (self.latitude, self.longitude)
