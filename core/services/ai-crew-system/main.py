"""
Main AI Crew System FastAPI Application

This module provides the main FastAPI application for the AI Crew System,
integrating with the existing BizOSaaS Brain API routing system.
"""

from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import asyncio
import logging
from datetime import datetime
import os

from .crew_orchestrator import (
    CrewOrchestrator, 
    TaskRequest, 
    TaskResponse,
    crew_orchestrator
)
from .crew_integration import (
    CrewAIIntegration,
    CrewTaskRequest,
    CrewExecutionResult,
    CrewSystemStatus,
    create_crew_routes,
    integrate_with_brain_api,
    crew_integration
)
from .specialized_crews.crm_crew import CRMSpecializedCrew
from .performance_monitor import performance_monitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="BizOSaaS AI Crew System",
    description="Hierarchical AI Agent Orchestration for Intelligent Business Automation",
    version="1.0.0",
    docs_url="/api/crew/docs",
    redoc_url="/api/crew/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global crew instances
crm_crew = CRMSpecializedCrew()

@app.on_event("startup")
async def startup_event():
    """Initialize the crew system on startup"""
    logger.info("Starting BizOSaaS AI Crew System...")
    
    try:
        # Initialize performance monitoring
        performance_monitor.toggle_monitoring(True)
        
        # Validate crew integration
        health_check = await crew_orchestrator.health_check()
        logger.info(f"Crew orchestrator health: {health_check}")
        
        # Initialize specialized crews
        logger.info("Specialized crews initialized successfully")
        
        logger.info("AI Crew System startup completed successfully")
        
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("Shutting down AI Crew System...")
    
    # Clean up old performance data
    await performance_monitor.clear_old_data(retention_days=7)
    
    logger.info("AI Crew System shutdown completed")

# Health and Status Endpoints
@app.get("/api/crew/health")
async def health_check():
    """Health check endpoint"""
    try:
        health = await crew_orchestrator.health_check()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "crew_system": health,
            "performance_monitoring": performance_monitor.monitoring_active
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/crew/status", response_model=CrewSystemStatus)
async def get_system_status():
    """Get comprehensive system status"""
    try:
        return await crew_integration.get_system_status()
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Core Crew Execution Endpoints
@app.post("/api/crew/execute", response_model=CrewExecutionResult)
async def execute_crew_task(
    request: CrewTaskRequest,
    background_tasks: BackgroundTasks
):
    """Execute a task using the AI crew system"""
    try:
        logger.info(f"Executing crew task: {request.type} for tenant: {request.tenant_id}")
        result = await crew_integration.execute_crew_task(request, background_tasks)
        return result
    except Exception as e:
        logger.error(f"Task execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/crew/task/{task_id}")
async def get_task_status(task_id: str):
    """Get status of a specific task"""
    try:
        status = await crew_integration.get_task_status(task_id)
        if not status:
            raise HTTPException(status_code=404, detail="Task not found")
        return status
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Task status check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/crew/task/{task_id}")
async def cancel_task(task_id: str):
    """Cancel a running task"""
    try:
        success = await crew_integration.cancel_task(task_id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found or already completed")
        return {"status": "cancelled", "task_id": task_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Task cancellation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Specialized Crew Endpoints
@app.post("/api/crew/crm/lead-scoring")
async def crm_lead_scoring(
    lead_data: Dict[str, Any],
    scoring_criteria: Optional[Dict[str, float]] = None,
    include_recommendations: bool = True
):
    """Execute CRM lead scoring"""
    try:
        from .specialized_crews.crm_crew import LeadScoringRequest
        
        request = LeadScoringRequest(
            lead_data=lead_data,
            scoring_criteria=scoring_criteria,
            include_recommendations=include_recommendations
        )
        
        result = await crm_crew.execute_lead_scoring(request)
        return result
    except Exception as e:
        logger.error(f"CRM lead scoring failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/crew/crm/customer-segmentation")
async def crm_customer_segmentation(
    customer_data: List[Dict[str, Any]],
    segmentation_type: str = "behavioral",
    segment_count: int = 5
):
    """Execute CRM customer segmentation"""
    try:
        from .specialized_crews.crm_crew import CustomerSegmentationRequest
        
        request = CustomerSegmentationRequest(
            customer_data=customer_data,
            segmentation_type=segmentation_type,
            segment_count=segment_count
        )
        
        result = await crm_crew.execute_customer_segmentation(request)
        return result
    except Exception as e:
        logger.error(f"CRM customer segmentation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/crew/crm/nurturing-campaign")
async def crm_nurturing_campaign(
    lead_segments: List[str],
    campaign_objective: str,
    duration_days: int = 30,
    touchpoint_frequency: str = "weekly"
):
    """Execute CRM nurturing campaign creation"""
    try:
        from .specialized_crews.crm_crew import NurturingCampaignRequest
        
        request = NurturingCampaignRequest(
            lead_segments=lead_segments,
            campaign_objective=campaign_objective,
            duration_days=duration_days,
            touchpoint_frequency=touchpoint_frequency
        )
        
        result = await crm_crew.execute_nurturing_campaign(request)
        return result
    except Exception as e:
        logger.error(f"CRM nurturing campaign failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/crew/crm/pipeline-optimization")
async def crm_pipeline_optimization(pipeline_data: Dict[str, Any]):
    """Execute CRM pipeline optimization"""
    try:
        result = await crm_crew.execute_pipeline_optimization(pipeline_data)
        return result
    except Exception as e:
        logger.error(f"CRM pipeline optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/crew/crm/comprehensive-analysis")
async def crm_comprehensive_analysis(crm_data: Dict[str, Any]):
    """Execute comprehensive CRM analysis"""
    try:
        result = await crm_crew.execute_comprehensive_crm_analysis(crm_data)
        return result
    except Exception as e:
        logger.error(f"CRM comprehensive analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Performance and Analytics Endpoints
@app.get("/api/crew/performance/summary")
async def get_performance_summary():
    """Get performance summary"""
    try:
        summary = await performance_monitor.get_performance_summary()
        return summary
    except Exception as e:
        logger.error(f"Performance summary failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/crew/performance/metrics")
async def get_detailed_metrics(
    metric_type: Optional[str] = None,
    strategy: Optional[str] = None,
    hours: int = 24
):
    """Get detailed performance metrics"""
    try:
        from datetime import timedelta
        from .performance_monitor import MetricType
        
        metric_type_enum = None
        if metric_type:
            try:
                metric_type_enum = MetricType(metric_type)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid metric type: {metric_type}")
        
        time_range = timedelta(hours=hours)
        
        metrics = await performance_monitor.get_detailed_metrics(
            metric_type=metric_type_enum,
            strategy=strategy,
            time_range=time_range
        )
        
        return {
            "metrics": metrics,
            "filters": {
                "metric_type": metric_type,
                "strategy": strategy,
                "time_range_hours": hours
            },
            "total_count": len(metrics)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Detailed metrics failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/crew/performance/export")
async def export_performance_data(format: str = "json"):
    """Export performance data"""
    try:
        if format.lower() not in ["json"]:
            raise HTTPException(status_code=400, detail="Only JSON format supported currently")
        
        exported_data = await performance_monitor.export_metrics(format)
        
        return JSONResponse(
            content={"data": exported_data, "format": format},
            headers={
                "Content-Disposition": f"attachment; filename=crew_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Performance export failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# System Management Endpoints
@app.post("/api/crew/optimize")
async def optimize_system():
    """Optimize delegation rules and system performance"""
    try:
        optimization_result = await crew_integration.optimize_delegation_rules()
        return optimization_result
    except Exception as e:
        logger.error(f"System optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/crew/statistics")
async def get_system_statistics():
    """Get detailed system statistics"""
    try:
        return {
            "orchestrator": crew_orchestrator.get_orchestrator_statistics(),
            "delegation": crew_integration.delegation_engine.get_delegation_statistics(),
            "hierarchy": crew_integration.hierarchy.get_hierarchy_status(),
            "performance": await performance_monitor.get_performance_summary()
        }
    except Exception as e:
        logger.error(f"Statistics retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/crew/config/monitoring")
async def toggle_monitoring(active: bool):
    """Enable or disable performance monitoring"""
    try:
        performance_monitor.toggle_monitoring(active)
        return {
            "monitoring_active": active,
            "message": f"Performance monitoring {'enabled' if active else 'disabled'}"
        }
    except Exception as e:
        logger.error(f"Monitoring toggle failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Integration Test Endpoints
@app.post("/api/crew/test/simple-task")
async def test_simple_task():
    """Test simple task execution"""
    try:
        test_request = CrewTaskRequest(
            type="test_simple_operation",
            description="Test simple database operation",
            tenant_id="test_tenant",
            domain="crm",
            data_volume=10,
            requires_ai=False
        )
        
        background_tasks = BackgroundTasks()
        result = await crew_integration.execute_crew_task(test_request, background_tasks)
        
        return {
            "test_type": "simple_task",
            "result": result,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Simple task test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/crew/test/complex-workflow")
async def test_complex_workflow():
    """Test complex workflow execution"""
    try:
        test_request = CrewTaskRequest(
            type="test_complex_workflow",
            description="Test multi-agent workflow coordination",
            tenant_id="test_tenant",
            multi_domain=True,
            requires_ai=True,
            parameters={
                "required_domains": ["crm", "analytics"],
                "complexity": "high"
            }
        )
        
        background_tasks = BackgroundTasks()
        result = await crew_integration.execute_crew_task(test_request, background_tasks)
        
        return {
            "test_type": "complex_workflow",
            "result": result,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Complex workflow test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception in {request.url.path}: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,  # Different port from Brain API (8001)
        reload=True,
        log_level="info"
    )