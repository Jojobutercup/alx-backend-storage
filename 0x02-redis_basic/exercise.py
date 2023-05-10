#!/usr/bin/env python3
"""
A module that defines a Cache class that uses Redis for storage.
"""

import redis
import uuid
from typing import Union

class Cache:
    """
    A class that represents a cache that uses Redis for storage.
    """
    def __init__(self) -> None:
        """
        Initializes a new instance of the Cache class and flushes the Redis instance.
        """
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis using a generated key and returns the key.

        Args:
            data: The data to be stored. Can be a string, bytes, int or float.

        Returns:
            A string representing the generated key used to store the data in Redis.
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

