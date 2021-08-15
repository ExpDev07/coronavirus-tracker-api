from abc import *

class DataSourcesInterface(ABC):
    @abstractmethod
    async def get_locations(self):
        pass

  