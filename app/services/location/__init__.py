"""app.services.location"""
from abc import ABC, abstractmethod


class LocationServiceAdaptor:
    """
    Service for retrieving locations.
    """
    def __init__(self, source):
        self.source = source

    @abstractmethod
    async def get_all(self):
        """
        Gets and returns all of the locations.

        :returns: The locations.
        :rtype: List[Location]
        """
        return await self.source.get_locations()
        raise NotImplementedError

    @abstractmethod
    async def get(self, id):  # pylint: disable=redefined-builtin,invalid-name
        """
        Gets and returns location with the provided id.

        :returns: The location.
        :rtype: Location
        """
        locations = await self.source()
        return locations[id]
