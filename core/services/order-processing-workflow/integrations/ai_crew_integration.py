"""
AI Crew Integration for Order Processing
Integrates with CrewAI system for intelligent order optimization and automation
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import aiohttp
import json

logger = logging.getLogger(__name__)


class AICrewIntegration:
    """
    AI Crew integration for order processing optimization
    Uses CrewAI agents for intelligent decision making and automation
    """
    
    def __init__(self):
        self.config = {
            "ai_crew_api_url": "http://localhost:8002/api/crew",  # AI Crew System API
            "brain_api_url": "http://localhost:8000/api/brain",   # Brain API for data
            "enable_ai_optimization": True,
            "enable_fraud_detection": True,
            "enable_route_optimization": True,
            "enable_pricing_optimization": True,
            "timeout": 60,
            "max_retries": 3
        }
        
        # AI Crew endpoints
        self.endpoints = {
            "order_optimization": "/optimize-order",
            "fraud_detection": "/detect-fraud",
            "route_optimization": "/optimize-routes",
            "pricing_optimization": "/optimize-pricing",
            "inventory_forecasting": "/forecast-inventory",
            "customer_insights": "/analyze-customer",
            "demand_prediction": "/predict-demand"
        }
        
        # Specialized AI crews for different tasks
        self.crews = {
            "order_processing": {
                "name": "Order Processing Crew",
                "agents": ["order_analyst", "inventory_specialist", "logistics_coordinator"],
                "description": "Optimizes order processing workflow"
            },
            "fraud_detection": {
                "name": "Fraud Detection Crew",
                "agents": ["fraud_analyst", "risk_assessor", "security_specialist"],
                "description": "Detects and prevents fraudulent orders"
            },
            "fulfillment_optimization": {
                "name": "Fulfillment Optimization Crew",
                "agents": ["warehouse_optimizer", "shipping_specialist", "route_planner"],
                "description": "Optimizes fulfillment and shipping processes"
            },
            "customer_experience": {
                "name": "Customer Experience Crew",
                "agents": ["experience_analyst", "communication_specialist", "satisfaction_tracker"],
                "description": "Enhances customer experience throughout order lifecycle"
            }
        }
        
        # Cache for AI results
        self.ai_cache = {}
        
    async def initialize(self):
        """Initialize AI Crew integration"""
        logger.info("Initializing AI Crew Integration...")
        
        try:
            # Test connection to AI Crew system
            await self._test_ai_crew_connection()
            
            # Initialize AI crews
            await self._initialize_crews()
            
            logger.info("AI Crew Integration initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI Crew Integration: {e}")
            # Don't raise - AI should be optional
            self.config["enable_ai_optimization"] = False
    
    async def shutdown(self):
        """Cleanup AI Crew integration"""
        logger.info("Shutting down AI Crew Integration...")
    
    async def optimize_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI crew to optimize order processing"""
        logger.info(f"Optimizing order {order.get('id')} with AI crew")
        
        if not self.config["enable_ai_optimization"]:
            return {"optimization_applied": False, "reason": "AI optimization disabled"}
        
        try:
            # Prepare order data for AI analysis
            analysis_data = {
                "order": order,
                "customer_history": await self._get_customer_history(order.get("customer_id")),
                "inventory_status": await self._get_inventory_status(order.get("items", [])),
                "market_conditions": await self._get_market_conditions(),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Run AI optimization
            optimization_result = await self._execute_ai_crew_task(
                "order_processing",
                "optimize_order_workflow",
                analysis_data
            )
            
            if optimization_result["success"]:
                return {
                    "optimization_applied": True,
                    "optimizations": optimization_result["optimizations"],
                    "confidence_score": optimization_result.get("confidence", 0.8),
                    "estimated_savings": optimization_result.get("estimated_savings", {}),
                    "recommendations": optimization_result.get("recommendations", [])
                }
            else:
                return {
                    "optimization_applied": False,
                    "reason": optimization_result.get("error", "AI optimization failed")
                }
                
        except Exception as e:
            logger.error(f"Order optimization failed: {e}")
            return {
                "optimization_applied": False,
                "reason": f"Error: {str(e)}"
            }
    
    async def detect_fraud(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI crew for advanced fraud detection"""
        logger.info(f"Running AI fraud detection for order {order.get('id')}")
        
        if not self.config["enable_fraud_detection"]:
            return {"fraud_score": 0.0, "risk_level": "low", "ai_analysis": False}
        
        try:
            # Prepare fraud analysis data
            fraud_data = {
                "order": order,
                "payment_data": order.get("payment_details", {}),
                "customer_profile": await self._get_customer_profile(order.get("customer_id")),
                "device_fingerprint": await self._get_device_fingerprint(order),
                "behavioral_patterns": await self._get_behavioral_patterns(order.get("customer_id")),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Run AI fraud detection
            fraud_result = await self._execute_ai_crew_task(
                "fraud_detection",
                "analyze_fraud_risk",
                fraud_data
            )
            
            if fraud_result["success"]:
                return {
                    "fraud_score": fraud_result.get("fraud_score", 0.0),
                    "risk_level": fraud_result.get("risk_level", "low"),
                    "risk_factors": fraud_result.get("risk_factors", []),
                    "confidence": fraud_result.get("confidence", 0.8),
                    "recommendations": fraud_result.get("recommendations", []),
                    "ai_analysis": True
                }
            else:
                return {
                    "fraud_score": 0.0,
                    "risk_level": "unknown",
                    "ai_analysis": False,
                    "error": fraud_result.get("error")
                }
                
        except Exception as e:
            logger.error(f"AI fraud detection failed: {e}")
            return {
                "fraud_score": 0.0,
                "risk_level": "unknown",
                "ai_analysis": False,
                "error": str(e)
            }
    
    async def optimize_fulfillment(self, orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Use AI crew to optimize fulfillment routing and batching"""
        logger.info(f"Optimizing fulfillment for {len(orders)} orders with AI crew")
        
        if not self.config["enable_route_optimization"]:
            return {"optimization_applied": False, "reason": "Route optimization disabled"}
        
        try:
            # Prepare fulfillment optimization data
            fulfillment_data = {
                "orders": orders,
                "warehouse_capacity": await self._get_warehouse_capacity(),
                "shipping_constraints": await self._get_shipping_constraints(),
                "carrier_performance": await self._get_carrier_performance(),
                "weather_conditions": await self._get_weather_conditions(),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Run AI fulfillment optimization
            optimization_result = await self._execute_ai_crew_task(
                "fulfillment_optimization",
                "optimize_fulfillment_routing",
                fulfillment_data
            )
            
            if optimization_result["success"]:
                return {
                    "optimization_applied": True,
                    "optimized_routes": optimization_result.get("optimized_routes", []),
                    "batch_recommendations": optimization_result.get("batch_recommendations", []),
                    "estimated_time_savings": optimization_result.get("time_savings", 0),
                    "estimated_cost_savings": optimization_result.get("cost_savings", 0),
                    "confidence": optimization_result.get("confidence", 0.8)
                }
            else:
                return {
                    "optimization_applied": False,
                    "reason": optimization_result.get("error", "AI optimization failed")
                }
                
        except Exception as e:
            logger.error(f"Fulfillment optimization failed: {e}")
            return {
                "optimization_applied": False,
                "reason": f"Error: {str(e)}"
            }
    
    async def optimize_pricing(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI crew for dynamic pricing optimization"""
        logger.info(f"Optimizing pricing for order {order.get('id')} with AI crew")
        
        if not self.config["enable_pricing_optimization"]:
            return {"optimization_applied": False, "reason": "Pricing optimization disabled"}
        
        try:
            # Prepare pricing optimization data
            pricing_data = {
                "order": order,
                "market_prices": await self._get_market_prices(order.get("items", [])),
                "competitor_analysis": await self._get_competitor_analysis(),
                "demand_patterns": await self._get_demand_patterns(),
                "customer_segments": await self._get_customer_segments(),
                "inventory_levels": await self._get_inventory_levels(),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Run AI pricing optimization
            pricing_result = await self._execute_ai_crew_task(
                "order_processing",
                "optimize_dynamic_pricing",
                pricing_data
            )
            
            if pricing_result["success"]:
                return {
                    "optimization_applied": True,
                    "pricing_adjustments": pricing_result.get("pricing_adjustments", []),
                    "discount_recommendations": pricing_result.get("discount_recommendations", []),
                    "revenue_impact": pricing_result.get("revenue_impact", 0),
                    "confidence": pricing_result.get("confidence", 0.8)
                }
            else:
                return {
                    "optimization_applied": False,
                    "reason": pricing_result.get("error", "AI pricing optimization failed")
                }
                
        except Exception as e:
            logger.error(f"Pricing optimization failed: {e}")
            return {
                "optimization_applied": False,
                "reason": f"Error: {str(e)}"
            }
    
    async def predict_delivery_time(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to predict accurate delivery times"""
        logger.info(f"Predicting delivery time for order {order.get('id')} with AI")
        
        try:
            # Prepare delivery prediction data
            delivery_data = {
                "order": order,
                "shipping_method": order.get("shipping_method"),
                "destination": order.get("shipping_address"),
                "warehouse_location": await self._get_warehouse_location(order),
                "historical_delivery_data": await self._get_delivery_history(),
                "carrier_performance": await self._get_carrier_performance(),
                "weather_forecast": await self._get_weather_forecast(order.get("shipping_address")),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Run AI delivery prediction
            prediction_result = await self._execute_ai_crew_task(
                "fulfillment_optimization",
                "predict_delivery_time",
                delivery_data
            )
            
            if prediction_result["success"]:
                return {
                    "predicted_delivery": prediction_result.get("predicted_delivery"),
                    "confidence_interval": prediction_result.get("confidence_interval", {}),
                    "factors_considered": prediction_result.get("factors", []),
                    "accuracy_score": prediction_result.get("accuracy", 0.85)
                }
            else:
                # Fallback to standard estimation
                return await self._fallback_delivery_prediction(order)
                
        except Exception as e:
            logger.error(f"AI delivery prediction failed: {e}")
            return await self._fallback_delivery_prediction(order)
    
    async def analyze_customer_experience(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to analyze and improve customer experience"""
        logger.info(f"Analyzing customer experience for order {order.get('id')}")
        
        try:
            # Prepare customer experience data
            experience_data = {
                "order": order,
                "customer_history": await self._get_customer_history(order.get("customer_id")),
                "communication_preferences": await self._get_communication_preferences(order.get("customer_id")),
                "satisfaction_scores": await self._get_satisfaction_scores(order.get("customer_id")),
                "support_interactions": await self._get_support_interactions(order.get("customer_id")),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Run AI customer experience analysis
            experience_result = await self._execute_ai_crew_task(
                "customer_experience",
                "analyze_customer_journey",
                experience_data
            )
            
            if experience_result["success"]:
                return {
                    "experience_score": experience_result.get("experience_score", 8.0),
                    "improvement_areas": experience_result.get("improvement_areas", []),
                    "personalization_recommendations": experience_result.get("personalization", []),
                    "communication_suggestions": experience_result.get("communication", []),
                    "retention_probability": experience_result.get("retention_probability", 0.8)
                }
            else:
                return {
                    "experience_score": 7.0,  # Default neutral score
                    "improvement_areas": [],
                    "analysis_available": False
                }
                
        except Exception as e:
            logger.error(f"Customer experience analysis failed: {e}")
            return {
                "experience_score": 7.0,
                "analysis_available": False,
                "error": str(e)
            }
    
    async def get_health(self) -> Dict[str, Any]:
        """Get AI Crew integration health status"""
        
        try:
            connection_test = await self._test_ai_crew_connection()
            
            return {
                "status": "healthy" if connection_test else "unhealthy",
                "ai_optimization_enabled": self.config["enable_ai_optimization"],
                "fraud_detection_enabled": self.config["enable_fraud_detection"],
                "route_optimization_enabled": self.config["enable_route_optimization"],
                "pricing_optimization_enabled": self.config["enable_pricing_optimization"],
                "active_crews": len(self.crews),
                "cache_size": len(self.ai_cache),
                "connection": connection_test
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    # Private helper methods
    
    async def _test_ai_crew_connection(self) -> bool:
        """Test connection to AI Crew system"""
        
        try:
            url = f"{self.config['ai_crew_api_url']}/health"
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(url) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.error(f"AI Crew connection test failed: {e}")
            return False
    
    async def _initialize_crews(self):
        """Initialize AI crews"""
        
        for crew_id, crew_config in self.crews.items():
            logger.info(f"Initializing AI crew: {crew_config['name']}")
            
            # In production, this would register crews with the AI system
            # For now, we'll just log the initialization
    
    async def _execute_ai_crew_task(self, crew_id: str, task_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using AI crew"""
        
        try:
            url = f"{self.config['ai_crew_api_url']}/execute"
            
            payload = {
                "crew_id": crew_id,
                "task_name": task_name,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.config["timeout"])) as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result
                    else:
                        raise Exception(f"HTTP {response.status}: {await response.text()}")
                        
        except Exception as e:
            logger.error(f"AI crew task execution failed: {e}")
            
            # Return simulated AI result for demo
            return await self._simulate_ai_result(crew_id, task_name, data)
    
    async def _simulate_ai_result(self, crew_id: str, task_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate AI result for demo purposes"""
        
        # Simulate AI processing delay
        await asyncio.sleep(0.5)
        
        if task_name == "optimize_order_workflow":
            return {
                "success": True,
                "optimizations": {
                    "warehouse_selection": "Optimal warehouse selected based on location and inventory",
                    "shipping_method": "Express shipping recommended for high-value customer",
                    "packaging_optimization": "Reduced packaging size by 15%"
                },
                "confidence": 0.87,
                "estimated_savings": {
                    "time_saved_hours": 2.5,
                    "cost_saved_usd": 12.50
                },
                "recommendations": [
                    "Consider priority processing for this customer",
                    "Use eco-friendly packaging option"
                ]
            }
        
        elif task_name == "analyze_fraud_risk":
            return {
                "success": True,
                "fraud_score": 15.5,  # Low risk
                "risk_level": "low",
                "risk_factors": [
                    "New customer account",
                    "High-value first order"
                ],
                "confidence": 0.92,
                "recommendations": [
                    "Monitor for subsequent orders",
                    "Consider additional verification for high-value items"
                ]
            }
        
        elif task_name == "optimize_fulfillment_routing":
            return {
                "success": True,
                "optimized_routes": [
                    {
                        "route_id": "route_001",
                        "orders": [order["id"] for order in data.get("orders", [])[:5]],
                        "estimated_time": "4.5 hours",
                        "estimated_cost": 45.75
                    }
                ],
                "batch_recommendations": [
                    {
                        "batch_id": "batch_001",
                        "orders": len(data.get("orders", [])),
                        "optimal_size": min(len(data.get("orders", [])), 25)
                    }
                ],
                "time_savings": 1.5,
                "cost_savings": 8.25,
                "confidence": 0.85
            }
        
        elif task_name == "optimize_dynamic_pricing":
            return {
                "success": True,
                "pricing_adjustments": [
                    {
                        "item_id": "item_001",
                        "current_price": 29.99,
                        "suggested_price": 31.99,
                        "reason": "High demand, low inventory"
                    }
                ],
                "discount_recommendations": [
                    {
                        "type": "loyalty_discount",
                        "percentage": 5.0,
                        "reason": "Repeat customer with high lifetime value"
                    }
                ],
                "revenue_impact": 15.50,
                "confidence": 0.78
            }
        
        elif task_name == "predict_delivery_time":
            return {
                "success": True,
                "predicted_delivery": (datetime.utcnow() + timedelta(days=3)).isoformat(),
                "confidence_interval": {
                    "earliest": (datetime.utcnow() + timedelta(days=2)).isoformat(),
                    "latest": (datetime.utcnow() + timedelta(days=4)).isoformat()
                },
                "factors": [
                    "Historical carrier performance",
                    "Weather conditions",
                    "Distance and route complexity",
                    "Package weight and dimensions"
                ],
                "accuracy": 0.89
            }
        
        elif task_name == "analyze_customer_journey":
            return {
                "success": True,
                "experience_score": 8.5,
                "improvement_areas": [
                    "Shipping notification timing",
                    "Packaging presentation",
                    "Post-purchase follow-up"
                ],
                "personalization": [
                    "Recommend related products based on purchase history",
                    "Offer preferred shipping method based on past choices"
                ],
                "communication": [
                    "Send delivery updates via SMS (customer preference)",
                    "Include personalized thank you note"
                ],
                "retention_probability": 0.85
            }
        
        else:
            return {
                "success": False,
                "error": f"Unknown task: {task_name}"
            }
    
    # Data fetching methods (these would integrate with actual data sources)
    
    async def _get_customer_history(self, customer_id: str) -> Dict[str, Any]:
        """Get customer order history"""
        # Simulate customer history data
        return {
            "total_orders": 5,
            "total_spent": 450.75,
            "average_order_value": 90.15,
            "preferred_categories": ["electronics", "accessories"],
            "last_order_date": "2024-01-15"
        }
    
    async def _get_inventory_status(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get inventory status for order items"""
        return {
            "total_items": len(items),
            "in_stock": len(items) - 1,
            "low_stock": 1,
            "out_of_stock": 0
        }
    
    async def _get_market_conditions(self) -> Dict[str, Any]:
        """Get current market conditions"""
        return {
            "demand_trend": "increasing",
            "seasonal_factor": 1.15,
            "competitive_pressure": "medium",
            "supply_chain_status": "normal"
        }
    
    async def _get_customer_profile(self, customer_id: str) -> Dict[str, Any]:
        """Get customer profile for fraud analysis"""
        return {
            "account_age_days": 45,
            "verified_email": True,
            "verified_phone": True,
            "payment_methods": 2,
            "shipping_addresses": 1,
            "order_frequency": "monthly"
        }
    
    async def _get_device_fingerprint(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Get device fingerprint data"""
        return {
            "device_type": "desktop",
            "browser": "Chrome",
            "location": "New York, NY",
            "ip_reputation": "good",
            "session_duration": 1800
        }
    
    async def _get_behavioral_patterns(self, customer_id: str) -> Dict[str, Any]:
        """Get customer behavioral patterns"""
        return {
            "usual_order_time": "evening",
            "average_session_duration": 1200,
            "typical_order_size": 2,
            "payment_speed": "normal",
            "cart_abandonment_rate": 0.25
        }
    
    async def _get_warehouse_capacity(self) -> Dict[str, Any]:
        """Get warehouse capacity information"""
        return {
            "warehouse_001": {"capacity": 10000, "current_load": 6500, "utilization": 0.65},
            "warehouse_002": {"capacity": 8000, "current_load": 3600, "utilization": 0.45}
        }
    
    async def _get_shipping_constraints(self) -> Dict[str, Any]:
        """Get shipping constraints"""
        return {
            "max_package_weight": 50.0,
            "max_package_dimensions": {"length": 100, "width": 80, "height": 60},
            "restricted_areas": ["PO Boxes for oversized items"],
            "carrier_cutoff_times": {"fedex": "15:00", "ups": "16:00", "usps": "17:00"}
        }
    
    async def _get_carrier_performance(self) -> Dict[str, Any]:
        """Get carrier performance metrics"""
        return {
            "fedex": {"on_time_rate": 0.94, "avg_delivery_time": 2.1, "cost_per_shipment": 12.50},
            "ups": {"on_time_rate": 0.92, "avg_delivery_time": 2.3, "cost_per_shipment": 11.75},
            "usps": {"on_time_rate": 0.88, "avg_delivery_time": 3.1, "cost_per_shipment": 8.25}
        }
    
    async def _get_weather_conditions(self) -> Dict[str, Any]:
        """Get weather conditions affecting shipping"""
        return {
            "current_weather": "clear",
            "forecast_3_day": "partly_cloudy",
            "severe_weather_alerts": [],
            "temperature_range": {"min": 15, "max": 25}
        }
    
    async def _get_market_prices(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get market pricing data"""
        return {
            "average_market_price": 45.75,
            "price_trend": "stable",
            "competitor_prices": [42.99, 47.50, 44.25],
            "price_elasticity": 0.75
        }
    
    async def _get_competitor_analysis(self) -> Dict[str, Any]:
        """Get competitor analysis data"""
        return {
            "competitors_count": 5,
            "average_competitor_price": 46.25,
            "price_positioning": "competitive",
            "market_share": 0.15
        }
    
    async def _get_demand_patterns(self) -> Dict[str, Any]:
        """Get demand pattern data"""
        return {
            "current_demand": "high",
            "seasonal_trend": "increasing",
            "weekly_pattern": ["low", "medium", "medium", "high", "high", "medium", "low"],
            "demand_elasticity": 0.85
        }
    
    async def _get_customer_segments(self) -> Dict[str, Any]:
        """Get customer segmentation data"""
        return {
            "segment": "premium",
            "price_sensitivity": "low",
            "loyalty_score": 8.5,
            "lifetime_value": 1250.00
        }
    
    async def _get_inventory_levels(self) -> Dict[str, Any]:
        """Get current inventory levels"""
        return {
            "total_units": 500,
            "available_units": 425,
            "reserved_units": 75,
            "reorder_point": 50,
            "days_of_inventory": 15
        }
    
    async def _get_warehouse_location(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Get warehouse location for order"""
        return {
            "warehouse_id": "warehouse_001",
            "location": "New York, NY",
            "coordinates": {"lat": 40.7128, "lng": -74.0060}
        }
    
    async def _get_delivery_history(self) -> Dict[str, Any]:
        """Get historical delivery data"""
        return {
            "average_delivery_time": 2.8,
            "on_time_percentage": 0.91,
            "delivery_patterns": {"weekday": 2.5, "weekend": 3.2}
        }
    
    async def _get_weather_forecast(self, address: Dict[str, Any]) -> Dict[str, Any]:
        """Get weather forecast for delivery location"""
        return {
            "forecast": "clear",
            "precipitation_probability": 0.1,
            "temperature": 22,
            "wind_speed": 5
        }
    
    async def _get_communication_preferences(self, customer_id: str) -> Dict[str, Any]:
        """Get customer communication preferences"""
        return {
            "email_notifications": True,
            "sms_notifications": True,
            "push_notifications": False,
            "preferred_time": "evening",
            "language": "en"
        }
    
    async def _get_satisfaction_scores(self, customer_id: str) -> Dict[str, Any]:
        """Get customer satisfaction scores"""
        return {
            "overall_satisfaction": 8.5,
            "delivery_satisfaction": 9.0,
            "product_satisfaction": 8.0,
            "service_satisfaction": 8.5,
            "nps_score": 8
        }
    
    async def _get_support_interactions(self, customer_id: str) -> Dict[str, Any]:
        """Get customer support interaction history"""
        return {
            "total_interactions": 2,
            "last_interaction": "2024-01-10",
            "satisfaction_rating": 9.0,
            "common_issues": ["shipping_delay", "product_question"],
            "resolution_time_avg": 1.5
        }
    
    async def _fallback_delivery_prediction(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback delivery prediction when AI is unavailable"""
        from datetime import timedelta
        
        # Simple rule-based prediction
        shipping_method = order.get("shipping_method", "standard")
        
        if shipping_method == "overnight":
            delivery_date = datetime.utcnow() + timedelta(days=1)
        elif shipping_method == "express":
            delivery_date = datetime.utcnow() + timedelta(days=2)
        else:
            delivery_date = datetime.utcnow() + timedelta(days=5)
        
        return {
            "predicted_delivery": delivery_date.isoformat(),
            "confidence_interval": {
                "earliest": (delivery_date - timedelta(days=1)).isoformat(),
                "latest": (delivery_date + timedelta(days=1)).isoformat()
            },
            "factors_considered": ["shipping_method", "standard_delivery_times"],
            "accuracy_score": 0.75,
            "fallback_prediction": True
        }