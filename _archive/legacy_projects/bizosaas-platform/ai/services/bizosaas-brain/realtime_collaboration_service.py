"""
Real-time Collaboration Service for BizOSaaS Platform
Provides WebSocket-based real-time AI assistance and collaborative editing across all platforms
"""

import asyncio
import json
import structlog
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Any, Union
from uuid import UUID, uuid4
from enum import Enum
from dataclasses import dataclass, asdict
from pydantic import BaseModel, Field

import websockets
from fastapi import WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.websockets import WebSocketState

from enhanced_tenant_context import EnhancedTenantContext, PlatformType
from tenant_aware_ai_coordinator import TenantAwareAICoordinator, AgentSpecialization
from shared.rls_manager import RLSManager

logger = structlog.get_logger(__name__)


class CollaborationEventType(str, Enum):
    """Types of real-time collaboration events"""
    # AI Assistance Events
    AI_QUERY = "ai_query"
    AI_RESPONSE = "ai_response"
    AI_THINKING = "ai_thinking"
    AI_AGENT_ASSIGNMENT = "ai_agent_assignment"
    AI_TASK_UPDATE = "ai_task_update"

    # Document Collaboration Events
    DOCUMENT_EDIT = "document_edit"
    CURSOR_POSITION = "cursor_position"
    SELECTION_CHANGE = "selection_change"
    DOCUMENT_LOCK = "document_lock"
    DOCUMENT_UNLOCK = "document_unlock"

    # User Presence Events
    USER_JOIN = "user_join"
    USER_LEAVE = "user_leave"
    USER_TYPING = "user_typing"
    USER_ACTIVE = "user_active"
    USER_IDLE = "user_idle"

    # System Events
    NOTIFICATION = "notification"
    ERROR = "error"
    HEARTBEAT = "heartbeat"


class CollaborationScope(str, Enum):
    """Scope of collaboration sessions"""
    TENANT_WIDE = "tenant_wide"
    PLATFORM_SPECIFIC = "platform_specific"
    DOCUMENT_SPECIFIC = "document_specific"
    CAMPAIGN_SPECIFIC = "campaign_specific"
    PROJECT_SPECIFIC = "project_specific"


@dataclass
class CollaborationEvent:
    """Real-time collaboration event"""
    event_id: str
    event_type: CollaborationEventType
    scope: CollaborationScope
    tenant_id: str
    platform: PlatformType
    user_id: str
    session_id: str
    timestamp: datetime
    data: Dict[str, Any]
    target_users: Optional[List[str]] = None  # None means broadcast to all


class UserPresence(BaseModel):
    """User presence information"""
    user_id: str
    tenant_id: str
    platform: PlatformType
    session_id: str
    status: str = "active"  # active, idle, away
    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    current_document: Optional[str] = None
    cursor_position: Optional[Dict[str, Any]] = None
    capabilities: Dict[str, bool] = Field(default_factory=dict)


class CollaborationSession(BaseModel):
    """Collaboration session management"""
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str
    platform: PlatformType
    scope: CollaborationScope
    scope_id: str  # document_id, campaign_id, etc.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    participants: Dict[str, UserPresence] = Field(default_factory=dict)
    active_locks: Dict[str, str] = Field(default_factory=dict)  # resource_id -> user_id
    shared_state: Dict[str, Any] = Field(default_factory=dict)


class AIAssistanceSession(BaseModel):
    """AI assistance session tracking"""
    assistance_id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str
    user_id: str
    platform: PlatformType
    agent_assignments: Dict[str, str] = Field(default_factory=dict)  # task_id -> agent_id
    active_tasks: List[str] = Field(default_factory=list)
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    context_data: Dict[str, Any] = Field(default_factory=dict)


class RealtimeCollaborationService:
    """
    Service for managing real-time collaboration and AI assistance
    """

    def __init__(
        self,
        ai_coordinator: TenantAwareAICoordinator,
        rls_manager: RLSManager
    ):
        self.ai_coordinator = ai_coordinator
        self.rls_manager = rls_manager
        self.logger = logger.bind(component="realtime_collaboration")

        # Connection management
        self.active_connections: Dict[str, WebSocket] = {}  # session_id -> websocket
        self.user_sessions: Dict[str, Set[str]] = {}  # user_id -> set of session_ids
        self.tenant_sessions: Dict[str, Set[str]] = {}  # tenant_id -> set of session_ids

        # Session management
        self.collaboration_sessions: Dict[str, CollaborationSession] = {}
        self.ai_assistance_sessions: Dict[str, AIAssistanceSession] = {}

        # Event queues for different scopes
        self.event_queues: Dict[str, asyncio.Queue] = {}

        # Background tasks
        self.background_tasks: Set[asyncio.Task] = set()

        # Start background services
        asyncio.create_task(self._heartbeat_monitor())
        asyncio.create_task(self._cleanup_inactive_sessions())

    async def connect_websocket(
        self,
        websocket: WebSocket,
        tenant_context: EnhancedTenantContext,
        user_id: str,
        platform: PlatformType,
        scope: CollaborationScope,
        scope_id: str
    ) -> str:
        """
        Connect a WebSocket for real-time collaboration
        """
        try:
            await websocket.accept()

            session_id = str(uuid4())
            self.active_connections[session_id] = websocket

            # Track user sessions
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = set()
            self.user_sessions[user_id].add(session_id)

            # Track tenant sessions
            if tenant_context.tenant_id not in self.tenant_sessions:
                self.tenant_sessions[tenant_context.tenant_id] = set()
            self.tenant_sessions[tenant_context.tenant_id].add(session_id)

            # Create or join collaboration session
            collaboration_session = await self._get_or_create_collaboration_session(
                tenant_context.tenant_id, platform, scope, scope_id
            )

            # Add user presence
            user_presence = UserPresence(
                user_id=user_id,
                tenant_id=tenant_context.tenant_id,
                platform=platform,
                session_id=session_id
            )
            collaboration_session.participants[user_id] = user_presence

            # Create AI assistance session
            ai_session = AIAssistanceSession(
                tenant_id=tenant_context.tenant_id,
                user_id=user_id,
                platform=platform
            )
            self.ai_assistance_sessions[session_id] = ai_session

            # Broadcast user join event
            await self._broadcast_event(
                CollaborationEvent(
                    event_id=str(uuid4()),
                    event_type=CollaborationEventType.USER_JOIN,
                    scope=scope,
                    tenant_id=tenant_context.tenant_id,
                    platform=platform,
                    user_id=user_id,
                    session_id=session_id,
                    timestamp=datetime.now(timezone.utc),
                    data={"user_presence": asdict(user_presence)}
                ),
                exclude_user=user_id
            )

            # Send current collaboration state to new user
            await self._send_collaboration_state(websocket, collaboration_session)

            self.logger.info(
                "User connected to collaboration session",
                session_id=session_id,
                user_id=user_id,
                tenant_id=tenant_context.tenant_id,
                platform=platform.value,
                scope=scope.value
            )

            return session_id

        except Exception as e:
            self.logger.error(
                "Failed to connect WebSocket",
                error=str(e),
                user_id=user_id,
                tenant_id=tenant_context.tenant_id
            )
            await websocket.close(code=1011, reason="Connection failed")
            raise

    async def disconnect_websocket(self, session_id: str) -> None:
        """
        Disconnect a WebSocket and clean up resources
        """
        try:
            if session_id not in self.active_connections:
                return

            websocket = self.active_connections[session_id]

            # Get session info before cleanup
            ai_session = self.ai_assistance_sessions.get(session_id)
            if ai_session:
                user_id = ai_session.user_id
                tenant_id = ai_session.tenant_id
                platform = ai_session.platform

                # Find collaboration session
                collaboration_session = None
                for session in self.collaboration_sessions.values():
                    if user_id in session.participants:
                        collaboration_session = session
                        break

                # Remove user presence
                if collaboration_session and user_id in collaboration_session.participants:
                    del collaboration_session.participants[user_id]

                    # Broadcast user leave event
                    await self._broadcast_event(
                        CollaborationEvent(
                            event_id=str(uuid4()),
                            event_type=CollaborationEventType.USER_LEAVE,
                            scope=collaboration_session.scope,
                            tenant_id=tenant_id,
                            platform=platform,
                            user_id=user_id,
                            session_id=session_id,
                            timestamp=datetime.now(timezone.utc),
                            data={"reason": "disconnect"}
                        ),
                        exclude_user=user_id
                    )

            # Clean up connections
            del self.active_connections[session_id]

            # Clean up user sessions
            if ai_session and user_id in self.user_sessions:
                self.user_sessions[user_id].discard(session_id)
                if not self.user_sessions[user_id]:
                    del self.user_sessions[user_id]

            # Clean up tenant sessions
            if ai_session and tenant_id in self.tenant_sessions:
                self.tenant_sessions[tenant_id].discard(session_id)
                if not self.tenant_sessions[tenant_id]:
                    del self.tenant_sessions[tenant_id]

            # Clean up AI assistance session
            if session_id in self.ai_assistance_sessions:
                del self.ai_assistance_sessions[session_id]

            # Close WebSocket if still open
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.close()

            self.logger.info(
                "User disconnected from collaboration session",
                session_id=session_id
            )

        except Exception as e:
            self.logger.error(
                "Error during WebSocket disconnect",
                session_id=session_id,
                error=str(e)
            )

    async def handle_websocket_message(
        self,
        session_id: str,
        message: Dict[str, Any]
    ) -> None:
        """
        Handle incoming WebSocket message
        """
        try:
            ai_session = self.ai_assistance_sessions.get(session_id)
            if not ai_session:
                await self._send_error(session_id, "Session not found")
                return

            event_type = CollaborationEventType(message.get("type"))
            data = message.get("data", {})

            # Update user activity
            await self._update_user_activity(session_id)

            # Handle different event types
            if event_type == CollaborationEventType.AI_QUERY:
                await self._handle_ai_query(session_id, data)

            elif event_type == CollaborationEventType.DOCUMENT_EDIT:
                await self._handle_document_edit(session_id, data)

            elif event_type == CollaborationEventType.CURSOR_POSITION:
                await self._handle_cursor_position(session_id, data)

            elif event_type == CollaborationEventType.USER_TYPING:
                await self._handle_user_typing(session_id, data)

            elif event_type == CollaborationEventType.DOCUMENT_LOCK:
                await self._handle_document_lock(session_id, data)

            elif event_type == CollaborationEventType.DOCUMENT_UNLOCK:
                await self._handle_document_unlock(session_id, data)

            elif event_type == CollaborationEventType.HEARTBEAT:
                await self._handle_heartbeat(session_id)

            else:
                self.logger.warning(
                    "Unknown event type",
                    session_id=session_id,
                    event_type=event_type
                )

        except Exception as e:
            self.logger.error(
                "Error handling WebSocket message",
                session_id=session_id,
                error=str(e),
                message=message
            )
            await self._send_error(session_id, f"Message handling error: {str(e)}")

    async def _handle_ai_query(self, session_id: str, data: Dict[str, Any]) -> None:
        """
        Handle AI query from user
        """
        ai_session = self.ai_assistance_sessions.get(session_id)
        if not ai_session:
            return

        query = data.get("query", "")
        context = data.get("context", {})

        # Send thinking notification
        await self._send_to_session(
            session_id,
            {
                "type": CollaborationEventType.AI_THINKING,
                "data": {
                    "message": "AI is analyzing your request...",
                    "query": query
                }
            }
        )

        try:
            # Get tenant context
            async with self.rls_manager.pool.acquire() as conn:
                tenant_context_data = await conn.fetchrow(
                    "SELECT * FROM tenants WHERE tenant_id = $1",
                    ai_session.tenant_id
                )

                if not tenant_context_data:
                    await self._send_error(session_id, "Tenant not found")
                    return

            # Coordinate with AI agents
            response = await self.ai_coordinator.process_user_query(
                tenant_id=ai_session.tenant_id,
                platform=ai_session.platform,
                user_id=ai_session.user_id,
                query=query,
                context=context
            )

            # Update AI session
            ai_session.conversation_history.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "type": "user_query",
                "query": query,
                "context": context
            })

            ai_session.conversation_history.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "type": "ai_response",
                "response": response
            })

            # Send AI response
            await self._send_to_session(
                session_id,
                {
                    "type": CollaborationEventType.AI_RESPONSE,
                    "data": {
                        "response": response,
                        "query": query,
                        "agent_assignments": response.get("agent_assignments", {})
                    }
                }
            )

        except Exception as e:
            self.logger.error(
                "Error processing AI query",
                session_id=session_id,
                error=str(e)
            )
            await self._send_error(session_id, f"AI processing error: {str(e)}")

    async def _handle_document_edit(self, session_id: str, data: Dict[str, Any]) -> None:
        """
        Handle document editing events
        """
        ai_session = self.ai_assistance_sessions.get(session_id)
        if not ai_session:
            return

        # Find collaboration session
        collaboration_session = None
        for session in self.collaboration_sessions.values():
            if ai_session.user_id in session.participants:
                collaboration_session = session
                break

        if not collaboration_session:
            return

        # Broadcast edit to other participants
        await self._broadcast_event(
            CollaborationEvent(
                event_id=str(uuid4()),
                event_type=CollaborationEventType.DOCUMENT_EDIT,
                scope=collaboration_session.scope,
                tenant_id=ai_session.tenant_id,
                platform=ai_session.platform,
                user_id=ai_session.user_id,
                session_id=session_id,
                timestamp=datetime.now(timezone.utc),
                data=data
            ),
            exclude_user=ai_session.user_id
        )

    async def _handle_cursor_position(self, session_id: str, data: Dict[str, Any]) -> None:
        """
        Handle cursor position updates
        """
        ai_session = self.ai_assistance_sessions.get(session_id)
        if not ai_session:
            return

        # Update user presence
        for session in self.collaboration_sessions.values():
            if ai_session.user_id in session.participants:
                session.participants[ai_session.user_id].cursor_position = data
                break

        # Broadcast cursor position
        await self._broadcast_event(
            CollaborationEvent(
                event_id=str(uuid4()),
                event_type=CollaborationEventType.CURSOR_POSITION,
                scope=CollaborationScope.DOCUMENT_SPECIFIC,
                tenant_id=ai_session.tenant_id,
                platform=ai_session.platform,
                user_id=ai_session.user_id,
                session_id=session_id,
                timestamp=datetime.now(timezone.utc),
                data=data
            ),
            exclude_user=ai_session.user_id
        )

    async def _handle_user_typing(self, session_id: str, data: Dict[str, Any]) -> None:
        """
        Handle user typing indicators
        """
        ai_session = self.ai_assistance_sessions.get(session_id)
        if not ai_session:
            return

        await self._broadcast_event(
            CollaborationEvent(
                event_id=str(uuid4()),
                event_type=CollaborationEventType.USER_TYPING,
                scope=CollaborationScope.DOCUMENT_SPECIFIC,
                tenant_id=ai_session.tenant_id,
                platform=ai_session.platform,
                user_id=ai_session.user_id,
                session_id=session_id,
                timestamp=datetime.now(timezone.utc),
                data=data
            ),
            exclude_user=ai_session.user_id
        )

    async def _handle_document_lock(self, session_id: str, data: Dict[str, Any]) -> None:
        """
        Handle document locking for exclusive editing
        """
        ai_session = self.ai_assistance_sessions.get(session_id)
        if not ai_session:
            return

        resource_id = data.get("resource_id")
        if not resource_id:
            return

        # Find collaboration session
        collaboration_session = None
        for session in self.collaboration_sessions.values():
            if ai_session.user_id in session.participants:
                collaboration_session = session
                break

        if not collaboration_session:
            return

        # Check if resource is already locked
        if resource_id in collaboration_session.active_locks:
            await self._send_error(session_id, f"Resource {resource_id} is already locked")
            return

        # Lock the resource
        collaboration_session.active_locks[resource_id] = ai_session.user_id

        # Broadcast lock event
        await self._broadcast_event(
            CollaborationEvent(
                event_id=str(uuid4()),
                event_type=CollaborationEventType.DOCUMENT_LOCK,
                scope=collaboration_session.scope,
                tenant_id=ai_session.tenant_id,
                platform=ai_session.platform,
                user_id=ai_session.user_id,
                session_id=session_id,
                timestamp=datetime.now(timezone.utc),
                data=data
            )
        )

    async def _handle_document_unlock(self, session_id: str, data: Dict[str, Any]) -> None:
        """
        Handle document unlocking
        """
        ai_session = self.ai_assistance_sessions.get(session_id)
        if not ai_session:
            return

        resource_id = data.get("resource_id")
        if not resource_id:
            return

        # Find collaboration session
        collaboration_session = None
        for session in self.collaboration_sessions.values():
            if ai_session.user_id in session.participants:
                collaboration_session = session
                break

        if not collaboration_session:
            return

        # Check if user owns the lock
        if collaboration_session.active_locks.get(resource_id) != ai_session.user_id:
            await self._send_error(session_id, f"You don't own the lock for {resource_id}")
            return

        # Unlock the resource
        del collaboration_session.active_locks[resource_id]

        # Broadcast unlock event
        await self._broadcast_event(
            CollaborationEvent(
                event_id=str(uuid4()),
                event_type=CollaborationEventType.DOCUMENT_UNLOCK,
                scope=collaboration_session.scope,
                tenant_id=ai_session.tenant_id,
                platform=ai_session.platform,
                user_id=ai_session.user_id,
                session_id=session_id,
                timestamp=datetime.now(timezone.utc),
                data=data
            )
        )

    async def _handle_heartbeat(self, session_id: str) -> None:
        """
        Handle heartbeat to keep connection alive
        """
        await self._update_user_activity(session_id)
        await self._send_to_session(
            session_id,
            {
                "type": CollaborationEventType.HEARTBEAT,
                "data": {"timestamp": datetime.now(timezone.utc).isoformat()}
            }
        )

    async def _get_or_create_collaboration_session(
        self,
        tenant_id: str,
        platform: PlatformType,
        scope: CollaborationScope,
        scope_id: str
    ) -> CollaborationSession:
        """
        Get existing or create new collaboration session
        """
        session_key = f"{tenant_id}:{platform.value}:{scope.value}:{scope_id}"

        if session_key not in self.collaboration_sessions:
            self.collaboration_sessions[session_key] = CollaborationSession(
                tenant_id=tenant_id,
                platform=platform,
                scope=scope,
                scope_id=scope_id
            )

        return self.collaboration_sessions[session_key]

    async def _update_user_activity(self, session_id: str) -> None:
        """
        Update user's last activity timestamp
        """
        ai_session = self.ai_assistance_sessions.get(session_id)
        if not ai_session:
            return

        # Update presence in collaboration session
        for session in self.collaboration_sessions.values():
            if ai_session.user_id in session.participants:
                session.participants[ai_session.user_id].last_activity = datetime.now(timezone.utc)
                session.participants[ai_session.user_id].status = "active"
                break

    async def _broadcast_event(
        self,
        event: CollaborationEvent,
        exclude_user: Optional[str] = None
    ) -> None:
        """
        Broadcast event to relevant participants
        """
        try:
            # Determine target sessions based on scope
            target_sessions = set()

            if event.scope == CollaborationScope.TENANT_WIDE:
                target_sessions = self.tenant_sessions.get(event.tenant_id, set())

            elif event.scope in [
                CollaborationScope.PLATFORM_SPECIFIC,
                CollaborationScope.DOCUMENT_SPECIFIC,
                CollaborationScope.CAMPAIGN_SPECIFIC,
                CollaborationScope.PROJECT_SPECIFIC
            ]:
                # Find relevant collaboration sessions
                for session in self.collaboration_sessions.values():
                    if (session.tenant_id == event.tenant_id and
                        session.platform == event.platform):
                        target_sessions.update(
                            session_id for user_id, presence in session.participants.items()
                            for session_id in self.user_sessions.get(user_id, set())
                        )

            # Send to target sessions
            message = {
                "type": event.event_type,
                "data": event.data,
                "metadata": {
                    "event_id": event.event_id,
                    "timestamp": event.timestamp.isoformat(),
                    "user_id": event.user_id,
                    "platform": event.platform.value
                }
            }

            tasks = []
            for session_id in target_sessions:
                ai_session = self.ai_assistance_sessions.get(session_id)
                if ai_session and (not exclude_user or ai_session.user_id != exclude_user):
                    tasks.append(self._send_to_session(session_id, message))

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

        except Exception as e:
            self.logger.error(
                "Error broadcasting event",
                event_type=event.event_type,
                error=str(e)
            )

    async def _send_to_session(self, session_id: str, message: Dict[str, Any]) -> None:
        """
        Send message to specific session
        """
        try:
            websocket = self.active_connections.get(session_id)
            if websocket and websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_json(message)
        except Exception as e:
            self.logger.error(
                "Error sending message to session",
                session_id=session_id,
                error=str(e)
            )
            # Clean up broken connection
            await self.disconnect_websocket(session_id)

    async def _send_error(self, session_id: str, error_message: str) -> None:
        """
        Send error message to session
        """
        await self._send_to_session(
            session_id,
            {
                "type": CollaborationEventType.ERROR,
                "data": {
                    "error": error_message,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )

    async def _send_collaboration_state(
        self,
        websocket: WebSocket,
        session: CollaborationSession
    ) -> None:
        """
        Send current collaboration state to new participant
        """
        try:
            state = {
                "type": "collaboration_state",
                "data": {
                    "session_id": session.session_id,
                    "participants": {
                        user_id: {
                            "user_id": presence.user_id,
                            "status": presence.status,
                            "cursor_position": presence.cursor_position,
                            "last_activity": presence.last_activity.isoformat()
                        }
                        for user_id, presence in session.participants.items()
                    },
                    "active_locks": session.active_locks,
                    "shared_state": session.shared_state
                }
            }

            await websocket.send_json(state)

        except Exception as e:
            self.logger.error(
                "Error sending collaboration state",
                session_id=session.session_id,
                error=str(e)
            )

    async def _heartbeat_monitor(self) -> None:
        """
        Background task to monitor connection health
        """
        while True:
            try:
                await asyncio.sleep(30)  # Check every 30 seconds

                current_time = datetime.now(timezone.utc)
                inactive_sessions = []

                # Check for inactive sessions
                for session_id, ai_session in self.ai_assistance_sessions.items():
                    websocket = self.active_connections.get(session_id)
                    if not websocket or websocket.client_state != WebSocketState.CONNECTED:
                        inactive_sessions.append(session_id)
                        continue

                    # Send heartbeat
                    try:
                        await websocket.ping()
                    except Exception:
                        inactive_sessions.append(session_id)

                # Clean up inactive sessions
                for session_id in inactive_sessions:
                    await self.disconnect_websocket(session_id)

            except Exception as e:
                self.logger.error("Error in heartbeat monitor", error=str(e))

    async def _cleanup_inactive_sessions(self) -> None:
        """
        Background task to clean up old collaboration sessions
        """
        while True:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes

                current_time = datetime.now(timezone.utc)
                sessions_to_remove = []

                # Find empty or old sessions
                for session_key, session in self.collaboration_sessions.items():
                    if not session.participants:
                        sessions_to_remove.append(session_key)
                    elif (current_time - session.created_at).total_seconds() > 86400:  # 24 hours
                        # Check if any participants are still active
                        has_active_participants = any(
                            (current_time - presence.last_activity).total_seconds() < 3600
                            for presence in session.participants.values()
                        )
                        if not has_active_participants:
                            sessions_to_remove.append(session_key)

                # Remove old sessions
                for session_key in sessions_to_remove:
                    del self.collaboration_sessions[session_key]

                self.logger.info(
                    "Cleaned up inactive sessions",
                    removed_count=len(sessions_to_remove)
                )

            except Exception as e:
                self.logger.error("Error in session cleanup", error=str(e))

    async def get_collaboration_stats(self, tenant_id: str) -> Dict[str, Any]:
        """
        Get collaboration statistics for a tenant
        """
        try:
            tenant_sessions = self.tenant_sessions.get(tenant_id, set())
            active_users = set()
            platform_distribution = {}

            for session_id in tenant_sessions:
                ai_session = self.ai_assistance_sessions.get(session_id)
                if ai_session:
                    active_users.add(ai_session.user_id)
                    platform = ai_session.platform.value
                    platform_distribution[platform] = platform_distribution.get(platform, 0) + 1

            # Get collaboration sessions for tenant
            active_collaborations = [
                session for session in self.collaboration_sessions.values()
                if session.tenant_id == tenant_id and session.participants
            ]

            return {
                "active_sessions": len(tenant_sessions),
                "active_users": len(active_users),
                "active_collaborations": len(active_collaborations),
                "platform_distribution": platform_distribution,
                "collaboration_sessions": [
                    {
                        "session_id": session.session_id,
                        "platform": session.platform.value,
                        "scope": session.scope.value,
                        "participant_count": len(session.participants),
                        "created_at": session.created_at.isoformat()
                    }
                    for session in active_collaborations
                ]
            }

        except Exception as e:
            self.logger.error(
                "Error getting collaboration stats",
                tenant_id=tenant_id,
                error=str(e)
            )
            return {}


# Singleton instance
collaboration_service: Optional[RealtimeCollaborationService] = None


def get_collaboration_service() -> RealtimeCollaborationService:
    """Get the global collaboration service instance"""
    global collaboration_service
    if collaboration_service is None:
        raise RuntimeError("Collaboration service not initialized")
    return collaboration_service


def initialize_collaboration_service(
    ai_coordinator: TenantAwareAICoordinator,
    rls_manager: RLSManager
) -> RealtimeCollaborationService:
    """Initialize the global collaboration service"""
    global collaboration_service
    collaboration_service = RealtimeCollaborationService(ai_coordinator, rls_manager)
    return collaboration_service