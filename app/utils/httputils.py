"""app.utils.httputils.py"""
import logging

from aiohttp import ClientSession


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
