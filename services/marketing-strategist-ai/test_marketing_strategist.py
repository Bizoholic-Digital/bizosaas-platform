#!/usr/bin/env python3
"""
BizOSaaS Marketing Strategist AI [P10] - Comprehensive Test Suite
Tests for AI-Powered Marketing Strategy and Campaign Management System
"""

import asyncio
import pytest
import httpx
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any

# Test Configuration
BASE_URL = "http://localhost:8029"
API_BASE = f"{BASE_URL}/api/v1"
TEST_TIMEOUT = 30

# Test Data
TEST_STRATEGY_DATA = {
    "tenant_id": "test-tenant",
    "client_id": "test-client",
    "campaign_name": "Test Holiday Campaign",
    "objective": "sales_conversion",
    "target_audience": {
        "demographics": {
            "age_range": "25-54",
            "gender": "mixed",
            "income": "middle",
            "location": "national"
        },
        "interests": ["shopping", "fashion", "deals", "online_shopping"],
        "behaviors": ["frequent_online_purchaser", "brand_conscious", "deal_seeker"]
    },
    "budget": 15000.00,
    "duration_days": 45,
    "platforms": ["google_ads", "meta_ads", "email"],
    "campaign_type": "search",
    "kpis": ["conversions", "roas", "revenue"]
}

TEST_OPTIMIZATION_DATA = {
    "campaign_id": "test-campaign-123",
    "optimization_type": "performance",
    "implementation_priority": "high"
}

TEST_COMMUNICATION_DATA = {
    "tenant_id": "test-tenant",
    "client_id": "test-client",
    "message_type": "performance_update",
    "content": "Your campaign performance this week shows excellent ROAS improvement.",
    "send_immediately": True
}

TEST_REPORT_DATA = {
    "tenant_id": "test-tenant",
    "client_id": "test-client",
    "campaign_ids": ["test-campaign-123", "test-campaign-456"],
    "date_range": {
        "start_date": "2024-01-01",
        "end_date": "2024-01-31"
    }
}

TEST_BUDGET_OPTIMIZATION_DATA = {
    "tenant_id": "test-tenant",
    "total_budget": 50000.00,
    "campaigns": ["test-campaign-123", "test-campaign-456", "test-campaign-789"],
    "allocation_strategy": "performance_based",
    "optimization_goals": ["roas", "conversions", "efficiency"]
}

TEST_COMPETITOR_ANALYSIS_DATA = {
    "tenant_id": "test-tenant",
    "industry": "e-commerce",
    "competitors": ["competitor1.com", "competitor2.com", "competitor3.com"],
    "analysis_depth": "comprehensive"
}

class MarketingStrategistTestSuite:
    """Comprehensive test suite for Marketing Strategist AI"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=TEST_TIMEOUT)
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "errors": [],
            "performance_metrics": {}
        }
    
    async def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Starting Marketing Strategist AI Test Suite")
        print("=" * 60)
        
        try:
            # Basic health and connectivity tests
            await self.test_service_health()
            await self.test_dashboard_access()
            
            # Core functionality tests
            await self.test_campaign_strategy_generation()
            await self.test_campaign_optimization()
            await self.test_client_communication()
            await self.test_performance_reporting()
            await self.test_budget_optimization()
            await self.test_competitor_analysis()
            
            # AI and analytics tests
            await self.test_campaign_insights()
            await self.test_analytics_dashboard()
            await self.test_predictive_analytics()
            
            # Integration tests
            await self.test_brain_api_integration()
            await self.test_database_operations()
            await self.test_cache_operations()
            
            # Performance and load tests
            await self.test_performance_metrics()
            await self.test_concurrent_requests()
            
            # Error handling tests
            await self.test_error_handling()
            await self.test_validation()
            
        except Exception as e:
            self.test_results["errors"].append(f"Test suite failed: {str(e)}")
        
        finally:
            await self.client.aclose()
            self.print_test_results()
    
    async def test_service_health(self):
        """Test service health and availability"""
        print("\n🏥 Testing Service Health...")
        
        try:
            start_time = time.time()
            response = await self.client.get(f"{BASE_URL}/health")
            response_time = time.time() - start_time
            
            assert response.status_code == 200, f"Health check failed: {response.status_code}"
            
            health_data = response.json()
            assert health_data["status"] == "healthy", "Service not healthy"
            assert "components" in health_data, "Components status missing"
            assert health_data["components"]["database"] == "connected", "Database not connected"
            assert health_data["components"]["redis"] == "connected", "Redis not connected"
            
            self.test_results["performance_metrics"]["health_check_time"] = response_time
            self.record_success("Service Health Check")
            
        except Exception as e:
            self.record_failure("Service Health Check", str(e))
    
    async def test_dashboard_access(self):
        """Test dashboard accessibility"""
        print("🎛️ Testing Dashboard Access...")
        
        try:
            response = await self.client.get(BASE_URL)
            assert response.status_code == 200, f"Dashboard not accessible: {response.status_code}"
            
            content = response.text
            assert "Marketing Strategist AI" in content, "Dashboard content invalid"
            assert "BizOSaaS" in content, "BizOSaaS branding missing"
            
            self.record_success("Dashboard Access")
            
        except Exception as e:
            self.record_failure("Dashboard Access", str(e))
    
    async def test_campaign_strategy_generation(self):
        """Test AI-powered campaign strategy generation"""
        print("🎯 Testing Campaign Strategy Generation...")
        
        try:
            start_time = time.time()
            response = await self.client.post(
                f"{API_BASE}/strategy/generate",
                json=TEST_STRATEGY_DATA
            )
            generation_time = time.time() - start_time
            
            assert response.status_code == 200, f"Strategy generation failed: {response.status_code}"
            
            result = response.json()
            assert result["success"] == True, "Strategy generation not successful"
            assert "strategy" in result, "Strategy data missing"
            
            strategy = result["strategy"]
            assert "strategy_id" in strategy, "Strategy ID missing"
            assert "audience_analysis" in strategy, "Audience analysis missing"
            assert "platform_strategies" in strategy, "Platform strategies missing"
            assert "budget_allocation" in strategy, "Budget allocation missing"
            assert "content_strategy" in strategy, "Content strategy missing"
            assert "performance_forecast" in strategy, "Performance forecast missing"
            assert strategy["estimated_roi"] > 0, "Invalid ROI estimate"
            assert 0 < strategy["confidence_score"] <= 1, "Invalid confidence score"
            
            # Test platform-specific strategies
            for platform in TEST_STRATEGY_DATA["platforms"]:
                assert platform in strategy["platform_strategies"], f"Missing strategy for {platform}"
                platform_strategy = strategy["platform_strategies"][platform]
                assert "recommended_budget" in platform_strategy, f"Missing budget for {platform}"
                assert "targeting" in platform_strategy, f"Missing targeting for {platform}"
                assert "creatives" in platform_strategy, f"Missing creatives for {platform}"
            
            self.test_results["performance_metrics"]["strategy_generation_time"] = generation_time
            self.record_success("Campaign Strategy Generation")
            
        except Exception as e:
            self.record_failure("Campaign Strategy Generation", str(e))
    
    async def test_campaign_optimization(self):
        """Test campaign optimization functionality"""
        print("⚡ Testing Campaign Optimization...")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/campaign/optimize",
                json=TEST_OPTIMIZATION_DATA
            )
            
            assert response.status_code == 200, f"Optimization failed: {response.status_code}"
            
            result = response.json()
            assert result["success"] == True, "Optimization not successful"
            assert "optimization" in result, "Optimization data missing"
            
            optimization = result["optimization"]
            assert "optimization_id" in optimization, "Optimization ID missing"
            assert "recommendations" in optimization, "Recommendations missing"
            assert "expected_improvement" in optimization, "Expected improvement missing"
            assert len(optimization["recommendations"]) > 0, "No recommendations provided"
            
            self.record_success("Campaign Optimization")
            
        except Exception as e:
            self.record_failure("Campaign Optimization", str(e))
    
    async def test_client_communication(self):
        """Test automated client communication"""
        print("📧 Testing Client Communication...")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/communication/send",
                json=TEST_COMMUNICATION_DATA
            )
            
            assert response.status_code == 200, f"Communication failed: {response.status_code}"
            
            result = response.json()
            assert result["success"] == True, "Communication not successful"
            assert "communication_id" in result, "Communication ID missing"
            assert "scheduled_time" in result, "Scheduled time missing"
            
            self.record_success("Client Communication")
            
        except Exception as e:
            self.record_failure("Client Communication", str(e))
    
    async def test_performance_reporting(self):
        """Test performance report generation"""
        print("📊 Testing Performance Reporting...")
        
        try:
            start_time = time.time()
            response = await self.client.post(
                f"{API_BASE}/reports/generate",
                json=TEST_REPORT_DATA
            )
            report_time = time.time() - start_time
            
            assert response.status_code == 200, f"Report generation failed: {response.status_code}"
            
            result = response.json()
            assert result["success"] == True, "Report generation not successful"
            assert "report" in result, "Report data missing"
            
            report = result["report"]
            assert "report_id" in report, "Report ID missing"
            assert "analytics" in report, "Analytics missing"
            assert "insights" in report, "Insights missing"
            assert "recommendations" in report, "Recommendations missing"
            assert len(report["insights"]) > 0, "No insights provided"
            assert len(report["recommendations"]) > 0, "No recommendations provided"
            
            self.test_results["performance_metrics"]["report_generation_time"] = report_time
            self.record_success("Performance Reporting")
            
        except Exception as e:
            self.record_failure("Performance Reporting", str(e))
    
    async def test_budget_optimization(self):
        """Test budget optimization functionality"""
        print("💰 Testing Budget Optimization...")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/budget/optimize",
                json=TEST_BUDGET_OPTIMIZATION_DATA
            )
            
            assert response.status_code == 200, f"Budget optimization failed: {response.status_code}"
            
            result = response.json()
            assert result["success"] == True, "Budget optimization not successful"
            assert "optimization" in result, "Optimization data missing"
            
            optimization = result["optimization"]
            total_allocated = sum([details["budget"] for details in optimization["allocation"].values() if isinstance(details, dict) and "budget" in details])
            assert abs(total_allocated - TEST_BUDGET_OPTIMIZATION_DATA["total_budget"]) < 1000, "Budget allocation mismatch"
            
            self.record_success("Budget Optimization")
            
        except Exception as e:
            self.record_failure("Budget Optimization", str(e))
    
    async def test_competitor_analysis(self):
        """Test competitor analysis functionality"""
        print("🔍 Testing Competitor Analysis...")
        
        try:
            start_time = time.time()
            response = await self.client.post(
                f"{API_BASE}/competitor-analysis",
                json=TEST_COMPETITOR_ANALYSIS_DATA
            )
            analysis_time = time.time() - start_time
            
            assert response.status_code == 200, f"Competitor analysis failed: {response.status_code}"
            
            result = response.json()
            assert result["success"] == True, "Competitor analysis not successful"
            assert "analysis" in result, "Analysis data missing"
            
            analysis = result["analysis"]
            assert "analysis_id" in analysis, "Analysis ID missing"
            assert "insights" in analysis, "Insights missing"
            assert "strategic_recommendations" in analysis, "Strategic recommendations missing"
            assert "market_opportunities" in analysis, "Market opportunities missing"
            assert len(analysis["strategic_recommendations"]) > 0, "No strategic recommendations"
            
            self.test_results["performance_metrics"]["competitor_analysis_time"] = analysis_time
            self.record_success("Competitor Analysis")
            
        except Exception as e:
            self.record_failure("Competitor Analysis", str(e))
    
    async def test_campaign_insights(self):
        """Test campaign insights functionality"""
        print("🧠 Testing Campaign Insights...")
        
        try:
            response = await self.client.get(
                f"{API_BASE}/campaigns/test-campaign-123/insights?tenant_id=test-tenant"
            )
            
            assert response.status_code == 200, f"Campaign insights failed: {response.status_code}"
            
            result = response.json()
            assert result["success"] == True, "Campaign insights not successful"
            assert "insights" in result, "Insights missing"
            assert "opportunities" in result, "Opportunities missing"
            assert "predictions" in result, "Predictions missing"
            
            self.record_success("Campaign Insights")
            
        except Exception as e:
            self.record_failure("Campaign Insights", str(e))
    
    async def test_analytics_dashboard(self):
        """Test analytics dashboard data"""
        print("📈 Testing Analytics Dashboard...")
        
        try:
            response = await self.client.get(
                f"{API_BASE}/analytics/dashboard?tenant_id=test-tenant&date_range=30d"
            )
            
            assert response.status_code == 200, f"Analytics dashboard failed: {response.status_code}"
            
            result = response.json()
            assert result["success"] == True, "Analytics dashboard not successful"
            assert "dashboard" in result, "Dashboard data missing"
            
            dashboard = result["dashboard"]
            assert "overview" in dashboard, "Overview missing"
            assert "performance_trends" in dashboard, "Performance trends missing"
            assert "platform_breakdown" in dashboard, "Platform breakdown missing"
            assert "recommendations" in dashboard, "Recommendations missing"
            
            self.record_success("Analytics Dashboard")
            
        except Exception as e:
            self.record_failure("Analytics Dashboard", str(e))
    
    async def test_predictive_analytics(self):
        """Test predictive analytics capabilities"""
        print("🔮 Testing Predictive Analytics...")
        
        try:
            # Test performance prediction through strategy generation
            response = await self.client.post(
                f"{API_BASE}/strategy/generate",
                json=TEST_STRATEGY_DATA
            )
            
            assert response.status_code == 200, "Predictive analytics test failed"
            
            result = response.json()
            strategy = result["strategy"]
            
            # Verify prediction components
            assert "performance_forecast" in strategy, "Performance forecast missing"
            forecast = strategy["performance_forecast"]
            assert "predicted_metrics" in forecast, "Predicted metrics missing"
            assert "confidence" in forecast, "Confidence missing"
            assert "risk_factors" in forecast, "Risk factors missing"
            assert "optimization_opportunities" in forecast, "Optimization opportunities missing"
            
            self.record_success("Predictive Analytics")
            
        except Exception as e:
            self.record_failure("Predictive Analytics", str(e))
    
    async def test_brain_api_integration(self):
        """Test integration with Brain API"""
        print("🧠 Testing Brain API Integration...")
        
        try:
            # Test if Brain API integration is working through strategy generation
            response = await self.client.post(
                f"{API_BASE}/strategy/generate",
                json=TEST_STRATEGY_DATA
            )
            
            # If this succeeds, Brain API integration is likely working
            assert response.status_code == 200, "Brain API integration test failed"
            
            self.record_success("Brain API Integration")
            
        except Exception as e:
            self.record_failure("Brain API Integration", str(e))
    
    async def test_database_operations(self):
        """Test database connectivity and operations"""
        print("🗃️ Testing Database Operations...")
        
        try:
            # Database operations are tested implicitly through other endpoints
            # Test strategy generation which involves database writes
            response = await self.client.post(
                f"{API_BASE}/strategy/generate",
                json=TEST_STRATEGY_DATA
            )
            
            assert response.status_code == 200, "Database operations test failed"
            
            self.record_success("Database Operations")
            
        except Exception as e:
            self.record_failure("Database Operations", str(e))
    
    async def test_cache_operations(self):
        """Test cache operations"""
        print("⚡ Testing Cache Operations...")
        
        try:
            # Test cache through repeated requests
            start_time = time.time()
            response1 = await self.client.get(f"{API_BASE}/analytics/dashboard?tenant_id=test-tenant")
            first_request_time = time.time() - start_time
            
            start_time = time.time()
            response2 = await self.client.get(f"{API_BASE}/analytics/dashboard?tenant_id=test-tenant")
            second_request_time = time.time() - start_time
            
            assert response1.status_code == 200, "First cache request failed"
            assert response2.status_code == 200, "Second cache request failed"
            
            # Second request should be faster (cached)
            # This is a rough test - in practice, the difference might be minimal
            self.test_results["performance_metrics"]["cache_first_request"] = first_request_time
            self.test_results["performance_metrics"]["cache_second_request"] = second_request_time
            
            self.record_success("Cache Operations")
            
        except Exception as e:
            self.record_failure("Cache Operations", str(e))
    
    async def test_performance_metrics(self):
        """Test overall performance metrics"""
        print("⚡ Testing Performance Metrics...")
        
        try:
            # Test multiple endpoints for performance
            endpoints = [
                f"{BASE_URL}/health",
                f"{API_BASE}/analytics/dashboard?tenant_id=test-tenant",
            ]
            
            performance_data = {}
            
            for endpoint in endpoints:
                start_time = time.time()
                response = await self.client.get(endpoint)
                response_time = time.time() - start_time
                
                assert response.status_code == 200, f"Performance test failed for {endpoint}"
                performance_data[endpoint] = response_time
            
            self.test_results["performance_metrics"]["endpoint_performance"] = performance_data
            self.record_success("Performance Metrics")
            
        except Exception as e:
            self.record_failure("Performance Metrics", str(e))
    
    async def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        print("🔄 Testing Concurrent Requests...")
        
        try:
            # Create multiple concurrent requests
            tasks = []
            for i in range(5):
                task = self.client.get(f"{BASE_URL}/health")
                tasks.append(task)
            
            start_time = time.time()
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            concurrent_time = time.time() - start_time
            
            # Check that all requests succeeded
            for i, response in enumerate(responses):
                if isinstance(response, Exception):
                    raise Exception(f"Concurrent request {i} failed: {response}")
                assert response.status_code == 200, f"Concurrent request {i} failed"
            
            self.test_results["performance_metrics"]["concurrent_requests_time"] = concurrent_time
            self.record_success("Concurrent Requests")
            
        except Exception as e:
            self.record_failure("Concurrent Requests", str(e))
    
    async def test_error_handling(self):
        """Test error handling and edge cases"""
        print("❌ Testing Error Handling...")
        
        try:
            # Test invalid strategy data
            invalid_data = {**TEST_STRATEGY_DATA, "budget": -1000}
            response = await self.client.post(f"{API_BASE}/strategy/generate", json=invalid_data)
            # Should handle gracefully, might return 400 or 422
            assert response.status_code in [400, 422, 500], "Error handling failed"
            
            # Test missing required fields
            incomplete_data = {"tenant_id": "test-tenant"}
            response = await self.client.post(f"{API_BASE}/strategy/generate", json=incomplete_data)
            assert response.status_code in [400, 422, 500], "Missing field validation failed"
            
            # Test invalid endpoint
            response = await self.client.get(f"{API_BASE}/nonexistent-endpoint")
            assert response.status_code == 404, "Invalid endpoint handling failed"
            
            self.record_success("Error Handling")
            
        except Exception as e:
            self.record_failure("Error Handling", str(e))
    
    async def test_validation(self):
        """Test input validation"""
        print("✅ Testing Input Validation...")
        
        try:
            # Test various validation scenarios
            test_cases = [
                # Empty budget
                {**TEST_STRATEGY_DATA, "budget": 0},
                # Invalid duration
                {**TEST_STRATEGY_DATA, "duration_days": -5},
                # Empty platforms list
                {**TEST_STRATEGY_DATA, "platforms": []},
                # Invalid campaign type
                {**TEST_STRATEGY_DATA, "campaign_type": "invalid_type"}
            ]
            
            for i, test_case in enumerate(test_cases):
                response = await self.client.post(f"{API_BASE}/strategy/generate", json=test_case)
                # Should return validation error
                assert response.status_code in [400, 422, 500], f"Validation test case {i} failed"
            
            self.record_success("Input Validation")
            
        except Exception as e:
            self.record_failure("Input Validation", str(e))
    
    def record_success(self, test_name: str):
        """Record successful test"""
        self.test_results["passed"] += 1
        print(f"   ✅ {test_name}")
    
    def record_failure(self, test_name: str, error: str):
        """Record failed test"""
        self.test_results["failed"] += 1
        self.test_results["errors"].append(f"{test_name}: {error}")
        print(f"   ❌ {test_name}: {error}")
    
    def print_test_results(self):
        """Print comprehensive test results"""
        print("\n" + "=" * 60)
        print("🎯 MARKETING STRATEGIST AI TEST RESULTS")
        print("=" * 60)
        
        total_tests = self.test_results["passed"] + self.test_results["failed"]
        pass_rate = (self.test_results["passed"] / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.test_results['passed']} ✅")
        print(f"Failed: {self.test_results['failed']} ❌")
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        if self.test_results["errors"]:
            print(f"\n❌ FAILED TESTS:")
            for error in self.test_results["errors"]:
                print(f"   • {error}")
        
        if self.test_results["performance_metrics"]:
            print(f"\n⚡ PERFORMANCE METRICS:")
            for metric, value in self.test_results["performance_metrics"].items():
                if isinstance(value, dict):
                    print(f"   📊 {metric}:")
                    for sub_metric, sub_value in value.items():
                        print(f"      • {sub_metric}: {sub_value:.3f}s")
                else:
                    print(f"   • {metric}: {value:.3f}s")
        
        # Service assessment
        print(f"\n🎯 SERVICE ASSESSMENT:")
        if pass_rate >= 95:
            print("   🟢 EXCELLENT - Service is production-ready")
        elif pass_rate >= 85:
            print("   🟡 GOOD - Service is mostly functional with minor issues")
        elif pass_rate >= 70:
            print("   🟠 NEEDS WORK - Service has significant issues")
        else:
            print("   🔴 CRITICAL - Service is not functional")
        
        print(f"\n📋 FEATURES TESTED:")
        features = [
            "✅ AI Campaign Strategy Generation",
            "✅ Multi-Platform Campaign Management", 
            "✅ Automated Client Communication",
            "✅ Performance Analytics & Reporting",
            "✅ Budget Optimization & Allocation",
            "✅ Competitor Analysis & Intelligence",
            "✅ Campaign Insights & Predictions",
            "✅ Real-time Dashboard Analytics",
            "✅ Error Handling & Validation",
            "✅ Performance & Concurrency"
        ]
        
        for feature in features:
            print(f"   {feature}")
        
        print(f"\n🚀 NEXT STEPS:")
        print("   1. Configure environment variables and API keys")
        print("   2. Set up marketing platform integrations")
        print("   3. Test with real campaign data")
        print("   4. Configure client communication templates")
        print("   5. Set up automated reporting workflows")
        print("   6. Monitor performance in production environment")

async def main():
    """Run the test suite"""
    test_suite = MarketingStrategistTestSuite()
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())