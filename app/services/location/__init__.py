"""app.services.location"""
from abc import ABC, abstractmethod


class LocationService(ABC):
    """
    Service for retrieving locations.
    """

    # this class variable will store the singleton instance for 
    # the LocationService instance from the child class
    __instance__ = None

    @abstractmethod
    async def get_all(self):
        """
        Gets and returns all of the locations.

        :returns: The locations.
        :rtype: List[Location]
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, id):  # pylint: disable=redefined-builtin,invalid-name
        """
        Gets and returns location with the provided id.

        :returns: The location.
        :rtype: Location
        """
        raise NotImplementedError
    
    @classmethod
    def getInstance(cls):
        # singleton pattern
        if cls.__instance__ is None:
            # instantiate new object from the class (note that we are 
            # expecting 0 parameters for the constructor. if parameters 
            # needed this method should be overridden by the subclass)
            cls.__instance__ = cls()
        return cls.__instance__
