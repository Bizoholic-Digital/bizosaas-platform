"""
CrewAI Integration Layer for BizOSaaS Platform

This module provides integration between the AI Crew System and the existing
FastAPI Brain routing system, enabling seamless crew orchestration through
the /api/brain/ endpoints.
"""

from typing import Dict, Any, List, Optional, Union
from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import asyncio
import logging
from datetime import datetime
import httpx

from .crew_orchestrator import (
    CrewOrchestrator, 
    TaskRequest, 
    TaskResponse, 
    crew_orchestrator
)
from .smart_delegation import smart_delegation_engine
from .agent_hierarchy import agent_hierarchy
from .performance_monitor import CrewPerformanceMonitor

logger = logging.getLogger(__name__)

class CrewTaskRequest(BaseModel):
    """Extended task request for crew operations"""
    # Core task data
    type: str
    description: str
    tenant_id: str
    
    # Optional parameters
    domain: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    data_volume: int = 0
    requires_ai: bool = False
    multi_domain: bool = False
    priority: int = 5
    timeout: int = 300
    
    # Crew-specific options
    preferred_strategy: Optional[str] = None
    force_crew: bool = False
    async_execution: bool = False
    callback_url: Optional[str] = None
    
    # Metadata
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class CrewExecutionResult(BaseModel):
    """Result of crew execution"""
    task_id: str
    workflow_id: str
    status: str
    strategy_used: str
    execution_type: str
    execution_time: float
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    agents_used: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)

class CrewSystemStatus(BaseModel):
    """System status response"""
    status: str
    timestamp: str
    orchestrator: Dict[str, Any]
    delegation_engine: Dict[str, Any]
    agent_hierarchy: Dict[str, Any]
    performance: Dict[str, Any]

class CrewAIIntegration:
    """Main integration class for CrewAI system"""
    
    def __init__(self):
        self.orchestrator = crew_orchestrator
        self.delegation_engine = smart_delegation_engine
        self.hierarchy = agent_hierarchy
        self.performance_monitor = CrewPerformanceMonitor()
        self.async_tasks: Dict[str, asyncio.Task] = {}
    
    async def execute_crew_task(
        self, 
        request: CrewTaskRequest,
        background_tasks: BackgroundTasks
    ) -> CrewExecutionResult:
        """Execute a task using the crew system"""
        
        try:
            # Convert to internal task request
            task_request = TaskRequest(
                tenant_id=request.tenant_id,
                type=request.type,
                description=request.description,
                domain=request.domain,
                parameters=request.parameters,
                data_volume=request.data_volume,
                requires_ai=request.requires_ai or request.force_crew,
                multi_domain=request.multi_domain,
                priority=request.priority,
                timeout=request.timeout,
                preferred_strategy=request.preferred_strategy,
                callback_url=request.callback_url,
                metadata={
                    **request.metadata,
                    "user_id": request.user_id,
                    "session_id": request.session_id
                }
            )
            
            # Execute synchronously or asynchronously
            if request.async_execution:
                # Start background task
                task = asyncio.create_task(
                    self._execute_async_task(task_request, request.callback_url)
                )
                self.async_tasks[task_request.id] = task
                
                return CrewExecutionResult(
                    task_id=task_request.id,
                    workflow_id="pending",
                    status="accepted",
                    strategy_used="async",
                    execution_type="background",
                    execution_time=0.0,
                    result={"message": "Task accepted for async execution"},
                    metrics={"async": True}
                )
            else:
                # Execute synchronously
                response = await self.orchestrator.execute_task(task_request)
                
                # Add performance monitoring
                background_tasks.add_task(
                    self.performance_monitor.record_execution,
                    response
                )
                
                return self._convert_response(response)
        
        except Exception as e:
            logger.error(f"Crew task execution failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _execute_async_task(
        self, 
        task_request: TaskRequest, 
        callback_url: Optional[str]
    ):
        """Execute task asynchronously with callback"""
        
        try:
            response = await self.orchestrator.execute_task(task_request)
            
            # Record performance
            await self.performance_monitor.record_execution(response)
            
            # Send callback if provided
            if callback_url:
                await self._send_callback(callback_url, response)
        
        except Exception as e:
            logger.error(f"Async task execution failed: {str(e)}")
            
            # Send error callback
            if callback_url:
                error_response = TaskResponse(
                    task_id=task_request.id,
                    workflow_id="unknown",
                    status="failed",
                    strategy_used="unknown",
                    execution_time=0.0,
                    error=str(e)
                )
                await self._send_callback(callback_url, error_response)
        
        finally:
            # Clean up task reference
            if task_request.id in self.async_tasks:
                del self.async_tasks[task_request.id]
    
    async def _send_callback(self, callback_url: str, response: TaskResponse):
        """Send callback to specified URL"""
        
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    callback_url,
                    json=response.dict(),
                    timeout=10.0
                )
                logger.info(f"Callback sent to {callback_url}")
        
        except Exception as e:
            logger.error(f"Failed to send callback to {callback_url}: {str(e)}")
    
    def _convert_response(self, response: TaskResponse) -> CrewExecutionResult:
        """Convert internal response to API response"""
        
        # Generate recommendations based on execution
        recommendations = self._generate_recommendations(response)
        
        return CrewExecutionResult(
            task_id=response.task_id,
            workflow_id=response.workflow_id,
            status=response.status,
            strategy_used=response.strategy_used,
            execution_type=response.metrics.get("execution_type", "unknown"),
            execution_time=response.execution_time,
            result=response.result,
            error=response.error,
            agents_used=response.agents_used,
            metrics=response.metrics,
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, response: TaskResponse) -> List[str]:
        """Generate recommendations based on execution results"""
        
        recommendations = []
        
        # Performance-based recommendations
        if response.execution_time > 60:
            recommendations.append(
                "Consider breaking down complex tasks into smaller components"
            )
        
        if response.strategy_used == "crew_workflow" and response.execution_time < 10:
            recommendations.append(
                "Task may be suitable for simpler execution strategy"
            )
        
        # Error-based recommendations
        if response.error:
            if "timeout" in response.error.lower():
                recommendations.append("Increase task timeout for better reliability")
            elif "agent" in response.error.lower():
                recommendations.append("Check agent availability and configuration")
        
        # Success-based recommendations
        if response.status == "completed" and len(response.agents_used) > 3:
            recommendations.append(
                "Task successfully coordinated multiple agents - consider similar decomposition for related tasks"
            )
        
        return recommendations
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        
        # Check async tasks first
        if task_id in self.async_tasks:
            task = self.async_tasks[task_id]
            return {
                "task_id": task_id,
                "status": "running" if not task.done() else "completed",
                "is_async": True
            }
        
        # Check workflow history
        for workflow in self.orchestrator.workflow_history:
            if workflow.id == task_id or any(task_id in str(workflow.id) for _ in [1]):
                return await self.orchestrator.get_workflow_status(workflow.id)
        
        return None
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task"""
        
        # Cancel async task if exists
        if task_id in self.async_tasks:
            task = self.async_tasks[task_id]
            task.cancel()
            del self.async_tasks[task_id]
            return True
        
        # Cancel workflow
        return await self.orchestrator.cancel_workflow(task_id)
    
    async def get_system_status(self) -> CrewSystemStatus:
        """Get comprehensive system status"""
        
        orchestrator_stats = self.orchestrator.get_orchestrator_statistics()
        delegation_stats = self.delegation_engine.get_delegation_statistics()
        hierarchy_status = self.hierarchy.get_hierarchy_status()
        performance_stats = await self.performance_monitor.get_performance_summary()
        
        return CrewSystemStatus(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            orchestrator=orchestrator_stats,
            delegation_engine=delegation_stats,
            agent_hierarchy=hierarchy_status,
            performance=performance_stats
        )
    
    async def optimize_delegation_rules(self) -> Dict[str, Any]:
        """Optimize delegation rules based on performance data"""
        
        performance_data = await self.performance_monitor.get_performance_summary()
        
        # Analyze performance patterns
        optimizations = []
        
        # Check strategy effectiveness
        strategy_performance = performance_data.get("strategy_performance", {})
        for strategy, metrics in strategy_performance.items():
            if metrics.get("success_rate", 0) < 0.8:
                optimizations.append(f"Strategy {strategy} has low success rate: {metrics['success_rate']:.2f}")
        
        # Check execution time patterns
        avg_times = performance_data.get("average_execution_times", {})
        for strategy, avg_time in avg_times.items():
            if avg_time > 120:  # 2 minutes
                optimizations.append(f"Strategy {strategy} has high execution time: {avg_time:.1f}s")
        
        return {
            "optimizations_identified": len(optimizations),
            "recommendations": optimizations,
            "current_performance": performance_data
        }

# FastAPI Integration Functions
crew_integration = CrewAIIntegration()

async def get_crew_integration() -> CrewAIIntegration:
    """Dependency to get crew integration instance"""
    return crew_integration

def create_crew_routes(app: FastAPI):
    """Create CrewAI routes for the FastAPI app"""
    
    @app.post("/api/brain/crew/execute", response_model=CrewExecutionResult)
    async def execute_crew_task(
        request: CrewTaskRequest,
        background_tasks: BackgroundTasks,
        integration: CrewAIIntegration = Depends(get_crew_integration)
    ):
        """Execute a task using the AI crew system"""
        return await integration.execute_crew_task(request, background_tasks)
    
    @app.get("/api/brain/crew/status/{task_id}")
    async def get_task_status(
        task_id: str,
        integration: CrewAIIntegration = Depends(get_crew_integration)
    ):
        """Get status of a specific task"""
        status = await integration.get_task_status(task_id)
        if not status:
            raise HTTPException(status_code=404, detail="Task not found")
        return status
    
    @app.delete("/api/brain/crew/cancel/{task_id}")
    async def cancel_task(
        task_id: str,
        integration: CrewAIIntegration = Depends(get_crew_integration)
    ):
        """Cancel a running task"""
        success = await integration.cancel_task(task_id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found or already completed")
        return {"status": "cancelled", "task_id": task_id}
    
    @app.get("/api/brain/crew/system-status", response_model=CrewSystemStatus)
    async def get_system_status(
        integration: CrewAIIntegration = Depends(get_crew_integration)
    ):
        """Get comprehensive system status"""
        return await integration.get_system_status()
    
    @app.post("/api/brain/crew/optimize")
    async def optimize_system(
        integration: CrewAIIntegration = Depends(get_crew_integration)
    ):
        """Optimize delegation rules and system performance"""
        return await integration.optimize_delegation_rules()
    
    @app.get("/api/brain/crew/health")
    async def health_check():
        """Health check endpoint"""
        return await crew_orchestrator.health_check()
    
    @app.get("/api/brain/crew/statistics")
    async def get_statistics(
        integration: CrewAIIntegration = Depends(get_crew_integration)
    ):
        """Get detailed system statistics"""
        return {
            "orchestrator": crew_orchestrator.get_orchestrator_statistics(),
            "delegation": smart_delegation_engine.get_delegation_statistics(),
            "hierarchy": agent_hierarchy.get_hierarchy_status(),
            "performance": await integration.performance_monitor.get_performance_summary()
        }

# Middleware for request logging and monitoring
class CrewRequestMiddleware:
    """Middleware for logging and monitoring crew requests"""
    
    def __init__(self, app: FastAPI):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Log crew-related requests
            if request.url.path.startswith("/api/brain/crew/"):
                start_time = datetime.now()
                
                # Process request
                response = await self.app(scope, receive, send)
                
                # Log execution time
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.info(
                    f"Crew API call: {request.method} {request.url.path} "
                    f"completed in {execution_time:.3f}s"
                )
                
                return response
        
        return await self.app(scope, receive, send)

# Context managers for crew operations
@asynccontextmanager
async def crew_operation_context(operation_name: str, metadata: Dict[str, Any] = None):
    """Context manager for crew operations with automatic logging and monitoring"""
    
    start_time = datetime.now()
    operation_id = f"{operation_name}_{start_time.strftime('%Y%m%d_%H%M%S')}"
    
    logger.info(f"Starting crew operation: {operation_name} [{operation_id}]")
    
    try:
        yield operation_id
        
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.info(
            f"Crew operation completed: {operation_name} [{operation_id}] "
            f"in {execution_time:.3f}s"
        )
    
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.error(
            f"Crew operation failed: {operation_name} [{operation_id}] "
            f"after {execution_time:.3f}s - {str(e)}"
        )
        raise

# Integration helper functions
async def integrate_with_brain_api(brain_app: FastAPI):
    """Integrate crew system with existing Brain API"""
    
    # Add crew routes
    create_crew_routes(brain_app)
    
    # Add middleware
    brain_app.middleware("http")(CrewRequestMiddleware(brain_app))
    
    logger.info("CrewAI system integrated with Brain API")

async def validate_crew_integration() -> Dict[str, Any]:
    """Validate that crew integration is working correctly"""
    
    try:
        # Test basic functionality
        health = await crew_orchestrator.health_check()
        system_status = await crew_integration.get_system_status()
        
        return {
            "status": "healthy",
            "health_check": health,
            "system_status": system_status.dict(),
            "integration_complete": True
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "integration_complete": False
        }