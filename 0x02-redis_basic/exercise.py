#!/usr/bin/env python3
"""
Cache module
"""
import redis
import uuid
from typing import Any, Callable, Optional, Union


class Cache:
    """
    Cache class that uses Redis to store data.
    """

    def __init__(self) -> None:
        """
        Constructor that initializes the Redis client and flushes the instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key and stores the input data in Redis using the random key.

        Args:
            data: The data to be stored. Can be a str, bytes, int or float.

        Returns:
            The generated key as a str.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[Any], Any]] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves the data from Redis for the given key and applies the optional conversion function.

        Args:
            key: The key of the data to be retrieved.
            fn: An optional callable that will be used to convert the data back to the desired format.

        Returns:
            The retrieved data, optionally converted to the desired format.
            Returns None if the key does not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves the data from Redis for the given key as a string.

        Args:
            key: The key of the data to be retrieved.

        Returns:
            The retrieved data as a string.
            Returns None if the key does not exist.
        """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves the data from Redis for the given key as an integer.

        Args:
            key: The key of the data to be retrieved.

        Returns:
            The retrieved data as an integer.
            Returns None if the key does not exist.
        """
        return self.get(key, fn=int)


