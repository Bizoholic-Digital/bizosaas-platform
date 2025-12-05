"""
WebSocket connection manager for real-time chat functionality
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass
from collections import defaultdict

from fastapi import WebSocket, WebSocketDisconnect
from .models import ChatSession, ChatMessage, MessageType, UserRole, WebSocketMessage

logger = logging.getLogger(__name__)

@dataclass
class ConnectionInfo:
    """Information about a WebSocket connection"""
    websocket: WebSocket
    user_id: str
    tenant_id: str
    role: UserRole
    session_id: str
    connected_at: datetime
    last_activity: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class WebSocketManager:
    """Manages WebSocket connections for real-time chat"""
    
    def __init__(self):
        # Active connections by session ID
        self.connections: Dict[str, ConnectionInfo] = {}
        
        # User sessions mapping
        self.user_sessions: Dict[str, ChatSession] = {}
        
        # Connections by tenant for broadcasting
        self.tenant_connections: Dict[str, Set[str]] = defaultdict(set)
        
        # Connections by user for multi-device support
        self.user_connections: Dict[str, Set[str]] = defaultdict(set)
        
        # Typing indicators
        self.typing_sessions: Dict[str, datetime] = {}
        
        # Message queue for offline users
        self.offline_messages: Dict[str, List[WebSocketMessage]] = defaultdict(list)
    
    async def connect(
        self, 
        websocket: WebSocket, 
        session_id: str,
        user_id: str,
        tenant_id: str,
        role: UserRole,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> bool:
        """Accept WebSocket connection and register session"""
        try:
            await websocket.accept()
            
            # Create connection info
            connection_info = ConnectionInfo(
                websocket=websocket,
                user_id=user_id,
                tenant_id=tenant_id,
                role=role,
                session_id=session_id,
                connected_at=datetime.now(timezone.utc),
                last_activity=datetime.now(timezone.utc),
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Register connection
            self.connections[session_id] = connection_info
            self.tenant_connections[tenant_id].add(session_id)
            self.user_connections[user_id].add(session_id)
            
            # Create or restore chat session
            if session_id not in self.user_sessions:
                self.user_sessions[session_id] = ChatSession(
                    id=session_id,
                    user_id=user_id,
                    tenant_id=tenant_id,
                    role=role
                )
            
            # Send connection confirmation
            await self.send_system_message(
                session_id,
                "Connected to AI Chat Service",
                {"connection_time": connection_info.connected_at.isoformat()}
            )
            
            # Send any queued offline messages
            await self._send_offline_messages(user_id, session_id)
            
            logger.info(f"WebSocket connected: session={session_id}, user={user_id}, tenant={tenant_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error connecting WebSocket: {e}")
            return False
    
    async def disconnect(self, session_id: str, reason: str = "client_disconnect"):
        """Disconnect WebSocket session"""
        if session_id not in self.connections:
            return
        
        connection_info = self.connections[session_id]
        
        try:
            # Update session as inactive
            if session_id in self.user_sessions:
                self.user_sessions[session_id].is_active = False
                self.user_sessions[session_id].last_activity = datetime.now(timezone.utc)
            
            # Remove from tracking
            self.tenant_connections[connection_info.tenant_id].discard(session_id)
            self.user_connections[connection_info.user_id].discard(session_id)
            
            # Clean up empty sets
            if not self.tenant_connections[connection_info.tenant_id]:
                del self.tenant_connections[connection_info.tenant_id]
            if not self.user_connections[connection_info.user_id]:
                del self.user_connections[connection_info.user_id]
            
            # Remove typing indicator
            if session_id in self.typing_sessions:
                del self.typing_sessions[session_id]
            
            # Remove connection
            del self.connections[session_id]
            
            logger.info(f"WebSocket disconnected: session={session_id}, reason={reason}")
            
        except Exception as e:
            logger.error(f"Error disconnecting WebSocket: {e}")
    
    async def send_message(self, session_id: str, message: WebSocketMessage) -> bool:
        """Send message to specific session"""
        if session_id not in self.connections:
            # Queue message for offline delivery
            await self._queue_offline_message(session_id, message)
            return False
        
        try:
            connection_info = self.connections[session_id]
            message_data = message.dict()
            
            await connection_info.websocket.send_text(json.dumps(message_data))
            
            # Update last activity
            connection_info.last_activity = datetime.now(timezone.utc)
            
            return True
            
        except WebSocketDisconnect:
            await self.disconnect(session_id, "connection_lost")
            return False
        except Exception as e:
            logger.error(f"Error sending message to {session_id}: {e}")
            return False
    
    async def send_system_message(
        self, 
        session_id: str, 
        content: str, 
        metadata: Dict[str, Any] = None
    ) -> bool:
        """Send system message to session"""
        message = WebSocketMessage(
            type="system",
            content=content,
            session_id=session_id,
            metadata=metadata or {}
        )
        return await self.send_message(session_id, message)
    
    async def send_chat_message(
        self,
        session_id: str,
        chat_message: ChatMessage
    ) -> bool:
        """Send chat message via WebSocket"""
        ws_message = WebSocketMessage(
            type="message",
            content=chat_message.content,
            session_id=session_id,
            user_id=chat_message.user_id,
            metadata={
                "message_id": chat_message.id,
                "message_type": chat_message.type,
                "agent_name": chat_message.agent_name,
                "confidence": chat_message.confidence,
                "suggested_actions": chat_message.suggested_actions,
                "timestamp": chat_message.timestamp.isoformat()
            }
        )
        return await self.send_message(session_id, ws_message)
    
    async def broadcast_to_tenant(
        self, 
        tenant_id: str, 
        message: WebSocketMessage,
        exclude_session: Optional[str] = None
    ) -> int:
        """Broadcast message to all sessions in a tenant"""
        if tenant_id not in self.tenant_connections:
            return 0
        
        sent_count = 0
        session_ids = list(self.tenant_connections[tenant_id])
        
        for session_id in session_ids:
            if exclude_session and session_id == exclude_session:
                continue
            
            if await self.send_message(session_id, message):
                sent_count += 1
        
        return sent_count
    
    async def broadcast_to_user(
        self,
        user_id: str,
        message: WebSocketMessage,
        exclude_session: Optional[str] = None
    ) -> int:
        """Broadcast message to all sessions of a user (multi-device)"""
        if user_id not in self.user_connections:
            return 0
        
        sent_count = 0
        session_ids = list(self.user_connections[user_id])
        
        for session_id in session_ids:
            if exclude_session and session_id == exclude_session:
                continue
            
            if await self.send_message(session_id, message):
                sent_count += 1
        
        return sent_count
    
    async def handle_typing_indicator(
        self, 
        session_id: str, 
        is_typing: bool
    ):
        """Handle typing indicator updates"""
        if session_id not in self.connections:
            return
        
        connection_info = self.connections[session_id]
        
        if is_typing:
            self.typing_sessions[session_id] = datetime.now(timezone.utc)
        else:
            self.typing_sessions.pop(session_id, None)
        
        # Broadcast typing status to other sessions of the same user
        typing_message = WebSocketMessage(
            type="typing",
            content="typing" if is_typing else "stopped_typing",
            session_id=session_id,
            user_id=connection_info.user_id,
            metadata={
                "is_typing": is_typing,
                "session_id": session_id
            }
        )
        
        await self.broadcast_to_user(
            connection_info.user_id, 
            typing_message, 
            exclude_session=session_id
        )
    
    async def _queue_offline_message(self, session_id: str, message: WebSocketMessage):
        """Queue message for offline delivery"""
        # In a production system, you might want to:
        # 1. Store in a persistent queue (Redis, database)
        # 2. Implement TTL for messages
        # 3. Limit queue size per user
        
        connection_info = self.connections.get(session_id)
        if connection_info:
            user_id = connection_info.user_id
            self.offline_messages[user_id].append(message)
            
            # Limit offline queue size
            if len(self.offline_messages[user_id]) > 50:
                self.offline_messages[user_id] = self.offline_messages[user_id][-50:]
    
    async def _send_offline_messages(self, user_id: str, session_id: str):
        """Send queued offline messages to newly connected session"""
        if user_id not in self.offline_messages:
            return
        
        messages = self.offline_messages[user_id]
        sent_count = 0
        
        for message in messages:
            if await self.send_message(session_id, message):
                sent_count += 1
        
        # Clear offline messages after sending
        if sent_count > 0:
            del self.offline_messages[user_id]
            logger.info(f"Delivered {sent_count} offline messages to user {user_id}")
    
    async def cleanup_inactive_connections(self, max_idle_minutes: int = 30):
        """Clean up inactive WebSocket connections"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=max_idle_minutes)
        
        inactive_sessions = []
        for session_id, connection_info in self.connections.items():
            if connection_info.last_activity < cutoff_time:
                inactive_sessions.append(session_id)
        
        for session_id in inactive_sessions:
            await self.disconnect(session_id, "idle_timeout")
        
        return len(inactive_sessions)
    
    async def cleanup_typing_indicators(self, max_typing_seconds: int = 10):
        """Clean up stale typing indicators"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=max_typing_seconds)
        
        stale_sessions = []
        for session_id, typing_time in self.typing_sessions.items():
            if typing_time < cutoff_time:
                stale_sessions.append(session_id)
        
        for session_id in stale_sessions:
            await self.handle_typing_indicator(session_id, False)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        active_connections = len(self.connections)
        tenants_with_connections = len(self.tenant_connections)
        users_with_connections = len(self.user_connections)
        typing_sessions = len(self.typing_sessions)
        queued_messages = sum(len(messages) for messages in self.offline_messages.values())
        
        # Calculate average session duration
        now = datetime.now(timezone.utc)
        session_durations = [
            (now - conn.connected_at).total_seconds()
            for conn in self.connections.values()
        ]
        avg_session_duration = sum(session_durations) / len(session_durations) if session_durations else 0
        
        return {
            "active_connections": active_connections,
            "tenants_with_connections": tenants_with_connections,
            "users_with_connections": users_with_connections,
            "typing_sessions": typing_sessions,
            "queued_offline_messages": queued_messages,
            "average_session_duration_seconds": round(avg_session_duration, 2),
            "connection_by_role": self._get_connections_by_role()
        }
    
    def _get_connections_by_role(self) -> Dict[str, int]:
        """Get connection count by user role"""
        role_counts = defaultdict(int)
        for connection_info in self.connections.values():
            role_counts[connection_info.role] += 1
        return dict(role_counts)
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific session"""
        if session_id not in self.connections:
            return None
        
        connection_info = self.connections[session_id]
        session = self.user_sessions.get(session_id)
        
        return {
            "session_id": session_id,
            "user_id": connection_info.user_id,
            "tenant_id": connection_info.tenant_id,
            "role": connection_info.role,
            "connected_at": connection_info.connected_at.isoformat(),
            "last_activity": connection_info.last_activity.isoformat(),
            "ip_address": connection_info.ip_address,
            "user_agent": connection_info.user_agent,
            "is_typing": session_id in self.typing_sessions,
            "message_count": len(session.messages) if session else 0,
            "session_active": session.is_active if session else False
        }

# Global WebSocket manager instance
websocket_manager = WebSocketManager()

# Periodic cleanup task
async def periodic_cleanup():
    """Periodic cleanup of inactive connections and stale data"""
    while True:
        try:
            # Clean up inactive connections (30 minutes)
            inactive_count = await websocket_manager.cleanup_inactive_connections(30)
            
            # Clean up stale typing indicators (10 seconds)
            await websocket_manager.cleanup_typing_indicators(10)
            
            if inactive_count > 0:
                logger.info(f"Cleaned up {inactive_count} inactive WebSocket connections")
            
        except Exception as e:
            logger.error(f"Error in periodic cleanup: {e}")
        
        # Run cleanup every 5 minutes
        await asyncio.sleep(300)