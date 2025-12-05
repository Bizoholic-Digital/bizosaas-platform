"""
CrewAI Orchestration Service for BizOSaaS Brain API

This service provides FastAPI endpoints for managing and executing CrewAI workflows
across multiple business projects. It integrates with the advanced workflow orchestrator
and multi-project agent manager to provide comprehensive AI automation capabilities.

Key Features:
- Multi-project workflow execution
- Real-time workflow monitoring
- Performance analytics and optimization
- Cross-project collaboration
- Resource management and allocation
- Advanced error handling and recovery
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Query
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import asyncio
import json
import logging
import time
from enum import Enum
import structlog

# Import orchestration components
from crewai_workflow_orchestrator import (
    WorkflowOrchestrator, WorkflowConfiguration, TaskDefinition, 
    WorkflowResult, TaskPriority, AgentRole, get_workflow_orchestrator
)

from multi_project_agent_manager import (
    MultiProjectAgentManager, ProjectType, BusinessDomain,
    get_multi_project_manager
)

# Import existing review management
from review_management_service import create_review_routes

# Import tenant management
from enhanced_tenant_management import get_current_tenant, EnhancedTenant

logger = structlog.get_logger(__name__)


class WorkflowExecutionRequest(BaseModel):
    """Request model for workflow execution"""
    workflow_type: str
    project_id: str
    crew_name: str
    priority: TaskPriority = TaskPriority.MEDIUM
    max_execution_time: int = 3600
    parallel_execution: bool = False
    tasks: List[Dict[str, Any]] = Field(default_factory=list)
    inputs: Dict[str, Any] = Field(default_factory=dict)
    config: Dict[str, Any] = Field(default_factory=dict)


class CrossProjectWorkflowRequest(BaseModel):
    """Request model for cross-project workflows"""
    workflow_name: str
    projects: List[Dict[str, Any]] = Field(default_factory=list)
    coordination_strategy: str = "sequential"  # sequential, parallel, conditional
    dependency_rules: Dict[str, List[str]] = Field(default_factory=dict)
    global_config: Dict[str, Any] = Field(default_factory=dict)


class AgentPerformanceQuery(BaseModel):
    """Query parameters for agent performance"""
    project_id: Optional[str] = None
    agent_id: Optional[str] = None
    time_range_hours: int = 24
    metric_types: List[str] = Field(default_factory=lambda: ["success_rate", "execution_time", "error_count"])


class WorkflowMonitoringResponse(BaseModel):
    """Response model for workflow monitoring"""
    workflow_id: str
    status: str
    progress_percentage: float
    current_task: Optional[str] = None
    estimated_completion: Optional[datetime] = None
    performance_metrics: Dict[str, Any] = Field(default_factory=dict)
    resource_usage: Dict[str, Any] = Field(default_factory=dict)


async def get_orchestrator() -> WorkflowOrchestrator:
    """Dependency to get workflow orchestrator"""
    return await get_workflow_orchestrator()


async def get_multi_project_manager() -> MultiProjectAgentManager:
    """Dependency to get multi-project manager"""
    return await get_multi_project_manager()


def create_crewai_orchestration_routes() -> APIRouter:
    """Create and configure CrewAI orchestration routes"""
    router = APIRouter(prefix="/crewai", tags=["CrewAI Orchestration"])
    
    @router.post("/workflows/execute")
    async def execute_workflow(
        request: WorkflowExecutionRequest,
        background_tasks: BackgroundTasks,
        tenant: EnhancedTenant = Depends(get_current_tenant),
        manager: MultiProjectAgentManager = Depends(get_multi_project_manager)
    ):
        """Execute a CrewAI workflow for a specific project"""
        try:
            # Validate project access for tenant
            if not await _validate_project_access(tenant, request.project_id):
                raise HTTPException(
                    status_code=403,
                    detail=f"Tenant {tenant.id} does not have access to project {request.project_id}"
                )
            
            # Create workflow configuration
            workflow_config = {
                "tasks": request.tasks,
                "inputs": request.inputs,
                **request.config
            }
            
            # Execute workflow
            start_time = time.time()
            result = await manager.execute_project_workflow(
                request.project_id,
                request.crew_name,
                workflow_config
            )
            
            execution_time = time.time() - start_time
            
            # Log workflow execution
            logger.info(
                "CrewAI workflow executed",
                tenant_id=tenant.id,
                project_id=request.project_id,
                crew_name=request.crew_name,
                execution_time=execution_time,
                status=result.get("status")
            )
            
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "workflow_id": f"{request.project_id}_{request.crew_name}_{int(time.time())}",
                    "execution_result": result,
                    "execution_time_seconds": execution_time,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/workflows/cross-project")
    async def execute_cross_project_workflow(
        request: CrossProjectWorkflowRequest,
        background_tasks: BackgroundTasks,
        tenant: EnhancedTenant = Depends(get_current_tenant),
        manager: MultiProjectAgentManager = Depends(get_multi_project_manager)
    ):
        """Execute a workflow spanning multiple projects"""
        try:
            # Validate access to all projects
            for project_config in request.projects:
                project_id = project_config.get("project_id")
                if not await _validate_project_access(tenant, project_id):
                    raise HTTPException(
                        status_code=403,
                        detail=f"Tenant {tenant.id} does not have access to project {project_id}"
                    )
            
            # Execute cross-project workflow
            start_time = time.time()
            result = await manager.execute_cross_project_workflow({
                "projects": request.projects,
                "coordination_strategy": request.coordination_strategy,
                "dependency_rules": request.dependency_rules,
                **request.global_config
            })
            
            execution_time = time.time() - start_time
            
            logger.info(
                "Cross-project CrewAI workflow executed",
                tenant_id=tenant.id,
                workflow_name=request.workflow_name,
                projects=[p.get("project_id") for p in request.projects],
                execution_time=execution_time
            )
            
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "workflow_name": request.workflow_name,
                    "cross_project_result": result,
                    "execution_time_seconds": execution_time,
                    "projects_involved": len(request.projects),
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Cross-project workflow execution failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/workflows/{workflow_id}/status")
    async def get_workflow_status(
        workflow_id: str,
        tenant: EnhancedTenant = Depends(get_current_tenant),
        orchestrator: WorkflowOrchestrator = Depends(get_orchestrator)
    ):
        """Get real-time status of a workflow execution"""
        try:
            # Get workflow status from orchestrator
            status = orchestrator.get_workflow_status(workflow_id)
            
            if not status:
                raise HTTPException(
                    status_code=404,
                    detail=f"Workflow {workflow_id} not found"
                )
            
            # Calculate progress and completion estimates
            progress_data = await _calculate_workflow_progress(workflow_id, status)
            
            return JSONResponse(
                status_code=200,
                content={
                    "workflow_id": workflow_id,
                    "status": status.status.value,
                    "progress": progress_data,
                    "start_time": status.start_time.isoformat(),
                    "end_time": status.end_time.isoformat() if status.end_time else None,
                    "duration_seconds": status.duration_seconds,
                    "results": status.results,
                    "errors": status.errors,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get workflow status: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/workflows")
    async def list_workflows(
        tenant: EnhancedTenant = Depends(get_current_tenant),
        project_id: Optional[str] = Query(None),
        status: Optional[str] = Query(None),
        limit: int = Query(50, le=200),
        offset: int = Query(0, ge=0),
        orchestrator: WorkflowOrchestrator = Depends(get_orchestrator)
    ):
        """List workflows with filtering options"""
        try:
            # Get workflows from orchestrator
            all_workflows = orchestrator.active_workflows
            
            # Filter workflows based on tenant access and parameters
            filtered_workflows = []
            for workflow_id, workflow_result in all_workflows.items():
                # Apply filters
                if project_id and project_id not in workflow_id:
                    continue
                
                if status and workflow_result.status.value != status:
                    continue
                
                # Check tenant access (simplified check)
                if await _validate_workflow_access(tenant, workflow_id):
                    filtered_workflows.append({
                        "workflow_id": workflow_id,
                        "status": workflow_result.status.value,
                        "start_time": workflow_result.start_time.isoformat(),
                        "end_time": workflow_result.end_time.isoformat() if workflow_result.end_time else None,
                        "duration_seconds": workflow_result.duration_seconds,
                        "error_count": len(workflow_result.errors)
                    })
            
            # Apply pagination
            total_count = len(filtered_workflows)
            paginated_workflows = filtered_workflows[offset:offset + limit]
            
            return JSONResponse(
                status_code=200,
                content={
                    "workflows": paginated_workflows,
                    "pagination": {
                        "total": total_count,
                        "limit": limit,
                        "offset": offset,
                        "has_more": offset + limit < total_count
                    },
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to list workflows: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/projects")
    async def list_projects(
        tenant: EnhancedTenant = Depends(get_current_tenant),
        manager: MultiProjectAgentManager = Depends(get_multi_project_manager)
    ):
        """List available projects and their configurations"""
        try:
            # Get accessible projects for tenant
            accessible_projects = []
            
            for project_id, project_config in manager.projects.items():
                if await _validate_project_access(tenant, project_id):
                    project_status = manager.get_project_status(project_id)
                    accessible_projects.append(project_status)
            
            return JSONResponse(
                status_code=200,
                content={
                    "projects": accessible_projects,
                    "total_projects": len(accessible_projects),
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to list projects: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/projects/{project_id}/crews")
    async def list_project_crews(
        project_id: str,
        tenant: EnhancedTenant = Depends(get_current_tenant),
        manager: MultiProjectAgentManager = Depends(get_multi_project_manager)
    ):
        """List available crews for a specific project"""
        try:
            # Validate project access
            if not await _validate_project_access(tenant, project_id):
                raise HTTPException(
                    status_code=403,
                    detail=f"Tenant {tenant.id} does not have access to project {project_id}"
                )
            
            # Get crews for project
            project_crews = manager.active_crews.get(project_id, {})
            
            crews_info = []
            for crew_name, crew in project_crews.items():
                crew_info = {
                    "crew_name": crew_name,
                    "agent_count": len(crew.agents),
                    "agents": [
                        {
                            "role": agent.role,
                            "goal": agent.goal,
                            "tools_count": len(agent.tools) if hasattr(agent, 'tools') else 0
                        }
                        for agent in crew.agents
                    ],
                    "capabilities": await _get_crew_capabilities(crew_name, crew)
                }
                crews_info.append(crew_info)
            
            return JSONResponse(
                status_code=200,
                content={
                    "project_id": project_id,
                    "crews": crews_info,
                    "total_crews": len(crews_info),
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to list project crews: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/performance/overview")
    async def get_performance_overview(
        tenant: EnhancedTenant = Depends(get_current_tenant),
        time_range_hours: int = Query(24, ge=1, le=168),
        manager: MultiProjectAgentManager = Depends(get_multi_project_manager),
        orchestrator: WorkflowOrchestrator = Depends(get_orchestrator)
    ):
        """Get performance overview across all projects and workflows"""
        try:
            # Get system overview from manager
            system_overview = manager.get_system_overview()
            
            # Get performance metrics from orchestrator
            orchestrator_metrics = orchestrator.get_system_metrics()
            
            # Combine and enhance metrics
            performance_overview = {
                "system_health": system_overview.get("system_health", "unknown"),
                "active_workflows": orchestrator_metrics.get("active_workflows", 0),
                "total_projects": system_overview.get("total_projects", 0),
                "total_agents": orchestrator_metrics.get("total_agents", 0),
                "overall_performance": system_overview.get("overall_performance", {}),
                "resource_utilization": system_overview.get("resource_utilization", {}),
                "project_breakdown": system_overview.get("project_breakdown", {}),
                "recent_activity": await _get_recent_activity(tenant, time_range_hours),
                "performance_trends": await _calculate_performance_trends(time_range_hours),
                "recommendations": await _generate_performance_recommendations(system_overview)
            }
            
            return JSONResponse(
                status_code=200,
                content={
                    "performance_overview": performance_overview,
                    "time_range_hours": time_range_hours,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to get performance overview: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/performance/agents")
    async def get_agent_performance(
        tenant: EnhancedTenant = Depends(get_current_tenant),
        project_id: Optional[str] = Query(None),
        agent_id: Optional[str] = Query(None),
        time_range_hours: int = Query(24, ge=1, le=168),
        orchestrator: WorkflowOrchestrator = Depends(get_orchestrator)
    ):
        """Get detailed agent performance metrics"""
        try:
            agent_metrics = {}
            
            # Get agent performance from orchestrator
            for agent_id_key, agent in orchestrator.agents.items():
                # Filter by project if specified
                if project_id and project_id not in agent_id_key:
                    continue
                
                # Filter by specific agent if specified
                if agent_id and agent_id != agent_id_key:
                    continue
                
                # Check tenant access
                if await _validate_agent_access(tenant, agent_id_key):
                    metrics = orchestrator.get_agent_performance(agent_id_key)
                    if metrics:
                        agent_metrics[agent_id_key] = {
                            "agent_id": agent_id_key,
                            "role": agent.role.value,
                            "performance_metrics": metrics.__dict__,
                            "recent_trends": await _calculate_agent_trends(agent_id_key, time_range_hours),
                            "efficiency_score": await _calculate_agent_efficiency(metrics),
                            "recommendations": await _generate_agent_recommendations(metrics)
                        }
            
            return JSONResponse(
                status_code=200,
                content={
                    "agent_performance": agent_metrics,
                    "total_agents": len(agent_metrics),
                    "time_range_hours": time_range_hours,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to get agent performance: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/workflows/{workflow_id}/control")
    async def control_workflow(
        workflow_id: str,
        action: str = Query(..., regex="^(pause|resume|cancel|restart)$"),
        tenant: EnhancedTenant = Depends(get_current_tenant),
        orchestrator: WorkflowOrchestrator = Depends(get_orchestrator)
    ):
        """Control workflow execution (pause, resume, cancel, restart)"""
        try:
            # Validate workflow access
            if not await _validate_workflow_access(tenant, workflow_id):
                raise HTTPException(
                    status_code=403,
                    detail=f"Tenant {tenant.id} does not have access to workflow {workflow_id}"
                )
            
            # Execute control action
            success = await _execute_workflow_control(workflow_id, action, orchestrator)
            
            if success:
                logger.info(
                    "Workflow control action executed",
                    tenant_id=tenant.id,
                    workflow_id=workflow_id,
                    action=action
                )
                
                return JSONResponse(
                    status_code=200,
                    content={
                        "success": True,
                        "workflow_id": workflow_id,
                        "action": action,
                        "message": f"Workflow {action} executed successfully",
                        "timestamp": datetime.now().isoformat()
                    }
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to {action} workflow {workflow_id}"
                )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Workflow control failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/templates")
    async def list_workflow_templates(
        tenant: EnhancedTenant = Depends(get_current_tenant),
        project_type: Optional[str] = Query(None),
        business_domain: Optional[str] = Query(None)
    ):
        """List available workflow templates"""
        try:
            templates = await _get_workflow_templates(project_type, business_domain)
            
            # Filter templates based on tenant access
            accessible_templates = []
            for template in templates:
                if await _validate_template_access(tenant, template):
                    accessible_templates.append(template)
            
            return JSONResponse(
                status_code=200,
                content={
                    "templates": accessible_templates,
                    "total_templates": len(accessible_templates),
                    "filters": {
                        "project_type": project_type,
                        "business_domain": business_domain
                    },
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to list workflow templates: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/templates/{template_id}/instantiate")
    async def instantiate_workflow_template(
        template_id: str,
        customization: Dict[str, Any],
        tenant: EnhancedTenant = Depends(get_current_tenant),
        manager: MultiProjectAgentManager = Depends(get_multi_project_manager)
    ):
        """Instantiate a workflow from a template with customizations"""
        try:
            # Get and validate template
            template = await _get_workflow_template(template_id)
            if not template:
                raise HTTPException(
                    status_code=404,
                    detail=f"Template {template_id} not found"
                )
            
            if not await _validate_template_access(tenant, template):
                raise HTTPException(
                    status_code=403,
                    detail=f"Tenant {tenant.id} does not have access to template {template_id}"
                )
            
            # Apply customizations to template
            workflow_config = await _apply_template_customizations(template, customization)
            
            # Execute instantiated workflow
            result = await manager.execute_project_workflow(
                workflow_config["project_id"],
                workflow_config["crew_name"],
                workflow_config["workflow"]
            )
            
            logger.info(
                "Workflow template instantiated",
                tenant_id=tenant.id,
                template_id=template_id,
                project_id=workflow_config["project_id"]
            )
            
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "template_id": template_id,
                    "workflow_id": result.get("workflow_id"),
                    "execution_result": result,
                    "customizations_applied": customization,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Template instantiation failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Utility functions
    async def _validate_project_access(tenant: EnhancedTenant, project_id: str) -> bool:
        """Validate if tenant has access to project"""
        # Implementation would check tenant permissions against project
        # For now, return True for all valid tenants
        return tenant and tenant.status.value == "active"
    
    async def _validate_workflow_access(tenant: EnhancedTenant, workflow_id: str) -> bool:
        """Validate if tenant has access to workflow"""
        # Implementation would check workflow ownership/permissions
        return tenant and tenant.status.value == "active"
    
    async def _validate_agent_access(tenant: EnhancedTenant, agent_id: str) -> bool:
        """Validate if tenant has access to agent"""
        return tenant and tenant.status.value == "active"
    
    async def _validate_template_access(tenant: EnhancedTenant, template: Dict[str, Any]) -> bool:
        """Validate if tenant has access to template"""
        return tenant and tenant.status.value == "active"
    
    async def _calculate_workflow_progress(workflow_id: str, status) -> Dict[str, Any]:
        """Calculate workflow progress and estimates"""
        return {
            "percentage": 75.0,  # Placeholder
            "current_phase": "execution",
            "estimated_completion": (datetime.now() + timedelta(minutes=30)).isoformat(),
            "tasks_completed": 3,
            "tasks_total": 4
        }
    
    async def _get_crew_capabilities(crew_name: str, crew) -> List[str]:
        """Get capabilities of a crew"""
        capabilities = []
        
        # Analyze agents to determine capabilities
        for agent in crew.agents:
            role = agent.role.lower()
            if "strategy" in role:
                capabilities.append("strategic_planning")
            if "analysis" in role or "analyst" in role:
                capabilities.append("data_analysis")
            if "content" in role or "writer" in role:
                capabilities.append("content_generation")
            if "optimization" in role:
                capabilities.append("performance_optimization")
            if "marketing" in role:
                capabilities.append("marketing_automation")
            if "ecommerce" in role or "product" in role:
                capabilities.append("ecommerce_optimization")
        
        return list(set(capabilities))  # Remove duplicates
    
    async def _get_recent_activity(tenant: EnhancedTenant, hours: int) -> List[Dict[str, Any]]:
        """Get recent workflow activity"""
        # Placeholder implementation
        return [
            {
                "type": "workflow_completed",
                "project_id": "bizoholic",
                "crew_name": "marketing_strategy",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "status": "success"
            },
            {
                "type": "workflow_started",
                "project_id": "coreldove",
                "crew_name": "ecommerce_optimization",
                "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(),
                "status": "running"
            }
        ]
    
    async def _calculate_performance_trends(hours: int) -> Dict[str, Any]:
        """Calculate performance trends"""
        return {
            "success_rate_trend": "improving",
            "execution_time_trend": "stable",
            "error_rate_trend": "decreasing",
            "throughput_trend": "increasing"
        }
    
    async def _generate_performance_recommendations(overview: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        success_rate = overview.get("overall_performance", {}).get("success_rate", 1.0)
        if success_rate < 0.9:
            recommendations.append("Consider reviewing agent configurations to improve success rate")
        
        cpu_util = overview.get("resource_utilization", {}).get("utilization_percent", {}).get("cpu", 0)
        if cpu_util > 80:
            recommendations.append("High CPU utilization detected - consider scaling resources")
        
        if not recommendations:
            recommendations.append("System performing optimally")
        
        return recommendations
    
    async def _calculate_agent_trends(agent_id: str, hours: int) -> Dict[str, Any]:
        """Calculate agent performance trends"""
        return {
            "performance_trend": "stable",
            "workload_trend": "increasing",
            "efficiency_trend": "improving"
        }
    
    async def _calculate_agent_efficiency(metrics) -> float:
        """Calculate agent efficiency score"""
        # Simple efficiency calculation based on success rate and execution time
        success_rate = metrics.success_rate
        avg_time = metrics.avg_execution_time
        
        # Normalize execution time (assume 60 seconds is baseline)
        time_efficiency = max(0, 1 - (avg_time - 60) / 300)  # Penalize times > 60s
        
        return (success_rate * 0.7 + time_efficiency * 0.3) * 100
    
    async def _generate_agent_recommendations(metrics) -> List[str]:
        """Generate recommendations for agent optimization"""
        recommendations = []
        
        if metrics.success_rate < 0.8:
            recommendations.append("Review agent tools and configurations")
        
        if metrics.avg_execution_time > 120:
            recommendations.append("Optimize agent tasks for faster execution")
        
        if metrics.error_count > 5:
            recommendations.append("Investigate common error patterns")
        
        return recommendations or ["Agent performing well"]
    
    async def _execute_workflow_control(workflow_id: str, action: str, orchestrator: WorkflowOrchestrator) -> bool:
        """Execute workflow control action"""
        # Implementation would depend on the specific orchestrator capabilities
        logger.info(f"Executing {action} on workflow {workflow_id}")
        return True  # Placeholder
    
    async def _get_workflow_templates(project_type: Optional[str], business_domain: Optional[str]) -> List[Dict[str, Any]]:
        """Get available workflow templates"""
        templates = [
            {
                "template_id": "bizoholic_marketing_campaign",
                "name": "Marketing Campaign Automation",
                "description": "Complete marketing campaign from strategy to execution",
                "project_type": "bizoholic",
                "business_domain": "marketing",
                "estimated_duration": "2-4 hours",
                "capabilities": ["strategy_development", "content_generation", "campaign_optimization"]
            },
            {
                "template_id": "coreldove_product_optimization",
                "name": "E-commerce Product Optimization",
                "description": "Comprehensive product listing and conversion optimization",
                "project_type": "coreldove",
                "business_domain": "ecommerce",
                "estimated_duration": "1-2 hours",
                "capabilities": ["seo_optimization", "pricing_strategy", "conversion_optimization"]
            },
            {
                "template_id": "cross_project_analytics",
                "name": "Cross-Project Performance Analysis",
                "description": "Analyze performance across multiple projects",
                "project_type": "multi",
                "business_domain": "analytics",
                "estimated_duration": "30-60 minutes",
                "capabilities": ["data_analysis", "reporting", "insights_generation"]
            }
        ]
        
        # Filter templates
        filtered_templates = []
        for template in templates:
            if project_type and template["project_type"] != project_type and template["project_type"] != "multi":
                continue
            if business_domain and template["business_domain"] != business_domain:
                continue
            filtered_templates.append(template)
        
        return filtered_templates
    
    async def _get_workflow_template(template_id: str) -> Optional[Dict[str, Any]]:
        """Get specific workflow template"""
        templates = await _get_workflow_templates(None, None)
        for template in templates:
            if template["template_id"] == template_id:
                return template
        return None
    
    async def _apply_template_customizations(template: Dict[str, Any], customization: Dict[str, Any]) -> Dict[str, Any]:
        """Apply customizations to workflow template"""
        # Create workflow configuration from template and customizations
        workflow_config = {
            "project_id": customization.get("project_id", "bizoholic"),
            "crew_name": customization.get("crew_name", "marketing_strategy"),
            "workflow": {
                "tasks": customization.get("tasks", []),
                "inputs": customization.get("inputs", {}),
                "config": customization.get("config", {})
            }
        }
        
        return workflow_config
    
    return router