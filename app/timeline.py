from datetime import datetime
from collections import OrderedDict

class Timeline:
    """
    Timeline with history of data.
    """

    def __init__(self, history = {}):
        self.__timeline = history

    @property
    def timeline(self):
        """
        Gets the history sorted by date (key).
        """
        return OrderedDict(sorted(self.__timeline.items()))

    @property
    def latest(self):
        """
        Gets the latest available history value.
        """
        return list(self.timeline.values())[-1] or 0

    def serialize(self):
        """
        Serializes the data into a dict.
        """
        return {
            'latest'  : self.latest,
            'timeline': self.timeline
        }