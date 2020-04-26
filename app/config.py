"""app.config.py"""
import functools
import logging

import pydantic

CFG_LOGGER = logging.getLogger("app.config")


class _Settings(pydantic.BaseSettings):
    port: int = 5000


@functools.lru_cache()
def get_settings(**kwargs):
    """
    Read settings from the environment or `.env` file.
    https://pydantic-docs.helpmanual.io/usage/settings/#dotenv-env-support

    Usage:
        import app.config

        settings = app.config.get_settings(_env_file="")
        port_number = settings.port
    """
    CFG_LOGGER.info("Loading Config settings from Environment ...")
    return _Settings(**kwargs)
