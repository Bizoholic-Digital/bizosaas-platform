"""
WebSocket endpoints for real-time collaboration and AI assistance
Integrates with BizOSaaS Platform across all 5 platforms
"""

import asyncio
import json
import structlog
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Request
from fastapi.websockets import WebSocketState
from fastapi.responses import JSONResponse

from enhanced_tenant_context import EnhancedTenantContext, PlatformType
from shared.rls_middleware import RLSRequestHelper, get_tenant_context
from realtime_collaboration_service import (
    RealtimeCollaborationService,
    CollaborationScope,
    get_collaboration_service
)

logger = structlog.get_logger(__name__)


def setup_collaboration_endpoints(app: FastAPI) -> None:
    """
    Setup WebSocket endpoints for real-time collaboration
    """

    @app.websocket("/ws/collaboration/{platform}/{scope}/{scope_id}")
    async def websocket_collaboration_endpoint(
        websocket: WebSocket,
        platform: str,
        scope: str,
        scope_id: str,
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None
    ):
        """
        WebSocket endpoint for real-time collaboration

        Platform: bizoholic, coreldove, business-directory, thrillring, quanttrade
        Scope: tenant-wide, platform-specific, document-specific, campaign-specific, project-specific
        """
        session_id = None
        collaboration_service = get_collaboration_service()

        try:
            # Validate platform
            try:
                platform_type = PlatformType(platform.replace('-', '_').upper())
            except ValueError:
                await websocket.close(code=1008, reason=f"Invalid platform: {platform}")
                return

            # Validate scope
            try:
                collaboration_scope = CollaborationScope(scope.replace('-', '_').upper())
            except ValueError:
                await websocket.close(code=1008, reason=f"Invalid scope: {scope}")
                return

            # Get tenant and user info from query parameters or headers
            if not tenant_id:
                tenant_id = websocket.query_params.get("tenant_id")
            if not user_id:
                user_id = websocket.query_params.get("user_id")

            if not tenant_id or not user_id:
                await websocket.close(code=1008, reason="Missing tenant_id or user_id")
                return

            # Get tenant context (simplified for WebSocket - in production use proper auth)
            # TODO: Implement proper JWT token validation for WebSocket connections
            from enhanced_tenant_context import TenantContextManager
            tenant_manager = TenantContextManager()
            tenant_context = await tenant_manager.get_context(tenant_id)

            if not tenant_context:
                await websocket.close(code=1008, reason="Invalid tenant")
                return

            # Validate platform access
            platform_access = tenant_context.platform_access.get(platform_type)
            if not platform_access or not platform_access.enabled:
                await websocket.close(code=1008, reason=f"No access to {platform} platform")
                return

            # Connect to collaboration service
            session_id = await collaboration_service.connect_websocket(
                websocket=websocket,
                tenant_context=tenant_context,
                user_id=user_id,
                platform=platform_type,
                scope=collaboration_scope,
                scope_id=scope_id
            )

            logger.info(
                "WebSocket collaboration session started",
                session_id=session_id,
                platform=platform,
                scope=scope,
                tenant_id=tenant_id,
                user_id=user_id
            )

            # Message handling loop
            while True:
                try:
                    # Receive message from client
                    message = await websocket.receive_json()

                    # Handle the message
                    await collaboration_service.handle_websocket_message(session_id, message)

                except WebSocketDisconnect:
                    logger.info(
                        "WebSocket client disconnected",
                        session_id=session_id
                    )
                    break

                except Exception as e:
                    logger.error(
                        "Error in WebSocket message loop",
                        session_id=session_id,
                        error=str(e)
                    )
                    await websocket.send_json({
                        "type": "error",
                        "data": {
                            "error": "Message processing error",
                            "details": str(e)
                        }
                    })

        except WebSocketDisconnect:
            logger.info("WebSocket disconnected during setup")
        except Exception as e:
            logger.error(
                "Error in WebSocket collaboration endpoint",
                error=str(e),
                platform=platform,
                scope=scope
            )
            try:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.close(code=1011, reason="Internal server error")
            except:
                pass
        finally:
            # Clean up session
            if session_id:
                await collaboration_service.disconnect_websocket(session_id)

    @app.websocket("/ws/ai-assistant/{platform}/{tenant_id}")
    async def websocket_ai_assistant_endpoint(
        websocket: WebSocket,
        platform: str,
        tenant_id: str,
        user_id: Optional[str] = None
    ):
        """
        Dedicated WebSocket endpoint for AI assistant chat
        Provides direct access to the 93+ AI agents ecosystem
        """
        session_id = None
        collaboration_service = get_collaboration_service()

        try:
            # Validate platform
            try:
                platform_type = PlatformType(platform.replace('-', '_').upper())
            except ValueError:
                await websocket.close(code=1008, reason=f"Invalid platform: {platform}")
                return

            # Get user ID
            if not user_id:
                user_id = websocket.query_params.get("user_id")
            if not user_id:
                await websocket.close(code=1008, reason="Missing user_id")
                return

            # Get tenant context
            from enhanced_tenant_context import TenantContextManager
            tenant_manager = TenantContextManager()
            tenant_context = await tenant_manager.get_context(tenant_id)

            if not tenant_context:
                await websocket.close(code=1008, reason="Invalid tenant")
                return

            # Connect with tenant-wide scope for AI assistant
            session_id = await collaboration_service.connect_websocket(
                websocket=websocket,
                tenant_context=tenant_context,
                user_id=user_id,
                platform=platform_type,
                scope=CollaborationScope.TENANT_WIDE,
                scope_id="ai_assistant"
            )

            # Send welcome message with available AI capabilities
            await websocket.send_json({
                "type": "ai_assistant_ready",
                "data": {
                    "message": f"AI Assistant ready for {platform} platform",
                    "capabilities": [
                        "Campaign Strategy & Optimization",
                        "Content Generation & SEO",
                        "Social Media Management",
                        "Lead Generation & CRM",
                        "Analytics & Reporting",
                        "Market Research & Competitor Analysis",
                        "Website Audit & Technical SEO",
                        "Email Marketing Automation",
                        "PPC Campaign Management",
                        "Reputation Management"
                    ],
                    "agent_count": "93+ specialized AI agents available",
                    "platform_features": tenant_context.platform_access.get(platform_type, {}).features if tenant_context.platform_access.get(platform_type) else {}
                }
            })

            logger.info(
                "AI Assistant WebSocket session started",
                session_id=session_id,
                platform=platform,
                tenant_id=tenant_id,
                user_id=user_id
            )

            # Message handling loop for AI assistant
            while True:
                try:
                    message = await websocket.receive_json()
                    await collaboration_service.handle_websocket_message(session_id, message)

                except WebSocketDisconnect:
                    logger.info("AI Assistant WebSocket disconnected", session_id=session_id)
                    break

                except Exception as e:
                    logger.error(
                        "Error in AI Assistant WebSocket",
                        session_id=session_id,
                        error=str(e)
                    )
                    await websocket.send_json({
                        "type": "error",
                        "data": {"error": str(e)}
                    })

        except Exception as e:
            logger.error(
                "Error in AI Assistant WebSocket endpoint",
                error=str(e),
                platform=platform,
                tenant_id=tenant_id
            )
            try:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.close(code=1011, reason="Internal server error")
            except:
                pass
        finally:
            if session_id:
                await collaboration_service.disconnect_websocket(session_id)

    @app.get("/api/collaboration/stats/{tenant_id}")
    async def get_collaboration_stats(
        request: Request,
        tenant_id: str,
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Get real-time collaboration statistics for a tenant
        """
        try:
            if tenant_context.tenant_id != tenant_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to tenant collaboration stats"
                )

            collaboration_service = get_collaboration_service()
            stats = await collaboration_service.get_collaboration_stats(tenant_id)

            return JSONResponse(content={
                "success": True,
                "data": stats,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error getting collaboration stats",
                tenant_id=tenant_id,
                error=str(e)
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get collaboration stats"
            )

    @app.get("/api/collaboration/sessions/{tenant_id}")
    async def get_active_sessions(
        request: Request,
        tenant_id: str,
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Get active collaboration sessions for a tenant
        """
        try:
            if tenant_context.tenant_id != tenant_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to tenant sessions"
                )

            collaboration_service = get_collaboration_service()

            # Get tenant sessions
            tenant_sessions = collaboration_service.tenant_sessions.get(tenant_id, set())

            sessions = []
            for session_id in tenant_sessions:
                ai_session = collaboration_service.ai_assistance_sessions.get(session_id)
                if ai_session:
                    sessions.append({
                        "session_id": session_id,
                        "user_id": ai_session.user_id,
                        "platform": ai_session.platform.value,
                        "active_tasks": len(ai_session.active_tasks),
                        "conversation_length": len(ai_session.conversation_history)
                    })

            return JSONResponse(content={
                "success": True,
                "data": {
                    "active_sessions": sessions,
                    "total_count": len(sessions)
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error getting active sessions",
                tenant_id=tenant_id,
                error=str(e)
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get active sessions"
            )

    @app.post("/api/collaboration/broadcast/{tenant_id}")
    async def broadcast_message(
        request: Request,
        tenant_id: str,
        message_data: Dict[str, Any],
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Broadcast message to all active sessions for a tenant
        """
        try:
            if tenant_context.tenant_id != tenant_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to broadcast messages"
                )

            collaboration_service = get_collaboration_service()

            # Get tenant sessions
            tenant_sessions = collaboration_service.tenant_sessions.get(tenant_id, set())

            message = {
                "type": "system_broadcast",
                "data": message_data,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

            # Send to all tenant sessions
            tasks = []
            for session_id in tenant_sessions:
                tasks.append(collaboration_service._send_to_session(session_id, message))

            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                successful = sum(1 for result in results if not isinstance(result, Exception))
            else:
                successful = 0

            return JSONResponse(content={
                "success": True,
                "data": {
                    "message": "Broadcast completed",
                    "target_sessions": len(tenant_sessions),
                    "successful_deliveries": successful
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error broadcasting message",
                tenant_id=tenant_id,
                error=str(e)
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to broadcast message"
            )

    @app.get("/api/collaboration/health")
    async def collaboration_health_check():
        """
        Health check for collaboration service
        """
        try:
            collaboration_service = get_collaboration_service()

            # Get basic stats
            total_connections = len(collaboration_service.active_connections)
            total_sessions = len(collaboration_service.collaboration_sessions)
            total_ai_sessions = len(collaboration_service.ai_assistance_sessions)

            return JSONResponse(content={
                "success": True,
                "data": {
                    "status": "healthy",
                    "active_connections": total_connections,
                    "collaboration_sessions": total_sessions,
                    "ai_assistance_sessions": total_ai_sessions,
                    "uptime": "Service is running"
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        except Exception as e:
            logger.error("Collaboration health check failed", error=str(e))
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "success": False,
                    "error": "Collaboration service unhealthy",
                    "details": str(e)
                }
            )

    logger.info("Real-time collaboration endpoints configured successfully")