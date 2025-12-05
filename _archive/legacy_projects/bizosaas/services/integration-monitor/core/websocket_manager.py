"""
WebSocket Manager
Manages real-time WebSocket connections for dashboard updates
"""

import asyncio
import json
import logging
from typing import List, Dict, Any
from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class WebSocketManager:
    """
    Manages WebSocket connections for real-time dashboard updates
    Handles connection lifecycle, broadcasting, and message routing
    """
    
    def __init__(self):
        # Store active connections
        self.active_connections: List[WebSocket] = []
        
        # Connection metadata
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
        
        # Statistics
        self.stats = {
            'total_connections': 0,
            'current_connections': 0,
            'messages_sent': 0,
            'messages_failed': 0,
            'connection_errors': 0
        }
        
        logger.info("WebSocket Manager initialized")
    
    async def connect(self, websocket: WebSocket, client_info: Dict[str, Any] = None):
        """Accept a new WebSocket connection"""
        try:
            await websocket.accept()
            
            # Add to active connections
            self.active_connections.append(websocket)
            
            # Store connection metadata
            self.connection_metadata[websocket] = {
                'connected_at': asyncio.get_event_loop().time(),
                'client_info': client_info or {},
                'messages_sent': 0,
                'last_activity': asyncio.get_event_loop().time()
            }
            
            # Update statistics
            self.stats['total_connections'] += 1
            self.stats['current_connections'] = len(self.active_connections)
            
            logger.info(f"WebSocket connection accepted. Total connections: {len(self.active_connections)}")
            
            # Send welcome message
            await self.send_personal_message(websocket, {
                'type': 'connection_established',
                'timestamp': asyncio.get_event_loop().time(),
                'connection_id': id(websocket),
                'message': 'Connected to BizOSaaS Integration Monitor'
            })
            
        except Exception as e:
            logger.error(f"Failed to accept WebSocket connection: {e}")
            self.stats['connection_errors'] += 1
            raise
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        try:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
                
                # Remove metadata
                if websocket in self.connection_metadata:
                    metadata = self.connection_metadata.pop(websocket)
                    connection_duration = asyncio.get_event_loop().time() - metadata['connected_at']
                    
                    logger.info(f"WebSocket disconnected after {connection_duration:.2f}s. "
                              f"Messages sent: {metadata['messages_sent']}")
                
                # Update statistics
                self.stats['current_connections'] = len(self.active_connections)
                
                logger.info(f"WebSocket connection removed. Active connections: {len(self.active_connections)}")
            
        except Exception as e:
            logger.error(f"Error during WebSocket disconnect: {e}")
    
    async def send_personal_message(self, websocket: WebSocket, message: Dict[str, Any]):
        """Send message to a specific WebSocket connection"""
        try:
            # Convert message to JSON
            message_str = json.dumps(message, default=str)
            
            # Send message
            await websocket.send_text(message_str)
            
            # Update statistics
            self.stats['messages_sent'] += 1
            
            # Update connection metadata
            if websocket in self.connection_metadata:
                self.connection_metadata[websocket]['messages_sent'] += 1
                self.connection_metadata[websocket]['last_activity'] = asyncio.get_event_loop().time()
            
            logger.debug(f"Message sent to WebSocket {id(websocket)}: {message.get('type', 'unknown')}")
            
        except WebSocketDisconnect:
            logger.info(f"WebSocket {id(websocket)} disconnected during message send")
            self.disconnect(websocket)
        except Exception as e:
            logger.error(f"Failed to send message to WebSocket {id(websocket)}: {e}")
            self.stats['messages_failed'] += 1
            # Don't disconnect on send errors, the connection might still be valid
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all active WebSocket connections"""
        if not self.active_connections:
            logger.debug("No active WebSocket connections for broadcast")
            return
        
        logger.debug(f"Broadcasting message to {len(self.active_connections)} connections: {message.get('type', 'unknown')}")
        
        # Send to all connections concurrently
        tasks = []
        for connection in self.active_connections.copy():  # Copy to avoid modification during iteration
            task = asyncio.create_task(self.send_personal_message(connection, message))
            tasks.append(task)
        
        # Wait for all sends to complete
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def broadcast_to_subset(self, message: Dict[str, Any], filter_func=None):
        """Broadcast message to subset of connections based on filter"""
        if not self.active_connections:
            return
        
        # Filter connections
        target_connections = []
        for connection in self.active_connections:
            if filter_func is None or filter_func(connection, self.connection_metadata.get(connection, {})):
                target_connections.append(connection)
        
        if not target_connections:
            logger.debug("No connections match filter criteria")
            return
        
        logger.debug(f"Broadcasting to {len(target_connections)} filtered connections")
        
        # Send to filtered connections
        tasks = []
        for connection in target_connections:
            task = asyncio.create_task(self.send_personal_message(connection, message))
            tasks.append(task)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def send_alert_notification(self, alert_data: Dict[str, Any]):
        """Send alert notification to all connections"""
        message = {
            'type': 'alert_notification',
            'timestamp': asyncio.get_event_loop().time(),
            'data': alert_data,
            'priority': alert_data.get('severity', 'medium')
        }
        
        await self.broadcast(message)
    
    async def send_health_update(self, health_data: Dict[str, Any]):
        """Send health status update to all connections"""
        message = {
            'type': 'health_update',
            'timestamp': asyncio.get_event_loop().time(),
            'data': health_data
        }
        
        await self.broadcast(message)
    
    async def send_metrics_update(self, metrics_data: Dict[str, Any]):
        """Send metrics update to all connections"""
        message = {
            'type': 'metrics_update',
            'timestamp': asyncio.get_event_loop().time(),
            'data': metrics_data
        }
        
        await self.broadcast(message)
    
    async def send_failover_notification(self, failover_data: Dict[str, Any]):
        """Send failover notification to all connections"""
        message = {
            'type': 'failover_notification',
            'timestamp': asyncio.get_event_loop().time(),
            'data': failover_data,
            'priority': 'high'
        }
        
        await self.broadcast(message)
    
    async def ping_all_connections(self):
        """Send ping to all connections to keep them alive"""
        if not self.active_connections:
            return
        
        ping_message = {
            'type': 'ping',
            'timestamp': asyncio.get_event_loop().time()
        }
        
        # Send ping and remove failed connections
        failed_connections = []
        
        for connection in self.active_connections.copy():
            try:
                await self.send_personal_message(connection, ping_message)
            except Exception as e:
                logger.warning(f"Ping failed for connection {id(connection)}: {e}")
                failed_connections.append(connection)
        
        # Remove failed connections
        for connection in failed_connections:
            self.disconnect(connection)
    
    async def cleanup_stale_connections(self, max_idle_time: int = 3600):
        """Remove connections that have been idle for too long"""
        current_time = asyncio.get_event_loop().time()
        stale_connections = []
        
        for connection, metadata in self.connection_metadata.items():
            idle_time = current_time - metadata['last_activity']
            if idle_time > max_idle_time:
                stale_connections.append(connection)
        
        for connection in stale_connections:
            logger.info(f"Removing stale connection {id(connection)} (idle for {idle_time:.2f}s)")
            self.disconnect(connection)
            
            # Close the connection
            try:
                await connection.close(code=1000, reason="Connection idle timeout")
            except Exception as e:
                logger.debug(f"Error closing stale connection: {e}")
    
    def has_connections(self) -> bool:
        """Check if there are any active connections"""
        return len(self.active_connections) > 0
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        current_time = asyncio.get_event_loop().time()
        
        # Calculate connection durations
        connection_durations = []
        total_messages = 0
        
        for connection, metadata in self.connection_metadata.items():
            duration = current_time - metadata['connected_at']
            connection_durations.append(duration)
            total_messages += metadata['messages_sent']
        
        avg_duration = sum(connection_durations) / len(connection_durations) if connection_durations else 0
        
        return {
            **self.stats,
            'average_connection_duration': avg_duration,
            'total_messages_to_clients': total_messages,
            'connections_by_duration': {
                'under_1min': len([d for d in connection_durations if d < 60]),
                'under_5min': len([d for d in connection_durations if 60 <= d < 300]),
                'under_30min': len([d for d in connection_durations if 300 <= d < 1800]),
                'over_30min': len([d for d in connection_durations if d >= 1800])
            }
        }
    
    def get_connection_details(self) -> List[Dict[str, Any]]:
        """Get detailed information about all connections"""
        current_time = asyncio.get_event_loop().time()
        details = []
        
        for connection, metadata in self.connection_metadata.items():
            details.append({
                'connection_id': id(connection),
                'connected_at': metadata['connected_at'],
                'duration': current_time - metadata['connected_at'],
                'messages_sent': metadata['messages_sent'],
                'last_activity': metadata['last_activity'],
                'idle_time': current_time - metadata['last_activity'],
                'client_info': metadata['client_info']
            })
        
        return details
    
    async def start_background_tasks(self):
        """Start background maintenance tasks"""
        # Start ping task
        asyncio.create_task(self._ping_task())
        
        # Start cleanup task
        asyncio.create_task(self._cleanup_task())
        
        logger.info("WebSocket background tasks started")
    
    async def _ping_task(self):
        """Background task to ping connections periodically"""
        while True:
            try:
                await asyncio.sleep(30)  # Ping every 30 seconds
                await self.ping_all_connections()
            except Exception as e:
                logger.error(f"Error in ping task: {e}")
    
    async def _cleanup_task(self):
        """Background task to cleanup stale connections"""
        while True:
            try:
                await asyncio.sleep(300)  # Cleanup every 5 minutes
                await self.cleanup_stale_connections()
            except Exception as e:
                logger.error(f"Error in cleanup task: {e}")
    
    async def shutdown(self):
        """Shutdown WebSocket manager and close all connections"""
        logger.info("Shutting down WebSocket Manager")
        
        # Send shutdown notification to all connections
        shutdown_message = {
            'type': 'server_shutdown',
            'timestamp': asyncio.get_event_loop().time(),
            'message': 'Server is shutting down'
        }
        
        await self.broadcast(shutdown_message)
        
        # Close all connections
        for connection in self.active_connections.copy():
            try:
                await connection.close(code=1001, reason="Server shutdown")
            except Exception as e:
                logger.debug(f"Error closing connection during shutdown: {e}")
            
            self.disconnect(connection)
        
        logger.info("All WebSocket connections closed")