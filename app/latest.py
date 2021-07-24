"""app.latest.py"""


class Latest:
    """
    A position on earth using decimal coordinates (latitude and longitude).
    """

    def __init__(self, confirmed, deaths, recovered):
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered

    def serialize(self):
        """
        Serializes the latest data into a dict.

        :returns: The serialized latest confirmed deaths and recovered cases
        :rtype: dict
        """
        return {"confirmed": self.confirmed, "deaths": self.deaths, "recovered": self.recovered}

    def __str__(self):
        return "confirmed: %s, deaths: %s, recovered: %s" % (self.confirmed, self.deaths, self.recovered)
