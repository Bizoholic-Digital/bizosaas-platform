#!/usr/bin/env python3
"""
Test script for Amazon Attribution APIs Brain AI Agent Coordination Integration

Tests all AI agent endpoints to ensure proper functionality for marketing attribution:
- Amazon Attribution Analytics AI Agent (Cross-channel attribution modeling and measurement)
- Amazon Conversion Tracking AI Agent (Purchase path analysis and funnel optimization)
- Amazon Campaign Attribution AI Agent (Multi-touchpoint campaign performance analysis)
- Amazon ROI Measurement AI Agent (Revenue attribution and return calculations)
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class AmazonAttributionAPIsBrainIntegrationTester:
    """Test class for Amazon Attribution APIs Brain AI Agent Integration"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_ai_attribution_analytics(self):
        """Test AI Amazon Attribution Analytics Agent endpoint"""
        print("🧪 Testing AI Amazon Attribution Analytics Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "campaign_ids": [
                "amazon_campaign_12345",
                "amazon_campaign_67890", 
                "amazon_campaign_54321"
            ],
            "date_range": {
                "start_date": "2025-08-01",
                "end_date": "2025-09-14"
            },
            "attribution_model": "data_driven",
            "conversion_events": [
                "purchase",
                "add_to_cart",
                "view_product"
            ],
            "marketplace_id": "ATVPDKIKX0DER",
            "analysis_scope": [
                "cross_channel_analysis",
                "touchpoint_optimization",
                "attribution_modeling",
                "channel_performance"
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-attribution/ai-attribution-analytics",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon Attribution Analytics AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Campaigns Analyzed: {result['business_result']['campaigns_analyzed']}")
                        print(f"   Attribution Model: {result['business_result']['attribution_model_used']}")
                        print(f"   Attributed Conversions: {result['business_result']['total_attributed_conversions']}")
                        print(f"   Attributed Revenue: ${result['business_result']['attributed_revenue']:,.2f}")
                        print(f"   Top Channel: {result['business_result']['top_performing_channel']}")
                        print(f"   ROAS: {result['business_result']['roas_performance']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Amazon Attribution Analytics AI", "PASS", result))
                    else:
                        print("❌ Amazon Attribution Analytics AI Agent - FAILED")
                        self.test_results.append(("Amazon Attribution Analytics AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon Attribution Analytics AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Amazon Attribution Analytics AI", "ERROR", str(e)))
    
    async def test_ai_conversion_tracking(self):
        """Test AI Amazon Conversion Tracking Agent endpoint"""
        print("🧪 Testing AI Amazon Conversion Tracking Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "customer_journeys": [
                {
                    "customer_id": "cust_001",
                    "touchpoints": [
                        {"channel": "sponsored_display", "timestamp": "2025-09-10T10:00:00Z"},
                        {"channel": "sponsored_products", "timestamp": "2025-09-11T14:30:00Z"},
                        {"channel": "direct", "timestamp": "2025-09-12T16:45:00Z"}
                    ],
                    "conversion_event": "purchase",
                    "conversion_value": 89.99
                },
                {
                    "customer_id": "cust_002", 
                    "touchpoints": [
                        {"channel": "sponsored_brands", "timestamp": "2025-09-08T09:15:00Z"},
                        {"channel": "sponsored_products", "timestamp": "2025-09-09T11:20:00Z"}
                    ],
                    "conversion_event": "add_to_cart",
                    "conversion_value": 45.50
                },
                {
                    "customer_id": "cust_003",
                    "touchpoints": [
                        {"channel": "dsp", "timestamp": "2025-09-07T13:00:00Z"},
                        {"channel": "sponsored_display", "timestamp": "2025-09-08T15:30:00Z"},
                        {"channel": "sponsored_products", "timestamp": "2025-09-09T17:45:00Z"}
                    ],
                    "conversion_event": "purchase",
                    "conversion_value": 124.75
                }
            ],
            "conversion_events": [
                "purchase",
                "add_to_cart",
                "view_product"
            ],
            "attribution_window": 30,
            "analysis_type": [
                "funnel_analysis",
                "path_optimization",
                "journey_insights",
                "conversion_prediction"
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-attribution/ai-conversion-tracking",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon Conversion Tracking AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Journeys Analyzed: {result['business_result']['journeys_analyzed']}")
                        print(f"   Total Conversions: {result['business_result']['total_conversions']}")
                        print(f"   Conversion Value: ${result['business_result']['conversion_value']:,.2f}")
                        print(f"   Conversion Rate: {result['business_result']['conversion_rate']}")
                        print(f"   Optimization Opportunities: {result['business_result']['funnel_optimization_opportunities']}")
                        print(f"   Average Order Value: ${result['business_result']['average_order_value']:,.2f}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Amazon Conversion Tracking AI", "PASS", result))
                    else:
                        print("❌ Amazon Conversion Tracking AI Agent - FAILED")
                        self.test_results.append(("Amazon Conversion Tracking AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon Conversion Tracking AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Amazon Conversion Tracking AI", "ERROR", str(e)))
    
    async def test_ai_campaign_attribution(self):
        """Test AI Amazon Campaign Attribution Agent endpoint"""
        print("🧪 Testing AI Amazon Campaign Attribution Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "campaign_ids": [
                "amazon_campaign_12345",
                "amazon_campaign_67890",
                "amazon_campaign_54321",
                "amazon_campaign_98765"
            ],
            "date_range": {
                "start_date": "2025-08-01", 
                "end_date": "2025-09-14"
            },
            "attribution_model": "position_based",
            "conversion_events": [
                "purchase",
                "add_to_cart",
                "initiate_checkout"
            ],
            "marketplace_id": "ATVPDKIKX0DER",
            "analysis_scope": [
                "multi_touchpoint_analysis",
                "campaign_synergies",
                "budget_optimization",
                "performance_attribution"
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-attribution/ai-campaign-attribution",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon Campaign Attribution AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Campaigns Analyzed: {result['business_result']['campaigns_analyzed']}")
                        print(f"   Total Touchpoints: {result['business_result']['total_touchpoints']}")
                        print(f"   Attributed Conversions: {result['business_result']['attributed_conversions']}")
                        print(f"   Cross-Campaign Influence: {result['business_result']['cross_campaign_influence']}")
                        print(f"   Campaign Synergies: {result['business_result']['campaign_synergies_identified']}")
                        print(f"   Expected Performance Lift: {result['business_result']['expected_performance_lift']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Amazon Campaign Attribution AI", "PASS", result))
                    else:
                        print("❌ Amazon Campaign Attribution AI Agent - FAILED")
                        self.test_results.append(("Amazon Campaign Attribution AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon Campaign Attribution AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Amazon Campaign Attribution AI", "ERROR", str(e)))
    
    async def test_ai_roi_measurement(self):
        """Test AI Amazon ROI Measurement Agent endpoint"""
        print("🧪 Testing AI Amazon ROI Measurement Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "campaign_ids": [
                "amazon_campaign_12345",
                "amazon_campaign_67890",
                "amazon_campaign_54321"
            ],
            "date_range": {
                "start_date": "2025-08-01",
                "end_date": "2025-09-14"
            },
            "attribution_model": "data_driven",
            "conversion_events": [
                "purchase",
                "subscribe",
                "complete_registration"
            ],
            "marketplace_id": "ATVPDKIKX0DER",
            "analysis_scope": [
                "revenue_attribution",
                "profit_analysis",
                "roi_optimization",
                "cost_efficiency"
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-attribution/ai-roi-measurement",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon ROI Measurement AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Campaigns Analyzed: {result['business_result']['campaigns_analyzed']}")
                        print(f"   Total Ad Spend: ${result['business_result']['total_ad_spend']:,.2f}")
                        print(f"   Attributed Revenue: ${result['business_result']['attributed_revenue']:,.2f}")
                        print(f"   ROAS: {result['business_result']['return_on_ad_spend']}")
                        print(f"   ROI: {result['business_result']['return_on_investment']}%")
                        print(f"   Profit Margin: {result['business_result']['profit_margin']}")
                        print(f"   ROI Improvement: {result['business_result']['predicted_roi_improvement']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Amazon ROI Measurement AI", "PASS", result))
                    else:
                        print("❌ Amazon ROI Measurement AI Agent - FAILED")
                        self.test_results.append(("Amazon ROI Measurement AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon ROI Measurement AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Amazon ROI Measurement AI", "ERROR", str(e)))
    
    async def test_ai_agents_status(self):
        """Test AI Agents Status endpoint"""
        print("🧪 Testing Amazon Attribution AI Agents Status...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/brain/integrations/amazon-attribution/ai-agents-status?tenant_id=test_tenant_001"
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon Attribution AI Agents Status - SUCCESS")
                        print(f"   Total Active Agents: {result['total_active_agents']}")
                        print(f"   Brain API Version: {result['brain_api_version']}")
                        print(f"   Coordination Mode: {result['agents_status']['coordination_mode']}")
                        print(f"   Attribution Models: {', '.join(result['supported_attribution_models']).replace('_', ' ').title()}")
                        print(f"   Attribution Analyses: {result['coordination_metrics']['total_attribution_analyses']}")
                        print(f"   Conversions Tracked: {result['coordination_metrics']['total_conversions_tracked']}")
                        print(f"   Revenue Attributed: ${result['coordination_metrics']['total_revenue_attributed']:,.2f}")
                        print(f"   Average ROAS Improvement: {result['coordination_metrics']['average_roas_improvement']}")
                        print(f"   Attribution Accuracy: {result['performance_stats']['attribution_accuracy']}")
                        self.test_results.append(("Amazon Attribution AI Agents Status", "PASS", result))
                    else:
                        print("❌ Amazon Attribution AI Agents Status - FAILED")
                        self.test_results.append(("Amazon Attribution AI Agents Status", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon Attribution AI Agents Status - ERROR: {str(e)}")
            self.test_results.append(("Amazon Attribution AI Agents Status", "ERROR", str(e)))
    
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
        """Run all Amazon Attribution APIs Brain integration tests"""
        print("🚀 Starting Amazon Attribution APIs Brain AI Agent Integration Tests\n")
        
        # Test Brain API health first
        await self.test_brain_api_health()
        print()
        
        # Test all AI agent endpoints for attribution analysis
        await self.test_ai_attribution_analytics()
        print()
        
        await self.test_ai_conversion_tracking()
        print()
        
        await self.test_ai_campaign_attribution()
        print()
        
        await self.test_ai_roi_measurement()
        print()
        
        await self.test_ai_agents_status()
        print()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("=" * 85)
        print("🔍 AMAZON ATTRIBUTION APIS BRAIN AI INTEGRATION TEST SUMMARY")
        print("=" * 85)
        
        passed = sum(1 for _, status, _ in self.test_results if status == "PASS")
        failed = sum(1 for _, status, _ in self.test_results if status == "FAIL") 
        errors = sum(1 for _, status, _ in self.test_results if status == "ERROR")
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Errors: {errors}")
        print(f"Success Rate: {(passed / len(self.test_results) * 100):.1f}%\n")
        
        print("Detailed Results:")
        print("-" * 65)
        
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
        
        print("\n" + "=" * 85)
        
        if passed == len(self.test_results):
            print("🎉 ALL TESTS PASSED! Amazon Attribution APIs Brain AI Integration is fully operational.")
            print("📊 Supported Models: Data-Driven, First-Click, Last-Click, Linear, Time-Decay, Position-Based")
            print("🤖 AI Agents: Attribution Analytics, Conversion Tracking, Campaign Attribution, ROI Measurement")
            print("📈 Attribution Features: Cross-channel analysis, multi-touchpoint tracking, revenue attribution")
            print("💡 Intelligence Capabilities: Customer journey optimization, funnel analysis, campaign synergies")
            print("🎯 ROI Optimization: Revenue attribution, profit analysis, budget reallocation recommendations")
            print("📋 Conversion Events: Purchase, Add-to-Cart, View-Product, Checkout, Registration, Subscription")
            print("🌍 Marketplace Coverage: 10 global marketplaces with comprehensive attribution modeling")
        elif passed > failed + errors:
            print("⚡ Most tests passed. Amazon Attribution Brain AI Integration is mostly functional.")
        else:
            print("🔧 Issues detected. Please check failed tests and fix integration.")
        
        print("=" * 85)

async def main():
    """Main test execution function"""
    tester = AmazonAttributionAPIsBrainIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    print("Amazon Attribution APIs Brain AI Agent Integration Tester")
    print("=" * 65)
    print("📊 Marketing Attribution & Conversion Tracking Intelligence Testing")
    print("=" * 65)
    asyncio.run(main())