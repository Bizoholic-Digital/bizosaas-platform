#!/usr/bin/env python3
"""
Test script for Payment Processing APIs Brain AI Agent Coordination Integration

Tests all AI agent endpoints to ensure proper functionality:
- Stripe Payment AI Agent (Global payment processing with fraud detection)
- PayPal Payment AI Agent (Digital wallet optimization)  
- Razorpay Payment AI Agent (Indian market optimization with UPI/banking)
- Payment Analytics AI Agent (Cross-processor insights and optimization)
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class PaymentProcessingAPIsBrainIntegrationTester:
    """Test class for Payment Processing APIs Brain AI Agent Integration"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_ai_stripe_payment(self):
        """Test AI Stripe Payment Processing Agent endpoint"""
        print("🧪 Testing AI Stripe Payment Processing Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "amount": 299.99,
            "currency": "usd",
            "description": "Premium subscription payment - AI-powered business automation",
            "customer_id": "customer_stripe_12345",
            "payment_method": "card",
            "metadata": {
                "source": "web_checkout",
                "campaign": "premium_upgrade_2025",
                "ip_country": "US",
                "card_country": "US",
                "user_type": "returning"
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/payment-processing/ai-stripe-payment",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Stripe Payment AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_id']}")
                        print(f"   Payment Status: {result['payment_result']['status']}")
                        print(f"   Fraud Risk Score: {result['agent_analysis']['fraud_assessment']['risk_score']}")
                        print(f"   Processing Fee: ${result['payment_result']['fees']['stripe_fee']}")
                        print(f"   Net Amount: ${result['payment_result']['net_amount']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Stripe Payment AI", "PASS", result))
                    else:
                        print("❌ Stripe Payment AI Agent - FAILED")
                        self.test_results.append(("Stripe Payment AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Stripe Payment AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Stripe Payment AI", "ERROR", str(e)))
    
    async def test_ai_paypal_payment(self):
        """Test AI PayPal Payment Processing Agent endpoint"""
        print("🧪 Testing AI PayPal Payment Processing Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "amount": 149.50,
            "currency": "eur",
            "description": "CoreLDove e-commerce product purchase - AI-sourced premium item",
            "customer_id": "customer_paypal_67890",
            "payment_method": "paypal_wallet",
            "metadata": {
                "source": "mobile_app",
                "product_category": "electronics",
                "shipping_country": "DE",
                "payment_preference": "express_checkout"
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/payment-processing/ai-paypal-payment",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ PayPal Payment AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_id']}")
                        print(f"   Transaction ID: {result['payment_result']['id']}")
                        print(f"   Payment State: {result['payment_result']['state']}")
                        print(f"   Recommended Flow: {result['agent_analysis']['route_optimization']['recommended_flow']}")
                        print(f"   Processing Fee: ${result['payment_result']['fees']['paypal_fee']}")
                        print(f"   Net Amount: ${result['payment_result']['net_amount']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("PayPal Payment AI", "PASS", result))
                    else:
                        print("❌ PayPal Payment AI Agent - FAILED")
                        self.test_results.append(("PayPal Payment AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ PayPal Payment AI Agent - ERROR: {str(e)}")
            self.test_results.append(("PayPal Payment AI", "ERROR", str(e)))
    
    async def test_ai_razorpay_payment(self):
        """Test AI Razorpay Payment Processing Agent endpoint"""
        print("🧪 Testing AI Razorpay Payment Processing Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "amount": 1999.00,
            "currency": "inr",
            "description": "BizOSaaS subscription payment - AI marketing automation for Indian SMBs",
            "customer_id": "customer_india_54321",
            "payment_method": "upi",
            "metadata": {
                "source": "mobile_web",
                "region": "south_india",
                "business_type": "small_business",
                "preferred_upi_app": "gpay"
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/payment-processing/ai-razorpay-payment",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Razorpay Payment AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_id']}")
                        print(f"   Payment ID: {result['payment_result']['id']}")
                        print(f"   Payment Status: {result['payment_result']['status']}")
                        print(f"   Recommended Method: {result['agent_analysis']['method_recommendations']['primary_method']}")
                        print(f"   UPI VPA: {result['payment_result']['vpa']}")
                        print(f"   Processing Fee: ₹{result['payment_result']['fees']['razorpay_fee']}")
                        print(f"   Net Amount: ₹{result['payment_result']['net_amount']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Razorpay Payment AI", "PASS", result))
                    else:
                        print("❌ Razorpay Payment AI Agent - FAILED")
                        self.test_results.append(("Razorpay Payment AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Razorpay Payment AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Razorpay Payment AI", "ERROR", str(e)))
    
    async def test_ai_payment_analytics(self):
        """Test AI Payment Analytics Agent endpoint"""
        print("🧪 Testing AI Payment Analytics Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "date_range": {
                "start_date": "2025-08-01",
                "end_date": "2025-09-14"
            },
            "processors": ["stripe", "paypal", "razorpay"],
            "metrics": ["revenue", "transactions", "success_rates", "fees", "conversion"]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/payment-processing/ai-analytics",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Payment Analytics AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Analysis Period: {result['agent_analysis']['analytics_data']['analysis_period']}")
                        print(f"   Total Transactions: {result['agent_analysis']['analytics_data']['total_transactions']:,}")
                        print(f"   Total Revenue: ${result['agent_analysis']['analytics_data']['total_revenue']:,.2f}")
                        print(f"   Top Performer: {result['agent_analysis']['ai_insights']['top_performer'].title()}")
                        print(f"   Cost Leader: {result['agent_analysis']['ai_insights']['cost_leader'].title()}")
                        print(f"   Potential Savings: ${result['agent_analysis']['analytics_data']['cost_analysis']['potential_savings']:,.2f}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Payment Analytics AI", "PASS", result))
                    else:
                        print("❌ Payment Analytics AI Agent - FAILED")
                        self.test_results.append(("Payment Analytics AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Payment Analytics AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Payment Analytics AI", "ERROR", str(e)))
    
    async def test_ai_agents_status(self):
        """Test AI Agents Status endpoint"""
        print("🧪 Testing Payment Processing AI Agents Status...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/brain/integrations/payment-processing/ai-agents-status?tenant_id=test_tenant_001"
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Payment Processing AI Agents Status - SUCCESS")
                        print(f"   Total Active Agents: {result['total_active_agents']}")
                        print(f"   Brain API Version: {result['brain_api_version']}")
                        print(f"   Coordination Mode: {result['agents_status']['coordination_mode']}")
                        print(f"   Supported Processors: {', '.join(result['supported_processors']).title()}")
                        print(f"   Payments Processed: {result['coordination_metrics']['total_payments_processed']}")
                        print(f"   Success Rate Optimization: {result['performance_stats']['success_rate_optimization']}")
                        print(f"   Cost Optimization: {result['performance_stats']['cost_optimization']}")
                        self.test_results.append(("Payment AI Agents Status", "PASS", result))
                    else:
                        print("❌ Payment Processing AI Agents Status - FAILED")
                        self.test_results.append(("Payment AI Agents Status", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Payment Processing AI Agents Status - ERROR: {str(e)}")
            self.test_results.append(("Payment AI Agents Status", "ERROR", str(e)))
    
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
        """Run all Payment Processing APIs Brain integration tests"""
        print("🚀 Starting Payment Processing APIs Brain AI Agent Integration Tests\n")
        
        # Test Brain API health first
        await self.test_brain_api_health()
        print()
        
        # Test all AI agent endpoints
        await self.test_ai_stripe_payment()
        print()
        
        await self.test_ai_paypal_payment()
        print()
        
        await self.test_ai_razorpay_payment()
        print()
        
        await self.test_ai_payment_analytics()
        print()
        
        await self.test_ai_agents_status()
        print()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("=" * 80)
        print("🔍 PAYMENT PROCESSING APIS BRAIN AI INTEGRATION TEST SUMMARY")
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
                    agent_id = result['agent_analysis'].get('agent_id', 'N/A')
                    print(f"    Agent ID: {agent_id}")
                elif 'total_active_agents' in result:
                    agents_count = result.get('total_active_agents', 'N/A')
                    print(f"    Active Agents: {agents_count}")
        
        print("\n" + "=" * 80)
        
        if passed == len(self.test_results):
            print("🎉 ALL TESTS PASSED! Payment Processing APIs Brain AI Integration is fully operational.")
            print("💳 Supported Processors: Stripe, PayPal, Razorpay")
            print("🤖 AI Agents: Payment Processing, Fraud Detection, Analytics, Optimization")
            print("🌏 Market Coverage: Global (Stripe), Digital Wallets (PayPal), Indian Market (Razorpay)")
            print("🔒 Security Features: Fraud detection, compliance, secure processing")
        elif passed > failed + errors:
            print("⚡ Most tests passed. Payment Processing Brain AI Integration is mostly functional.")
        else:
            print("🔧 Issues detected. Please check failed tests and fix integration.")
        
        print("=" * 80)

async def main():
    """Main test execution function"""
    tester = PaymentProcessingAPIsBrainIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    print("Payment Processing APIs Brain AI Agent Integration Tester")
    print("=" * 60)
    asyncio.run(main())