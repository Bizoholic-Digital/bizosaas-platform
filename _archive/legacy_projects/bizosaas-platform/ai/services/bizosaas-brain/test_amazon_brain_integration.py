#!/usr/bin/env python3
"""
Test script for Amazon SP-API Brain AI Agent Coordination Integration

Tests all AI agent endpoints to ensure proper functionality:
- Product Sourcing AI Agent
- Pricing Optimization AI Agent  
- Inventory Management AI Agent
- Order Automation AI Agent
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class AmazonBrainIntegrationTester:
    """Test class for Amazon SP-API Brain AI Agent Integration"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_ai_product_sourcing(self):
        """Test AI Product Sourcing Agent endpoint"""
        print("🧪 Testing AI Product Sourcing Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "marketplace_ids": ["ATVPDKIKX0DER", "A2EUQ1WTGCTBG2"],
            "budget_range": {"min": 100, "max": 2500},
            "target_margin": 30.0,
            "categories": ["Electronics", "Smart Home", "Fitness"]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-sp/ai-product-sourcing",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Product Sourcing AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Sourcing Recommendations: {len(result['agent_analysis']['sourcing_recommendations'])}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Product Sourcing AI", "PASS", result))
                    else:
                        print("❌ Product Sourcing AI Agent - FAILED")
                        self.test_results.append(("Product Sourcing AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Product Sourcing AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Product Sourcing AI", "ERROR", str(e)))
    
    async def test_ai_pricing_optimization(self):
        """Test AI Pricing Optimization Agent endpoint"""
        print("🧪 Testing AI Pricing Optimization Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "asins": ["B08N5WRWNW", "B07XJ8C8F5", "B094DBJLDS"],
            "strategy": "balanced"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-sp/ai-pricing-optimization",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Pricing Optimization AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Strategy: {result['agent_analysis']['strategy']}")
                        print(f"   Pricing Recommendations: {len(result['agent_analysis']['pricing_recommendations'])}")
                        self.test_results.append(("Pricing Optimization AI", "PASS", result))
                    else:
                        print("❌ Pricing Optimization AI Agent - FAILED")
                        self.test_results.append(("Pricing Optimization AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Pricing Optimization AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Pricing Optimization AI", "ERROR", str(e)))
    
    async def test_ai_inventory_management(self):
        """Test AI Inventory Management Agent endpoint"""
        print("🧪 Testing AI Inventory Management Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "marketplace_ids": ["ATVPDKIKX0DER", "A1F83G8C2ARO7P"],
            "include_fba": True
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-sp/ai-inventory-management",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Inventory Management AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Inventory Items: {len(result['agent_analysis']['inventory_status'])}")
                        print(f"   Reorder Recommendations: {len(result['agent_analysis']['reorder_recommendations'])}")
                        self.test_results.append(("Inventory Management AI", "PASS", result))
                    else:
                        print("❌ Inventory Management AI Agent - FAILED")
                        self.test_results.append(("Inventory Management AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Inventory Management AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Inventory Management AI", "ERROR", str(e)))
    
    async def test_ai_order_automation(self):
        """Test AI Order Automation Agent endpoint"""
        print("🧪 Testing AI Order Automation Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "filters": {"status": "Unshipped"},
            "automation_level": "standard"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-sp/ai-order-automation",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Order Automation AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Orders Processed: {result['agent_analysis']['order_processing_summary']['total_orders_processed']}")
                        print(f"   Automation Level: {result['agent_analysis']['automation_level']}")
                        self.test_results.append(("Order Automation AI", "PASS", result))
                    else:
                        print("❌ Order Automation AI Agent - FAILED")
                        self.test_results.append(("Order Automation AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Order Automation AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Order Automation AI", "ERROR", str(e)))
    
    async def test_ai_agents_status(self):
        """Test AI Agents Status endpoint"""
        print("🧪 Testing AI Agents Status...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/brain/integrations/amazon-sp/ai-agents-status?tenant_id=test_tenant_001"
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ AI Agents Status - SUCCESS")
                        print(f"   Total Active Agents: {result['total_active_agents']}")
                        print(f"   Brain API Version: {result['brain_api_version']}")
                        print(f"   Coordination Mode: {result['agents_status']['coordination_mode']}")
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
        """Run all Amazon SP-API Brain integration tests"""
        print("🚀 Starting Amazon SP-API Brain AI Agent Integration Tests\n")
        
        # Test Brain API health first
        await self.test_brain_api_health()
        print()
        
        # Test all AI agent endpoints
        await self.test_ai_product_sourcing()
        print()
        
        await self.test_ai_pricing_optimization()
        print()
        
        await self.test_ai_inventory_management()
        print()
        
        await self.test_ai_order_automation()
        print()
        
        await self.test_ai_agents_status()
        print()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("=" * 70)
        print("🔍 AMAZON SP-API BRAIN AI INTEGRATION TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for _, status, _ in self.test_results if status == "PASS")
        failed = sum(1 for _, status, _ in self.test_results if status == "FAIL") 
        errors = sum(1 for _, status, _ in self.test_results if status == "ERROR")
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Errors: {errors}")
        print(f"Success Rate: {(passed / len(self.test_results) * 100):.1f}%\n")
        
        print("Detailed Results:")
        print("-" * 50)
        
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
        
        print("\n" + "=" * 70)
        
        if passed == len(self.test_results):
            print("🎉 ALL TESTS PASSED! Amazon SP-API Brain AI Integration is fully operational.")
        elif passed > failed + errors:
            print("⚡ Most tests passed. Brain AI Integration is mostly functional.")
        else:
            print("🔧 Issues detected. Please check failed tests and fix integration.")
        
        print("=" * 70)

async def main():
    """Main test execution function"""
    tester = AmazonBrainIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    print("Amazon SP-API Brain AI Agent Integration Tester")
    print("=" * 50)
    asyncio.run(main())