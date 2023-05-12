#!/usr/bin/env python3
"""
Module that defines a Cache class that uses Redis as a backend
"""

import redis
import uuid
from typing import Callable, Optional, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that increments a key counter every time the method is called.
    The key is the qualified name of the method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    A Cache class that uses Redis as a backend
    """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis using a generated random key.
        Returns the key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves the data associated with the input key from Redis.
        If fn is provided, applies fn to the data before returning.
        Returns None if the key is not found.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Returns the string value associated with the input key from Redis.
        Returns None if the key is not found.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Returns the integer value associated with the input key from Redis.
        Returns None if the key is not found.
        """
        return self.get(key, fn=int)

