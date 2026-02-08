"""
Redis Cache utilities for QuantTrade
"""

import redis
import json
from typing import Any, Optional, Dict
import structlog
from contextlib import asynccontextmanager

from core.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()

# Global Redis client
redis_client: Optional[redis.Redis] = None


async def init_cache():
    """Initialize Redis cache connection"""
    global redis_client
    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            health_check_interval=30
        )

        # Test connection
        await redis_client.ping()
        logger.info("Redis cache initialized successfully")

    except Exception as e:
        logger.error("Failed to initialize Redis cache", error=str(e))
        # For development, create a mock Redis client
        redis_client = MockRedisClient()


async def close_cache():
    """Close Redis cache connection"""
    global redis_client
    if redis_client:
        try:
            if hasattr(redis_client, 'close'):
                redis_client.close()
            logger.info("Redis cache connection closed")
        except Exception as e:
            logger.error("Error closing Redis cache", error=str(e))


def get_redis_client() -> redis.Redis:
    """Get the Redis client instance"""
    if redis_client is None:
        raise RuntimeError("Redis client not initialized. Call init_cache() first.")
    return redis_client


class MockRedisClient:
    """Mock Redis client for development/testing"""

    def __init__(self):
        self.data: Dict[str, Any] = {}
        logger.info("Using mock Redis client for development")

    async def get(self, key: str) -> Optional[str]:
        return self.data.get(key)

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        self.data[key] = value
        return True

    async def setex(self, key: str, time: int, value: str) -> bool:
        self.data[key] = value
        return True

    async def delete(self, key: str) -> int:
        if key in self.data:
            del self.data[key]
            return 1
        return 0

    async def exists(self, key: str) -> int:
        return 1 if key in self.data else 0

    async def expire(self, key: str, time: int) -> bool:
        return True

    async def ping(self) -> bool:
        return True

    def close(self):
        self.data.clear()


class CacheManager:
    """High-level cache manager with JSON serialization"""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def get_json(self, key: str) -> Optional[Any]:
        """Get and deserialize JSON data from cache"""
        try:
            data = await self.redis.get(key)
            if data:
                return json.loads(data)
            return None
        except (json.JSONDecodeError, Exception) as e:
            logger.error("Error getting JSON from cache", key=key, error=str(e))
            return None

    async def set_json(self, key: str, value: Any, expiry: Optional[int] = None) -> bool:
        """Serialize and store JSON data in cache"""
        try:
            serialized = json.dumps(value, default=str)
            if expiry:
                return await self.redis.setex(key, expiry, serialized)
            else:
                return await self.redis.set(key, serialized)
        except (json.JSONEncodeError, Exception) as e:
            logger.error("Error setting JSON to cache", key=key, error=str(e))
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            result = await self.redis.delete(key)
            return result > 0
        except Exception as e:
            logger.error("Error deleting from cache", key=key, error=str(e))
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            result = await self.redis.exists(key)
            return result > 0
        except Exception as e:
            logger.error("Error checking cache existence", key=key, error=str(e))
            return False


# Cache decorators and utilities
def cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate cache key from prefix and arguments"""
    key_parts = [prefix]

    # Add positional arguments
    for arg in args:
        key_parts.append(str(arg))

    # Add keyword arguments
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}:{v}")

    return ":".join(key_parts)


@asynccontextmanager
async def cache_manager():
    """Context manager for cache operations"""
    client = get_redis_client()
    manager = CacheManager(client)
    try:
        yield manager
    except Exception as e:
        logger.error("Cache manager error", error=str(e))
        raise


# Common cache keys
class CacheKeys:
    """Common cache key patterns"""

    MARKET_QUOTE = "market:quote"
    INTRADAY_DATA = "market:intraday"
    HISTORICAL_DATA = "market:historical"
    PORTFOLIO_VALUE = "portfolio:value"
    USER_POSITIONS = "user:positions"
    STRATEGY_RESULT = "strategy:result"
    BACKTEST_RESULT = "backtest:result"
    AI_ANALYSIS = "ai:analysis"

    @staticmethod
    def market_quote(symbol: str) -> str:
        return f"{CacheKeys.MARKET_QUOTE}:{symbol.upper()}"

    @staticmethod
    def intraday_data(symbol: str, interval: str, period: str) -> str:
        return f"{CacheKeys.INTRADAY_DATA}:{symbol.upper()}:{interval}:{period}"

    @staticmethod
    def historical_data(symbol: str, start_date: str, end_date: str) -> str:
        return f"{CacheKeys.HISTORICAL_DATA}:{symbol.upper()}:{start_date}:{end_date}"

    @staticmethod
    def portfolio_value(user_id: str) -> str:
        return f"{CacheKeys.PORTFOLIO_VALUE}:{user_id}"

    @staticmethod
    def user_positions(user_id: str) -> str:
        return f"{CacheKeys.USER_POSITIONS}:{user_id}"

    @staticmethod
    def strategy_result(strategy_id: str, timestamp: str) -> str:
        return f"{CacheKeys.STRATEGY_RESULT}:{strategy_id}:{timestamp}"

    @staticmethod
    def backtest_result(backtest_id: str) -> str:
        return f"{CacheKeys.BACKTEST_RESULT}:{backtest_id}"

    @staticmethod
    def ai_analysis(agent_id: str, symbol: str, timestamp: str) -> str:
        return f"{CacheKeys.AI_ANALYSIS}:{agent_id}:{symbol.upper()}:{timestamp}"


# Cache timeouts (in seconds)
class CacheTimeouts:
    """Common cache timeout values"""

    MARKET_QUOTE = 30  # 30 seconds
    INTRADAY_DATA = 60  # 1 minute
    HISTORICAL_DATA = 3600  # 1 hour
    PORTFOLIO_VALUE = 300  # 5 minutes
    USER_POSITIONS = 300  # 5 minutes
    STRATEGY_RESULT = 1800  # 30 minutes
    BACKTEST_RESULT = 86400  # 24 hours
    AI_ANALYSIS = 1800  # 30 minutes