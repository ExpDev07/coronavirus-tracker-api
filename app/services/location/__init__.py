"""app.services.location"""


class LocationService:

    def __init__(self, resource):
        self.resource = resource

    async def get_all(self):
        return await self.resource.get_locations()

    async def get(self, id):
        locations = await self.get_all()
        return locations[id]
