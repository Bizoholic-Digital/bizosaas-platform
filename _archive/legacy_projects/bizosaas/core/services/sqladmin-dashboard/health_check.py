#!/usr/bin/env python3

"""
Health Check Script for SQLAdmin Dashboard
Verifies service integration and dependencies
"""

import asyncio
import aiohttp
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine

# Configuration
UNIFIED_AUTH_URL = os.getenv("UNIFIED_AUTH_URL", "http://localhost:3002")
SQLADMIN_URL = os.getenv("SQLADMIN_URL", "http://localhost:5000")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://bizosaas:bizosaas@localhost:5432/bizosaas")
DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL", "postgresql://bizosaas:bizosaas@localhost:5432/bizosaas")

class HealthChecker:
    """Comprehensive health checker for SQLAdmin service"""
    
    def __init__(self):
        self.results = {}
    
    async def check_all(self) -> Dict[str, Any]:
        """Run all health checks"""
        print("🏥 SQLAdmin Dashboard Health Check")
        print("=" * 50)
        
        # Run all checks
        checks = [
            ("Database (Async)", self.check_database_async),
            ("Database (Sync)", self.check_database_sync),
            ("Auth Service", self.check_auth_service),
            ("SQLAdmin Service", self.check_sqladmin_service),
            ("Environment", self.check_environment),
        ]
        
        for check_name, check_func in checks:
            print(f"\n🔍 Checking {check_name}...")
            try:
                result = await check_func()
                self.results[check_name] = result
                status = "✅ PASS" if result.get("status") == "healthy" else "❌ FAIL"
                print(f"   {status}: {result.get('message', 'No message')}")
                
                if result.get("details"):
                    for key, value in result["details"].items():
                        print(f"     - {key}: {value}")
                        
            except Exception as e:
                self.results[check_name] = {"status": "error", "message": str(e)}
                print(f"   ❌ ERROR: {str(e)}")
        
        # Summary
        print(f"\n📊 Health Check Summary")
        print("=" * 50)
        
        healthy_count = sum(1 for r in self.results.values() if r.get("status") == "healthy")
        total_count = len(self.results)
        
        print(f"Total Checks: {total_count}")
        print(f"Healthy: {healthy_count}")
        print(f"Failed: {total_count - healthy_count}")
        print(f"Overall Status: {'✅ HEALTHY' if healthy_count == total_count else '❌ UNHEALTHY'}")
        
        return self.results
    
    async def check_database_async(self) -> Dict[str, Any]:
        """Check async database connection"""
        try:
            engine = create_async_engine(DATABASE_URL)
            
            async with engine.begin() as conn:
                # Test basic connectivity
                result = await conn.execute(text("SELECT 1 as test"))
                test_value = result.scalar()
                
                # Check database name
                db_result = await conn.execute(text("SELECT current_database()"))
                db_name = db_result.scalar()
                
                # Check for required tables
                tables_result = await conn.execute(text("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name IN ('users', 'tenants', 'user_sessions')
                """))
                tables = [row[0] for row in tables_result]
                
                # Check user count
                if 'users' in tables:
                    user_count_result = await conn.execute(text("SELECT COUNT(*) FROM users"))
                    user_count = user_count_result.scalar()
                else:
                    user_count = 0
            
            await engine.dispose()
            
            return {
                "status": "healthy",
                "message": "Async database connection successful",
                "details": {
                    "database": db_name,
                    "test_query": test_value == 1,
                    "required_tables": f"{len(tables)}/3 found",
                    "user_count": user_count,
                    "url": DATABASE_URL.split("@")[1] if "@" in DATABASE_URL else "configured"
                }
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Async database connection failed: {str(e)}",
                "details": {"url": DATABASE_URL.split("@")[1] if "@" in DATABASE_URL else "configured"}
            }
    
    async def check_database_sync(self) -> Dict[str, Any]:
        """Check sync database connection (for SQLAdmin)"""
        try:
            engine = create_engine(DATABASE_SYNC_URL)
            
            with engine.begin() as conn:
                # Test basic connectivity
                result = conn.execute(text("SELECT 1 as test"))
                test_value = result.scalar()
                
                # Check active connections
                conn_result = conn.execute(text("""
                    SELECT count(*) FROM pg_stat_activity 
                    WHERE state = 'active' AND datname = current_database()
                """))
                active_connections = conn_result.scalar()
            
            engine.dispose()
            
            return {
                "status": "healthy",
                "message": "Sync database connection successful",
                "details": {
                    "test_query": test_value == 1,
                    "active_connections": active_connections,
                    "url": DATABASE_SYNC_URL.split("@")[1] if "@" in DATABASE_SYNC_URL else "configured"
                }
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Sync database connection failed: {str(e)}",
                "details": {"url": DATABASE_SYNC_URL.split("@")[1] if "@" in DATABASE_SYNC_URL else "configured"}
            }
    
    async def check_auth_service(self) -> Dict[str, Any]:
        """Check unified auth service connectivity"""
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10.0)
            ) as session:
                
                # Test health endpoint
                try:
                    async with session.get(f"{UNIFIED_AUTH_URL}/health") as response:
                        if response.status == 200:
                            data = await response.json()
                            return {
                                "status": "healthy",
                                "message": "Auth service is accessible",
                                "details": {
                                    "url": UNIFIED_AUTH_URL,
                                    "response_status": response.status,
                                    "service_status": data.get("status", "unknown")
                                }
                            }
                except aiohttp.ClientError:
                    pass
                
                # Test root endpoint as fallback
                async with session.get(f"{UNIFIED_AUTH_URL}/") as response:
                    return {
                        "status": "healthy" if response.status == 200 else "unhealthy",
                        "message": f"Auth service responded with status {response.status}",
                        "details": {
                            "url": UNIFIED_AUTH_URL,
                            "response_status": response.status
                        }
                    }
                    
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Auth service connection failed: {str(e)}",
                "details": {"url": UNIFIED_AUTH_URL}
            }
    
    async def check_sqladmin_service(self) -> Dict[str, Any]:
        """Check SQLAdmin service itself"""
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=5.0)
            ) as session:
                
                # Test health endpoint if service is running
                try:
                    async with session.get(f"{SQLADMIN_URL}/api/system/health") as response:
                        if response.status in [200, 401, 403]:  # 401/403 means auth is working
                            return {
                                "status": "healthy",
                                "message": "SQLAdmin service is running",
                                "details": {
                                    "url": SQLADMIN_URL,
                                    "response_status": response.status,
                                    "auth_required": response.status in [401, 403]
                                }
                            }
                except aiohttp.ClientConnectorError:
                    return {
                        "status": "unhealthy",
                        "message": "SQLAdmin service is not running",
                        "details": {"url": SQLADMIN_URL}
                    }
                
                return {
                    "status": "unhealthy",
                    "message": f"SQLAdmin service returned unexpected status",
                    "details": {"url": SQLADMIN_URL}
                }
                
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"SQLAdmin service check failed: {str(e)}",
                "details": {"url": SQLADMIN_URL}
            }
    
    async def check_environment(self) -> Dict[str, Any]:
        """Check environment configuration"""
        required_vars = [
            "DATABASE_URL",
            "DATABASE_SYNC_URL", 
            "UNIFIED_AUTH_URL"
        ]
        
        optional_vars = [
            "SECRET_KEY",
            "DEBUG",
            "LOG_LEVEL"
        ]
        
        missing_required = []
        configured_optional = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_required.append(var)
        
        for var in optional_vars:
            if os.getenv(var):
                configured_optional.append(var)
        
        status = "healthy" if not missing_required else "unhealthy"
        message = "Environment configuration is valid" if status == "healthy" else f"Missing required variables: {', '.join(missing_required)}"
        
        return {
            "status": status,
            "message": message,
            "details": {
                "required_vars": f"{len(required_vars) - len(missing_required)}/{len(required_vars)} configured",
                "optional_vars": f"{len(configured_optional)}/{len(optional_vars)} configured",
                "missing_required": missing_required if missing_required else "none"
            }
        }

async def main():
    """Main health check function"""
    checker = HealthChecker()
    results = await checker.check_all()
    
    # Exit with error code if any checks failed
    failed_checks = [name for name, result in results.items() if result.get("status") != "healthy"]
    
    if failed_checks:
        print(f"\n❌ Health check failed. Failed checks: {', '.join(failed_checks)}")
        sys.exit(1)
    else:
        print(f"\n✅ All health checks passed!")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())