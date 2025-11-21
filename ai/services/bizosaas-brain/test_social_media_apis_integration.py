#!/usr/bin/env python3
"""
Test script for Social Media APIs Brain AI Agent Coordination Integration

Tests all AI agent endpoints to ensure proper functionality:
- Facebook Marketing AI Agent (Meta Business)
- LinkedIn Marketing AI Agent (LinkedIn Marketing API)
- Twitter Marketing AI Agent (Twitter/X API v2)
- TikTok Marketing AI Agent (TikTok Marketing API)
- Pinterest Marketing AI Agent (Pinterest Business API)
- Social Media Analytics AI Agent
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class SocialMediaAPIsBrainIntegrationTester:
    """Test class for Social Media APIs Brain AI Agent Integration"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_ai_facebook_campaign(self):
        """Test AI Facebook Marketing Agent endpoint"""
        print("🧪 Testing AI Facebook Marketing Agent (Meta Business)...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "campaign_name": "AI Marketing Revolution Campaign",
            "objective": "TRAFFIC",
            "budget": 200.0,
            "duration_days": 7,
            "target_audience": {
                "age_range": [25, 45],
                "interests": ["marketing", "business", "technology", "ai"],
                "location": ["US", "CA", "UK"]
            },
            "ad_creative": {
                "primary_text": "Discover the power of AI marketing automation",
                "headline": "Transform Your Marketing with AI",
                "description": "Join thousands of businesses using AI to boost their marketing ROI"
            },
            "placement": ["facebook", "instagram"],
            "optimization_goal": "LINK_CLICKS",
            "bid_strategy": "LOWEST_COST"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/social-media/ai-facebook-campaign",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Facebook Marketing AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Campaign ID: {result['agent_analysis']['campaign_result']['campaign_id']}")
                        print(f"   Estimated Reach: {result['agent_analysis']['audience_reach']:,}")
                        print(f"   Optimization Score: {result['agent_analysis']['optimization_score']}")
                        print(f"   Cost Per Result: {result['agent_analysis']['cost_per_result']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Facebook Marketing AI", "PASS", result))
                    else:
                        print("❌ Facebook Marketing AI Agent - FAILED")
                        self.test_results.append(("Facebook Marketing AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Facebook Marketing AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Facebook Marketing AI", "ERROR", str(e)))
    
    async def test_ai_linkedin_campaign(self):
        """Test AI LinkedIn Marketing Agent endpoint"""
        print("🧪 Testing AI LinkedIn Marketing Agent (LinkedIn Marketing API)...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "campaign_name": "B2B AI Solutions Lead Generation",
            "campaign_type": "SPONSORED_CONTENT",
            "budget": 300.0,
            "duration_days": 14,
            "targeting": {
                "job_functions": ["marketing", "sales", "business_development"],
                "seniority_levels": ["manager", "director", "vp"],
                "company_sizes": ["201-500", "501-1000", "1001-5000"],
                "industries": ["technology", "financial_services", "manufacturing"]
            },
            "content": {
                "headline": "Boost B2B Sales with AI Marketing Automation",
                "description": "See how leading companies increase leads by 300% with AI-powered marketing strategies",
                "call_to_action": "Learn More"
            },
            "bid_type": "CPC",
            "objective": "WEBSITE_VISITS"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/social-media/ai-linkedin-campaign",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ LinkedIn Marketing AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Campaign ID: {result['agent_analysis']['campaign_result']['campaign_id']}")
                        print(f"   Professional Reach: {result['agent_analysis']['professional_reach']:,}")
                        print(f"   Lead Quality Score: {result['agent_analysis']['lead_quality_score']}")
                        print(f"   Cost Per Click: {result['agent_analysis']['campaign_result']['cost_per_click']}")
                        print(f"   Estimated Leads: {result['agent_analysis']['campaign_result']['professional_metrics']['estimated_leads']}")
                        self.test_results.append(("LinkedIn Marketing AI", "PASS", result))
                    else:
                        print("❌ LinkedIn Marketing AI Agent - FAILED")
                        self.test_results.append(("LinkedIn Marketing AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ LinkedIn Marketing AI Agent - ERROR: {str(e)}")
            self.test_results.append(("LinkedIn Marketing AI", "ERROR", str(e)))
    
    async def test_ai_twitter_campaign(self):
        """Test AI Twitter Marketing Agent endpoint"""
        print("🧪 Testing AI Twitter Marketing Agent (Twitter/X API v2)...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "campaign_name": "AI Marketing Tips Viral Campaign",
            "campaign_type": "PROMOTED_TWEETS",
            "budget": 180.0,
            "duration_days": 10,
            "tweet_content": "🚀 Just discovered how AI is transforming marketing ROI! Here are 3 game-changing strategies that boosted our clients' results by 400%... 🧵 Thread below 👇 #MarketingTips #AI #BusinessGrowth",
            "targeting": {
                "interests": ["marketing", "business", "entrepreneurship", "technology"],
                "demographics": {"age_range": [22, 50]},
                "behaviors": ["engaged_with_business_content"]
            },
            "engagement_goals": ["clicks", "retweets", "likes", "replies"]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/social-media/ai-twitter-campaign",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Twitter Marketing AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Campaign ID: {result['agent_analysis']['campaign_result']['campaign_id']}")
                        print(f"   Estimated Reach: {result['agent_analysis']['campaign_result']['estimated_reach']:,}")
                        print(f"   Viral Potential: {result['agent_analysis']['viral_potential']}")
                        print(f"   Hashtag Performance: {result['agent_analysis']['hashtag_performance']['trending_score']}")
                        print(f"   Expected Engagements: {result['agent_analysis']['campaign_result']['estimated_engagements']:,}")
                        self.test_results.append(("Twitter Marketing AI", "PASS", result))
                    else:
                        print("❌ Twitter Marketing AI Agent - FAILED")
                        self.test_results.append(("Twitter Marketing AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Twitter Marketing AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Twitter Marketing AI", "ERROR", str(e)))
    
    async def test_ai_tiktok_campaign(self):
        """Test AI TikTok Marketing Agent endpoint"""
        print("🧪 Testing AI TikTok Marketing Agent (TikTok Marketing API)...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "campaign_name": "Business Tips Going Viral",
            "campaign_type": "REACH",
            "budget": 250.0,
            "duration_days": 7,
            "video_content": {
                "format": "9:16",
                "duration": 30,
                "theme": "behind_the_scenes_business",
                "hooks": ["You won't believe what happened when I used AI for marketing..."],
                "call_to_action": "Follow for more business tips"
            },
            "targeting": {
                "age_range": [18, 35],
                "interests": ["business", "entrepreneurship", "marketing", "side_hustles"],
                "demographics": "gen_z_millennials"
            },
            "optimization_goal": "VIDEO_VIEW"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/social-media/ai-tiktok-campaign",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ TikTok Marketing AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Campaign ID: {result['agent_analysis']['campaign_result']['campaign_id']}")
                        print(f"   Estimated Reach: {result['agent_analysis']['campaign_result']['estimated_reach']:,}")
                        print(f"   Viral Score: {result['agent_analysis']['viral_score']}")
                        print(f"   For You Page Probability: {result['agent_analysis']['campaign_result']['viral_metrics']['for_you_page_probability']}")
                        print(f"   Video Completion Rate: {result['agent_analysis']['campaign_result']['creative_performance']['video_completion_rate']}")
                        self.test_results.append(("TikTok Marketing AI", "PASS", result))
                    else:
                        print("❌ TikTok Marketing AI Agent - FAILED")
                        self.test_results.append(("TikTok Marketing AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ TikTok Marketing AI Agent - ERROR: {str(e)}")
            self.test_results.append(("TikTok Marketing AI", "ERROR", str(e)))
    
    async def test_ai_pinterest_campaign(self):
        """Test AI Pinterest Marketing Agent endpoint"""
        print("🧪 Testing AI Pinterest Marketing Agent (Pinterest Business API)...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "campaign_name": "Business Growth Ideas Collection",
            "campaign_type": "AWARENESS", 
            "budget": 150.0,
            "duration_days": 21,
            "pin_content": {
                "title": "10 AI Marketing Strategies That Actually Work",
                "description": "Discover proven AI marketing strategies that top businesses use to increase their ROI by 300%+",
                "image_url": "https://example.com/ai-marketing-infographic.jpg",
                "landing_page": "https://example.com/ai-marketing-guide"
            },
            "targeting": {
                "keywords": ["marketing tips", "business growth", "ai marketing", "digital marketing"],
                "interests": ["business", "marketing", "entrepreneurship", "productivity"],
                "demographics": {"age_range": [25, 55]}
            },
            "placement": "ALL"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/social-media/ai-pinterest-campaign",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Pinterest Marketing AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Campaign ID: {result['agent_analysis']['campaign_result']['campaign_id']}")
                        print(f"   Estimated Reach: {result['agent_analysis']['campaign_result']['estimated_reach']:,}")
                        print(f"   Discovery Potential: {result['agent_analysis']['discovery_potential']}")
                        print(f"   Expected Saves: {result['agent_analysis']['campaign_result']['estimated_saves']:,}")
                        print(f"   Search Visibility: {result['agent_analysis']['seasonal_alignment']}")
                        self.test_results.append(("Pinterest Marketing AI", "PASS", result))
                    else:
                        print("❌ Pinterest Marketing AI Agent - FAILED")
                        self.test_results.append(("Pinterest Marketing AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Pinterest Marketing AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Pinterest Marketing AI", "ERROR", str(e)))
    
    async def test_ai_social_media_analytics(self):
        """Test AI Social Media Analytics Agent endpoint"""
        print("🧪 Testing AI Social Media Analytics Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "platforms": ["facebook", "linkedin", "twitter", "tiktok", "pinterest"],
            "date_range": {
                "start_date": "2025-08-01",
                "end_date": "2025-09-14"
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/social-media/ai-analytics",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Social Media Analytics AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Analysis Period: {result['agent_analysis']['analysis_period']}")
                        print(f"   Platforms Analyzed: {len(result['agent_analysis']['platforms_analyzed'])}")
                        print(f"   Overall ROAS: {result['agent_analysis']['roi_optimization']['overall_roas']}x")
                        print(f"   Best Performing Platform: {result['agent_analysis']['unified_insights']['best_performing_platform']}")
                        print(f"   Highest ROI Platform: {result['agent_analysis']['unified_insights']['highest_roi_platform']}")
                        print(f"   Trend Predictions: {len(result['agent_analysis']['trend_forecasting']['emerging_trends'])}")
                        self.test_results.append(("Social Media Analytics AI", "PASS", result))
                    else:
                        print("❌ Social Media Analytics AI Agent - FAILED")
                        self.test_results.append(("Social Media Analytics AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Social Media Analytics AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Social Media Analytics AI", "ERROR", str(e)))
    
    async def test_ai_agents_status(self):
        """Test AI Agents Status endpoint"""
        print("🧪 Testing AI Agents Status...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/brain/integrations/social-media/ai-agents-status?tenant_id=test_tenant_001"
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ AI Agents Status - SUCCESS")
                        print(f"   Total Active Agents: {result['total_active_agents']}")
                        print(f"   Brain API Version: {result['brain_api_version']}")
                        print(f"   Coordination Mode: {result['agents_status']['coordination_mode']}")
                        print(f"   Supported Platforms: {', '.join(result['supported_platforms'])}")
                        print(f"   Total Decisions Coordinated: {result['coordination_metrics']['total_decisions_coordinated']}")
                        print(f"   Cross-platform Optimization: {result['coordination_metrics']['cross_platform_optimization']}")
                        self.test_results.append(("AI Agents Status", "PASS", result))
                    else:
                        print("❌ AI Agents Status - FAILED")
                        self.test_results.append(("AI Agents Status", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ AI Agents Status - ERROR: {str(e)}")
            self.test_results.append(("AI Agents Status", "ERROR", str(e)))
    
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
        """Run all Social Media APIs Brain integration tests"""
        print("🚀 Starting Social Media APIs Brain AI Agent Integration Tests\\n")
        
        # Test Brain API health first
        await self.test_brain_api_health()
        print()
        
        # Test all AI agent endpoints
        await self.test_ai_facebook_campaign()
        print()
        
        await self.test_ai_linkedin_campaign()
        print()
        
        await self.test_ai_twitter_campaign()
        print()
        
        await self.test_ai_tiktok_campaign()
        print()
        
        await self.test_ai_pinterest_campaign()
        print()
        
        await self.test_ai_social_media_analytics()
        print()
        
        await self.test_ai_agents_status()
        print()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("=" * 90)
        print("🔍 SOCIAL MEDIA APIS BRAIN AI INTEGRATION TEST SUMMARY")
        print("=" * 90)
        
        passed = sum(1 for _, status, _ in self.test_results if status == "PASS")
        failed = sum(1 for _, status, _ in self.test_results if status == "FAIL") 
        errors = sum(1 for _, status, _ in self.test_results if status == "ERROR")
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Errors: {errors}")
        print(f"Success Rate: {(passed / len(self.test_results) * 100):.1f}%\\n")
        
        print("Detailed Results:")
        print("-" * 70)
        
        for test_name, status, result in self.test_results:
            status_icon = "✅" if status == "PASS" else ("❌" if status == "FAIL" else "⚠️")
            print(f"{status_icon} {test_name}: {status}")
            
            if status == "PASS" and isinstance(result, dict):
                if 'agent_analysis' in result:
                    agent_id = result['agent_analysis'].get('agent_id', 'N/A')
                    print(f"    Agent ID: {agent_id}")
                elif 'agents_status' in result:
                    agents_count = result.get('total_active_agents', 'N/A')
                    print(f"    Active Agents: {agents_count}")
        
        print("\\n" + "=" * 90)
        
        if passed == len(self.test_results):
            print("🎉 ALL TESTS PASSED! Social Media APIs Brain AI Integration is fully operational.")
            print("📱 Supported Platforms: Facebook, LinkedIn, Twitter/X, TikTok, Pinterest")
            print("🤖 AI Agents: Campaign Management, Cross-Platform Analytics, Viral Optimization")
            print("🚀 Features: Multi-platform campaigns, trend analysis, ROI optimization, competitor insights")
        elif passed > failed + errors:
            print("⚡ Most tests passed. Brain AI Integration is mostly functional.")
        else:
            print("🔧 Issues detected. Please check failed tests and fix integration.")
        
        print("=" * 90)

async def main():
    """Main test execution function"""
    tester = SocialMediaAPIsBrainIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    print("Social Media APIs Brain AI Agent Integration Tester")
    print("Including Facebook, LinkedIn, Twitter/X, TikTok, Pinterest")
    print("=" * 70)
    asyncio.run(main())