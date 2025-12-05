#!/usr/bin/env python3
"""
Test script for Communication APIs Brain AI Agent Coordination Integration

Tests all AI agent endpoints to ensure proper functionality:
- Voice Synthesis AI Agent (ElevenLabs)
- Speech Recognition AI Agent (Deepgram)  
- SMS Campaign AI Agent (Twilio)
- Voice Calls AI Agent (Twilio)
- Communication Analytics AI Agent
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class CommunicationAPIsBrainIntegrationTester:
    """Test class for Communication APIs Brain AI Agent Integration"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_ai_voice_synthesis(self):
        """Test AI Voice Synthesis Agent endpoint"""
        print("🧪 Testing AI Voice Synthesis Agent (ElevenLabs)...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "text": "Welcome to our AI-powered communication system. This is a premium voice synthesis demonstration using advanced neural networks.",
            "voice_id": "premium_voice_001",
            "model_id": "eleven_monolingual_v1",
            "stability": 0.7,
            "similarity_boost": 0.8,
            "style": 0.3,
            "use_speaker_boost": True,
            "output_format": "mp3_44100_192"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/communication-apis/ai-voice-synthesis",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Voice Synthesis AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Quality Score: {result['agent_analysis']['quality_score']}")
                        print(f"   Audio Duration: {result['agent_analysis']['synthesis_result']['audio_duration']}")
                        print(f"   Estimated Cost: {result['agent_analysis']['synthesis_result']['estimated_cost']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Voice Synthesis AI", "PASS", result))
                    else:
                        print("❌ Voice Synthesis AI Agent - FAILED")
                        self.test_results.append(("Voice Synthesis AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Voice Synthesis AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Voice Synthesis AI", "ERROR", str(e)))
    
    async def test_ai_speech_recognition(self):
        """Test AI Speech Recognition Agent endpoint"""
        print("🧪 Testing AI Speech Recognition Agent (Deepgram)...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "audio_url": "https://example.com/sample-audio-meeting.wav",
            "model": "nova-2",
            "language": "en-US",
            "detect_language": True,
            "punctuate": True,
            "diarize": True,
            "smart_format": True,
            "summarize": True,
            "detect_topics": True
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/communication-apis/ai-speech-recognition",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Speech Recognition AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Confidence Score: {result['agent_analysis']['confidence_score']}")
                        print(f"   Language Detected: {result['agent_analysis']['language_detected']}")
                        print(f"   Speakers Detected: {result['agent_analysis']['speakers_detected']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Speech Recognition AI", "PASS", result))
                    else:
                        print("❌ Speech Recognition AI Agent - FAILED")
                        self.test_results.append(("Speech Recognition AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Speech Recognition AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Speech Recognition AI", "ERROR", str(e)))
    
    async def test_ai_sms_campaign(self):
        """Test AI SMS Campaign Agent endpoint"""
        print("🧪 Testing AI SMS Campaign Agent (Twilio)...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "to_numbers": ["+1234567890", "+1987654321", "+1555123456"],
            "message": "🚀 Exciting news! Your AI-powered marketing campaign is ready. Click here to see your personalized results: https://example.com/results",
            "from_number": "+1555000000",
            "personalization": {
                "company": "TechCorp",
                "industry": "Technology"
            },
            "campaign_name": "AI Marketing Launch Campaign",
            "track_responses": True
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/communication-apis/ai-sms-campaign",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ SMS Campaign AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Messages Sent: {result['agent_analysis']['campaign_result']['messages_sent']}")
                        print(f"   Delivery Rate: {result['agent_analysis']['delivery_rate']}")
                        print(f"   Estimated Responses: {result['agent_analysis']['campaign_result']['estimated_responses']}")
                        print(f"   Total Cost: {result['agent_analysis']['campaign_result']['total_cost']}")
                        self.test_results.append(("SMS Campaign AI", "PASS", result))
                    else:
                        print("❌ SMS Campaign AI Agent - FAILED")
                        self.test_results.append(("SMS Campaign AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ SMS Campaign AI Agent - ERROR: {str(e)}")
            self.test_results.append(("SMS Campaign AI", "ERROR", str(e)))
    
    async def test_ai_voice_calls(self):
        """Test AI Voice Calls Agent endpoint"""
        print("🧪 Testing AI Voice Calls Agent (Twilio)...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "to_numbers": ["+1234567890", "+1987654321"],
            "voice_message": "Hello! This is an automated call from your AI marketing assistant. We have important updates about your campaign performance. Press 1 to hear more details or press 2 to schedule a callback.",
            "from_number": "+1555000000",
            "record_call": True,
            "gather_input": True,
            "max_call_duration": 180
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/communication-apis/ai-voice-calls",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Voice Calls AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Calls Attempted: {result['agent_analysis']['call_result']['calls_attempted']}")
                        print(f"   Connection Rate: {result['agent_analysis']['connection_rate']}")
                        print(f"   Average Duration: {result['agent_analysis']['call_result']['average_call_duration']}")
                        print(f"   Total Cost: {result['agent_analysis']['call_result']['total_cost']}")
                        self.test_results.append(("Voice Calls AI", "PASS", result))
                    else:
                        print("❌ Voice Calls AI Agent - FAILED")
                        self.test_results.append(("Voice Calls AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Voice Calls AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Voice Calls AI", "ERROR", str(e)))
    
    async def test_ai_communication_analytics(self):
        """Test AI Communication Analytics Agent endpoint"""
        print("🧪 Testing AI Communication Analytics Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "date_range": {
                "start_date": "2025-08-01",
                "end_date": "2025-09-14"
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/communication-apis/ai-analytics",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Communication Analytics AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Analysis Period: {result['agent_analysis']['analysis_period']}")
                        print(f"   ROI Percentage: {result['agent_analysis']['roi_analysis']['roi_percentage']}%")
                        print(f"   Total Investment: ${result['agent_analysis']['roi_analysis']['total_investment']}")
                        print(f"   Optimization Recommendations: {len(result['agent_analysis']['optimization_recommendations'])}")
                        self.test_results.append(("Communication Analytics AI", "PASS", result))
                    else:
                        print("❌ Communication Analytics AI Agent - FAILED")
                        self.test_results.append(("Communication Analytics AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Communication Analytics AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Communication Analytics AI", "ERROR", str(e)))
    
    async def test_ai_agents_status(self):
        """Test AI Agents Status endpoint"""
        print("🧪 Testing AI Agents Status...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/brain/integrations/communication-apis/ai-agents-status?tenant_id=test_tenant_001"
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
        """Run all Communication APIs Brain integration tests"""
        print("🚀 Starting Communication APIs Brain AI Agent Integration Tests\\n")
        
        # Test Brain API health first
        await self.test_brain_api_health()
        print()
        
        # Test all AI agent endpoints
        await self.test_ai_voice_synthesis()
        print()
        
        await self.test_ai_speech_recognition()
        print()
        
        await self.test_ai_sms_campaign()
        print()
        
        await self.test_ai_voice_calls()
        print()
        
        await self.test_ai_communication_analytics()
        print()
        
        await self.test_ai_agents_status()
        print()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("=" * 80)
        print("🔍 COMMUNICATION APIS BRAIN AI INTEGRATION TEST SUMMARY")
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
            print("🎉 ALL TESTS PASSED! Communication APIs Brain AI Integration is fully operational.")
            print("🎤 Supported Services: ElevenLabs, Deepgram, Twilio, Azure Speech, Google Speech")
            print("🤖 AI Agents: Voice Synthesis, Speech Recognition, SMS Campaigns, Voice Calls, Analytics")
        elif passed > failed + errors:
            print("⚡ Most tests passed. Brain AI Integration is mostly functional.")
        else:
            print("🔧 Issues detected. Please check failed tests and fix integration.")
        
        print("=" * 80)

async def main():
    """Main test execution function"""
    tester = CommunicationAPIsBrainIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    print("Communication APIs Brain AI Agent Integration Tester")
    print("=" * 60)
    asyncio.run(main())