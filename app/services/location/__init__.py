from abc import ABC, abstractmethod

class LocationService(ABC):
    """
    Service for retrieving locations.
    """

    @abstractmethod
    def get_all(self):
        """
        Gets and returns all of the locations.

        :returns: The locations.
        :rtype: List[Location]
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, id):
        """
        Gets and returns location with the provided id.

        :returns: The location.
        :rtype: Location
        """
        raise NotImplementedError