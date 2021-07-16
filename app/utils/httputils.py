"""app.utils.httputils.py"""
import logging

from aiohttp import ClientSession


class Session:
    __CLIENT_SESSION: ClientSession
    __LOGGER = logging.getLogger(__name__)
    
    async def setup_client_session(self) -> None:
        """Set up the application-global aiohttp.ClientSession instance.

        aiohttp recommends that only one ClientSession exist for the lifetime of an application.
        See: https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request

        """
        self.__LOGGER.info("Setting up global aiohttp.ClientSession.")
        self.__CLIENT_SESSION = ClientSession()
    


    async def teardown_client_session():
        """Close the application-global aiohttp.ClientSession.
        """
        self.__LOGGER.info("Closing global aiohttp.ClientSession.")
        await self.__CLIENT_SESSION.close()




