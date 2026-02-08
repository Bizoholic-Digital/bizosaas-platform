#!/usr/bin/env python3
"""
Test script for Flipkart Seller API Brain AI Agent Coordination Integration

Tests all AI agent endpoints to ensure proper functionality:
- Product Listing AI Agent
- Price Optimization AI Agent
- Inventory Sync AI Agent  
- Order Processing AI Agent
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class FlipkartBrainIntegrationTester:
    """Test class for Flipkart Seller API Brain AI Agent Integration"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_ai_product_listing(self):
        """Test AI Product Listing Agent endpoint"""
        print("🧪 Testing AI Product Listing Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "products": [
                {
                    "seller_sku": "ELEC001",
                    "title": "Premium Wireless Earbuds",
                    "price": 2499.99,
                    "category": "Electronics"
                },
                {
                    "seller_sku": "ELEC002", 
                    "title": "Smart Fitness Tracker",
                    "price": 3999.99,
                    "category": "Fitness"
                }
            ],
            "category": "Electronics",
            "pricing_strategy": "competitive",
            "auto_optimize": True
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/flipkart-seller/ai-product-listing",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Product Listing AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Listing Recommendations: {len(result['agent_analysis']['listing_recommendations'])}")
                        print(f"   Market Opportunity Score: {result['agent_analysis']['market_opportunity_score']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Product Listing AI", "PASS", result))
                    else:
                        print("❌ Product Listing AI Agent - FAILED")
                        self.test_results.append(("Product Listing AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Product Listing AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Product Listing AI", "ERROR", str(e)))
    
    async def test_ai_price_optimization(self):
        """Test AI Price Optimization Agent endpoint"""
        print("🧪 Testing AI Price Optimization Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "seller_skus": ["ELEC001", "ELEC002", "ELEC003"],
            "strategy": "balanced",
            "competitor_analysis": True
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/flipkart-seller/ai-price-optimization",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Price Optimization AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Strategy: {result['agent_analysis']['strategy']}")
                        print(f"   Pricing Recommendations: {len(result['agent_analysis']['pricing_recommendations'])}")
                        print(f"   Revenue Projection: ₹{result['agent_analysis']['revenue_projection']['monthly_revenue_increase']}")
                        self.test_results.append(("Price Optimization AI", "PASS", result))
                    else:
                        print("❌ Price Optimization AI Agent - FAILED")
                        self.test_results.append(("Price Optimization AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Price Optimization AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Price Optimization AI", "ERROR", str(e)))
    
    async def test_ai_inventory_sync(self):
        """Test AI Inventory Sync Agent endpoint"""
        print("🧪 Testing AI Inventory Sync Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "warehouse_id": "primary_warehouse",
            "include_reserved": True,
            "sync_frequency": "real_time"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/flipkart-seller/ai-inventory-sync",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Inventory Sync AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Inventory Items: {len(result['agent_analysis']['inventory_status'])}")
                        print(f"   Optimization Recommendations: {len(result['agent_analysis']['optimization_recommendations'])}")
                        print(f"   Inventory Health Score: {result['agent_analysis']['inventory_health_score']['overall_score']}")
                        self.test_results.append(("Inventory Sync AI", "PASS", result))
                    else:
                        print("❌ Inventory Sync AI Agent - FAILED")
                        self.test_results.append(("Inventory Sync AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Inventory Sync AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Inventory Sync AI", "ERROR", str(e)))
    
    async def test_ai_order_processing(self):
        """Test AI Order Processing Agent endpoint"""
        print("🧪 Testing AI Order Processing Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "order_status": "APPROVED",
            "automation_level": "standard",
            "auto_shipping": True
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/flipkart-seller/ai-order-processing",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Order Processing AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Orders Processed: {result['agent_analysis']['order_processing_summary']['total_orders_processed']}")
                        print(f"   Automated Orders: {result['agent_analysis']['order_processing_summary']['automated_orders']}")
                        print(f"   Success Rate: {result['agent_analysis']['order_processing_summary']['success_rate']}%")
                        self.test_results.append(("Order Processing AI", "PASS", result))
                    else:
                        print("❌ Order Processing AI Agent - FAILED")
                        self.test_results.append(("Order Processing AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Order Processing AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Order Processing AI", "ERROR", str(e)))
    
    async def test_ai_agents_status(self):
        """Test AI Agents Status endpoint"""
        print("🧪 Testing AI Agents Status...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/brain/integrations/flipkart-seller/ai-agents-status?tenant_id=test_tenant_001"
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ AI Agents Status - SUCCESS")
                        print(f"   Total Active Agents: {result['total_active_agents']}")
                        print(f"   Brain API Version: {result['brain_api_version']}")
                        print(f"   Coordination Mode: {result['agents_status']['coordination_mode']}")
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
        """Run all Flipkart Seller API Brain integration tests"""
        print("🚀 Starting Flipkart Seller API Brain AI Agent Integration Tests\\n")
        
        # Test Brain API health first
        await self.test_brain_api_health()
        print()
        
        # Test all AI agent endpoints
        await self.test_ai_product_listing()
        print()
        
        await self.test_ai_price_optimization()
        print()
        
        await self.test_ai_inventory_sync()
        print()
        
        await self.test_ai_order_processing()
        print()
        
        await self.test_ai_agents_status()
        print()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("=" * 70)
        print("🔍 FLIPKART SELLER API BRAIN AI INTEGRATION TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for _, status, _ in self.test_results if status == "PASS")
        failed = sum(1 for _, status, _ in self.test_results if status == "FAIL") 
        errors = sum(1 for _, status, _ in self.test_results if status == "ERROR")
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Errors: {errors}")
        print(f"Success Rate: {(passed / len(self.test_results) * 100):.1f}%\\n")
        
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
        
        print("\\n" + "=" * 70)
        
        if passed == len(self.test_results):
            print("🎉 ALL TESTS PASSED! Flipkart Seller API Brain AI Integration is fully operational.")
        elif passed > failed + errors:
            print("⚡ Most tests passed. Brain AI Integration is mostly functional.")
        else:
            print("🔧 Issues detected. Please check failed tests and fix integration.")
        
        print("=" * 70)

async def main():
    """Main test execution function"""
    tester = FlipkartBrainIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    print("Flipkart Seller API Brain AI Agent Integration Tester")
    print("=" * 50)
    asyncio.run(main())