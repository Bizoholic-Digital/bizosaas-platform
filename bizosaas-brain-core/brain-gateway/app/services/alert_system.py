"""
Real-time Alert System
WebSocket-based real-time alerts for critical platform events.
"""

import asyncio
import logging
from typing import Dict, Any, List, Set
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict
from fastapi import WebSocket
import json

logger = logging.getLogger(__name__)


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertCategory(str, Enum):
    """Alert categories"""
    WORKFLOW = "workflow"
    TENANT = "tenant"
    SYSTEM = "system"
    SECURITY = "security"
    FINANCIAL = "financial"


@dataclass
class Alert:
    """Real-time alert"""
    id: str
    category: AlertCategory
    severity: AlertSeverity
    title: str
    message: str
    timestamp: str
    metadata: Dict[str, Any] = None
    
    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category.value,
            "severity": self.severity.value,
            "title": self.title,
            "message": self.message,
            "timestamp": self.timestamp,
            "metadata": self.metadata or {}
        }


class AlertManager:
    """
    Manages real-time alerts and WebSocket connections.
    """
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.alert_history: List[Alert] = []
        self.max_history = 100
    
    async def connect(self, websocket: WebSocket):
        """
        Register a new WebSocket connection.
        """
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")
        
        # Send recent alerts to new connection
        await self._send_alert_history(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection.
        """
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def send_alert(self, alert: Alert):
        """
        Send an alert to all connected clients.
        """
        # Add to history
        self.alert_history.append(alert)
        if len(self.alert_history) > self.max_history:
            self.alert_history.pop(0)
        
        # Broadcast to all connections
        message = json.dumps({
            "type": "alert",
            "data": alert.to_dict()
        })
        
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Failed to send alert to connection: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
        
        logger.info(f"Alert sent to {len(self.active_connections)} clients: {alert.title}")
    
    async def _send_alert_history(self, websocket: WebSocket):
        """
        Send recent alert history to a newly connected client.
        """
        if not self.alert_history:
            return
        
        message = json.dumps({
            "type": "history",
            "data": [alert.to_dict() for alert in self.alert_history[-10:]]  # Last 10 alerts
        })
        
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Failed to send alert history: {e}")
    
    async def create_workflow_alert(
        self,
        workflow_id: str,
        workflow_name: str,
        severity: AlertSeverity,
        message: str
    ):
        """
        Create and send a workflow-related alert.
        """
        alert = Alert(
            id=f"wf_{workflow_id}_{int(datetime.utcnow().timestamp())}",
            category=AlertCategory.WORKFLOW,
            severity=severity,
            title=f"Workflow Alert: {workflow_name}",
            message=message,
            timestamp=datetime.utcnow().isoformat(),
            metadata={"workflow_id": workflow_id, "workflow_name": workflow_name}
        )
        
        await self.send_alert(alert)
    
    async def create_tenant_alert(
        self,
        tenant_id: str,
        severity: AlertSeverity,
        title: str,
        message: str
    ):
        """
        Create and send a tenant-related alert.
        """
        alert = Alert(
            id=f"tenant_{tenant_id}_{int(datetime.utcnow().timestamp())}",
            category=AlertCategory.TENANT,
            severity=severity,
            title=title,
            message=message,
            timestamp=datetime.utcnow().isoformat(),
            metadata={"tenant_id": tenant_id}
        )
        
        await self.send_alert(alert)
    
    async def create_system_alert(
        self,
        severity: AlertSeverity,
        title: str,
        message: str,
        metadata: Dict[str, Any] = None
    ):
        """
        Create and send a system-related alert.
        """
        alert = Alert(
            id=f"system_{int(datetime.utcnow().timestamp())}",
            category=AlertCategory.SYSTEM,
            severity=severity,
            title=title,
            message=message,
            timestamp=datetime.utcnow().isoformat(),
            metadata=metadata
        )
        
        await self.send_alert(alert)
    
    def get_alert_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent alert history.
        """
        return [alert.to_dict() for alert in self.alert_history[-limit:]]


# Global alert manager instance
alert_manager = AlertManager()


async def monitor_workflow_health():
    """
    Background task to monitor workflow health and send alerts.
    """
    from app.dependencies import get_db
    from app.services.workflow_monitor import WorkflowMonitor
    
    while True:
        try:
            db = next(get_db())
            monitor = WorkflowMonitor(db)
            
            # Check last hour metrics
            metrics = await monitor.get_aggregated_metrics(time_range_hours=1)
            
            # Alert on high failure rate
            if metrics.total_executions > 0 and metrics.success_rate < 80:
                await alert_manager.create_system_alert(
                    severity=AlertSeverity.WARNING if metrics.success_rate >= 50 else AlertSeverity.CRITICAL,
                    title="High Workflow Failure Rate",
                    message=f"Workflow success rate is {metrics.success_rate:.1f}% in the last hour ({metrics.failed_executions} failures)",
                    metadata={
                        "success_rate": metrics.success_rate,
                        "failed_executions": metrics.failed_executions,
                        "total_executions": metrics.total_executions
                    }
                )
            
            # Alert on top failing workflows
            for failing_wf in metrics.top_failing_workflows[:3]:
                if failing_wf["failure_count"] >= 5:
                    await alert_manager.create_workflow_alert(
                        workflow_id=failing_wf["workflow_id"],
                        workflow_name=failing_wf["workflow_name"],
                        severity=AlertSeverity.ERROR,
                        message=f"{failing_wf['failure_count']} failures in the last hour"
                    )
            
        except Exception as e:
            logger.error(f"Error in workflow health monitor: {e}")
        
        # Check every 5 minutes
        await asyncio.sleep(300)


async def monitor_tenant_health():
    """
    Background task to monitor tenant health and send alerts.
    """
    from app.dependencies import get_db
    try:
        from app.models.user import User
    except ImportError:
        logger.error("Could not import User model in monitor_tenant_health")
        return

    from datetime import timedelta
    
    while True:
        try:
            db = next(get_db())
            
            # Check for at-risk tenants (no login in 30+ days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            # Defensive check for last_login_at vs last_login
            last_login_attr = getattr(User, 'last_login_at', None) or getattr(User, 'last_login', None)
            
            if last_login_attr:
                at_risk = db.query(User).filter(
                    User.role == "tenant",
                    last_login_attr < thirty_days_ago
                ).count()
                
                if at_risk > 0:
                    await alert_manager.create_tenant_alert(
                        tenant_id="platform",
                        severity=AlertSeverity.WARNING,
                        title="Tenants at Risk of Churn",
                        message=f"{at_risk} tenants haven't logged in for 30+ days",
                    )
            else:
               logger.warning("User model missing last_login_at attribute, skipping churn check.")
            
        except Exception as e:
            logger.error(f"Error in tenant health monitor: {e}")
        
        # Check every hour
        await asyncio.sleep(3600)


async def start_alert_monitors():
    """
    Start all background alert monitoring tasks.
    """
    asyncio.create_task(monitor_workflow_health())
    asyncio.create_task(monitor_tenant_health())
    logger.info("Alert monitoring tasks started")
