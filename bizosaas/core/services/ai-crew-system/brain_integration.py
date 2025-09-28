"""
Brain API Integration Module

This module provides integration between the AI Crew System and the existing
BizOSaaS Brain API, enabling routing of crew tasks through the /api/brain/ endpoints.
"""

from typing import Dict, Any, List, Optional
import asyncio
import httpx
import logging
from datetime import datetime
from fastapi import FastAPI

from .crew_integration import CrewTaskRequest, CrewExecutionResult, crew_integration

logger = logging.getLogger(__name__)

class BrainAPIIntegration:
    """Integration with BizOSaaS Brain API"""
    
    def __init__(self, brain_api_url: str = "http://localhost:8001"):
        self.brain_api_url = brain_api_url.rstrip('/')
        self.client = None
        self.registered_routes = []
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.client = httpx.AsyncClient(timeout=30.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.aclose()
    
    async def register_crew_routes_with_brain(self) -> Dict[str, Any]:
        """Register crew system routes with the Brain API"""
        
        try:
            # Define crew routes to register
            crew_routes = [
                {
                    "path": "/api/brain/crew/execute",
                    "method": "POST",
                    "description": "Execute AI crew task with intelligent delegation",
                    "crew_system_endpoint": "/api/crew/execute",
                    "delegation_enabled": True
                },
                {
                    "path": "/api/brain/crew/crm/lead-scoring",
                    "method": "POST", 
                    "description": "CRM lead scoring and qualification",
                    "crew_system_endpoint": "/api/crew/crm/lead-scoring",
                    "domain": "crm"
                },
                {
                    "path": "/api/brain/crew/crm/customer-segmentation",
                    "method": "POST",
                    "description": "Customer segmentation analysis",
                    "crew_system_endpoint": "/api/crew/crm/customer-segmentation",
                    "domain": "crm"
                },
                {
                    "path": "/api/brain/crew/analytics/generate-report",
                    "method": "POST",
                    "description": "Generate intelligent analytics reports",
                    "crew_system_endpoint": "/api/crew/analytics/report-generation",
                    "domain": "analytics"
                },
                {
                    "path": "/api/brain/crew/status/{task_id}",
                    "method": "GET",
                    "description": "Get crew task execution status",
                    "crew_system_endpoint": "/api/crew/task/{task_id}",
                    "monitoring": True
                }
            ]
            
            # Register routes with Brain API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.brain_api_url}/api/brain/admin/register-crew-routes",
                    json={
                        "routes": crew_routes,
                        "crew_system_url": "http://ai-crew-system:8002",
                        "registration_timestamp": datetime.now().isoformat()
                    }
                )
                
                if response.status_code == 200:
                    self.registered_routes = crew_routes
                    logger.info("Successfully registered crew routes with Brain API")
                    return response.json()
                else:
                    logger.error(f"Failed to register routes: {response.status_code} - {response.text}")
                    return {"error": "Registration failed", "details": response.text}
        
        except Exception as e:
            logger.error(f"Route registration failed: {str(e)}")
            return {"error": str(e)}
    
    async def handle_brain_crew_request(
        self, 
        brain_request: Dict[str, Any], 
        route_path: str
    ) -> Dict[str, Any]:
        """Handle crew request routed from Brain API"""
        
        try:
            # Extract tenant information from Brain request
            tenant_id = brain_request.get("tenant_id", "default")
            user_id = brain_request.get("user_id")
            session_id = brain_request.get("session_id")
            
            # Determine task type based on route
            task_type = self._extract_task_type_from_route(route_path)
            
            # Create crew task request
            crew_request = CrewTaskRequest(
                type=task_type,
                description=brain_request.get("description", f"Brain routed task: {task_type}"),
                tenant_id=tenant_id,
                domain=brain_request.get("domain"),
                parameters=brain_request.get("parameters", {}),
                data_volume=brain_request.get("data_volume", 0),
                requires_ai=brain_request.get("requires_ai", True),  # Brain routes assume AI needed
                multi_domain=brain_request.get("multi_domain", False),
                priority=brain_request.get("priority", 5),
                timeout=brain_request.get("timeout", 300),
                user_id=user_id,
                session_id=session_id,
                metadata={
                    "brain_routed": True,
                    "original_route": route_path,
                    "brain_request_id": brain_request.get("request_id")
                }
            )
            
            # Execute crew task
            from fastapi import BackgroundTasks
            background_tasks = BackgroundTasks()
            
            result = await crew_integration.execute_crew_task(crew_request, background_tasks)
            
            # Format response for Brain API
            return {
                "status": "success",
                "crew_result": result.dict(),
                "brain_integration": {
                    "routed_from": route_path,
                    "task_type": task_type,
                    "execution_strategy": result.strategy_used,
                    "agents_used": result.agents_used
                }
            }
        
        except Exception as e:
            logger.error(f"Brain crew request handling failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "brain_integration": {
                    "routed_from": route_path,
                    "failed_at": "crew_execution"
                }
            }
    
    def _extract_task_type_from_route(self, route_path: str) -> str:
        """Extract task type from Brain API route"""
        
        route_mapping = {
            "/api/brain/crew/execute": "generic_crew_task",
            "/api/brain/crew/crm/lead-scoring": "crm_lead_scoring",
            "/api/brain/crew/crm/customer-segmentation": "crm_customer_segmentation",
            "/api/brain/crew/crm/nurturing-campaign": "crm_nurturing_campaign",
            "/api/brain/crew/crm/pipeline-optimization": "crm_pipeline_optimization",
            "/api/brain/crew/analytics/generate-report": "analytics_report_generation",
            "/api/brain/crew/analytics/insights": "analytics_insights_generation",
            "/api/brain/crew/ecommerce/inventory-optimization": "ecommerce_inventory_optimization",
            "/api/brain/crew/ecommerce/product-recommendations": "ecommerce_product_recommendations",
            "/api/brain/crew/billing/subscription-optimization": "billing_subscription_optimization",
            "/api/brain/crew/cms/content-optimization": "cms_content_optimization",
            "/api/brain/crew/integrations/sync-optimization": "integrations_sync_optimization"
        }
        
        return route_mapping.get(route_path, "unknown_crew_task")
    
    async def notify_brain_of_task_completion(
        self, 
        task_id: str, 
        result: CrewExecutionResult
    ):
        """Notify Brain API when a crew task completes"""
        
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{self.brain_api_url}/api/brain/notifications/crew-task-completed",
                    json={
                        "task_id": task_id,
                        "completion_time": datetime.now().isoformat(),
                        "status": result.status,
                        "execution_time": result.execution_time,
                        "strategy_used": result.strategy_used,
                        "agents_used": result.agents_used,
                        "success": result.status == "completed"
                    }
                )
                
                logger.info(f"Notified Brain API of task completion: {task_id}")
        
        except Exception as e:
            logger.error(f"Failed to notify Brain API: {str(e)}")
    
    async def sync_tenant_data_with_brain(self, tenant_id: str) -> Dict[str, Any]:
        """Sync tenant-specific data with Brain API"""
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.brain_api_url}/api/brain/tenants/{tenant_id}/data"
                )
                
                if response.status_code == 200:
                    tenant_data = response.json()
                    
                    # Extract relevant data for crew operations
                    return {
                        "tenant_id": tenant_id,
                        "subscription_tier": tenant_data.get("subscription_tier"),
                        "enabled_features": tenant_data.get("enabled_features", []),
                        "api_limits": tenant_data.get("api_limits", {}),
                        "preferences": tenant_data.get("preferences", {}),
                        "integration_settings": tenant_data.get("integrations", {})
                    }
                else:
                    logger.warning(f"Could not fetch tenant data: {response.status_code}")
                    return {"tenant_id": tenant_id, "error": "data_fetch_failed"}
        
        except Exception as e:
            logger.error(f"Tenant data sync failed: {str(e)}")
            return {"tenant_id": tenant_id, "error": str(e)}
    
    async def validate_brain_integration(self) -> Dict[str, Any]:
        """Validate integration with Brain API"""
        
        validation_results = {
            "brain_api_accessible": False,
            "routes_registered": False,
            "health_check": False,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Check Brain API accessibility
            async with httpx.AsyncClient() as client:
                health_response = await client.get(f"{self.brain_api_url}/api/brain/health")
                validation_results["brain_api_accessible"] = health_response.status_code == 200
                validation_results["brain_health"] = health_response.json() if health_response.status_code == 200 else None
        
        except Exception as e:
            validation_results["brain_api_error"] = str(e)
        
        try:
            # Check route registration
            if validation_results["brain_api_accessible"]:
                registration_result = await self.register_crew_routes_with_brain()
                validation_results["routes_registered"] = "error" not in registration_result
                validation_results["registration_details"] = registration_result
        
        except Exception as e:
            validation_results["registration_error"] = str(e)
        
        try:
            # Test crew integration
            test_request = {
                "type": "test_integration",
                "description": "Brain integration validation test",
                "tenant_id": "test_tenant",
                "requires_ai": False,
                "parameters": {"test": True}
            }
            
            integration_result = await self.handle_brain_crew_request(
                test_request, 
                "/api/brain/crew/execute"
            )
            
            validation_results["health_check"] = integration_result.get("status") == "success"
            validation_results["test_result"] = integration_result
        
        except Exception as e:
            validation_results["health_check_error"] = str(e)
        
        return validation_results

def create_brain_integration_routes(app: FastAPI, brain_integration: BrainAPIIntegration):
    """Add Brain integration routes to the crew system"""
    
    @app.post("/api/crew/brain/register-routes")
    async def register_routes_with_brain():
        """Register crew routes with Brain API"""
        result = await brain_integration.register_crew_routes_with_brain()
        return result
    
    @app.post("/api/crew/brain/handle-request")
    async def handle_brain_request(request_data: Dict[str, Any]):
        """Handle request routed from Brain API"""
        route_path = request_data.get("route_path", "/api/brain/crew/execute")
        result = await brain_integration.handle_brain_crew_request(request_data, route_path)
        return result
    
    @app.get("/api/crew/brain/validate-integration")
    async def validate_integration():
        """Validate Brain API integration"""
        result = await brain_integration.validate_brain_integration()
        return result
    
    @app.post("/api/crew/brain/sync-tenant/{tenant_id}")
    async def sync_tenant_data(tenant_id: str):
        """Sync tenant data with Brain API"""
        result = await brain_integration.sync_tenant_data_with_brain(tenant_id)
        return result

# Global brain integration instance
brain_integration = BrainAPIIntegration()

async def initialize_brain_integration(brain_api_url: str = None) -> Dict[str, Any]:
    """Initialize Brain API integration"""
    
    if brain_api_url:
        global brain_integration
        brain_integration = BrainAPIIntegration(brain_api_url)
    
    # Validate and register integration
    validation_result = await brain_integration.validate_brain_integration()
    
    logger.info(f"Brain integration initialized: {validation_result}")
    
    return validation_result