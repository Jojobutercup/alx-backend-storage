#!/usr/bin/env python3

"""
Cache module
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class
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

