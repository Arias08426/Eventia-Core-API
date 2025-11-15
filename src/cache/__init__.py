"""
Sistema de caché con Redis
"""
from .redis_client import RedisClient, cache

__all__ = ["RedisClient", "cache"]
