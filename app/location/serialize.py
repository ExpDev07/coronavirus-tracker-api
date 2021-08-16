
class serialize():
    def serialize(self, timelines=False):  # pylint: disable=arguments-differ,unused-argument
        """
        Serializes the location into a dict.

        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize(timelines)

        # Update with new fields.
        serialized.update(
            {"state": self.state, "county": self.county,}
        )

        # Return the serialized location.
        return serialized
    
