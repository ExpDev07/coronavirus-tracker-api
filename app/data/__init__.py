"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService

# Singleton Class


class DataSource:

    __instance = None

    __DATA_SOURCES = {
        "jhu": JhuLocationService(),
        "csbs": CSBSLocationService(),
        "nyt": NYTLocationService(),
    }

    @staticmethod
    def getInstance():
        if DataSource.__instance == None:
            DataSource()
        return DataSource.__instance

    def __init__(self):
        if DataSource.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DataSource.__instance = self

    def setSource(self, source):
        self.dataSource = self.__DATA_SOURCES.get(source.lower())

    def getSource(self):
        return self.dataSource
