"""app.coordinates.py"""
from abc import ABCMeta, abstractmethod


class Location(metaclass=ABCMeta):

    def __init__(self, latitude, longitude):
            """implement"""

    def serialize(self):
        """implement"""

    def __str__(self):
        """implement"""

class Coordinates(Location):
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


class history(Location):
      def __init__(self, latitude, longitude):
          self.latitude = latitude
          self.longitude = longitude
          self.hisLocations = []

      def add(self, hisLocation):
          self.hisLocations.append(hisLocation)
          self.latitude += hisLocation.latitude
          self.longitude += hisLocation.longitude


      def serialize(self):
          for hisLocation in self.hisLocations:
               hisLocation.serialize
          return {"Total longitude": self.longitude, "Total latitude": self.latitude}

      def __str__(self):
          return "lat: %s, long: %s" % (self.latitude, self.longitude)