"""app.coordinates.py"""


class Coordinates:
    __instance = None
    """
    A position on earth using decimal coordinates (latitude and longitude).
    """

    def __init__(self, latitude, longitude):
        if Coordinates.__instance is not None:
            raise Exception("I have already got an latitude and longitude")
        else:
            self.latitude = latitude
            self.longitude = longitude

    @staticmethod
    def get_instance():
        if Coordinates.__instance is None:
            Coordinates(0, 0)
        return Coordinates.__instance



    def serialize(self):
        """
        Serializes the coordinates into a dict.

        :returns: The serialized coordinates.
        :rtype: dict
        """
        return {"latitude": self.latitude, "longitude": self.longitude}

    def __str__(self):
        return "lat: %s, long: %s" % (self.latitude, self.longitude)
