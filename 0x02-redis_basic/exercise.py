#!/usr/bin/env python3
"""
Redis exercise module
"""

import uuid
import redis
from typing import Callable, List


class Cache:
    """
    Cache class
    """

    def __init__(self):
        """
        Constructor
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def _generate_key() -> str:
        """
        Generates a unique key
        """
        return str(uuid.uuid4())

    @staticmethod
    def call_history(method: Callable) -> Callable:
        """
        Decorator to store inputs and outputs history of a function
        """
        def wrapper(self, *args, **kwargs):
            inputs_key = f"{method.__qualname__}:inputs"
            outputs_key = f"{method.__qualname__}:outputs"

            # Append input to the inputs key
            self._redis.rpush(inputs_key, str(args))

            # Execute the function and store the output
            output = method(self, *args, **kwargs)
            self._redis.rpush(outputs_key, output)

            return output

        return wrapper

    @call_history
    def store(self, value: str) -> str:
        """
        Store a value in the cache
        """
        key = self._generate_key()
        self._redis.set(key, value)
        return key

    def get(self, key: str) -> str:
        """
        Retrieve a value from the cache
        """
        return self._redis.get(key)


