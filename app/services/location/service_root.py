from jhu import JHULocationService
from nyt import NYTLocationService
from csbs import CSBSLocationService

class ServiceRoot:

    def __init__(self, source, service):
        if source == '' or source == None or source == 'jhu':
            self.source = 'jhu'
            self.service = JHULocationService()
        elif source == 'nyt':
            self.source = source
            self.service = NYTLocationService()
        elif source == 'csbs':
            self.source = source
            self.service = CSBSLocationService()
        else
            self.source = None

        async def get_all(self):
            locations = await self.service.get_all()
            return locations

        async def get(self, id):
            location = await self.service.get(id)
            return location
