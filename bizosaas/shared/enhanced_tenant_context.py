"""
Enhanced Tenant Context Propagation System
Advanced multi-tenant architecture with AI-aware routing across all BizOSaaS platforms
"""

from typing import Dict, List, Optional, Any, Union, Callable, Tuple
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
import asyncio
import logging
import hashlib
import time
import json
import jwt
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# ========================================================================================
# ENHANCED TENANT CONTEXT MODELS
# ========================================================================================

class PlatformType(str, Enum):
    """Supported platforms in the BizOSaaS ecosystem"""
    BIZOHOLIC = "bizoholic"           # Marketing Agency (Port 3008)
    CORELDOVE = "coreldove"           # E-commerce (Port 3007)
    BUSINESS_DIRECTORY = "business_directory"  # Directory (Port 3004)
    THRILLRING = "thrillring"         # Gaming (Port 3005)
    QUANTTRADE = "quanttrade"         # Trading (Port 3012)
    CLIENT_PORTAL = "client_portal"   # Unified Portal (Port 3006)
    ADMIN_DASHBOARD = "admin_dashboard"  # Admin (Port 3009)

class TenantTier(str, Enum):
    """Enhanced subscription tiers with platform-specific features"""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    WHITE_LABEL = "white_label"

class AccessLevel(str, Enum):
    """Granular access control levels"""
    NONE = "none"
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    OWNER = "owner"
    SUPER_ADMIN = "super_admin"

class AIAgentCapability(str, Enum):
    """AI agent capabilities per tenant"""
    BASIC_CHAT = "basic_chat"
    ADVANCED_ANALYTICS = "advanced_analytics"
    AUTOMATION = "automation"
    CROSS_PLATFORM = "cross_platform"
    CUSTOM_TRAINING = "custom_training"
    WHITE_LABEL_AI = "white_label_ai"

@dataclass
class PlatformAccess:
    """Platform-specific access configuration"""
    platform: PlatformType
    access_level: AccessLevel
    features_enabled: List[str] = field(default_factory=list)
    rate_limits: Dict[str, int] = field(default_factory=dict)
    custom_config: Dict[str, Any] = field(default_factory=dict)
    last_accessed: Optional[datetime] = None

@dataclass
class AIAgentContext:
    """AI agent context for tenant-specific intelligence"""
    agent_ids: List[str] = field(default_factory=list)
    capabilities: List[AIAgentCapability] = field(default_factory=list)
    custom_prompts: Dict[str, str] = field(default_factory=dict)
    learning_preferences: Dict[str, Any] = field(default_factory=dict)
    privacy_settings: Dict[str, bool] = field(default_factory=dict)
    cross_client_learning: bool = False

class EnhancedTenantContext(BaseModel):
    """Enhanced tenant context with comprehensive platform and AI integration"""

    # Core Identity
    tenant_uuid: UUID = Field(default_factory=uuid4)
    tenant_id: str = Field(..., description="Human-readable tenant identifier")
    organization_name: str = Field(..., description="Organization display name")

    # Enhanced Subscription Management
    subscription_tier: TenantTier = TenantTier.FREE
    subscription_status: str = "active"
    subscription_start: datetime = Field(default_factory=datetime.utcnow)
    subscription_end: Optional[datetime] = None
    trial_end: Optional[datetime] = None

    # Platform Access Control
    platform_access: Dict[PlatformType, PlatformAccess] = Field(default_factory=dict)
    primary_platform: PlatformType = PlatformType.CLIENT_PORTAL

    # AI Agent Integration
    ai_context: AIAgentContext = Field(default_factory=AIAgentContext)
    ai_agent_quota: Dict[str, int] = Field(default_factory=dict)
    ai_usage_current: Dict[str, int] = Field(default_factory=dict)

    # Security & Privacy
    data_residency_region: str = "us-east-1"
    privacy_level: str = "standard"
    audit_logging_enabled: bool = True

    # Cross-Platform Data
    unified_user_id: str = Field(..., description="Unified user ID across platforms")
    platform_user_mappings: Dict[PlatformType, str] = Field(default_factory=dict)

    # Performance & Analytics
    usage_analytics: Dict[str, Any] = Field(default_factory=dict)
    performance_metrics: Dict[str, float] = Field(default_factory=dict)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }

# ========================================================================================
# TENANT CONTEXT MANAGER
# ========================================================================================

class TenantContextManager:
    """Manages tenant context across all platforms with AI integration"""

    def __init__(self):
        self.context_cache: Dict[str, EnhancedTenantContext] = {}
        self.context_ttl: Dict[str, datetime] = {}
        self.ai_agent_mappings: Dict[str, List[str]] = {}
        self.platform_routing: Dict[PlatformType, str] = {
            PlatformType.BIZOHOLIC: "http://localhost:3008",
            PlatformType.CORELDOVE: "http://localhost:3007",
            PlatformType.BUSINESS_DIRECTORY: "http://localhost:3004",
            PlatformType.THRILLRING: "http://localhost:3005",
            PlatformType.QUANTTRADE: "http://localhost:3012",
            PlatformType.CLIENT_PORTAL: "http://localhost:3006",
            PlatformType.ADMIN_DASHBOARD: "http://localhost:3009"
        }

    async def get_tenant_context(
        self,
        tenant_id: str,
        platform: PlatformType,
        force_refresh: bool = False
    ) -> Optional[EnhancedTenantContext]:
        """Get enhanced tenant context with platform-specific configuration"""

        cache_key = f"{tenant_id}:{platform.value}"

        # Check cache first
        if not force_refresh and cache_key in self.context_cache:
            cached_time = self.context_ttl.get(cache_key)
            if cached_time and datetime.utcnow() < cached_time:
                context = self.context_cache[cache_key]
                context.last_active = datetime.utcnow()
                return context

        # Fetch fresh context
        context = await self._fetch_tenant_context(tenant_id, platform)
        if context:
            # Cache for 30 minutes
            self.context_cache[cache_key] = context
            self.context_ttl[cache_key] = datetime.utcnow() + timedelta(minutes=30)

        return context

    async def _fetch_tenant_context(
        self,
        tenant_id: str,
        platform: PlatformType
    ) -> Optional[EnhancedTenantContext]:
        """Fetch tenant context from database with platform-specific enhancements"""

        try:
            # Mock implementation - in production, fetch from database
            context = EnhancedTenantContext(
                tenant_id=tenant_id,
                organization_name=f"Organization {tenant_id}",
                subscription_tier=TenantTier.PROFESSIONAL,
                primary_platform=platform,
                unified_user_id=f"user_{tenant_id}"
            )

            # Configure platform-specific access
            await self._configure_platform_access(context, platform)

            # Configure AI agent capabilities
            await self._configure_ai_capabilities(context, platform)

            return context

        except Exception as e:
            logger.error(f"Error fetching tenant context: {e}")
            return None

    async def _configure_platform_access(
        self,
        context: EnhancedTenantContext,
        platform: PlatformType
    ):
        """Configure platform-specific access based on subscription tier"""

        tier = context.subscription_tier

        # Define platform access based on subscription tier
        platform_configs = {
            PlatformType.BIZOHOLIC: {
                TenantTier.FREE: AccessLevel.READ,
                TenantTier.STARTER: AccessLevel.WRITE,
                TenantTier.PROFESSIONAL: AccessLevel.ADMIN,
                TenantTier.ENTERPRISE: AccessLevel.OWNER
            },
            PlatformType.CORELDOVE: {
                TenantTier.FREE: AccessLevel.NONE,
                TenantTier.STARTER: AccessLevel.READ,
                TenantTier.PROFESSIONAL: AccessLevel.WRITE,
                TenantTier.ENTERPRISE: AccessLevel.ADMIN
            },
            PlatformType.BUSINESS_DIRECTORY: {
                TenantTier.FREE: AccessLevel.READ,
                TenantTier.STARTER: AccessLevel.WRITE,
                TenantTier.PROFESSIONAL: AccessLevel.ADMIN,
                TenantTier.ENTERPRISE: AccessLevel.OWNER
            },
            PlatformType.THRILLRING: {
                TenantTier.FREE: AccessLevel.READ,
                TenantTier.STARTER: AccessLevel.READ,
                TenantTier.PROFESSIONAL: AccessLevel.WRITE,
                TenantTier.ENTERPRISE: AccessLevel.ADMIN
            },
            PlatformType.QUANTTRADE: {
                TenantTier.FREE: AccessLevel.NONE,
                TenantTier.STARTER: AccessLevel.NONE,
                TenantTier.PROFESSIONAL: AccessLevel.READ,
                TenantTier.ENTERPRISE: AccessLevel.WRITE
            }
        }

        # Configure access for all platforms
        for platform_type, tier_access in platform_configs.items():
            access_level = tier_access.get(tier, AccessLevel.NONE)

            platform_access = PlatformAccess(
                platform=platform_type,
                access_level=access_level,
                features_enabled=self._get_platform_features(tier, platform_type),
                rate_limits=self._get_rate_limits(tier, platform_type),
                last_accessed=datetime.utcnow() if platform_type == platform else None
            )

            context.platform_access[platform_type] = platform_access

    def _get_platform_features(self, tier: TenantTier, platform: PlatformType) -> List[str]:
        """Get enabled features for platform and tier combination"""

        feature_matrix = {
            PlatformType.BIZOHOLIC: {
                TenantTier.FREE: ["basic_contact_forms", "blog_reading"],
                TenantTier.STARTER: ["contact_forms", "blog_management", "basic_analytics"],
                TenantTier.PROFESSIONAL: ["advanced_forms", "custom_content", "advanced_analytics", "ai_assistance"],
                TenantTier.ENTERPRISE: ["white_label", "custom_domains", "priority_support", "advanced_ai"]
            },
            PlatformType.CORELDOVE: {
                TenantTier.FREE: [],
                TenantTier.STARTER: ["basic_store", "product_catalog"],
                TenantTier.PROFESSIONAL: ["advanced_store", "inventory_management", "payment_processing"],
                TenantTier.ENTERPRISE: ["multi_store", "advanced_analytics", "ai_recommendations"]
            },
            PlatformType.BUSINESS_DIRECTORY: {
                TenantTier.FREE: ["basic_listing", "search"],
                TenantTier.STARTER: ["enhanced_listing", "basic_analytics"],
                TenantTier.PROFESSIONAL: ["premium_listing", "seo_tools", "lead_generation"],
                TenantTier.ENTERPRISE: ["white_label_directory", "api_access", "custom_integrations"]
            },
            PlatformType.THRILLRING: {
                TenantTier.FREE: ["game_browsing", "basic_profiles"],
                TenantTier.STARTER: ["game_reviews", "basic_tournaments"],
                TenantTier.PROFESSIONAL: ["tournament_management", "streaming_integration"],
                TenantTier.ENTERPRISE: ["custom_tournaments", "api_access", "white_label"]
            },
            PlatformType.QUANTTRADE: {
                TenantTier.FREE: [],
                TenantTier.STARTER: [],
                TenantTier.PROFESSIONAL: ["basic_trading", "market_data", "simple_strategies"],
                TenantTier.ENTERPRISE: ["advanced_trading", "ai_strategies", "real_time_data", "custom_indicators"]
            }
        }

        return feature_matrix.get(platform, {}).get(tier, [])

    def _get_rate_limits(self, tier: TenantTier, platform: PlatformType) -> Dict[str, int]:
        """Get rate limits for platform and tier combination"""

        base_limits = {
            TenantTier.FREE: {"requests_per_minute": 10, "ai_requests_per_hour": 5},
            TenantTier.STARTER: {"requests_per_minute": 60, "ai_requests_per_hour": 50},
            TenantTier.PROFESSIONAL: {"requests_per_minute": 300, "ai_requests_per_hour": 500},
            TenantTier.ENTERPRISE: {"requests_per_minute": 1000, "ai_requests_per_hour": 2000}
        }

        return base_limits.get(tier, base_limits[TenantTier.FREE])

    async def _configure_ai_capabilities(
        self,
        context: EnhancedTenantContext,
        platform: PlatformType
    ):
        """Configure AI agent capabilities based on subscription and platform"""

        tier = context.subscription_tier

        # Base AI capabilities by tier
        tier_capabilities = {
            TenantTier.FREE: [AIAgentCapability.BASIC_CHAT],
            TenantTier.STARTER: [AIAgentCapability.BASIC_CHAT, AIAgentCapability.ADVANCED_ANALYTICS],
            TenantTier.PROFESSIONAL: [
                AIAgentCapability.BASIC_CHAT,
                AIAgentCapability.ADVANCED_ANALYTICS,
                AIAgentCapability.AUTOMATION,
                AIAgentCapability.CROSS_PLATFORM
            ],
            TenantTier.ENTERPRISE: [
                AIAgentCapability.BASIC_CHAT,
                AIAgentCapability.ADVANCED_ANALYTICS,
                AIAgentCapability.AUTOMATION,
                AIAgentCapability.CROSS_PLATFORM,
                AIAgentCapability.CUSTOM_TRAINING,
                AIAgentCapability.WHITE_LABEL_AI
            ]
        }

        # Get available AI agents for platform
        platform_agents = await self._get_platform_ai_agents(platform)

        context.ai_context = AIAgentContext(
            agent_ids=platform_agents,
            capabilities=tier_capabilities.get(tier, [AIAgentCapability.BASIC_CHAT]),
            privacy_settings={
                "data_sharing": tier in [TenantTier.PROFESSIONAL, TenantTier.ENTERPRISE],
                "cross_client_learning": tier == TenantTier.ENTERPRISE,
                "custom_training": tier == TenantTier.ENTERPRISE
            }
        )

        # Set AI quotas based on tier
        quota_limits = {
            TenantTier.FREE: {"daily_requests": 100, "monthly_ai_hours": 5},
            TenantTier.STARTER: {"daily_requests": 1000, "monthly_ai_hours": 50},
            TenantTier.PROFESSIONAL: {"daily_requests": 5000, "monthly_ai_hours": 200},
            TenantTier.ENTERPRISE: {"daily_requests": 20000, "monthly_ai_hours": 1000}
        }

        context.ai_agent_quota = quota_limits.get(tier, quota_limits[TenantTier.FREE])

    async def _get_platform_ai_agents(self, platform: PlatformType) -> List[str]:
        """Get AI agents available for specific platform"""

        platform_agent_mapping = {
            PlatformType.BIZOHOLIC: [
                "marketing_strategist", "content_creator", "seo_optimizer",
                "lead_scorer", "campaign_manager", "social_media_manager"
            ],
            PlatformType.CORELDOVE: [
                "product_recommender", "inventory_optimizer", "price_analyst",
                "customer_segmenter", "sales_forecaster", "logistics_optimizer"
            ],
            PlatformType.BUSINESS_DIRECTORY: [
                "local_seo_specialist", "business_analyzer", "competitor_researcher",
                "review_manager", "location_optimizer", "citation_builder"
            ],
            PlatformType.THRILLRING: [
                "game_recommender", "tournament_organizer", "community_manager",
                "performance_analyst", "streaming_optimizer", "esports_scout"
            ],
            PlatformType.QUANTTRADE: [
                "market_analyst", "risk_manager", "strategy_optimizer",
                "sentiment_analyzer", "portfolio_manager", "trading_advisor"
            ],
            PlatformType.CLIENT_PORTAL: [
                "unified_assistant", "task_coordinator", "analytics_reporter",
                "workflow_optimizer", "cross_platform_sync", "performance_monitor"
            ],
            PlatformType.ADMIN_DASHBOARD: [
                "system_monitor", "security_analyst", "performance_optimizer",
                "user_behavior_analyst", "cost_optimizer", "compliance_monitor"
            ]
        }

        return platform_agent_mapping.get(platform, ["basic_assistant"])

    async def propagate_context_to_ai_agents(
        self,
        context: EnhancedTenantContext,
        agent_ids: List[str]
    ) -> Dict[str, bool]:
        """Propagate tenant context to AI agents for personalized responses"""

        results = {}

        for agent_id in agent_ids:
            try:
                # Prepare agent context
                agent_context = {
                    "tenant_id": context.tenant_id,
                    "platform": context.primary_platform.value,
                    "subscription_tier": context.subscription_tier.value,
                    "capabilities": [cap.value for cap in context.ai_context.capabilities],
                    "privacy_settings": context.ai_context.privacy_settings,
                    "custom_prompts": context.ai_context.custom_prompts,
                    "platform_access": {
                        platform.value: {
                            "access_level": access.access_level.value,
                            "features": access.features_enabled
                        }
                        for platform, access in context.platform_access.items()
                    }
                }

                # Send context to AI agent (mock implementation)
                success = await self._send_context_to_agent(agent_id, agent_context)
                results[agent_id] = success

            except Exception as e:
                logger.error(f"Failed to propagate context to agent {agent_id}: {e}")
                results[agent_id] = False

        return results

    async def _send_context_to_agent(self, agent_id: str, context: Dict[str, Any]) -> bool:
        """Send context to specific AI agent"""

        try:
            # Mock implementation - in production, use message queue or direct API call
            logger.info(f"Propagating context to agent {agent_id}")

            # Simulate network delay
            await asyncio.sleep(0.1)

            return True

        except Exception as e:
            logger.error(f"Error sending context to agent {agent_id}: {e}")
            return False

    async def validate_platform_access(
        self,
        context: EnhancedTenantContext,
        platform: PlatformType,
        required_level: AccessLevel
    ) -> bool:
        """Validate if tenant has required access level for platform"""

        platform_access = context.platform_access.get(platform)
        if not platform_access:
            return False

        # Define access level hierarchy
        level_hierarchy = {
            AccessLevel.NONE: 0,
            AccessLevel.READ: 1,
            AccessLevel.WRITE: 2,
            AccessLevel.ADMIN: 3,
            AccessLevel.OWNER: 4,
            AccessLevel.SUPER_ADMIN: 5
        }

        current_level = level_hierarchy.get(platform_access.access_level, 0)
        required_level_value = level_hierarchy.get(required_level, 0)

        return current_level >= required_level_value

    async def update_usage_metrics(
        self,
        tenant_id: str,
        platform: PlatformType,
        metrics: Dict[str, Any]
    ):
        """Update usage metrics for tenant and platform"""

        cache_key = f"{tenant_id}:{platform.value}"
        context = self.context_cache.get(cache_key)

        if context:
            # Update usage analytics
            platform_key = platform.value
            if platform_key not in context.usage_analytics:
                context.usage_analytics[platform_key] = {}

            for metric, value in metrics.items():
                if metric in context.usage_analytics[platform_key]:
                    context.usage_analytics[platform_key][metric] += value
                else:
                    context.usage_analytics[platform_key][metric] = value

            # Update AI usage if applicable
            if "ai_requests" in metrics:
                current_usage = context.ai_usage_current.get("daily_requests", 0)
                context.ai_usage_current["daily_requests"] = current_usage + metrics["ai_requests"]

            context.updated_at = datetime.utcnow()
            context.last_active = datetime.utcnow()

# ========================================================================================
# CONTEXT MIDDLEWARE
# ========================================================================================

class TenantContextMiddleware:
    """FastAPI middleware for tenant context propagation"""

    def __init__(self, app, context_manager: TenantContextManager):
        self.app = app
        self.context_manager = context_manager

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Extract tenant information from request
            headers = dict(scope.get("headers", []))

            # Get tenant ID from various sources
            tenant_id = self._extract_tenant_id(headers, scope)
            platform = self._extract_platform(headers, scope)

            if tenant_id and platform:
                # Get tenant context
                context = await self.context_manager.get_tenant_context(tenant_id, platform)

                if context:
                    # Add context to request scope
                    scope["tenant_context"] = context

                    # Update last active
                    await self.context_manager.update_usage_metrics(
                        tenant_id, platform, {"requests": 1}
                    )

        await self.app(scope, receive, send)

    def _extract_tenant_id(self, headers: Dict[bytes, bytes], scope: Dict) -> Optional[str]:
        """Extract tenant ID from request headers or path"""

        # Try header first
        tenant_header = headers.get(b"x-tenant-id")
        if tenant_header:
            return tenant_header.decode()

        # Try authorization header (JWT)
        auth_header = headers.get(b"authorization")
        if auth_header:
            try:
                token = auth_header.decode().replace("Bearer ", "")
                # Mock JWT decode - in production, use proper JWT validation
                # payload = jwt.decode(token, key, algorithms=["HS256"])
                # return payload.get("tenant_id")
                return "demo_tenant"  # Mock for development
            except:
                pass

        # Try path parameter
        path = scope.get("path", "")
        if "/tenant/" in path:
            parts = path.split("/tenant/")
            if len(parts) > 1:
                return parts[1].split("/")[0]

        return None

    def _extract_platform(self, headers: Dict[bytes, bytes], scope: Dict) -> Optional[PlatformType]:
        """Extract platform type from request"""

        # Try header first
        platform_header = headers.get(b"x-platform")
        if platform_header:
            try:
                return PlatformType(platform_header.decode())
            except ValueError:
                pass

        # Try host header to determine platform
        host_header = headers.get(b"host")
        if host_header:
            host = host_header.decode()

            # Map ports to platforms
            if ":3008" in host:
                return PlatformType.BIZOHOLIC
            elif ":3007" in host:
                return PlatformType.CORELDOVE
            elif ":3004" in host:
                return PlatformType.BUSINESS_DIRECTORY
            elif ":3005" in host:
                return PlatformType.THRILLRING
            elif ":3012" in host:
                return PlatformType.QUANTTRADE
            elif ":3006" in host:
                return PlatformType.CLIENT_PORTAL
            elif ":3009" in host:
                return PlatformType.ADMIN_DASHBOARD

        # Default to client portal
        return PlatformType.CLIENT_PORTAL

# ========================================================================================
# UTILITY FUNCTIONS
# ========================================================================================

async def get_tenant_context_from_request(request) -> Optional[EnhancedTenantContext]:
    """Get tenant context from FastAPI request object"""
    return getattr(request.scope, "tenant_context", None)

def require_platform_access(platform: PlatformType, level: AccessLevel):
    """Decorator to require specific platform access level"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract request from args
            request = None
            for arg in args:
                if hasattr(arg, "scope"):
                    request = arg
                    break

            if not request:
                raise Exception("Request object not found")

            context = await get_tenant_context_from_request(request)
            if not context:
                raise Exception("Tenant context not found")

            # Validate access
            context_manager = TenantContextManager()
            has_access = await context_manager.validate_platform_access(
                context, platform, level
            )

            if not has_access:
                raise Exception(f"Insufficient access to {platform.value}")

            return await func(*args, **kwargs)
        return wrapper
    return decorator

def get_ai_agents_for_context(context: EnhancedTenantContext) -> List[str]:
    """Get available AI agents for tenant context"""
    return context.ai_context.agent_ids

def check_ai_quota(context: EnhancedTenantContext, requests_needed: int = 1) -> bool:
    """Check if tenant has sufficient AI quota"""
    daily_quota = context.ai_agent_quota.get("daily_requests", 0)
    current_usage = context.ai_usage_current.get("daily_requests", 0)

    return (current_usage + requests_needed) <= daily_quota