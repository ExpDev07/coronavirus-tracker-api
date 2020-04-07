from enum import Enum


class Sources(str, Enum):
    """
    A source available for retrieving data.
    """

    jhu = "jhu"
    csbs = "csbs"
    nyt = "nyt"
