"""app.services.location"""
from abc import ABC, abstractmethod


class LocationServicer: # The 'Remote' of the Pattern
    """
    Abstraction class handling the 'Front End' portion of the project
    """
    @abstractmethod
    def __init__(self, implementation):
        self.implementation = implementation
    
    @abstractmethod
    def all_locations(self):
        return self.implementation.get_all()
    
    @abstractmethod
    def locations(self):
        return self.implementation.get()

class LocationServicee: # The 'Device' with the implmentation
    """
    Implementation Interface
    """

    def get_all(self):
        # No implementation - interface method
        pass

    def get(self):
        # No implementation - interface method
        pass



