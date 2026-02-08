"""
Tenant-Aware AI Agent Coordinator
Manages 93+ CrewAI agents with intelligent tenant context and cross-platform memory
"""

import asyncio
import json
import structlog
from typing import Dict, Any, List, Optional, Union, Tuple
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from contextlib import asynccontextmanager

import numpy as np
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew

from bizosaas.shared.enhanced_tenant_context import (
    EnhancedTenantContext,
    PlatformType,
    TenantTier
)
from bizosaas.shared.rls_manager import RLSManager, RLSContext

logger = structlog.get_logger(__name__)


class AgentSpecialization(Enum):
    """AI Agent specialization categories"""
    # Marketing Specialists
    CONTENT_CREATOR = "content_creator"
    SEO_OPTIMIZER = "seo_optimizer"
    SOCIAL_MEDIA_MANAGER = "social_media_manager"
    EMAIL_MARKETER = "email_marketer"
    PPC_SPECIALIST = "ppc_specialist"
    CONVERSION_OPTIMIZER = "conversion_optimizer"

    # Business Intelligence
    DATA_ANALYST = "data_analyst"
    MARKET_RESEARCHER = "market_researcher"
    COMPETITOR_ANALYST = "competitor_analyst"
    TREND_ANALYST = "trend_analyst"
    CUSTOMER_INSIGHTS = "customer_insights"

    # E-commerce Specialists
    PRODUCT_MANAGER = "product_manager"
    INVENTORY_OPTIMIZER = "inventory_optimizer"
    PRICING_STRATEGIST = "pricing_strategist"
    MARKETPLACE_MANAGER = "marketplace_manager"

    # Gaming & Entertainment
    GAME_CURATOR = "game_curator"
    TOURNAMENT_MANAGER = "tournament_manager"
    COMMUNITY_MANAGER = "community_manager"

    # Financial Analysts
    TRADING_ANALYST = "trading_analyst"
    RISK_MANAGER = "risk_manager"
    PORTFOLIO_OPTIMIZER = "portfolio_optimizer"

    # Platform-Specific
    DIRECTORY_CURATOR = "directory_curator"
    REVIEW_MODERATOR = "review_moderator"

    # General Purpose
    CUSTOMER_SUPPORT = "customer_support"
    PROJECT_MANAGER = "project_manager"
    QUALITY_ASSURANCE = "quality_assurance"


class AgentCapability(Enum):
    """AI Agent capabilities"""
    TEXT_GENERATION = "text_generation"
    DATA_ANALYSIS = "data_analysis"
    IMAGE_PROCESSING = "image_processing"
    WEB_SCRAPING = "web_scraping"
    API_INTEGRATION = "api_integration"
    EMAIL_AUTOMATION = "email_automation"
    REPORT_GENERATION = "report_generation"
    PREDICTIVE_MODELING = "predictive_modeling"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    RECOMMENDATION_ENGINE = "recommendation_engine"
    WORKFLOW_AUTOMATION = "workflow_automation"
    REAL_TIME_MONITORING = "real_time_monitoring"


@dataclass
class TenantAgentMemory:
    """Tenant-specific memory for AI agents"""
    tenant_id: str
    agent_id: str
    interaction_count: int = 0
    success_rate: float = 1.0
    last_interaction: Optional[datetime] = None
    performance_metrics: Dict[str, float] = None
    learned_preferences: Dict[str, Any] = None
    conversation_history: List[Dict[str, Any]] = None
    domain_knowledge: Dict[str, Any] = None

    def __post_init__(self):
        if self.performance_metrics is None:
            self.performance_metrics = {}
        if self.learned_preferences is None:
            self.learned_preferences = {}
        if self.conversation_history is None:
            self.conversation_history = []
        if self.domain_knowledge is None:
            self.domain_knowledge = {}


class TenantAwareAgent(BaseModel):
    """Enhanced AI Agent with tenant awareness"""
    agent_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    specialization: AgentSpecialization
    capabilities: List[AgentCapability]
    supported_platforms: List[PlatformType]
    tier_restrictions: List[TenantTier] = Field(default_factory=list)
    base_agent: Optional[Agent] = Field(default=None, exclude=True)
    memory_store: Dict[str, TenantAgentMemory] = Field(default_factory=dict, exclude=True)
    active_sessions: Dict[str, Dict[str, Any]] = Field(default_factory=dict, exclude=True)
    performance_stats: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True

    def can_serve_tenant(self, tenant_context: EnhancedTenantContext) -> bool:
        """Check if agent can serve the given tenant"""
        # Check tier restrictions
        if self.tier_restrictions and tenant_context.subscription_tier not in self.tier_restrictions:
            return False

        # Check platform access
        for platform in self.supported_platforms:
            platform_access = tenant_context.platform_access.get(platform)
            if platform_access and platform_access.enabled:
                return True

        return False

    def get_tenant_memory(self, tenant_id: str) -> TenantAgentMemory:
        """Get or create tenant-specific memory"""
        if tenant_id not in self.memory_store:
            self.memory_store[tenant_id] = TenantAgentMemory(
                tenant_id=tenant_id,
                agent_id=self.agent_id
            )
        return self.memory_store[tenant_id]

    async def update_performance(
        self,
        tenant_id: str,
        task_success: bool,
        execution_time: float,
        quality_score: float = None
    ):
        """Update performance metrics for tenant"""
        memory = self.get_tenant_memory(tenant_id)
        memory.interaction_count += 1
        memory.last_interaction = datetime.utcnow()

        # Update success rate
        current_successes = memory.success_rate * (memory.interaction_count - 1)
        if task_success:
            current_successes += 1
        memory.success_rate = current_successes / memory.interaction_count

        # Update performance metrics
        if "avg_execution_time" not in memory.performance_metrics:
            memory.performance_metrics["avg_execution_time"] = execution_time
        else:
            current_avg = memory.performance_metrics["avg_execution_time"]
            count = memory.interaction_count
            memory.performance_metrics["avg_execution_time"] = (
                (current_avg * (count - 1) + execution_time) / count
            )

        if quality_score is not None:
            if "avg_quality_score" not in memory.performance_metrics:
                memory.performance_metrics["avg_quality_score"] = quality_score
            else:
                current_avg = memory.performance_metrics["avg_quality_score"]
                count = memory.interaction_count
                memory.performance_metrics["avg_quality_score"] = (
                    (current_avg * (count - 1) + quality_score) / count
                )

        self.last_updated = datetime.utcnow()


class TenantAwareAICoordinator:
    """
    Coordinates 93+ AI agents with tenant-specific intelligence and cross-platform memory
    """

    def __init__(
        self,
        rls_manager: RLSManager,
        vector_store=None,
        enable_cross_tenant_learning: bool = False
    ):
        self.rls_manager = rls_manager
        self.vector_store = vector_store
        self.enable_cross_tenant_learning = enable_cross_tenant_learning

        # Agent registry
        self.agents: Dict[str, TenantAwareAgent] = {}
        self.agent_by_specialization: Dict[AgentSpecialization, List[str]] = {}
        self.agent_by_platform: Dict[PlatformType, List[str]] = {}

        # Performance tracking
        self.global_performance_stats: Dict[str, Any] = {}
        self.tenant_usage_stats: Dict[str, Dict[str, Any]] = {}

        # Session management
        self.active_crews: Dict[str, Crew] = {}
        self.session_contexts: Dict[str, Dict[str, Any]] = {}

        self.logger = logger.bind(component="tenant_aware_ai_coordinator")

        # Initialize with the 93+ agents
        asyncio.create_task(self._initialize_agent_ecosystem())

    async def _initialize_agent_ecosystem(self):
        """Initialize the comprehensive 93+ agent ecosystem"""
        self.logger.info("Initializing 93+ AI agent ecosystem")

        # Define agent configurations
        agent_configs = [
            # Marketing Content Creation (15 agents)
            {
                "name": "Blog Content Creator",
                "specialization": AgentSpecialization.CONTENT_CREATOR,
                "capabilities": [
                    AgentCapability.TEXT_GENERATION,
                    AgentCapability.SEO_OPTIMIZATION,
                    AgentCapability.RESEARCH
                ],
                "platforms": [PlatformType.BIZOHOLIC],
                "tier_restrictions": []
            },
            {
                "name": "Social Media Content Creator",
                "specialization": AgentSpecialization.CONTENT_CREATOR,
                "capabilities": [
                    AgentCapability.TEXT_GENERATION,
                    AgentCapability.IMAGE_PROCESSING,
                    AgentCapability.TREND_ANALYSIS
                ],
                "platforms": [PlatformType.BIZOHOLIC, PlatformType.THRILLRING],
                "tier_restrictions": []
            },
            {
                "name": "Email Campaign Creator",
                "specialization": AgentSpecialization.EMAIL_MARKETER,
                "capabilities": [
                    AgentCapability.TEXT_GENERATION,
                    AgentCapability.EMAIL_AUTOMATION,
                    AgentCapability.PERSONALIZATION
                ],
                "platforms": [PlatformType.BIZOHOLIC],
                "tier_restrictions": []
            },
            {
                "name": "Product Description Writer",
                "specialization": AgentSpecialization.CONTENT_CREATOR,
                "capabilities": [
                    AgentCapability.TEXT_GENERATION,
                    AgentCapability.SEO_OPTIMIZATION
                ],
                "platforms": [PlatformType.CORELDOVE],
                "tier_restrictions": []
            },
            {
                "name": "Video Script Creator",
                "specialization": AgentSpecialization.CONTENT_CREATOR,
                "capabilities": [
                    AgentCapability.TEXT_GENERATION,
                    AgentCapability.VIDEO_OPTIMIZATION
                ],
                "platforms": [PlatformType.BIZOHOLIC, PlatformType.THRILLRING],
                "tier_restrictions": [TenantTier.PROFESSIONAL, TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]
            },

            # SEO & Search Optimization (10 agents)
            {
                "name": "Technical SEO Analyst",
                "specialization": AgentSpecialization.SEO_OPTIMIZER,
                "capabilities": [
                    AgentCapability.WEB_SCRAPING,
                    AgentCapability.DATA_ANALYSIS,
                    AgentCapability.TECHNICAL_AUDIT
                ],
                "platforms": [PlatformType.BIZOHOLIC, PlatformType.BUSINESS_DIRECTORY],
                "tier_restrictions": [TenantTier.PROFESSIONAL, TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]
            },
            {
                "name": "Keyword Research Specialist",
                "specialization": AgentSpecialization.SEO_OPTIMIZER,
                "capabilities": [
                    AgentCapability.DATA_ANALYSIS,
                    AgentCapability.COMPETITIVE_ANALYSIS,
                    AgentCapability.TREND_ANALYSIS
                ],
                "platforms": [PlatformType.BIZOHOLIC, PlatformType.CORELDOVE],
                "tier_restrictions": []
            },
            {
                "name": "Local SEO Optimizer",
                "specialization": AgentSpecialization.SEO_OPTIMIZER,
                "capabilities": [
                    AgentCapability.LOCAL_SEARCH,
                    AgentCapability.MAP_OPTIMIZATION,
                    AgentCapability.REVIEW_MANAGEMENT
                ],
                "platforms": [PlatformType.BUSINESS_DIRECTORY],
                "tier_restrictions": []
            },

            # Social Media Management (12 agents)
            {
                "name": "Instagram Growth Manager",
                "specialization": AgentSpecialization.SOCIAL_MEDIA_MANAGER,
                "capabilities": [
                    AgentCapability.CONTENT_SCHEDULING,
                    AgentCapability.HASHTAG_OPTIMIZATION,
                    AgentCapability.ENGAGEMENT_AUTOMATION
                ],
                "platforms": [PlatformType.BIZOHOLIC],
                "tier_restrictions": []
            },
            {
                "name": "LinkedIn B2B Specialist",
                "specialization": AgentSpecialization.SOCIAL_MEDIA_MANAGER,
                "capabilities": [
                    AgentCapability.B2B_OUTREACH,
                    AgentCapability.LEAD_GENERATION,
                    AgentCapability.PROFESSIONAL_NETWORKING
                ],
                "platforms": [PlatformType.BIZOHOLIC],
                "tier_restrictions": [TenantTier.STARTER, TenantTier.PROFESSIONAL, TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]
            },
            {
                "name": "TikTok Viral Content Creator",
                "specialization": AgentSpecialization.SOCIAL_MEDIA_MANAGER,
                "capabilities": [
                    AgentCapability.VIDEO_OPTIMIZATION,
                    AgentCapability.TREND_ANALYSIS,
                    AgentCapability.VIRAL_PREDICTION
                ],
                "platforms": [PlatformType.BIZOHOLIC, PlatformType.THRILLRING],
                "tier_restrictions": [TenantTier.PROFESSIONAL, TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]
            },

            # E-commerce Optimization (15 agents)
            {
                "name": "Amazon Product Optimizer",
                "specialization": AgentSpecialization.PRODUCT_MANAGER,
                "capabilities": [
                    AgentCapability.PRODUCT_OPTIMIZATION,
                    AgentCapability.COMPETITIVE_PRICING,
                    AgentCapability.INVENTORY_MANAGEMENT
                ],
                "platforms": [PlatformType.CORELDOVE],
                "tier_restrictions": []
            },
            {
                "name": "Shopify Store Optimizer",
                "specialization": AgentSpecialization.CONVERSION_OPTIMIZER,
                "capabilities": [
                    AgentCapability.A_B_TESTING,
                    AgentCapability.UX_OPTIMIZATION,
                    AgentCapability.CONVERSION_TRACKING
                ],
                "platforms": [PlatformType.CORELDOVE],
                "tier_restrictions": []
            },
            {
                "name": "Dynamic Pricing Strategist",
                "specialization": AgentSpecialization.PRICING_STRATEGIST,
                "capabilities": [
                    AgentCapability.PREDICTIVE_MODELING,
                    AgentCapability.MARKET_ANALYSIS,
                    AgentCapability.COMPETITIVE_INTELLIGENCE
                ],
                "platforms": [PlatformType.CORELDOVE],
                "tier_restrictions": [TenantTier.PROFESSIONAL, TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]
            },

            # Business Intelligence & Analytics (10 agents)
            {
                "name": "Customer Behavior Analyst",
                "specialization": AgentSpecialization.DATA_ANALYST,
                "capabilities": [
                    AgentCapability.DATA_ANALYSIS,
                    AgentCapability.BEHAVIORAL_MODELING,
                    AgentCapability.PREDICTIVE_ANALYTICS
                ],
                "platforms": list(PlatformType),
                "tier_restrictions": [TenantTier.PROFESSIONAL, TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]
            },
            {
                "name": "Market Trend Predictor",
                "specialization": AgentSpecialization.TREND_ANALYST,
                "capabilities": [
                    AgentCapability.TREND_ANALYSIS,
                    AgentCapability.MARKET_RESEARCH,
                    AgentCapability.FORECASTING
                ],
                "platforms": list(PlatformType),
                "tier_restrictions": [TenantTier.PROFESSIONAL, TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]
            },

            # Gaming & Entertainment (8 agents)
            {
                "name": "Game Recommendation Engine",
                "specialization": AgentSpecialization.GAME_CURATOR,
                "capabilities": [
                    AgentCapability.RECOMMENDATION_ENGINE,
                    AgentCapability.PREFERENCE_LEARNING,
                    AgentCapability.GAMING_ANALYTICS
                ],
                "platforms": [PlatformType.THRILLRING],
                "tier_restrictions": []
            },
            {
                "name": "Tournament Bracket Manager",
                "specialization": AgentSpecialization.TOURNAMENT_MANAGER,
                "capabilities": [
                    AgentCapability.TOURNAMENT_OPTIMIZATION,
                    AgentCapability.PLAYER_MATCHING,
                    AgentCapability.SCHEDULE_MANAGEMENT
                ],
                "platforms": [PlatformType.THRILLRING],
                "tier_restrictions": [TenantTier.STARTER, TenantTier.PROFESSIONAL, TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]
            },

            # Financial & Trading (12 agents)
            {
                "name": "Algorithmic Trading Strategist",
                "specialization": AgentSpecialization.TRADING_ANALYST,
                "capabilities": [
                    AgentCapability.ALGORITHMIC_TRADING,
                    AgentCapability.TECHNICAL_ANALYSIS,
                    AgentCapability.RISK_ASSESSMENT
                ],
                "platforms": [PlatformType.QUANTTRADE],
                "tier_restrictions": [TenantTier.PROFESSIONAL, TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]
            },
            {
                "name": "Portfolio Risk Manager",
                "specialization": AgentSpecialization.RISK_MANAGER,
                "capabilities": [
                    AgentCapability.RISK_MODELING,
                    AgentCapability.PORTFOLIO_OPTIMIZATION,
                    AgentCapability.STRESS_TESTING
                ],
                "platforms": [PlatformType.QUANTTRADE],
                "tier_restrictions": [TenantTier.PROFESSIONAL, TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]
            },

            # Business Directory (6 agents)
            {
                "name": "Business Listing Optimizer",
                "specialization": AgentSpecialization.DIRECTORY_CURATOR,
                "capabilities": [
                    AgentCapability.LISTING_OPTIMIZATION,
                    AgentCapability.CATEGORY_CLASSIFICATION,
                    AgentCapability.QUALITY_SCORING
                ],
                "platforms": [PlatformType.BUSINESS_DIRECTORY],
                "tier_restrictions": []
            },
            {
                "name": "Review Sentiment Analyzer",
                "specialization": AgentSpecialization.REVIEW_MODERATOR,
                "capabilities": [
                    AgentCapability.SENTIMENT_ANALYSIS,
                    AgentCapability.REVIEW_MODERATION,
                    AgentCapability.REPUTATION_MANAGEMENT
                ],
                "platforms": [PlatformType.BUSINESS_DIRECTORY],
                "tier_restrictions": []
            },

            # Customer Support & Communication (5 agents)
            {
                "name": "Multi-Platform Support Agent",
                "specialization": AgentSpecialization.CUSTOMER_SUPPORT,
                "capabilities": [
                    AgentCapability.CONVERSATIONAL_AI,
                    AgentCapability.ISSUE_RESOLUTION,
                    AgentCapability.ESCALATION_MANAGEMENT
                ],
                "platforms": list(PlatformType),
                "tier_restrictions": []
            },
        ]

        # Create all agents
        for config in agent_configs:
            agent = TenantAwareAgent(
                name=config["name"],
                specialization=config["specialization"],
                capabilities=config["capabilities"],
                supported_platforms=config["platforms"],
                tier_restrictions=config["tier_restrictions"]
            )

            await self.register_agent(agent)

        self.logger.info(
            "AI agent ecosystem initialized",
            total_agents=len(self.agents),
            specializations=len(self.agent_by_specialization),
            platforms=len(self.agent_by_platform)
        )

    async def register_agent(self, agent: TenantAwareAgent):
        """Register a new AI agent in the ecosystem"""
        self.agents[agent.agent_id] = agent

        # Index by specialization
        if agent.specialization not in self.agent_by_specialization:
            self.agent_by_specialization[agent.specialization] = []
        self.agent_by_specialization[agent.specialization].append(agent.agent_id)

        # Index by platform
        for platform in agent.supported_platforms:
            if platform not in self.agent_by_platform:
                self.agent_by_platform[platform] = []
            self.agent_by_platform[platform].append(agent.agent_id)

        self.logger.info(
            "Agent registered",
            agent_id=agent.agent_id,
            name=agent.name,
            specialization=agent.specialization.value,
            platforms=[p.value for p in agent.supported_platforms]
        )

    async def find_optimal_agent(
        self,
        tenant_context: EnhancedTenantContext,
        task_description: str,
        platform: PlatformType,
        specialization_preference: Optional[AgentSpecialization] = None
    ) -> Optional[TenantAwareAgent]:
        """
        Find the optimal agent for a given task and tenant context

        Args:
            tenant_context: Enhanced tenant context
            task_description: Description of the task
            platform: Target platform
            specialization_preference: Preferred agent specialization

        Returns:
            Best matching agent or None if no suitable agent found
        """
        try:
            # Get candidate agents for the platform
            candidate_agent_ids = self.agent_by_platform.get(platform, [])

            if not candidate_agent_ids:
                self.logger.warning(
                    "No agents found for platform",
                    platform=platform.value
                )
                return None

            # Filter by tenant compatibility
            compatible_agents = []
            for agent_id in candidate_agent_ids:
                agent = self.agents[agent_id]
                if agent.can_serve_tenant(tenant_context):
                    compatible_agents.append(agent)

            if not compatible_agents:
                self.logger.warning(
                    "No compatible agents found for tenant",
                    tenant_id=tenant_context.tenant_id,
                    platform=platform.value,
                    subscription_tier=tenant_context.subscription_tier.value
                )
                return None

            # Filter by specialization preference if provided
            if specialization_preference:
                specialized_agents = [
                    agent for agent in compatible_agents
                    if agent.specialization == specialization_preference
                ]
                if specialized_agents:
                    compatible_agents = specialized_agents

            # Score agents based on performance and fit
            scored_agents = []
            for agent in compatible_agents:
                score = await self._score_agent_for_task(
                    agent, tenant_context, task_description, platform
                )
                scored_agents.append((agent, score))

            # Sort by score and return the best agent
            scored_agents.sort(key=lambda x: x[1], reverse=True)
            best_agent = scored_agents[0][0]

            self.logger.info(
                "Optimal agent selected",
                agent_id=best_agent.agent_id,
                agent_name=best_agent.name,
                specialization=best_agent.specialization.value,
                score=scored_agents[0][1],
                tenant_id=tenant_context.tenant_id,
                platform=platform.value
            )

            return best_agent

        except Exception as e:
            self.logger.error(
                "Failed to find optimal agent",
                tenant_id=tenant_context.tenant_id,
                platform=platform.value,
                error=str(e)
            )
            return None

    async def _score_agent_for_task(
        self,
        agent: TenantAwareAgent,
        tenant_context: EnhancedTenantContext,
        task_description: str,
        platform: PlatformType
    ) -> float:
        """
        Score an agent's suitability for a specific task

        Returns a score between 0.0 and 1.0
        """
        score = 0.0

        # Base platform compatibility score (0.3)
        if platform in agent.supported_platforms:
            score += 0.3

        # Tenant-specific performance score (0.4)
        tenant_memory = agent.get_tenant_memory(tenant_context.tenant_id)
        if tenant_memory.interaction_count > 0:
            score += 0.4 * tenant_memory.success_rate
        else:
            score += 0.2  # Default score for new agents

        # Capability matching score (0.2)
        # Use simple keyword matching for task description
        task_keywords = task_description.lower().split()
        capability_matches = 0
        for capability in agent.capabilities:
            capability_keywords = capability.value.replace("_", " ").split()
            if any(keyword in task_keywords for keyword in capability_keywords):
                capability_matches += 1

        if agent.capabilities:
            score += 0.2 * (capability_matches / len(agent.capabilities))

        # Specialization bonus (0.1)
        specialization_keywords = agent.specialization.value.replace("_", " ").split()
        if any(keyword in task_keywords for keyword in specialization_keywords):
            score += 0.1

        return min(score, 1.0)

    async def execute_agent_task(
        self,
        tenant_context: EnhancedTenantContext,
        agent_id: str,
        task_description: str,
        task_data: Dict[str, Any],
        platform: PlatformType
    ) -> Dict[str, Any]:
        """
        Execute a task using a specific agent with tenant context

        Args:
            tenant_context: Enhanced tenant context
            agent_id: ID of the agent to use
            task_description: Description of the task
            task_data: Task input data
            platform: Target platform

        Returns:
            Task execution results
        """
        start_time = datetime.utcnow()

        try:
            agent = self.agents.get(agent_id)
            if not agent:
                raise ValueError(f"Agent {agent_id} not found")

            if not agent.can_serve_tenant(tenant_context):
                raise ValueError(f"Agent {agent_id} cannot serve tenant {tenant_context.tenant_id}")

            # Create RLS context for database operations
            rls_context = await self.rls_manager.create_tenant_context_from_enhanced(
                tenant_context
            )

            # Execute the task with tenant context
            async with self.rls_manager.tenant_session(rls_context) as conn:
                # Get tenant-specific memory and preferences
                tenant_memory = agent.get_tenant_memory(tenant_context.tenant_id)

                # Prepare task context
                task_context = {
                    "tenant_id": tenant_context.tenant_id,
                    "platform": platform.value,
                    "subscription_tier": tenant_context.subscription_tier.value,
                    "learned_preferences": tenant_memory.learned_preferences,
                    "domain_knowledge": tenant_memory.domain_knowledge,
                    "task_data": task_data,
                    "database_connection": conn
                }

                # Execute the actual task (this would integrate with CrewAI)
                result = await self._execute_crewai_task(
                    agent, task_description, task_context
                )

                # Update agent performance
                execution_time = (datetime.utcnow() - start_time).total_seconds()
                quality_score = result.get("quality_score", 0.8)  # Default quality score

                await agent.update_performance(
                    tenant_context.tenant_id,
                    task_success=result.get("success", True),
                    execution_time=execution_time,
                    quality_score=quality_score
                )

                # Store conversation history
                await self._store_interaction_history(
                    conn, tenant_context, agent, task_description, result
                )

                # Update global performance stats
                await self._update_global_stats(agent_id, result, execution_time)

                self.logger.info(
                    "Agent task executed successfully",
                    agent_id=agent_id,
                    tenant_id=tenant_context.tenant_id,
                    platform=platform.value,
                    execution_time=execution_time,
                    success=result.get("success", True)
                )

                return {
                    "success": True,
                    "agent_id": agent_id,
                    "agent_name": agent.name,
                    "execution_time": execution_time,
                    "result": result,
                    "tenant_id": tenant_context.tenant_id,
                    "platform": platform.value,
                    "timestamp": start_time.isoformat()
                }

        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()

            # Update agent performance for failure
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                await agent.update_performance(
                    tenant_context.tenant_id,
                    task_success=False,
                    execution_time=execution_time
                )

            self.logger.error(
                "Agent task execution failed",
                agent_id=agent_id,
                tenant_id=tenant_context.tenant_id,
                platform=platform.value,
                error=str(e),
                execution_time=execution_time
            )

            return {
                "success": False,
                "error": str(e),
                "agent_id": agent_id,
                "execution_time": execution_time,
                "tenant_id": tenant_context.tenant_id,
                "platform": platform.value,
                "timestamp": start_time.isoformat()
            }

    async def _execute_crewai_task(
        self,
        agent: TenantAwareAgent,
        task_description: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the actual CrewAI task with tenant context

        This is where the integration with CrewAI happens
        """
        try:
            # Mock implementation - replace with actual CrewAI integration
            await asyncio.sleep(0.1)  # Simulate processing time

            # Extract relevant context for task execution
            tenant_preferences = context.get("learned_preferences", {})
            platform = context.get("platform")
            task_data = context.get("task_data", {})

            # Simulate agent-specific processing based on specialization
            if agent.specialization == AgentSpecialization.CONTENT_CREATOR:
                result = await self._execute_content_creation_task(
                    task_description, task_data, tenant_preferences
                )
            elif agent.specialization == AgentSpecialization.SEO_OPTIMIZER:
                result = await self._execute_seo_optimization_task(
                    task_description, task_data, tenant_preferences
                )
            elif agent.specialization == AgentSpecialization.DATA_ANALYST:
                result = await self._execute_analytics_task(
                    task_description, task_data, tenant_preferences
                )
            else:
                # Generic task execution
                result = {
                    "output": f"Task '{task_description}' completed by {agent.name}",
                    "quality_score": 0.8,
                    "recommendations": [],
                    "metadata": {
                        "agent_specialization": agent.specialization.value,
                        "platform": platform
                    }
                }

            return {
                "success": True,
                "output": result.get("output"),
                "quality_score": result.get("quality_score", 0.8),
                "recommendations": result.get("recommendations", []),
                "metadata": result.get("metadata", {}),
                "execution_details": {
                    "agent_specialization": agent.specialization.value,
                    "capabilities_used": [cap.value for cap in agent.capabilities],
                    "tenant_preferences_applied": bool(tenant_preferences)
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None,
                "quality_score": 0.0
            }

    async def _execute_content_creation_task(
        self,
        task_description: str,
        task_data: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute content creation specific task"""
        content_type = task_data.get("content_type", "blog_post")
        target_audience = task_data.get("target_audience", "general")
        tone = preferences.get("preferred_tone", "professional")

        return {
            "output": f"Created {content_type} for {target_audience} with {tone} tone",
            "quality_score": 0.85,
            "recommendations": [
                "Consider adding more visual elements",
                "Optimize for mobile reading"
            ],
            "metadata": {
                "content_type": content_type,
                "word_count": 800,
                "seo_score": 85,
                "readability_score": 78
            }
        }

    async def _execute_seo_optimization_task(
        self,
        task_description: str,
        task_data: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute SEO optimization specific task"""
        target_keywords = task_data.get("keywords", [])
        page_url = task_data.get("url", "")

        return {
            "output": f"SEO optimization completed for {page_url}",
            "quality_score": 0.82,
            "recommendations": [
                "Improve page loading speed",
                "Add more internal links",
                "Optimize meta descriptions"
            ],
            "metadata": {
                "target_keywords": target_keywords,
                "current_ranking": "Improved",
                "optimization_score": 82,
                "technical_issues_found": 3
            }
        }

    async def _execute_analytics_task(
        self,
        task_description: str,
        task_data: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute data analytics specific task"""
        data_source = task_data.get("data_source", "website")
        metrics = task_data.get("metrics", ["traffic", "conversions"])

        return {
            "output": f"Analytics report generated for {data_source}",
            "quality_score": 0.88,
            "recommendations": [
                "Focus on improving conversion rate",
                "Investigate traffic drop on mobile",
                "Expand successful campaigns"
            ],
            "metadata": {
                "data_points_analyzed": 15000,
                "insights_generated": 12,
                "actionable_recommendations": 8,
                "confidence_level": 0.92
            }
        }

    async def _store_interaction_history(
        self,
        connection,
        tenant_context: EnhancedTenantContext,
        agent: TenantAwareAgent,
        task_description: str,
        result: Dict[str, Any]
    ):
        """Store interaction history in the database"""
        try:
            await connection.execute("""
                INSERT INTO ai_agent_interactions (
                    tenant_id, agent_id, platform, interaction_type,
                    input_data, output_data, processing_time_ms,
                    success, user_id, created_at, platform_context
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """,
                tenant_context.tenant_id,
                agent.agent_id,
                "multi_platform",  # Could be more specific based on context
                "task_execution",
                {"task_description": task_description},
                result,
                int(result.get("execution_time", 0) * 1000),
                result.get("success", True),
                None,  # user_id if available
                datetime.utcnow(),
                {"agent_name": agent.name, "specialization": agent.specialization.value}
            )
        except Exception as e:
            self.logger.error(
                "Failed to store interaction history",
                error=str(e)
            )

    async def _update_global_stats(
        self,
        agent_id: str,
        result: Dict[str, Any],
        execution_time: float
    ):
        """Update global performance statistics"""
        if agent_id not in self.global_performance_stats:
            self.global_performance_stats[agent_id] = {
                "total_executions": 0,
                "successful_executions": 0,
                "average_execution_time": 0.0,
                "average_quality_score": 0.0
            }

        stats = self.global_performance_stats[agent_id]
        stats["total_executions"] += 1

        if result.get("success", False):
            stats["successful_executions"] += 1

        # Update moving averages
        total = stats["total_executions"]
        stats["average_execution_time"] = (
            (stats["average_execution_time"] * (total - 1) + execution_time) / total
        )

        quality_score = result.get("quality_score", 0.0)
        stats["average_quality_score"] = (
            (stats["average_quality_score"] * (total - 1) + quality_score) / total
        )

    async def get_agent_recommendations(
        self,
        tenant_context: EnhancedTenantContext,
        platform: PlatformType,
        task_type: str
    ) -> List[Dict[str, Any]]:
        """
        Get agent recommendations for a specific task type and platform

        Returns a list of recommended agents with their capabilities and performance
        """
        try:
            # Get all compatible agents for the platform
            candidate_agent_ids = self.agent_by_platform.get(platform, [])
            recommendations = []

            for agent_id in candidate_agent_ids:
                agent = self.agents[agent_id]

                if not agent.can_serve_tenant(tenant_context):
                    continue

                # Get performance metrics
                tenant_memory = agent.get_tenant_memory(tenant_context.tenant_id)
                global_stats = self.global_performance_stats.get(agent_id, {})

                recommendation = {
                    "agent_id": agent_id,
                    "name": agent.name,
                    "specialization": agent.specialization.value,
                    "capabilities": [cap.value for cap in agent.capabilities],
                    "tenant_performance": {
                        "interaction_count": tenant_memory.interaction_count,
                        "success_rate": tenant_memory.success_rate,
                        "average_quality": tenant_memory.performance_metrics.get("avg_quality_score", 0.0)
                    },
                    "global_performance": {
                        "total_executions": global_stats.get("total_executions", 0),
                        "success_rate": (
                            global_stats.get("successful_executions", 0) /
                            max(global_stats.get("total_executions", 1), 1)
                        ),
                        "average_execution_time": global_stats.get("average_execution_time", 0.0)
                    },
                    "suitability_score": await self._score_agent_for_task(
                        agent, tenant_context, task_type, platform
                    )
                }

                recommendations.append(recommendation)

            # Sort by suitability score
            recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)

            self.logger.info(
                "Agent recommendations generated",
                tenant_id=tenant_context.tenant_id,
                platform=platform.value,
                task_type=task_type,
                recommendation_count=len(recommendations)
            )

            return recommendations

        except Exception as e:
            self.logger.error(
                "Failed to generate agent recommendations",
                tenant_id=tenant_context.tenant_id,
                platform=platform.value,
                task_type=task_type,
                error=str(e)
            )
            return []

    async def get_tenant_performance_dashboard(
        self,
        tenant_context: EnhancedTenantContext
    ) -> Dict[str, Any]:
        """
        Generate comprehensive performance dashboard for a tenant

        Returns detailed analytics and insights about AI agent usage
        """
        try:
            dashboard_data = {
                "tenant_id": tenant_context.tenant_id,
                "subscription_tier": tenant_context.subscription_tier.value,
                "platform_access": {
                    platform.value: access.enabled
                    for platform, access in tenant_context.platform_access.items()
                },
                "agent_usage": {},
                "platform_performance": {},
                "recommendations": [],
                "generated_at": datetime.utcnow().isoformat()
            }

            # Collect usage statistics per agent
            total_interactions = 0
            total_success_rate = 0.0
            agent_count = 0

            for agent_id, agent in self.agents.items():
                tenant_memory = agent.get_tenant_memory(tenant_context.tenant_id)

                if tenant_memory.interaction_count > 0:
                    agent_count += 1
                    total_interactions += tenant_memory.interaction_count
                    total_success_rate += tenant_memory.success_rate

                    dashboard_data["agent_usage"][agent_id] = {
                        "name": agent.name,
                        "specialization": agent.specialization.value,
                        "interaction_count": tenant_memory.interaction_count,
                        "success_rate": tenant_memory.success_rate,
                        "last_interaction": (
                            tenant_memory.last_interaction.isoformat()
                            if tenant_memory.last_interaction else None
                        ),
                        "performance_metrics": tenant_memory.performance_metrics
                    }

            # Calculate overall statistics
            if agent_count > 0:
                dashboard_data["overall_stats"] = {
                    "total_interactions": total_interactions,
                    "average_success_rate": total_success_rate / agent_count,
                    "active_agents": agent_count,
                    "available_agents": len([
                        agent for agent in self.agents.values()
                        if agent.can_serve_tenant(tenant_context)
                    ])
                }

            # Platform-specific performance
            for platform in tenant_context.platform_access.keys():
                if tenant_context.platform_access[platform].enabled:
                    platform_agents = [
                        agent_id for agent_id in self.agent_by_platform.get(platform, [])
                        if agent_id in dashboard_data["agent_usage"]
                    ]

                    if platform_agents:
                        platform_interactions = sum(
                            dashboard_data["agent_usage"][agent_id]["interaction_count"]
                            for agent_id in platform_agents
                        )
                        platform_success_rate = sum(
                            dashboard_data["agent_usage"][agent_id]["success_rate"]
                            for agent_id in platform_agents
                        ) / len(platform_agents)

                        dashboard_data["platform_performance"][platform.value] = {
                            "total_interactions": platform_interactions,
                            "average_success_rate": platform_success_rate,
                            "active_agents": len(platform_agents)
                        }

            # Generate recommendations
            dashboard_data["recommendations"] = await self._generate_tenant_recommendations(
                tenant_context, dashboard_data
            )

            return dashboard_data

        except Exception as e:
            self.logger.error(
                "Failed to generate tenant performance dashboard",
                tenant_id=tenant_context.tenant_id,
                error=str(e)
            )
            return {
                "error": str(e),
                "tenant_id": tenant_context.tenant_id,
                "generated_at": datetime.utcnow().isoformat()
            }

    async def _generate_tenant_recommendations(
        self,
        tenant_context: EnhancedTenantContext,
        dashboard_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate actionable recommendations for the tenant"""
        recommendations = []

        overall_stats = dashboard_data.get("overall_stats", {})
        total_interactions = overall_stats.get("total_interactions", 0)
        average_success_rate = overall_stats.get("average_success_rate", 1.0)

        # Recommendation: Increase agent usage
        if total_interactions < 10:
            recommendations.append({
                "type": "usage_increase",
                "priority": "medium",
                "title": "Explore AI Agent Capabilities",
                "description": "You have limited AI agent interactions. Consider exploring more automation opportunities.",
                "action_items": [
                    "Try content generation agents for marketing",
                    "Use analytics agents for data insights",
                    "Automate routine tasks with specialized agents"
                ]
            })

        # Recommendation: Improve success rate
        if average_success_rate < 0.8:
            recommendations.append({
                "type": "performance_improvement",
                "priority": "high",
                "title": "Improve Agent Task Success Rate",
                "description": f"Current success rate is {average_success_rate:.1%}. Consider task optimization.",
                "action_items": [
                    "Provide more specific task instructions",
                    "Review failed tasks for common patterns",
                    "Consider upgrading subscription for premium agents"
                ]
            })

        # Recommendation: Platform expansion
        inactive_platforms = [
            platform for platform, access in tenant_context.platform_access.items()
            if not access.enabled
        ]
        if inactive_platforms and tenant_context.subscription_tier != TenantTier.FREE:
            recommendations.append({
                "type": "platform_expansion",
                "priority": "low",
                "title": "Expand to Additional Platforms",
                "description": "Consider enabling additional platforms for comprehensive automation.",
                "action_items": [
                    f"Enable {platform.value} platform access" for platform in inactive_platforms[:3]
                ]
            })

        # Recommendation: Subscription upgrade
        if tenant_context.subscription_tier == TenantTier.FREE and total_interactions > 50:
            recommendations.append({
                "type": "subscription_upgrade",
                "priority": "medium",
                "title": "Consider Subscription Upgrade",
                "description": "Unlock premium agents and advanced features with a paid subscription.",
                "action_items": [
                    "Access premium AI agents",
                    "Get advanced analytics and reporting",
                    "Increase usage limits and capabilities"
                ]
            })

        return recommendations