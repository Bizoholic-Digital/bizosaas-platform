#!/usr/bin/env python3
"""
Comprehensive BizOSaaS Platform API Testing Suite
Tests all API endpoints, integrations, and data flows across the platform.
"""

import asyncio
import aiohttp
import json
import time
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class TestResult:
    endpoint: str
    method: str
    status_code: int
    response_time: float
    success: bool
    error_message: Optional[str] = None
    response_data: Optional[Dict] = None

@dataclass
class ServiceHealth:
    name: str
    port: int
    status: str
    response_time: float
    healthy: bool

class BizOSaaSAPITester:
    def __init__(self):
        self.base_url = "http://localhost"
        self.results: List[TestResult] = []
        self.session: Optional[aiohttp.ClientSession] = None
        self.auth_token: Optional[str] = None
        
        # Service configuration
        self.services = {
            "central_hub": {"port": 8001, "name": "Central Hub API Gateway"},
            "client_portal": {"port": 3000, "name": "Client Portal"},
            "coreldove": {"port": 3002, "name": "CoreLDove Frontend"},
            "saleor_api": {"port": 8000, "name": "Saleor GraphQL API"},
            "sql_admin": {"port": 8005, "name": "SQL Admin Dashboard"},
            "superset": {"port": 8088, "name": "Apache Superset"},
            "ai_agents": {"port": 8010, "name": "AI Agents Service"},
            "auth_service": {"port": 8007, "name": "Authentication Service"},
            "business_directory": {"port": 8004, "name": "Business Directory API"},
            "wagtail_cms": {"port": 8002, "name": "Wagtail CMS"},
            "temporal": {"port": 8009, "name": "Temporal Workflow"},
            "bizoholic": {"port": 3001, "name": "Bizoholic Complete"}
        }
        
        # Test credentials
        self.credentials = {
            "database": {"user": "postgres", "password": "SharedInfra2024!SuperSecure"},
            "amazon_api": {"email": "wahie.reema@outlook.com", "password": "QrDM474ckcbG87"},
            "openrouter_api": "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"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(limit=100)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def test_endpoint(self, endpoint: str, method: str = "GET", 
                          data: Optional[Dict] = None, 
                          headers: Optional[Dict] = None) -> TestResult:
        """Test a single API endpoint"""
        start_time = time.time()
        
        try:
            if headers is None:
                headers = {"Content-Type": "application/json"}
            
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"
            
            async with self.session.request(
                method, endpoint, 
                json=data if method != "GET" else None,
                headers=headers
            ) as response:
                response_time = time.time() - start_time
                
                try:
                    response_data = await response.json()
                except:
                    response_data = {"text": await response.text()[:500]}
                
                return TestResult(
                    endpoint=endpoint,
                    method=method,
                    status_code=response.status,
                    response_time=response_time,
                    success=200 <= response.status < 400,
                    response_data=response_data
                )
        
        except Exception as e:
            response_time = time.time() - start_time
            return TestResult(
                endpoint=endpoint,
                method=method,
                status_code=0,
                response_time=response_time,
                success=False,
                error_message=str(e)
            )

    async def check_service_health(self) -> List[ServiceHealth]:
        """Check health status of all services"""
        health_results = []
        
        for service_key, config in self.services.items():
            port = config["port"]
            name = config["name"]
            
            # Try multiple health endpoints
            health_endpoints = [
                f"{self.base_url}:{port}/health",
                f"{self.base_url}:{port}/api/health",
                f"{self.base_url}:{port}/",
                f"{self.base_url}:{port}/status"
            ]
            
            best_result = None
            for endpoint in health_endpoints:
                result = await self.test_endpoint(endpoint)
                if result.success:
                    best_result = result
                    break
                elif best_result is None or result.status_code > 0:
                    best_result = result
            
            if best_result:
                health_results.append(ServiceHealth(
                    name=name,
                    port=port,
                    status=f"HTTP {best_result.status_code}",
                    response_time=best_result.response_time,
                    healthy=best_result.success
                ))
            else:
                health_results.append(ServiceHealth(
                    name=name,
                    port=port,
                    status="Unreachable",
                    response_time=0.0,
                    healthy=False
                ))
        
        return health_results

    async def test_central_hub_api(self):
        """Test Central Hub API Gateway (/api/brain/* endpoints)"""
        print("\n=== Testing Central Hub API Gateway ===")
        
        base_url = f"{self.base_url}:8001"
        brain_endpoints = [
            "/api/brain/health",
            "/api/brain/status",
            "/api/brain/saleor/products",
            "/api/brain/saleor/categories",
            "/api/brain/auth/me",
            "/api/brain/analytics/dashboard",
            "/api/brain/ai/agents/status",
            "/api/brain/integrations/status"
        ]
        
        for endpoint in brain_endpoints:
            result = await self.test_endpoint(f"{base_url}{endpoint}")
            self.results.append(result)
            print(f"  {endpoint}: {result.status_code} ({result.response_time:.3f}s)")

    async def test_saleor_graphql_api(self):
        """Test Saleor GraphQL API functionality"""
        print("\n=== Testing Saleor GraphQL API ===")
        
        base_url = f"{self.base_url}:8000"
        
        # Test GraphQL introspection
        introspection_query = {
            "query": """
            {
                __schema {
                    types {
                        name
                    }
                }
            }
            """
        }
        
        result = await self.test_endpoint(
            f"{base_url}/graphql/",
            method="POST",
            data=introspection_query
        )
        self.results.append(result)
        print(f"  GraphQL Introspection: {result.status_code} ({result.response_time:.3f}s)")
        
        # Test products query
        products_query = {
            "query": """
            {
                products(first: 5) {
                    edges {
                        node {
                            id
                            name
                            slug
                        }
                    }
                }
            }
            """
        }
        
        result = await self.test_endpoint(
            f"{base_url}/graphql/",
            method="POST", 
            data=products_query
        )
        self.results.append(result)
        print(f"  Products Query: {result.status_code} ({result.response_time:.3f}s)")

    async def test_coreldove_api(self):
        """Test CoreLDove product sourcing API"""
        print("\n=== Testing CoreLDove API ===")
        
        base_url = f"{self.base_url}:3002"
        endpoints = [
            "/api/products/search",
            "/api/amazon/products",
            "/api/sourcing/status",
            "/api/health"
        ]
        
        for endpoint in endpoints:
            result = await self.test_endpoint(f"{base_url}{endpoint}")
            self.results.append(result)
            print(f"  {endpoint}: {result.status_code} ({result.response_time:.3f}s)")

    async def test_authentication_api(self):
        """Test authentication API endpoints and JWT handling"""
        print("\n=== Testing Authentication API ===")
        
        base_url = f"{self.base_url}:8007"
        
        # Test login endpoint
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        result = await self.test_endpoint(
            f"{base_url}/auth/login",
            method="POST",
            data=login_data
        )
        self.results.append(result)
        print(f"  Login: {result.status_code} ({result.response_time:.3f}s)")
        
        # Test registration endpoint
        register_data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "first_name": "Test",
            "last_name": "User"
        }
        
        result = await self.test_endpoint(
            f"{base_url}/auth/register",
            method="POST",
            data=register_data
        )
        self.results.append(result)
        print(f"  Register: {result.status_code} ({result.response_time:.3f}s)")

    async def test_ai_agents_api(self):
        """Test AI agent service APIs"""
        print("\n=== Testing AI Agents API ===")
        
        base_url = f"{self.base_url}:8010"
        endpoints = [
            "/health",
            "/agents/status",
            "/agents/digital-presence-audit",
            "/agents/campaign-strategy",
            "/agents/optimize-campaign"
        ]
        
        for endpoint in endpoints:
            if endpoint in ["/agents/digital-presence-audit", "/agents/campaign-strategy"]:
                # POST endpoints with sample data
                test_data = {
                    "company_name": "Test Company",
                    "website": "https://example.com",
                    "industry": "Technology"
                }
                result = await self.test_endpoint(f"{base_url}{endpoint}", method="POST", data=test_data)
            else:
                result = await self.test_endpoint(f"{base_url}{endpoint}")
            
            self.results.append(result)
            print(f"  {endpoint}: {result.status_code} ({result.response_time:.3f}s)")

    async def test_database_connectivity(self):
        """Test database connectivity and queries"""
        print("\n=== Testing Database Connectivity ===")
        
        try:
            import asyncpg
            
            conn = await asyncpg.connect(
                host="localhost",
                port=5432,
                user="postgres",
                password="SharedInfra2024!SuperSecure",
                database="postgres"
            )
            
            # Test basic query
            version = await conn.fetchval("SELECT version()")
            print(f"  PostgreSQL Connection: SUCCESS")
            print(f"  Version: {version[:50]}...")
            
            # Test table existence
            tables = await conn.fetch("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                LIMIT 10
            """)
            print(f"  Tables found: {len(tables)}")
            
            await conn.close()
            
        except Exception as e:
            print(f"  Database Connection: FAILED - {e}")

    async def test_analytics_endpoints(self):
        """Test analytics API endpoints"""
        print("\n=== Testing Analytics Endpoints ===")
        
        # Test SQL Admin
        result = await self.test_endpoint(f"{self.base_url}:8005/api/health")
        self.results.append(result)
        print(f"  SQL Admin Health: {result.status_code} ({result.response_time:.3f}s)")
        
        # Test Superset (if accessible)
        result = await self.test_endpoint(f"{self.base_url}:8088/health")
        self.results.append(result)
        print(f"  Superset Health: {result.status_code} ({result.response_time:.3f}s)")

    async def performance_test(self, endpoint: str, concurrent_requests: int = 10):
        """Run basic performance test on an endpoint"""
        print(f"\n=== Performance Testing: {endpoint} ===")
        
        tasks = []
        for i in range(concurrent_requests):
            task = self.test_endpoint(endpoint)
            tasks.append(task)
        
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        total_time = time.time() - start_time
        
        successful_requests = sum(1 for r in results if isinstance(r, TestResult) and r.success)
        avg_response_time = sum(r.response_time for r in results if isinstance(r, TestResult)) / len(results)
        
        print(f"  Concurrent Requests: {concurrent_requests}")
        print(f"  Successful: {successful_requests}")
        print(f"  Total Time: {total_time:.3f}s")
        print(f"  Avg Response Time: {avg_response_time:.3f}s")
        print(f"  Requests/Second: {concurrent_requests/total_time:.2f}")

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - successful_tests
        
        avg_response_time = sum(r.response_time for r in self.results) / total_tests if total_tests > 0 else 0
        
        # Group results by status code
        status_codes = {}
        for result in self.results:
            code = result.status_code
            status_codes[code] = status_codes.get(code, 0) + 1
        
        # Identify critical failures
        critical_failures = [r for r in self.results if r.status_code >= 500 or r.status_code == 0]
        
        return {
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
                "avg_response_time": avg_response_time
            },
            "status_code_distribution": status_codes,
            "critical_failures": len(critical_failures),
            "test_timestamp": datetime.now().isoformat(),
            "detailed_results": [asdict(r) for r in self.results]
        }

    async def run_comprehensive_tests(self):
        """Run all API tests"""
        print("🚀 Starting Comprehensive BizOSaaS API Testing Suite")
        print("=" * 60)
        
        # Check service health first
        print("\n📊 Checking Service Health Status...")
        health_results = await self.check_service_health()
        
        healthy_services = sum(1 for h in health_results if h.healthy)
        total_services = len(health_results)
        
        print(f"\nServices Status: {healthy_services}/{total_services} healthy")
        for health in health_results:
            status_icon = "✅" if health.healthy else "❌"
            print(f"  {status_icon} {health.name} (:{health.port}) - {health.status} ({health.response_time:.3f}s)")
        
        # Run comprehensive API tests
        test_functions = [
            self.test_central_hub_api,
            self.test_saleor_graphql_api,
            self.test_coreldove_api,
            self.test_authentication_api,
            self.test_ai_agents_api,
            self.test_analytics_endpoints,
            self.test_database_connectivity
        ]
        
        for test_func in test_functions:
            try:
                await test_func()
            except Exception as e:
                print(f"❌ Test failed: {test_func.__name__} - {e}")
        
        # Performance test on healthy endpoints
        healthy_endpoints = [
            f"{self.base_url}:3000/",  # Client Portal
            f"{self.base_url}:8000/",  # Saleor API
            f"{self.base_url}:8004/health"  # Business Directory
        ]
        
        for endpoint in healthy_endpoints:
            try:
                await self.performance_test(endpoint, concurrent_requests=5)
            except Exception as e:
                print(f"❌ Performance test failed for {endpoint}: {e}")
        
        # Generate and save report
        report = self.generate_report()
        
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {report['summary']['total_tests']}")
        print(f"Successful: {report['summary']['successful_tests']}")
        print(f"Failed: {report['summary']['failed_tests']}")
        print(f"Success Rate: {report['summary']['success_rate']:.1f}%")
        print(f"Avg Response Time: {report['summary']['avg_response_time']:.3f}s")
        print(f"Critical Failures: {report['critical_failures']}")
        
        return report

async def main():
    """Main execution function"""
    async with BizOSaaSAPITester() as tester:
        report = await tester.run_comprehensive_tests()
        
        # Save detailed report
        with open('/home/alagiri/projects/bizoholic/bizosaas-platform/api_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📁 Detailed report saved to: api_test_report.json")
        
        # Return exit code based on success rate
        success_rate = report['summary']['success_rate']
        if success_rate >= 80:
            print("✅ API Testing: PASSED")
            return 0
        elif success_rate >= 60:
            print("⚠️ API Testing: PARTIAL SUCCESS")
            return 1
        else:
            print("❌ API Testing: FAILED")
            return 2

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Testing failed with error: {e}")
        sys.exit(2)