import asyncio
import os
import sys
import logging
from dotenv import load_dotenv

# Add the project root to sys.path
sys.path.append(os.getcwd())
load_dotenv()

from app.core.redis_cache import redis_cache

logging.basicConfig(level=logging.INFO)

@redis_cache.cache_result(ttl=10, prefix="rest_test")
async def slow_function(n):
    print(f"Executing slow_function for {n} (simulated 1s delay)...")
    await asyncio.sleep(1)
    return {"result": n * 2, "timestamp": "cached_via_rest_api"}

async def main():
    print("--- Redis Cloud REST Cache Test ---")
    
    # 1. First call (should be slow)
    print("Call 1...")
    res1 = await slow_function(42)
    print(f"Result 1: {res1}")
    
    # 2. Second call (should be fast - cache hit)
    print("\nCall 2 (should be fast if Cloud API is working)...")
    res2 = await slow_function(42)
    print(f"Result 2: {res2}")
    
    # 3. Different args (should be slow)
    print("\nCall 3 (different args)...")
    res3 = await slow_function(100)
    print(f"Result 3: {res3}")

if __name__ == "__main__":
    asyncio.run(main())
