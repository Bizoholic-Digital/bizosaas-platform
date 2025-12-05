#!/usr/bin/env python3
"""
Test script for Amazon DSP APIs Brain AI Agent Coordination Integration

Tests all AI agent endpoints to ensure proper functionality for programmatic advertising:
- Amazon DSP Programmatic Campaign AI Agent (Automated display and video advertising campaigns)
- Amazon DSP Audience Intelligence AI Agent (Advanced audience targeting and lookalike modeling)
- Amazon DSP Creative Optimization AI Agent (Dynamic creative optimization and A/B testing)
- Amazon DSP Performance Analytics AI Agent (Real-time performance analysis and bid optimization)
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class AmazonDSPAPIsBrainIntegrationTester:
    """Test class for Amazon DSP APIs Brain AI Agent Integration"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_ai_programmatic_campaign(self):
        """Test AI Amazon DSP Programmatic Campaign Agent endpoint"""
        print("🧪 Testing AI Amazon DSP Programmatic Campaign Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "campaign_type": "video",
            "budget": 15000.0,
            "target_audience": {
                "segments": ["premium_electronics", "tech_enthusiasts", "smart_home_buyers"],
                "age_ranges": ["25-34", "35-44", "45-54"],
                "gender": "all",
                "interests": ["technology", "gaming", "smart_home", "premium_brands"],
                "locations": ["US", "CA", "UK", "DE", "FR"],
                "devices": ["mobile", "desktop", "tablet", "connected_tv"],
                "income_levels": ["upper_middle", "high"],
                "purchase_patterns": ["frequent_online", "premium_products"]
            },
            "bidding_strategy": "auto_bid",
            "creative_assets": [
                {
                    "type": "video",
                    "duration": 30,
                    "format": "mp4",
                    "resolution": "1920x1080",
                    "asset_id": "video_premium_tech_30s"
                },
                {
                    "type": "display", 
                    "size": "728x90",
                    "format": "jpg",
                    "asset_id": "display_leaderboard_tech"
                },
                {
                    "type": "native",
                    "format": "responsive",
                    "asset_id": "native_tech_story"
                }
            ],
            "campaign_goals": ["brand_awareness", "conversions", "video_views"],
            "marketplace_id": "ATVPDKIKX0DER"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-dsp/ai-programmatic-campaign",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon DSP Programmatic Campaign AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Campaign ID: {result['business_result']['campaign_id']}")
                        print(f"   Budget Allocated: ${result['business_result']['budget_allocated']:,.2f}")
                        print(f"   Estimated Reach: {result['business_result']['estimated_reach']:,}")
                        print(f"   Predicted Impressions: {result['business_result']['predicted_impressions']:,}")
                        print(f"   Expected Conversions: {result['business_result']['expected_conversions']:,}")
                        print(f"   Targeting Segments: {result['business_result']['targeting_segments']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Amazon DSP Programmatic Campaign AI", "PASS", result))
                    else:
                        print("❌ Amazon DSP Programmatic Campaign AI Agent - FAILED")
                        self.test_results.append(("Amazon DSP Programmatic Campaign AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon DSP Programmatic Campaign AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Amazon DSP Programmatic Campaign AI", "ERROR", str(e)))
    
    async def test_ai_audience_intelligence(self):
        """Test AI Amazon DSP Audience Intelligence Agent endpoint"""
        print("🧪 Testing AI Amazon DSP Audience Intelligence Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "audience_segments": [
                {
                    "segment_id": "premium_tech_buyers",
                    "segment_name": "Premium Technology Buyers",
                    "size": 2847563,
                    "characteristics": {
                        "age_range": "25-45",
                        "income": "high",
                        "interests": ["technology", "premium_brands", "innovation"]
                    }
                },
                {
                    "segment_id": "gaming_enthusiasts",
                    "segment_name": "Gaming Enthusiasts",
                    "size": 1945728,
                    "characteristics": {
                        "age_range": "18-35",
                        "interests": ["gaming", "esports", "streaming", "hardware"]
                    }
                },
                {
                    "segment_id": "smart_home_adopters",
                    "segment_name": "Smart Home Early Adopters",
                    "size": 1274639,
                    "characteristics": {
                        "age_range": "30-50",
                        "income": "upper_middle",
                        "interests": ["smart_home", "iot", "automation", "security"]
                    }
                }
            ],
            "analysis_type": [
                "demographic_analysis",
                "behavioral_insights",
                "lookalike_modeling",
                "competition_analysis",
                "expansion_opportunities"
            ],
            "campaign_context": {
                "industry": "consumer_electronics",
                "product_category": "smart_devices",
                "price_range": "premium",
                "launch_timeline": "Q4_2025"
            },
            "targeting_goals": [
                "maximize_reach",
                "improve_engagement",
                "reduce_acquisition_cost",
                "increase_conversion_rate"
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-dsp/ai-audience-intelligence",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon DSP Audience Intelligence AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Total Audience Analyzed: {result['business_result']['total_audience_analyzed']:,}")
                        print(f"   Targetable Audience: {result['business_result']['targetable_audience']:,}")
                        print(f"   Audience Quality Score: {result['business_result']['audience_quality_score']}")
                        print(f"   High-Value Segments: {result['business_result']['high_value_segments']}")
                        print(f"   Lookalike Opportunities: {result['business_result']['lookalike_opportunities']}")
                        print(f"   Expected Reach Increase: {result['business_result']['expected_reach_increase']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Amazon DSP Audience Intelligence AI", "PASS", result))
                    else:
                        print("❌ Amazon DSP Audience Intelligence AI Agent - FAILED")
                        self.test_results.append(("Amazon DSP Audience Intelligence AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon DSP Audience Intelligence AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Amazon DSP Audience Intelligence AI", "ERROR", str(e)))
    
    async def test_ai_creative_optimization(self):
        """Test AI Amazon DSP Creative Optimization Agent endpoint"""
        print("🧪 Testing AI Amazon DSP Creative Optimization Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "campaign_type": "display",
            "budget": 8000.0,
            "target_audience": {
                "segments": ["tech_early_adopters", "premium_shoppers"],
                "demographics": {
                    "age_range": "28-42",
                    "income": "high",
                    "education": "college_plus"
                }
            },
            "bidding_strategy": "viewable_cpm",
            "creative_assets": [
                {
                    "asset_id": "display_premium_001",
                    "type": "display",
                    "size": "300x250",
                    "format": "jpg",
                    "creative_elements": {
                        "headline": "Premium Smart Devices",
                        "description": "Transform your home with AI",
                        "cta": "Shop Now",
                        "color_scheme": "blue_gradient"
                    },
                    "current_performance": {
                        "impressions": 45672,
                        "clicks": 1456,
                        "ctr": 0.032,
                        "conversions": 89,
                        "conversion_rate": 0.061
                    }
                },
                {
                    "asset_id": "video_premium_002",
                    "type": "video",
                    "duration": 15,
                    "format": "mp4",
                    "creative_elements": {
                        "opening": "lifestyle_scene",
                        "product_focus": "smart_speaker",
                        "music": "upbeat_modern",
                        "cta": "Learn More"
                    },
                    "current_performance": {
                        "impressions": 28945,
                        "views": 23456,
                        "view_rate": 0.81,
                        "clicks": 892,
                        "ctr": 0.038
                    }
                },
                {
                    "asset_id": "native_premium_003",
                    "type": "native",
                    "format": "responsive",
                    "creative_elements": {
                        "headline": "The Future of Smart Living",
                        "image": "modern_home_setup",
                        "content": "article_style"
                    },
                    "current_performance": {
                        "impressions": 18734,
                        "clicks": 723,
                        "ctr": 0.039,
                        "engagement_time": "2.4s"
                    }
                }
            ],
            "campaign_goals": ["engagement", "conversions", "brand_awareness"],
            "marketplace_id": "ATVPDKIKX0DER"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-dsp/ai-creative-optimization",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon DSP Creative Optimization AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Creatives Analyzed: {result['business_result']['creatives_analyzed']}")
                        print(f"   DCO Variants Generated: {result['business_result']['dco_variants_generated']}")
                        print(f"   CTR Improvement: {result['business_result']['ctr_improvement']}")
                        print(f"   Conversion Rate Lift: {result['business_result']['conversion_rate_lift']}")
                        print(f"   Performance Variance: {result['business_result']['performance_variance']}")
                        print(f"   Optimization Potential: {result['business_result']['optimization_potential']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Amazon DSP Creative Optimization AI", "PASS", result))
                    else:
                        print("❌ Amazon DSP Creative Optimization AI Agent - FAILED")
                        self.test_results.append(("Amazon DSP Creative Optimization AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon DSP Creative Optimization AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Amazon DSP Creative Optimization AI", "ERROR", str(e)))
    
    async def test_ai_performance_analytics(self):
        """Test AI Amazon DSP Performance Analytics Agent endpoint"""
        print("🧪 Testing AI Amazon DSP Performance Analytics Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "campaign_type": "video",
            "budget": 12000.0,
            "target_audience": {
                "segments": ["tech_professionals", "premium_consumers"],
                "targeting_parameters": {
                    "device_types": ["mobile", "desktop", "connected_tv"],
                    "placement_types": ["premium_inventory", "video_content"]
                }
            },
            "bidding_strategy": "target_cpa",
            "creative_assets": [
                {
                    "asset_id": "video_campaign_main",
                    "type": "video",
                    "performance_data": {
                        "impressions": 1245673,
                        "views": 987456,
                        "clicks": 34567,
                        "conversions": 2456,
                        "spend": 8945.67
                    }
                },
                {
                    "asset_id": "display_campaign_support", 
                    "type": "display",
                    "performance_data": {
                        "impressions": 567823,
                        "clicks": 18945,
                        "conversions": 1234,
                        "spend": 3254.33
                    }
                }
            ],
            "campaign_goals": ["conversions", "brand_awareness"],
            "marketplace_id": "ATVPDKIKX0DER"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-dsp/ai-performance-analytics",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon DSP Performance Analytics AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Impressions Delivered: {result['business_result']['impressions_delivered']:,}")
                        print(f"   Clicks Generated: {result['business_result']['clicks_generated']:,}")
                        print(f"   Conversions Tracked: {result['business_result']['conversions_tracked']:,}")
                        print(f"   Click-Through Rate: {result['business_result']['click_through_rate']}")
                        print(f"   Conversion Rate: {result['business_result']['conversion_rate']}")
                        print(f"   Return on Ad Spend: {result['business_result']['return_on_ad_spend']}")
                        print(f"   Scaling Recommendation: {result['business_result']['scaling_recommendation']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Amazon DSP Performance Analytics AI", "PASS", result))
                    else:
                        print("❌ Amazon DSP Performance Analytics AI Agent - FAILED")
                        self.test_results.append(("Amazon DSP Performance Analytics AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon DSP Performance Analytics AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Amazon DSP Performance Analytics AI", "ERROR", str(e)))
    
    async def test_ai_agents_status(self):
        """Test AI Agents Status endpoint"""
        print("🧪 Testing Amazon DSP AI Agents Status...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/brain/integrations/amazon-dsp/ai-agents-status?tenant_id=test_tenant_001"
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Amazon DSP AI Agents Status - SUCCESS")
                        print(f"   Total Active Agents: {result['total_active_agents']}")
                        print(f"   Brain API Version: {result['brain_api_version']}")
                        print(f"   Coordination Mode: {result['agents_status']['coordination_mode']}")
                        print(f"   Campaign Types: {', '.join(result['supported_campaign_types']).replace('_', ' ').title()}")
                        print(f"   Campaigns Managed: {result['coordination_metrics']['total_campaigns_managed']}")
                        print(f"   Impressions Delivered: {result['coordination_metrics']['total_impressions_delivered']:,}")
                        print(f"   Conversions Generated: {result['coordination_metrics']['total_conversions_generated']:,}")
                        print(f"   Average ROAS: {result['coordination_metrics']['average_roas_achieved']}")
                        print(f"   Campaign Success Rate: {result['performance_stats']['campaign_success_rate']}")
                        print(f"   CTR Improvement: {result['performance_stats']['average_ctr_improvement']}")
                        self.test_results.append(("Amazon DSP AI Agents Status", "PASS", result))
                    else:
                        print("❌ Amazon DSP AI Agents Status - FAILED")
                        self.test_results.append(("Amazon DSP AI Agents Status", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon DSP AI Agents Status - ERROR: {str(e)}")
            self.test_results.append(("Amazon DSP AI Agents Status", "ERROR", str(e)))
    
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
        """Run all Amazon DSP APIs Brain integration tests"""
        print("🚀 Starting Amazon DSP APIs Brain AI Agent Integration Tests\n")
        
        # Test Brain API health first
        await self.test_brain_api_health()
        print()
        
        # Test all AI agent endpoints for programmatic advertising
        await self.test_ai_programmatic_campaign()
        print()
        
        await self.test_ai_audience_intelligence()
        print()
        
        await self.test_ai_creative_optimization()
        print()
        
        await self.test_ai_performance_analytics()
        print()
        
        await self.test_ai_agents_status()
        print()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("=" * 80)
        print("🔍 AMAZON DSP APIS BRAIN AI INTEGRATION TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for _, status, _ in self.test_results if status == "PASS")
        failed = sum(1 for _, status, _ in self.test_results if status == "FAIL") 
        errors = sum(1 for _, status, _ in self.test_results if status == "ERROR")
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Errors: {errors}")
        print(f"Success Rate: {(passed / len(self.test_results) * 100):.1f}%\n")
        
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
        
        print("\n" + "=" * 80)
        
        if passed == len(self.test_results):
            print("🎉 ALL TESTS PASSED! Amazon DSP APIs Brain AI Integration is fully operational.")
            print("📺 Supported Formats: Display, Video, Audio, Native, Connected TV, Mobile App")
            print("🤖 AI Agents: Programmatic Campaign, Audience Intelligence, Creative Optimization, Performance Analytics")
            print("🎯 Targeting Capabilities: Demographic, Behavioral, Contextual, Lookalike, Retargeting, Custom")
            print("💡 Intelligence Features: Real-time bidding, dynamic creative optimization, audience modeling")
            print("📊 Performance Optimization: Automated bid management, creative testing, audience expansion")
            print("🔄 Bidding Strategies: CPM, CPC, CPA, Viewable CPM, Auto-Bid, Target CPA")
            print("🌐 Cross-Device Tracking: Mobile, Desktop, Tablet, Connected TV integration")
        elif passed > failed + errors:
            print("⚡ Most tests passed. Amazon DSP Brain AI Integration is mostly functional.")
        else:
            print("🔧 Issues detected. Please check failed tests and fix integration.")
        
        print("=" * 80)

async def main():
    """Main test execution function"""
    tester = AmazonDSPAPIsBrainIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    print("Amazon DSP APIs Brain AI Agent Integration Tester")
    print("=" * 60)
    print("📺 Programmatic Advertising & Display Intelligence Testing")
    print("=" * 60)
    asyncio.run(main())