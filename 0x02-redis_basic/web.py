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
    using the requests module.
    
    Track the number of times the URL is accessed in
    the key "count:{url}".

    Cache the result with an expiration time of 10 seconds.
    """
    count_key = f"count:{url}"
    count = int(requests.get(f"http://slowwly.robertomurray.co.uk/delay/1000/url/{count_key}").text)
    return requests.get(url).text


if __name__ == '__main__':
    url = 'https://www.example.com'
    print(get_page(url))

