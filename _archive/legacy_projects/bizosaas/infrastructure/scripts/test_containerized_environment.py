#!/usr/bin/env python3
"""
BizOSaaS Containerized Environment Test

This script tests that our containerized environment setup is correct
by validating connections to test infrastructure and configuration.
"""

import asyncio
import asyncpg
import redis.asyncio as redis
import httpx
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test Environment Configuration
TEST_CONFIG = {
    "postgres": {
        "host": "localhost",
        "port": 5434,
        "database": "postgres", 
        "user": "postgres",
        "password": os.getenv("POSTGRES_PASSWORD", "SharedInfra2024!SuperSecure")
    },
    "redis": {
        "host": "localhost", 
        "port": 6381,
        "password": os.getenv("REDIS_PASSWORD", "SecureRedis2024Unified")
    },
    "native_services": {
        "brain_api": "http://localhost:8001",
        "dashboard": "http://localhost:5004", 
        "wagtail_cms": "http://localhost:4000",
        "directory": "http://localhost:4001",
        "telegram": "http://localhost:4006",
        "image_service": "http://localhost:4007"
    }
}

async def test_postgres_connection():
    """Test connection to test PostgreSQL container"""
    try:
        conn = await asyncpg.connect(
            host=TEST_CONFIG["postgres"]["host"],
            port=TEST_CONFIG["postgres"]["port"],
            database=TEST_CONFIG["postgres"]["database"],
            user=TEST_CONFIG["postgres"]["user"],
            password=TEST_CONFIG["postgres"]["password"]
        )
        
        # Test basic query
        result = await conn.fetchrow("SELECT version()")
        await conn.close()
        
        return {
            "status": "✅ SUCCESS",
            "service": "PostgreSQL Test Container",
            "port": TEST_CONFIG["postgres"]["port"],
            "version": result["version"][:50] + "..." if result else "Unknown"
        }
    except Exception as e:
        return {
            "status": "❌ FAILED", 
            "service": "PostgreSQL Test Container",
            "port": TEST_CONFIG["postgres"]["port"],
            "error": str(e)
        }

async def test_redis_connection():
    """Test connection to test Redis container"""
    try:
        r = redis.Redis(
            host=TEST_CONFIG["redis"]["host"],
            port=TEST_CONFIG["redis"]["port"],
            password=TEST_CONFIG["redis"]["password"],
            decode_responses=True
        )
        
        # Test basic operations
        await r.set("test_key", "containerized_test")
        result = await r.get("test_key") 
        await r.delete("test_key")
        await r.close()
        
        return {
            "status": "✅ SUCCESS",
            "service": "Redis Test Container", 
            "port": TEST_CONFIG["redis"]["port"],
            "test_result": result
        }
    except Exception as e:
        return {
            "status": "❌ FAILED",
            "service": "Redis Test Container",
            "port": TEST_CONFIG["redis"]["port"], 
            "error": str(e)
        }

async def test_native_service(name: str, url: str):
    """Test connection to native running services"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Try /health first, then fall back to root
            for endpoint in ["/health", "/"]:
                try:
                    response = await client.get(f"{url}{endpoint}")
                    if response.status_code in [200, 404, 422]:  # Any response means service is running
                        return {
                            "status": "✅ SUCCESS" if response.status_code == 200 else "✅ RUNNING",
                            "service": f"Native {name}",
                            "url": url,
                            "endpoint": endpoint,
                            "status_code": response.status_code,
                            "response": "Service responding" 
                        }
                except Exception:
                    continue
            
            # If both endpoints failed
            return {
                "status": "❌ FAILED",
                "service": f"Native {name}",
                "url": url,
                "error": "No response from /health or / endpoints"
            }
    except Exception as e:
        return {
            "status": "❌ FAILED",
            "service": f"Native {name}",
            "url": url,
            "error": str(e)
        }

async def validate_environment_configuration():
    """Validate that all environment variables are correctly configured"""
    required_vars = [
        "POSTGRES_PASSWORD",
        "REDIS_PASSWORD", 
        "JWT_SECRET_KEY",
        "OPENROUTER_API_KEY",
        "TELEGRAM_JONNYAI_BOT_TOKEN",
        "TELEGRAM_BIZOHOLIC_BOT_TOKEN"
    ]
    
    results = []
    for var in required_vars:
        value = os.getenv(var)
        results.append({
            "variable": var,
            "status": "✅ SET" if value else "❌ MISSING",
            "length": len(value) if value else 0,
            "masked": f"{value[:8]}..." if value and len(value) > 8 else "Not set"
        })
    
    return results

async def main():
    """Main test execution"""
    print("🚀 BizOSaaS Containerized Environment Test")
    print("=" * 60)
    
    # Test infrastructure containers
    print("\n📊 Testing Test Infrastructure Containers:")
    postgres_result = await test_postgres_connection()
    redis_result = await test_redis_connection()
    
    print(f"  {postgres_result['status']} {postgres_result['service']} (Port {postgres_result['port']})")
    if 'error' in postgres_result:
        print(f"    Error: {postgres_result['error']}")
    else:
        print(f"    Version: {postgres_result['version']}")
        
    print(f"  {redis_result['status']} {redis_result['service']} (Port {redis_result['port']})")
    if 'error' in redis_result:
        print(f"    Error: {redis_result['error']}")
    else:
        print(f"    Test Result: {redis_result['test_result']}")
    
    # Test native services
    print("\n🔄 Testing Native Running Services:")
    service_tasks = [
        test_native_service(name, url) 
        for name, url in TEST_CONFIG["native_services"].items()
    ]
    
    service_results = await asyncio.gather(*service_tasks, return_exceptions=True)
    
    for result in service_results:
        if isinstance(result, Exception):
            print(f"  ❌ FAILED Service test: {result}")
        else:
            print(f"  {result['status']} {result['service']}")
            if 'error' in result:
                print(f"    Error: {result['error']}")
            else:
                print(f"    Status: {result['status_code']} - {result['url']}")
    
    # Validate environment
    print("\n🔐 Environment Configuration:")
    env_results = await validate_environment_configuration()
    for result in env_results:
        print(f"  {result['status']} {result['variable']} ({result['length']} chars)")
    
    # Summary
    print("\n📋 Test Summary:")
    total_tests = 2 + len(TEST_CONFIG["native_services"]) + len(env_results)
    passed_tests = sum([
        1 if postgres_result['status'] == "✅ SUCCESS" else 0,
        1 if redis_result['status'] == "✅ SUCCESS" else 0,
        len([r for r in service_results if not isinstance(r, Exception) and r['status'] == "✅ SUCCESS"]),
        len([r for r in env_results if r['status'] == "✅ SET"])
    ])
    
    print(f"  Tests Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("  🎉 All tests passed! Containerized environment is ready for deployment.")
        return True
    else:
        print("  ⚠️  Some tests failed. Review errors before deployment.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)