"""app.coordinates.py"""
from pydantic import BaseModel


class Coordinates(BaseModel):
    """
    A position on earth using decimal coordinates (latitude and longitude).
    """

    latitude: float = None
    longitude: float = None

    def __str__(self):
        return "lat: %s, long: %s" % (self.latitude, self.longitude)
