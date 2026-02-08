#!/usr/bin/env python3
"""
BizOSaaS AI Response Caching Service
FastAPI-Cache2 integration for high-performance AI response caching
"""

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as aioredis
from typing import Dict, Any, Optional, Union, Callable
import json
import hashlib
import os
import logging
from datetime import datetime, timedelta
import asyncio

# Set up logging
logger = logging.getLogger(__name__)

class BizOSaaSCacheService:
    """Enhanced caching service for AI responses and API calls"""
    
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client = None
        self.cache_prefix = "bizosaas"
        
        # Cache TTL settings (in seconds)
        self.cache_ttl = {
            "ai_response": 3600,      # AI responses cached for 1 hour
            "api_call": 300,          # API calls cached for 5 minutes
            "user_data": 1800,        # User data cached for 30 minutes
            "tenant_config": 7200,    # Tenant config cached for 2 hours
            "lead_analysis": 1800,    # Lead analysis cached for 30 minutes
            "content_generation": 3600, # Content generation cached for 1 hour
            "seo_analysis": 7200,     # SEO analysis cached for 2 hours
            "social_media": 900,      # Social media data cached for 15 minutes
            "ecommerce_data": 600,    # E-commerce data cached for 10 minutes
        }
        
    async def initialize(self):
        """Initialize Redis connection and FastAPI-Cache2"""
        try:
            # Create Redis connection
            self.redis_client = aioredis.from_url(
                self.redis_url,
                encoding="utf8",
                decode_responses=True
            )
            
            # Test connection
            await self.redis_client.ping()
            logger.info("Redis connection established successfully")
            
            # Initialize FastAPI-Cache2
            FastAPICache.init(
                RedisBackend(self.redis_client),
                prefix=f"{self.cache_prefix}:fastapi_cache"
            )
            
            logger.info("BizOSaaS Cache Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize cache service: {e}")
            raise
    
    def generate_cache_key(self, category: str, tenant_id: str, identifier: str, params: Dict[str, Any] = None) -> str:
        """Generate consistent cache keys"""
        base_key = f"{self.cache_prefix}:{category}:{tenant_id}:{identifier}"
        
        if params:
            # Sort parameters for consistent hashing
            param_str = json.dumps(params, sort_keys=True)
            param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
            base_key += f":{param_hash}"
        
        return base_key
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.redis_client:
                value = await self.redis_client.get(key)
                if value:
                    return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL"""
        try:
            if self.redis_client:
                serialized_value = json.dumps(value, default=str)
                await self.redis_client.setex(key, ttl, serialized_value)
                return True
            return False
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            if self.redis_client:
                await self.redis_client.delete(key)
                return True
            return False
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        try:
            if self.redis_client:
                keys = await self.redis_client.keys(pattern)
                if keys:
                    deleted_count = await self.redis_client.delete(*keys)
                    logger.info(f"Deleted {deleted_count} keys matching pattern: {pattern}")
                    return deleted_count
            return 0
        except Exception as e:
            logger.error(f"Cache pattern delete error for pattern {pattern}: {e}")
            return 0
    
    async def invalidate_tenant_cache(self, tenant_id: str, category: Optional[str] = None) -> int:
        """Invalidate all cache entries for a tenant"""
        if category:
            pattern = f"{self.cache_prefix}:{category}:{tenant_id}:*"
        else:
            pattern = f"{self.cache_prefix}:*:{tenant_id}:*"
        
        return await self.delete_pattern(pattern)
    
    async def cache_ai_response(self, tenant_id: str, prompt_hash: str, response: Dict[str, Any]) -> bool:
        """Cache AI response with metadata"""
        key = self.generate_cache_key("ai_response", tenant_id, prompt_hash)
        
        cached_response = {
            "response": response,
            "cached_at": datetime.utcnow().isoformat(),
            "tenant_id": tenant_id,
            "cache_hit": True
        }
        
        return await self.set(key, cached_response, self.cache_ttl["ai_response"])
    
    async def get_cached_ai_response(self, tenant_id: str, prompt_hash: str) -> Optional[Dict[str, Any]]:
        """Get cached AI response"""
        key = self.generate_cache_key("ai_response", tenant_id, prompt_hash)
        return await self.get(key)
    
    async def cache_api_response(self, tenant_id: str, api_endpoint: str, params: Dict[str, Any], response: Any) -> bool:
        """Cache API response"""
        key = self.generate_cache_key("api_call", tenant_id, api_endpoint, params)
        
        cached_data = {
            "response": response,
            "cached_at": datetime.utcnow().isoformat(),
            "endpoint": api_endpoint,
            "params": params
        }
        
        return await self.set(key, cached_data, self.cache_ttl["api_call"])
    
    async def get_cached_api_response(self, tenant_id: str, api_endpoint: str, params: Dict[str, Any]) -> Optional[Any]:
        """Get cached API response"""
        key = self.generate_cache_key("api_call", tenant_id, api_endpoint, params)
        cached_data = await self.get(key)
        return cached_data.get("response") if cached_data else None
    
    async def cache_user_data(self, tenant_id: str, user_id: str, data: Dict[str, Any]) -> bool:
        """Cache user-specific data"""
        key = self.generate_cache_key("user_data", tenant_id, user_id)
        return await self.set(key, data, self.cache_ttl["user_data"])
    
    async def get_cached_user_data(self, tenant_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get cached user data"""
        key = self.generate_cache_key("user_data", tenant_id, user_id)
        return await self.get(key)
    
    async def cache_tenant_config(self, tenant_id: str, config: Dict[str, Any]) -> bool:
        """Cache tenant configuration"""
        key = self.generate_cache_key("tenant_config", tenant_id, "config")
        return await self.set(key, config, self.cache_ttl["tenant_config"])
    
    async def get_cached_tenant_config(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Get cached tenant configuration"""
        key = self.generate_cache_key("tenant_config", tenant_id, "config")
        return await self.get(key)
    
    async def cache_lead_analysis(self, tenant_id: str, lead_id: str, analysis: Dict[str, Any]) -> bool:
        """Cache lead analysis results"""
        key = self.generate_cache_key("lead_analysis", tenant_id, lead_id)
        return await self.set(key, analysis, self.cache_ttl["lead_analysis"])
    
    async def get_cached_lead_analysis(self, tenant_id: str, lead_id: str) -> Optional[Dict[str, Any]]:
        """Get cached lead analysis"""
        key = self.generate_cache_key("lead_analysis", tenant_id, lead_id)
        return await self.get(key)
    
    async def cache_seo_analysis(self, tenant_id: str, url_hash: str, analysis: Dict[str, Any]) -> bool:
        """Cache SEO analysis results"""
        key = self.generate_cache_key("seo_analysis", tenant_id, url_hash)
        return await self.set(key, analysis, self.cache_ttl["seo_analysis"])
    
    async def get_cached_seo_analysis(self, tenant_id: str, url_hash: str) -> Optional[Dict[str, Any]]:
        """Get cached SEO analysis"""
        key = self.generate_cache_key("seo_analysis", tenant_id, url_hash)
        return await self.get(key)
    
    def create_cache_decorator(self, category: str, ttl: Optional[int] = None):
        """Create custom cache decorator for specific categories"""
        cache_ttl = ttl or self.cache_ttl.get(category, 3600)
        
        @cache(expire=cache_ttl, namespace=f"{self.cache_prefix}:{category}")
        def cache_decorator(func):
            return func
        
        return cache_decorator
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            if not self.redis_client:
                return {"status": "disconnected"}
            
            # Get Redis info
            redis_info = await self.redis_client.info()
            
            # Count keys by category
            categories = {}
            for category in self.cache_ttl.keys():
                pattern = f"{self.cache_prefix}:{category}:*"
                keys = await self.redis_client.keys(pattern)
                categories[category] = len(keys)
            
            return {
                "status": "connected",
                "redis_info": {
                    "used_memory": redis_info.get("used_memory_human"),
                    "connected_clients": redis_info.get("connected_clients"),
                    "total_keys": redis_info.get("db0", {}).get("keys", 0) if "db0" in redis_info else 0,
                    "uptime_days": redis_info.get("uptime_in_days")
                },
                "categories": categories,
                "cache_ttl": self.cache_ttl,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {"status": "error", "error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for cache service"""
        try:
            if self.redis_client:
                await self.redis_client.ping()
                return {
                    "status": "healthy",
                    "service": "cache",
                    "backend": "redis",
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "status": "unhealthy",
                    "service": "cache",
                    "error": "Redis client not initialized",
                    "timestamp": datetime.utcnow().isoformat()
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "service": "cache",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Cache service connections closed")

# Global cache service instance
cache_service = BizOSaaSCacheService()

# Convenience decorators for common caching patterns
def cache_ai_response(expire: int = 3600):
    """Decorator for caching AI responses"""
    return cache(expire=expire, namespace=f"{cache_service.cache_prefix}:ai_response")

def cache_api_call(expire: int = 300):
    """Decorator for caching API calls"""
    return cache(expire=expire, namespace=f"{cache_service.cache_prefix}:api_call")

def cache_user_data(expire: int = 1800):
    """Decorator for caching user data"""
    return cache(expire=expire, namespace=f"{cache_service.cache_prefix}:user_data")

def cache_tenant_data(expire: int = 7200):
    """Decorator for caching tenant data"""
    return cache(expire=expire, namespace=f"{cache_service.cache_prefix}:tenant_config")