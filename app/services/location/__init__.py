"""app.services.location"""

class LocationService:
    """
    Service for retrieving locations.
    """

    async def get_all(self):
        # Get the locations.
        locations = await get_locations()
        return locations

    async def get(self, loc_id):  # pylint: disable=arguments-differ
        # Get location at the index equal to the provided id.
        locations = await self.get_all()
        return locations[loc_id]

    @abstractmethod
    async def get_locations():
        raise NotImplementedError