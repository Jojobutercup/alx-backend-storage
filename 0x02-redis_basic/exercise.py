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
        Constructor method
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store input data in Redis using a random key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


