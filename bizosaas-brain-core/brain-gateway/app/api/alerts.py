"""
Real-time Alerts WebSocket API
WebSocket endpoint for real-time alert streaming to Admin Portal.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.alert_system import alert_manager
from app.dependencies import require_role
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin/alerts", tags=["real-time-alerts"])


@router.websocket("/ws")
async def websocket_alerts(websocket: WebSocket):
    """
    WebSocket endpoint for real-time alerts.
    Admins connect to this endpoint to receive instant notifications.
    """
    await alert_manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            
            # Handle ping/pong for connection health
            if data == "ping":
                await websocket.send_text("pong")
    
    except WebSocketDisconnect:
        alert_manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        alert_manager.disconnect(websocket)


@router.get("/history")
async def get_alert_history(limit: int = 50):
    """
    Get recent alert history.
    """
    history = alert_manager.get_alert_history(limit)
    
    return {
        "total": len(history),
        "alerts": history
    }


@router.post("/test")
async def send_test_alert():
    """
    Send a test alert (for development/testing).
    """
    from app.services.alert_system import Alert, AlertCategory, AlertSeverity
    from datetime import datetime
    
    alert = Alert(
        id=f"test_{int(datetime.utcnow().timestamp())}",
        category=AlertCategory.SYSTEM,
        severity=AlertSeverity.INFO,
        title="Test Alert",
        message="This is a test alert to verify the real-time alert system is working correctly.",
        timestamp=datetime.utcnow().isoformat(),
        metadata={"test": True}
    )
    
    await alert_manager.send_alert(alert)
    
    return {
        "status": "success",
        "message": "Test alert sent",
        "alert": alert.to_dict()
    }
