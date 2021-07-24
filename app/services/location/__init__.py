"""app.services.location"""
from abc import ABC, abstractmethod


class LocationService(ABC):
    """
    Service for retrieving locations.
    """

    async def get_all(self):
        # Get the locations.
        locations = await self.get_locations()
        return locations

    async def get(self, loc_id):  # pylint: disable=arguments-differ
        # Get location at the index equal to the provided id.
        locations = await self.get_all()
        return locations[loc_id]    

    @abstractmethod
    async def get_locations(self):
        raise NotImplementedError

def getDataSources():
    from .csbs import CSBSLocationService
    from .jhu import JhuLocationService
    from .nyt import NYTLocationService
    return {"jhu": JhuLocationService(), "csbs": CSBSLocationService(), "nyt": NYTLocationService()}