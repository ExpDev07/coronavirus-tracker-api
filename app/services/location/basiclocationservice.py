"""app.services.location.basiclocationservice.py"""

from . import LocationService

class BasicLocationService(LocationService):
    """
    Service for retrieving locations from csbs
    """
    async def get_all(self):
        # Get the locations.
        locations = await self.dataSource.get_locations()
        return locations

    async def get(self, loc_id):  # pylint: disable=arguments-differ
        # Get location at the index equal to the provided id.
        locations = await self.get_all()
        return locations[loc_id]


