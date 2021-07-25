"""app.services.location"""
from abc import ABC, abstractmethod


class LocationService:
    """
    Service for retrieving locations.
    """
    """
        Service for retrieving locations from csbs
        """

    def __init__(self, gateway: "LocationGateway"):
        self.gateway = gateway

    async def get_all(self):
        # Get the locations.
        locations = await self.gateway.get_locations()
        return locations

    async def get(self, loc_id):  # pylint: disable=arguments-differ
        # Get location at the index equal to the provided id.
        locations = await self.get_all()
        return locations[loc_id]

    def set_gateway(self, gateway: "LocationGateway"):
        self.gateway = gateway


class LocationGateway(ABC):
    """
    real processing for all kinds of locations
    """

    @abstractmethod
    async def get_locations(self):
        """
        parse all locations from the datasource
        """
        raise NotImplementedError
