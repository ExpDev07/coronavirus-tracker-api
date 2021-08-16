"""app.services.location"""
from abc import ABC, abstractmethod


class LocationService(ABC):
    """
    Service for retrieving locations.
    """
    async def get_all(self):
        # Get the locations.
        locations = await get_locations()
        return locations

    async def get(self, loc_id):  # pylint: disable=arguments-differ
        # Get location at the index equal to provided id.
        locations = await self.get_all()
        return locations[loc_id]



