#!/usr/bin/env python3

"""
Cache module
"""

import random
import redis
import uuid
from typing import Callable, Optional, Union

def call_history(method: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        redis_instance = redis.Redis()
        redis_instance.rpush(input_key, str(args))
        result = method(*args, **kwargs)
        redis_instance.rpush(output_key, result)

        return result
    return wrapper

class Cache:
    """
    Cache class
    """

    def __init__(self):
        """
        Initializes a new instance of the Cache class.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis using a randomly generated key.

        Args:
            data: The data to store in Redis.

        Returns:
            A randomly generated key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, bytes, int, float]]:
        """
        Gets the value associated with the specified key from Redis.

        Args:
            key: The key to lookup in Redis.
            fn: An optional callable that takes a byte string and returns the desired type.

        Returns:
            The value associated with the specified key, converted to the desired type if fn is specified.
            None if the key does not exist in Redis.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Gets the string value associated with the specified key from Redis.

        Args:
            key: The key to lookup in Redis.

        Returns:
            The string value associated with the specified key, or None if the key does not exist in Redis.
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Gets the integer value associated with the specified key from Redis.

        Args:
            key: The key to lookup in Redis.

        Returns:
            The integer value associated with the specified key, or None if the key does not exist in Redis.
        """
        return self.get(key, fn=lambda x: int(x))


if __name__ == '__main__':
    Cache = Cache()

    s1 = Cache.store("first")
    print(s1)
    s2 = Cache.store("second")
    print(s2)
    s3 = Cache.store("third")
    print(s3)

    inputs = Cache._redis.lrange(f"{Cache.store.__qualname__}:inputs", 0, -1)
    outputs = Cache._redis.lrange(f"{Cache.store.__qualname__}:outputs", 0, -1)

    print("inputs:", inputs)
    print("outputs:", outputs)

