"""
Dashboard Integration for Amazon Sourcing Workflow
Real-time monitoring, analytics, and management interface
"""

import asyncio
import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import jinja2

from amazon_sourcing_workflow import (
    AmazonSourcingWorkflowManager,
    AmazonSourcingStatus,
    get_amazon_sourcing_manager
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardEventType(str, Enum):
    """Dashboard event types"""
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_UPDATED = "workflow_updated"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"
    METRICS_UPDATE = "metrics_update"
    SYSTEM_ALERT = "system_alert"

@dataclass
class DashboardEvent:
    """Dashboard event data structure"""
    event_type: DashboardEventType
    workflow_id: Optional[str] = None
    data: Dict[str, Any] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)

class WebSocketManager:
    """WebSocket connection manager for real-time dashboard updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_info: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, client_info: Dict[str, Any] = None):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_info[websocket] = client_info or {}
        
        logger.info(f"📱 Dashboard client connected. Total connections: {len(self.active_connections)}")
        
        # Send welcome message with current stats
        await self.send_personal_message(websocket, {
            "type": "connection_established",
            "message": "Connected to Amazon Sourcing Dashboard",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "connection_id": str(uuid.uuid4())
        })
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            self.connection_info.pop(websocket, None)
            
        logger.info(f"📱 Dashboard client disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, websocket: WebSocket, message: dict):
        """Send message to specific WebSocket connection"""
        try:
            await websocket.send_text(json.dumps(message, default=str))
        except Exception as e:
            logger.error(f"Failed to send personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return
        
        message_text = json.dumps(message, default=str)
        disconnected = []
        
        for websocket in self.active_connections:
            try:
                await websocket.send_text(message_text)
            except Exception as e:
                logger.error(f"Failed to broadcast to client: {e}")
                disconnected.append(websocket)
        
        # Clean up disconnected clients
        for websocket in disconnected:
            self.disconnect(websocket)
    
    async def broadcast_event(self, event: DashboardEvent):
        """Broadcast dashboard event to all clients"""
        message = {
            "event_type": event.event_type,
            "workflow_id": event.workflow_id,
            "data": event.data,
            "timestamp": event.timestamp.isoformat()
        }
        
        await self.broadcast(message)
        logger.info(f"📢 Broadcasted event: {event.event_type}")

class DashboardManager:
    """Main dashboard management class"""
    
    def __init__(self, workflow_manager: AmazonSourcingWorkflowManager):
        self.workflow_manager = workflow_manager
        self.websocket_manager = WebSocketManager()
        self.dashboard_metrics = {}
        self.active_workflows = {}
        self.recent_events = []
        
        # Start background tasks
        asyncio.create_task(self.metrics_updater())
        asyncio.create_task(self.workflow_monitor())
    
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        
        # Get workflow metrics
        workflow_metrics = await self.workflow_manager.get_workflow_metrics()
        
        # Get recent workflows
        recent_workflows = await self.workflow_manager.list_workflows(limit=20)
        
        # Get system health
        system_health = await self.get_system_health()
        
        # Get performance statistics
        performance_stats = await self.get_performance_statistics()
        
        dashboard_data = {
            "overview": {
                "total_workflows": workflow_metrics.get('total_workflows', 0),
                "active_workflows": workflow_metrics.get('active_workflows', 0),
                "completed_workflows": workflow_metrics.get('completed_workflows', 0),
                "success_rate": workflow_metrics.get('success_rate', 0),
                "average_duration": workflow_metrics.get('average_duration_seconds', 0)
            },
            "workflows": {
                "recent": recent_workflows[:10],
                "active": [w for w in recent_workflows if w.get('status') in ['running', 'pending']],
                "failed": [w for w in recent_workflows if w.get('status') == 'failed']
            },
            "metrics": {
                "hourly_throughput": self.calculate_hourly_throughput(recent_workflows),
                "status_distribution": self.calculate_status_distribution(recent_workflows),
                "error_analysis": workflow_metrics.get('most_common_errors', [])
            },
            "system": {
                "health": system_health,
                "performance": performance_stats,
                "uptime": self.calculate_uptime()
            },
            "events": {
                "recent": self.recent_events[-50:],  # Last 50 events
                "alerts": [e for e in self.recent_events if e.get('event_type') == 'system_alert']
            },
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        return dashboard_data
    
    async def get_workflow_details(self, workflow_id: str) -> Dict[str, Any]:
        """Get detailed information for a specific workflow"""
        
        workflow_status = await self.workflow_manager.get_workflow_status(workflow_id)
        
        if not workflow_status:
            return None
        
        # Get workflow history/timeline
        timeline = self.generate_workflow_timeline(workflow_status)
        
        # Get performance metrics for this workflow
        performance = self.calculate_workflow_performance(workflow_status)
        
        details = {
            "workflow": workflow_status,
            "timeline": timeline,
            "performance": performance,
            "logs": await self.get_workflow_logs(workflow_id),
            "related_workflows": await self.get_related_workflows(workflow_id)
        }
        
        return details
    
    async def start_workflow_from_dashboard(
        self, 
        amazon_url: str, 
        config: Dict[str, Any],
        user_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Start a new workflow from the dashboard"""
        
        try:
            # Start the workflow
            response = await self.workflow_manager.start_amazon_sourcing_workflow(
                amazon_url=amazon_url,
                tenant_id=user_info.get('tenant_id', 'dashboard_user'),
                user_id=user_info.get('user_id', 'dashboard_user'),
                **config
            )
            
            # Broadcast event
            await self.websocket_manager.broadcast_event(DashboardEvent(
                event_type=DashboardEventType.WORKFLOW_STARTED,
                workflow_id=response.workflow_id,
                data={
                    "amazon_url": amazon_url,
                    "user": user_info.get('user_id', 'dashboard_user'),
                    "config": config
                }
            ))
            
            return {
                "success": True,
                "workflow_id": response.workflow_id,
                "message": "Workflow started successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to start workflow from dashboard: {e}")
            
            await self.websocket_manager.broadcast_event(DashboardEvent(
                event_type=DashboardEventType.SYSTEM_ALERT,
                data={
                    "level": "error",
                    "message": f"Failed to start workflow: {str(e)}",
                    "amazon_url": amazon_url
                }
            ))
            
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to start workflow"
            }
    
    async def cancel_workflow_from_dashboard(
        self, 
        workflow_id: str, 
        user_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Cancel a workflow from the dashboard"""
        
        try:
            success = await self.workflow_manager.cancel_workflow(workflow_id)
            
            if success:
                await self.websocket_manager.broadcast_event(DashboardEvent(
                    event_type=DashboardEventType.WORKFLOW_UPDATED,
                    workflow_id=workflow_id,
                    data={
                        "status": "cancelled",
                        "cancelled_by": user_info.get('user_id', 'dashboard_user'),
                        "cancelled_at": datetime.now(timezone.utc).isoformat()
                    }
                ))
                
                return {
                    "success": True,
                    "message": "Workflow cancelled successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to cancel workflow"
                }
                
        except Exception as e:
            logger.error(f"Failed to cancel workflow from dashboard: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Error cancelling workflow"
            }
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get system health information"""
        
        health = {
            "temporal": {"status": "healthy", "response_time": 45},
            "saleor": {"status": "healthy", "response_time": 120},
            "crewai": {"status": "healthy", "response_time": 200},
            "database": {"status": "healthy", "response_time": 15},
            "redis": {"status": "healthy", "response_time": 8}
        }
        
        # In production, you would actually check these services
        overall_status = "healthy" if all(s["status"] == "healthy" for s in health.values()) else "degraded"
        
        return {
            "overall": overall_status,
            "services": health,
            "last_check": datetime.now(timezone.utc).isoformat()
        }
    
    async def get_performance_statistics(self) -> Dict[str, Any]:
        """Get system performance statistics"""
        
        return {
            "cpu_usage": 65.5,
            "memory_usage": 78.2,
            "disk_usage": 45.8,
            "network_io": 234.5,
            "active_connections": len(self.websocket_manager.active_connections),
            "queue_size": 5,
            "cache_hit_rate": 89.2
        }
    
    def calculate_hourly_throughput(self, workflows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate hourly workflow throughput"""
        
        # Group workflows by hour
        hourly_data = {}
        
        for workflow in workflows:
            started_at = workflow.get('started_at')
            if started_at:
                hour = started_at.replace(minute=0, second=0, microsecond=0)
                hour_key = hour.isoformat()
                
                if hour_key not in hourly_data:
                    hourly_data[hour_key] = {"started": 0, "completed": 0, "failed": 0}
                
                hourly_data[hour_key]["started"] += 1
                
                if workflow.get('status') == 'completed':
                    hourly_data[hour_key]["completed"] += 1
                elif workflow.get('status') == 'failed':
                    hourly_data[hour_key]["failed"] += 1
        
        # Convert to list for charting
        return [
            {"hour": hour, **data} 
            for hour, data in sorted(hourly_data.items())
        ]
    
    def calculate_status_distribution(self, workflows: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate workflow status distribution"""
        
        distribution = {}
        
        for workflow in workflows:
            status = workflow.get('status', 'unknown')
            distribution[status] = distribution.get(status, 0) + 1
        
        return distribution
    
    def generate_workflow_timeline(self, workflow_status: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate timeline for workflow execution"""
        
        timeline = []
        
        # Mock timeline data based on workflow status
        statuses = [
            ("Workflow Started", workflow_status.get('started_at')),
            ("Extracting Product Data", None),
            ("Enhancing with AI", None),
            ("Creating Saleor Product", None),
            ("Processing Images", None),
            ("Validating Product", None),
            ("Sending Notifications", None),
            ("Workflow Completed", workflow_status.get('completed_at'))
        ]
        
        for i, (step, timestamp) in enumerate(statuses):
            timeline.append({
                "step": step,
                "timestamp": timestamp,
                "status": "completed" if timestamp else "pending",
                "duration": 30 + i * 15  # Mock duration
            })
        
        return timeline
    
    def calculate_workflow_performance(self, workflow_status: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance metrics for a workflow"""
        
        started_at = workflow_status.get('started_at')
        completed_at = workflow_status.get('completed_at')
        
        duration = 0
        if started_at and completed_at:
            duration = (completed_at - started_at).total_seconds()
        
        return {
            "duration_seconds": duration,
            "steps_completed": 6,
            "success_rate": 100.0 if workflow_status.get('status') == 'completed' else 0.0,
            "performance_score": 85.5,  # Mock score
            "bottlenecks": ["AI Enhancement", "Image Processing"]  # Mock bottlenecks
        }
    
    def calculate_uptime(self) -> Dict[str, Any]:
        """Calculate system uptime"""
        
        # Mock uptime calculation
        start_time = datetime.now(timezone.utc) - timedelta(hours=24, minutes=15)
        uptime_seconds = (datetime.now(timezone.utc) - start_time).total_seconds()
        
        return {
            "uptime_seconds": uptime_seconds,
            "uptime_percentage": 99.85,
            "last_restart": start_time.isoformat()
        }
    
    async def get_workflow_logs(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get logs for a specific workflow"""
        
        # Mock log data
        return [
            {
                "timestamp": datetime.now(timezone.utc) - timedelta(minutes=10),
                "level": "INFO",
                "message": "Workflow started",
                "component": "workflow_engine"
            },
            {
                "timestamp": datetime.now(timezone.utc) - timedelta(minutes=8),
                "level": "INFO", 
                "message": "Product data extracted successfully",
                "component": "amazon_scraper"
            },
            {
                "timestamp": datetime.now(timezone.utc) - timedelta(minutes=5),
                "level": "INFO",
                "message": "AI enhancement completed",
                "component": "crewai_service"
            }
        ]
    
    async def get_related_workflows(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get related workflows"""
        
        # Mock related workflows
        return []
    
    async def metrics_updater(self):
        """Background task to update dashboard metrics"""
        
        while True:
            try:
                # Update metrics every 30 seconds
                await asyncio.sleep(30)
                
                # Get latest metrics
                metrics = await self.get_dashboard_data()
                
                # Broadcast metrics update
                await self.websocket_manager.broadcast_event(DashboardEvent(
                    event_type=DashboardEventType.METRICS_UPDATE,
                    data=metrics
                ))
                
            except Exception as e:
                logger.error(f"Error updating dashboard metrics: {e}")
    
    async def workflow_monitor(self):
        """Background task to monitor workflow status changes"""
        
        known_workflows = set()
        
        while True:
            try:
                # Check for workflow changes every 10 seconds
                await asyncio.sleep(10)
                
                # Get current workflows
                current_workflows = await self.workflow_manager.list_workflows(limit=100)
                
                for workflow in current_workflows:
                    workflow_id = workflow['workflow_id']
                    status = workflow.get('status')
                    
                    # Check for new workflows
                    if workflow_id not in known_workflows:
                        known_workflows.add(workflow_id)
                        
                        await self.websocket_manager.broadcast_event(DashboardEvent(
                            event_type=DashboardEventType.WORKFLOW_STARTED,
                            workflow_id=workflow_id,
                            data=workflow
                        ))
                    
                    # Check for completed workflows
                    elif status in ['completed', 'failed']:
                        event_type = (DashboardEventType.WORKFLOW_COMPLETED 
                                     if status == 'completed' 
                                     else DashboardEventType.WORKFLOW_FAILED)
                        
                        await self.websocket_manager.broadcast_event(DashboardEvent(
                            event_type=event_type,
                            workflow_id=workflow_id,
                            data=workflow
                        ))
                
            except Exception as e:
                logger.error(f"Error monitoring workflows: {e}")

# Dashboard HTML template
DASHBOARD_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazon Sourcing Dashboard - BizOSaaS</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
</head>
<body class="bg-gray-100 min-h-screen">
    <div id="dashboard" x-data="dashboardData()" x-init="init()" class="container mx-auto px-4 py-8">
        
        <!-- Header -->
        <header class="mb-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">Amazon Sourcing Dashboard</h1>
            <p class="text-gray-600">Real-time monitoring of product sourcing workflows</p>
            <div class="mt-4 flex items-center space-x-4">
                <div class="flex items-center">
                    <div class="w-3 h-3 rounded-full mr-2" :class="connectionStatus === 'connected' ? 'bg-green-500' : 'bg-red-500'"></div>
                    <span class="text-sm" x-text="connectionStatus === 'connected' ? 'Connected' : 'Disconnected'"></span>
                </div>
                <div class="text-sm text-gray-500" x-text="'Last updated: ' + lastUpdated"></div>
            </div>
        </header>

        <!-- Overview Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Total Workflows</h3>
                <div class="text-3xl font-bold text-blue-600" x-text="metrics.total_workflows"></div>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Active Workflows</h3>
                <div class="text-3xl font-bold text-green-600" x-text="metrics.active_workflows"></div>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Success Rate</h3>
                <div class="text-3xl font-bold text-purple-600" x-text="metrics.success_rate + '%'"></div>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Avg Duration</h3>
                <div class="text-3xl font-bold text-orange-600" x-text="Math.round(metrics.average_duration) + 's'"></div>
            </div>
        </div>

        <!-- Start New Workflow -->
        <div class="bg-white rounded-lg shadow p-6 mb-8">
            <h3 class="text-lg font-semibold text-gray-700 mb-4">Start New Workflow</h3>
            <div class="flex space-x-4">
                <input 
                    type="url" 
                    x-model="newWorkflow.amazon_url" 
                    placeholder="Enter Amazon product URL" 
                    class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                <button 
                    @click="startWorkflow()" 
                    :disabled="!newWorkflow.amazon_url || isStarting"
                    class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    x-text="isStarting ? 'Starting...' : 'Start Workflow'"
                ></button>
            </div>
        </div>

        <!-- Recent Workflows -->
        <div class="bg-white rounded-lg shadow mb-8">
            <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-700">Recent Workflows</h3>
            </div>
            <div class="p-6">
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Workflow ID</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amazon URL</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Started</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <template x-for="workflow in workflows" :key="workflow.workflow_id">
                                <tr>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900" x-text="workflow.workflow_id.substr(-8)"></td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900" x-text="workflow.amazon_url || 'N/A'"></td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" 
                                              :class="getStatusColor(workflow.status)" 
                                              x-text="workflow.status">
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500" x-text="formatDate(workflow.started_at)"></td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                        <button @click="viewWorkflow(workflow.workflow_id)" class="text-blue-600 hover:text-blue-900 mr-3">View</button>
                                        <button 
                                            x-show="workflow.status === 'running'" 
                                            @click="cancelWorkflow(workflow.workflow_id)" 
                                            class="text-red-600 hover:text-red-900"
                                        >Cancel</button>
                                    </td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Real-time Events -->
        <div class="bg-white rounded-lg shadow">
            <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-700">Real-time Events</h3>
            </div>
            <div class="p-6">
                <div class="space-y-2 max-h-64 overflow-y-auto">
                    <template x-for="event in events.slice().reverse()" :key="event.timestamp">
                        <div class="flex items-center space-x-3 p-2 rounded bg-gray-50">
                            <div class="w-2 h-2 rounded-full" :class="getEventColor(event.event_type)"></div>
                            <div class="text-sm text-gray-600" x-text="formatDate(event.timestamp)"></div>
                            <div class="text-sm text-gray-900" x-text="event.event_type"></div>
                            <div class="text-sm text-gray-600" x-text="event.workflow_id || ''"></div>
                        </div>
                    </template>
                </div>
            </div>
        </div>
    </div>

    <script>
        function dashboardData() {
            return {
                // Connection status
                connectionStatus: 'disconnected',
                websocket: null,
                
                // Data
                metrics: {
                    total_workflows: 0,
                    active_workflows: 0,
                    success_rate: 0,
                    average_duration: 0
                },
                workflows: [],
                events: [],
                lastUpdated: 'Never',
                
                // UI state
                newWorkflow: {
                    amazon_url: ''
                },
                isStarting: false,
                
                // Methods
                init() {
                    this.connectWebSocket();
                    this.loadInitialData();
                },
                
                connectWebSocket() {
                    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                    const wsUrl = `${protocol}//${window.location.host}/ws/dashboard`;
                    
                    this.websocket = new WebSocket(wsUrl);
                    
                    this.websocket.onopen = () => {
                        this.connectionStatus = 'connected';
                        console.log('Connected to dashboard WebSocket');
                    };
                    
                    this.websocket.onmessage = (event) => {
                        const data = JSON.parse(event.data);
                        this.handleWebSocketMessage(data);
                    };
                    
                    this.websocket.onclose = () => {
                        this.connectionStatus = 'disconnected';
                        console.log('Disconnected from dashboard WebSocket');
                        
                        // Reconnect after 5 seconds
                        setTimeout(() => {
                            this.connectWebSocket();
                        }, 5000);
                    };
                    
                    this.websocket.onerror = (error) => {
                        console.error('WebSocket error:', error);
                    };
                },
                
                handleWebSocketMessage(data) {
                    switch (data.event_type) {
                        case 'connection_established':
                            console.log('Dashboard connection established');
                            break;
                            
                        case 'workflow_started':
                            this.addEvent(data);
                            this.loadWorkflows();
                            break;
                            
                        case 'workflow_updated':
                        case 'workflow_completed':
                        case 'workflow_failed':
                            this.addEvent(data);
                            this.loadWorkflows();
                            break;
                            
                        case 'metrics_update':
                            this.updateMetrics(data.data);
                            break;
                            
                        case 'system_alert':
                            this.addEvent(data);
                            break;
                    }
                    
                    this.lastUpdated = new Date().toLocaleTimeString();
                },
                
                addEvent(eventData) {
                    this.events.push(eventData);
                    
                    // Keep only last 50 events
                    if (this.events.length > 50) {
                        this.events = this.events.slice(-50);
                    }
                },
                
                async loadInitialData() {
                    try {
                        const response = await fetch('/amazon-sourcing/dashboard-data');
                        const data = await response.json();
                        
                        this.metrics = data.overview;
                        this.workflows = data.workflows.recent;
                        this.events = data.events.recent;
                        this.lastUpdated = new Date().toLocaleTimeString();
                        
                    } catch (error) {
                        console.error('Failed to load initial data:', error);
                    }
                },
                
                async loadWorkflows() {
                    try {
                        const response = await fetch('/amazon-sourcing/workflows');
                        const data = await response.json();
                        this.workflows = data.workflows;
                        
                    } catch (error) {
                        console.error('Failed to load workflows:', error);
                    }
                },
                
                updateMetrics(metricsData) {
                    this.metrics = metricsData.overview;
                    this.workflows = metricsData.workflows.recent;
                },
                
                async startWorkflow() {
                    if (!this.newWorkflow.amazon_url) return;
                    
                    this.isStarting = true;
                    
                    try {
                        const response = await fetch('/amazon-sourcing/start', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(this.newWorkflow)
                        });
                        
                        const result = await response.json();
                        
                        if (result.workflow_id) {
                            this.newWorkflow.amazon_url = '';
                            alert('Workflow started successfully!');
                        } else {
                            alert('Failed to start workflow: ' + (result.detail || 'Unknown error'));
                        }
                        
                    } catch (error) {
                        console.error('Failed to start workflow:', error);
                        alert('Failed to start workflow: ' + error.message);
                    } finally {
                        this.isStarting = false;
                    }
                },
                
                async cancelWorkflow(workflowId) {
                    if (!confirm('Are you sure you want to cancel this workflow?')) return;
                    
                    try {
                        const response = await fetch(`/amazon-sourcing/cancel/${workflowId}`, {
                            method: 'POST'
                        });
                        
                        const result = await response.json();
                        
                        if (result.message) {
                            alert(result.message);
                        }
                        
                    } catch (error) {
                        console.error('Failed to cancel workflow:', error);
                        alert('Failed to cancel workflow: ' + error.message);
                    }
                },
                
                viewWorkflow(workflowId) {
                    // Open workflow details in new tab or modal
                    window.open(`/amazon-sourcing/dashboard/workflow/${workflowId}`, '_blank');
                },
                
                getStatusColor(status) {
                    const colors = {
                        'pending': 'bg-yellow-100 text-yellow-800',
                        'running': 'bg-blue-100 text-blue-800',
                        'completed': 'bg-green-100 text-green-800',
                        'failed': 'bg-red-100 text-red-800',
                        'cancelled': 'bg-gray-100 text-gray-800'
                    };
                    return colors[status] || 'bg-gray-100 text-gray-800';
                },
                
                getEventColor(eventType) {
                    const colors = {
                        'workflow_started': 'bg-blue-500',
                        'workflow_completed': 'bg-green-500',
                        'workflow_failed': 'bg-red-500',
                        'workflow_updated': 'bg-yellow-500',
                        'metrics_update': 'bg-purple-500',
                        'system_alert': 'bg-orange-500'
                    };
                    return colors[eventType] || 'bg-gray-500';
                },
                
                formatDate(dateString) {
                    if (!dateString) return 'N/A';
                    return new Date(dateString).toLocaleString();
                }
            }
        }
    </script>
</body>
</html>
"""

# Create dashboard manager instance
dashboard_manager = None

async def get_dashboard_manager() -> DashboardManager:
    """Get dashboard manager instance"""
    global dashboard_manager
    if dashboard_manager is None:
        workflow_manager = await get_amazon_sourcing_manager()
        dashboard_manager = DashboardManager(workflow_manager)
    return dashboard_manager

# Export classes and functions
__all__ = [
    'DashboardManager',
    'WebSocketManager', 
    'DashboardEvent',
    'DashboardEventType',
    'get_dashboard_manager',
    'DASHBOARD_HTML_TEMPLATE'
]