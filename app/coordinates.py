"""app.coordinates.py"""


class Coordinates:
    """
    A position on earth using decimal coordinates (latitude and longitude).
    """

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Serialize:
    def serialize(self,latitude,longitude):
        """
        Serializes the coordinates into a dict.

        :returns: The serialized coordinates.
        :rtype: dict
        """
        self.latitude=latitude
        self.longitude=longitude

        return {self.latitude,self.longitude}

    def __str__(self):
        return "lat: %s, long: %s" % (self.latitude, self.longitude)

latitude = Coordinates("latitude")
longitude= Coordinates("longitude")
