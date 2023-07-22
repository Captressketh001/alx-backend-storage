#!/usr/bin/env python3
"""
Writing strings to Redis
"""
from functools import wraps
import redis
from uuid import uuid4
from typing import Union, Callable, Optional

def call_history(method: Callable) -> Callable:
    key = method.__qualname__
    inputs = key + ':inputs'
    outputs = key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper function"""
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def count_calls(method: Callable) -> Callable:

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper function"""
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper

    
class Cache:
    """Represents a class Cache"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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

