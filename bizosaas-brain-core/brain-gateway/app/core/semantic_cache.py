import os
import logging
import json
import asyncio
from typing import Dict, Any, Optional
from langcache import LangCache
from app.core.vault import get_config_val
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class SemanticCache:
    """
    Redis LangCache integration for LLM response caching.
    Uses Redis Cloud's managed LangCache service with server-side embeddings.
    Wraps the synchronous SDK in async methods to avoid blocking the event loop.
    """
    
    def __init__(self):
        self.api_key = get_config_val("LANGCACHE_API_KEY")
        self.cache_id = "c8f7b6d3cc024c578f91a83ec05d12f1"
        self.url = "https://aws-ap-south-1.langcache.redis.io"
        self._executor = ThreadPoolExecutor(max_workers=5)
        
        if not self.api_key:
            logger.warning("LANGCACHE_API_KEY not set, semantic cache disabled")
            self.client = None
            return

        try:
            self.client = LangCache(
                server_url=self.url,
                cache_id=self.cache_id,
                api_key=self.api_key
            )
            logger.info(f"Initialized LangCache connected to {self.cache_id}")
        except Exception as e:
            logger.error(f"Failed to initialize LangCache: {e}")
            self.client = None

    async def get(self, query: str, similarity_threshold: float = 0.95) -> Optional[str]:
        """
        Retrieve cached response for a similar query.
        Async wrapper for synchronous SDK call.
        """
        if not self.client:
            return None
            
        loop = asyncio.get_running_loop()
        try:
            # Run the synchronous search in a thread pool
            result = await loop.run_in_executor(
                self._executor,
                lambda: self.client.search(
                    prompt=query,
                    search_strategies=["semantic"]
                )
            )
            
            if result and hasattr(result, "data") and len(result.data) > 0:
                # result.data is the list of hits
                match = result.data[0]
                logger.info(f"LangCache HIT for query: {query[:50]}...")
                return match.response
            
            logger.debug(f"LangCache MISS for query: {query[:50]}...")
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving from LangCache: {e}")
            return None
    
    async def set(
        self,
        query: str,
        response: str,
        metadata: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None
    ):
        """
        Store a query-response pair in the cache.
        Async wrapper for synchronous SDK call.
        """
        if not self.client:
            return

        loop = asyncio.get_running_loop()
        try:
            await loop.run_in_executor(
                self._executor,
                lambda: self.client.set(
                    prompt=query,
                    response=response,
                    attributes=metadata or {}
                )
            )
            logger.info(f"Cached response in LangCache for query: {query[:50]}...")
            
        except Exception as e:
            logger.error(f"Error storing in LangCache: {e}")

    async def invalidate(self, pattern: str = "*"):
        """
        Placeholder for invalidation.
        """
        logger.warning("Manual invalidation not fully supported in LangCache SDK wrapper yet.")

# Singleton instance
semantic_cache = SemanticCache()
