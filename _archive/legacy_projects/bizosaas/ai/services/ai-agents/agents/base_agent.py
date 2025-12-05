"""
Base Agent Class for Centralized BizOSaas AI Agents
Provides common functionality and integration patterns
"""

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from abc import ABC, abstractmethod

from pydantic import BaseModel, Field
import structlog

# Shared imports
import sys
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from shared.database.connection import get_postgres_session, get_redis_client
from shared.events.event_bus import EventBus, EventFactory, EventType
from shared.auth.jwt_auth import UserContext

# Cross-client learning imports
from .cross_client_learning import (
    CrossClientLearningEngine, 
    LearningPatternType, 
    get_cross_client_insights,
    learning_engine
)

# Configure structured logging
logger = structlog.get_logger(__name__)

class AgentRole(str, Enum):
    MARKETING = "marketing"
    ECOMMERCE = "ecommerce" 
    ANALYTICS = "analytics"
    OPERATIONS = "operations"
    WORKFLOW = "workflow"

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class AgentTaskRequest(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    user_id: str
    task_type: str
    input_data: Dict[str, Any]
    priority: TaskPriority = TaskPriority.NORMAL
    timeout_seconds: int = 300
    callback_url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentTaskResponse(BaseModel):
    task_id: str
    agent_name: str
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time_ms: int
    timestamp: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BaseAgent(ABC):
    """Base class for all BizOSaas AI agents"""
    
    def __init__(
        self,
        agent_name: str,
        agent_role: AgentRole,
        description: str,
        version: str = "1.0.0"
    ):
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.description = description
        self.version = version
        self.logger = structlog.get_logger().bind(agent=agent_name)
        
        # Integration components
        self.event_bus: Optional[EventBus] = None
        self.redis_client = None
        self.postgres_session = None
        
        # Cross-client learning
        self.learning_enabled = True
        self.learning_engine: Optional[CrossClientLearningEngine] = None
        
        # Performance tracking
        self.task_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.avg_execution_time = 0.0
        
    async def initialize(self):
        """Initialize agent with required services"""
        try:
            self.redis_client = await get_redis_client()
            self.event_bus = EventBus(self.redis_client)
            
            # Initialize cross-client learning engine
            if self.learning_enabled:
                self.learning_engine = learning_engine
                await self.learning_engine.initialize()
                
            self.logger.info("Agent initialized successfully", 
                           agent=self.agent_name, 
                           learning_enabled=self.learning_enabled)
        except Exception as e:
            self.logger.error("Failed to initialize agent", agent=self.agent_name, error=str(e))
            raise
    
    async def execute_task(self, task_request: AgentTaskRequest) -> AgentTaskResponse:
        """Execute an agent task with full monitoring and error handling"""
        start_time = datetime.now(timezone.utc)
        execution_start = asyncio.get_event_loop().time()
        
        self.logger.info(
            "Starting task execution",
            task_id=task_request.task_id,
            task_type=task_request.task_type,
            tenant_id=task_request.tenant_id
        )
        
        try:
            # Validate tenant access and permissions
            await self._validate_tenant_access(task_request.tenant_id, task_request.user_id)
            
            # Update task status to running
            await self._update_task_status(task_request.task_id, TaskStatus.RUNNING)
            
            # Execute the actual agent logic
            result = await self._execute_agent_logic(task_request)
            
            # Calculate execution time
            execution_time_ms = int((asyncio.get_event_loop().time() - execution_start) * 1000)
            
            # Create successful response
            response = AgentTaskResponse(
                task_id=task_request.task_id,
                agent_name=self.agent_name,
                status=TaskStatus.COMPLETED,
                result=result,
                execution_time_ms=execution_time_ms,
                timestamp=start_time,
                metadata={
                    "agent_role": self.agent_role.value,
                    "agent_version": self.version,
                    "tenant_id": task_request.tenant_id
                }
            )
            
            # Update performance metrics
            await self._update_performance_metrics(execution_time_ms, True)
            
            # Publish completion event
            await self._publish_task_completion_event(task_request, response)
            
            # Capture cross-client learning pattern (if enabled)
            if self.learning_enabled and self.learning_engine and result:
                try:
                    effectiveness_metrics = await self._calculate_effectiveness_metrics(
                        task_request, result, execution_time_ms
                    )
                    
                    # Create user context for learning
                    user_context = UserContext(
                        user_id=task_request.user_id,
                        tenant_id=task_request.tenant_id
                    )
                    
                    await self.learning_engine.capture_learning_pattern(
                        tenant_id=task_request.tenant_id,
                        agent_role=self.agent_role.value,
                        task_type=task_request.task_type,
                        input_data=task_request.input_data,
                        output_data=result,
                        effectiveness_metrics=effectiveness_metrics,
                        user_context=user_context
                    )
                    
                    self.logger.info("Learning pattern captured", task_id=task_request.task_id)
                    
                except Exception as e:
                    # Learning failure shouldn't affect task success
                    self.logger.warning("Failed to capture learning pattern", 
                                      task_id=task_request.task_id, 
                                      error=str(e))
            
            self.logger.info(
                "Task completed successfully",
                task_id=task_request.task_id,
                execution_time_ms=execution_time_ms
            )
            
            return response
            
        except Exception as e:
            execution_time_ms = int((asyncio.get_event_loop().time() - execution_start) * 1000)
            
            # Create error response
            response = AgentTaskResponse(
                task_id=task_request.task_id,
                agent_name=self.agent_name,
                status=TaskStatus.FAILED,
                error_message=str(e),
                execution_time_ms=execution_time_ms,
                timestamp=start_time,
                metadata={
                    "agent_role": self.agent_role.value,
                    "agent_version": self.version,
                    "tenant_id": task_request.tenant_id
                }
            )
            
            # Update performance metrics
            await self._update_performance_metrics(execution_time_ms, False)
            
            # Publish error event
            await self._publish_task_error_event(task_request, response)
            
            self.logger.error(
                "Task execution failed",
                task_id=task_request.task_id,
                error=str(e),
                execution_time_ms=execution_time_ms
            )
            
            return response
    
    @abstractmethod
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Abstract method for agent-specific logic implementation"""
        pass
    
    async def _validate_tenant_access(self, tenant_id: str, user_id: str):
        """Validate that user has access to the tenant"""
        try:
            async with get_postgres_session() as session:
                # Implement tenant access validation logic
                # This would query the user_management.tenants and user_management.users tables
                pass
        except Exception as e:
            raise PermissionError(f"Tenant access validation failed: {str(e)}")
    
    async def _update_task_status(self, task_id: str, status: TaskStatus):
        """Update task status in Redis for real-time monitoring"""
        if self.redis_client:
            await self.redis_client.set(
                f"agent_task:{task_id}:status",
                status.value,
                ex=3600  # 1 hour expiration
            )
    
    async def _update_performance_metrics(self, execution_time_ms: int, success: bool):
        """Update agent performance metrics"""
        self.task_count += 1
        
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
            
        # Update average execution time
        self.avg_execution_time = (
            (self.avg_execution_time * (self.task_count - 1) + execution_time_ms) / 
            self.task_count
        )
        
        # Store metrics in Redis
        if self.redis_client:
            metrics = {
                "task_count": self.task_count,
                "success_count": self.success_count,
                "failure_count": self.failure_count,
                "avg_execution_time": self.avg_execution_time,
                "success_rate": self.success_count / self.task_count if self.task_count > 0 else 0
            }
            
            await self.redis_client.hset(
                f"agent_metrics:{self.agent_name}",
                mapping=metrics
            )
    
    async def _publish_task_completion_event(self, task_request: AgentTaskRequest, response: AgentTaskResponse):
        """Publish task completion event to event bus"""
        if self.event_bus:
            event = EventFactory.create_custom_event(
                event_type="AGENT_TASK_COMPLETED",
                tenant_id=task_request.tenant_id,
                data={
                    "task_id": task_request.task_id,
                    "agent_name": self.agent_name,
                    "agent_role": self.agent_role.value,
                    "execution_time_ms": response.execution_time_ms,
                    "task_type": task_request.task_type
                }
            )
            await self.event_bus.publish(event)
    
    async def _publish_task_error_event(self, task_request: AgentTaskRequest, response: AgentTaskResponse):
        """Publish task error event to event bus"""
        if self.event_bus:
            event = EventFactory.create_custom_event(
                event_type="AGENT_TASK_FAILED",
                tenant_id=task_request.tenant_id,
                data={
                    "task_id": task_request.task_id,
                    "agent_name": self.agent_name,
                    "agent_role": self.agent_role.value,
                    "error_message": response.error_message,
                    "execution_time_ms": response.execution_time_ms,
                    "task_type": task_request.task_type
                }
            )
            await self.event_bus.publish(event)
    
    async def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information and current metrics"""
        return {
            "agent_name": self.agent_name,
            "agent_role": self.agent_role.value,
            "description": self.description,
            "version": self.version,
            "performance_metrics": {
                "task_count": self.task_count,
                "success_count": self.success_count,
                "failure_count": self.failure_count,
                "avg_execution_time_ms": self.avg_execution_time,
                "success_rate": self.success_count / self.task_count if self.task_count > 0 else 0
            },
            "status": "active"
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform agent health check"""
        try:
            # Check Redis connection
            redis_healthy = False
            if self.redis_client:
                await self.redis_client.ping()
                redis_healthy = True
            
            # Check event bus
            event_bus_healthy = self.event_bus is not None
            
            return {
                "agent_name": self.agent_name,
                "status": "healthy" if redis_healthy and event_bus_healthy else "unhealthy",
                "checks": {
                    "redis_connection": redis_healthy,
                    "event_bus": event_bus_healthy
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            return {
                "agent_name": self.agent_name,
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    async def _calculate_effectiveness_metrics(
        self, 
        task_request: AgentTaskRequest, 
        result: Dict[str, Any], 
        execution_time_ms: int
    ) -> Dict[str, float]:
        """Calculate effectiveness metrics for learning patterns"""
        try:
            # Base metrics from execution
            base_score = 0.8 if execution_time_ms < 30000 else 0.6  # Good if under 30 seconds
            
            # Result-specific scoring
            result_quality_score = 1.0
            if isinstance(result, dict):
                if result.get('confidence_score'):
                    result_quality_score = float(result['confidence_score'])
                elif result.get('success', True):
                    result_quality_score = 0.9
                else:
                    result_quality_score = 0.3
            
            # Priority-based weighting
            priority_weight = {
                TaskPriority.URGENT: 1.0,
                TaskPriority.HIGH: 0.9,
                TaskPriority.NORMAL: 0.8,
                TaskPriority.LOW: 0.7
            }.get(task_request.priority, 0.8)
            
            overall_score = (base_score * 0.3) + (result_quality_score * 0.5) + (priority_weight * 0.2)
            
            return {
                'overall_score': overall_score,
                'execution_speed_score': base_score,
                'result_quality_score': result_quality_score,
                'priority_weight': priority_weight
            }
            
        except Exception as e:
            self.logger.warning(f"Failed to calculate effectiveness metrics: {e}")
            return {'overall_score': 0.5}  # Default moderate score
    
    async def get_cross_client_insights(
        self,
        task_request: AgentTaskRequest
    ) -> List[Dict[str, Any]]:
        """Get relevant cross-client insights before executing a task"""
        if not self.learning_enabled or not self.learning_engine:
            return []
        
        try:
            insights = await self.learning_engine.get_relevant_insights(
                tenant_id=task_request.tenant_id,
                agent_role=self.agent_role.value,
                task_type=task_request.task_type,
                context=task_request.input_data
            )
            
            self.logger.info(
                f"Retrieved {len(insights)} cross-client insights",
                task_id=task_request.task_id
            )
            
            return insights
            
        except Exception as e:
            self.logger.warning(f"Failed to get cross-client insights: {e}")
            return []
    
    async def validate_learning_effectiveness(
        self,
        pattern_id: str,
        tenant_id: str,
        actual_results: Dict[str, float]
    ):
        """Validate the effectiveness of a learning pattern based on real results"""
        if not self.learning_enabled or not self.learning_engine:
            return
        
        try:
            await self.learning_engine.validate_pattern_effectiveness(
                pattern_id, tenant_id, actual_results
            )
            
            self.logger.info(
                "Learning pattern effectiveness validated",
                pattern_id=pattern_id,
                tenant_id=tenant_id
            )
            
        except Exception as e:
            self.logger.warning(f"Failed to validate learning effectiveness: {e}")