#!/usr/bin/env python3
"""
BizOSaaS Platform Connectivity Test
Tests all core infrastructure components before full deployment
"""

import asyncio
import asyncpg
import redis
import requests
from datetime import datetime
import sys

async def test_postgresql():
    """Test PostgreSQL connection"""
    try:
        conn = await asyncpg.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='SharedInfra2024!SuperSecure',
            database='bizosaas'
        )
        
        result = await conn.fetchval('SELECT 1')
        await conn.close()
        
        if result == 1:
            print("✅ PostgreSQL: Connected successfully")
            return True
        else:
            print("❌ PostgreSQL: Unexpected result")
            return False
            
    except Exception as e:
        print(f"❌ PostgreSQL: {e}")
        return False

def test_redis():
    """Test Redis connection"""
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        r.set('test_key', 'test_value')
        value = r.get('test_key')
        r.delete('test_key')
        
        if value == b'test_value':
            print("✅ Redis: Connected successfully")
            return True
        else:
            print("❌ Redis: Unexpected result")
            return False
            
    except Exception as e:
        print(f"❌ Redis: {e}")
        return False

def test_services():
    """Test running services"""
    services = {
        'API Gateway': 'http://localhost:8080/health',
        'AI Agents': 'http://localhost:8001/health',
        'Django CRM': 'http://localhost:8007/health/',
        'Wagtail CMS': 'http://localhost:8010/admin/',
    }
    
    results = {}
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 302]:  # 302 for redirects like Wagtail admin
                print(f"✅ {name}: Service responding")
                results[name] = True
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
                results[name] = False
        except Exception as e:
            print(f"❌ {name}: {e}")
            results[name] = False
    
    return results

async def main():
    """Run all connectivity tests"""
    print("🚀 BizOSaaS Platform Connectivity Test")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    # Test infrastructure
    print("📦 Testing Infrastructure Components:")
    pg_ok = await test_postgresql()
    redis_ok = test_redis()
    print()
    
    # Test services
    print("🌐 Testing Running Services:")
    service_results = test_services()
    print()
    
    # Summary
    print("📊 Test Summary:")
    print(f"PostgreSQL: {'✅' if pg_ok else '❌'}")
    print(f"Redis: {'✅' if redis_ok else '❌'}")
    
    for service, status in service_results.items():
        print(f"{service}: {'✅' if status else '❌'}")
    
    # Overall status
    all_infrastructure = pg_ok and redis_ok
    working_services = sum(service_results.values())
    total_services = len(service_results)
    
    print()
    if all_infrastructure and working_services >= 3:
        print("🎉 Platform Status: READY FOR CONTAINERIZATION")
        print(f"Infrastructure: ✅ | Services: {working_services}/{total_services} working")
        sys.exit(0)
    elif all_infrastructure:
        print("⚠️  Platform Status: INFRASTRUCTURE OK, SOME SERVICES DOWN")
        print(f"Infrastructure: ✅ | Services: {working_services}/{total_services} working")
        sys.exit(1)
    else:
        print("🔥 Platform Status: INFRASTRUCTURE ISSUES")
        print(f"Infrastructure: ❌ | Services: {working_services}/{total_services} working")
        sys.exit(2)

if __name__ == "__main__":
    asyncio.run(main())