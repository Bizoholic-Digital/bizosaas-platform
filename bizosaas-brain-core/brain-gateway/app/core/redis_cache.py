import os
import json
import logging
import hashlib
import functools
import asyncio
from typing import Any, Callable, Optional, TypeVar, Dict
from langcache import LangCache
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

T = TypeVar("T")

class RedisCloudCache:
    """
    Managed Cloud Caching using LangCache SDK.
    Offloads all state and processing to the Redis Cloud / LangCache managed service.
    This ensures zero persistent TCP connections on the platform and leverages
    the recommended "Cloud API" approach.
    """
    def __init__(self):
        self.api_key = os.getenv("LANGCACHE_API_KEY")
        self.cache_id = "c8f7b6d3cc024c578f91a83ec05d12f1" # Same as semantic_cache for platform consistency
        self.url = os.getenv("LANGCACHE_URL", "https://aws-ap-south-1.langcache.redis.io")
        self._executor = ThreadPoolExecutor(max_workers=5)
        
        if not self.api_key:
            logger.warning("LANGCACHE_API_KEY not set, cloud caching disabled")
            self.client = None
        else:
            try:
                self.client = LangCache(
                    server_url=self.url,
                    cache_id=self.cache_id,
                    api_key=self.api_key
                )
                logger.info(f"Initialized RedisCloudCache via LangCache API ({self.cache_id})")
            except Exception as e:
                logger.error(f"Failed to initialize LangCache for RedisCloudCache: {e}")
                self.client = None

    async def get(self, key: str) -> Optional[str]:
        if not self.client:
            return None
            
        loop = asyncio.get_running_loop()
        try:
            # Using exact search strategy for direct key-value mapping
            result = await loop.run_in_executor(
                self._executor,
                lambda: self.client.search(
                    prompt=key,
                    search_strategies=["exact"]
                )
            )
            
            # SearchResponse handling: results are in the 'data' attribute
            if result and hasattr(result, "data"):
                hits = result.data
                if isinstance(hits, (list, tuple)) and len(hits) > 0:
                    logger.debug(f"Cloud Cache HIT: {key[:50]}")
                    return hits[0].response
            
            return None
        except Exception as e:
            logger.error(f"Cloud Cache GET failed: {e}")
            return None

    async def set(self, key: str, value: str):
        if not self.client:
            return

        loop = asyncio.get_running_loop()
        try:
            # Removed attributes/metadata to avoid 400 error on caches not configured for them
            await loop.run_in_executor(
                self._executor,
                lambda: self.client.set(
                    prompt=key,
                    response=value,
                )
            )
            logger.debug(f"Cloud Cache SET: {key[:50]}")
        except Exception as e:
            logger.error(f"Cloud Cache SET failed: {e}")

    def cache_result(self, ttl: int = 3600, prefix: str = "generic"):
        """
        Decorator to cache the result of an async function using LangCache Cloud API.
        """
        def decorator(func: Callable[..., Any]):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                if not self.client:
                    return await func(*args, **kwargs)

                # Generate a unique key
                key_content = f"{func.__module__}:{func.__name__}:{args}:{kwargs}"
                key_hash = hashlib.md5(key_content.encode()).hexdigest()
                cache_key = f"cache:{prefix}:{key_hash}"

                cached_data = await self.get(cache_key)
                if cached_data:
                    try:
                        return json.loads(cached_data)
                    except json.JSONDecodeError:
                        return cached_data

                # Call actual function
                result = await func(*args, **kwargs)

                # Store result
                try:
                    await self.set(cache_key, json.dumps(result))
                except Exception as e:
                    logger.error(f"Error caching to Cloud API: {e}")

                return result
            return wrapper
        return decorator

# Global instance
redis_cache = RedisCloudCache()
