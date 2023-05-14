#!/usr/bin/env python3
"""
This module contains the cache decorator is used
to cache the result of a page
<module 'web' from '
/tmp/correction/5252228877214899593155699675041642034389_5/1234/76939/0x02-redis_basic/web.py'>
for a certain duration
"""

import requests
import time
from functools import wraps

CACHE_EXPIRATION_TIME = 10  # seconds


def cache(maxsize):
    """
    Decorator function that caches the result
    of the decorated function with
    the given expiration time in seconds.
    """
    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args):
            if args in cache:
                result, timestamp = cache[args]
                if time.time() - timestamp < maxsize:
                    return result
            result = func(*args)
            cache[args] = (result, time.time())
            return result

        return wrapper

    return decorator


@cache(CACHE_EXPIRATION_TIME)
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of the given URL
    using the requests module
    Track the number of times the URL is accessed in
    the key "count:{url}".
    Cache the result with an expiration time of 10 seconds.
    """
    count_key = f"count:{url}"
    count = int(requests.get(f"http://slowwly.robertomurray.co.uk/delay/1000/url/{count_key}").text)
    requests.get(count_key)  # Increment count
    return requests.get(url).text


if __name__ == '__main__':
    # Test with google.com
    url = 'http://google.com'
    print(get_page(url))

    # Wait for cache to expire
    time.sleep(10)

    # Test again with google.com to ensure cache has expired
    print(get_page(url))
