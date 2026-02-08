import pytest
import os
import redis.asyncio as redis

@pytest.mark.asyncio
async def test_redis_connectivity():
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        pytest.skip("REDIS_URL not set")
    
    r = redis.from_url(redis_url)
    try:
        pong = await r.ping()
        assert pong is True
    finally:
        await r.close()

@pytest.mark.asyncio
async def test_redis_set_get():
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        pytest.skip("REDIS_URL not set")
    
    r = redis.from_url(redis_url)
    try:
        await r.set("test_key", "test_value")
        val = await r.get("test_key")
        assert val == b"test_value"
        await r.delete("test_key")
    finally:
        await r.close()
