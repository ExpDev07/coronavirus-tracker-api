"""app.utils.date.py"""
from dateutil.parser import parse
from datetime import datetime
import logging

LOGGER = logging.getLogger("services.location.jhu")

class Date:

    def get_history(self, list):
        return History(list).get_history

    def parse_history(key: tuple, locations: list, index: int):
        return History().parse_history(key, locations, index)

    def format_date(date, format):
        return datetime.strptime(date, format).isoformat() 

    def format_now():
        return  datetime.utcnow().isoformat() + "Z"
          

    def is_date(string, fuzzy=False):
        """
        Return whether the string can be interpreted as a date.
        - https://stackoverflow.com/a/25341965/7120095

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """

        try:
            parse(string, fuzzy=fuzzy)
            return True
        except ValueError:
            return False


class History:
    def __init__(self, history_list):
        self.history_list = history_list

    def get_history(self):
        return {date: int(float(amount or 0)) for date, amount in  self.history_list}

    
    def parse_history(key: tuple, locations: list, index: int):
        """
        Helper for validating and extracting history content from
        locations data based on index. Validates with the current country/province
        key to make sure no index/column issue.

        TEMP: solution because implement a more efficient and better approach in the refactor.
        """
        location_history = {}
        try:
            if key == (locations[index]["country"], locations[index]["province"]):
                location_history = locations[index]["history"]
        except (IndexError, KeyError):
            LOGGER.debug(f"iteration data merge error: {index} {key}")

        return location_history


