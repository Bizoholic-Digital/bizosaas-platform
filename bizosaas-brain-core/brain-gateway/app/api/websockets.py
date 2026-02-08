from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
import psutil
import logging
from app.observability.health import get_dependency_health

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/brain/ws", tags=["websockets"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                # Connection might be dead
                pass

manager = ConnectionManager()

@router.websocket("/health")
async def websocket_health_stream(websocket: WebSocket):
    """
    WebSocket endpoint that streams system and occupancy health every 2 seconds.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Gather metrics
            health_data = await get_dependency_health()
            
            # Add some live spice
            health_data["ws_active_connections"] = len(manager.active_connections)
            
            await websocket.send_json(health_data)
            await asyncio.sleep(2)  # Stream interval
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket Error: {e}")
        manager.disconnect(websocket)
