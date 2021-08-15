

from datetime import date, datetime

import requests

CACHE_TIME_MIN = 20


class LocationCachingProxy:

    def __init__(self) -> None:
        self.cache = {
        }

    def cached_get(self, request_url):
        cached_data = self.cache.get(request_url)

        if cached_data:
            cache_time = cached_data[0]
            if (datetime.now - datetime.timedelta(minutes=CACHE_TIME_MIN)) < cache_time:
                return cached_data[1]

        new_data = self.requests.get(request_url)
        self.cache[request_url] = (datetime.now(), new_data)

        return new_data


PROXY = LocationCachingProxy()
