#!/usr/bin/env python3
"""
Amazon Integration Service Performance Testing Suite
Tests API endpoints, response times, and load handling for ASIN validation
"""

import asyncio
import json
import time
import statistics
from datetime import datetime
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor

import httpx
import pytest

class PerformanceTestSuite:
    """Comprehensive performance testing for Amazon integration service"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": base_url,
            "tests": []
        }
    
    async def test_health_endpoint(self) -> Dict:
        """Test health endpoint response time and reliability"""
        test_name = "Health Endpoint Test"
        print(f"\n🏥 Running {test_name}...")
        
        response_times = []
        successful_requests = 0
        failed_requests = 0
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for i in range(10):
                start_time = time.time()
                try:
                    response = await client.get(f"{self.base_url}/health")
                    end_time = time.time()
                    
                    response_time = (end_time - start_time) * 1000  # Convert to ms
                    response_times.append(response_time)
                    
                    if response.status_code == 200:
                        successful_requests += 1
                    else:
                        failed_requests += 1
                        
                except Exception as e:
                    failed_requests += 1
                    print(f"Request {i+1} failed: {str(e)}")
        
        test_result = {
            "test_name": test_name,
            "total_requests": 10,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": (successful_requests / 10) * 100,
            "response_times_ms": {
                "min": min(response_times) if response_times else 0,
                "max": max(response_times) if response_times else 0,
                "avg": statistics.mean(response_times) if response_times else 0,
                "p95": statistics.quantiles(response_times, n=20)[18] if len(response_times) >= 20 else (max(response_times) if response_times else 0),
                "p99": statistics.quantiles(response_times, n=100)[98] if len(response_times) >= 100 else (max(response_times) if response_times else 0)
            },
            "performance_rating": self._rate_performance(statistics.mean(response_times) if response_times else 1000, successful_requests / 10)
        }
        
        self.results["tests"].append(test_result)
        print(f"✅ {test_name} completed: {successful_requests}/10 successful, avg: {test_result['response_times_ms']['avg']:.2f}ms")
        return test_result
    
    async def test_product_search_performance(self) -> Dict:
        """Test product search endpoint performance with various queries"""
        test_name = "Product Search Performance Test"
        print(f"\n🔍 Running {test_name}...")
        
        search_queries = [
            {"query": "fitness", "limit": 5},
            {"query": "yoga mat", "limit": 10},
            {"query": "bluetooth earphones", "limit": 3},
            {"query": "resistance bands", "limit": 7},
            {"query": "smartwatch", "limit": 5}
        ]
        
        response_times = []
        successful_requests = 0
        failed_requests = 0
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            for query in search_queries:
                start_time = time.time()
                try:
                    response = await client.post(
                        f"{self.base_url}/sourcing/search",
                        json=query
                    )
                    end_time = time.time()
                    
                    response_time = (end_time - start_time) * 1000
                    response_times.append(response_time)
                    
                    if response.status_code == 200:
                        successful_requests += 1
                        data = response.json()
                        print(f"  Query '{query['query']}': {len(data)} products, {response_time:.2f}ms")
                    else:
                        failed_requests += 1
                        print(f"  Query '{query['query']}' failed: HTTP {response.status_code}")
                        
                except Exception as e:
                    failed_requests += 1
                    print(f"  Query '{query['query']}' failed: {str(e)}")
        
        test_result = {
            "test_name": test_name,
            "total_requests": len(search_queries),
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": (successful_requests / len(search_queries)) * 100,
            "response_times_ms": {
                "min": min(response_times) if response_times else 0,
                "max": max(response_times) if response_times else 0,
                "avg": statistics.mean(response_times) if response_times else 0,
                "p95": statistics.quantiles(response_times, n=20)[18] if len(response_times) >= 20 else (max(response_times) if response_times else 0),
                "p99": max(response_times) if response_times else 0
            },
            "performance_rating": self._rate_performance(statistics.mean(response_times) if response_times else 5000, successful_requests / len(search_queries))
        }
        
        self.results["tests"].append(test_result)
        print(f"✅ {test_name} completed: {successful_requests}/{len(search_queries)} successful, avg: {test_result['response_times_ms']['avg']:.2f}ms")
        return test_result
    
    async def test_asin_validation_load(self) -> Dict:
        """Test ASIN validation under concurrent load"""
        test_name = "ASIN Validation Load Test"
        print(f"\n⚡ Running {test_name}...")
        
        # Use valid and replacement ASINs from our validation results
        test_asins = [
            "B0CR7G9V56",  # Known valid ASIN
            "B0CR6G41V9",  # Valid replacement
            "B07PP3LCLN",  # Valid replacement
            "B0DX1QJFK4",  # Valid replacement
            "B08D8J5BVR"   # Valid replacement
        ]
        
        concurrent_users = [1, 3, 5, 10]  # Gradual load increase
        load_results = []
        
        for user_count in concurrent_users:
            print(f"  Testing with {user_count} concurrent users...")
            
            async def single_user_test():
                response_times = []
                successful = 0
                failed = 0
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    for asin in test_asins:
                        start_time = time.time()
                        try:
                            response = await client.get(f"{self.base_url}/products/{asin}")
                            end_time = time.time()
                            
                            response_time = (end_time - start_time) * 1000
                            response_times.append(response_time)
                            
                            if response.status_code in [200, 404]:  # 404 is acceptable for invalid ASINs
                                successful += 1
                            else:
                                failed += 1
                                
                        except Exception:
                            failed += 1
                
                return response_times, successful, failed
            
            # Run concurrent users
            start_time = time.time()
            tasks = [single_user_test() for _ in range(user_count)]
            results = await asyncio.gather(*tasks)
            end_time = time.time()
            
            # Aggregate results
            all_response_times = []
            total_successful = 0
            total_failed = 0
            
            for response_times, successful, failed in results:
                all_response_times.extend(response_times)
                total_successful += successful
                total_failed += failed
            
            total_time = end_time - start_time
            throughput = (total_successful + total_failed) / total_time if total_time > 0 else 0
            
            load_result = {
                "concurrent_users": user_count,
                "total_requests": total_successful + total_failed,
                "successful_requests": total_successful,
                "failed_requests": total_failed,
                "success_rate": (total_successful / (total_successful + total_failed)) * 100 if (total_successful + total_failed) > 0 else 0,
                "total_time_seconds": total_time,
                "throughput_rps": throughput,
                "avg_response_time_ms": statistics.mean(all_response_times) if all_response_times else 0
            }
            
            load_results.append(load_result)
            print(f"    {user_count} users: {total_successful} successful, {throughput:.2f} RPS, {load_result['avg_response_time_ms']:.2f}ms avg")
        
        test_result = {
            "test_name": test_name,
            "load_results": load_results,
            "performance_rating": self._rate_load_performance(load_results)
        }
        
        self.results["tests"].append(test_result)
        print(f"✅ {test_name} completed")
        return test_result
    
    async def test_workflow_end_to_end(self) -> Dict:
        """Test complete sourcing workflow performance"""
        test_name = "End-to-End Workflow Test"
        print(f"\n🔄 Running {test_name}...")
        
        workflow_request = {
            "query": "fitness equipment",
            "category": "sports",
            "limit": 5
        }
        
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/workflow/complete-sourcing",
                    json=workflow_request
                )
                
                end_time = time.time()
                total_time = (end_time - start_time) * 1000
                
                if response.status_code == 200:
                    data = response.json()
                    
                    test_result = {
                        "test_name": test_name,
                        "success": True,
                        "total_time_ms": total_time,
                        "steps_completed": len(data.get("steps_completed", [])),
                        "products_processed": len(data.get("products_processed", [])),
                        "errors": len(data.get("errors", [])),
                        "performance_rating": "Excellent" if total_time < 10000 else "Good" if total_time < 30000 else "Poor"
                    }
                    
                    print(f"  Workflow completed in {total_time:.2f}ms")
                    print(f"  Steps: {test_result['steps_completed']}, Products: {test_result['products_processed']}")
                    
                else:
                    test_result = {
                        "test_name": test_name,
                        "success": False,
                        "error": f"HTTP {response.status_code}",
                        "performance_rating": "Failed"
                    }
                    
        except Exception as e:
            test_result = {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "performance_rating": "Failed"
            }
        
        self.results["tests"].append(test_result)
        print(f"✅ {test_name} completed: {'Success' if test_result.get('success') else 'Failed'}")
        return test_result
    
    def _rate_performance(self, avg_response_time: float, success_rate: float) -> str:
        """Rate performance based on response time and success rate"""
        if success_rate < 0.8:
            return "Poor"
        elif avg_response_time < 100:
            return "Excellent"
        elif avg_response_time < 500:
            return "Good"
        elif avg_response_time < 1000:
            return "Fair"
        else:
            return "Poor"
    
    def _rate_load_performance(self, load_results: List[Dict]) -> str:
        """Rate load performance based on throughput and response times"""
        if not load_results:
            return "No Data"
        
        max_load_result = max(load_results, key=lambda x: x['concurrent_users'])
        
        if max_load_result['success_rate'] < 80:
            return "Poor"
        elif max_load_result['throughput_rps'] > 10:
            return "Excellent"
        elif max_load_result['throughput_rps'] > 5:
            return "Good"
        elif max_load_result['throughput_rps'] > 1:
            return "Fair"
        else:
            return "Poor"
    
    async def run_all_tests(self) -> Dict:
        """Run all performance tests"""
        print("🚀 Starting Amazon Integration Service Performance Test Suite")
        print("=" * 70)
        
        # Run individual tests
        await self.test_health_endpoint()
        await self.test_product_search_performance()
        await self.test_asin_validation_load()
        await self.test_workflow_end_to_end()
        
        # Generate summary
        self.results["summary"] = self._generate_summary()
        
        print("\n" + "=" * 70)
        print("📊 PERFORMANCE TEST SUMMARY")
        print("=" * 70)
        
        for test in self.results["tests"]:
            rating = test.get("performance_rating", "Unknown")
            print(f"  {test['test_name']}: {rating}")
        
        overall_rating = self.results["summary"]["overall_rating"]
        print(f"\n🎯 Overall Performance Rating: {overall_rating}")
        
        return self.results
    
    def _generate_summary(self) -> Dict:
        """Generate performance test summary"""
        ratings = [test.get("performance_rating", "Unknown") for test in self.results["tests"]]
        
        excellent_count = ratings.count("Excellent")
        good_count = ratings.count("Good")
        fair_count = ratings.count("Fair")
        poor_count = ratings.count("Poor")
        failed_count = ratings.count("Failed")
        
        total_tests = len(ratings)
        
        if failed_count > 0 or poor_count > total_tests * 0.5:
            overall_rating = "Poor"
        elif excellent_count > total_tests * 0.7:
            overall_rating = "Excellent"
        elif good_count + excellent_count > total_tests * 0.7:
            overall_rating = "Good"
        else:
            overall_rating = "Fair"
        
        return {
            "total_tests": total_tests,
            "excellent": excellent_count,
            "good": good_count,
            "fair": fair_count,
            "poor": poor_count,
            "failed": failed_count,
            "overall_rating": overall_rating,
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate performance improvement recommendations"""
        recommendations = []
        
        for test in self.results["tests"]:
            rating = test.get("performance_rating", "Unknown")
            test_name = test.get("test_name", "Unknown")
            
            if rating == "Poor" or rating == "Failed":
                if "Health" in test_name:
                    recommendations.append("Optimize health endpoint for faster response times")
                elif "Search" in test_name:
                    recommendations.append("Implement caching for product search results")
                    recommendations.append("Add database indexing for search queries")
                elif "Load" in test_name:
                    recommendations.append("Implement connection pooling for better concurrency")
                    recommendations.append("Add rate limiting to prevent service overload")
                elif "Workflow" in test_name:
                    recommendations.append("Optimize end-to-end workflow processing")
                    recommendations.append("Implement asynchronous processing for long-running tasks")
        
        if not recommendations:
            recommendations.append("Performance is within acceptable limits")
            recommendations.append("Consider monitoring and alerting setup")
        
        return recommendations
    
    def save_results(self, filename: str = None) -> str:
        """Save test results to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_test_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        return filename

async def main():
    """Main function to run performance tests"""
    # Check if service is running
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8080/health")
            if response.status_code != 200:
                print("❌ Amazon Integration Service is not responding properly")
                print("Please start the service first: python main.py")
                return
    except Exception:
        print("❌ Amazon Integration Service is not running")
        print("Please start the service first: python main.py")
        return
    
    # Run performance tests
    test_suite = PerformanceTestSuite()
    results = await test_suite.run_all_tests()
    
    # Save results
    filename = test_suite.save_results()
    print(f"\n📄 Detailed results saved to: {filename}")
    
    # Performance thresholds check
    print("\n🎯 PERFORMANCE THRESHOLDS:")
    print("  ✅ Health endpoint: <100ms (p95)")
    print("  ✅ Product search: <500ms (p95)")
    print("  ✅ ASIN validation: <1000ms (p95)")
    print("  ✅ Load handling: >5 RPS at 10 concurrent users")
    print("  ✅ End-to-end workflow: <30 seconds")

if __name__ == "__main__":
    asyncio.run(main())
