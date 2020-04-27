"""app.caches.py"""
# from walrus import Database
import logging
import asyncio
import functools

import aiocache

import config

LOGGER = logging.getLogger(name="app.caches")

SETTINGS = config.get_settings()

if SETTINGS.rediscloud_url:
    REDIS_URL = SETTINGS.rediscloud_url
else:
    REDIS_URL = SETTINGS.local_redis_url


@functools.lru_cache()
def get_cache(namespace, redis=False) -> aiocache.RedisCache:
    """Retunr """
    if redis:
        return aiocache.RedisCache(
            endpoint=REDIS_URL.host,
            port=REDIS_URL.port,
            password=REDIS_URL.password,
            namespace=namespace,
            create_connection_timeout=5,
        )
    return aiocache.SimpleMemoryCache(namespace=namespace)


CACHE = get_cache("test", redis=False)


async def cach_test():
    try:
        await CACHE.set("foo", {"foobar": "bar"}, ttl=30)
    except OSError as redis_err:
        LOGGER.error(f"Redis Error: {redis_err}")
        return
    print(await CACHE.get("foo"))
    await CACHE.close()


if __name__ == "__main__":
    # print(REDIS_DB)
    # h = REDIS_DB.Hash("Test Hash")
    # h["foo"] = "bar"
    # print(h)
    asyncio.get_event_loop().run_until_complete(cach_test())
