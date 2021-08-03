"""app.services.location"""
from abc import ABC, abstractmethod, abstractstaticmethod

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



'''
This is the interface for the client to interact with in order to handle the calls
'''
class LocationServiceAbstraction(ABC):
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


'''
This is the implementation that the client will interact with in order to execute the required locationservice implementation
'''
class LocationServiceAbstractionImpl(LocationServiceAbstraction):
    def __init__(self, implementation):
        self.__provider = implementation
    
    async def get_all(self):
        return await self.__provider.get_locations()
    
    async def get(self, id):
        return await self.__provider.get(id)


'''
interface for all location services to implement in order to satisfy consistency with each type of locationservice alongside the bridge pattern
'''
class ILocationService(ABC):
    @abstractmethod
    async def get_locations(self):
        return NotImplementedError

    @abstractmethod
    async def get(self, id):
        return NotImplementedError

