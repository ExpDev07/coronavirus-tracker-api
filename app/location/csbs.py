from . import Location

class CSBSLocation(Location):
    """
    A CSBS (county) location.
    """
    def __init__(self, id, state, county, coordinates, last_updated, confirmed, deaths):
        super().__init__(
            # General info.
            id, 'US', state, coordinates, last_updated, 
            
            # Statistics.
            confirmed=confirmed,
            deaths=deaths, 
            recovered=0
        )

        self.state = state
        self.county = county
    
    def serialize(self, timelines=False):
        """
        Serializes the location into a dict.

        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize()

        # Update with new fields.
        serialized.update({
            'state': self.state,
            'county': self.county,
        })

        # Return the serialized location.
        return serialized