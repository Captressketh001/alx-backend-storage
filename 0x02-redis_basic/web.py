#!/usr/bin/env python3
"""Implement an expiring web cache and tracker"""
import redis
imprt requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
"""redis
storage"""


def data_catcher(method: Callable) -> Callable:
    """Wrapper Function
    """
    @wraps(method)
    def invoker(url) -> str:
        """Wrapper Function
        """
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result: {url}')
        if result:
            return result.decode("utf-8")
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'count:{}', 10, result)
        return
    return invoker


@data_catcher
def get_page(url: str) -> str:
    """return url"""
    return request.get(url).text

