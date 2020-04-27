"""app.caches.py"""
import functools
import logging
from typing import Union

import aiocache

from .config import get_settings

LOGGER = logging.getLogger(name="app.caches")

SETTINGS = get_settings()

if SETTINGS.rediscloud_url:
    REDIS_URL = SETTINGS.rediscloud_url
    LOGGER.info("Using Rediscloud")
else:
    REDIS_URL = SETTINGS.local_redis_url
    LOGGER.info("Using Local Redis")


@functools.lru_cache()
def get_cache(namespace) -> Union[aiocache.RedisCache, aiocache.SimpleMemoryCache]:
    """Retunr """
    if REDIS_URL:
        LOGGER.info("using RedisCache")
        return aiocache.RedisCache(
            endpoint=REDIS_URL.host,
            port=REDIS_URL.port,
            password=REDIS_URL.password,
            namespace=namespace,
            create_connection_timeout=5,
        )
    LOGGER.info("using SimpleMemoryCache")
    return aiocache.SimpleMemoryCache(namespace=namespace)


async def check_cache(data_id: str, namespace: str = None):
    """Check the data of a cache given an id."""
    cache = get_cache(namespace)
    result = await cache.get(data_id, None)
    LOGGER.info(f"{data_id} cache pulled")
    await cache.close()
    return result


async def load_cache(data_id: str, data, namespace: str = None, cache_life: int = 3600):
    """Load data into the cache."""
    cache = get_cache(namespace)
    await cache.set(data_id, data, ttl=cache_life)
    LOGGER.info(f"{data_id} cache loaded")
    await cache.close()
