"""
Crew Orchestrator for BizOSaaS AI Crew System

This module orchestrates the execution of AI crews for complex business workflows,
integrating with the existing FastAPI Brain routing system.
"""

from typing import Dict, Any, List, Optional, Union, Callable
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio
import logging
import json
import uuid
from contextlib import asynccontextmanager

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from .agent_hierarchy import (
    AgentHierarchy, 
    BaseHierarchicalAgent, 
    AgentDomain, 
    AgentStatus,
    agent_hierarchy
)
from .smart_delegation import (
    SmartDelegationEngine, 
    ExecutionStrategy, 
    TaskComplexity,
    smart_delegation_engine
)

logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"

class CrewType(Enum):
    """Types of crew configurations"""
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"
    CONSENSUS = "consensus"
    PARALLEL = "parallel"

@dataclass
class WorkflowExecution:
    """Represents a workflow execution instance"""
    id: str
    tenant_id: str
    workflow_type: str
    status: WorkflowStatus
    strategy: ExecutionStrategy
    crew_type: Optional[CrewType]
    start_time: datetime
    end_time: Optional[datetime] = None
    agents_used: List[str] = None
    tasks_completed: int = 0
    total_tasks: int = 0
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metrics: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.agents_used is None:
            self.agents_used = []
        if self.metrics is None:
            self.metrics = {}

class TaskRequest(BaseModel):
    """Request model for task execution"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    type: str
    description: str
    domain: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    data_volume: int = 0
    requires_ai: bool = False
    multi_domain: bool = False
    priority: int = 5  # 1-10, 10 being highest
    timeout: int = 300  # seconds
    preferred_strategy: Optional[str] = None
    callback_url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TaskResponse(BaseModel):
    """Response model for task execution"""
    task_id: str
    workflow_id: str
    status: str
    strategy_used: str
    execution_time: float
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    agents_used: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)

class CrewConfiguration:
    """Configuration for different types of crews"""
    
    def __init__(self, crew_type: CrewType):
        self.crew_type = crew_type
        self.process_mapping = {
            CrewType.SEQUENTIAL: Process.sequential,
            CrewType.HIERARCHICAL: Process.hierarchical,
            CrewType.CONSENSUS: Process.sequential,  # Custom consensus logic
            CrewType.PARALLEL: Process.sequential  # Custom parallel logic
        }
    
    def create_crew(
        self, 
        agents: List[Agent], 
        tasks: List[Task], 
        **kwargs
    ) -> Crew:
        """Create a crew based on configuration"""
        
        process = self.process_mapping[self.crew_type]
        
        crew_config = {
            "agents": agents,
            "tasks": tasks,
            "verbose": kwargs.get("verbose", True),
            "process": process,
            "memory": kwargs.get("memory", True),
            "cache": kwargs.get("cache", True),
            "max_rpm": kwargs.get("max_rpm", 100),
            "share_crew": kwargs.get("share_crew", True)
        }
        
        # Add configuration-specific settings
        if self.crew_type == CrewType.HIERARCHICAL:
            crew_config["manager_llm"] = kwargs.get("manager_llm")
        
        return Crew(**crew_config)

class CrewOrchestrator:
    """Main orchestrator for AI crew execution"""
    
    def __init__(self):
        self.agent_hierarchy = agent_hierarchy
        self.delegation_engine = smart_delegation_engine
        self.active_workflows: Dict[str, WorkflowExecution] = {}
        self.workflow_history: List[WorkflowExecution] = []
        self.crew_configurations = {
            CrewType.SEQUENTIAL: CrewConfiguration(CrewType.SEQUENTIAL),
            CrewType.HIERARCHICAL: CrewConfiguration(CrewType.HIERARCHICAL),
            CrewType.CONSENSUS: CrewConfiguration(CrewType.CONSENSUS),
            CrewType.PARALLEL: CrewConfiguration(CrewType.PARALLEL)
        }
    
    async def execute_task(self, task_request: TaskRequest) -> TaskResponse:
        """Main entry point for task execution"""
        
        start_time = datetime.now()
        workflow_id = str(uuid.uuid4())
        
        try:
            # Create workflow execution record
            workflow = WorkflowExecution(
                id=workflow_id,
                tenant_id=task_request.tenant_id,
                workflow_type=task_request.type,
                status=WorkflowStatus.PENDING,
                strategy=ExecutionStrategy.DIRECT_DB,  # Will be updated
                start_time=start_time
            )
            
            self.active_workflows[workflow_id] = workflow
            
            # Analyze and delegate task
            strategy, analysis = await self.delegation_engine.delegate_task(
                task_request.dict()
            )
            
            workflow.strategy = strategy
            workflow.status = WorkflowStatus.RUNNING
            
            # Execute based on strategy
            result = await self._execute_by_strategy(
                strategy, task_request, analysis, workflow
            )
            
            # Update workflow
            workflow.status = WorkflowStatus.COMPLETED
            workflow.end_time = datetime.now()
            workflow.result = result
            
            execution_time = (workflow.end_time - workflow.start_time).total_seconds()
            
            # Create response
            response = TaskResponse(
                task_id=task_request.id,
                workflow_id=workflow_id,
                status="completed",
                strategy_used=strategy.value,
                execution_time=execution_time,
                result=result,
                agents_used=workflow.agents_used,
                metrics=workflow.metrics
            )
            
            await self._finalize_workflow(workflow)
            
            return response
        
        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}")
            
            # Update workflow with error
            workflow.status = WorkflowStatus.FAILED
            workflow.end_time = datetime.now()
            workflow.error = str(e)
            
            execution_time = (workflow.end_time - workflow.start_time).total_seconds()
            
            response = TaskResponse(
                task_id=task_request.id,
                workflow_id=workflow_id,
                status="failed",
                strategy_used=strategy.value if 'strategy' in locals() else "unknown",
                execution_time=execution_time,
                error=str(e)
            )
            
            await self._finalize_workflow(workflow)
            
            return response
    
    async def _execute_by_strategy(
        self,
        strategy: ExecutionStrategy,
        task_request: TaskRequest,
        analysis: Any,
        workflow: WorkflowExecution
    ) -> Dict[str, Any]:
        """Execute task based on delegation strategy"""
        
        execution_map = {
            ExecutionStrategy.DIRECT_DB: self._execute_direct_db,
            ExecutionStrategy.DIRECT_API: self._execute_direct_api,
            ExecutionStrategy.SINGLE_AGENT: self._execute_single_agent,
            ExecutionStrategy.MULTI_AGENT: self._execute_multi_agent,
            ExecutionStrategy.CREW_WORKFLOW: self._execute_crew_workflow
        }
        
        executor = execution_map.get(strategy)
        if not executor:
            raise ValueError(f"Unknown execution strategy: {strategy}")
        
        return await executor(task_request, analysis, workflow)
    
    async def _execute_direct_db(
        self,
        task_request: TaskRequest,
        analysis: Any,
        workflow: WorkflowExecution
    ) -> Dict[str, Any]:
        """Execute direct database operations"""
        
        # Simulate direct database operation
        await asyncio.sleep(0.1)  # Simulate DB query time
        
        workflow.metrics["execution_type"] = "direct_database"
        workflow.metrics["queries_executed"] = 1
        
        return {
            "status": "success",
            "execution_type": "direct_database",
            "message": f"Executed {task_request.type} directly on database",
            "affected_rows": task_request.parameters.get("limit", 1)
        }
    
    async def _execute_direct_api(
        self,
        task_request: TaskRequest,
        analysis: Any,
        workflow: WorkflowExecution
    ) -> Dict[str, Any]:
        """Execute direct API calls"""
        
        # Simulate API call
        await asyncio.sleep(0.5)  # Simulate API response time
        
        workflow.metrics["execution_type"] = "direct_api"
        workflow.metrics["api_calls"] = 1
        
        return {
            "status": "success",
            "execution_type": "direct_api",
            "message": f"Executed {task_request.type} via direct API call",
            "api_response": "success"
        }
    
    async def _execute_single_agent(
        self,
        task_request: TaskRequest,
        analysis: Any,
        workflow: WorkflowExecution
    ) -> Dict[str, Any]:
        """Execute task using a single AI agent"""
        
        # Find appropriate agent
        domain = AgentDomain(task_request.domain) if task_request.domain else None
        agent = await self._find_best_agent(domain, task_request)
        
        if not agent:
            raise Exception(f"No suitable agent found for domain: {task_request.domain}")
        
        workflow.agents_used.append(agent.config.name)
        
        # Execute task with agent
        task_data = task_request.dict()
        result = await agent.execute_task(task_data)
        
        workflow.metrics["execution_type"] = "single_agent"
        workflow.metrics["agent_used"] = agent.config.name
        
        return result
    
    async def _execute_multi_agent(
        self,
        task_request: TaskRequest,
        analysis: Any,
        workflow: WorkflowExecution
    ) -> Dict[str, Any]:
        """Execute task using multiple AI agents"""
        
        # Determine required agents
        required_domains = task_request.parameters.get("required_domains", [])
        if not required_domains and task_request.domain:
            required_domains = [task_request.domain]
        
        agents = []
        for domain_str in required_domains:
            domain = AgentDomain(domain_str)
            agent = await self._find_best_agent(domain, task_request)
            if agent:
                agents.append(agent)
        
        if not agents:
            # Fallback to single agent
            return await self._execute_single_agent(task_request, analysis, workflow)
        
        # Create tasks for each agent
        tasks = []
        crewai_agents = []
        
        for agent in agents:
            workflow.agents_used.append(agent.config.name)
            
            task_description = f"Handle {agent.config.domain.value} aspects of: {task_request.description}"
            
            task = Task(
                description=task_description,
                agent=agent.agent,
                expected_output=f"Processed {agent.config.domain.value} results"
            )
            
            tasks.append(task)
            crewai_agents.append(agent.agent)
        
        # Create and execute crew
        crew_config = self.crew_configurations[CrewType.SEQUENTIAL]
        crew = crew_config.create_crew(crewai_agents, tasks)
        
        result = crew.kickoff(task_request.dict())
        
        workflow.metrics["execution_type"] = "multi_agent"
        workflow.metrics["agents_used"] = len(agents)
        workflow.crew_type = CrewType.SEQUENTIAL
        
        return {
            "status": "success",
            "execution_type": "multi_agent",
            "result": result,
            "agents_used": [agent.config.name for agent in agents]
        }
    
    async def _execute_crew_workflow(
        self,
        task_request: TaskRequest,
        analysis: Any,
        workflow: WorkflowExecution
    ) -> Dict[str, Any]:
        """Execute complex workflow using full crew orchestration"""
        
        # Use hierarchical routing through agent hierarchy
        task_data = task_request.dict()
        result = await self.agent_hierarchy.route_task(task_data)
        
        workflow.metrics["execution_type"] = "crew_workflow"
        workflow.metrics["orchestration_type"] = "hierarchical"
        workflow.crew_type = CrewType.HIERARCHICAL
        
        # Extract agents used from result
        if isinstance(result, dict) and "agents_used" in result:
            workflow.agents_used.extend(result["agents_used"])
        
        return result
    
    async def _find_best_agent(
        self,
        domain: Optional[AgentDomain],
        task_request: TaskRequest
    ) -> Optional[BaseHierarchicalAgent]:
        """Find the best available agent for a task"""
        
        if domain:
            domain_agents = self.agent_hierarchy.get_agents_by_domain(domain)
        else:
            domain_agents = self.agent_hierarchy.get_available_agents()
        
        # Filter available agents
        available_agents = [
            agent for agent in domain_agents
            if agent.status == AgentStatus.AVAILABLE
        ]
        
        if not available_agents:
            return None
        
        # Find best agent based on task compatibility and performance
        best_agent = None
        best_score = 0
        
        for agent in available_agents:
            if agent.can_handle_task(task_request.dict()):
                # Score based on success rate and load
                score = agent.metrics.success_rate * (1 - agent.metrics.load_factor)
                
                # Boost score for exact domain match
                if domain and agent.config.domain == domain:
                    score *= 1.5
                
                if score > best_score:
                    best_score = score
                    best_agent = agent
        
        return best_agent
    
    async def _finalize_workflow(self, workflow: WorkflowExecution):
        """Finalize workflow execution"""
        
        # Move from active to history
        if workflow.id in self.active_workflows:
            del self.active_workflows[workflow.id]
        
        self.workflow_history.append(workflow)
        
        # Keep only last 1000 workflow executions
        if len(self.workflow_history) > 1000:
            self.workflow_history = self.workflow_history[-1000:]
        
        # Log completion
        logger.info(
            f"Workflow {workflow.id} completed with status: {workflow.status.value}"
        )
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a workflow"""
        
        # Check active workflows
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
        else:
            # Check history
            workflow = next(
                (w for w in self.workflow_history if w.id == workflow_id),
                None
            )
        
        if not workflow:
            return None
        
        return {
            "id": workflow.id,
            "tenant_id": workflow.tenant_id,
            "type": workflow.workflow_type,
            "status": workflow.status.value,
            "strategy": workflow.strategy.value,
            "crew_type": workflow.crew_type.value if workflow.crew_type else None,
            "start_time": workflow.start_time.isoformat(),
            "end_time": workflow.end_time.isoformat() if workflow.end_time else None,
            "agents_used": workflow.agents_used,
            "tasks_completed": workflow.tasks_completed,
            "total_tasks": workflow.total_tasks,
            "error": workflow.error,
            "metrics": workflow.metrics
        }
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel an active workflow"""
        
        if workflow_id not in self.active_workflows:
            return False
        
        workflow = self.active_workflows[workflow_id]
        workflow.status = WorkflowStatus.CANCELLED
        workflow.end_time = datetime.now()
        
        await self._finalize_workflow(workflow)
        
        return True
    
    def get_orchestrator_statistics(self) -> Dict[str, Any]:
        """Get comprehensive orchestrator statistics"""
        
        total_workflows = len(self.workflow_history)
        active_count = len(self.active_workflows)
        
        if total_workflows == 0:
            return {
                "total_workflows": 0,
                "active_workflows": active_count,
                "message": "No workflow history available"
            }
        
        # Status distribution
        status_counts = {}
        for workflow in self.workflow_history:
            status = workflow.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Strategy distribution
        strategy_counts = {}
        for workflow in self.workflow_history:
            strategy = workflow.strategy.value
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        # Average execution time
        completed_workflows = [
            w for w in self.workflow_history 
            if w.status == WorkflowStatus.COMPLETED and w.end_time
        ]
        
        avg_execution_time = 0
        if completed_workflows:
            execution_times = [
                (w.end_time - w.start_time).total_seconds()
                for w in completed_workflows
            ]
            avg_execution_time = sum(execution_times) / len(execution_times)
        
        # Success rate
        success_rate = len(completed_workflows) / total_workflows if total_workflows > 0 else 0
        
        return {
            "total_workflows": total_workflows,
            "active_workflows": active_count,
            "status_distribution": status_counts,
            "strategy_distribution": strategy_counts,
            "success_rate": success_rate,
            "average_execution_time": avg_execution_time,
            "agent_hierarchy_status": self.agent_hierarchy.get_hierarchy_status(),
            "recent_workflows": [
                {
                    "id": w.id,
                    "type": w.workflow_type,
                    "status": w.status.value,
                    "strategy": w.strategy.value,
                    "execution_time": (
                        (w.end_time - w.start_time).total_seconds()
                        if w.end_time else None
                    )
                }
                for w in self.workflow_history[-10:]
            ]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Check system health"""
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "active_workflows": len(self.active_workflows),
            "agent_hierarchy": {
                "total_agents": len(self.agent_hierarchy.agents),
                "available_agents": len(self.agent_hierarchy.get_available_agents())
            },
            "delegation_engine": {
                "rules_count": len(self.delegation_engine.delegation_rules),
                "decisions_count": len(self.delegation_engine.execution_history)
            }
        }

# Global instance
crew_orchestrator = CrewOrchestrator()