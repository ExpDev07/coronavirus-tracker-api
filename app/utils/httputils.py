"""app.utils.httputils.py"""
import logging
from aiohttp import ClientSession


class Session:
    # Singleton aiohttp.ClientSession instance.
    def __init__(self):
        __CLIENT_SESSION: ClientSession
        __LOGGER = logging.getLogger(__name__)

    def getClientSession(self):
        """returns value in __CLIENT_SESSION"""
        return self.__CLIENT_SESSION

    def getLogger(self):
        """returns value in __LOGGER"""
        return self.__LOGGER

    async def setup_client_session(self):
        """Set up the application-global aiohttp.ClientSession instance.

        aiohttp recommends that only one ClientSession exist for the lifetime of an application.
        See: https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request

        """
        # global CLIENT_SESSION  # pylint: disable=global-statement
        self.getLogger().info("Setting up global aiohttp.ClientSession.")
        self.__CLIENT_SESSION = ClientSession()

    async def teardown_client_session(self):
        """Close the application-global aiohttp.ClientSession.
        """
        # global CLIENT_SESSION  # pylint: disable=global-statement
        self.getLogger().info("Closing global aiohttp.ClientSession.")
        await self.getClientSession().close()
