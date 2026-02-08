#!/usr/bin/env python3
"""
Test script for Email Service Providers Brain AI Agent Coordination Integration

Tests all AI agent endpoints to ensure proper functionality:
- Email Campaign AI Agent
- Email Analytics AI Agent
- Email Deliverability AI Agent
- Email Template AI Agent
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class EmailProvidersBrainIntegrationTester:
    """Test class for Email Service Providers Brain AI Agent Integration"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_ai_campaign_optimization(self):
        """Test AI Email Campaign Agent endpoint"""
        print("🧪 Testing AI Email Campaign Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "provider": "sendgrid",
            "campaign_name": "Welcome Campaign 2025",
            "subject": "Welcome to our exclusive community!",
            "recipients": [
                {"email": "customer1@example.com", "first_name": "John", "company": "TechCorp"},
                {"email": "customer2@example.com", "first_name": "Jane", "company": "StartupInc"}
            ],
            "template_type": "marketing",
            "ab_test_enabled": True,
            "personalization": {"industry": "technology", "tone": "friendly"}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/email-providers/ai-campaign-optimization",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Email Campaign AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   AI Confidence Score: {result['agent_analysis']['ai_confidence_score']}%")
                        print(f"   Expected Improvement: {result['agent_analysis']['expected_improvement']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Email Campaign AI", "PASS", result))
                    else:
                        print("❌ Email Campaign AI Agent - FAILED")
                        self.test_results.append(("Email Campaign AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Email Campaign AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Email Campaign AI", "ERROR", str(e)))
    
    async def test_ai_analytics(self):
        """Test AI Email Analytics Agent endpoint"""
        print("🧪 Testing AI Email Analytics Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "provider": "sendgrid",
            "date_range": {
                "start_date": "2025-08-01",
                "end_date": "2025-09-14"
            },
            "campaign_ids": ["campaign_001", "campaign_002"],
            "metrics": ["open_rate", "click_rate", "conversion_rate", "deliverability"]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/email-providers/ai-analytics",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Email Analytics AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Performance Analysis Period: {result['agent_analysis']['analysis_period']}")
                        print(f"   AI Insights Generated: {len(result['agent_analysis']['ai_insights'])}")
                        print(f"   Improvement Opportunities: {len(result['agent_analysis']['improvement_opportunities'])}")
                        self.test_results.append(("Email Analytics AI", "PASS", result))
                    else:
                        print("❌ Email Analytics AI Agent - FAILED")
                        self.test_results.append(("Email Analytics AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Email Analytics AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Email Analytics AI", "ERROR", str(e)))
    
    async def test_ai_deliverability(self):
        """Test AI Email Deliverability Agent endpoint"""
        print("🧪 Testing AI Email Deliverability Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "provider": "amazon_ses",
            "sender_domains": ["mail.example.com", "newsletters.example.com"],
            "analyze_reputation": True,
            "fix_issues": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/email-providers/ai-deliverability",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Email Deliverability AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Deliverability Score: {result['agent_analysis']['deliverability_score']}")
                        print(f"   Sender Reputation: {result['agent_analysis']['sender_reputation']['overall_reputation']}")
                        print(f"   Expected Improvement: {result['agent_analysis']['expected_improvement']}")
                        self.test_results.append(("Email Deliverability AI", "PASS", result))
                    else:
                        print("❌ Email Deliverability AI Agent - FAILED")
                        self.test_results.append(("Email Deliverability AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Email Deliverability AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Email Deliverability AI", "ERROR", str(e)))
    
    async def test_ai_template_generation(self):
        """Test AI Email Template Agent endpoint"""
        print("🧪 Testing AI Email Template Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "provider": "brevo",
            "template_type": "newsletter",
            "industry": "technology",
            "tone": "professional",
            "personalization_fields": ["first_name", "company", "industry", "last_purchase"]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/email-providers/ai-template-generation",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Email Template AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Template Type: {result['agent_analysis']['template_type']}")
                        print(f"   Optimization Score: {result['agent_analysis']['optimization_score']}")
                        print(f"   Template Variants: {len(result['agent_analysis']['template_variants'])}")
                        print(f"   Implementation Ready: {result['agent_analysis']['implementation_ready']}")
                        self.test_results.append(("Email Template AI", "PASS", result))
                    else:
                        print("❌ Email Template AI Agent - FAILED")
                        self.test_results.append(("Email Template AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Email Template AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Email Template AI", "ERROR", str(e)))
    
    async def test_ai_agents_status(self):
        """Test AI Agents Status endpoint"""
        print("🧪 Testing AI Agents Status...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/brain/integrations/email-providers/ai-agents-status?tenant_id=test_tenant_001"
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ AI Agents Status - SUCCESS")
                        print(f"   Total Active Agents: {result['total_active_agents']}")
                        print(f"   Brain API Version: {result['brain_api_version']}")
                        print(f"   Coordination Mode: {result['agents_status']['coordination_mode']}")
                        print(f"   Supported Providers: {', '.join(result['supported_providers'])}")
                        print(f"   Total Decisions Coordinated: {result['coordination_metrics']['total_decisions_coordinated']}")
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
        """Run all Email Service Providers Brain integration tests"""
        print("🚀 Starting Email Service Providers Brain AI Agent Integration Tests\\n")
        
        # Test Brain API health first
        await self.test_brain_api_health()
        print()
        
        # Test all AI agent endpoints
        await self.test_ai_campaign_optimization()
        print()
        
        await self.test_ai_analytics()
        print()
        
        await self.test_ai_deliverability()
        print()
        
        await self.test_ai_template_generation()
        print()
        
        await self.test_ai_agents_status()
        print()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("=" * 80)
        print("🔍 EMAIL SERVICE PROVIDERS BRAIN AI INTEGRATION TEST SUMMARY")
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
                    agent_id = result['agent_analysis'].get('agent_id', 'N/A')
                    print(f"    Agent ID: {agent_id}")
                elif 'agents_status' in result:
                    agents_count = result.get('total_active_agents', 'N/A')
                    print(f"    Active Agents: {agents_count}")
        
        print("\\n" + "=" * 80)
        
        if passed == len(self.test_results):
            print("🎉 ALL TESTS PASSED! Email Service Providers Brain AI Integration is fully operational.")
            print("📧 Supported Providers: Amazon SES, SendGrid, Brevo, Mailchimp")
            print("🤖 AI Agents: Campaign Optimization, Analytics, Deliverability, Template Generation")
        elif passed > failed + errors:
            print("⚡ Most tests passed. Brain AI Integration is mostly functional.")
        else:
            print("🔧 Issues detected. Please check failed tests and fix integration.")
        
        print("=" * 80)

async def main():
    """Main test execution function"""
    tester = EmailProvidersBrainIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    print("Email Service Providers Brain AI Agent Integration Tester")
    print("=" * 60)
    asyncio.run(main())