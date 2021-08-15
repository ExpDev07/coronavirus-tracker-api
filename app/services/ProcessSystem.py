from location.csbs import CSBSLocationService
from location.jhu import JhuLocationService
from location.nyt import NYTLocationService

from aiohttp import ClientSession

class ProcessSystem():
    """
    provide all the functionalities related to the system

    use singleton and facade pattern

    """
    __instance = None

    @staticmethod
    def get_instance():

        if ProcessSystem.__instance is None:
            ProcessSystem.__instance = ProcessSystem()

        return ProcessSystem.__instance


    def __init__(self):

        if ProcessSystem.__instance is not None:
            raise Exception("Process system only has one instance")

        self.data_sources = {
            "jhu": JhuLocationService(),
            "csbs": CSBSLocationService(),
            "nyt": NYTLocationService()
        }

        self.CLIENT_SESSION = None

    async def get_all_locations(self, source: str):
        """
        Extract all the locations in one source
        """

        if source not in self.data_sources:
            return None
        return await self.data_sources[source].get_all()

    async def get_specify_location(self, source: str, id):
        """
        Extract one specific location based on the id
        """

        if source not in self.data_sources:
            return None
        return await self.data_sources[source].get(id)


    def get_all_sources(self):
        """
        return the current sources of the system
        """
        return list(self.data_sources.keys())

    """
    http util related functions
    """

    async def setup_client_session(self):
        self.CLIENT_SESSION = ClientSession()

    async def teardown_client_session(self):
        await self.CLIENT_SESSION.close()

    def get_client_session(self):
        return self.CLIENT_SESSION






