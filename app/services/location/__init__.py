"""app.services.location"""
from abc import ABC, abstractmethod


class LocationService(ABC):
    """
    Service for retrieving locations.
    """

    @abstractmethod
    async def get_all(self):
        """
        Gets and returns all of the locations.

        :returns: The locations.
        :rtype: List[Location]
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, id):  # pylint: disable=redefined-builtin,invalid-name
        """
        Gets and returns location with the provided id.

        :returns: The location.
        :rtype: Location
        """
        raise NotImplementedError
