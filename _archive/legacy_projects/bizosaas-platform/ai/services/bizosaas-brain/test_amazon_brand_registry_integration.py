#!/usr/bin/env python3
"""
Comprehensive Test Suite for Amazon Brand Registry APIs Integration
BizOSaaS Brain AI Gateway - Brand Protection and Management Testing

This test suite validates all Amazon Brand Registry AI agents and their integration
with the Brain API Gateway. Tests cover brand protection, analytics, content optimization,
and compliance monitoring across multiple scenarios and edge cases.

Test Coverage:
- Brand protection and trademark monitoring
- Counterfeit detection and analysis
- Brand analytics and performance tracking
- Competitive intelligence gathering
- Content optimization (A+ content, brand store)
- Brand compliance and IP protection
- Multi-marketplace operations
- Error handling and edge cases
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Test configuration
BASE_URL = "http://localhost:8001"
TEST_TIMEOUT = 30

class TestAmazonBrandRegistryIntegration:
    """Test class for Amazon Brand Registry API integration with BizOSaaS Brain"""

    def sample_brand_protection_request(self):
        """Sample brand protection monitoring request"""
        return {
            "tenant_id": "test_brand_protection",
            "keywords": [
                "TestBrand Premium",
                "TestBrand Original", 
                "TestBrand Professional",
                "TestBrand Elite"
            ],
            "marketplaces": ["US", "UK", "DE", "FR"],
            "protection_level": "enhanced",
            "monitoring_frequency": "hourly",
            "trademark_numbers": ["TM123456", "TM789012"]
        }

    def sample_counterfeit_detection_request(self):
        """Sample counterfeit detection request"""
        return {
            "tenant_id": "test_counterfeit_detection",
            "suspected_products": [
                {
                    "asin": "B078ABCD12",
                    "title": "Premium TestBrand Product - Suspected Counterfeit",
                    "marketplace": "US",
                    "price": 19.99,
                    "authentic_price": 49.99,
                    "seller_id": "SUSPICIOUS001"
                },
                {
                    "asin": "B089EFGH34",
                    "title": "TestBrand Professional Kit - Quality Concerns",
                    "marketplace": "UK", 
                    "price": 15.50,
                    "authentic_price": 39.99,
                    "seller_id": "COUNTERFEIT002"
                },
                {
                    "asin": "B091IJKL56",
                    "title": "Original TestBrand Series - Image Issues",
                    "marketplace": "DE",
                    "price": 25.00,
                    "authentic_price": 59.99,
                    "seller_id": "FAKE003"
                }
            ]
        }

    def sample_brand_analytics_request(self):
        """Sample brand analytics request"""
        return {
            "tenant_id": "test_brand_analytics", 
            "marketplaces": ["US", "UK", "DE", "FR", "IT"],
            "analysis_period": "30_days",
            "metrics": [
                "sales_performance",
                "market_share", 
                "brand_awareness",
                "competitive_position"
            ]
        }

    def sample_competitive_intelligence_request(self):
        """Sample competitive intelligence request"""
        return {
            "tenant_id": "test_competitive_intelligence",
            "competitors": [
                {
                    "competitor_id": "COMP001",
                    "name": "CompetitorBrand Alpha",
                    "markets": ["US", "UK", "DE"]
                },
                {
                    "competitor_id": "COMP002", 
                    "name": "CompetitorBrand Beta",
                    "markets": ["US", "FR", "IT"]
                },
                {
                    "competitor_id": "COMP003",
                    "name": "CompetitorBrand Gamma", 
                    "markets": ["UK", "DE", "ES"]
                }
            ],
            "analysis_depth": "comprehensive"
        }

    def sample_content_optimization_request(self):
        """Sample brand content optimization request"""
        return {
            "tenant_id": "test_content_optimization",
            "content_assets": [
                {
                    "asset_id": "aplus_001",
                    "type": "a_plus_content",
                    "current_performance": {
                        "click_through_rate": 2.8,
                        "conversion_rate": 3.5
                    }
                },
                {
                    "asset_id": "store_001",
                    "type": "brand_store",
                    "current_performance": {
                        "click_through_rate": 4.2,
                        "conversion_rate": 5.1
                    }
                },
                {
                    "asset_id": "ebc_001", 
                    "type": "enhanced_brand_content",
                    "current_performance": {
                        "click_through_rate": 3.1,
                        "conversion_rate": 4.3
                    }
                }
            ],
            "optimization_goals": ["conversion", "engagement", "mobile_performance"]
        }

    def sample_brand_store_request(self):
        """Sample brand store management request"""
        return {
            "tenant_id": "test_brand_store",
            "store_sections": [
                {
                    "section_id": "hero_001",
                    "type": "hero",
                    "current_metrics": {
                        "page_views": 1250,
                        "click_through_rate": 4.2
                    }
                },
                {
                    "section_id": "featured_001",
                    "type": "featured",
                    "current_metrics": {
                        "page_views": 890,
                        "click_through_rate": 3.8
                    }
                },
                {
                    "section_id": "categories_001",
                    "type": "categories", 
                    "current_metrics": {
                        "page_views": 670,
                        "click_through_rate": 2.9
                    }
                }
            ]
        }

    def sample_compliance_monitoring_request(self):
        """Sample compliance monitoring request"""
        return {
            "tenant_id": "test_compliance_monitoring",
            "monitored_areas": ["trademark", "content", "sellers", "policies"],
            "compliance_level": "enterprise",
            "audit_frequency": "weekly"
        }

    def sample_ip_protection_request(self):
        """Sample IP protection request"""
        return {
            "tenant_id": "test_ip_protection",
            "protection_scope": ["trademarks", "copyrights", "patents"],
            "jurisdictions": ["US", "EU", "UK", "CA"],
            "monitoring_intensity": "high"
        }

    async def test_brand_protection_endpoint(self, sample_brand_protection_request):
        """Test AI brand protection monitoring endpoint"""
        print("\n🧪 Testing AI Brand Protection Endpoint...")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{BASE_URL}/api/brain/integrations/amazon-brand-registry/ai-brand-protection",
                    json=sample_brand_protection_request,
                    timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
                ) as response:
                    
                    assert response.status == 200, f"Expected status 200, got {response.status}"
                    
                    result = await response.json()
                    print(f"✅ Brand Protection Response: {json.dumps(result, indent=2)}")
                    
                    # Validate response structure
                    assert result.get('success') is True, "Brand protection request should succeed"
                    assert 'agent_analysis' in result, "Should include agent analysis"
                    assert 'tenant_id' in result, "Should include tenant ID"
                    assert 'request_type' in result, "Should include request type"
                    
                    # Validate brand protection specific data
                    agent_analysis = result.get('agent_analysis', {})
                    assert 'brand_protection' in agent_analysis, "Should include brand protection analysis"
                    assert 'violation_detection' in agent_analysis['brand_protection'], "Should include violation detection"
                    assert 'risk_assessment' in agent_analysis['brand_protection'], "Should include risk assessment"
                    
                    print("✅ Brand protection endpoint test passed!")
                    
            except Exception as e:
                print(f"❌ Brand protection test failed: {e}")
                raise

    async def test_counterfeit_detection_endpoint(self, sample_counterfeit_detection_request):
        """Test counterfeit detection functionality"""
        print("\n🧪 Testing Counterfeit Detection...")
        
        async with aiohttp.ClientSession() as session:
            try:
                # Create request for counterfeit detection
                detection_request = {
                    **sample_counterfeit_detection_request,
                    "detection_type": "counterfeit_analysis"
                }
                
                async with session.post(
                    f"{BASE_URL}/api/brain/integrations/amazon-brand-registry/ai-brand-protection",
                    json=detection_request,
                    timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
                ) as response:
                    
                    assert response.status == 200
                    result = await response.json()
                    print(f"✅ Counterfeit Detection Response: {json.dumps(result, indent=2)}")
                    
                    # Validate counterfeit detection response
                    assert result.get('success') is True
                    agent_analysis = result.get('agent_analysis', {})
                    
                    # Should contain analysis of suspected products
                    assert 'brand_protection' in agent_analysis
                    brand_protection = agent_analysis['brand_protection']
                    assert 'violation_detection' in brand_protection
                    
                    print("✅ Counterfeit detection test passed!")
                    
            except Exception as e:
                print(f"❌ Counterfeit detection test failed: {e}")
                raise

    async def test_brand_analytics_endpoint(self, sample_brand_analytics_request):
        """Test AI brand analytics endpoint"""
        print("\n🧪 Testing AI Brand Analytics Endpoint...")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{BASE_URL}/api/brain/integrations/amazon-brand-registry/ai-brand-analytics",
                    json=sample_brand_analytics_request,
                    timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
                ) as response:
                    
                    assert response.status == 200
                    result = await response.json()
                    print(f"✅ Brand Analytics Response: {json.dumps(result, indent=2)}")
                    
                    # Validate analytics response
                    assert result.get('success') is True
                    agent_analysis = result.get('agent_analysis', {})
                    assert 'brand_performance' in agent_analysis
                    
                    # Validate performance metrics
                    brand_performance = agent_analysis['brand_performance']
                    assert 'marketplaces_analyzed' in brand_performance
                    assert 'marketplace_data' in brand_performance
                    assert 'consolidated_metrics' in brand_performance
                    
                    print("✅ Brand analytics endpoint test passed!")
                    
            except Exception as e:
                print(f"❌ Brand analytics test failed: {e}")
                raise

    async def test_competitive_intelligence_endpoint(self, sample_competitive_intelligence_request):
        """Test competitive intelligence analysis"""
        print("\n🧪 Testing Competitive Intelligence Analysis...")
        
        async with aiohttp.ClientSession() as session:
            try:
                # Create request for competitive intelligence
                intelligence_request = {
                    **sample_competitive_intelligence_request,
                    "analysis_type": "competitive_intelligence"
                }
                
                async with session.post(
                    f"{BASE_URL}/api/brain/integrations/amazon-brand-registry/ai-brand-analytics",
                    json=intelligence_request,
                    timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
                ) as response:
                    
                    assert response.status == 200
                    result = await response.json()
                    print(f"✅ Competitive Intelligence Response: {json.dumps(result, indent=2)}")
                    
                    # Validate competitive intelligence response
                    assert result.get('success') is True
                    agent_analysis = result.get('agent_analysis', {})
                    
                    # Should contain competitor analysis
                    assert 'brand_performance' in agent_analysis or 'competitive_intelligence' in agent_analysis
                    
                    print("✅ Competitive intelligence test passed!")
                    
            except Exception as e:
                print(f"❌ Competitive intelligence test failed: {e}")
                raise

    async def test_brand_content_endpoint(self, sample_content_optimization_request):
        """Test AI brand content optimization endpoint"""  
        print("\n🧪 Testing AI Brand Content Optimization Endpoint...")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{BASE_URL}/api/brain/integrations/amazon-brand-registry/ai-brand-content",
                    json=sample_content_optimization_request,
                    timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
                ) as response:
                    
                    assert response.status == 200
                    result = await response.json()
                    print(f"✅ Brand Content Response: {json.dumps(result, indent=2)}")
                    
                    # Validate content optimization response
                    assert result.get('success') is True
                    agent_analysis = result.get('agent_analysis', {})
                    assert 'content_optimization' in agent_analysis
                    
                    # Validate content optimization metrics
                    content_optimization = agent_analysis['content_optimization']
                    assert 'assets_analyzed' in content_optimization
                    assert 'optimization_recommendations' in content_optimization
                    
                    print("✅ Brand content endpoint test passed!")
                    
            except Exception as e:
                print(f"❌ Brand content test failed: {e}")
                raise

    async def test_brand_store_management(self, sample_brand_store_request):
        """Test brand store management functionality"""
        print("\n🧪 Testing Brand Store Management...")
        
        async with aiohttp.ClientSession() as session:
            try:
                # Create request for brand store management
                store_request = {
                    **sample_brand_store_request,
                    "optimization_type": "brand_store_management"
                }
                
                async with session.post(
                    f"{BASE_URL}/api/brain/integrations/amazon-brand-registry/ai-brand-content",
                    json=store_request,
                    timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
                ) as response:
                    
                    assert response.status == 200
                    result = await response.json()
                    print(f"✅ Brand Store Management Response: {json.dumps(result, indent=2)}")
                    
                    # Validate store management response
                    assert result.get('success') is True
                    agent_analysis = result.get('agent_analysis', {})
                    
                    # Should contain store optimization data
                    assert 'content_optimization' in agent_analysis or 'brand_store_optimization' in agent_analysis
                    
                    print("✅ Brand store management test passed!")
                    
            except Exception as e:
                print(f"❌ Brand store management test failed: {e}")
                raise

    async def test_brand_compliance_endpoint(self, sample_compliance_monitoring_request):
        """Test AI brand compliance monitoring endpoint"""
        print("\n🧪 Testing AI Brand Compliance Monitoring Endpoint...")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{BASE_URL}/api/brain/integrations/amazon-brand-registry/ai-brand-compliance",
                    json=sample_compliance_monitoring_request,
                    timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
                ) as response:
                    
                    assert response.status == 200
                    result = await response.json()
                    print(f"✅ Brand Compliance Response: {json.dumps(result, indent=2)}")
                    
                    # Validate compliance response
                    assert result.get('success') is True
                    agent_analysis = result.get('agent_analysis', {})
                    assert 'compliance_monitoring' in agent_analysis
                    
                    # Validate compliance monitoring metrics
                    compliance_monitoring = agent_analysis['compliance_monitoring']
                    assert 'areas_monitored' in compliance_monitoring
                    assert 'compliance_analysis' in compliance_monitoring
                    assert 'overall_compliance' in compliance_monitoring
                    
                    print("✅ Brand compliance endpoint test passed!")
                    
            except Exception as e:
                print(f"❌ Brand compliance test failed: {e}")
                raise

    async def test_ip_protection_reporting(self, sample_ip_protection_request):
        """Test IP protection reporting functionality"""
        print("\n🧪 Testing IP Protection Reporting...")
        
        async with aiohttp.ClientSession() as session:
            try:
                # Create request for IP protection
                protection_request = {
                    **sample_ip_protection_request,
                    "report_type": "ip_protection"
                }
                
                async with session.post(
                    f"{BASE_URL}/api/brain/integrations/amazon-brand-registry/ai-brand-compliance",
                    json=protection_request,
                    timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
                ) as response:
                    
                    assert response.status == 200
                    result = await response.json()
                    print(f"✅ IP Protection Response: {json.dumps(result, indent=2)}")
                    
                    # Validate IP protection response
                    assert result.get('success') is True
                    agent_analysis = result.get('agent_analysis', {})
                    
                    # Should contain IP protection analysis
                    assert 'compliance_monitoring' in agent_analysis or 'ip_protection_report' in agent_analysis
                    
                    print("✅ IP protection reporting test passed!")
                    
            except Exception as e:
                print(f"❌ IP protection reporting test failed: {e}")
                raise

    async def test_agents_status_endpoint(self):
        """Test AI agents status endpoint"""
        print("\n🧪 Testing AI Agents Status Endpoint...")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{BASE_URL}/api/brain/integrations/amazon-brand-registry/ai-agents-status",
                    params={"tenant_id": "test_status"},
                    timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
                ) as response:
                    
                    assert response.status == 200
                    result = await response.json()
                    print(f"✅ Agents Status Response: {json.dumps(result, indent=2)}")
                    
                    # Validate agents status response
                    assert 'tenant_id' in result
                    assert 'integration_status' in result
                    assert 'ai_agents' in result
                    
                    # Validate each agent status
                    ai_agents = result['ai_agents']
                    expected_agents = ['brand_protection', 'brand_analytics', 'brand_content', 'brand_compliance']
                    
                    for agent in expected_agents:
                        assert agent in ai_agents, f"Agent {agent} should be present"
                        agent_info = ai_agents[agent]
                        assert 'agent_id' in agent_info
                        assert 'status' in agent_info
                        assert 'capabilities' in agent_info
                        assert 'performance' in agent_info
                    
                    print("✅ Agents status endpoint test passed!")
                    
            except Exception as e:
                print(f"❌ Agents status test failed: {e}")
                raise

    async def test_error_handling(self):
        """Test error handling scenarios"""
        print("\n🧪 Testing Error Handling Scenarios...")
        
        async with aiohttp.ClientSession() as session:
            # Test with invalid data
            try:
                invalid_request = {"invalid": "data"}
                
                async with session.post(
                    f"{BASE_URL}/api/brain/integrations/amazon-brand-registry/ai-brand-protection",
                    json=invalid_request,
                    timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
                ) as response:
                    
                    result = await response.json()
                    print(f"📝 Error handling response: {json.dumps(result, indent=2)}")
                    
                    # Should handle gracefully - either succeed with defaults or return error
                    assert 'success' in result
                    
                    print("✅ Error handling test passed!")
                    
            except Exception as e:
                print(f"❌ Error handling test failed: {e}")
                raise

    async def test_multi_marketplace_operations(self):
        """Test multi-marketplace brand registry operations"""
        print("\n🧪 Testing Multi-Marketplace Operations...")
        
        multi_marketplace_request = {
            "tenant_id": "test_multi_marketplace",
            "keywords": ["GlobalBrand", "InternationalProduct"],
            "marketplaces": ["US", "UK", "DE", "FR", "IT", "ES", "CA", "AU", "JP"],
            "protection_level": "premium",
            "regional_settings": {
                "US": {"language": "en", "currency": "USD"},
                "UK": {"language": "en", "currency": "GBP"}, 
                "DE": {"language": "de", "currency": "EUR"},
                "FR": {"language": "fr", "currency": "EUR"},
                "IT": {"language": "it", "currency": "EUR"},
                "ES": {"language": "es", "currency": "EUR"},
                "CA": {"language": "en", "currency": "CAD"},
                "AU": {"language": "en", "currency": "AUD"},
                "JP": {"language": "ja", "currency": "JPY"}
            }
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{BASE_URL}/api/brain/integrations/amazon-brand-registry/ai-brand-protection",
                    json=multi_marketplace_request,
                    timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
                ) as response:
                    
                    assert response.status == 200
                    result = await response.json()
                    print(f"✅ Multi-marketplace Response: {json.dumps(result, indent=2)}")
                    
                    assert result.get('success') is True
                    agent_analysis = result.get('agent_analysis', {})
                    
                    # Should handle multiple marketplaces
                    assert 'brand_protection' in agent_analysis
                    
                    print("✅ Multi-marketplace operations test passed!")
                    
            except Exception as e:
                print(f"❌ Multi-marketplace test failed: {e}")
                raise

    async def test_performance_benchmarks(self):
        """Test performance benchmarks and response times"""
        print("\n🧪 Testing Performance Benchmarks...")
        
        performance_request = {
            "tenant_id": "test_performance",
            "keywords": ["PerformanceBrand"] * 10,  # Larger dataset
            "marketplaces": ["US", "UK", "DE", "FR", "IT"],
            "analysis_depth": "comprehensive"
        }
        
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            
            try:
                async with session.post(
                    f"{BASE_URL}/api/brain/integrations/amazon-brand-registry/ai-brand-protection",
                    json=performance_request,
                    timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
                ) as response:
                    
                    end_time = time.time()
                    response_time = end_time - start_time
                    
                    assert response.status == 200
                    result = await response.json()
                    
                    print(f"📊 Performance Metrics:")
                    print(f"   Response Time: {response_time:.3f} seconds")
                    print(f"   Processing Time: {result.get('processing_time', 'N/A')} seconds")
                    
                    # Performance assertions
                    assert response_time < 10.0, f"Response time {response_time:.3f}s should be under 10 seconds"
                    
                    print("✅ Performance benchmarks test passed!")
                    
            except Exception as e:
                print(f"❌ Performance test failed: {e}")
                raise

# Test execution functions
async def run_all_tests():
    """Run all Amazon Brand Registry integration tests"""
    print("🚀 Starting Amazon Brand Registry API Integration Tests...")
    print("=" * 80)
    
    # Create test instance and sample data
    test_instance = TestAmazonBrandRegistryIntegration()
    brand_protection_request = test_instance.sample_brand_protection_request()
    counterfeit_detection_request = test_instance.sample_counterfeit_detection_request()
    brand_analytics_request = test_instance.sample_brand_analytics_request()
    competitive_intelligence_request = test_instance.sample_competitive_intelligence_request()
    content_optimization_request = test_instance.sample_content_optimization_request()
    brand_store_request = test_instance.sample_brand_store_request()
    compliance_monitoring_request = test_instance.sample_compliance_monitoring_request()
    ip_protection_request = test_instance.sample_ip_protection_request()
    
    tests = [
        ("Brand Protection", test_instance.test_brand_protection_endpoint(brand_protection_request)),
        ("Counterfeit Detection", test_instance.test_counterfeit_detection_endpoint(counterfeit_detection_request)),
        ("Brand Analytics", test_instance.test_brand_analytics_endpoint(brand_analytics_request)),
        ("Competitive Intelligence", test_instance.test_competitive_intelligence_endpoint(competitive_intelligence_request)),
        ("Brand Content", test_instance.test_brand_content_endpoint(content_optimization_request)),
        ("Brand Store Management", test_instance.test_brand_store_management(brand_store_request)),
        ("Brand Compliance", test_instance.test_brand_compliance_endpoint(compliance_monitoring_request)),
        ("IP Protection Reporting", test_instance.test_ip_protection_reporting(ip_protection_request)),
        ("Agents Status", test_instance.test_agents_status_endpoint()),
        ("Error Handling", test_instance.test_error_handling()),
        ("Multi-Marketplace Operations", test_instance.test_multi_marketplace_operations()),
        ("Performance Benchmarks", test_instance.test_performance_benchmarks())
    ]
    
    results = []
    for test_name, test_coro in tests:
        try:
            print(f"\n🧪 Running {test_name} Test...")
            await test_coro
            results.append(f"✅ {test_name}: PASSED")
        except Exception as e:
            results.append(f"❌ {test_name}: FAILED - {str(e)}")
            print(f"❌ {test_name} test failed: {e}")
    
    # Test Summary
    print("\n" + "=" * 80)
    print("📋 AMAZON BRAND REGISTRY INTEGRATION TEST SUMMARY")
    print("=" * 80)
    
    passed = len([r for r in results if "PASSED" in r])
    failed = len([r for r in results if "FAILED" in r])
    
    for result in results:
        print(result)
    
    print(f"\n📊 Results: {passed} passed, {failed} failed out of {len(results)} total tests")
    
    if failed == 0:
        print("🎉 All Amazon Brand Registry integration tests passed successfully!")
        return True
    else:
        print(f"⚠️ {failed} tests failed. Please review the failures above.")
        return False

if __name__ == "__main__":
    """Run tests when executed directly"""
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)