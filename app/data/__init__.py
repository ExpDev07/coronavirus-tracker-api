"""app.data"""
from abc import ABC, abstractmethod
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService

class DataSourceFactory(ABC):
    def __init__(self):
        pass
   
    @abstractmethod 
    def getInstance():
        pass

    @abstractmethod
    def getService():
        pass

class JhuFactory(DataSourceFactory):
    __instance = None
    __service = None

    def __init__(self):
        if JhuFactory.__instance != None:
            raise Exception("Factory is singleton!")
        elif JhuFactory.__service != None:
            raise Exception("Service is singleton!")
        else:
            JhuFactory.__instance = self
            JhuFactory.__service = JhuLocationService()
        
    @staticmethod 
    def getInstance():
      if JhuFactory.__instance == None:
         JhuFactory()
      return JhuFactory.__instance
        
    @staticmethod 
    def getService():
      if JhuFactory.__service == None:
         JhuFactory()
      return JhuFactory.__service

class CSBSFactory(DataSourceFactory):
    __instance = None
    __service = None

    def __init__(self):
        if CSBSFactory.__instance != None:
            raise Exception("Factory is singleton!")
        elif CSBSFactory.__service != None:
            raise Exception("Service is singleton!")
        else:
            CSBSFactory.__instance = self
            CSBSFactory.__service = CSBSLocationService()
   
    @staticmethod 
    def getInstance():
      if CSBSFactory.__instance == None:
         CSBSFactory()
      return CSBSFactory.__instance

    @staticmethod 
    def getService():
      if CSBSFactory.__service == None:
         CSBSFactory()
      return CSBSFactory.__service

class NYTFactory(DataSourceFactory):
    __instance = None
    __service = None

    def __init__(self):
        if NYTFactory.__instance != None:
            raise Exception("Factory is singleton!")
        elif NYTFactory.__service != None:
            raise Exception("Service is singleton!")
        else:
            NYTFactory.__instance = self
            NYTFactory.__service = NYTLocationService()
   
    @staticmethod 
    def getInstance():
      if NYTFactory.__instance == None:
         NYTFactory()
      return NYTFactory.__instance

    @staticmethod 
    def getService():
      if NYTFactory.__service == None:
         NYTFactory()
      return NYTFactory.__service


# Mapping of factories to data-sources.
DATA_SOURCES = {
    "jhu": JhuFactory.getInstance(),
    "csbs": CSBSFactory.getInstance(),
    "nyt": NYTFactory.getInstance(),
}

def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return DATA_SOURCES.get(source.lower()).getService()
