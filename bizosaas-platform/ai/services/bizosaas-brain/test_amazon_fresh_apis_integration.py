#!/usr/bin/env python3
"""
Test script for Amazon Fresh APIs Brain AI Agent Coordination Integration

Tests all AI agent endpoints to ensure proper functionality:
- Fresh Delivery Management AI Agent (Route optimization and delivery scheduling)
- Fresh Inventory Management AI Agent (Expiry tracking and stock optimization)
- Fresh Customer Experience AI Agent (Preference learning and satisfaction optimization)
- Fresh Market Analytics AI Agent (Demand forecasting and market trend analysis)
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class AmazonFreshAPIsBrainIntegrationTester:
    """Test class for Amazon Fresh APIs Brain AI Agent Integration"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_ai_delivery_management(self):
        """Test AI Fresh Delivery Management Agent endpoint"""
        print("🧪 Testing AI Fresh Delivery Management Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "delivery_requests": [
                {
                    "delivery_id": "fresh_delivery_001",
                    "customer_id": "customer_12345",
                    "address": {
                        "street": "123 Fresh Avenue",
                        "city": "Seattle",
                        "state": "WA",
                        "zip": "98101",
                        "coordinates": {"lat": 47.6062, "lng": -122.3321}
                    },
                    "time_window": {
                        "preferred_time": "14:00",
                        "window": "13:30-14:30"
                    },
                    "items": [
                        {
                            "product_id": "fresh_salmon_001",
                            "name": "Fresh Atlantic Salmon",
                            "quantity": 2,
                            "weight": "1.5 lbs",
                            "temperature_control": "refrigerated"
                        },
                        {
                            "product_id": "organic_spinach_001", 
                            "name": "Organic Baby Spinach",
                            "quantity": 1,
                            "weight": "0.5 lbs",
                            "temperature_control": "fresh_produce"
                        }
                    ],
                    "special_instructions": "Leave at door, ring doorbell",
                    "delivery_type": "two_hour"
                },
                {
                    "delivery_id": "fresh_delivery_002",
                    "customer_id": "customer_67890",
                    "address": {
                        "street": "456 Grocery Lane",
                        "city": "Seattle",
                        "state": "WA", 
                        "zip": "98105",
                        "coordinates": {"lat": 47.6205, "lng": -122.3493}
                    },
                    "time_window": {
                        "preferred_time": "16:00",
                        "window": "15:30-16:30"
                    },
                    "items": [
                        {
                            "product_id": "greek_yogurt_001",
                            "name": "Greek Yogurt Variety Pack",
                            "quantity": 2,
                            "weight": "2.0 lbs",
                            "temperature_control": "refrigerated"
                        },
                        {
                            "product_id": "frozen_berries_001",
                            "name": "Frozen Mixed Berries",
                            "quantity": 1,
                            "weight": "1.0 lbs", 
                            "temperature_control": "frozen"
                        }
                    ],
                    "special_instructions": "Contactless delivery preferred",
                    "delivery_type": "same_day"
                }
            ],
            "optimization_goals": [
                "minimize_delivery_time",
                "reduce_fuel_consumption",
                "maximize_freshness_preservation"
            ],
            "delivery_region": "seattle_metro"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-fresh/ai-delivery-management",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Fresh Delivery Management AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Routes Optimized: {result['agent_analysis']['delivery_optimization']['total_routes_optimized']}")
                        print(f"   Distance Saved: {result['agent_analysis']['delivery_optimization']['efficiency_improvements']['total_distance_saved_km']} km")
                        print(f"   Time Saved: {result['agent_analysis']['delivery_optimization']['efficiency_improvements']['estimated_time_saved_minutes']} minutes")
                        print(f"   On-time Rate: {result['agent_analysis']['delivery_optimization']['delivery_performance']['on_time_delivery_rate']}%")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Fresh Delivery Management AI", "PASS", result))
                    else:
                        print("❌ Fresh Delivery Management AI Agent - FAILED")
                        self.test_results.append(("Fresh Delivery Management AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Fresh Delivery Management AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Fresh Delivery Management AI", "ERROR", str(e)))
    
    async def test_ai_inventory_management(self):
        """Test AI Fresh Inventory Management Agent endpoint"""
        print("🧪 Testing AI Fresh Inventory Management Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "current_stock": [
                {
                    "product_id": "organic_bananas_001",
                    "name": "Organic Bananas",
                    "category": "produce",
                    "stock": 45,
                    "optimal": 65,
                    "freshness": "premium_fresh",
                    "expiry_days": 3,
                    "supplier": "organic_farms_001",
                    "harvest_date": "2025-09-12"
                },
                {
                    "product_id": "fresh_salmon_001", 
                    "name": "Fresh Atlantic Salmon",
                    "category": "seafood",
                    "stock": 12,
                    "optimal": 25,
                    "freshness": "ultra_fresh",
                    "expiry_days": 1,
                    "supplier": "coastal_fisheries_001",
                    "harvest_date": "2025-09-13"
                },
                {
                    "product_id": "organic_milk_001",
                    "name": "Organic Whole Milk",
                    "category": "dairy",
                    "stock": 38,
                    "optimal": 50,
                    "freshness": "standard_fresh",
                    "expiry_days": 7,
                    "supplier": "organic_dairy_001"
                },
                {
                    "product_id": "artisan_bread_001",
                    "name": "Artisan Sourdough Bread",
                    "category": "bakery",
                    "stock": 8,
                    "optimal": 20,
                    "freshness": "best_by_soon",
                    "expiry_days": 2,
                    "supplier": "local_bakery_001",
                    "baked_date": "2025-09-12"
                }
            ],
            "warehouse_conditions": {
                "temperature_zones": {
                    "frozen": {"temperature": -18, "humidity": 65},
                    "refrigerated": {"temperature": 3, "humidity": 80},
                    "fresh_produce": {"temperature": 10, "humidity": 85},
                    "ambient": {"temperature": 20, "humidity": 60}
                }
            },
            "demand_patterns": {
                "seasonal_factors": ["fall_produce", "holiday_baking"],
                "promotional_impact": "back_to_school_season"
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-fresh/ai-inventory-management",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Fresh Inventory Management AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Products Analyzed: {result['agent_analysis']['inventory_optimization']['total_products_analyzed']}")
                        print(f"   Freshness Score: {result['agent_analysis']['inventory_optimization']['inventory_health']['overall_freshness_score']}")
                        print(f"   Expiry Alerts: {result['agent_analysis']['inventory_optimization']['expiry_management']['total_alerts']}")
                        print(f"   Restock Needed: {result['agent_analysis']['inventory_optimization']['restock_planning']['total_restock_needed']}")
                        print(f"   Waste Reduction: {result['agent_analysis']['inventory_optimization']['inventory_health']['waste_reduction_potential']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Fresh Inventory Management AI", "PASS", result))
                    else:
                        print("❌ Fresh Inventory Management AI Agent - FAILED")
                        self.test_results.append(("Fresh Inventory Management AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Fresh Inventory Management AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Fresh Inventory Management AI", "ERROR", str(e)))
    
    async def test_ai_customer_experience(self):
        """Test AI Fresh Customer Experience Agent endpoint"""
        print("🧪 Testing AI Fresh Customer Experience Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "customers": [
                {
                    "customer_id": "customer_12345",
                    "name": "Sarah Johnson",
                    "level": "prime",
                    "history": 18,
                    "order_history": [
                        {
                            "date": "2025-09-10",
                            "items": ["organic_vegetables", "fresh_fish", "dairy"],
                            "value": 67.50,
                            "delivery_rating": 5
                        },
                        {
                            "date": "2025-09-03",
                            "items": ["produce", "meat", "bakery"],
                            "value": 85.25,
                            "delivery_rating": 4
                        }
                    ],
                    "preferences": {
                        "organic_priority": True,
                        "local_sourced": True,
                        "dietary_restrictions": ["gluten_free"],
                        "delivery_window": "17:00-19:00"
                    },
                    "instructions": "Leave at door, text when delivered"
                },
                {
                    "customer_id": "customer_67890",
                    "name": "Mike Chen",
                    "level": "prime",
                    "history": 24,
                    "order_history": [
                        {
                            "date": "2025-09-11",
                            "items": ["frozen_meals", "beverages", "snacks"],
                            "value": 42.99,
                            "delivery_rating": 5
                        },
                        {
                            "date": "2025-09-08",
                            "items": ["dairy", "meat", "produce"],
                            "value": 73.45,
                            "delivery_rating": 4
                        }
                    ],
                    "preferences": {
                        "organic_priority": False,
                        "convenience_focus": True,
                        "dietary_restrictions": [],
                        "delivery_window": "14:00-16:00"
                    },
                    "instructions": "Contactless delivery, ring doorbell"
                },
                {
                    "customer_id": "customer_11111",
                    "name": "Emily Davis",
                    "level": "prime_plus",
                    "history": 36,
                    "order_history": [
                        {
                            "date": "2025-09-12",
                            "items": ["premium_organic", "artisan_cheese", "wine"],
                            "value": 124.75,
                            "delivery_rating": 5
                        }
                    ],
                    "preferences": {
                        "organic_priority": True,
                        "premium_products": True,
                        "local_sourced": True,
                        "delivery_window": "10:00-12:00"
                    },
                    "instructions": "Please inspect produce quality before delivery"
                }
            ],
            "satisfaction_metrics": {
                "overall_rating": 4.6,
                "delivery_satisfaction": 4.7,
                "product_quality": 4.5,
                "customer_service": 4.8
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-fresh/ai-customer-experience",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Fresh Customer Experience AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Customers Analyzed: {result['agent_analysis']['customer_analysis']['total_customers_analyzed']}")
                        print(f"   Average Satisfaction: {result['agent_analysis']['customer_analysis']['experience_metrics']['average_satisfaction']}")
                        print(f"   Retention Rate: {result['agent_analysis']['customer_analysis']['experience_metrics']['retention_rate']}%")
                        print(f"   Recommendation Accuracy: {result['agent_analysis']['customer_analysis']['experience_metrics']['recommendation_accuracy']}%")
                        print(f"   Organic Preference: {result['agent_analysis']['customer_analysis']['behavioral_insights']['organic_preference_rate']}")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Fresh Customer Experience AI", "PASS", result))
                    else:
                        print("❌ Fresh Customer Experience AI Agent - FAILED")
                        self.test_results.append(("Fresh Customer Experience AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Fresh Customer Experience AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Fresh Customer Experience AI", "ERROR", str(e)))
    
    async def test_ai_market_analytics(self):
        """Test AI Fresh Market Analytics Agent endpoint"""
        print("🧪 Testing AI Fresh Market Analytics Agent...")
        
        payload = {
            "tenant_id": "test_tenant_001",
            "regions": ["US", "CA", "UK"],
            "analysis_period": {
                "start_date": "2025-08-01",
                "end_date": "2025-09-14"
            },
            "market_segments": [
                "fresh_produce",
                "organic_foods", 
                "seafood_meat",
                "dairy_products",
                "bakery_items"
            ],
            "competitive_data": {
                "major_competitors": ["Whole Foods", "Safeway", "Local Grocers"],
                "market_dynamics": "increasing_health_consciousness"
            },
            "seasonal_factors": [
                "back_to_school_season",
                "fall_harvest_season",
                "holiday_preparation"
            ],
            "consumer_trends": [
                "organic_preference_growth",
                "convenience_delivery_demand",
                "local_sourcing_priority",
                "sustainability_focus"
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/brain/integrations/amazon-fresh/ai-market-analytics",
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print("✅ Fresh Market Analytics AI Agent - SUCCESS")
                        print(f"   Agent ID: {result['agent_analysis']['agent_id']}")
                        print(f"   Regions Analyzed: {result['agent_analysis']['market_analysis']['regions_analyzed']}")
                        print(f"   Fastest Growing Region: {result['agent_analysis']['market_analysis']['cross_regional_insights']['fastest_growing_region']}")
                        print(f"   Largest Market: {result['agent_analysis']['market_analysis']['cross_regional_insights']['largest_market']}")
                        print(f"   Organic Leader: {result['agent_analysis']['market_analysis']['cross_regional_insights']['organic_adoption_leader']}")
                        print(f"   Forecast Accuracy: {result['agent_analysis']['forecast_accuracy']}%")
                        print(f"   Processing Time: {result['processing_time']}")
                        self.test_results.append(("Fresh Market Analytics AI", "PASS", result))
                    else:
                        print("❌ Fresh Market Analytics AI Agent - FAILED")
                        self.test_results.append(("Fresh Market Analytics AI", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Fresh Market Analytics AI Agent - ERROR: {str(e)}")
            self.test_results.append(("Fresh Market Analytics AI", "ERROR", str(e)))
    
    async def test_ai_agents_status(self):
        """Test AI Agents Status endpoint"""
        print("🧪 Testing AI Agents Status endpoint...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/brain/integrations/amazon-fresh/ai-agents-status?tenant_id=test_tenant_001"
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('integration_status') == 'active':
                        print("✅ Amazon Fresh AI Agents Status - SUCCESS")
                        print(f"   Integration Status: {result['integration_status']}")
                        print(f"   Delivery Agent: {result['ai_agents']['delivery_management']['status']}")
                        print(f"   Inventory Agent: {result['ai_agents']['inventory_management']['status']}")
                        print(f"   Customer Agent: {result['ai_agents']['customer_experience']['status']}")
                        print(f"   Analytics Agent: {result['ai_agents']['market_analytics']['status']}")
                        print(f"   Total Deliveries Today: {result['fresh_metrics']['total_deliveries_today']}")
                        print(f"   Freshness Guarantee Rate: {result['fresh_metrics']['freshness_guarantee_rate']}%")
                        self.test_results.append(("Amazon Fresh AI Agents Status", "PASS", result))
                    else:
                        print("❌ Amazon Fresh AI Agents Status - FAILED")
                        self.test_results.append(("Amazon Fresh AI Agents Status", "FAIL", result))
                        
        except Exception as e:
            print(f"❌ Amazon Fresh AI Agents Status - ERROR: {str(e)}")
            self.test_results.append(("Amazon Fresh AI Agents Status", "ERROR", str(e)))
    
    async def run_comprehensive_test(self):
        """Run all Amazon Fresh API Brain integration tests"""
        print("🚀 Starting Amazon Fresh APIs Brain AI Agent Integration Tests")
        print("=" * 80)
        
        # Test all endpoints
        await self.test_ai_delivery_management()
        print("-" * 80)
        
        await self.test_ai_inventory_management()
        print("-" * 80)
        
        await self.test_ai_customer_experience()
        print("-" * 80)
        
        await self.test_ai_market_analytics()
        print("-" * 80)
        
        await self.test_ai_agents_status()
        print("-" * 80)
        
        # Print comprehensive results
        await self.print_test_summary()
    
    async def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("\n📊 AMAZON FRESH APIs BRAIN INTEGRATION TEST SUMMARY")
        print("=" * 80)
        
        passed = len([t for t in self.test_results if t[1] == "PASS"])
        failed = len([t for t in self.test_results if t[1] == "FAIL"])
        errors = len([t for t in self.test_results if t[1] == "ERROR"])
        total = len(self.test_results)
        
        print(f"📈 Test Results Overview:")
        print(f"   ✅ Passed: {passed}/{total}")
        print(f"   ❌ Failed: {failed}/{total}")
        print(f"   💥 Errors: {errors}/{total}")
        print(f"   📊 Success Rate: {(passed/total)*100:.1f}%")
        
        print(f"\n🔍 Detailed Results:")
        for test_name, status, result in self.test_results:
            status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "💥"
            print(f"   {status_emoji} {test_name}: {status}")
        
        print(f"\n🎯 Amazon Fresh AI Agent Performance:")
        if passed > 0:
            print("   🧠 Fresh Delivery Management: Route optimization and delivery scheduling")
            print("   📦 Fresh Inventory Management: Expiry tracking and stock optimization")
            print("   👤 Fresh Customer Experience: Preference learning and satisfaction optimization")
            print("   📈 Fresh Market Analytics: Demand forecasting and trend analysis")
        
        print("\n🏆 Integration Status: All AI agents coordinating Amazon Fresh operations through Brain API Gateway")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - Amazon Fresh Brain Integration is fully operational!")
        elif passed > total * 0.7:
            print("⚠️ MOSTLY SUCCESSFUL - Some issues need attention")
        else:
            print("🚨 CRITICAL ISSUES - Integration needs immediate attention")
        
        print("=" * 80)

async def main():
    """Run Amazon Fresh APIs Brain integration tests"""
    tester = AmazonFreshAPIsBrainIntegrationTester()
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())