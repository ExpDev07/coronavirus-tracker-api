"""app.services.location"""
from abc import ABC, abstractmethod


class LocationServices:
    def __init__(self,location_services: list[LocationService]):
        self.location_services = location_services

    def add_service(self,location_service):
        self.location_services.append(location_service)

    def get_service(self):
        return location_services

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
