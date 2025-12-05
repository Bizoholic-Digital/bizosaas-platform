"""
Enhanced Tenant Integration for BizOSaaS Brain API Gateway
Integrates the enhanced tenant context system with the central FastAPI hub
Now includes unified chat interface for all 5 platform dashboards
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import asyncio
import sys
import os
import json
from uuid import uuid4

# Add shared modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from enhanced_tenant_context import (
    TenantContextManager,
    TenantContextMiddleware,
    EnhancedTenantContext,
    PlatformType,
    AccessLevel,
    get_tenant_context_from_request,
    require_platform_access,
    get_ai_agents_for_context,
    check_ai_quota
)

from rls_manager import RLSManager, create_rls_manager
from rls_middleware import RLSMiddleware

# Import AI coordinator components
from tenant_aware_ai_coordinator import TenantAwareAICoordinator, AgentSpecialization
from ai_coordinator_endpoints import router as ai_coordinator_router, initialize_ai_coordinator

import structlog

logger = structlog.get_logger(__name__)

# Global instances
tenant_context_manager = TenantContextManager()
rls_manager: Optional[RLSManager] = None
ai_coordinator: Optional[TenantAwareAICoordinator] = None

# WebSocket connection manager for real-time chat
class ChatConnectionManager:
    """Manages WebSocket connections for real-time chat across all platforms"""

    def __init__(self):
        # tenant_id -> {platform -> [websockets]}
        self.connections: Dict[str, Dict[str, List[WebSocket]]] = {}
        self.user_sessions: Dict[str, Dict[str, Any]] = {}

    async def connect(self, websocket: WebSocket, tenant_id: str, platform: str, user_id: str = None):
        """Connect a WebSocket for a tenant and platform"""
        await websocket.accept()

        if tenant_id not in self.connections:
            self.connections[tenant_id] = {}
        if platform not in self.connections[tenant_id]:
            self.connections[tenant_id][platform] = []

        self.connections[tenant_id][platform].append(websocket)

        # Store session info
        session_id = str(uuid4())
        self.user_sessions[session_id] = {
            "tenant_id": tenant_id,
            "platform": platform,
            "user_id": user_id,
            "websocket": websocket,
            "connected_at": datetime.utcnow(),
            "last_activity": datetime.utcnow()
        }

        logger.info(
            "WebSocket connected",
            tenant_id=tenant_id,
            platform=platform,
            user_id=user_id,
            session_id=session_id
        )

        return session_id

    async def disconnect(self, websocket: WebSocket, tenant_id: str, platform: str):
        """Disconnect a WebSocket"""
        try:
            if tenant_id in self.connections and platform in self.connections[tenant_id]:
                self.connections[tenant_id][platform].remove(websocket)

                # Clean up empty structures
                if not self.connections[tenant_id][platform]:
                    del self.connections[tenant_id][platform]
                if not self.connections[tenant_id]:
                    del self.connections[tenant_id]

            # Remove from sessions
            session_to_remove = None
            for session_id, session in self.user_sessions.items():
                if session["websocket"] == websocket:
                    session_to_remove = session_id
                    break

            if session_to_remove:
                del self.user_sessions[session_to_remove]

            logger.info(
                "WebSocket disconnected",
                tenant_id=tenant_id,
                platform=platform
            )
        except Exception as e:
            logger.error("Error during WebSocket disconnect", error=str(e))

    async def send_to_tenant_platform(self, tenant_id: str, platform: str, message: Dict[str, Any]):
        """Send message to all connections for a tenant and platform"""
        if tenant_id not in self.connections or platform not in self.connections[tenant_id]:
            return

        dead_connections = []
        for websocket in self.connections[tenant_id][platform]:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.warning(
                    "Failed to send WebSocket message",
                    tenant_id=tenant_id,
                    platform=platform,
                    error=str(e)
                )
                dead_connections.append(websocket)

        # Clean up dead connections
        for dead_ws in dead_connections:
            await self.disconnect(dead_ws, tenant_id, platform)

    async def broadcast_to_tenant(self, tenant_id: str, message: Dict[str, Any]):
        """Broadcast message to all platforms for a tenant"""
        if tenant_id not in self.connections:
            return

        for platform in self.connections[tenant_id]:
            await self.send_to_tenant_platform(tenant_id, platform, message)

# Global chat manager
chat_manager = ChatConnectionManager()

# ========================================================================================
# UNIFIED CHAT WEBSOCKET ENDPOINTS
# ========================================================================================

async def setup_chat_websockets(app: FastAPI):
    """Setup WebSocket endpoints for unified chat interface"""

    @app.websocket("/ws/chat/{platform}/{tenant_id}")
    async def websocket_chat_endpoint(
        websocket: WebSocket,
        platform: str,
        tenant_id: str,
        user_id: Optional[str] = None
    ):
        """
        Unified WebSocket chat endpoint for all platforms
        Provides real-time conversational AI across Bizoholic, CoreLDove, Business Directory, ThrillRing, QuantTrade
        """
        session_id = None
        try:
            # Validate platform
            try:
                platform_enum = PlatformType(platform)
            except ValueError:
                await websocket.close(code=1008, reason="Invalid platform")
                return

            # Get tenant context
            tenant_context = await tenant_context_manager.get_context(tenant_id)
            if not tenant_context:
                await websocket.close(code=1008, reason="Invalid tenant")
                return

            # Check platform access
            platform_access = tenant_context.platform_access.get(platform_enum)
            if not platform_access or not platform_access.enabled:
                await websocket.close(code=1008, reason="Platform access denied")
                return

            # Connect to chat manager
            session_id = await chat_manager.connect(websocket, tenant_id, platform, user_id)

            # Send welcome message
            welcome_msg = {
                "type": "system",
                "message": f"Connected to {platform} AI Assistant",
                "timestamp": datetime.utcnow().isoformat(),
                "session_id": session_id,
                "available_agents": len([
                    agent for agent in ai_coordinator.agents.values()
                    if platform_enum in agent.supported_platforms and agent.can_serve_tenant(tenant_context)
                ]) if ai_coordinator else 0
            }
            await websocket.send_json(welcome_msg)

            # Handle incoming messages
            while True:
                try:
                    # Receive message with timeout
                    message_data = await asyncio.wait_for(
                        websocket.receive_json(),
                        timeout=300.0  # 5 minute timeout
                    )

                    # Process the chat message
                    response = await process_chat_message(
                        message_data, tenant_context, platform_enum, session_id
                    )

                    # Send response
                    await websocket.send_json(response)

                    # Broadcast to other connections if needed
                    if message_data.get("broadcast", False):
                        await chat_manager.send_to_tenant_platform(
                            tenant_id, platform, response
                        )

                except asyncio.TimeoutError:
                    # Send keepalive
                    await websocket.send_json({
                        "type": "keepalive",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                except WebSocketDisconnect:
                    break
                except Exception as e:
                    logger.error(
                        "Error processing chat message",
                        tenant_id=tenant_id,
                        platform=platform,
                        session_id=session_id,
                        error=str(e)
                    )
                    await websocket.send_json({
                        "type": "error",
                        "message": "Failed to process message",
                        "error": str(e),
                        "timestamp": datetime.utcnow().isoformat()
                    })

        except Exception as e:
            logger.error(
                "WebSocket connection error",
                tenant_id=tenant_id,
                platform=platform,
                error=str(e)
            )
        finally:
            if session_id:
                await chat_manager.disconnect(websocket, tenant_id, platform)

async def process_chat_message(
    message_data: Dict[str, Any],
    tenant_context: EnhancedTenantContext,
    platform: PlatformType,
    session_id: str
) -> Dict[str, Any]:
    """Process incoming chat message and generate AI response"""
    try:
        message_type = message_data.get("type", "user_message")
        user_message = message_data.get("message", "")
        conversation_id = message_data.get("conversation_id")
        agent_preference = message_data.get("agent_preference")

        if message_type == "user_message" and user_message:
            # Use AI coordinator to process the message
            if not ai_coordinator:
                return {
                    "type": "error",
                    "message": "AI coordinator not available",
                    "timestamp": datetime.utcnow().isoformat()
                }

            # Find optimal agent for the message
            optimal_agent = await ai_coordinator.find_optimal_agent(
                tenant_context,
                user_message,
                platform,
                agent_preference=agent_preference
            )

            if not optimal_agent:
                return {
                    "type": "agent_response",
                    "message": "I'm sorry, but I couldn't find an appropriate assistant for your request at the moment. Please try again later.",
                    "agent_id": "fallback",
                    "agent_name": "System",
                    "timestamp": datetime.utcnow().isoformat(),
                    "conversation_id": conversation_id or str(uuid4())
                }

            # Execute the conversational task
            task_result = await ai_coordinator.execute_agent_task(
                tenant_context,
                optimal_agent.agent_id,
                f"Conversational assistance: {user_message}",
                {
                    "message": user_message,
                    "conversation_id": conversation_id or str(uuid4()),
                    "session_id": session_id,
                    "message_type": "chat"
                },
                platform
            )

            if task_result["success"]:
                result_data = task_result["result"]
                return {
                    "type": "agent_response",
                    "message": result_data.get("output", "I'm here to help!"),
                    "agent_id": optimal_agent.agent_id,
                    "agent_name": optimal_agent.name,
                    "agent_specialization": optimal_agent.specialization.value,
                    "suggestions": result_data.get("recommendations", []),
                    "actions": await generate_chat_actions(platform, user_message, optimal_agent.specialization),
                    "execution_time": task_result["execution_time"],
                    "quality_score": result_data.get("quality_score", 0.8),
                    "timestamp": datetime.utcnow().isoformat(),
                    "conversation_id": conversation_id or str(uuid4()),
                    "metadata": result_data.get("metadata", {})
                }
            else:
                return {
                    "type": "agent_response",
                    "message": "I encountered an issue processing your request. Please try rephrasing your question.",
                    "agent_id": optimal_agent.agent_id,
                    "agent_name": optimal_agent.name,
                    "error": task_result.get("error"),
                    "timestamp": datetime.utcnow().isoformat(),
                    "conversation_id": conversation_id or str(uuid4())
                }

        elif message_type == "agent_list_request":
            # Return available agents for the platform
            available_agents = [
                {
                    "agent_id": agent.agent_id,
                    "name": agent.name,
                    "specialization": agent.specialization.value,
                    "capabilities": [cap.value for cap in agent.capabilities]
                }
                for agent in ai_coordinator.agents.values()
                if platform in agent.supported_platforms and agent.can_serve_tenant(tenant_context)
            ] if ai_coordinator else []

            return {
                "type": "agent_list",
                "agents": available_agents,
                "total_agents": len(available_agents),
                "platform": platform.value,
                "timestamp": datetime.utcnow().isoformat()
            }

        elif message_type == "platform_info_request":
            # Return platform-specific information
            platform_info = await get_platform_capabilities(platform, tenant_context)
            return {
                "type": "platform_info",
                "platform": platform.value,
                "capabilities": platform_info,
                "timestamp": datetime.utcnow().isoformat()
            }

        else:
            return {
                "type": "error",
                "message": "Unknown message type or empty message",
                "timestamp": datetime.utcnow().isoformat()
            }

    except Exception as e:
        logger.error(
            "Error processing chat message",
            message_data=message_data,
            tenant_id=tenant_context.tenant_id,
            platform=platform.value,
            error=str(e)
        )
        return {
            "type": "error",
            "message": "Failed to process your message",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

async def generate_chat_actions(
    platform: PlatformType,
    user_message: str,
    agent_specialization: AgentSpecialization
) -> List[Dict[str, Any]]:
    """Generate contextual actions for chat interface"""
    actions = []

    # Platform-specific quick actions
    if platform == PlatformType.BIZOHOLIC:
        actions.extend([
            {
                "type": "quick_action",
                "title": "Create Campaign",
                "description": "Start a new marketing campaign",
                "action": "create_campaign",
                "icon": "📈"
            },
            {
                "type": "quick_action",
                "title": "Analyze Performance",
                "description": "Review campaign performance",
                "action": "view_analytics",
                "icon": "📊"
            },
            {
                "type": "quick_action",
                "title": "Lead Management",
                "description": "Manage and score leads",
                "action": "manage_leads",
                "icon": "👥"
            }
        ])
    elif platform == PlatformType.CORELDOVE:
        actions.extend([
            {
                "type": "quick_action",
                "title": "Add Product",
                "description": "Add new product to store",
                "action": "add_product",
                "icon": "🛍️"
            },
            {
                "type": "quick_action",
                "title": "View Orders",
                "description": "Check recent orders",
                "action": "view_orders",
                "icon": "📦"
            },
            {
                "type": "quick_action",
                "title": "Inventory Check",
                "description": "Review inventory levels",
                "action": "check_inventory",
                "icon": "📋"
            }
        ])
    elif platform == PlatformType.BUSINESS_DIRECTORY:
        actions.extend([
            {
                "type": "quick_action",
                "title": "Add Business",
                "description": "Add new business listing",
                "action": "add_business",
                "icon": "🏢"
            },
            {
                "type": "quick_action",
                "title": "Moderate Reviews",
                "description": "Review and moderate listings",
                "action": "moderate_reviews",
                "icon": "⭐"
            }
        ])
    elif platform == PlatformType.THRILLRING:
        actions.extend([
            {
                "type": "quick_action",
                "title": "Browse Games",
                "description": "Explore game library",
                "action": "browse_games",
                "icon": "🎮"
            },
            {
                "type": "quick_action",
                "title": "Create Tournament",
                "description": "Set up new tournament",
                "action": "create_tournament",
                "icon": "🏆"
            }
        ])
    elif platform == PlatformType.QUANTTRADE:
        actions.extend([
            {
                "type": "quick_action",
                "title": "Portfolio Overview",
                "description": "View portfolio performance",
                "action": "view_portfolio",
                "icon": "💼"
            },
            {
                "type": "quick_action",
                "title": "Market Analysis",
                "description": "Get market insights",
                "action": "market_analysis",
                "icon": "📈"
            }
        ])

    # Agent specialization specific actions
    if agent_specialization == AgentSpecialization.CONTENT_CREATOR:
        actions.append({
            "type": "specialized_action",
            "title": "Generate Content",
            "description": "Create blog posts, social media content",
            "action": "generate_content",
            "icon": "✍️"
        })
    elif agent_specialization == AgentSpecialization.DATA_ANALYST:
        actions.append({
            "type": "specialized_action",
            "title": "Data Analysis",
            "description": "Analyze data and generate insights",
            "action": "analyze_data",
            "icon": "📊"
        })

    return actions

async def get_platform_capabilities(
    platform: PlatformType,
    tenant_context: EnhancedTenantContext
) -> Dict[str, Any]:
    """Get platform-specific capabilities and features"""
    base_capabilities = {
        "ai_agents_available": len([
            agent for agent in ai_coordinator.agents.values()
            if platform in agent.supported_platforms and agent.can_serve_tenant(tenant_context)
        ]) if ai_coordinator else 0,
        "subscription_tier": tenant_context.subscription_tier.value,
        "platform_enabled": tenant_context.platform_access.get(platform, {}).get("enabled", False)
    }

    platform_specific = {
        PlatformType.BIZOHOLIC: {
            "features": ["Campaign Management", "Lead Scoring", "SEO Optimization", "Content Creation"],
            "integrations": ["Google Ads", "Facebook Ads", "Email Marketing", "CRM"]
        },
        PlatformType.CORELDOVE: {
            "features": ["Product Management", "Order Processing", "Inventory Tracking", "Pricing Optimization"],
            "integrations": ["Amazon API", "Saleor", "Payment Gateways", "Shipping APIs"]
        },
        PlatformType.BUSINESS_DIRECTORY: {
            "features": ["Business Listings", "Review Management", "Local SEO", "Category Management"],
            "integrations": ["Google Maps", "Yelp", "Local APIs", "Verification Services"]
        },
        PlatformType.THRILLRING: {
            "features": ["Game Database", "Tournament Management", "Player Matching", "Gaming Analytics"],
            "integrations": ["IGDB", "Steam API", "Gaming Platforms", "Tournament Systems"]
        },
        PlatformType.QUANTTRADE: {
            "features": ["Portfolio Management", "Trading Algorithms", "Risk Analysis", "Market Data"],
            "integrations": ["Market Data APIs", "Broker APIs", "Financial Data", "Trading Platforms"]
        }
    }

    return {**base_capabilities, **platform_specific.get(platform, {})}

# ========================================================================================
# TENANT CONTEXT API ENDPOINTS
# ========================================================================================

async def setup_tenant_routes(app: FastAPI):
    """Setup tenant context routes in the Brain API Gateway"""

    @app.get("/api/brain/tenant/context")
    async def get_current_tenant_context(request: Request):
        """Get current tenant context"""
        try:
            context = await get_tenant_context_from_request(request)
            if not context:
                raise HTTPException(status_code=401, detail="No tenant context found")

            return {
                "tenant_id": context.tenant_id,
                "organization_name": context.organization_name,
                "subscription_tier": context.subscription_tier.value,
                "primary_platform": context.primary_platform.value,
                "platform_access": {
                    platform.value: {
                        "access_level": access.access_level.value,
                        "features_enabled": access.features_enabled,
                        "last_accessed": access.last_accessed.isoformat() if access.last_accessed else None
                    }
                    for platform, access in context.platform_access.items()
                },
                "ai_capabilities": [cap.value for cap in context.ai_context.capabilities],
                "ai_quota": context.ai_agent_quota,
                "ai_usage": context.ai_usage_current,
                "last_active": context.last_active.isoformat()
            }

        except Exception as e:
            logger.error("Error getting tenant context", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/brain/tenant/platforms")
    async def get_platform_access(request: Request):
        """Get platform access information for current tenant"""
        try:
            context = await get_tenant_context_from_request(request)
            if not context:
                raise HTTPException(status_code=401, detail="No tenant context found")

            platform_info = {}
            for platform, access in context.platform_access.items():
                platform_info[platform.value] = {
                    "access_level": access.access_level.value,
                    "features_enabled": access.features_enabled,
                    "rate_limits": access.rate_limits,
                    "platform_url": tenant_context_manager.platform_routing.get(platform),
                    "last_accessed": access.last_accessed.isoformat() if access.last_accessed else None,
                    "custom_config": access.custom_config
                }

            return {
                "platforms": platform_info,
                "primary_platform": context.primary_platform.value,
                "subscription_tier": context.subscription_tier.value
            }

        except Exception as e:
            logger.error("Error getting platform access", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/brain/tenant/ai-agents")
    async def get_available_ai_agents(request: Request):
        """Get available AI agents for current tenant"""
        try:
            context = await get_tenant_context_from_request(request)
            if not context:
                raise HTTPException(status_code=401, detail="No tenant context found")

            # Get agents for current platform
            available_agents = get_ai_agents_for_context(context)

            # Get agents for all platforms tenant has access to
            all_agents = {}
            for platform, access in context.platform_access.items():
                if access.access_level != AccessLevel.NONE:
                    platform_agents = await tenant_context_manager._get_platform_ai_agents(platform)
                    all_agents[platform.value] = platform_agents

            return {
                "current_platform_agents": available_agents,
                "all_platform_agents": all_agents,
                "ai_capabilities": [cap.value for cap in context.ai_context.capabilities],
                "quota": context.ai_agent_quota,
                "current_usage": context.ai_usage_current,
                "privacy_settings": context.ai_context.privacy_settings
            }

        except Exception as e:
            logger.error("Error getting AI agents", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/brain/tenant/ai-chat")
    async def ai_chat_with_context(
        request: Request,
        chat_request: Dict[str, Any],
        background_tasks: BackgroundTasks
    ):
        """AI chat with tenant context and agent coordination"""
        try:
            context = await get_tenant_context_from_request(request)
            if not context:
                raise HTTPException(status_code=401, detail="No tenant context found")

            message = chat_request.get("message", "")
            platform = chat_request.get("platform", context.primary_platform.value)
            agent_preference = chat_request.get("agent", "auto")

            # Check AI quota
            if not check_ai_quota(context, 1):
                raise HTTPException(
                    status_code=429,
                    detail="AI quota exceeded. Please upgrade your subscription."
                )

            # Get appropriate agent for platform and message
            selected_agent = await _select_optimal_agent(
                context, platform, message, agent_preference
            )

            # Prepare agent context
            agent_context = {
                "tenant_id": context.tenant_id,
                "platform": platform,
                "subscription_tier": context.subscription_tier.value,
                "user_capabilities": [cap.value for cap in context.ai_context.capabilities],
                "platform_access": {
                    p.value: a.access_level.value
                    for p, a in context.platform_access.items()
                },
                "conversation_context": chat_request.get("conversation_history", [])
            }

            # Send to AI agent (mock implementation)
            response = await _process_ai_chat(
                selected_agent, message, agent_context
            )

            # Update usage metrics in background
            background_tasks.add_task(
                tenant_context_manager.update_usage_metrics,
                context.tenant_id,
                PlatformType(platform),
                {"ai_requests": 1, "messages": 1}
            )

            return {
                "response": response,
                "agent_used": selected_agent,
                "platform": platform,
                "quota_remaining": context.ai_agent_quota.get("daily_requests", 0) - context.ai_usage_current.get("daily_requests", 0),
                "timestamp": datetime.utcnow().isoformat()
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in AI chat", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/brain/tenant/propagate-context")
    async def propagate_context_to_agents(
        request: Request,
        propagation_request: Dict[str, Any]
    ):
        """Propagate tenant context to specified AI agents"""
        try:
            context = await get_tenant_context_from_request(request)
            if not context:
                raise HTTPException(status_code=401, detail="No tenant context found")

            agent_ids = propagation_request.get("agent_ids", [])
            if not agent_ids:
                # Get all available agents
                agent_ids = get_ai_agents_for_context(context)

            # Propagate context
            results = await tenant_context_manager.propagate_context_to_ai_agents(
                context, agent_ids
            )

            successful_propagations = sum(1 for success in results.values() if success)

            return {
                "total_agents": len(agent_ids),
                "successful_propagations": successful_propagations,
                "results": results,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error("Error propagating context", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/brain/tenant/update-preferences")
    async def update_tenant_preferences(
        request: Request,
        preferences: Dict[str, Any]
    ):
        """Update tenant AI and platform preferences"""
        try:
            context = await get_tenant_context_from_request(request)
            if not context:
                raise HTTPException(status_code=401, detail="No tenant context found")

            # Update AI preferences
            if "ai_preferences" in preferences:
                ai_prefs = preferences["ai_preferences"]

                if "custom_prompts" in ai_prefs:
                    context.ai_context.custom_prompts.update(ai_prefs["custom_prompts"])

                if "learning_preferences" in ai_prefs:
                    context.ai_context.learning_preferences.update(ai_prefs["learning_preferences"])

                if "privacy_settings" in ai_prefs:
                    context.ai_context.privacy_settings.update(ai_prefs["privacy_settings"])

            # Update platform preferences
            if "platform_preferences" in preferences:
                platform_prefs = preferences["platform_preferences"]

                if "primary_platform" in platform_prefs:
                    try:
                        context.primary_platform = PlatformType(platform_prefs["primary_platform"])
                    except ValueError:
                        pass

            context.updated_at = datetime.utcnow()

            return {
                "status": "success",
                "message": "Preferences updated successfully",
                "updated_at": context.updated_at.isoformat()
            }

        except Exception as e:
            logger.error("Error updating preferences", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/brain/tenant/analytics")
    async def get_tenant_analytics(request: Request):
        """Get tenant usage analytics across platforms"""
        try:
            context = await get_tenant_context_from_request(request)
            if not context:
                raise HTTPException(status_code=401, detail="No tenant context found")

            return {
                "tenant_id": context.tenant_id,
                "subscription_tier": context.subscription_tier.value,
                "usage_analytics": context.usage_analytics,
                "performance_metrics": context.performance_metrics,
                "ai_usage": {
                    "quota": context.ai_agent_quota,
                    "current_usage": context.ai_usage_current,
                    "usage_percentage": {
                        metric: (context.ai_usage_current.get(metric, 0) / context.ai_agent_quota.get(metric, 1)) * 100
                        for metric in context.ai_agent_quota.keys()
                    }
                },
                "platform_activity": {
                    platform.value: {
                        "last_accessed": access.last_accessed.isoformat() if access.last_accessed else None,
                        "access_level": access.access_level.value
                    }
                    for platform, access in context.platform_access.items()
                },
                "created_at": context.created_at.isoformat(),
                "last_active": context.last_active.isoformat()
            }

        except Exception as e:
            logger.error("Error getting analytics", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))

# ========================================================================================
# AI AGENT COORDINATION FUNCTIONS
# ========================================================================================

async def _select_optimal_agent(
    context: EnhancedTenantContext,
    platform: str,
    message: str,
    agent_preference: str = "auto"
) -> str:
    """Select optimal AI agent based on context, platform, and message content"""

    try:
        platform_type = PlatformType(platform)
    except ValueError:
        platform_type = context.primary_platform

    # Get available agents for platform
    available_agents = await tenant_context_manager._get_platform_ai_agents(platform_type)

    if agent_preference != "auto" and agent_preference in available_agents:
        return agent_preference

    # Simple agent selection based on message keywords
    message_lower = message.lower()

    agent_keywords = {
        "marketing_strategist": ["campaign", "marketing", "strategy", "promotion", "advertising"],
        "content_creator": ["content", "blog", "article", "write", "create"],
        "seo_optimizer": ["seo", "search", "ranking", "optimization", "keywords"],
        "product_recommender": ["product", "recommend", "suggest", "buy", "purchase"],
        "inventory_optimizer": ["inventory", "stock", "supply", "warehouse"],
        "market_analyst": ["market", "analysis", "trend", "forecast", "data"],
        "risk_manager": ["risk", "security", "compliance", "safety"],
        "game_recommender": ["game", "play", "recommend", "gaming"],
        "tournament_organizer": ["tournament", "competition", "event", "organize"],
        "local_seo_specialist": ["local", "business", "directory", "location"],
        "unified_assistant": ["help", "assist", "general", "support"]
    }

    # Score agents based on keyword matches
    agent_scores = {}
    for agent in available_agents:
        score = 0
        keywords = agent_keywords.get(agent, [])
        for keyword in keywords:
            if keyword in message_lower:
                score += 1
        agent_scores[agent] = score

    # Return agent with highest score, or first available agent
    if agent_scores:
        best_agent = max(agent_scores.items(), key=lambda x: x[1])
        if best_agent[1] > 0:
            return best_agent[0]

    return available_agents[0] if available_agents else "unified_assistant"

async def _process_ai_chat(
    agent_id: str,
    message: str,
    agent_context: Dict[str, Any]
) -> str:
    """Process AI chat message with selected agent"""

    try:
        # Mock AI response - in production, call actual AI agent
        platform = agent_context.get("platform", "client_portal")
        tenant_id = agent_context.get("tenant_id", "unknown")

        # Simulate processing delay
        await asyncio.sleep(0.5)

        # Generate contextual response based on agent and platform
        response_templates = {
            "marketing_strategist": f"As your marketing strategist for {platform}, I can help you develop targeted campaigns. Based on your message about '{message[:50]}...', I recommend focusing on your target audience analysis.",

            "content_creator": f"I can help create engaging content for your {platform} presence. For your request about '{message[:50]}...', let me suggest some content ideas that would resonate with your audience.",

            "seo_optimizer": f"For SEO optimization on {platform}, regarding '{message[:50]}...', I recommend focusing on keyword research and content optimization strategies.",

            "product_recommender": f"Based on your {platform} data and the query '{message[:50]}...', I can suggest products that would be perfect for your customers.",

            "market_analyst": f"Looking at the market data for your {platform} business and your question about '{message[:50]}...', here's my analysis of current trends.",

            "game_recommender": f"For gaming recommendations on {platform}, regarding '{message[:50]}...', I can suggest games that match your preferences and community interests.",

            "local_seo_specialist": f"For local business optimization on {platform}, about '{message[:50]}...', let me help you improve your local search presence.",

            "unified_assistant": f"I'm here to help with any questions about your {platform} experience. Regarding '{message[:50]}...', let me provide comprehensive assistance."
        }

        response = response_templates.get(
            agent_id,
            f"Hello! I'm your AI assistant for {platform}. I understand you're asking about '{message[:50]}...'. How can I help you with this?"
        )

        return response

    except Exception as e:
        logger.error(f"Error processing AI chat with agent {agent_id}", error=str(e))
        return "I apologize, but I'm having trouble processing your request right now. Please try again later."

# ========================================================================================
# MIDDLEWARE SETUP
# ========================================================================================

def setup_tenant_middleware(app: FastAPI):
    """Setup tenant context middleware for the Brain API Gateway"""

    # Add tenant context middleware
    middleware = TenantContextMiddleware(app, tenant_context_manager)

    # Note: In FastAPI, we need to add this as a custom middleware
    # This is a simplified version - in production, use proper FastAPI middleware pattern

    @app.middleware("http")
    async def tenant_context_middleware(request: Request, call_next):
        """Tenant context middleware implementation"""

        # Extract tenant information
        tenant_id = request.headers.get("x-tenant-id")
        platform_header = request.headers.get("x-platform")

        # Try to get from authorization header if not in custom headers
        if not tenant_id:
            auth_header = request.headers.get("authorization")
            if auth_header:
                # Mock JWT extraction - in production, properly decode JWT
                tenant_id = "demo_tenant"

        # Determine platform from host or header
        platform = None
        if platform_header:
            try:
                platform = PlatformType(platform_header)
            except ValueError:
                pass

        if not platform:
            host = request.headers.get("host", "")
            if ":3008" in host:
                platform = PlatformType.BIZOHOLIC
            elif ":3007" in host:
                platform = PlatformType.CORELDOVE
            elif ":3004" in host:
                platform = PlatformType.BUSINESS_DIRECTORY
            elif ":3005" in host:
                platform = PlatformType.THRILLRING
            elif ":3012" in host:
                platform = PlatformType.QUANTTRADE
            elif ":3006" in host:
                platform = PlatformType.CLIENT_PORTAL
            elif ":3009" in host:
                platform = PlatformType.ADMIN_DASHBOARD
            else:
                platform = PlatformType.CLIENT_PORTAL

        # Get tenant context if we have tenant_id and platform
        if tenant_id and platform:
            try:
                context = await tenant_context_manager.get_tenant_context(tenant_id, platform)
                if context:
                    # Store in request state
                    request.scope["tenant_context"] = context

                    # Update usage metrics
                    await tenant_context_manager.update_usage_metrics(
                        tenant_id, platform, {"requests": 1}
                    )
            except Exception as e:
                logger.error("Error getting tenant context in middleware", error=str(e))

        response = await call_next(request)
        return response

# ========================================================================================
# INITIALIZATION
# ========================================================================================

async def initialize_tenant_system(app: FastAPI):
    """Initialize the enhanced tenant system in the Brain API Gateway"""

    logger.info("Initializing enhanced tenant context system")

    # Setup middleware
    setup_tenant_middleware(app)

    # Setup routes
    await setup_tenant_routes(app)

    # Initialize tenant context manager
    # In production, this would load configuration from database
    logger.info("Tenant context system initialized successfully")

async def get_tenant_context_for_request(request: Request) -> Optional[EnhancedTenantContext]:
    """Utility function to get tenant context from request"""
    return getattr(request.scope, "tenant_context", None)