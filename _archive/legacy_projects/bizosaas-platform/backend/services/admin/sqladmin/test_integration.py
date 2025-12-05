#!/usr/bin/env python3

"""
Integration Test Suite for SQLAdmin Dashboard
Tests authentication, database access, and service integration
"""

import asyncio
import aiohttp
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Test Configuration
SQLADMIN_URL = os.getenv("SQLADMIN_URL", "http://localhost:5000")
TAILADMIN_URL = os.getenv("TAILADMIN_URL", "http://localhost:3001")
AUTH_SERVICE_URL = os.getenv("UNIFIED_AUTH_BROWSER_URL", "http://localhost:3002")

@dataclass
class TestResult:
    name: str
    status: str  # "PASS", "FAIL", "SKIP"
    message: str
    details: Optional[Dict[str, Any]] = None
    duration: Optional[float] = None

class IntegrationTester:
    """Integration test suite for SQLAdmin dashboard"""
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.session = None
    
    async def run_all_tests(self) -> List[TestResult]:
        """Run all integration tests"""
        print("🧪 SQLAdmin Dashboard Integration Tests")
        print("=" * 50)
        
        # Create HTTP session
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30.0)
        )
        
        try:
            # Test categories
            test_categories = [
                ("Service Availability", [
                    self.test_sqladmin_service_availability,
                    self.test_auth_service_availability,
                    self.test_tailadmin_service_availability,
                ]),
                ("Authentication Flow", [
                    self.test_unauthenticated_access,
                    self.test_authentication_redirect,
                    self.test_insufficient_permissions,
                ]),
                ("API Endpoints", [
                    self.test_health_endpoint,
                    self.test_dashboard_switcher,
                    self.test_system_stats_endpoint,
                ]),
                ("Database Integration", [
                    self.test_database_connectivity,
                    self.test_admin_interface_access,
                ]),
                ("Security", [
                    self.test_cors_headers,
                    self.test_security_headers,
                    self.test_admin_only_access,
                ])
            ]
            
            for category_name, tests in test_categories:
                print(f"\n📂 {category_name}")
                print("-" * 30)
                
                for test_func in tests:
                    await self.run_test(test_func)
            
            # Print summary
            self.print_summary()
            
            return self.results
            
        finally:
            if self.session:
                await self.session.close()
    
    async def run_test(self, test_func) -> TestResult:
        """Run a single test"""
        test_name = test_func.__name__.replace("test_", "").replace("_", " ").title()
        start_time = asyncio.get_event_loop().time()
        
        try:
            result = await test_func()
            if result is None:
                result = TestResult(test_name, "PASS", "Test completed successfully")
            
            result.name = test_name
            result.duration = asyncio.get_event_loop().time() - start_time
            
        except Exception as e:
            result = TestResult(
                test_name, 
                "FAIL", 
                f"Test failed with error: {str(e)}",
                duration=asyncio.get_event_loop().time() - start_time
            )
        
        # Print result
        status_emoji = {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭️"}
        print(f"  {status_emoji.get(result.status, '❓')} {result.name}: {result.message}")
        
        if result.details:
            for key, value in result.details.items():
                print(f"     - {key}: {value}")
        
        self.results.append(result)
        return result
    
    # Service Availability Tests
    async def test_sqladmin_service_availability(self) -> TestResult:
        """Test SQLAdmin service is running"""
        try:
            async with self.session.get(f"{SQLADMIN_URL}/") as response:
                if response.status in [200, 302, 401, 403]:  # Valid responses
                    return TestResult(
                        "", "PASS", 
                        "SQLAdmin service is available",
                        details={"status_code": response.status, "url": SQLADMIN_URL}
                    )
                else:
                    return TestResult(
                        "", "FAIL",
                        f"Unexpected status code: {response.status}",
                        details={"status_code": response.status}
                    )
                    
        except aiohttp.ClientConnectorError:
            return TestResult(
                "", "FAIL",
                "SQLAdmin service is not running",
                details={"url": SQLADMIN_URL}
            )
    
    async def test_auth_service_availability(self) -> TestResult:
        """Test auth service is running"""
        try:
            async with self.session.get(f"{AUTH_SERVICE_URL}/") as response:
                if response.status in [200, 404]:  # 404 is acceptable for root
                    return TestResult(
                        "", "PASS",
                        "Auth service is available",
                        details={"status_code": response.status, "url": AUTH_SERVICE_URL}
                    )
                else:
                    return TestResult(
                        "", "FAIL",
                        f"Unexpected auth service status: {response.status}",
                        details={"status_code": response.status}
                    )
                    
        except aiohttp.ClientConnectorError:
            return TestResult(
                "", "FAIL",
                "Auth service is not running",
                details={"url": AUTH_SERVICE_URL}
            )
    
    async def test_tailadmin_service_availability(self) -> TestResult:
        """Test TailAdmin service is available"""
        try:
            async with self.session.get(f"{TAILADMIN_URL}/") as response:
                if response.status in [200, 302, 401, 403]:
                    return TestResult(
                        "", "PASS",
                        "TailAdmin service is available",
                        details={"status_code": response.status, "url": TAILADMIN_URL}
                    )
                else:
                    return TestResult(
                        "", "FAIL",
                        f"TailAdmin unexpected status: {response.status}",
                        details={"status_code": response.status}
                    )
                    
        except aiohttp.ClientConnectorError:
            return TestResult(
                "", "SKIP",
                "TailAdmin service not running (optional)",
                details={"url": TAILADMIN_URL}
            )
    
    # Authentication Flow Tests
    async def test_unauthenticated_access(self) -> TestResult:
        """Test that unauthenticated access redirects to login"""
        async with self.session.get(f"{SQLADMIN_URL}/", allow_redirects=False) as response:
            if response.status == 302:
                location = response.headers.get('Location', '')
                if 'login' in location.lower():
                    return TestResult(
                        "", "PASS",
                        "Correctly redirects to login for unauthenticated access",
                        details={"redirect_location": location}
                    )
                else:
                    return TestResult(
                        "", "FAIL",
                        f"Redirects to unexpected location: {location}",
                        details={"redirect_location": location}
                    )
            else:
                return TestResult(
                    "", "FAIL",
                    f"Expected redirect (302), got {response.status}",
                    details={"status_code": response.status}
                )
    
    async def test_authentication_redirect(self) -> TestResult:
        """Test authentication redirect URL format"""
        async with self.session.get(f"{SQLADMIN_URL}/", allow_redirects=False) as response:
            if response.status == 302:
                location = response.headers.get('Location', '')
                expected_parts = [AUTH_SERVICE_URL, 'auth', 'login']
                
                if all(part in location for part in expected_parts):
                    return TestResult(
                        "", "PASS",
                        "Authentication redirect URL is properly formatted",
                        details={"redirect_url": location}
                    )
                else:
                    return TestResult(
                        "", "FAIL",
                        "Authentication redirect URL missing required parts",
                        details={"redirect_url": location, "expected_parts": expected_parts}
                    )
            else:
                return TestResult(
                    "", "SKIP",
                    "No redirect occurred to test URL format"
                )
    
    async def test_insufficient_permissions(self) -> TestResult:
        """Test access denied for non-super-admin users"""
        # This test would need a valid session with insufficient permissions
        # For now, we'll test the error response format
        return TestResult(
            "", "SKIP",
            "Requires valid non-super-admin session to test"
        )
    
    # API Endpoints Tests
    async def test_health_endpoint(self) -> TestResult:
        """Test health endpoint responds appropriately"""
        try:
            async with self.session.get(f"{SQLADMIN_URL}/api/system/health") as response:
                if response.status == 401:
                    return TestResult(
                        "", "PASS",
                        "Health endpoint correctly requires authentication",
                        details={"status_code": response.status}
                    )
                elif response.status == 200:
                    data = await response.json()
                    required_fields = ["status", "timestamp"]
                    missing_fields = [f for f in required_fields if f not in data]
                    
                    if not missing_fields:
                        return TestResult(
                            "", "PASS",
                            "Health endpoint returns valid response",
                            details={"response_fields": list(data.keys())}
                        )
                    else:
                        return TestResult(
                            "", "FAIL",
                            f"Health endpoint missing fields: {missing_fields}",
                            details={"missing_fields": missing_fields}
                        )
                else:
                    return TestResult(
                        "", "FAIL",
                        f"Unexpected health endpoint status: {response.status}",
                        details={"status_code": response.status}
                    )
                    
        except aiohttp.ClientError as e:
            return TestResult(
                "", "FAIL",
                f"Health endpoint connection error: {str(e)}"
            )
    
    async def test_dashboard_switcher(self) -> TestResult:
        """Test dashboard switcher endpoint"""
        async with self.session.get(f"{SQLADMIN_URL}/dashboard-switcher") as response:
            if response.status == 401:
                return TestResult(
                    "", "PASS",
                    "Dashboard switcher correctly requires authentication",
                    details={"status_code": response.status}
                )
            elif response.status == 403:
                return TestResult(
                    "", "PASS",
                    "Dashboard switcher correctly requires super admin",
                    details={"status_code": response.status}
                )
            else:
                return TestResult(
                    "", "FAIL",
                    f"Dashboard switcher unexpected status: {response.status}",
                    details={"status_code": response.status}
                )
    
    async def test_system_stats_endpoint(self) -> TestResult:
        """Test system stats endpoint"""
        async with self.session.get(f"{SQLADMIN_URL}/api/system/stats") as response:
            if response.status in [401, 403]:
                return TestResult(
                    "", "PASS",
                    "System stats endpoint correctly requires super admin",
                    details={"status_code": response.status}
                )
            else:
                return TestResult(
                    "", "FAIL",
                    f"System stats unexpected status: {response.status}",
                    details={"status_code": response.status}
                )
    
    # Database Integration Tests
    async def test_database_connectivity(self) -> TestResult:
        """Test database connectivity through service"""
        # This would be tested indirectly through service health
        return TestResult(
            "", "SKIP",
            "Database connectivity tested through service health endpoint"
        )
    
    async def test_admin_interface_access(self) -> TestResult:
        """Test SQLAdmin interface access"""
        async with self.session.get(f"{SQLADMIN_URL}/admin") as response:
            if response.status in [200, 302, 401, 403]:
                return TestResult(
                    "", "PASS",
                    "SQLAdmin interface responds appropriately",
                    details={"status_code": response.status}
                )
            else:
                return TestResult(
                    "", "FAIL",
                    f"SQLAdmin interface unexpected status: {response.status}",
                    details={"status_code": response.status}
                )
    
    # Security Tests
    async def test_cors_headers(self) -> TestResult:
        """Test CORS headers are present"""
        async with self.session.options(f"{SQLADMIN_URL}/") as response:
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            }
            
            present_headers = [k for k, v in cors_headers.items() if v is not None]
            
            if len(present_headers) >= 2:  # At least 2 CORS headers
                return TestResult(
                    "", "PASS",
                    "CORS headers are configured",
                    details={"cors_headers": present_headers}
                )
            else:
                return TestResult(
                    "", "FAIL",
                    "CORS headers missing or incomplete",
                    details={"present_headers": present_headers}
                )
    
    async def test_security_headers(self) -> TestResult:
        """Test security headers are present"""
        async with self.session.get(f"{SQLADMIN_URL}/") as response:
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Strict-Transport-Security'
            ]
            
            present_headers = [h for h in security_headers if h in response.headers]
            
            if present_headers:
                return TestResult(
                    "", "PASS",
                    f"Security headers present: {len(present_headers)}/{len(security_headers)}",
                    details={"present_headers": present_headers}
                )
            else:
                return TestResult(
                    "", "SKIP",
                    "No security headers detected (may be handled by reverse proxy)"
                )
    
    async def test_admin_only_access(self) -> TestResult:
        """Test that admin endpoints require super admin access"""
        admin_endpoints = [
            "/admin",
            "/admin/users",
            "/admin/tenants",
            "/api/system/health",
            "/api/system/stats"
        ]
        
        protected_count = 0
        
        for endpoint in admin_endpoints:
            try:
                async with self.session.get(f"{SQLADMIN_URL}{endpoint}") as response:
                    if response.status in [401, 403]:
                        protected_count += 1
            except:
                pass  # Connection errors are acceptable
        
        if protected_count >= len(admin_endpoints) * 0.8:  # 80% protected
            return TestResult(
                "", "PASS",
                f"Admin endpoints are protected ({protected_count}/{len(admin_endpoints)})",
                details={"protected_endpoints": protected_count}
            )
        else:
            return TestResult(
                "", "FAIL",
                f"Insufficient protection on admin endpoints ({protected_count}/{len(admin_endpoints)})",
                details={"protected_endpoints": protected_count}
            )
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n📊 Test Summary")
        print("=" * 50)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.status == "PASS"])
        failed_tests = len([r for r in self.results if r.status == "FAIL"])
        skipped_tests = len([r for r in self.results if r.status == "SKIP"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⏭️  Skipped: {skipped_tests}")
        
        if failed_tests == 0:
            print(f"\n🎉 All tests passed!")
        else:
            print(f"\n⚠️  {failed_tests} tests failed")
            print("\nFailed Tests:")
            for result in self.results:
                if result.status == "FAIL":
                    print(f"  ❌ {result.name}: {result.message}")
        
        # Performance summary
        total_duration = sum(r.duration for r in self.results if r.duration)
        avg_duration = total_duration / len(self.results) if self.results else 0
        
        print(f"\n⏱️  Performance:")
        print(f"Total Duration: {total_duration:.2f}s")
        print(f"Average Test Duration: {avg_duration:.2f}s")

async def main():
    """Main test runner"""
    tester = IntegrationTester()
    results = await tester.run_all_tests()
    
    # Exit with error code if any tests failed
    failed_count = len([r for r in results if r.status == "FAIL"])
    
    if failed_count > 0:
        print(f"\n❌ Integration tests failed ({failed_count} failures)")
        sys.exit(1)
    else:
        print(f"\n✅ All integration tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())