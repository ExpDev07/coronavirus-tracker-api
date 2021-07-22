import logging

from aiohttp import ClientSession
from dateutil.parser import parse

class Utils: 
    # Singleton aiohttp.ClientSession instance.
    CLIENT_SESSION: ClientSession

    LOGGER = logging.getLogger(__name__)

    async def setup_client_session():
        """Set up the application-global aiohttp.ClientSession instance.

        aiohttp recommends that only one ClientSession exist for the lifetime of an application.
        See: https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request

        """
        global CLIENT_SESSION  # pylint: disable=global-statement
        LOGGER.info("Setting up global aiohttp.ClientSession.")
        CLIENT_SESSION = ClientSession()

    async def teardown_client_session():
        """Close the application-global aiohttp.ClientSession.
        """
        global CLIENT_SESSION  # pylint: disable=global-statement
        LOGGER.info("Closing global aiohttp.ClientSession.")
        await CLIENT_SESSION.close()


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