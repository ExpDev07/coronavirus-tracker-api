"""app.data"""
from ..services.location.csbs import CSBSLocationServicee
from ..services.location.jhu import JhuLocationServicee
from ..services.location.nyt import NYTLocationServicee
from app.services.location.__init__ import LocationServicer

class DataSourceSingletonMeta(type):
    """
    access point to the DataSource 
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DataSourceSingleton(metaclass=DataSourceSingletonMeta):
        DATA_SOURCES = {
            "jhu": LocationServicer(JhuLocationServicee()),
            "csbs": LocationServicer(CSBSLocationServicee()),
            "nyt": LocationServicer(NYTLocationServicee()),
        }
        def get_data_source(self, dataSource):
            return self.DATA_SOURCES.get(dataSource.lower())
        ...

        def get_data_source_list(self): 
            return self.DATA_SOURCES

        
