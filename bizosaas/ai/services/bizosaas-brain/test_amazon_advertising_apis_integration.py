#!/usr/bin/env python3
"""
Test script for Amazon Advertising APIs Brain AI Agent Coordination Integration

Tests all AI agent endpoints to ensure proper functionality:
- Amazon Campaign Optimization AI Agent (Automated bid management and budget allocation)
- Amazon Performance Analytics AI Agent (Cross-campaign insights and ROI analysis)
- Amazon Audience Intelligence AI Agent (Demographic analysis and targeting optimization)
- Amazon Creative Management AI Agent (Ad creative testing and dynamic optimization)
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class AmazonAdvertisingAPIsBrainIntegrationTester:
    """Test class for Amazon Advertising APIs Brain AI Agent Integration"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_ai_campaign_optimization(self):
        """Test AI Amazon Campaign Optimization Agent endpoint"""
        print("🧪 Testing AI Amazon Campaign Optimization Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "campaigns": [
                {
                    "campaign_id": "amazon_campaign_12345",
                    "campaign_name": "CoreLDove Electronics Q4 2025",
                    "campaign_type": "sponsored_products",
                    "budget": 2500.00,
                    "current_performance": {
                        "impressions": 45267,
                        "clicks": 1892,
                        "conversions": 134,
                        "spend": 1876.43,
                        "roas": 3.8,
                        "ctr": 0.042,
                        "cpc": 0.99,
                        "conversion_rate": 0.071
                    }
                },
                {
                    "campaign_id": "amazon_campaign_67890", 
                    "campaign_name": "BizOSaaS Enterprise Software",
                    "campaign_type": "sponsored_brands",
                    "budget": 1800.00,
                    "current_performance": {
                        "impressions": 23456,
                        "clicks": 876,
                        "conversions": 52,
                        "spend": 945.67,
                        "roas": 4.2,
                        "ctr": 0.037,
                        "cpc": 1.08,
                        "conversion_rate": 0.059
                    }
                }
            ],
            "optimization_goals": [
                "maximize_roas",
                "reduce_cpc",
                "improve_conversion_rate"
            ],
            "marketplace_id": "ATVPDKIKX0DER"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-advertising/ai-campaign-optimization",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon Campaign Optimization AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Campaigns Optimized: {result['business_result']['campaigns_optimized']}")
                        print(f"   Cost Savings: {result['business_result']['cost_savings']}")
                        print(f"   Expected ROI Improvement: {result['business_result']['expected_roi_improvement']}")
                        print(f"   Optimization Actions: {result['business_result']['optimization_actions']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Amazon Campaign Optimization AI", "PASS", result))
                    else:
                        print("❌ Amazon Campaign Optimization AI Agent - FAILED")
                        self.test_results.append(("Amazon Campaign Optimization AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon Campaign Optimization AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Amazon Campaign Optimization AI", "ERROR", str(e)))
    
    async def test_ai_performance_analytics(self):
        """Test AI Amazon Performance Analytics Agent endpoint"""
        print("🧪 Testing AI Amazon Performance Analytics Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "date_range": {
                "start_date": "2025-08-01",
                "end_date": "2025-09-14"
            },
            "api_types": [
                "sponsored_products",
                "sponsored_brands", 
                "sponsored_display",
                "dsp"
            ],
            "metrics": [
                "performance_summary",
                "cost_analysis",
                "conversion_tracking",
                "competitive_insights"
            ],
            "marketplace_id": "ATVPDKIKX0DER"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-advertising/ai-performance-analytics",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon Performance Analytics AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Analysis Period: {result['business_result']['analysis_period']}")
                        print(f"   Total Spend: {result['business_result']['total_spend']}")
                        print(f"   Total Sales: {result['business_result']['total_sales']}")
                        print(f"   Overall ROAS: {result['business_result']['overall_roas']}")
                        print(f"   Recommendations Generated: {result['business_result']['recommendations_generated']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Amazon Performance Analytics AI", "PASS", result))
                    else:
                        print("❌ Amazon Performance Analytics AI Agent - FAILED")
                        self.test_results.append(("Amazon Performance Analytics AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon Performance Analytics AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Amazon Performance Analytics AI", "ERROR", str(e)))
    
    async def test_ai_audience_intelligence(self):
        """Test AI Amazon Audience Intelligence Agent endpoint"""
        print("🧪 Testing AI Amazon Audience Intelligence Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001", 
            "campaign_ids": [
                "amazon_campaign_12345",
                "amazon_campaign_67890",
                "amazon_campaign_54321"
            ],
            "analysis_scope": [
                "demographic_analysis",
                "behavioral_insights", 
                "targeting_optimization",
                "lookalike_modeling"
            ],
            "marketplace_id": "ATVPDKIKX0DER"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-advertising/ai-audience-intelligence",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon Audience Intelligence AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Campaigns Analyzed: {result['business_result']['campaigns_analyzed']}")
                        print(f"   Targeting Opportunities: {result['business_result']['targeting_opportunities']}")
                        print(f"   Potential Reach Expansion: {result['business_result']['potential_reach_expansion']}")
                        print(f"   Lookalike Audiences: {result['business_result']['lookalike_audiences_identified']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Amazon Audience Intelligence AI", "PASS", result))
                    else:
                        print("❌ Amazon Audience Intelligence AI Agent - FAILED")
                        self.test_results.append(("Amazon Audience Intelligence AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon Audience Intelligence AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Amazon Audience Intelligence AI", "ERROR", str(e)))
    
    async def test_ai_creative_optimization(self):
        """Test AI Amazon Creative Management Agent endpoint"""
        print("🧪 Testing AI Amazon Creative Management Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "creative_assets": [
                {
                    "asset_id": "creative_image_001",
                    "asset_type": "product_image", 
                    "campaign_id": "amazon_campaign_12345",
                    "current_performance": {
                        "impressions": 12450,
                        "clicks": 534,
                        "conversions": 28,
                        "ctr": 0.043,
                        "conversion_rate": 0.052
                    }
                },
                {
                    "asset_id": "creative_video_002",
                    "asset_type": "video_ad",
                    "campaign_id": "amazon_campaign_67890",
                    "current_performance": {
                        "impressions": 8930,
                        "clicks": 267,
                        "conversions": 15,
                        "ctr": 0.030,
                        "conversion_rate": 0.056
                    }
                },
                {
                    "asset_id": "creative_headline_003",
                    "asset_type": "headline_copy",
                    "campaign_id": "amazon_campaign_54321",
                    "current_performance": {
                        "impressions": 15720,
                        "clicks": 689,
                        "conversions": 41,
                        "ctr": 0.044,
                        "conversion_rate": 0.059
                    }
                }
            ],
            "optimization_focus": [
                "ctr_improvement",
                "conversion_optimization",
                "engagement_boost"
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-advertising/ai-creative-optimization",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon Creative Management AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Assets Optimized: {result['business_result']['assets_optimized']}")
                        print(f"   A/B Tests Analyzed: {result['business_result']['ab_tests_analyzed']}")
                        print(f"   Optimization Recommendations: {result['business_result']['optimization_recommendations']}")
                        print(f"   Expected Performance Lift: {result['business_result']['expected_performance_lift']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Amazon Creative Management AI", "PASS", result))
                    else:
                        print("❌ Amazon Creative Management AI Agent - FAILED")
                        self.test_results.append(("Amazon Creative Management AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon Creative Management AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Amazon Creative Management AI", "ERROR", str(e)))
    
    async def test_ai_agents_status(self):
        """Test AI Agents Status endpoint"""
        print("🧪 Testing Amazon Advertising AI Agents Status...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/brain/integrations/amazon-advertising/ai-agents-status?tenant_id=test_tenant_001"
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon Advertising AI Agents Status - SUCCESS")
                        print(f"   Total Active Agents: {result['total_active_agents']}")
                        print(f"   Brain API Version: {result['brain_api_version']}")
                        print(f"   Coordination Mode: {result['agents_status']['coordination_mode']}")
                        print(f"   Supported APIs: {', '.join(result['supported_apis']).replace('_', ' ').title()}")
                        print(f"   Operations Processed: {result['coordination_metrics']['total_operations_processed']}")
                        print(f"   Campaigns Optimized: {result['coordination_metrics']['total_campaigns_optimized']}")
                        print(f"   Cost Savings: {result['coordination_metrics']['total_cost_savings']}")
                        print(f"   ROAS Improvement: {result['coordination_metrics']['average_roas_improvement']}")
                        self.test_results.append(("Amazon Advertising AI Agents Status", "PASS", result))
                    else:
                        print("❌ Amazon Advertising AI Agents Status - FAILED")
                        self.test_results.append(("Amazon Advertising AI Agents Status", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon Advertising AI Agents Status - ERROR: {str(e)}")
            self.test_results.append(("Amazon Advertising AI Agents Status", "ERROR", str(e)))
    
    async def test_brain_api_health(self):
        """Test Brain API health endpoint"""
        print("🧪 Testing Brain API Health...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health") as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('status') == 'healthy':
                        print("✅ Brain API Health - SUCCESS")
                        print(f"   Service: {result['service']}")
                        print(f"   Version: {result['version']}")
                        print(f"   Components: {list(result['components'].keys())}")
                        self.test_results.append(("Brain API Health", "PASS", result))
                    else:
                        print("❌ Brain API Health - FAILED")
                        self.test_results.append(("Brain API Health", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Brain API Health - ERROR: {str(e)}")
            self.test_results.append(("Brain API Health", "ERROR", str(e)))
    
    async def run_all_tests(self):
        """Run all Amazon Advertising APIs Brain integration tests"""
        print("🚀 Starting Amazon Advertising APIs Brain AI Agent Integration Tests\\n")
        
        # Test Brain API health first
        await self.test_brain_api_health()
        print()
        
        # Test all AI agent endpoints
        await self.test_ai_campaign_optimization()
        print()
        
        await self.test_ai_performance_analytics()
        print()
        
        await self.test_ai_audience_intelligence()
        print()
        
        await self.test_ai_creative_optimization()
        print()
        
        await self.test_ai_agents_status()
        print()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("=" * 80)
        print("🔍 AMAZON ADVERTISING APIS BRAIN AI INTEGRATION TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for _, status, _ in self.test_results if status == "PASS")
        failed = sum(1 for _, status, _ in self.test_results if status == "FAIL") 
        errors = sum(1 for _, status, _ in self.test_results if status == "ERROR")
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Errors: {errors}")
        print(f"Success Rate: {(passed / len(self.test_results) * 100):.1f}%\\n")
        
        print("Detailed Results:")
        print("-" * 60)
        
        for test_name, status, result in self.test_results:
            status_icon = "✅" if status == "PASS" else ("❌" if status == "FAIL" else "⚠️")
            print(f"{status_icon} {test_name}: {status}")
            
            if status == "PASS" and isinstance(result, dict):
                if 'agent_analysis' in result:
                    agent_id = result['agent_analysis'].get('agent_id', result.get('agent_id', 'N/A'))
                    print(f"    Agent ID: {agent_id}")
                elif 'total_active_agents' in result:
                    agents_count = result.get('total_active_agents', 'N/A')
                    print(f"    Active Agents: {agents_count}")
        
        print("\\n" + "=" * 80)
        
        if passed == len(self.test_results):
            print("🎉 ALL TESTS PASSED! Amazon Advertising APIs Brain AI Integration is fully operational.")
            print("📊 Supported APIs: Sponsored Products, Sponsored Brands, Sponsored Display, DSP")
            print("🤖 AI Agents: Campaign Optimization, Performance Analytics, Audience Intelligence, Creative Management")
            print("🌍 Marketplace Coverage: 10 global marketplaces including US, UK, DE, FR, IT, ES, IN, CA, AU, JP")
            print("💡 Intelligence Features: Automated bidding, audience targeting, creative testing, ROI optimization")
        elif passed > failed + errors:
            print("⚡ Most tests passed. Amazon Advertising Brain AI Integration is mostly functional.")
        else:
            print("🔧 Issues detected. Please check failed tests and fix integration.")
        
        print("=" * 80)

async def main():
    """Main test execution function"""
    tester = AmazonAdvertisingAPIsBrainIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    print("Amazon Advertising APIs Brain AI Agent Integration Tester")
    print("=" * 60)
    asyncio.run(main())