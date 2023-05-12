#!/usr/bin/env python3

"""
Cache module
"""

import redis
import uuid
from typing import Union, Callable


class Cache:
    """
    Cache class that stores data in Redis using random keys.
    """
    def __init__(self):
        """
        Initialize Cache instance with Redis client instance and flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.

        Args:
            data: The data to be stored in Redis. Can be a str, bytes, int or float.

        Returns:
            A string representing the key under which the data was stored in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve the value associated with the given key from Redis.

        Args:
            key: A string representing the key under which the data is stored in Redis.
            fn: An optional callable to be used to convert the retrieved data to the desired format.

        Returns:
            The value associated with the given key in Redis, converted to the desired format using the provided callable.
            If the key does not exist in Redis, returns None.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve the value associated with the given key from Redis and convert it to a string.

        Args:
            key: A string representing the key under which the data is stored in Redis.

        Returns:
            The value associated with the given key in Redis, converted to a string.
            If the key does not exist in Redis, returns None.
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve the value associated with the given key from Redis and convert it to an integer.

        Args:
            key: A string representing the key under which the data is stored in Redis.

        Returns:
            The value associated with the given key in Redis, converted to an integer.
            If the key does not exist in Redis, returns None.
        """
        return self.get(key, fn=lambda x: int(x))



