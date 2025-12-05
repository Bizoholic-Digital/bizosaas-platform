"""
Real-time AI Agent Activity Monitoring System
Comprehensive tracking for all CrewAI agents across BizOSaas
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from collections import defaultdict
import threading

# WebSocket and Redis imports
import websockets
import redis.asyncio as redis

logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    WAITING_TOOL = "waiting_tool"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"

class TaskType(Enum):
    """Types of tasks agents can perform"""
    CLASSIFICATION = "classification"
    KEYWORD_RESEARCH = "keyword_research"
    CONTENT_GENERATION = "content_generation"
    PRODUCT_SOURCING = "product_sourcing"
    MARKET_ANALYSIS = "market_analysis"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    SOCIAL_MEDIA = "social_media"
    EMAIL_CAMPAIGN = "email_campaign"
    REPORT_GENERATION = "report_generation"
    AUTOMATION = "automation"

@dataclass
class AgentTask:
    """Individual agent task tracking"""
    task_id: str
    agent_name: str
    task_type: TaskType
    status: AgentStatus
    project: str  # coreldove, bizoholic, thrillring, etc.
    tenant_id: str
    user_id: str
    started_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    duration: Optional[float] = None  # seconds
    input_data: Dict[str, Any] = None
    output_data: Dict[str, Any] = None
    error_message: Optional[str] = None
    tools_used: List[str] = None
    tokens_used: Optional[int] = None
    cost_estimate: Optional[float] = None
    progress_percentage: int = 0
    current_step: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        # Convert datetime objects to ISO strings
        data['started_at'] = self.started_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        if self.completed_at:
            data['completed_at'] = self.completed_at.isoformat()
        # Convert enums to strings
        data['status'] = self.status.value
        data['task_type'] = self.task_type.value
        return data

class AgentActivityMonitor:
    """
    Real-time monitoring system for AI agents
    Tracks performance, usage, and provides live dashboard data
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_client = None
        self.active_tasks: Dict[str, AgentTask] = {}
        self.completed_tasks: List[AgentTask] = []
        self.websocket_connections: Set[websockets.WebSocketServerProtocol] = set()
        self.statistics = {
            "total_tasks": 0,
            "active_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "average_duration": 0.0,
            "total_tokens_used": 0,
            "total_cost": 0.0,
            "agents_by_project": defaultdict(int),
            "tasks_by_type": defaultdict(int),
            "hourly_activity": defaultdict(int)
        }
        
    async def initialize(self):
        """Initialize Redis connection and load historical data"""
        try:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            await self.redis_client.ping()
            logger.info("Agent monitor connected to Redis")
            
            # Load active tasks from Redis
            await self._load_active_tasks()
            
        except Exception as e:
            logger.error(f"Failed to initialize agent monitor: {e}")
            # Continue without Redis for basic functionality
            
    async def start_task(self, 
                        agent_name: str,
                        task_type: TaskType,
                        project: str,
                        tenant_id: str,
                        user_id: str,
                        input_data: Dict[str, Any] = None) -> str:
        """Start tracking a new agent task"""
        
        task_id = str(uuid.uuid4())
        task = AgentTask(
            task_id=task_id,
            agent_name=agent_name,
            task_type=task_type,
            status=AgentStatus.STARTING,
            project=project,
            tenant_id=tenant_id,
            user_id=user_id,
            started_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            input_data=input_data or {},
            tools_used=[]
        )
        
        self.active_tasks[task_id] = task
        self.statistics["total_tasks"] += 1
        self.statistics["active_tasks"] += 1
        self.statistics["agents_by_project"][project] += 1
        self.statistics["tasks_by_type"][task_type.value] += 1
        
        # Store in Redis
        if self.redis_client:
            await self.redis_client.hset(
                "bizosaas:active_tasks",
                task_id,
                json.dumps(task.to_dict())
            )
        
        # Broadcast to WebSocket clients
        await self._broadcast_update("task_started", task.to_dict())
        
        logger.info(f"Started tracking task {task_id}: {agent_name} ({task_type.value})")
        return task_id
    
    async def update_task_status(self,
                               task_id: str,
                               status: AgentStatus,
                               progress_percentage: int = 0,
                               current_step: str = "",
                               tools_used: List[str] = None,
                               tokens_used: int = None,
                               error_message: str = None):
        """Update task status and progress"""
        
        if task_id not in self.active_tasks:
            logger.warning(f"Task {task_id} not found for status update")
            return
        
        task = self.active_tasks[task_id]
        task.status = status
        task.updated_at = datetime.now(timezone.utc)
        task.progress_percentage = progress_percentage
        task.current_step = current_step
        
        if tools_used:
            task.tools_used.extend(tools_used)
        
        if tokens_used:
            task.tokens_used = (task.tokens_used or 0) + tokens_used
            self.statistics["total_tokens_used"] += tokens_used
        
        if error_message:
            task.error_message = error_message
        
        # Update in Redis
        if self.redis_client:
            await self.redis_client.hset(
                "bizosaas:active_tasks",
                task_id,
                json.dumps(task.to_dict())
            )
        
        # Broadcast update
        await self._broadcast_update("task_updated", task.to_dict())
        
        logger.debug(f"Updated task {task_id}: {status.value} ({progress_percentage}%)")
    
    async def complete_task(self,
                          task_id: str,
                          output_data: Dict[str, Any] = None,
                          success: bool = True):
        """Mark task as completed"""
        
        if task_id not in self.active_tasks:
            logger.warning(f"Task {task_id} not found for completion")
            return
        
        task = self.active_tasks[task_id]
        task.completed_at = datetime.now(timezone.utc)
        task.duration = (task.completed_at - task.started_at).total_seconds()
        task.status = AgentStatus.COMPLETED if success else AgentStatus.FAILED
        task.output_data = output_data or {}
        task.progress_percentage = 100 if success else task.progress_percentage
        
        # Update statistics
        self.statistics["active_tasks"] -= 1
        if success:
            self.statistics["completed_tasks"] += 1
        else:
            self.statistics["failed_tasks"] += 1
        
        # Update average duration
        total_completed = self.statistics["completed_tasks"] + self.statistics["failed_tasks"]
        if total_completed > 0:
            total_duration = sum(t.duration for t in self.completed_tasks if t.duration) + task.duration
            self.statistics["average_duration"] = total_duration / total_completed
        
        # Move to completed tasks
        self.completed_tasks.append(task)
        del self.active_tasks[task_id]
        
        # Keep only recent completed tasks in memory (last 100)
        if len(self.completed_tasks) > 100:
            self.completed_tasks = self.completed_tasks[-100:]
        
        # Update Redis
        if self.redis_client:
            await self.redis_client.hdel("bizosaas:active_tasks", task_id)
            await self.redis_client.hset(
                "bizosaas:completed_tasks",
                task_id,
                json.dumps(task.to_dict())
            )
        
        # Broadcast completion
        await self._broadcast_update("task_completed", task.to_dict())
        
        logger.info(f"Completed task {task_id}: {task.agent_name} in {task.duration:.2f}s")
    
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        
        # Calculate real-time metrics
        current_hour = datetime.now(timezone.utc).hour
        self.statistics["hourly_activity"][current_hour] = len(self.active_tasks)
        
        # Get recent activity (last 10 tasks)
        recent_activity = []
        all_tasks = list(self.active_tasks.values()) + self.completed_tasks[-10:]
        all_tasks.sort(key=lambda x: x.updated_at, reverse=True)
        
        for task in all_tasks[:10]:
            recent_activity.append({
                "task_id": task.task_id,
                "agent_name": task.agent_name,
                "task_type": task.task_type.value,
                "status": task.status.value,
                "project": task.project,
                "progress": task.progress_percentage,
                "duration": task.duration,
                "updated_at": task.updated_at.isoformat()
            })
        
        # Get active tasks by status
        active_by_status = defaultdict(int)
        for task in self.active_tasks.values():
            active_by_status[task.status.value] += 1
        
        return {
            "statistics": dict(self.statistics),
            "active_tasks": len(self.active_tasks),
            "active_by_status": dict(active_by_status),
            "recent_activity": recent_activity,
            "agent_performance": self._get_agent_performance(),
            "project_breakdown": dict(self.statistics["agents_by_project"]),
            "task_type_breakdown": dict(self.statistics["tasks_by_type"]),
            "hourly_activity": dict(self.statistics["hourly_activity"]),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def _get_agent_performance(self) -> List[Dict[str, Any]]:
        """Calculate performance metrics for each agent"""
        
        agent_stats = defaultdict(lambda: {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "average_duration": 0.0,
            "success_rate": 0.0,
            "total_tokens": 0
        })
        
        # Analyze completed tasks
        for task in self.completed_tasks:
            stats = agent_stats[task.agent_name]
            stats["total_tasks"] += 1
            
            if task.status == AgentStatus.COMPLETED:
                stats["completed_tasks"] += 1
            else:
                stats["failed_tasks"] += 1
                
            if task.duration:
                stats["average_duration"] += task.duration
                
            if task.tokens_used:
                stats["total_tokens"] += task.tokens_used
        
        # Calculate averages and rates
        performance = []
        for agent_name, stats in agent_stats.items():
            if stats["total_tasks"] > 0:
                stats["success_rate"] = stats["completed_tasks"] / stats["total_tasks"] * 100
                stats["average_duration"] = stats["average_duration"] / stats["total_tasks"]
                
                performance.append({
                    "agent_name": agent_name,
                    **stats
                })
        
        return sorted(performance, key=lambda x: x["success_rate"], reverse=True)
    
    async def _load_active_tasks(self):
        """Load active tasks from Redis on startup"""
        if not self.redis_client:
            return
            
        try:
            tasks_data = await self.redis_client.hgetall("bizosaas:active_tasks")
            
            for task_id, task_json in tasks_data.items():
                task_dict = json.loads(task_json)
                
                # Convert back to AgentTask object
                task = AgentTask(
                    task_id=task_dict["task_id"],
                    agent_name=task_dict["agent_name"],
                    task_type=TaskType(task_dict["task_type"]),
                    status=AgentStatus(task_dict["status"]),
                    project=task_dict["project"],
                    tenant_id=task_dict["tenant_id"],
                    user_id=task_dict["user_id"],
                    started_at=datetime.fromisoformat(task_dict["started_at"]),
                    updated_at=datetime.fromisoformat(task_dict["updated_at"]),
                    input_data=task_dict.get("input_data", {}),
                    tools_used=task_dict.get("tools_used", []),
                    progress_percentage=task_dict.get("progress_percentage", 0),
                    current_step=task_dict.get("current_step", "")
                )
                
                self.active_tasks[task_id] = task
                
            logger.info(f"Loaded {len(self.active_tasks)} active tasks from Redis")
            
        except Exception as e:
            logger.error(f"Failed to load active tasks: {e}")
    
    async def _broadcast_update(self, event_type: str, data: Dict[str, Any]):
        """Broadcast updates to all connected WebSocket clients"""
        
        if not self.websocket_connections:
            return
            
        message = json.dumps({
            "type": event_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        # Send to all connected clients
        disconnected = set()
        for ws in self.websocket_connections.copy():
            try:
                await ws.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(ws)
            except Exception as e:
                logger.warning(f"Failed to send WebSocket message: {e}")
                disconnected.add(ws)
        
        # Remove disconnected clients
        self.websocket_connections -= disconnected
    
    async def add_websocket_client(self, websocket: websockets.WebSocketServerProtocol):
        """Add new WebSocket client"""
        self.websocket_connections.add(websocket)
        
        # Send initial dashboard data
        dashboard_data = await self.get_dashboard_data()
        await websocket.send(json.dumps({
            "type": "dashboard_data",
            "data": dashboard_data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }))
        
        logger.info(f"New WebSocket client connected. Total: {len(self.websocket_connections)}")
    
    def remove_websocket_client(self, websocket: websockets.WebSocketServerProtocol):
        """Remove WebSocket client"""
        self.websocket_connections.discard(websocket)
        logger.info(f"WebSocket client disconnected. Total: {len(self.websocket_connections)}")

# Global monitor instance
_monitor_instance = None
_monitor_lock = threading.Lock()

def get_agent_monitor() -> AgentActivityMonitor:
    """Get singleton instance of agent monitor"""
    global _monitor_instance
    
    if _monitor_instance is None:
        with _monitor_lock:
            if _monitor_instance is None:
                _monitor_instance = AgentActivityMonitor()
                # Initialize in background
                asyncio.create_task(_monitor_instance.initialize())
    
    return _monitor_instance

# Convenience functions for easy integration
async def start_agent_task(agent_name: str, 
                         task_type: str,
                         project: str,
                         tenant_id: str,
                         user_id: str,
                         input_data: Dict[str, Any] = None) -> str:
    """Start tracking an agent task"""
    monitor = get_agent_monitor()
    return await monitor.start_task(
        agent_name=agent_name,
        task_type=TaskType(task_type),
        project=project,
        tenant_id=tenant_id,
        user_id=user_id,
        input_data=input_data
    )

async def update_agent_task(task_id: str, 
                          status: str,
                          progress: int = 0,
                          current_step: str = "",
                          tools_used: List[str] = None,
                          tokens_used: int = None,
                          error_message: str = None):
    """Update agent task status"""
    monitor = get_agent_monitor()
    await monitor.update_task_status(
        task_id=task_id,
        status=AgentStatus(status),
        progress_percentage=progress,
        current_step=current_step,
        tools_used=tools_used,
        tokens_used=tokens_used,
        error_message=error_message
    )

async def complete_agent_task(task_id: str,
                            output_data: Dict[str, Any] = None,
                            success: bool = True):
    """Complete agent task tracking"""
    monitor = get_agent_monitor()
    await monitor.complete_task(task_id, output_data, success)

if __name__ == "__main__":
    # Test the monitoring system
    async def test_monitor():
        monitor = AgentActivityMonitor()
        await monitor.initialize()
        
        print("🔍 Testing Agent Activity Monitor...")
        
        # Simulate some tasks
        task1 = await monitor.start_task(
            "keyword_research_agent",
            TaskType.KEYWORD_RESEARCH,
            "coreldove",
            "tenant_123",
            "user_456",
            {"keywords": ["wireless headphones"]}
        )
        
        await monitor.update_task_status(task1, AgentStatus.RUNNING, 50, "Analyzing keywords")
        await monitor.complete_task(task1, {"results": "completed"}, True)
        
        # Get dashboard data
        dashboard = await monitor.get_dashboard_data()
        print(f"✅ Dashboard data: {json.dumps(dashboard, indent=2)}")
    
    asyncio.run(test_monitor())