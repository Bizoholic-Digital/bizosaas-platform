#!/usr/bin/env python3
"""
Targeted BizOSaaS Platform API Testing - Focus on Working Services
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Any
from datetime import datetime

class TargetedAPITester:
    def __init__(self):
        self.base_url = "http://localhost"
        self.results = []
        self.session = None
        
        # Working services based on initial tests
        self.working_services = {
            "saleor_api": {"port": 8000, "graphql": True},
            "business_directory": {"port": 8004, "rest": True},
            "sql_admin": {"port": 8005, "web": True},
            "coreldove": {"port": 3002, "frontend": True}
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def test_saleor_comprehensive(self):
        """Comprehensive Saleor GraphQL API testing"""
        print("\n🔍 SALEOR GRAPHQL API COMPREHENSIVE TESTING")
        print("=" * 60)
        
        base_url = f"{self.base_url}:8000"
        
        # Test 1: Schema Introspection
        print("\n1. Schema Introspection Test")
        introspection_query = {
            "query": "{ __schema { queryType { name } mutationType { name } } }"
        }
        
        async with self.session.post(
            f"{base_url}/graphql/",
            json=introspection_query,
            headers={"Content-Type": "application/json"}
        ) as response:
            data = await response.json()
            print(f"   Status: {response.status}")
            print(f"   Query Type: {data.get('data', {}).get('__schema', {}).get('queryType', {}).get('name', 'N/A')}")
            print(f"   Mutation Type: {data.get('data', {}).get('__schema', {}).get('mutationType', {}).get('name', 'N/A')}")
        
        # Test 2: Products Query with Pagination
        print("\n2. Products Query with Pagination")
        products_query = {
            "query": """
            query GetProducts($first: Int!, $after: String) {
                products(first: $first, after: $after) {
                    edges {
                        node {
                            id
                            name
                            slug
                            description
                            category {
                                name
                            }
                            productType {
                                name
                            }
                            variants {
                                id
                                name
                                sku
                                pricing {
                                    price {
                                        gross {
                                            amount
                                            currency
                                        }
                                    }
                                }
                            }
                        }
                        cursor
                    }
                    pageInfo {
                        hasNextPage
                        hasPreviousPage
                        startCursor
                        endCursor
                    }
                    totalCount
                }
            }
            """,
            "variables": {"first": 5}
        }
        
        async with self.session.post(
            f"{base_url}/graphql/",
            json=products_query,
            headers={"Content-Type": "application/json"}
        ) as response:
            data = await response.json()
            products = data.get('data', {}).get('products', {})
            edges = products.get('edges', [])
            total_count = products.get('totalCount', 0)
            
            print(f"   Status: {response.status}")
            print(f"   Total Products: {total_count}")
            print(f"   Products Retrieved: {len(edges)}")
            
            if edges:
                product = edges[0]['node']
                print(f"   Sample Product: {product.get('name', 'N/A')}")
                print(f"   Sample SKU: {product.get('variants', [{}])[0].get('sku', 'N/A') if product.get('variants') else 'N/A'}")
        
        # Test 3: Categories Query
        print("\n3. Categories Query")
        categories_query = {
            "query": """
            {
                categories(first: 10) {
                    edges {
                        node {
                            id
                            name
                            slug
                            description
                            parent {
                                name
                            }
                            children(first: 5) {
                                edges {
                                    node {
                                        name
                                    }
                                }
                            }
                        }
                    }
                    totalCount
                }
            }
            """
        }
        
        async with self.session.post(
            f"{base_url}/graphql/",
            json=categories_query,
            headers={"Content-Type": "application/json"}
        ) as response:
            data = await response.json()
            categories = data.get('data', {}).get('categories', {})
            edges = categories.get('edges', [])
            total_count = categories.get('totalCount', 0)
            
            print(f"   Status: {response.status}")
            print(f"   Total Categories: {total_count}")
            print(f"   Categories Retrieved: {len(edges)}")
            
            if edges:
                category = edges[0]['node']
                print(f"   Sample Category: {category.get('name', 'N/A')}")
        
        # Test 4: Collections Query
        print("\n4. Collections Query")
        collections_query = {
            "query": """
            {
                collections(first: 5) {
                    edges {
                        node {
                            id
                            name
                            slug
                            description
                            products(first: 3) {
                                totalCount
                                edges {
                                    node {
                                        name
                                    }
                                }
                            }
                        }
                    }
                    totalCount
                }
            }
            """
        }
        
        async with self.session.post(
            f"{base_url}/graphql/",
            json=collections_query,
            headers={"Content-Type": "application/json"}
        ) as response:
            data = await response.json()
            collections = data.get('data', {}).get('collections', {})
            edges = collections.get('edges', [])
            total_count = collections.get('totalCount', 0)
            
            print(f"   Status: {response.status}")
            print(f"   Total Collections: {total_count}")
            print(f"   Collections Retrieved: {len(edges)}")
        
        # Test 5: Shop Information
        print("\n5. Shop Information Query")
        shop_query = {
            "query": """
            {
                shop {
                    name
                    description
                    domain {
                        host
                        url
                    }
                    countries {
                        code
                        country
                    }
                    defaultCurrency
                    defaultCountry {
                        code
                        country
                    }
                    permissions {
                        code
                        name
                    }
                }
            }
            """
        }
        
        async with self.session.post(
            f"{base_url}/graphql/",
            json=shop_query,
            headers={"Content-Type": "application/json"}
        ) as response:
            data = await response.json()
            shop = data.get('data', {}).get('shop', {})
            
            print(f"   Status: {response.status}")
            print(f"   Shop Name: {shop.get('name', 'N/A')}")
            print(f"   Default Currency: {shop.get('defaultCurrency', 'N/A')}")
            print(f"   Countries Available: {len(shop.get('countries', []))}")
            print(f"   Permissions: {len(shop.get('permissions', []))}")

    async def test_business_directory_api(self):
        """Test Business Directory API endpoints"""
        print("\n🏢 BUSINESS DIRECTORY API TESTING")
        print("=" * 60)
        
        base_url = f"{self.base_url}:8004"
        
        # Test health endpoint
        print("\n1. Health Check")
        async with self.session.get(f"{base_url}/health") as response:
            data = await response.json()
            print(f"   Status: {response.status}")
            print(f"   Response: {data}")
        
        # Test root endpoint
        print("\n2. Root Endpoint")
        async with self.session.get(f"{base_url}/") as response:
            try:
                data = await response.json()
                print(f"   Status: {response.status}")
                print(f"   Response: {data}")
            except:
                text = await response.text()
                print(f"   Status: {response.status}")
                print(f"   Response: {text[:200]}...")
        
        # Test docs endpoint (common for FastAPI)
        print("\n3. API Documentation")
        async with self.session.get(f"{base_url}/docs") as response:
            print(f"   Docs Status: {response.status}")
        
        async with self.session.get(f"{base_url}/openapi.json") as response:
            if response.status == 200:
                openapi_spec = await response.json()
                paths = openapi_spec.get('paths', {})
                print(f"   OpenAPI Status: {response.status}")
                print(f"   Available Endpoints: {len(paths)}")
                for path in list(paths.keys())[:5]:
                    print(f"     - {path}")
            else:
                print(f"   OpenAPI Status: {response.status}")

    async def test_coreldove_frontend(self):
        """Test CoreLDove frontend and API endpoints"""
        print("\n🛒 CORELDOVE FRONTEND TESTING")
        print("=" * 60)
        
        base_url = f"{self.base_url}:3002"
        
        # Test main page
        print("\n1. Main Page")
        async with self.session.get(f"{base_url}/") as response:
            print(f"   Status: {response.status}")
            content_type = response.headers.get('content-type', '')
            print(f"   Content-Type: {content_type}")
        
        # Test API endpoints
        api_endpoints = [
            "/api/health",
            "/api/products",
            "/api/categories",
            "/api/search",
            "/api/status"
        ]
        
        print("\n2. API Endpoints")
        for endpoint in api_endpoints:
            try:
                async with self.session.get(f"{base_url}{endpoint}") as response:
                    print(f"   {endpoint}: {response.status}")
                    if response.status == 200:
                        try:
                            data = await response.json()
                            if isinstance(data, dict) and len(data) > 0:
                                print(f"     Data keys: {list(data.keys())[:3]}")
                        except:
                            pass
            except Exception as e:
                print(f"   {endpoint}: Error - {str(e)[:50]}")

    async def test_sql_admin_dashboard(self):
        """Test SQL Admin Dashboard"""
        print("\n💾 SQL ADMIN DASHBOARD TESTING")
        print("=" * 60)
        
        base_url = f"{self.base_url}:8005"
        
        # Test main page
        print("\n1. Dashboard Access")
        async with self.session.get(f"{base_url}/") as response:
            print(f"   Status: {response.status}")
            if response.status == 302:
                location = response.headers.get('location', '')
                print(f"   Redirect to: {location}")
        
        # Test login page
        print("\n2. Login Page")
        async with self.session.get(f"{base_url}/login") as response:
            print(f"   Login Status: {response.status}")
        
        # Test API endpoints
        api_endpoints = [
            "/api/status",
            "/api/health",
            "/api/databases",
            "/api/tables"
        ]
        
        print("\n3. API Endpoints")
        for endpoint in api_endpoints:
            try:
                async with self.session.get(f"{base_url}{endpoint}") as response:
                    print(f"   {endpoint}: {response.status}")
            except Exception as e:
                print(f"   {endpoint}: Error - {str(e)[:50]}")

    async def performance_stress_test(self):
        """Perform load testing on working endpoints"""
        print("\n⚡ PERFORMANCE STRESS TESTING")
        print("=" * 60)
        
        test_endpoints = [
            ("Saleor GraphQL", "http://localhost:8000/graphql/", "POST"),
            ("Business Directory", "http://localhost:8004/health", "GET"),
            ("CoreLDove", "http://localhost:3002/", "GET")
        ]
        
        for name, url, method in test_endpoints:
            print(f"\n{name} Load Test (50 concurrent requests)")
            
            if method == "POST" and "graphql" in url:
                # Simple GraphQL query for load testing
                payload = {
                    "query": "{ shop { name defaultCurrency } }"
                }
                
                async def make_request():
                    start_time = time.time()
                    try:
                        async with self.session.post(url, json=payload) as response:
                            await response.read()
                            return time.time() - start_time, response.status
                    except Exception as e:
                        return time.time() - start_time, 0
            else:
                async def make_request():
                    start_time = time.time()
                    try:
                        async with self.session.get(url) as response:
                            await response.read()
                            return time.time() - start_time, response.status
                    except Exception as e:
                        return time.time() - start_time, 0
            
            # Execute concurrent requests
            tasks = [make_request() for _ in range(50)]
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            total_time = time.time() - start_time
            
            # Calculate metrics
            response_times = []
            status_codes = {}
            successful_requests = 0
            
            for result in results:
                if isinstance(result, tuple):
                    response_time, status_code = result
                    response_times.append(response_time)
                    status_codes[status_code] = status_codes.get(status_code, 0) + 1
                    if 200 <= status_code < 400:
                        successful_requests += 1
            
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                min_response_time = min(response_times)
                max_response_time = max(response_times)
                
                # Calculate percentiles
                sorted_times = sorted(response_times)
                p95_index = int(0.95 * len(sorted_times))
                p95_response_time = sorted_times[p95_index] if p95_index < len(sorted_times) else sorted_times[-1]
                
                print(f"   Total Requests: 50")
                print(f"   Successful: {successful_requests}")
                print(f"   Success Rate: {(successful_requests/50)*100:.1f}%")
                print(f"   Total Time: {total_time:.3f}s")
                print(f"   Requests/Second: {50/total_time:.2f}")
                print(f"   Avg Response Time: {avg_response_time*1000:.1f}ms")
                print(f"   Min Response Time: {min_response_time*1000:.1f}ms")
                print(f"   Max Response Time: {max_response_time*1000:.1f}ms")
                print(f"   95th Percentile: {p95_response_time*1000:.1f}ms")
                print(f"   Status Codes: {status_codes}")

    async def data_integrity_tests(self):
        """Test data consistency and integrity"""
        print("\n🔍 DATA INTEGRITY TESTING")
        print("=" * 60)
        
        # Test Saleor data relationships
        print("\n1. Saleor Data Relationships")
        
        # Get product with variants and check consistency
        product_variants_query = {
            "query": """
            {
                products(first: 1) {
                    edges {
                        node {
                            id
                            name
                            variants {
                                id
                                name
                                product {
                                    id
                                    name
                                }
                            }
                        }
                    }
                }
            }
            """
        }
        
        async with self.session.post(
            f"http://localhost:8000/graphql/",
            json=product_variants_query,
            headers={"Content-Type": "application/json"}
        ) as response:
            data = await response.json()
            products = data.get('data', {}).get('products', {}).get('edges', [])
            
            if products:
                product = products[0]['node']
                product_id = product['id']
                product_name = product['name']
                variants = product.get('variants', [])
                
                print(f"   Product ID: {product_id}")
                print(f"   Product Name: {product_name}")
                print(f"   Variants Count: {len(variants)}")
                
                # Check if variant references match product
                for variant in variants:
                    variant_product_id = variant.get('product', {}).get('id')
                    if variant_product_id == product_id:
                        print(f"   ✅ Variant-Product relationship intact")
                    else:
                        print(f"   ❌ Variant-Product relationship broken")
                    break
            else:
                print("   No products found for relationship testing")

    async def security_basic_tests(self):
        """Basic security testing"""
        print("\n🔒 BASIC SECURITY TESTING")
        print("=" * 60)
        
        # Test for common security headers
        test_urls = [
            "http://localhost:8000/",
            "http://localhost:8004/",
            "http://localhost:3002/",
            "http://localhost:8005/"
        ]
        
        for url in test_urls:
            print(f"\nSecurity Headers for {url}")
            try:
                async with self.session.get(url) as response:
                    headers = response.headers
                    
                    security_headers = {
                        'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
                        'X-Frame-Options': headers.get('X-Frame-Options'),
                        'X-XSS-Protection': headers.get('X-XSS-Protection'),
                        'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
                        'Content-Security-Policy': headers.get('Content-Security-Policy'),
                        'Access-Control-Allow-Origin': headers.get('Access-Control-Allow-Origin')
                    }
                    
                    for header, value in security_headers.items():
                        if value:
                            print(f"   ✅ {header}: {value}")
                        else:
                            print(f"   ❌ {header}: Missing")
                            
            except Exception as e:
                print(f"   Error testing {url}: {e}")

    async def run_targeted_tests(self):
        """Run all targeted tests"""
        print("🚀 TARGETED BIZOSAAS API TESTING SUITE")
        print("Focus: Working Services Comprehensive Analysis")
        print("=" * 80)
        
        test_functions = [
            self.test_saleor_comprehensive,
            self.test_business_directory_api,
            self.test_coreldove_frontend,
            self.test_sql_admin_dashboard,
            self.performance_stress_test,
            self.data_integrity_tests,
            self.security_basic_tests
        ]
        
        start_time = time.time()
        
        for test_func in test_functions:
            try:
                await test_func()
            except Exception as e:
                print(f"❌ Test failed: {test_func.__name__} - {e}")
        
        total_time = time.time() - start_time
        
        print("\n" + "=" * 80)
        print("✅ TARGETED TESTING COMPLETE")
        print(f"Total Testing Time: {total_time:.2f} seconds")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 80)

async def main():
    async with TargetedAPITester() as tester:
        await tester.run_targeted_tests()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
    except Exception as e:
        print(f"\n💥 Testing failed with error: {e}")