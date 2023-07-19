#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional


class Cache:
    """Represents a class Cache"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Create a store method that takes a
        data argument and returns a string"""
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self,
            key:str,
            fn: Optional[callable] = None) -> Union[str, bytes, int, float]:
        """get the element"""
        data = self._redis.get(key)
        if (fn is not None):
            return fn(data)
        return (data)

    def get_str(self, data: str) -> str:
        """Conversion function"""
        return data.decode('utf-8')

    def get_int(self, data:str) -> int:
        """conversion function"""
        return int(data)

