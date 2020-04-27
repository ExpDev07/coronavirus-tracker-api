"""app.redis_cache.py"""
# from walrus import Database
import asyncio
import functools

import aiocache

import config

SETTINGS = config.get_settings()

if SETTINGS.rediscloud_url:
    REDIS_URL = SETTINGS.rediscloud_url
else:
    REDIS_URL = SETTINGS.local_redis_url


@functools.lru_cache()
def get_cache(namespace):
    return aiocache.Cache(
        aiocache.Cache.REDIS,
        endpoint=REDIS_URL.host,
        port=REDIS_URL.port,
        password=REDIS_URL.password,
        namespace=namespace,
        create_connection_timeout=5,
    )


REDIS_CACHE = get_cache("test")


async def cach_test():
    # CACHE = REDIS_DB.cache()
    await REDIS_CACHE.set("foo", "bar", ttl=30)
    print(await REDIS_CACHE.get("foo"))
    await REDIS_CACHE.close()


if __name__ == "__main__":
    # print(REDIS_DB)
    # h = REDIS_DB.Hash("Test Hash")
    # h["foo"] = "bar"
    # print(h)
    asyncio.get_event_loop().run_until_complete(cach_test())
