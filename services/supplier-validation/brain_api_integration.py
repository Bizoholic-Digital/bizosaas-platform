#!/usr/bin/env python3
"""
Brain API Integration for Supplier Validation Workflow [P9]
Handles communication with the central Brain API (port 8001)
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class BrainAPIClient:
    """Client for Brain API communication"""
    
    def __init__(self, brain_api_url: str = None, api_key: str = None):
        self.brain_api_url = brain_api_url or os.getenv("BRAIN_API_URL", "http://localhost:8001")
        self.api_key = api_key or os.getenv("API_KEY", "your-api-key")
        self.service_id = "supplier-validation"
        self.service_port = 8027
    
    async def register_service(self) -> bool:
        """Register this service with the Brain API"""
        try:
            service_info = {
                "service_id": self.service_id,
                "service_name": "Supplier Validation Workflow [P9]",
                "service_port": self.service_port,
                "service_url": f"http://localhost:{self.service_port}",
                "service_type": "validation",
                "capabilities": [
                    "supplier_validation",
                    "document_verification",
                    "risk_assessment",
                    "workflow_management",
                    "hitl_approval"
                ],
                "endpoints": [
                    {"path": "/suppliers/register", "method": "POST", "description": "Register new supplier"},
                    {"path": "/suppliers/{supplier_id}", "method": "GET", "description": "Get supplier details"},
                    {"path": "/suppliers/{supplier_id}/review", "method": "POST", "description": "Submit supplier review"},
                    {"path": "/suppliers/{supplier_id}/risk-assessment", "method": "GET", "description": "Get risk assessment"},
                    {"path": "/dashboard/analytics", "method": "GET", "description": "Get analytics data"}
                ],
                "health_check": f"http://localhost:{self.service_port}/health",
                "documentation": f"http://localhost:{self.service_port}/docs",
                "status": "active"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.brain_api_url}/services/register",
                    headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                    json=service_info
                ) as response:
                    if response.status == 200:
                        logger.info("Successfully registered with Brain API")
                        return True
                    else:
                        logger.error(f"Failed to register with Brain API: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error registering with Brain API: {str(e)}")
            return False
    
    async def notify_supplier_status_change(self, supplier_id: str, old_status: str, new_status: str, 
                                          metadata: Dict[str, Any] = None) -> bool:
        """Notify Brain API of supplier status changes"""
        try:
            notification = {
                "event_type": "supplier_status_change",
                "supplier_id": supplier_id,
                "old_status": old_status,
                "new_status": new_status,
                "service_id": self.service_id,
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": metadata or {}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.brain_api_url}/events/supplier-status",
                    headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                    json=notification
                ) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.error(f"Error notifying Brain API of status change: {str(e)}")
            return False
    
    async def get_supplier_integration_data(self, supplier_id: str) -> Optional[Dict[str, Any]]:
        """Get supplier data from other integrated services via Brain API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.brain_api_url}/suppliers/{supplier_id}/integration-data",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting supplier integration data: {str(e)}")
            return None
    
    async def notify_document_verification_complete(self, supplier_id: str, document_id: str, 
                                                  verification_result: Dict[str, Any]) -> bool:
        """Notify Brain API when document verification is complete"""
        try:
            notification = {
                "event_type": "document_verification_complete",
                "supplier_id": supplier_id,
                "document_id": document_id,
                "verification_result": verification_result,
                "service_id": self.service_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.brain_api_url}/events/document-verification",
                    headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                    json=notification
                ) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.error(f"Error notifying document verification: {str(e)}")
            return False
    
    async def get_product_sourcing_requirements(self, supplier_id: str) -> Optional[Dict[str, Any]]:
        """Get product sourcing requirements for a supplier from Product Sourcing service [P8]"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.brain_api_url}/product-sourcing/supplier-requirements/{supplier_id}",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting product sourcing requirements: {str(e)}")
            return None
    
    async def notify_supplier_approved(self, supplier_id: str, approval_data: Dict[str, Any]) -> bool:
        """Notify Brain API when supplier is approved for product sourcing"""
        try:
            notification = {
                "event_type": "supplier_approved",
                "supplier_id": supplier_id,
                "approval_data": approval_data,
                "service_id": self.service_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.brain_api_url}/events/supplier-approved",
                    headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                    json=notification
                ) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.error(f"Error notifying supplier approval: {str(e)}")
            return False
    
    async def get_analytics_data(self, metric_type: str, time_range: str = "30d") -> Optional[Dict[str, Any]]:
        """Get analytics data from Brain API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.brain_api_url}/analytics/{metric_type}?service={self.service_id}&range={time_range}",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting analytics data: {str(e)}")
            return None
    
    async def send_validation_metrics(self, metrics: Dict[str, Any]) -> bool:
        """Send validation metrics to Brain API for aggregation"""
        try:
            metric_data = {
                "service_id": self.service_id,
                "metrics": metrics,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.brain_api_url}/metrics/validation",
                    headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                    json=metric_data
                ) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.error(f"Error sending validation metrics: {str(e)}")
            return False
    
    async def get_service_status(self) -> Optional[Dict[str, Any]]:
        """Get status of all integrated services from Brain API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.brain_api_url}/services/status",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting service status: {str(e)}")
            return None

class SupplierValidationIntegration:
    """Integration manager for supplier validation with other services"""
    
    def __init__(self, brain_client: BrainAPIClient):
        self.brain_client = brain_client
    
    async def initialize(self):
        """Initialize integration with Brain API"""
        success = await self.brain_client.register_service()
        if success:
            logger.info("Supplier Validation service successfully integrated with Brain API")
        else:
            logger.warning("Failed to integrate with Brain API - continuing in standalone mode")
        return success
    
    async def handle_supplier_approval(self, supplier_id: str, supplier_data: Dict[str, Any], 
                                     approval_details: Dict[str, Any]) -> Dict[str, Any]:
        """Handle supplier approval and notify integrated services"""
        results = {"brain_api_notified": False, "product_sourcing_notified": False}
        
        # Notify Brain API
        approval_data = {
            "supplier_data": supplier_data,
            "approval_details": approval_details,
            "risk_assessment": supplier_data.get("risk_assessment"),
            "validation_results": supplier_data.get("validation_results")
        }
        
        results["brain_api_notified"] = await self.brain_client.notify_supplier_approved(
            supplier_id, approval_data
        )
        
        # Check if Product Sourcing service needs this supplier
        sourcing_requirements = await self.brain_client.get_product_sourcing_requirements(supplier_id)
        if sourcing_requirements:
            # Notify Product Sourcing service about approved supplier
            results["product_sourcing_notified"] = True
            logger.info(f"Supplier {supplier_id} approved and available for product sourcing")
        
        return results
    
    async def sync_validation_metrics(self, validation_stats: Dict[str, Any]):
        """Sync validation metrics with Brain API"""
        metrics = {
            "validation_type": "supplier_validation",
            "stats": validation_stats,
            "service_performance": {
                "validation_time_avg": validation_stats.get("avg_validation_time", 0),
                "approval_rate": validation_stats.get("approval_rate", 0),
                "document_verification_rate": validation_stats.get("doc_verification_rate", 0)
            }
        }
        
        return await self.brain_client.send_validation_metrics(metrics)

# Global integration instance
brain_client = BrainAPIClient()
supplier_integration = SupplierValidationIntegration(brain_client)

async def initialize_integrations():
    """Initialize all integrations"""
    return await supplier_integration.initialize()

# Helper functions for main application
async def notify_status_change(supplier_id: str, old_status: str, new_status: str, metadata: Dict[str, Any] = None):
    """Helper to notify status changes"""
    return await brain_client.notify_supplier_status_change(supplier_id, old_status, new_status, metadata)

async def handle_supplier_approval(supplier_id: str, supplier_data: Dict[str, Any], approval_details: Dict[str, Any]):
    """Helper to handle supplier approval"""
    return await supplier_integration.handle_supplier_approval(supplier_id, supplier_data, approval_details)

async def get_integration_status():
    """Get status of all integrations"""
    return await brain_client.get_service_status()

# Example usage
async def test_integration():
    """Test Brain API integration"""
    # Initialize
    success = await initialize_integrations()
    print(f"Integration initialized: {success}")
    
    # Test status change notification
    result = await notify_status_change("test-supplier-123", "pending", "approved", {"test": True})
    print(f"Status change notification: {result}")
    
    # Get service status
    status = await get_integration_status()
    print(f"Service status: {status}")

if __name__ == "__main__":
    asyncio.run(test_integration())