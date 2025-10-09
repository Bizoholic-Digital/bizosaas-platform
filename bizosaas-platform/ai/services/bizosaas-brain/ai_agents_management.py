"""
AI Agents Management Interface for BizOSaaS Brain API

Provides comprehensive management and monitoring capabilities for the 45+ CrewAI agents
including execution control, performance monitoring, and tenant-specific customization.
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field
import structlog

# Import event bus integration for agent events
from event_bus_integration import (
    publish_brain_event,
    publish_ai_agent_result,
    BrainEventTypes
)

# Import unified tenant system
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from unified_tenant_middleware import UnifiedTenant

logger = structlog.get_logger(__name__)


class AgentStatus(str, Enum):
    """AI Agent execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    DISABLED = "disabled"


class AgentCategory(str, Enum):
    """AI Agent categories for organization"""
    MARKETING = "marketing"
    SEO = "seo"
    CONTENT = "content"
    ANALYTICS = "analytics"
    AUTOMATION = "automation"
    CUSTOMER_SERVICE = "customer_service"
    LEAD_GENERATION = "lead_generation"
    SOCIAL_MEDIA = "social_media"
    EMAIL_MARKETING = "email_marketing"
    INFRASTRUCTURE = "infrastructure"
    MONITORING = "monitoring"
    SECURITY = "security"
    ECOMMERCE = "ecommerce"


class AgentPriority(str, Enum):
    """AI Agent execution priority"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class AIAgentConfig(BaseModel):
    """AI Agent configuration model"""
    agent_id: str = Field(..., description="Unique agent identifier")
    name: str = Field(..., description="Human-readable agent name")
    description: str = Field(..., description="Agent description and capabilities")
    category: AgentCategory = Field(..., description="Agent category")
    priority: AgentPriority = Field(default=AgentPriority.NORMAL, description="Execution priority")
    
    # Agent behavior configuration
    model: str = Field(default="gpt-4", description="AI model to use")
    temperature: float = Field(default=0.7, description="Model temperature")
    max_tokens: int = Field(default=2000, description="Maximum tokens")
    timeout_seconds: int = Field(default=300, description="Execution timeout")
    
    # Tenant configuration
    tenant_specific: bool = Field(default=True, description="Whether agent is tenant-specific")
    enabled_by_default: bool = Field(default=True, description="Whether enabled for new tenants")
    
    # Execution settings
    retry_attempts: int = Field(default=3, description="Number of retry attempts")
    cooldown_seconds: int = Field(default=60, description="Cooldown between executions")
    
    # Dependencies and triggers
    dependencies: List[str] = Field(default_factory=list, description="Required agent dependencies")
    triggers: List[str] = Field(default_factory=list, description="Event triggers")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    version: str = Field(default="1.0.0", description="Agent version")
    tags: List[str] = Field(default_factory=list, description="Agent tags")


class AIAgentExecution(BaseModel):
    """AI Agent execution record"""
    execution_id: str = Field(default_factory=lambda: str(uuid4()))
    agent_id: str = Field(..., description="Agent identifier")
    tenant_id: str = Field(..., description="Tenant identifier")
    
    # Execution details
    status: AgentStatus = Field(default=AgentStatus.IDLE)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    
    # Input/Output
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    
    # Performance metrics
    tokens_used: Optional[int] = None
    cost_usd: Optional[float] = None
    success_rate: Optional[float] = None
    
    # Metadata
    triggered_by: Optional[str] = None
    correlation_id: Optional[str] = None
    parent_execution_id: Optional[str] = None


class AIAgentMetrics(BaseModel):
    """AI Agent performance metrics"""
    agent_id: str
    tenant_id: Optional[str] = None
    time_period: str = "24h"
    
    # Execution statistics
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    average_duration_seconds: float = 0.0
    
    # Performance metrics
    success_rate: float = 0.0
    average_cost_usd: float = 0.0
    total_tokens_used: int = 0
    
    # Recent activity
    last_execution_at: Optional[datetime] = None
    status: AgentStatus = AgentStatus.IDLE
    
    # Trend data
    daily_executions: List[int] = Field(default_factory=list)
    hourly_success_rates: List[float] = Field(default_factory=list)


class AIAgentsManager:
    """
    Comprehensive AI Agents management system for BizOSaaS platform
    
    Provides full lifecycle management of CrewAI agents including:
    - Agent configuration and deployment
    - Execution monitoring and control
    - Performance analytics and optimization
    - Tenant-specific customization
    """
    
    def __init__(self, vault_client=None, redis_client=None):
        self.vault_client = vault_client
        self.redis_client = redis_client
        self.logger = logger.bind(component="ai_agents_manager")
        
        # Agent registry - will be loaded from Vault/database
        self.agent_registry: Dict[str, AIAgentConfig] = {}
        self.execution_history: Dict[str, List[AIAgentExecution]] = {}
        
        # Initialize with default agents
        self._initialize_default_agents()
    
    def _initialize_default_agents(self):
        """Initialize the comprehensive set of 45+ AI agents"""
        
        # Marketing Agents (12 agents)
        marketing_agents = [
            {
                "agent_id": "marketing_strategy_planner",
                "name": "Marketing Strategy Planner",
                "description": "Creates comprehensive marketing strategies based on business goals and market analysis",
                "category": AgentCategory.MARKETING,
                "priority": AgentPriority.HIGH,
                "triggers": ["tenant_created", "campaign_request"]
            },
            {
                "agent_id": "brand_voice_analyzer",
                "name": "Brand Voice Analyzer",
                "description": "Analyzes and maintains consistent brand voice across all marketing materials",
                "category": AgentCategory.MARKETING,
                "triggers": ["content_created", "brand_update"]
            },
            {
                "agent_id": "competitor_analyzer",
                "name": "Competitor Analysis Agent",
                "description": "Monitors competitors and provides strategic insights",
                "category": AgentCategory.MARKETING,
                "triggers": ["weekly_analysis", "competitor_update"]
            },
            {
                "agent_id": "market_research_agent",
                "name": "Market Research Specialist",
                "description": "Conducts market research and trend analysis",
                "category": AgentCategory.MARKETING,
                "triggers": ["market_research_request", "monthly_analysis"]
            },
            {
                "agent_id": "campaign_optimizer",
                "name": "Campaign Performance Optimizer",
                "description": "Optimizes marketing campaigns based on performance data",
                "category": AgentCategory.MARKETING,
                "priority": AgentPriority.HIGH,
                "triggers": ["campaign_data_update", "performance_alert"]
            },
            {
                "agent_id": "audience_segmentation_agent",
                "name": "Audience Segmentation Specialist",
                "description": "Creates and manages audience segments for targeted marketing",
                "category": AgentCategory.MARKETING,
                "triggers": ["customer_data_update", "segmentation_request"]
            },
            {
                "agent_id": "conversion_optimizer",
                "name": "Conversion Rate Optimizer",
                "description": "Analyzes and optimizes conversion funnels",
                "category": AgentCategory.MARKETING,
                "priority": AgentPriority.HIGH,
                "triggers": ["conversion_data_update", "funnel_analysis"]
            },
            {
                "agent_id": "roi_calculator",
                "name": "Marketing ROI Calculator",
                "description": "Calculates and tracks marketing return on investment",
                "category": AgentCategory.ANALYTICS,
                "triggers": ["campaign_completed", "roi_analysis_request"]
            },
            {
                "agent_id": "budget_allocator",
                "name": "Marketing Budget Allocator",
                "description": "Optimizes marketing budget allocation across channels",
                "category": AgentCategory.MARKETING,
                "priority": AgentPriority.HIGH,
                "triggers": ["budget_planning", "performance_review"]
            },
            {
                "agent_id": "creative_brief_generator",
                "name": "Creative Brief Generator",
                "description": "Generates detailed creative briefs for marketing materials",
                "category": AgentCategory.CONTENT,
                "triggers": ["creative_request", "campaign_brief_needed"]
            },
            {
                "agent_id": "ab_test_manager",
                "name": "A/B Test Manager",
                "description": "Designs, manages, and analyzes A/B tests",
                "category": AgentCategory.MARKETING,
                "triggers": ["ab_test_request", "test_results_ready"]
            },
            {
                "agent_id": "seasonal_campaign_planner",
                "name": "Seasonal Campaign Planner",
                "description": "Plans and schedules seasonal marketing campaigns",
                "category": AgentCategory.MARKETING,
                "triggers": ["season_approaching", "holiday_planning"]
            }
        ]
        
        # SEO Agents (8 agents)
        seo_agents = [
            {
                "agent_id": "keyword_researcher",
                "name": "Keyword Research Specialist",
                "description": "Conducts comprehensive keyword research and analysis",
                "category": AgentCategory.SEO,
                "triggers": ["seo_audit_request", "content_planning"]
            },
            {
                "agent_id": "content_optimizer",
                "name": "SEO Content Optimizer",
                "description": "Optimizes content for search engine visibility",
                "category": AgentCategory.SEO,
                "priority": AgentPriority.HIGH,
                "triggers": ["content_created", "seo_optimization_request"]
            },
            {
                "agent_id": "technical_seo_auditor",
                "name": "Technical SEO Auditor",
                "description": "Performs technical SEO audits and provides recommendations",
                "category": AgentCategory.SEO,
                "triggers": ["website_audit_request", "technical_issues_detected"]
            },
            {
                "agent_id": "backlink_analyzer",
                "name": "Backlink Analysis Agent",
                "description": "Analyzes backlink profiles and identifies opportunities",
                "category": AgentCategory.SEO,
                "triggers": ["backlink_analysis_request", "monthly_seo_review"]
            },
            {
                "agent_id": "local_seo_optimizer",
                "name": "Local SEO Optimizer",
                "description": "Optimizes local search presence and Google My Business",
                "category": AgentCategory.SEO,
                "triggers": ["local_seo_request", "location_update"]
            },
            {
                "agent_id": "serp_tracker",
                "name": "SERP Position Tracker",
                "description": "Tracks search engine ranking positions and changes",
                "category": AgentCategory.SEO,
                "triggers": ["daily_rank_check", "ranking_alert"]
            },
            {
                "agent_id": "schema_markup_generator",
                "name": "Schema Markup Generator",
                "description": "Generates and implements schema markup for better SERP visibility",
                "category": AgentCategory.SEO,
                "triggers": ["schema_request", "structured_data_needed"]
            },
            {
                "agent_id": "seo_report_generator",
                "name": "SEO Report Generator",
                "description": "Generates comprehensive SEO performance reports",
                "category": AgentCategory.SEO,
                "triggers": ["monthly_report", "seo_report_request"]
            }
        ]
        
        # Content Agents (8 agents)
        content_agents = [
            {
                "agent_id": "blog_writer",
                "name": "AI Blog Writer",
                "description": "Creates high-quality, SEO-optimized blog posts",
                "category": AgentCategory.CONTENT,
                "triggers": ["blog_content_request", "content_calendar_scheduled"]
            },
            {
                "agent_id": "social_media_creator",
                "name": "Social Media Content Creator",
                "description": "Creates engaging social media posts and campaigns",
                "category": AgentCategory.SOCIAL_MEDIA,
                "triggers": ["social_post_request", "social_calendar_scheduled"]
            },
            {
                "agent_id": "email_copywriter",
                "name": "Email Marketing Copywriter",
                "description": "Creates compelling email marketing content",
                "category": AgentCategory.EMAIL_MARKETING,
                "triggers": ["email_campaign_request", "newsletter_scheduled"]
            },
            {
                "agent_id": "landing_page_optimizer",
                "name": "Landing Page Copy Optimizer",
                "description": "Creates and optimizes landing page copy for conversions",
                "category": AgentCategory.CONTENT,
                "priority": AgentPriority.HIGH,
                "triggers": ["landing_page_request", "conversion_optimization"]
            },
            {
                "agent_id": "video_script_writer",
                "name": "Video Script Writer",
                "description": "Creates engaging video scripts for marketing content",
                "category": AgentCategory.CONTENT,
                "triggers": ["video_content_request", "script_needed"]
            },
            {
                "agent_id": "content_calendar_manager",
                "name": "Content Calendar Manager",
                "description": "Plans and manages content calendars across all channels",
                "category": AgentCategory.CONTENT,
                "triggers": ["calendar_planning", "content_schedule_update"]
            },
            {
                "agent_id": "content_repurposer",
                "name": "Content Repurposing Agent",
                "description": "Repurposes existing content across different formats and channels",
                "category": AgentCategory.CONTENT,
                "triggers": ["content_repurpose_request", "multi_channel_distribution"]
            },
            {
                "agent_id": "content_quality_checker",
                "name": "Content Quality Assurance",
                "description": "Reviews and ensures content quality and brand consistency",
                "category": AgentCategory.CONTENT,
                "triggers": ["content_review_needed", "quality_check_request"]
            }
        ]
        
        # Analytics & Monitoring Agents (6 agents)
        analytics_agents = [
            {
                "agent_id": "performance_analyzer",
                "name": "Performance Analytics Agent",
                "description": "Analyzes marketing performance across all channels",
                "category": AgentCategory.ANALYTICS,
                "priority": AgentPriority.HIGH,
                "triggers": ["daily_analytics", "performance_alert"]
            },
            {
                "agent_id": "customer_journey_analyzer",
                "name": "Customer Journey Analyzer",
                "description": "Maps and analyzes customer journeys and touchpoints",
                "category": AgentCategory.ANALYTICS,
                "triggers": ["journey_analysis_request", "customer_behavior_update"]
            },
            {
                "agent_id": "attribution_modeler",
                "name": "Marketing Attribution Modeler",
                "description": "Models marketing attribution across touchpoints",
                "category": AgentCategory.ANALYTICS,
                "triggers": ["attribution_analysis", "conversion_tracking"]
            },
            {
                "agent_id": "predictive_analyzer",
                "name": "Predictive Analytics Agent",
                "description": "Provides predictive insights for marketing decisions",
                "category": AgentCategory.ANALYTICS,
                "priority": AgentPriority.HIGH,
                "triggers": ["prediction_request", "trend_analysis"]
            },
            {
                "agent_id": "real_time_monitor",
                "name": "Real-time Performance Monitor",
                "description": "Monitors real-time marketing performance and alerts",
                "category": AgentCategory.MONITORING,
                "priority": AgentPriority.CRITICAL,
                "triggers": ["performance_threshold", "real_time_alert"]
            },
            {
                "agent_id": "report_automator",
                "name": "Automated Report Generator",
                "description": "Generates automated performance reports and insights",
                "category": AgentCategory.ANALYTICS,
                "triggers": ["scheduled_report", "report_request"]
            }
        ]
        
        # Lead Generation & Customer Service Agents (6 agents)
        lead_service_agents = [
            {
                "agent_id": "lead_scorer",
                "name": "AI Lead Scoring Agent",
                "description": "Scores and qualifies leads based on behavior and data",
                "category": AgentCategory.LEAD_GENERATION,
                "priority": AgentPriority.HIGH,
                "triggers": ["new_lead", "lead_activity_update"]
            },
            {
                "agent_id": "chatbot_trainer",
                "name": "Customer Service Chatbot",
                "description": "Provides AI-powered customer service and support",
                "category": AgentCategory.CUSTOMER_SERVICE,
                "triggers": ["customer_inquiry", "support_request"]
            },
            {
                "agent_id": "lead_nurture_agent",
                "name": "Lead Nurturing Specialist",
                "description": "Creates and manages lead nurturing workflows",
                "category": AgentCategory.LEAD_GENERATION,
                "triggers": ["lead_scored", "nurture_sequence_trigger"]
            },
            {
                "agent_id": "customer_feedback_analyzer",
                "name": "Customer Feedback Analyzer",
                "description": "Analyzes customer feedback and sentiment",
                "category": AgentCategory.CUSTOMER_SERVICE,
                "triggers": ["feedback_received", "review_posted"]
            },
            {
                "agent_id": "retention_optimizer",
                "name": "Customer Retention Optimizer",
                "description": "Identifies at-risk customers and creates retention strategies",
                "category": AgentCategory.CUSTOMER_SERVICE,
                "priority": AgentPriority.HIGH,
                "triggers": ["churn_risk_detected", "retention_analysis"]
            },
            {
                "agent_id": "upsell_identifier",
                "name": "Upsell Opportunity Identifier",
                "description": "Identifies upselling and cross-selling opportunities",
                "category": AgentCategory.LEAD_GENERATION,
                "triggers": ["customer_behavior_change", "product_usage_analysis"]
            }
        ]
        
        # Infrastructure & Security Agents (5 agents)
        infrastructure_agents = [
            {
                "agent_id": "system_health_monitor",
                "name": "System Health Monitor",
                "description": "Monitors system health and performance metrics",
                "category": AgentCategory.INFRASTRUCTURE,
                "priority": AgentPriority.CRITICAL,
                "triggers": ["health_check_scheduled", "system_alert"]
            },
            {
                "agent_id": "security_monitor",
                "name": "Security Monitoring Agent",
                "description": "Monitors security threats and vulnerabilities",
                "category": AgentCategory.SECURITY,
                "priority": AgentPriority.CRITICAL,
                "triggers": ["security_scan", "threat_detected"]
            },
            {
                "agent_id": "backup_manager",
                "name": "Automated Backup Manager",
                "description": "Manages automated backups and disaster recovery",
                "category": AgentCategory.INFRASTRUCTURE,
                "triggers": ["backup_scheduled", "disaster_recovery_test"]
            },
            {
                "agent_id": "resource_optimizer",
                "name": "Resource Usage Optimizer",
                "description": "Optimizes system resource usage and costs",
                "category": AgentCategory.INFRASTRUCTURE,
                "triggers": ["resource_analysis", "cost_optimization"]
            },
            {
                "agent_id": "deployment_manager",
                "name": "Automated Deployment Manager",
                "description": "Manages automated deployments and updates",
                "category": AgentCategory.INFRASTRUCTURE,
                "priority": AgentPriority.HIGH,
                "triggers": ["deployment_request", "update_available"]
            }
        ]
        
        # E-commerce Agents (12 agents)
        ecommerce_agents = [
            {
                "agent_id": "product_sourcing_specialist",
                "name": "Product Sourcing Specialist",
                "description": "AI Product Sourcing Specialist for intelligent product discovery and validation",
                "category": AgentCategory.ECOMMERCE,
                "priority": AgentPriority.HIGH,
                "triggers": ["product_sourcing_request", "market_research"]
            },
            {
                "agent_id": "price_optimization_specialist",
                "name": "Price Optimization Specialist",
                "description": "Dynamic pricing optimization for maximum profitability",
                "category": AgentCategory.ECOMMERCE,
                "priority": AgentPriority.HIGH,
                "triggers": ["price_analysis_request", "competitor_price_change"]
            },
            {
                "agent_id": "inventory_management_specialist",
                "name": "Inventory Management Specialist",
                "description": "AI-powered demand forecasting and inventory optimization",
                "category": AgentCategory.ECOMMERCE,
                "triggers": ["inventory_analysis", "stock_level_alert"]
            },
            {
                "agent_id": "supplier_relations_specialist",
                "name": "Supplier Relations Specialist",
                "description": "Vendor management and supplier relationship optimization",
                "category": AgentCategory.ECOMMERCE,
                "triggers": ["supplier_evaluation", "vendor_performance_review"]
            },
            {
                "agent_id": "fraud_detection_specialist",
                "name": "Fraud Detection Specialist",
                "description": "E-commerce fraud detection and security monitoring",
                "category": AgentCategory.SECURITY,
                "priority": AgentPriority.CRITICAL,
                "triggers": ["transaction_analysis", "fraud_alert"]
            },
            {
                "agent_id": "customer_segmentation_specialist",
                "name": "Customer Segmentation Specialist",
                "description": "Advanced customer segmentation for targeted e-commerce marketing",
                "category": AgentCategory.ECOMMERCE,
                "triggers": ["customer_analysis", "segmentation_request"]
            },
            {
                "agent_id": "sales_forecasting_specialist",
                "name": "Sales Forecasting Specialist",
                "description": "Predictive sales analytics and forecasting",
                "category": AgentCategory.ANALYTICS,
                "triggers": ["sales_forecast_request", "trend_analysis"]
            },
            {
                "agent_id": "aso_specialist",
                "name": "App Store Optimization Specialist",
                "description": "Mobile app store optimization and visibility enhancement",
                "category": AgentCategory.ECOMMERCE,
                "triggers": ["aso_analysis_request", "app_performance_review"]
            },
            {
                "agent_id": "amazon_optimization_specialist",
                "name": "Amazon Optimization Specialist",
                "description": "Amazon marketplace optimization and listing enhancement",
                "category": AgentCategory.ECOMMERCE,
                "priority": AgentPriority.HIGH,
                "triggers": ["amazon_listing_optimization", "marketplace_analysis"]
            },
            {
                "agent_id": "ecommerce_platform_integration_specialist",
                "name": "E-commerce Platform Integration Specialist",
                "description": "Multi-platform e-commerce integration and synchronization",
                "category": AgentCategory.ECOMMERCE,
                "triggers": ["platform_sync_request", "integration_setup"]
            },
            {
                "agent_id": "review_management_specialist",
                "name": "Review Management Specialist",
                "description": "Customer review and reputation management optimization",
                "category": AgentCategory.CUSTOMER_SERVICE,
                "triggers": ["review_analysis", "reputation_monitoring"]
            },
            {
                "agent_id": "conversion_optimization_specialist",
                "name": "Conversion Rate Optimization Specialist",
                "description": "E-commerce conversion rate optimization and sales maximization",
                "category": AgentCategory.ECOMMERCE,
                "priority": AgentPriority.HIGH,
                "triggers": ["conversion_analysis", "funnel_optimization"]
            }
        ]
        
        # Combine all agents
        all_agents = (
            marketing_agents + seo_agents + content_agents + 
            analytics_agents + lead_service_agents + infrastructure_agents + ecommerce_agents
        )
        
        # Initialize agent registry
        for agent_data in all_agents:
            agent_config = AIAgentConfig(**agent_data)
            self.agent_registry[agent_config.agent_id] = agent_config
        
        self.logger.info(f"Initialized {len(all_agents)} AI agents in registry")
    
    async def get_all_agents(
        self, 
        tenant: Optional[UnifiedTenant] = None,
        category: Optional[AgentCategory] = None,
        status: Optional[AgentStatus] = None
    ) -> List[AIAgentConfig]:
        """Get all agents with optional filtering"""
        agents = list(self.agent_registry.values())
        
        if category:
            agents = [agent for agent in agents if agent.category == category]
        
        # Add runtime status information
        for agent in agents:
            # Get current status from execution history or Redis
            current_status = await self._get_agent_status(agent.agent_id, tenant)
            # Note: We'll add status to the response metadata
        
        return agents
    
    async def get_agent_config(self, agent_id: str) -> Optional[AIAgentConfig]:
        """Get specific agent configuration"""
        return self.agent_registry.get(agent_id)
    
    async def update_agent_config(
        self, 
        agent_id: str, 
        updates: Dict[str, Any],
        tenant: Optional[UnifiedTenant] = None
    ) -> Optional[AIAgentConfig]:
        """Update agent configuration"""
        try:
            agent = self.agent_registry.get(agent_id)
            if not agent:
                return None
            
            # Update configuration
            agent_dict = agent.model_dump()
            agent_dict.update(updates)
            agent_dict['updated_at'] = datetime.now()
            
            updated_agent = AIAgentConfig(**agent_dict)
            self.agent_registry[agent_id] = updated_agent
            
            # Store in Vault if available
            if self.vault_client and tenant:
                vault_path = f"tenants/{tenant.slug}/agents/{agent_id}/config"
                self.vault_client.put_secret(vault_path, agent_dict)
            
            # Publish configuration update event
            if tenant:
                await publish_brain_event(
                    tenant=tenant,
                    event_type="brain.ai.agent_config_updated",
                    data={
                        "agent_id": agent_id,
                        "updates": updates,
                        "timestamp": datetime.now().isoformat()
                    }
                )
            
            self.logger.info(f"Updated agent configuration: {agent_id}")
            return updated_agent
            
        except Exception as e:
            self.logger.error(f"Failed to update agent config: {e}")
            return None
    
    async def execute_agent(
        self,
        agent_id: str,
        tenant: UnifiedTenant,
        input_data: Dict[str, Any],
        triggered_by: Optional[str] = None,
        correlation_id: Optional[str] = None
    ) -> AIAgentExecution:
        """Execute a specific AI agent"""
        try:
            # Get agent configuration
            agent_config = await self.get_agent_config(agent_id)
            if not agent_config:
                raise ValueError(f"Agent not found: {agent_id}")
            
            # Create execution record
            execution = AIAgentExecution(
                agent_id=agent_id,
                tenant_id=tenant.tenant_id,
                status=AgentStatus.RUNNING,
                started_at=datetime.now(),
                input_data=input_data,
                triggered_by=triggered_by,
                correlation_id=correlation_id
            )
            
            # Store execution start
            await self._store_execution(execution)
            
            # Publish agent start event
            await publish_brain_event(
                tenant=tenant,
                event_type=BrainEventTypes.AI_AGENT_TRIGGERED,
                data={
                    "agent_id": agent_id,
                    "execution_id": execution.execution_id,
                    "input_data": input_data,
                    "triggered_by": triggered_by
                }
            )
            
            # TODO: Integrate with actual CrewAI execution
            # This would connect to the CrewAI service at port 8000
            # For now, we'll simulate execution
            await self._simulate_agent_execution(execution, agent_config)
            
            # Update execution record
            execution.completed_at = datetime.now()
            execution.duration_seconds = (
                execution.completed_at - execution.started_at
            ).total_seconds()
            execution.status = AgentStatus.COMPLETED
            
            # Store final execution result
            await self._store_execution(execution)
            
            # Publish completion event
            await publish_ai_agent_result(
                tenant=tenant,
                agent_name=agent_config.name,
                result=execution.output_data,
                execution_time_ms=int(execution.duration_seconds * 1000),
                success=execution.status == AgentStatus.COMPLETED
            )
            
            self.logger.info(
                f"Agent execution completed",
                agent_id=agent_id,
                execution_id=execution.execution_id,
                duration=execution.duration_seconds
            )
            
            return execution
            
        except Exception as e:
            self.logger.error(f"Agent execution failed: {e}")
            
            # Update execution with failure
            execution.status = AgentStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.now()
            await self._store_execution(execution)
            
            # Publish failure event
            await publish_ai_agent_result(
                tenant=tenant,
                agent_name=agent_config.name if agent_config else agent_id,
                result={"error": str(e)},
                execution_time_ms=0,
                success=False
            )
            
            return execution
    
    async def get_agent_metrics(
        self,
        agent_id: str,
        tenant: Optional[UnifiedTenant] = None,
        time_period: str = "24h"
    ) -> AIAgentMetrics:
        """Get performance metrics for an agent"""
        try:
            # Get execution history
            executions = await self._get_execution_history(agent_id, tenant, time_period)
            
            # Calculate metrics
            total_executions = len(executions)
            successful_executions = len([e for e in executions if e.status == AgentStatus.COMPLETED])
            failed_executions = len([e for e in executions if e.status == AgentStatus.FAILED])
            
            success_rate = successful_executions / total_executions if total_executions > 0 else 0.0
            
            durations = [e.duration_seconds for e in executions if e.duration_seconds is not None]
            average_duration = sum(durations) / len(durations) if durations else 0.0
            
            costs = [e.cost_usd for e in executions if e.cost_usd is not None]
            average_cost = sum(costs) / len(costs) if costs else 0.0
            
            tokens = [e.tokens_used for e in executions if e.tokens_used is not None]
            total_tokens = sum(tokens) if tokens else 0
            
            last_execution = max(executions, key=lambda x: x.started_at) if executions else None
            
            return AIAgentMetrics(
                agent_id=agent_id,
                tenant_id=tenant.tenant_id if tenant else None,
                time_period=time_period,
                total_executions=total_executions,
                successful_executions=successful_executions,
                failed_executions=failed_executions,
                average_duration_seconds=average_duration,
                success_rate=success_rate,
                average_cost_usd=average_cost,
                total_tokens_used=total_tokens,
                last_execution_at=last_execution.started_at if last_execution else None,
                status=last_execution.status if last_execution else AgentStatus.IDLE
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get agent metrics: {e}")
            return AIAgentMetrics(agent_id=agent_id, tenant_id=tenant.tenant_id if tenant else None)
    
    async def get_dashboard_data(self, tenant: UnifiedTenant) -> Dict[str, Any]:
        """Get comprehensive dashboard data for tenant"""
        try:
            # Get all agents
            agents = await self.get_all_agents(tenant)
            
            # Get metrics for each category
            category_metrics = {}
            for category in AgentCategory:
                category_agents = [a for a in agents if a.category == category]
                category_metrics[category.value] = {
                    "total_agents": len(category_agents),
                    "enabled_agents": len([a for a in category_agents if a.enabled_by_default])
                }
            
            # Get recent executions
            recent_executions = await self._get_recent_executions(tenant, limit=10)
            
            # Get overall performance metrics
            overall_metrics = await self._get_overall_metrics(tenant)
            
            return {
                "total_agents": len(agents),
                "categories": category_metrics,
                "recent_executions": [e.model_dump() for e in recent_executions],
                "overall_metrics": overall_metrics,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get dashboard data: {e}")
            return {"error": str(e)}
    
    async def _get_agent_status(self, agent_id: str, tenant: Optional[UnifiedTenant]) -> AgentStatus:
        """Get current agent status"""
        # Check Redis for current execution status
        if self.redis_client:
            status_key = f"agent_status:{agent_id}"
            if tenant:
                status_key += f":{tenant.tenant_id}"
            
            status = await self.redis_client.get(status_key)
            if status:
                return AgentStatus(status.decode())
        
        return AgentStatus.IDLE
    
    async def _store_execution(self, execution: AIAgentExecution):
        """Store execution record"""
        if self.redis_client:
            # Store in Redis with TTL
            execution_key = f"agent_execution:{execution.execution_id}"
            await self.redis_client.setex(
                execution_key,
                86400,  # 24 hours TTL
                execution.model_dump_json()
            )
            
            # Update agent status
            status_key = f"agent_status:{execution.agent_id}:{execution.tenant_id}"
            await self.redis_client.setex(status_key, 3600, execution.status.value)
    
    async def _simulate_agent_execution(self, execution: AIAgentExecution, config: AIAgentConfig):
        """Simulate agent execution (replace with actual CrewAI integration)"""
        import random
        
        # Simulate processing time
        await asyncio.sleep(random.uniform(1, 5))
        
        # Simulate output data
        execution.output_data = {
            "result": f"Agent {config.name} executed successfully",
            "processed_items": random.randint(1, 10),
            "recommendations": [
                "Recommendation 1 based on analysis",
                "Recommendation 2 for optimization"
            ]
        }
        
        # Simulate metrics
        execution.tokens_used = random.randint(100, 2000)
        execution.cost_usd = execution.tokens_used * 0.00002  # Approximate cost
        execution.success_rate = random.uniform(0.85, 0.99)
    
    async def _get_execution_history(
        self, 
        agent_id: str, 
        tenant: Optional[UnifiedTenant], 
        time_period: str
    ) -> List[AIAgentExecution]:
        """Get execution history for metrics calculation"""
        # This would typically query from database or Redis
        # For now, return mock data
        return []
    
    async def _get_recent_executions(self, tenant: UnifiedTenant, limit: int = 10) -> List[AIAgentExecution]:
        """Get recent executions for dashboard"""
        # This would query the most recent executions
        return []
    
    async def _get_overall_metrics(self, tenant: UnifiedTenant) -> Dict[str, Any]:
        """Get overall performance metrics for tenant"""
        return {
            "total_executions_today": 0,
            "success_rate_24h": 0.95,
            "average_execution_time": 45.2,
            "total_cost_today": 0.0,
            "active_agents": 0
        }


# Global AI Agents Manager instance
_ai_agents_manager: Optional[AIAgentsManager] = None


def get_ai_agents_manager(vault_client=None, redis_client=None) -> AIAgentsManager:
    """Get or create the global AI Agents Manager"""
    global _ai_agents_manager
    
    if _ai_agents_manager is None:
        _ai_agents_manager = AIAgentsManager(vault_client, redis_client)
    
    return _ai_agents_manager


# Convenience functions for common operations
async def execute_agent_by_name(
    agent_name: str,
    tenant: UnifiedTenant,
    input_data: Dict[str, Any],
    **kwargs
) -> Optional[AIAgentExecution]:
    """Execute agent by name (convenience function)"""
    manager = get_ai_agents_manager()
    
    # Find agent by name
    for agent_id, config in manager.agent_registry.items():
        if config.name.lower() == agent_name.lower():
            return await manager.execute_agent(agent_id, tenant, input_data, **kwargs)
    
    return None


async def get_agents_by_category(category: AgentCategory, tenant: Optional[UnifiedTenant] = None) -> List[AIAgentConfig]:
    """Get all agents in a specific category"""
    manager = get_ai_agents_manager()
    return await manager.get_all_agents(tenant=tenant, category=category)


async def get_tenant_agent_dashboard(tenant: UnifiedTenant) -> Dict[str, Any]:
    """Get complete dashboard data for tenant"""
    manager = get_ai_agents_manager()
    return await manager.get_dashboard_data(tenant)