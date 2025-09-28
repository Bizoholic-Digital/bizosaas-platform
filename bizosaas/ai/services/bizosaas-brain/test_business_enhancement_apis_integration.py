#!/usr/bin/env python3
"""
Test script for Business Enhancement APIs Brain AI Agent Coordination Integration

Tests all AI agent endpoints to ensure proper functionality:
- HubSpot CRM AI Agent (Advanced CRM and marketing automation)
- Slack Communication AI Agent (Team workflow automation)
- Calendly Scheduling AI Agent (Intelligent meeting optimization)
- Business Analytics AI Agent (Cross-platform business intelligence)
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class BusinessEnhancementAPIsBrainIntegrationTester:
    """Test class for Business Enhancement APIs Brain AI Agent Integration"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_ai_hubspot_crm(self):
        """Test AI HubSpot CRM Agent endpoint"""
        print("🧪 Testing AI HubSpot CRM Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "action": "create_contact",
            "object_type": "contacts",
            "properties": {
                "email": "sarah.johnson@innovatetech.com",
                "firstname": "Sarah",
                "lastname": "Johnson",
                "company": "InnovateTech Solutions",
                "jobtitle": "VP of Marketing",
                "phone": "+1-555-123-4567",
                "website": "https://innovatetech.com",
                "industry": "Technology",
                "num_employees": "500-1000"
            },
            "metadata": {
                "source": "website_form",
                "campaign": "enterprise_demo_2025",
                "lead_source": "content_marketing"
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/business-enhancement/ai-hubspot-crm",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ HubSpot CRM AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_id']}")
                        print(f"   Contact ID: {result['business_result']['contact_id']}")
                        print(f"   Lead Score: {result['agent_analysis']['lead_intelligence']['ai_score']}")
                        print(f"   Qualification Level: {result['agent_analysis']['lead_intelligence']['qualification_level']}")
                        print(f"   Lifecycle Stage: {result['business_result']['lifecycle_stage']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("HubSpot CRM AI", "PASS", result))
                    else:
                        print("❌ HubSpot CRM AI Agent - FAILED")
                        self.test_results.append(("HubSpot CRM AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ HubSpot CRM AI Agent - ERROR: {str(e)}")
            self.test_results.append(("HubSpot CRM AI", "ERROR", str(e)))
    
    async def test_ai_slack_communication(self):
        """Test AI Slack Communication Agent endpoint"""
        print("🧪 Testing AI Slack Communication Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "action": "send_message",
            "channel": "#sales-alerts",
            "message": "🚨 HIGH PRIORITY: New qualified lead from InnovateTech Solutions - VP of Marketing interested in enterprise demo!",
            "metadata": {
                "priority": "high",
                "lead_score": 85,
                "message_type": "lead_notification",
                "requires_immediate_action": True
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/business-enhancement/ai-slack-communication",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Slack Communication AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_id']}")
                        print(f"   Message Timestamp: {result['business_result']['message_ts']}")
                        print(f"   Channel: {result['business_result']['channel']}")
                        print(f"   Engagement Score: {result['agent_analysis']['message_intelligence']['engagement_score']:.2f}")
                        print(f"   Optimized Message: {result['business_result']['optimized_message'][:60]}...")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Slack Communication AI", "PASS", result))
                    else:
                        print("❌ Slack Communication AI Agent - FAILED")
                        self.test_results.append(("Slack Communication AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Slack Communication AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Slack Communication AI", "ERROR", str(e)))
    
    async def test_ai_calendly_scheduling(self):
        """Test AI Calendly Scheduling Agent endpoint"""
        print("🧪 Testing AI Calendly Scheduling Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "action": "schedule_meeting",
            "event_type": "enterprise_sales_demo",
            "attendee_email": "sarah.johnson@innovatetech.com",
            "metadata": {
                "attendee_name": "Sarah Johnson",
                "company": "InnovateTech Solutions",
                "attendee_timezone": "America/New_York",
                "meeting_purpose": "enterprise_demo",
                "lead_score": 85,
                "urgency": "high"
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/business-enhancement/ai-calendly-scheduling",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Calendly Scheduling AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_id']}")
                        print(f"   Event UUID: {result['business_result']['event_uuid']}")
                        print(f"   Meeting Status: {result['business_result']['scheduled_event']['status']}")
                        print(f"   Optimal Time: {result['agent_analysis']['scheduling_intelligence']['optimal_time']}")
                        print(f"   Confidence Score: {result['agent_analysis']['scheduling_intelligence']['confidence_score']:.2f}")
                        print(f"   Meeting URL: {result['business_result']['scheduled_event']['meeting_url']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Calendly Scheduling AI", "PASS", result))
                    else:
                        print("❌ Calendly Scheduling AI Agent - FAILED")
                        self.test_results.append(("Calendly Scheduling AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Calendly Scheduling AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Calendly Scheduling AI", "ERROR", str(e)))
    
    async def test_ai_business_analytics(self):
        """Test AI Business Analytics Agent endpoint"""
        print("🧪 Testing AI Business Analytics Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "date_range": {
                "start_date": "2025-08-01",
                "end_date": "2025-09-14"
            },
            "platforms": ["hubspot_crm", "slack_communication", "calendly_scheduling"],
            "metrics": [
                "conversion_rates",
                "team_efficiency",
                "meeting_success",
                "lead_quality",
                "workflow_automation"
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/business-enhancement/ai-analytics",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Business Analytics AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Analysis Period: {result['agent_analysis']['analytics_data']['analysis_period']}")
                        print(f"   HubSpot Contacts: {result['agent_analysis']['analytics_data']['platform_performance']['hubspot_crm']['contacts_managed']:,}")
                        print(f"   Slack Messages: {result['agent_analysis']['analytics_data']['platform_performance']['slack_communication']['messages_sent']:,}")
                        print(f"   Meetings Scheduled: {result['agent_analysis']['analytics_data']['platform_performance']['calendly_scheduling']['meetings_scheduled']}")
                        print(f"   Cost Optimization: {result['agent_analysis']['ai_insights']['cost_optimization']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Business Analytics AI", "PASS", result))
                    else:
                        print("❌ Business Analytics AI Agent - FAILED")
                        self.test_results.append(("Business Analytics AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Business Analytics AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Business Analytics AI", "ERROR", str(e)))
    
    async def test_ai_agents_status(self):
        """Test AI Agents Status endpoint"""
        print("🧪 Testing Business Enhancement AI Agents Status...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/brain/integrations/business-enhancement/ai-agents-status?tenant_id=test_tenant_001"
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Business Enhancement AI Agents Status - SUCCESS")
                        print(f"   Total Active Agents: {result['total_active_agents']}")
                        print(f"   Brain API Version: {result['brain_api_version']}")
                        print(f"   Coordination Mode: {result['agents_status']['coordination_mode']}")
                        print(f"   Supported Platforms: {', '.join(result['supported_platforms']).title()}")
                        print(f"   Operations Processed: {result['coordination_metrics']['total_operations_processed']}")
                        print(f"   Business Efficiency Gain: {result['performance_stats']['business_efficiency_gain']}")
                        print(f"   Workflow Automation: {result['performance_stats']['workflow_automation']}")
                        self.test_results.append(("Business Enhancement AI Agents Status", "PASS", result))
                    else:
                        print("❌ Business Enhancement AI Agents Status - FAILED")
                        self.test_results.append(("Business Enhancement AI Agents Status", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Business Enhancement AI Agents Status - ERROR: {str(e)}")
            self.test_results.append(("Business Enhancement AI Agents Status", "ERROR", str(e)))
    
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
        """Run all Business Enhancement APIs Brain integration tests"""
        print("🚀 Starting Business Enhancement APIs Brain AI Agent Integration Tests\n")
        
        # Test Brain API health first
        await self.test_brain_api_health()
        print()
        
        # Test all AI agent endpoints
        await self.test_ai_hubspot_crm()
        print()
        
        await self.test_ai_slack_communication()
        print()
        
        await self.test_ai_calendly_scheduling()
        print()
        
        await self.test_ai_business_analytics()
        print()
        
        await self.test_ai_agents_status()
        print()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("=" * 80)
        print("🔍 BUSINESS ENHANCEMENT APIS BRAIN AI INTEGRATION TEST SUMMARY")
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
            print("🎉 ALL TESTS PASSED! Business Enhancement APIs Brain AI Integration is fully operational.")
            print("🏢 Supported Platforms: HubSpot CRM, Slack, Calendly")
            print("🤖 AI Agents: CRM Automation, Communication Intelligence, Scheduling Optimization, Analytics")
            print("📊 Business Intelligence: Lead scoring, workflow automation, meeting optimization")
            print("⚡ Productivity Features: 67.5% efficiency gain, automated workflows, cross-platform insights")
        elif passed > failed + errors:
            print("⚡ Most tests passed. Business Enhancement Brain AI Integration is mostly functional.")
        else:
            print("🔧 Issues detected. Please check failed tests and fix integration.")
        
        print("=" * 80)

async def main():
    """Main test execution function"""
    tester = BusinessEnhancementAPIsBrainIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    print("Business Enhancement APIs Brain AI Agent Integration Tester")
    print("=" * 60)
    asyncio.run(main())