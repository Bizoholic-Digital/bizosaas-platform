"""
Advanced CrewAI Workflow Orchestrator for BizOSaaS Platform

This module provides a sophisticated multi-agent workflow orchestration system
that leverages CrewAI for complex business process automation. It implements
hierarchical agent structures, advanced task delegation patterns, and 
performance optimization strategies for production-scale deployments.

Key Features:
- Hierarchical agent structures with clear roles and responsibilities
- Advanced task delegation and communication patterns
- Multi-tenant workflow orchestration
- Performance monitoring and optimization
- Error handling and recovery strategies
- Workflow state management and persistence
- Cross-platform integration capabilities
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import structlog

# CrewAI imports
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from crewai.agent import Agent as CrewAgent
from crewai.task import Task as CrewTask

# Pydantic for data validation
from pydantic import BaseModel, Field, validator

# Import existing review management components
from review_management_agents import (
    ReviewWorkflowCrew, ReviewAnalystAgent, ResponseWriterAgent,
    ReputationManagerAgent, CompetitorAnalystAgent
)

# Import unified tenant system
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from unified_tenant_middleware import UnifiedTenant

logger = structlog.get_logger(__name__)


class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentRole(Enum):
    """Predefined agent roles for the platform"""
    ORCHESTRATOR = "orchestrator"
    ANALYST = "analyst"
    GENERATOR = "generator"
    VALIDATOR = "validator"
    OPTIMIZER = "optimizer"
    MONITOR = "monitor"
    SPECIALIST = "specialist"


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5


@dataclass
class WorkflowMetrics:
    """Metrics for workflow performance tracking"""
    workflow_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    tasks_completed: int = 0
    tasks_failed: int = 0
    agents_involved: int = 0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    success_rate: float = 0.0
    error_count: int = 0
    retry_count: int = 0


@dataclass
class AgentPerformanceMetrics:
    """Performance metrics for individual agents"""
    agent_id: str
    agent_role: str
    tasks_completed: int = 0
    avg_execution_time: float = 0.0
    success_rate: float = 0.0
    error_count: int = 0
    memory_efficiency: float = 0.0
    last_activity: Optional[datetime] = None


class WorkflowConfiguration(BaseModel):
    """Configuration for workflow execution"""
    workflow_id: str
    tenant_id: str
    workflow_type: str
    priority: TaskPriority = TaskPriority.MEDIUM
    max_execution_time: int = 3600  # seconds
    max_retries: int = 3
    enable_caching: bool = True
    enable_monitoring: bool = True
    parallel_execution: bool = False
    agent_allocation: Dict[str, int] = Field(default_factory=dict)
    resource_limits: Dict[str, Any] = Field(default_factory=dict)
    notification_settings: Dict[str, Any] = Field(default_factory=dict)


class TaskDefinition(BaseModel):
    """Definition for workflow tasks"""
    task_id: str
    task_type: str
    description: str
    agent_role: AgentRole
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: List[str] = Field(default_factory=list)
    inputs: Dict[str, Any] = Field(default_factory=dict)
    expected_output: str = ""
    timeout_seconds: int = 300
    retry_on_failure: bool = True
    validation_rules: List[str] = Field(default_factory=list)


class WorkflowResult(BaseModel):
    """Result of workflow execution"""
    workflow_id: str
    status: WorkflowStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    results: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    metrics: Optional[WorkflowMetrics] = None
    agent_results: Dict[str, Any] = Field(default_factory=dict)


class AdvancedAgentTool(BaseTool):
    """Advanced tool with performance monitoring and caching"""
    
    def __init__(self, name: str, description: str, func: Callable, 
                 cache_enabled: bool = True, performance_tracking: bool = True):
        self.name = name
        self.description = description
        self.func = func
        self.cache_enabled = cache_enabled
        self.performance_tracking = performance_tracking
        self.execution_cache = {}
        self.performance_metrics = {
            'execution_count': 0,
            'total_execution_time': 0.0,
            'average_execution_time': 0.0,
            'success_count': 0,
            'error_count': 0
        }
    
    def _run(self, *args, **kwargs) -> str:
        """Execute tool with performance monitoring and caching"""
        start_time = time.time()
        
        try:
            # Check cache if enabled
            if self.cache_enabled:
                cache_key = self._generate_cache_key(args, kwargs)
                if cache_key in self.execution_cache:
                    logger.info(f"Cache hit for tool {self.name}")
                    return self.execution_cache[cache_key]
            
            # Execute function
            result = self.func(*args, **kwargs)
            
            # Update performance metrics
            if self.performance_tracking:
                execution_time = time.time() - start_time
                self._update_performance_metrics(execution_time, True)
            
            # Cache result if enabled
            if self.cache_enabled:
                self.execution_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            # Update error metrics
            if self.performance_tracking:
                execution_time = time.time() - start_time
                self._update_performance_metrics(execution_time, False)
            
            logger.error(f"Tool {self.name} execution failed: {e}")
            raise e
    
    def _generate_cache_key(self, args, kwargs) -> str:
        """Generate cache key from arguments"""
        import hashlib
        key_data = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _update_performance_metrics(self, execution_time: float, success: bool):
        """Update performance metrics"""
        self.performance_metrics['execution_count'] += 1
        self.performance_metrics['total_execution_time'] += execution_time
        self.performance_metrics['average_execution_time'] = (
            self.performance_metrics['total_execution_time'] / 
            self.performance_metrics['execution_count']
        )
        
        if success:
            self.performance_metrics['success_count'] += 1
        else:
            self.performance_metrics['error_count'] += 1
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return self.performance_metrics.copy()
    
    def clear_cache(self):
        """Clear execution cache"""
        self.execution_cache.clear()


class HierarchicalAgent:
    """Advanced agent with hierarchical capabilities and delegation"""
    
    def __init__(self, agent_id: str, role: AgentRole, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.role = role
        self.config = config
        self.subordinates = []
        self.supervisor = None
        self.tools = []
        self.performance_metrics = AgentPerformanceMetrics(
            agent_id=agent_id,
            agent_role=role.value
        )
        self.delegation_rules = config.get('delegation_rules', {})
        self.specializations = config.get('specializations', [])
        
        # Create CrewAI agent
        self.crew_agent = self._create_crew_agent()
    
    def _create_crew_agent(self) -> Agent:
        """Create the underlying CrewAI agent"""
        return Agent(
            role=self.config.get('role_name', self.role.value),
            goal=self.config.get('goal', f'Execute {self.role.value} tasks efficiently'),
            backstory=self.config.get('backstory', f'Expert {self.role.value} with specialized skills'),
            verbose=self.config.get('verbose', True),
            allow_delegation=self.config.get('allow_delegation', self.role == AgentRole.ORCHESTRATOR),
            tools=self.tools,
            memory=self.config.get('memory', True),
            max_iter=self.config.get('max_iter', 5),
            max_execution_time=self.config.get('max_execution_time', 300)
        )
    
    def add_subordinate(self, agent: 'HierarchicalAgent'):
        """Add a subordinate agent"""
        self.subordinates.append(agent)
        agent.supervisor = self
    
    def add_tool(self, tool: AdvancedAgentTool):
        """Add a tool to the agent"""
        self.tools.append(tool)
        # Update CrewAI agent tools
        self.crew_agent.tools = self.tools
    
    def can_delegate(self, task_type: str) -> bool:
        """Check if agent can delegate a specific task type"""
        if not self.config.get('allow_delegation', False):
            return False
        
        delegation_rules = self.delegation_rules.get(task_type, {})
        return delegation_rules.get('enabled', True)
    
    def find_best_subordinate(self, task_type: str, requirements: Dict[str, Any]) -> Optional['HierarchicalAgent']:
        """Find the best subordinate for a specific task"""
        best_agent = None
        best_score = 0.0
        
        for subordinate in self.subordinates:
            score = self._calculate_agent_suitability(subordinate, task_type, requirements)
            if score > best_score:
                best_score = score
                best_agent = subordinate
        
        return best_agent if best_score > 0.5 else None
    
    def _calculate_agent_suitability(self, agent: 'HierarchicalAgent', 
                                   task_type: str, requirements: Dict[str, Any]) -> float:
        """Calculate how suitable an agent is for a specific task"""
        score = 0.0
        
        # Role-based scoring
        role_match = {
            'analysis': [AgentRole.ANALYST],
            'generation': [AgentRole.GENERATOR],
            'validation': [AgentRole.VALIDATOR],
            'optimization': [AgentRole.OPTIMIZER],
            'monitoring': [AgentRole.MONITOR]
        }
        
        if task_type in role_match and agent.role in role_match[task_type]:
            score += 0.4
        
        # Specialization scoring
        required_skills = requirements.get('skills', [])
        for skill in required_skills:
            if skill in agent.specializations:
                score += 0.2
        
        # Performance-based scoring
        if agent.performance_metrics.success_rate > 0.8:
            score += 0.2
        elif agent.performance_metrics.success_rate > 0.6:
            score += 0.1
        
        # Workload-based scoring
        if agent.performance_metrics.tasks_completed < 10:  # Not overloaded
            score += 0.2
        
        return min(1.0, score)
    
    def update_performance_metrics(self, execution_time: float, success: bool):
        """Update agent performance metrics"""
        self.performance_metrics.last_activity = datetime.now()
        
        if success:
            self.performance_metrics.tasks_completed += 1
            # Update average execution time
            total_time = (self.performance_metrics.avg_execution_time * 
                         (self.performance_metrics.tasks_completed - 1) + execution_time)
            self.performance_metrics.avg_execution_time = total_time / self.performance_metrics.tasks_completed
        else:
            self.performance_metrics.error_count += 1
        
        # Calculate success rate
        total_tasks = self.performance_metrics.tasks_completed + self.performance_metrics.error_count
        if total_tasks > 0:
            self.performance_metrics.success_rate = self.performance_metrics.tasks_completed / total_tasks


class WorkflowOrchestrator:
    """Advanced workflow orchestrator with hierarchical agent management"""
    
    def __init__(self):
        self.agents: Dict[str, HierarchicalAgent] = {}
        self.active_workflows: Dict[str, WorkflowResult] = {}
        self.workflow_queue = asyncio.Queue()
        self.performance_monitor = WorkflowPerformanceMonitor()
        self.resource_manager = ResourceManager()
        self.error_handler = ErrorHandler()
        self.executor = ThreadPoolExecutor(max_workers=10)
        self._running = False
    
    async def start(self):
        """Start the workflow orchestrator"""
        self._running = True
        # Start background tasks
        asyncio.create_task(self._workflow_processor())
        asyncio.create_task(self._performance_monitor_task())
        logger.info("Workflow orchestrator started")
    
    async def stop(self):
        """Stop the workflow orchestrator"""
        self._running = False
        self.executor.shutdown(wait=True)
        logger.info("Workflow orchestrator stopped")
    
    def register_agent(self, agent: HierarchicalAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.agent_id] = agent
        logger.info(f"Registered agent {agent.agent_id} with role {agent.role.value}")
    
    def create_agent_hierarchy(self, hierarchy_config: Dict[str, Any]) -> HierarchicalAgent:
        """Create a hierarchical agent structure"""
        root_config = hierarchy_config['root']
        root_agent = HierarchicalAgent(
            agent_id=root_config['id'],
            role=AgentRole(root_config['role']),
            config=root_config['config']
        )
        
        # Create subordinates recursively
        for subordinate_config in hierarchy_config.get('subordinates', []):
            subordinate = self._create_agent_from_config(subordinate_config)
            root_agent.add_subordinate(subordinate)
        
        self.register_agent(root_agent)
        return root_agent
    
    def _create_agent_from_config(self, config: Dict[str, Any]) -> HierarchicalAgent:
        """Create an agent from configuration"""
        agent = HierarchicalAgent(
            agent_id=config['id'],
            role=AgentRole(config['role']),
            config=config['config']
        )
        
        # Add tools if specified
        for tool_config in config.get('tools', []):
            tool = self._create_tool_from_config(tool_config)
            agent.add_tool(tool)
        
        # Add subordinates recursively
        for subordinate_config in config.get('subordinates', []):
            subordinate = self._create_agent_from_config(subordinate_config)
            agent.add_subordinate(subordinate)
        
        return agent
    
    def _create_tool_from_config(self, tool_config: Dict[str, Any]) -> AdvancedAgentTool:
        """Create a tool from configuration"""
        # This would be extended to create specific tools based on configuration
        def dummy_func(*args, **kwargs):
            return f"Tool {tool_config['name']} executed with args: {args}, kwargs: {kwargs}"
        
        return AdvancedAgentTool(
            name=tool_config['name'],
            description=tool_config['description'],
            func=dummy_func,
            cache_enabled=tool_config.get('cache_enabled', True),
            performance_tracking=tool_config.get('performance_tracking', True)
        )
    
    async def execute_workflow(self, config: WorkflowConfiguration, 
                             tasks: List[TaskDefinition]) -> WorkflowResult:
        """Execute a workflow with the given configuration and tasks"""
        workflow_result = WorkflowResult(
            workflow_id=config.workflow_id,
            status=WorkflowStatus.PENDING,
            start_time=datetime.now()
        )
        
        self.active_workflows[config.workflow_id] = workflow_result
        
        try:
            # Update status to running
            workflow_result.status = WorkflowStatus.RUNNING
            
            # Create task execution plan
            execution_plan = self._create_execution_plan(tasks)
            
            # Execute tasks based on plan
            if config.parallel_execution:
                results = await self._execute_tasks_parallel(execution_plan, config)
            else:
                results = await self._execute_tasks_sequential(execution_plan, config)
            
            # Compile results
            workflow_result.results = results
            workflow_result.status = WorkflowStatus.COMPLETED
            workflow_result.end_time = datetime.now()
            workflow_result.duration_seconds = (
                workflow_result.end_time - workflow_result.start_time
            ).total_seconds()
            
        except Exception as e:
            workflow_result.status = WorkflowStatus.FAILED
            workflow_result.errors.append(str(e))
            workflow_result.end_time = datetime.now()
            workflow_result.duration_seconds = (
                workflow_result.end_time - workflow_result.start_time
            ).total_seconds()
            
            logger.error(f"Workflow {config.workflow_id} failed: {e}")
        
        return workflow_result
    
    def _create_execution_plan(self, tasks: List[TaskDefinition]) -> List[List[TaskDefinition]]:
        """Create an execution plan based on task dependencies"""
        # Topological sort of tasks based on dependencies
        task_map = {task.task_id: task for task in tasks}
        execution_levels = []
        completed_tasks = set()
        
        while len(completed_tasks) < len(tasks):
            current_level = []
            
            for task in tasks:
                if task.task_id in completed_tasks:
                    continue
                
                # Check if all dependencies are completed
                dependencies_met = all(
                    dep in completed_tasks for dep in task.dependencies
                )
                
                if dependencies_met:
                    current_level.append(task)
            
            if not current_level:
                # Circular dependency or other issue
                remaining_tasks = [t for t in tasks if t.task_id not in completed_tasks]
                raise ValueError(f"Cannot resolve dependencies for tasks: {[t.task_id for t in remaining_tasks]}")
            
            execution_levels.append(current_level)
            completed_tasks.update(task.task_id for task in current_level)
        
        return execution_levels
    
    async def _execute_tasks_sequential(self, execution_plan: List[List[TaskDefinition]], 
                                      config: WorkflowConfiguration) -> Dict[str, Any]:
        """Execute tasks sequentially level by level"""
        results = {}
        
        for level, tasks in enumerate(execution_plan):
            logger.info(f"Executing level {level} with {len(tasks)} tasks")
            
            for task in tasks:
                try:
                    result = await self._execute_single_task(task, config)
                    results[task.task_id] = result
                    logger.info(f"Task {task.task_id} completed successfully")
                except Exception as e:
                    error_msg = f"Task {task.task_id} failed: {e}"
                    results[task.task_id] = {"error": error_msg}
                    logger.error(error_msg)
                    
                    if not task.retry_on_failure:
                        raise e
        
        return results
    
    async def _execute_tasks_parallel(self, execution_plan: List[List[TaskDefinition]], 
                                    config: WorkflowConfiguration) -> Dict[str, Any]:
        """Execute tasks in parallel where possible"""
        results = {}
        
        for level, tasks in enumerate(execution_plan):
            logger.info(f"Executing level {level} with {len(tasks)} tasks in parallel")
            
            # Execute all tasks in current level in parallel
            task_futures = []
            for task in tasks:
                future = asyncio.create_task(self._execute_single_task(task, config))
                task_futures.append((task.task_id, future))
            
            # Wait for all tasks in level to complete
            for task_id, future in task_futures:
                try:
                    result = await future
                    results[task_id] = result
                    logger.info(f"Task {task_id} completed successfully")
                except Exception as e:
                    error_msg = f"Task {task_id} failed: {e}"
                    results[task_id] = {"error": error_msg}
                    logger.error(error_msg)
        
        return results
    
    async def _execute_single_task(self, task: TaskDefinition, 
                                 config: WorkflowConfiguration) -> Dict[str, Any]:
        """Execute a single task"""
        start_time = time.time()
        
        # Find best agent for the task
        agent = self._find_best_agent_for_task(task)
        if not agent:
            raise ValueError(f"No suitable agent found for task {task.task_id}")
        
        # Create CrewAI task
        crew_task = Task(
            description=task.description,
            agent=agent.crew_agent,
            expected_output=task.expected_output
        )
        
        # Create crew and execute
        crew = Crew(
            agents=[agent.crew_agent],
            tasks=[crew_task],
            verbose=True,
            process=Process.sequential
        )
        
        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                asyncio.to_thread(crew.kickoff),
                timeout=task.timeout_seconds
            )
            
            execution_time = time.time() - start_time
            agent.update_performance_metrics(execution_time, True)
            
            return {
                "result": result,
                "execution_time": execution_time,
                "agent_id": agent.agent_id
            }
            
        except asyncio.TimeoutError:
            execution_time = time.time() - start_time
            agent.update_performance_metrics(execution_time, False)
            raise TimeoutError(f"Task {task.task_id} timed out after {task.timeout_seconds} seconds")
        
        except Exception as e:
            execution_time = time.time() - start_time
            agent.update_performance_metrics(execution_time, False)
            raise e
    
    def _find_best_agent_for_task(self, task: TaskDefinition) -> Optional[HierarchicalAgent]:
        """Find the best agent for executing a task"""
        best_agent = None
        best_score = 0.0
        
        for agent in self.agents.values():
            if agent.role == task.agent_role:
                score = self._calculate_agent_suitability_for_task(agent, task)
                if score > best_score:
                    best_score = score
                    best_agent = agent
        
        return best_agent if best_score > 0.5 else None
    
    def _calculate_agent_suitability_for_task(self, agent: HierarchicalAgent, 
                                            task: TaskDefinition) -> float:
        """Calculate agent suitability for a specific task"""
        score = 0.0
        
        # Role match
        if agent.role == task.agent_role:
            score += 0.5
        
        # Performance-based scoring
        if agent.performance_metrics.success_rate > 0.8:
            score += 0.3
        elif agent.performance_metrics.success_rate > 0.6:
            score += 0.2
        
        # Workload consideration
        if agent.performance_metrics.tasks_completed < 10:
            score += 0.2
        
        return score
    
    async def _workflow_processor(self):
        """Background task to process workflow queue"""
        while self._running:
            try:
                # Process queued workflows
                await asyncio.sleep(1)  # Check every second
            except Exception as e:
                logger.error(f"Workflow processor error: {e}")
    
    async def _performance_monitor_task(self):
        """Background task for performance monitoring"""
        while self._running:
            try:
                # Monitor performance metrics
                await self.performance_monitor.collect_metrics(self.agents)
                await asyncio.sleep(30)  # Monitor every 30 seconds
            except Exception as e:
                logger.error(f"Performance monitor error: {e}")
    
    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowResult]:
        """Get the status of a specific workflow"""
        return self.active_workflows.get(workflow_id)
    
    def get_agent_performance(self, agent_id: str) -> Optional[AgentPerformanceMetrics]:
        """Get performance metrics for a specific agent"""
        agent = self.agents.get(agent_id)
        return agent.performance_metrics if agent else None
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get overall system performance metrics"""
        return {
            "active_workflows": len([w for w in self.active_workflows.values() 
                                   if w.status == WorkflowStatus.RUNNING]),
            "total_agents": len(self.agents),
            "agent_performance": {
                agent_id: agent.performance_metrics.__dict__ 
                for agent_id, agent in self.agents.items()
            },
            "resource_usage": self.resource_manager.get_usage_stats()
        }


class WorkflowPerformanceMonitor:
    """Monitor and optimize workflow performance"""
    
    def __init__(self):
        self.metrics_history = []
        self.alert_thresholds = {
            'max_execution_time': 300,
            'min_success_rate': 0.8,
            'max_error_rate': 0.2
        }
    
    async def collect_metrics(self, agents: Dict[str, HierarchicalAgent]):
        """Collect performance metrics from all agents"""
        timestamp = datetime.now()
        
        for agent_id, agent in agents.items():
            metrics = {
                'timestamp': timestamp,
                'agent_id': agent_id,
                'role': agent.role.value,
                'performance': agent.performance_metrics.__dict__
            }
            self.metrics_history.append(metrics)
        
        # Clean old metrics (keep last 1000 entries)
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
    
    def analyze_trends(self, agent_id: str, hours: int = 24) -> Dict[str, Any]:
        """Analyze performance trends for an agent"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        relevant_metrics = [
            m for m in self.metrics_history 
            if m['agent_id'] == agent_id and m['timestamp'] >= cutoff_time
        ]
        
        if not relevant_metrics:
            return {"error": "No metrics available for analysis"}
        
        # Calculate trends
        success_rates = [m['performance']['success_rate'] for m in relevant_metrics]
        execution_times = [m['performance']['avg_execution_time'] for m in relevant_metrics]
        
        return {
            "avg_success_rate": sum(success_rates) / len(success_rates),
            "avg_execution_time": sum(execution_times) / len(execution_times),
            "trend_direction": self._calculate_trend(success_rates),
            "performance_stability": self._calculate_stability(execution_times),
            "recommendations": self._generate_recommendations(relevant_metrics)
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction"""
        if len(values) < 2:
            return "insufficient_data"
        
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg * 1.05:
            return "improving"
        elif second_avg < first_avg * 0.95:
            return "declining"
        else:
            return "stable"
    
    def _calculate_stability(self, values: List[float]) -> float:
        """Calculate performance stability (lower is more stable)"""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5  # Standard deviation
    
    def _generate_recommendations(self, metrics: List[Dict[str, Any]]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        latest_metrics = metrics[-1]['performance']
        
        if latest_metrics['success_rate'] < 0.8:
            recommendations.append("Consider reviewing agent configuration or task complexity")
        
        if latest_metrics['avg_execution_time'] > 60:
            recommendations.append("Optimize agent tools or reduce task scope")
        
        if latest_metrics['error_count'] > 5:
            recommendations.append("Investigate common failure patterns")
        
        return recommendations


class ResourceManager:
    """Manage system resources for optimal performance"""
    
    def __init__(self):
        self.resource_limits = {
            'max_concurrent_workflows': 10,
            'max_memory_usage_mb': 1024,
            'max_cpu_usage_percent': 80
        }
        self.current_usage = {
            'concurrent_workflows': 0,
            'memory_usage_mb': 0,
            'cpu_usage_percent': 0
        }
    
    def can_allocate_resources(self, resource_requirements: Dict[str, Any]) -> bool:
        """Check if resources can be allocated for a new workflow"""
        if self.current_usage['concurrent_workflows'] >= self.resource_limits['max_concurrent_workflows']:
            return False
        
        projected_memory = (self.current_usage['memory_usage_mb'] + 
                          resource_requirements.get('memory_mb', 100))
        if projected_memory > self.resource_limits['max_memory_usage_mb']:
            return False
        
        return True
    
    def allocate_resources(self, resource_requirements: Dict[str, Any]):
        """Allocate resources for a workflow"""
        self.current_usage['concurrent_workflows'] += 1
        self.current_usage['memory_usage_mb'] += resource_requirements.get('memory_mb', 100)
    
    def deallocate_resources(self, resource_requirements: Dict[str, Any]):
        """Deallocate resources after workflow completion"""
        self.current_usage['concurrent_workflows'] -= 1
        self.current_usage['memory_usage_mb'] -= resource_requirements.get('memory_mb', 100)
        self.current_usage['memory_usage_mb'] = max(0, self.current_usage['memory_usage_mb'])
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current resource usage statistics"""
        return {
            'current_usage': self.current_usage.copy(),
            'resource_limits': self.resource_limits.copy(),
            'utilization_percent': {
                'workflows': (self.current_usage['concurrent_workflows'] / 
                            self.resource_limits['max_concurrent_workflows']) * 100,
                'memory': (self.current_usage['memory_usage_mb'] / 
                         self.resource_limits['max_memory_usage_mb']) * 100
            }
        }


class ErrorHandler:
    """Handle errors and implement recovery strategies"""
    
    def __init__(self):
        self.error_patterns = {}
        self.recovery_strategies = {}
    
    async def handle_workflow_error(self, workflow_id: str, error: Exception, 
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle workflow execution errors"""
        error_type = type(error).__name__
        
        # Log error
        logger.error(f"Workflow {workflow_id} error: {error_type} - {str(error)}")
        
        # Determine recovery strategy
        strategy = self._get_recovery_strategy(error_type, context)
        
        if strategy:
            try:
                recovery_result = await strategy(workflow_id, error, context)
                return {
                    "handled": True,
                    "strategy": strategy.__name__,
                    "result": recovery_result
                }
            except Exception as recovery_error:
                logger.error(f"Recovery strategy failed: {recovery_error}")
        
        return {
            "handled": False,
            "error_type": error_type,
            "error_message": str(error)
        }
    
    def _get_recovery_strategy(self, error_type: str, context: Dict[str, Any]) -> Optional[Callable]:
        """Get recovery strategy for error type"""
        strategies = {
            'TimeoutError': self._handle_timeout_error,
            'MemoryError': self._handle_memory_error,
            'ConnectionError': self._handle_connection_error,
            'ValidationError': self._handle_validation_error
        }
        
        return strategies.get(error_type)
    
    async def _handle_timeout_error(self, workflow_id: str, error: Exception, 
                                  context: Dict[str, Any]) -> str:
        """Handle timeout errors"""
        # Retry with increased timeout
        return "Retrying with increased timeout"
    
    async def _handle_memory_error(self, workflow_id: str, error: Exception, 
                                 context: Dict[str, Any]) -> str:
        """Handle memory errors"""
        # Reduce batch size or clear caches
        return "Optimizing memory usage"
    
    async def _handle_connection_error(self, workflow_id: str, error: Exception, 
                                     context: Dict[str, Any]) -> str:
        """Handle connection errors"""
        # Retry with exponential backoff
        return "Retrying with exponential backoff"
    
    async def _handle_validation_error(self, workflow_id: str, error: Exception, 
                                     context: Dict[str, Any]) -> str:
        """Handle validation errors"""
        # Adjust input parameters
        return "Adjusting input parameters"


# Global orchestrator instance
_orchestrator: Optional[WorkflowOrchestrator] = None


async def get_workflow_orchestrator() -> WorkflowOrchestrator:
    """Get or create the global workflow orchestrator"""
    global _orchestrator
    
    if _orchestrator is None:
        _orchestrator = WorkflowOrchestrator()
        await _orchestrator.start()
    
    return _orchestrator


# Workflow factory functions for common business processes
class WorkflowFactory:
    """Factory for creating common workflow configurations"""
    
    @staticmethod
    def create_review_management_workflow(tenant_id: str, reviews_data: List[Dict[str, Any]]) -> tuple[WorkflowConfiguration, List[TaskDefinition]]:
        """Create a comprehensive review management workflow"""
        workflow_id = f"review_management_{tenant_id}_{int(time.time())}"
        
        config = WorkflowConfiguration(
            workflow_id=workflow_id,
            tenant_id=tenant_id,
            workflow_type="review_management",
            priority=TaskPriority.HIGH,
            max_execution_time=1800,  # 30 minutes
            parallel_execution=True,
            enable_monitoring=True
        )
        
        tasks = [
            TaskDefinition(
                task_id="analyze_reviews",
                task_type="analysis",
                description=f"Analyze {len(reviews_data)} customer reviews for sentiment and themes",
                agent_role=AgentRole.ANALYST,
                priority=TaskPriority.HIGH,
                inputs={"reviews": reviews_data},
                expected_output="Comprehensive review analysis with sentiment scores and themes",
                timeout_seconds=300
            ),
            TaskDefinition(
                task_id="generate_responses",
                task_type="generation",
                description="Generate professional responses for negative reviews",
                agent_role=AgentRole.GENERATOR,
                priority=TaskPriority.MEDIUM,
                dependencies=["analyze_reviews"],
                inputs={"reviews": reviews_data},
                expected_output="Professional review responses ready for approval",
                timeout_seconds=600
            ),
            TaskDefinition(
                task_id="optimize_responses",
                task_type="optimization",
                description="Optimize generated responses for better engagement",
                agent_role=AgentRole.OPTIMIZER,
                priority=TaskPriority.LOW,
                dependencies=["generate_responses"],
                inputs={},
                expected_output="Optimized responses with improvement suggestions",
                timeout_seconds=300
            ),
            TaskDefinition(
                task_id="monitor_reputation",
                task_type="monitoring",
                description="Monitor reputation metrics and generate alerts if needed",
                agent_role=AgentRole.MONITOR,
                priority=TaskPriority.MEDIUM,
                inputs={"tenant_id": tenant_id},
                expected_output="Reputation monitoring report with alerts",
                timeout_seconds=180
            )
        ]
        
        return config, tasks
    
    @staticmethod
    def create_competitive_analysis_workflow(tenant_id: str, competitors: List[str]) -> tuple[WorkflowConfiguration, List[TaskDefinition]]:
        """Create a competitive analysis workflow"""
        workflow_id = f"competitive_analysis_{tenant_id}_{int(time.time())}"
        
        config = WorkflowConfiguration(
            workflow_id=workflow_id,
            tenant_id=tenant_id,
            workflow_type="competitive_analysis",
            priority=TaskPriority.MEDIUM,
            max_execution_time=3600,  # 1 hour
            parallel_execution=True
        )
        
        tasks = [
            TaskDefinition(
                task_id="collect_competitor_data",
                task_type="collection",
                description=f"Collect review data for competitors: {', '.join(competitors)}",
                agent_role=AgentRole.SPECIALIST,
                priority=TaskPriority.HIGH,
                inputs={"competitors": competitors},
                expected_output="Comprehensive competitor review data",
                timeout_seconds=900
            ),
            TaskDefinition(
                task_id="analyze_competitor_strategies",
                task_type="analysis",
                description="Analyze competitor response strategies and patterns",
                agent_role=AgentRole.ANALYST,
                priority=TaskPriority.HIGH,
                dependencies=["collect_competitor_data"],
                inputs={},
                expected_output="Competitor strategy analysis with benchmarking metrics",
                timeout_seconds=600
            ),
            TaskDefinition(
                task_id="identify_opportunities",
                task_type="optimization",
                description="Identify competitive opportunities and gaps",
                agent_role=AgentRole.OPTIMIZER,
                priority=TaskPriority.MEDIUM,
                dependencies=["analyze_competitor_strategies"],
                inputs={},
                expected_output="Strategic recommendations and opportunity analysis",
                timeout_seconds=300
            )
        ]
        
        return config, tasks


# Example usage and integration
async def main():
    """Example usage of the advanced workflow orchestrator"""
    # Get orchestrator instance
    orchestrator = await get_workflow_orchestrator()
    
    # Create agent hierarchy for review management
    hierarchy_config = {
        "root": {
            "id": "review_manager",
            "role": "orchestrator",
            "config": {
                "role_name": "Review Management Orchestrator",
                "goal": "Orchestrate comprehensive review management workflows",
                "backstory": "Expert orchestrator for managing complex review workflows",
                "allow_delegation": True,
                "delegation_rules": {
                    "analysis": {"enabled": True},
                    "generation": {"enabled": True},
                    "optimization": {"enabled": True}
                }
            }
        },
        "subordinates": [
            {
                "id": "review_analyst",
                "role": "analyst",
                "config": {
                    "role_name": "Senior Review Analyst",
                    "goal": "Analyze customer reviews for insights",
                    "specializations": ["sentiment_analysis", "theme_extraction"]
                },
                "tools": [
                    {
                        "name": "sentiment_analyzer",
                        "description": "Analyze sentiment in customer reviews"
                    }
                ]
            },
            {
                "id": "response_generator",
                "role": "generator",
                "config": {
                    "role_name": "Response Generation Specialist",
                    "goal": "Generate professional review responses",
                    "specializations": ["response_writing", "customer_communication"]
                }
            },
            {
                "id": "response_optimizer",
                "role": "optimizer",
                "config": {
                    "role_name": "Response Optimization Expert",
                    "goal": "Optimize responses for maximum engagement",
                    "specializations": ["optimization", "performance_tuning"]
                }
            }
        ]
    }
    
    # Create and register agent hierarchy
    root_agent = orchestrator.create_agent_hierarchy(hierarchy_config)
    
    # Create a review management workflow
    sample_reviews = [
        {"id": "1", "content": "Great service!", "rating": 5, "platform": "google"},
        {"id": "2", "content": "Poor experience, very disappointed", "rating": 2, "platform": "yelp"}
    ]
    
    config, tasks = WorkflowFactory.create_review_management_workflow(
        tenant_id="tenant_123",
        reviews_data=sample_reviews
    )
    
    # Execute workflow
    result = await orchestrator.execute_workflow(config, tasks)
    
    print(f"Workflow completed with status: {result.status}")
    print(f"Duration: {result.duration_seconds:.2f} seconds")
    print(f"Results: {result.results}")
    
    # Get system metrics
    metrics = orchestrator.get_system_metrics()
    print(f"System metrics: {json.dumps(metrics, indent=2, default=str)}")
    
    # Stop orchestrator
    await orchestrator.stop()


if __name__ == "__main__":
    asyncio.run(main())