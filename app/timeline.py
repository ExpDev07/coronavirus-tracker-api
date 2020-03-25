from datetime import datetime
from collections import OrderedDict


class Timeline:
    """
    Timeline with history of data.
    """

    def __init__(self, history={}):
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
        # Get values in a list.
        values = list(self.timeline.values())

        # Last item is the latest.
        if len(values):
            return values[-1] or 0

        # Fallback value of 0.
        return 0

    def serialize(self):
        """
        Serializes the timeline into a dict.

        :returns: The serialized timeline.
        :rtype: dict
        """
        return {"latest": self.latest, "timeline": self.timeline}
