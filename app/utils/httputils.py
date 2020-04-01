import logging

from aiohttp import ClientSession


# Singleton aiohttp.ClientSession instance.
client_session: ClientSession


LOGGER = logging.getLogger(__name__)


async def setup_client_session():
    """Set up the application-global aiohttp.ClientSession instance.

    aiohttp recommends that only one ClientSession exist for the lifetime of an application.
    See: https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request

    """
    global client_session
    LOGGER.info("Setting up global aiohttp.ClientSession.")
    client_session = ClientSession()


async def teardown_client_session():
    """Close the application-global aiohttp.ClientSession.
    """
    global client_session
    LOGGER.info("Closing global aiohttp.ClientSession.")
    await client_session.close()
