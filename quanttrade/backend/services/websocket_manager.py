"""
WebSocket connection manager
"""
from fastapi import WebSocket
from typing import Dict, List
import json
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manage WebSocket connections"""

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "market_data": [],
            "trading": [],
            "portfolio": []
        }

    async def connect(self, websocket: WebSocket, channel: str):
        """Accept new WebSocket connection"""
        await websocket.accept()
        if channel in self.active_connections:
            self.active_connections[channel].append(websocket)
            logger.info(f"New connection to {channel} channel. Total: {len(self.active_connections[channel])}")

    def disconnect(self, websocket: WebSocket, channel: str):
        """Remove WebSocket connection"""
        if channel in self.active_connections:
            if websocket in self.active_connections[channel]:
                self.active_connections[channel].remove(websocket)
                logger.info(f"Connection removed from {channel} channel. Total: {len(self.active_connections[channel])}")

    async def broadcast(self, message: dict, channel: str):
        """Broadcast message to all connections in a channel"""
        if channel not in self.active_connections:
            return

        disconnected = []
        for connection in self.active_connections[channel]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")
                disconnected.append(connection)

        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection, channel)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def disconnect_all(self):
        """Disconnect all WebSocket connections"""
        for channel in self.active_connections:
            for connection in self.active_connections[channel][:]:
                try:
                    await connection.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {e}")
            self.active_connections[channel].clear()
        logger.info("All WebSocket connections closed")
