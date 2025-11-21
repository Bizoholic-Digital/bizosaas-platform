"""
Agent Monitoring Service - Real-time Dashboard API
WebSocket and REST endpoints for AI agent activity tracking
"""

import asyncio
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Dict, Any, List
import uvicorn

# Import monitoring system
import sys
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from shared.agent_monitor import (
    get_agent_monitor,
    AgentActivityMonitor,
    TaskType,
    AgentStatus,
    start_agent_task,
    update_agent_task,
    complete_agent_task
)
from shared.vault_client import get_redis_url

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BizOSaas Agent Monitoring Service",
    description="Real-time monitoring and dashboard for AI agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global monitor instance
monitor = None

@app.on_event("startup")
async def startup_event():
    """Initialize monitoring system on startup"""
    global monitor
    monitor = get_agent_monitor()
    await monitor.initialize()
    logger.info("Agent monitoring service started")

@app.get("/")
async def root():
    """Service health check"""
    return {
        "service": "bizosaas-agent-monitor",
        "status": "healthy",
        "version": "1.0.0",
        "active_tasks": len(monitor.active_tasks) if monitor else 0
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    dashboard_data = await monitor.get_dashboard_data()
    
    return {
        "status": "healthy",
        "redis_connected": monitor.redis_client is not None,
        "active_websockets": len(monitor.websocket_connections),
        "statistics": dashboard_data["statistics"]
    }

@app.get("/dashboard")
async def get_dashboard_data():
    """Get comprehensive dashboard data"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    return await monitor.get_dashboard_data()

@app.get("/tasks/active")
async def get_active_tasks():
    """Get all currently active tasks"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    return [task.to_dict() for task in monitor.active_tasks.values()]

@app.get("/tasks/completed")
async def get_completed_tasks(limit: int = 50):
    """Get recent completed tasks"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    tasks = sorted(monitor.completed_tasks, key=lambda x: x.completed_at or x.updated_at, reverse=True)
    return [task.to_dict() for task in tasks[:limit]]

@app.get("/tasks/{task_id}")
async def get_task_details(task_id: str):
    """Get details for a specific task"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    # Check active tasks
    if task_id in monitor.active_tasks:
        return monitor.active_tasks[task_id].to_dict()
    
    # Check completed tasks
    for task in monitor.completed_tasks:
        if task.task_id == task_id:
            return task.to_dict()
    
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks/start")
async def start_task_endpoint(
    agent_name: str,
    task_type: str,
    project: str,
    tenant_id: str,
    user_id: str,
    input_data: Dict[str, Any] = None
):
    """Start tracking a new agent task"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    try:
        task_id = await start_agent_task(
            agent_name=agent_name,
            task_type=task_type,
            project=project,
            tenant_id=tenant_id,
            user_id=user_id,
            input_data=input_data
        )
        
        return {
            "task_id": task_id,
            "status": "started",
            "message": f"Started tracking task for {agent_name}"
        }
        
    except Exception as e:
        logger.error(f"Failed to start task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}/update")
async def update_task_endpoint(
    task_id: str,
    status: str,
    progress: int = 0,
    current_step: str = "",
    tools_used: List[str] = None,
    tokens_used: int = None,
    error_message: str = None
):
    """Update task status and progress"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    try:
        await update_agent_task(
            task_id=task_id,
            status=status,
            progress=progress,
            current_step=current_step,
            tools_used=tools_used,
            tokens_used=tokens_used,
            error_message=error_message
        )
        
        return {
            "task_id": task_id,
            "status": "updated",
            "message": f"Updated task status to {status}"
        }
        
    except Exception as e:
        logger.error(f"Failed to update task {task_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}/complete")
async def complete_task_endpoint(
    task_id: str,
    output_data: Dict[str, Any] = None,
    success: bool = True
):
    """Mark task as completed"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    try:
        await complete_agent_task(
            task_id=task_id,
            output_data=output_data,
            success=success
        )
        
        return {
            "task_id": task_id,
            "status": "completed",
            "success": success,
            "message": f"Task completed {'successfully' if success else 'with errors'}"
        }
        
    except Exception as e:
        logger.error(f"Failed to complete task {task_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/performance")
async def get_performance_stats():
    """Get agent performance statistics"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    dashboard_data = await monitor.get_dashboard_data()
    
    return {
        "agent_performance": dashboard_data["agent_performance"],
        "project_breakdown": dashboard_data["project_breakdown"],
        "task_type_breakdown": dashboard_data["task_type_breakdown"],
        "hourly_activity": dashboard_data["hourly_activity"]
    }

@app.websocket("/ws/dashboard")
async def dashboard_websocket(websocket: WebSocket):
    """Real-time dashboard WebSocket connection"""
    if not monitor:
        await websocket.close(code=1011, reason="Monitor not initialized")
        return
    
    await websocket.accept()
    await monitor.add_websocket_client(websocket)
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle client requests
                if message.get("type") == "get_dashboard":
                    dashboard_data = await monitor.get_dashboard_data()
                    await websocket.send(json.dumps({
                        "type": "dashboard_data",
                        "data": dashboard_data
                    }))
                    
            except Exception as e:
                logger.warning(f"WebSocket message error: {e}")
                break
                
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        monitor.remove_websocket_client(websocket)

@app.get("/ui/dashboard", response_class=HTMLResponse)
async def dashboard_ui():
    """Simple HTML dashboard for agent monitoring"""
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BizOSaas Agent Monitor</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
                text-align: center;
            }
            .stat-number {
                font-size: 2.5em;
                font-weight: bold;
                margin: 10px 0;
            }
            .activity-feed {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
                max-height: 400px;
                overflow-y: auto;
            }
            .task-item {
                padding: 10px;
                margin: 10px 0;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                border-left: 4px solid;
            }
            .status-running { border-color: #4CAF50; }
            .status-completed { border-color: #2196F3; }
            .status-failed { border-color: #f44336; }
            .status-idle { border-color: #FFC107; }
            .connection-status {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 10px 20px;
                border-radius: 20px;
                font-weight: bold;
            }
            .connected { background: #4CAF50; }
            .disconnected { background: #f44336; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 BizOSaas Agent Monitor</h1>
                <p>Real-time tracking of AI agents across all projects</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div>Active Tasks</div>
                    <div class="stat-number" id="activeTasks">-</div>
                </div>
                <div class="stat-card">
                    <div>Completed Today</div>
                    <div class="stat-number" id="completedTasks">-</div>
                </div>
                <div class="stat-card">
                    <div>Success Rate</div>
                    <div class="stat-number" id="successRate">-</div>
                </div>
                <div class="stat-card">
                    <div>Avg Duration</div>
                    <div class="stat-number" id="avgDuration">-</div>
                </div>
            </div>
            
            <div class="activity-feed">
                <h3>📊 Recent Activity</h3>
                <div id="activityList">
                    <p>Connecting to real-time feed...</p>
                </div>
            </div>
        </div>
        
        <div class="connection-status" id="connectionStatus">
            Connecting...
        </div>
        
        <script>
            const ws = new WebSocket(`ws://${window.location.host}/ws/dashboard`);
            const statusEl = document.getElementById('connectionStatus');
            const activityEl = document.getElementById('activityList');
            
            ws.onopen = function(event) {
                statusEl.className = 'connection-status connected';
                statusEl.textContent = '🟢 Connected';
                
                // Request initial dashboard data
                ws.send(JSON.stringify({type: 'get_dashboard'}));
            };
            
            ws.onmessage = function(event) {
                const message = JSON.parse(event.data);
                
                if (message.type === 'dashboard_data') {
                    updateDashboard(message.data);
                } else if (message.type === 'task_started' || message.type === 'task_updated' || message.type === 'task_completed') {
                    updateRecentActivity(message);
                }
            };
            
            ws.onclose = function(event) {
                statusEl.className = 'connection-status disconnected';
                statusEl.textContent = '🔴 Disconnected';
            };
            
            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
                statusEl.className = 'connection-status disconnected';
                statusEl.textContent = '⚠️ Error';
            };
            
            function updateDashboard(data) {
                document.getElementById('activeTasks').textContent = data.active_tasks;
                document.getElementById('completedTasks').textContent = data.statistics.completed_tasks;
                
                const totalTasks = data.statistics.completed_tasks + data.statistics.failed_tasks;
                const successRate = totalTasks > 0 ? Math.round((data.statistics.completed_tasks / totalTasks) * 100) : 0;
                document.getElementById('successRate').textContent = successRate + '%';
                
                const avgDuration = data.statistics.average_duration;
                document.getElementById('avgDuration').textContent = avgDuration ? avgDuration.toFixed(1) + 's' : '-';
                
                updateActivityFeed(data.recent_activity);
            }
            
            function updateActivityFeed(activities) {
                activityEl.innerHTML = '';
                
                activities.forEach(activity => {
                    const item = document.createElement('div');
                    item.className = `task-item status-${activity.status}`;
                    item.innerHTML = `
                        <strong>${activity.agent_name}</strong> - ${activity.task_type}
                        <br>
                        <small>Project: ${activity.project} | Progress: ${activity.progress}%</small>
                        <br>
                        <small>Updated: ${new Date(activity.updated_at).toLocaleTimeString()}</small>
                    `;
                    activityEl.appendChild(item);
                });
            }
            
            function updateRecentActivity(message) {
                // Add new activity to the top of the feed
                const item = document.createElement('div');
                const activity = message.data;
                item.className = `task-item status-${activity.status}`;
                item.innerHTML = `
                    <strong>${activity.agent_name}</strong> - ${activity.task_type}
                    <br>
                    <small>Project: ${activity.project} | Progress: ${activity.progress_percentage}%</small>
                    <br>
                    <small>Updated: ${new Date(activity.updated_at).toLocaleTimeString()}</small>
                `;
                
                activityEl.insertBefore(item, activityEl.firstChild);
                
                // Keep only latest 10 items
                while (activityEl.children.length > 10) {
                    activityEl.removeChild(activityEl.lastChild);
                }
            }
            
            // Auto-refresh dashboard data every 30 seconds
            setInterval(() => {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({type: 'get_dashboard'}));
                }
            }, 30000);
        </script>
    </body>
    </html>
    """
    
    return html_content

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )