"""
AI Agents Service - BizoholicSaaS
CrewAI orchestration and AI-powered workflows
Port: 8000
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union
import uuid
import os
from datetime import datetime, timedelta
import logging
import asyncio
import json
from enum import Enum
from dotenv import load_dotenv

# Load environment variables
loaded = load_dotenv()
logging.info(f"Loading .env in ai-agents: {loaded}")
if loaded:
    logging.info(f"Loaded REDIS_URL from env: {os.getenv('REDIS_URL', 'NOT_FOUND')[:20]}...")

# Shared imports with fallbacks
try:
    from shared.database.connection import get_postgres_session, get_redis_client, init_database
    from shared.events.event_bus import EventBus, EventFactory, EventType, event_handler
    from shared.auth.jwt_auth import get_current_user, UserContext, require_permission, Permission
    SHARED_AVAILABLE = True
except ImportError:
    logging.warning("Shared BizOSaas modules not found in main logic. Using Mock setup.")
    SHARED_AVAILABLE = False
    
    class EventBus:
        def __init__(self, *args, **kwargs): pass
        async def initialize(self): pass
        async def start(self): pass
        async def stop(self): pass
        async def publish(self, *args, **kwargs):
            logging.info(f"Mock EventBus: Publishing event {args}")
    
    async def get_redis_client():
        try:
            import redis.asyncio as redis_async
            url = os.getenv("REDIS_URL", "redis://redis:6379/1")
            logging.info(f"Mocking redis connection to {url}")
            client = redis_async.from_url(url, decode_responses=True)
            await client.ping()
            logging.info("Redis ping successful in mock mode")
            return client
        except Exception as e:
            logging.error(f"Failed to connect to Redis in mock mode: {e}")
            # Try to return a client anyway if the error was just the ping
            try:
                import redis.asyncio as redis_async
                return redis_async.from_url(os.getenv("REDIS_URL", "redis://redis:6379/1"), decode_responses=True)
            except:
                return None

    async def init_database(): pass
    def get_current_user(): return None
    class Permission:
        AGENT_EXECUTE = "agent:execute"
    class UserContext:
        def __init__(self):
            self.tenant_id = "default"
            self.user_id = "system"
            
    def require_permission(*args, **kwargs):
        def decorator(func): return func
        return decorator
    def event_handler(*args, **kwargs):
        def decorator(func): return func
        return decorator
    class EventFactory:
        @staticmethod
        def create_system_event(*args, **kwargs): return {"type": "system", "data": kwargs}
        @staticmethod
        def agent_task_started(*args, **kwargs): return {"type": "agent_task_started", "data": kwargs}
        @staticmethod
        def agent_task_completed(*args, **kwargs): return {"type": "agent_task_completed", "data": kwargs}
        @staticmethod
        def agent_task_failed(*args, **kwargs): return {"type": "agent_task_failed", "data": kwargs}
        
    class EventType:
        CAMPAIGN_STARTED = "campaign_started"
        USER_CREATED = "user_created"

# Import chat API
try:
    from chat_api import chat_app, agent_registry, chat_manager
    CHAT_API_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Chat API import failed: {e}. Chat functionality disabled.")
    CHAT_API_AVAILABLE = False

# Centralized BizOSaas AI Agents - using unified business logic layer
try:
    from agents.orchestration import WorkflowEngine, HierarchicalCrewOrchestrator
    from agents.marketing_agents import MarketingStrategistAgent, ContentCreatorAgent, SEOSpecialistAgent
    from agents.ecommerce_agents import EcommerceAgent, ProductSourcingAgent
    from agents.analytics_agents import DigitalPresenceAuditAgent, PerformanceAnalyticsAgent
    from agents.operations_agents import CustomerSupportAgent
    from agents.workflow_crews import DigitalAuditCrew, CampaignLaunchCrew
    
    # Refined 20 Core Agents
    from agents import (
        RefinedMarketResearchAgent,
        RefinedDataAnalyticsAgent,
        RefinedStrategicPlanningAgent,
        RefinedCompetitiveIntelligenceAgent,
        RefinedContentGenerationAgent,
        RefinedCreativeDesignAgent,
        RefinedSEOOptimizationAgent,
        RefinedVideoMarketingAgent,
        RefinedCampaignOrchestrationAgent,
        RefinedConversionOptimizationAgent,
        RefinedSocialMediaManagementAgent,
        RefinedCodeGenerationAgent,
        RefinedDevOpsAutomationAgent,
        RefinedTechnicalDocumentationAgent,
        RefinedCustomerEngagementAgent,
        RefinedSalesIntelligenceAgent,
        RefinedTradingStrategyAgent,
        RefinedFinancialAnalyticsAgent,
        RefinedGamingExperienceAgent,
        RefinedCommunityManagementAgent,
        RefinedMasterOrchestratorAgent,
        RefinedProductSourcingAgent,
        RefinedInventoryManagementAgent,
        RefinedOrderOrchestrationAgent,
        ContentCreationWorkflow,
        MarketingCampaignWorkflow,
        CompetitiveAnalysisWorkflow,
        DevelopmentSprintWorkflow,
        TradingStrategyWorkflow,
        GamingEventWorkflow,
        ECommerceSourcingWorkflow,
        ECommerceOperationsWorkflow,
        ECommerceInventoryLogisticsWorkflow,
        FullDigitalMarketing360Workflow,
        VideoContentMachineWorkflow,
        SEMAdCampaignWorkflow,
        OnboardingStrategyWorkflow,
        RefinedQualityAssuranceAgent,
        RelationExtractionAgent
    )
except ImportError as e:
    logging.warning(f"BizOSaas centralized agents import failed: {e}. Running in mock mode.")
    WorkflowEngine = None
    HierarchicalCrewOrchestrator = None
    MarketingStrategistAgent = None
    EcommerceAgent = None

# Configure logging (moved here so it's available for exception handlers below)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cross-client learning imports
try:
    from agents.cross_client_learning import (
        CrossClientLearningEngine, 
        LearningPatternType, 
        get_cross_client_insights,
        learning_engine
    )
    CROSS_CLIENT_LEARNING_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Cross-client learning import failed: {e}. Learning functionality disabled.")
    CROSS_CLIENT_LEARNING_AVAILABLE = False

app = FastAPI(
    title="BizoSaaS AI Agents",
    description="CrewAI orchestration and AI-powered workflows with Universal Chat Interface for BizoholicSaaS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Chat API
if CHAT_API_AVAILABLE:
    app.mount("/chat", chat_app, name="chat")

# Global variables
event_bus: EventBus = None
redis_client = None
workflow_engine = None
hierarchical_orchestrator = None
digital_audit_crew = None
marketing_strategist = None
ecommerce_agent = None

# Refined Agent Registry
refined_agent_registry = {}

# Enums
class AgentType(str, Enum):
    # Original Agents (Legacy)
    MARKETING_STRATEGIST = "marketing_strategist"
    CAMPAIGN_OPTIMIZER = "campaign_optimizer"
    CONTENT_CREATOR = "content_creator"
    ANALYTICS_SPECIALIST = "analytics_specialist"
    SEO_SPECIALIST = "seo_specialist"
    DIGITAL_AUDITOR = "digital_auditor"
    PERSONAL_ASSISTANT = "personal_assistant"
    ECOMMERCE_SPECIALIST = "ecommerce_specialist"
    SELF_MARKETING = "self_marketing"
    EMAIL_MARKETING_SPECIALIST = "email_marketing_specialist"

    # Refined 20 Core Agents (v2.0)
    # Cat 1: Business Intelligence
    MARKET_RESEARCH = "market_research"
    DATA_ANALYTICS = "data_analytics"
    STRATEGIC_PLANNING = "strategic_planning"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"

    # Cat 2: Content & Creative
    CONTENT_GENERATION = "content_generation"
    CREATIVE_DESIGN = "creative_design"
    SEO_OPTIMIZATION = "seo_optimization"
    VIDEO_MARKETING = "video_marketing"

    # Cat 3: Marketing & Growth
    CAMPAIGN_ORCHESTRATION = "campaign_orchestration"
    CONVERSION_OPTIMIZATION = "conversion_optimization"
    SOCIAL_MEDIA_MANAGEMENT = "social_media_management"

    # Cat 4: Technical
    CODE_GENERATION = "code_generation"
    DEVOPS_AUTOMATION = "devops_automation"
    TECHNICAL_DOCUMENTATION = "technical_documentation"

    # Cat 5: Customer & CRM
    CUSTOMER_ENGAGEMENT = "customer_engagement"
    SALES_INTELLIGENCE = "sales_intelligence"

    # Cat 6: Finance & Trading
    TRADING_STRATEGY = "trading_strategy"
    FINANCIAL_ANALYTICS = "financial_analytics"

    # Cat 7: Gaming & Community
    GAMING_EXPERIENCE = "gaming_experience"
    COMMUNITY_MANAGEMENT = "community_management"

    # Cat 8: Master
    MASTER_ORCHESTRATOR = "master_orchestrator"
    
    # E-commerce Refined
    ECOMM_SOURCING = "ecommerce_sourcing"
    ECOMM_INVENTORY = "ecommerce_inventory"
    ECOMM_ORDER_ORCHESTRATOR = "ecommerce_order_orchestrator"

    # Cat 10: Quality Assurance
    QUALITY_ASSURANCE = "quality_assurance"
    
    # Cat 11: Knowledge & Graph
    RELATION_EXTRACTION = "relation_extraction"

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

# Pydantic models
class AgentTaskRequest(BaseModel):
    agent_type: AgentType
    task_description: str
    input_data: Dict[str, Any]
    priority: TaskPriority = TaskPriority.NORMAL
    timeout_minutes: int = 30
    config: Dict[str, Any] = {}

class AgentTaskResponse(BaseModel):
    task_id: str
    agent_type: AgentType
    task_description: str
    status: WorkflowStatus
    result_data: Dict[str, Any]
    execution_time_seconds: Optional[float]
    cost_estimate: Optional[float]
    error_message: Optional[str]
    tenant_id: str
    created_at: datetime
    updated_at: datetime

class WorkflowRequest(BaseModel):
    workflow_type: str
    company_data: Dict[str, Any]
    objectives: List[str] = []
    budget: Optional[float] = None
    timeline: str = "30 days"
    config: Dict[str, Any] = {}

class WorkflowResponse(BaseModel):
    workflow_id: str
    workflow_type: str
    status: WorkflowStatus
    progress: float  # 0-100
    steps_completed: int
    total_steps: int
    result_data: Dict[str, Any]
    execution_logs: List[Dict[str, Any]]
    tenant_id: str
    created_at: datetime
    updated_at: datetime

class DigitalAuditRequest(BaseModel):
    company: str
    website: str
    email: str
    industry: Optional[str] = None
    competitors: List[str] = []
    audit_depth: str = "comprehensive"  # basic, comprehensive, detailed

class CampaignOptimizationRequest(BaseModel):
    campaign_data: Dict[str, Any]
    current_performance: Dict[str, Any]
    optimization_goals: List[str]
    constraints: Dict[str, Any] = {}

class ContentGenerationRequest(BaseModel):
    content_type: str  # blog_post, social_media, ad_copy, email
    topic: str
    target_audience: str
    keywords: List[str] = []
    tone: str = "professional"
    length: str = "medium"  # short, medium, long

class SEOAnalysisRequest(BaseModel):
    website_url: str
    target_keywords: List[str]
    competitor_urls: List[str] = []
    analysis_type: str = "comprehensive"

class SelfMarketingRequest(BaseModel):
    company_name: str = "BizoholicSaaS"
    target_keywords: List[str] = []
    content_frequency: Dict[str, int] = {}
    marketing_budget: float = 5000.0

class EmailMarketingRequest(BaseModel):
    campaign_type: str = "nurture"  # nurture, promotional, transactional, welcome
    target_audience: str
    email_objective: str
    subject_line_count: int = 5
    content_length: str = "medium"  # short, medium, long
    personalization_level: str = "high"  # low, medium, high
    include_templates: bool = True
    automation_triggers: List[str] = []
    funnel_stage: Optional[str] = None
    brand_voice: str = "professional"  # professional, friendly, urgent, conversational

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database, event bus, and centralized AI agents"""
    global event_bus, redis_client, workflow_engine, hierarchical_orchestrator, digital_audit_crew, marketing_strategist, ecommerce_agent
    
    try:
        # Vault Integration for API Keys
        try:
            import hvac
            vault_addr = os.getenv('VAULT_ADDR')
            vault_token = os.getenv('VAULT_TOKEN')
            
            if vault_addr and vault_token:
                client = hvac.Client(url=vault_addr, token=vault_token)
                if client.is_authenticated():
                    logger.info("Connected to Vault for API keys")
                    # Fetch API keys from Vault
                    secret = client.secrets.kv.v2.read_secret_version(path='platform/ai-agents', mount_point='bizosaas')
                    data = secret['data']['data']
                    
                    # Set environment variables for agents to use
                    if 'openai_api_key' in data:
                        os.environ['OPENAI_API_KEY'] = data['openai_api_key']
                    if 'anthropic_api_key' in data:
                        os.environ['ANTHROPIC_API_KEY'] = data['anthropic_api_key']
                    if 'openrouter_api_key' in data:
                        os.environ['OPENROUTER_API_KEY'] = data['openrouter_api_key']
                else:
                    logger.warning("Vault authentication failed")
            else:
                logger.warning("Vault credentials not provided")
        except Exception as e:
            logger.error(f"Failed to fetch secrets from Vault: {e}")

        await init_database()
        logger.info("Database connections initialized")
        
        redis_client = await get_redis_client()
        
        event_bus = EventBus(redis_client, "ai-agents")
        await event_bus.initialize()
        await event_bus.start()
        logger.info("Event bus initialized")
        
        # Initialize agents
        await setup_centralized_agents()
        
        # Start background task processor
        asyncio.create_task(process_agent_tasks())
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

async def setup_centralized_agents():
    """Initialize all centralized and refined agents in the registry"""
    global workflow_engine, hierarchical_orchestrator, digital_audit_crew, marketing_strategist, ecommerce_agent
    if WorkflowEngine:
        try:
            workflow_engine = WorkflowEngine()
            hierarchical_orchestrator = HierarchicalCrewOrchestrator()
            digital_audit_crew = DigitalAuditCrew()
            marketing_strategist = MarketingStrategistAgent()
            ecommerce_agent = EcommerceAgent()
            
            # Initialize Refined 24 Core Agents
            refined_agent_registry[AgentType.MARKET_RESEARCH.value] = RefinedMarketResearchAgent()
            refined_agent_registry[AgentType.DATA_ANALYTICS.value] = RefinedDataAnalyticsAgent()
            refined_agent_registry[AgentType.STRATEGIC_PLANNING.value] = RefinedStrategicPlanningAgent()
            refined_agent_registry[AgentType.COMPETITIVE_INTELLIGENCE.value] = RefinedCompetitiveIntelligenceAgent()
            refined_agent_registry[AgentType.CONTENT_GENERATION.value] = RefinedContentGenerationAgent()
            refined_agent_registry[AgentType.CREATIVE_DESIGN.value] = RefinedCreativeDesignAgent()
            refined_agent_registry[AgentType.SEO_OPTIMIZATION.value] = RefinedSEOOptimizationAgent()
            refined_agent_registry[AgentType.VIDEO_MARKETING.value] = RefinedVideoMarketingAgent()
            refined_agent_registry[AgentType.CAMPAIGN_ORCHESTRATION.value] = RefinedCampaignOrchestrationAgent()
            refined_agent_registry[AgentType.CONVERSION_OPTIMIZATION.value] = RefinedConversionOptimizationAgent()
            refined_agent_registry[AgentType.SOCIAL_MEDIA_MANAGEMENT.value] = RefinedSocialMediaManagementAgent()
            refined_agent_registry[AgentType.CODE_GENERATION.value] = RefinedCodeGenerationAgent()
            refined_agent_registry[AgentType.DEVOPS_AUTOMATION.value] = RefinedDevOpsAutomationAgent()
            refined_agent_registry[AgentType.TECHNICAL_DOCUMENTATION.value] = RefinedTechnicalDocumentationAgent()
            refined_agent_registry[AgentType.CUSTOMER_ENGAGEMENT.value] = RefinedCustomerEngagementAgent()
            refined_agent_registry[AgentType.SALES_INTELLIGENCE.value] = RefinedSalesIntelligenceAgent()
            refined_agent_registry[AgentType.TRADING_STRATEGY.value] = RefinedTradingStrategyAgent()
            refined_agent_registry[AgentType.FINANCIAL_ANALYTICS.value] = RefinedFinancialAnalyticsAgent()
            refined_agent_registry[AgentType.GAMING_EXPERIENCE.value] = RefinedGamingExperienceAgent()
            refined_agent_registry[AgentType.COMMUNITY_MANAGEMENT.value] = RefinedCommunityManagementAgent()
            refined_agent_registry[AgentType.MASTER_ORCHESTRATOR.value] = RefinedMasterOrchestratorAgent()
            
            # Register E-commerce Refined Agents
            refined_agent_registry[AgentType.ECOMM_SOURCING.value] = RefinedProductSourcingAgent()
            refined_agent_registry[AgentType.ECOMM_INVENTORY.value] = RefinedInventoryManagementAgent()
            refined_agent_registry[AgentType.ECOMM_ORDER_ORCHESTRATOR.value] = RefinedOrderOrchestrationAgent()
            
            # Register QA Agent
            refined_agent_registry[AgentType.QUALITY_ASSURANCE.value] = RefinedQualityAssuranceAgent()
            
            # Register Knowledge Agents
            refined_agent_registry[AgentType.RELATION_EXTRACTION.value] = RelationExtractionAgent()
            
            # Register Refined Workflows
            refined_agent_registry["content_creation_workflow"] = ContentCreationWorkflow()
            refined_agent_registry["marketing_campaign_workflow"] = MarketingCampaignWorkflow()
            refined_agent_registry["competitive_analysis_workflow"] = CompetitiveAnalysisWorkflow()
            refined_agent_registry["development_sprint_workflow"] = DevelopmentSprintWorkflow()
            refined_agent_registry["trading_strategy_workflow"] = TradingStrategyWorkflow()
            refined_agent_registry["gaming_event_workflow"] = GamingEventWorkflow()
            refined_agent_registry["ecommerce_sourcing_workflow"] = ECommerceSourcingWorkflow()
            refined_agent_registry["ecommerce_operations_workflow"] = ECommerceOperationsWorkflow()
            refined_agent_registry["ecommerce_inventory_workflow"] = ECommerceInventoryLogisticsWorkflow()
            refined_agent_registry["digital_marketing_360_workflow"] = FullDigitalMarketing360Workflow()
            refined_agent_registry["video_content_machine_workflow"] = VideoContentMachineWorkflow()
            refined_agent_registry["sem_ad_campaign_workflow"] = SEMAdCampaignWorkflow()
            refined_agent_registry["onboarding_strategy_workflow"] = OnboardingStrategyWorkflow()
            
            logger.info("BizOSaas centralized and refined agents initialized successfully")
        except Exception as e:
            logger.error(f"Agent initialization failed: {e}")
            raise
    else:
        logging.warning("Running in mock mode - BizOSaas centralized agents not available")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown of connections"""
    global event_bus
    
    if event_bus:
        await event_bus.stop()
    logger.info("AI Agents Service shutdown complete")

# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ai-agents",
        "centralized_agents_available": WorkflowEngine is not None,
        "agents_initialized": workflow_engine is not None,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    try:
        async with get_postgres_session("campaign_management") as session:
            await session.execute("SELECT 1")
        
        await redis_client.ping()
        
        return {
            "status": "ready",
            "service": "ai-agents",
            "centralized_agents_initialized": workflow_engine is not None,
            "orchestrator_ready": hierarchical_orchestrator is not None,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )

# Agent information endpoints
@app.get("/agents")
async def list_available_agents(
    current_user: UserContext = Depends(get_current_user)
):
    """List available AI agents and their capabilities"""
    
    agents = [
        {
            "type": AgentType.MARKETING_STRATEGIST.value,
            "name": "Marketing Strategist",
            "description": "Develops comprehensive marketing strategies and campaigns",
            "capabilities": ["strategy_development", "market_analysis", "competitor_research"],
            "estimated_cost_per_task": 0.50
        },
        {
            "type": AgentType.CAMPAIGN_OPTIMIZER.value,
            "name": "Campaign Optimizer",
            "description": "Optimizes existing marketing campaigns for better performance",
            "capabilities": ["performance_analysis", "budget_optimization", "targeting_refinement"],
            "estimated_cost_per_task": 0.30
        },
        {
            "type": AgentType.CONTENT_CREATOR.value,
            "name": "Content Creator",
            "description": "Generates high-quality marketing content across various formats",
            "capabilities": ["blog_writing", "ad_copy", "social_media_content", "email_campaigns"],
            "estimated_cost_per_task": 0.25
        },
        {
            "type": AgentType.ANALYTICS_SPECIALIST.value,
            "name": "Analytics Specialist",
            "description": "Analyzes marketing data and provides actionable insights",
            "capabilities": ["data_analysis", "report_generation", "trend_identification"],
            "estimated_cost_per_task": 0.35
        },
        {
            "type": AgentType.SEO_SPECIALIST.value,
            "name": "SEO Specialist",
            "description": "Optimizes websites and content for search engines",
            "capabilities": ["keyword_research", "on_page_seo", "technical_seo", "content_optimization"],
            "estimated_cost_per_task": 0.40
        },
        {
            "type": AgentType.DIGITAL_AUDITOR.value,
            "name": "Digital Presence Auditor",
            "description": "Conducts comprehensive audits of digital marketing presence",
            "capabilities": ["website_audit", "social_media_audit", "competitor_analysis"],
            "estimated_cost_per_task": 0.60
        },
        {
            "type": AgentType.ECOMMERCE_SPECIALIST.value,
            "name": "E-commerce Specialist",
            "description": "Specialized in e-commerce marketing and optimization",
            "capabilities": ["product_optimization", "conversion_optimization", "marketplace_strategies"],
            "estimated_cost_per_task": 0.45
        },
        {
            "type": AgentType.SELF_MARKETING.value,
            "name": "Self-Marketing Agent",
            "description": "Handles automated marketing for the BizoholicSaaS platform itself",
            "capabilities": ["content_automation", "seo_optimization", "social_media_management"],
            "estimated_cost_per_task": 0.20
        },
        {
            "type": AgentType.EMAIL_MARKETING_SPECIALIST.value,
            "name": "Email Marketing Specialist",
            "description": "Specialized AI agent for email marketing campaigns, automation, and optimization",
            "capabilities": ["email_campaign_creation", "subject_line_optimization", "automation_workflows", "behavioral_triggers", "a_b_testing", "personalization", "deliverability_optimization"],
            "estimated_cost_per_task": 0.35
        }
    ]
    
    return {
        "available_agents": agents,
        "total_agents": len(agents),
        "agents_status": "operational" if workflow_engine else "mock_mode",
        "centralized_system": True,
        "orchestrator_available": hierarchical_orchestrator is not None
    }

# Single agent task endpoints
@app.post("/tasks", response_model=AgentTaskResponse)
async def execute_agent_task(
    task_request: AgentTaskRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.AGENT_EXECUTE))
):
    """Execute a single AI agent task"""
    
    try:
        task_id = str(uuid.uuid4())
        
        # Store task in Redis for tracking
        task_data = {
            "task_id": task_id,
            "agent_type": task_request.agent_type.value,
            "task_description": task_request.task_description,
            "input_data": task_request.input_data,
            "priority": task_request.priority.value,
            "status": WorkflowStatus.PENDING.value,
            "tenant_id": current_user.tenant_id,
            "user_id": current_user.user_id,
            "created_at": datetime.utcnow().isoformat(),
            "config": task_request.config
        }
        
        await redis_client.hset(f"agent_task:{task_id}", mapping=task_data)
        await redis_client.expire(f"agent_task:{task_id}", 86400 * 7)  # 7 days TTL
        
        # Add to processing queue
        queue_name = f"agent_queue:{task_request.priority.value}"
        await redis_client.lpush(queue_name, task_id)
        
        # Publish task started event
        event = EventFactory.agent_task_started(
            tenant_id=current_user.tenant_id,
            task_id=task_id,
            agent_name=task_request.agent_type.value,
            task_data={
                "description": task_request.task_description,
                "priority": task_request.priority.value,
                "input_size": len(str(task_request.input_data))
            }
        )
        await event_bus.publish(event)
        
        return AgentTaskResponse(
            task_id=task_id,
            agent_type=task_request.agent_type,
            task_description=task_request.task_description,
            status=WorkflowStatus.PENDING,
            result_data={},
            execution_time_seconds=None,
            cost_estimate=get_cost_estimate(task_request.agent_type),
            error_message=None,
            tenant_id=current_user.tenant_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Execute agent task error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to execute agent task"
        )

def get_cost_estimate(agent_type: AgentType) -> float:
    """Get cost estimate for agent type"""
    
    cost_map = {
        AgentType.MARKETING_STRATEGIST: 0.50,
        AgentType.CAMPAIGN_OPTIMIZER: 0.30,
        AgentType.CONTENT_CREATOR: 0.25,
        AgentType.ANALYTICS_SPECIALIST: 0.35,
        AgentType.SEO_SPECIALIST: 0.40,
        AgentType.DIGITAL_AUDITOR: 0.60,
        AgentType.ECOMMERCE_SPECIALIST: 0.45,
        AgentType.SELF_MARKETING: 0.20,
        AgentType.EMAIL_MARKETING_SPECIALIST: 0.35
    }
    
    return cost_map.get(agent_type, 0.35)

@app.get("/tasks/{task_id}", response_model=AgentTaskResponse)
async def get_agent_task_status(
    task_id: str,
    current_user: UserContext = Depends(get_current_user)
):
    """Get status of an agent task"""
    
    try:
        # Get task data from Redis
        task_data = await redis_client.hgetall(f"agent_task:{task_id}")
        
        if not task_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Check tenant access
        if task_data.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return AgentTaskResponse(
            task_id=task_id,
            agent_type=AgentType(task_data["agent_type"]),
            task_description=task_data["task_description"],
            status=WorkflowStatus(task_data["status"]),
            result_data=json.loads(task_data.get("result_data", "{}")),
            execution_time_seconds=float(task_data["execution_time_seconds"]) if task_data.get("execution_time_seconds") else None,
            cost_estimate=float(task_data.get("cost_estimate", "0")),
            error_message=task_data.get("error_message"),
            tenant_id=task_data["tenant_id"],
            created_at=datetime.fromisoformat(task_data["created_at"]),
            updated_at=datetime.fromisoformat(task_data.get("updated_at", task_data["created_at"]))
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get agent task status error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get task status"
        )

@app.get("/tasks", response_model=List[AgentTaskResponse])
async def list_agent_tasks(
    current_user: UserContext = Depends(get_current_user),
    status_filter: Optional[WorkflowStatus] = None,
    limit: int = 50
):
    """List agent tasks for current tenant"""
    
    try:
        # Get task keys for tenant
        pattern = f"agent_task:*"
        task_keys = await redis_client.keys(pattern)
        
        tasks = []
        for key in task_keys[:limit]:  # Limit to prevent memory issues
            task_data = await redis_client.hgetall(key)
            
            # Filter by tenant
            if task_data.get("tenant_id") != current_user.tenant_id:
                continue
            
            # Filter by status if specified
            if status_filter and task_data.get("status") != status_filter.value:
                continue
            
            task_id = key.split(":")[-1]
            tasks.append(AgentTaskResponse(
                task_id=task_id,
                agent_type=AgentType(task_data["agent_type"]),
                task_description=task_data["task_description"],
                status=WorkflowStatus(task_data["status"]),
                result_data=json.loads(task_data.get("result_data", "{}")),
                execution_time_seconds=float(task_data["execution_time_seconds"]) if task_data.get("execution_time_seconds") else None,
                cost_estimate=float(task_data.get("cost_estimate", "0")),
                error_message=task_data.get("error_message"),
                tenant_id=task_data["tenant_id"],
                created_at=datetime.fromisoformat(task_data["created_at"]),
                updated_at=datetime.fromisoformat(task_data.get("updated_at", task_data["created_at"]))
            ))
        
        # Sort by creation time (newest first)
        tasks.sort(key=lambda x: x.created_at, reverse=True)
        
        return tasks
        
    except Exception as e:
        logger.error(f"List agent tasks error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list tasks"
        )

# Specialized agent endpoints
@app.post("/agents/digital-audit")
async def digital_presence_audit(
    audit_request: DigitalAuditRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.AGENT_EXECUTE))
):
    """Conduct comprehensive digital presence audit"""
    
    try:
        task_request = AgentTaskRequest(
            agent_type=AgentType.DIGITAL_AUDITOR,
            task_description=f"Digital presence audit for {audit_request.company}",
            input_data={
                "company": audit_request.company,
                "website": audit_request.website,
                "email": audit_request.email,
                "industry": audit_request.industry,
                "competitors": audit_request.competitors,
                "audit_depth": audit_request.audit_depth
            },
            priority=TaskPriority.HIGH
        )
        
        return await execute_agent_task(task_request, background_tasks, current_user)
        
    except Exception as e:
        logger.error(f"Digital presence audit error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start digital presence audit"
        )

@app.post("/agents/campaign-optimize")
async def optimize_campaign(
    optimization_request: CampaignOptimizationRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.AGENT_EXECUTE))
):
    """Optimize marketing campaign using AI"""
    
    try:
        task_request = AgentTaskRequest(
            agent_type=AgentType.CAMPAIGN_OPTIMIZER,
            task_description="AI-powered campaign optimization",
            input_data={
                "campaign_data": optimization_request.campaign_data,
                "current_performance": optimization_request.current_performance,
                "optimization_goals": optimization_request.optimization_goals,
                "constraints": optimization_request.constraints
            },
            priority=TaskPriority.HIGH
        )
        
        return await execute_agent_task(task_request, background_tasks, current_user)
        
    except Exception as e:
        logger.error(f"Campaign optimization error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start campaign optimization"
        )

@app.post("/agents/content-generate")
async def generate_content(
    content_request: ContentGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.AGENT_EXECUTE))
):
    """Generate marketing content using AI"""
    
    try:
        task_request = AgentTaskRequest(
            agent_type=AgentType.CONTENT_CREATOR,
            task_description=f"Generate {content_request.content_type} content about {content_request.topic}",
            input_data={
                "content_type": content_request.content_type,
                "topic": content_request.topic,
                "target_audience": content_request.target_audience,
                "keywords": content_request.keywords,
                "tone": content_request.tone,
                "length": content_request.length
            },
            priority=TaskPriority.NORMAL
        )
        
        return await execute_agent_task(task_request, background_tasks, current_user)
        
    except Exception as e:
        logger.error(f"Content generation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start content generation"
        )

@app.post("/agents/seo-analyze")
async def analyze_seo(
    seo_request: SEOAnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.AGENT_EXECUTE))
):
    """Perform SEO analysis using AI"""
    
    try:
        task_request = AgentTaskRequest(
            agent_type=AgentType.SEO_SPECIALIST,
            task_description=f"SEO analysis for {seo_request.website_url}",
            input_data={
                "website_url": seo_request.website_url,
                "target_keywords": seo_request.target_keywords,
                "competitor_urls": seo_request.competitor_urls,
                "analysis_type": seo_request.analysis_type
            },
            priority=TaskPriority.NORMAL
        )
        
        return await execute_agent_task(task_request, background_tasks, current_user)
        
    except Exception as e:
        logger.error(f"SEO analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start SEO analysis"
        )

@app.post("/agents/email-marketing")
async def create_email_marketing(
    email_request: EmailMarketingRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.AGENT_EXECUTE))
):
    """Create email marketing campaigns and automation using AI"""
    
    try:
        task_request = AgentTaskRequest(
            agent_type=AgentType.EMAIL_MARKETING_SPECIALIST,
            task_description=f"Email marketing campaign creation: {email_request.campaign_type} for {email_request.target_audience}",
            input_data={
                "campaign_type": email_request.campaign_type,
                "target_audience": email_request.target_audience,
                "email_objective": email_request.email_objective,
                "subject_line_count": email_request.subject_line_count,
                "content_length": email_request.content_length,
                "personalization_level": email_request.personalization_level,
                "include_templates": email_request.include_templates,
                "automation_triggers": email_request.automation_triggers,
                "funnel_stage": email_request.funnel_stage,
                "brand_voice": email_request.brand_voice
            },
            priority=TaskPriority.HIGH
        )
        
        return await execute_agent_task(task_request, background_tasks, current_user)
        
    except Exception as e:
        logger.error(f"Email marketing creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start email marketing creation"
        )

@app.post("/agents/email-funnel-sync")
async def sync_email_with_funnel(
    funnel_id: str,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.AGENT_EXECUTE))
):
    """Sync email content generation with sales funnel stages"""
    
    try:
        # This endpoint integrates with the Campaign Management Service funnel
        task_request = AgentTaskRequest(
            agent_type=AgentType.EMAIL_MARKETING_SPECIALIST,
            task_description=f"Generate email content for sales funnel: {funnel_id}",
            input_data={
                "campaign_type": "funnel_integration",
                "funnel_id": funnel_id,
                "generate_for_all_stages": True,
                "personalization_level": "high",
                "include_behavioral_triggers": True,
                "optimization_focus": "conversion"
            },
            priority=TaskPriority.HIGH,
            config={
                "integrate_with_mautic": True,
                "tenant_id": current_user.tenant_id
            }
        )
        
        return await execute_agent_task(task_request, background_tasks, current_user)
        
    except Exception as e:
        logger.error(f"Email funnel sync error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sync email with funnel"
        )

# Workflow orchestration endpoints
@app.post("/workflows", response_model=WorkflowResponse)
async def create_workflow(
    workflow_request: WorkflowRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.AGENT_EXECUTE))
):
    """Create and execute a multi-agent workflow"""
    
    try:
        workflow_id = str(uuid.uuid4())
        
        # Store workflow data
        workflow_data = {
            "workflow_id": workflow_id,
            "workflow_type": workflow_request.workflow_type,
            "company_data": workflow_request.company_data,
            "objectives": workflow_request.objectives,
            "budget": workflow_request.budget,
            "timeline": workflow_request.timeline,
            "config": workflow_request.config,
            "status": WorkflowStatus.PENDING.value,
            "progress": 0.0,
            "steps_completed": 0,
            "total_steps": get_workflow_steps_count(workflow_request.workflow_type),
            "result_data": {},
            "execution_logs": [],
            "tenant_id": current_user.tenant_id,
            "user_id": current_user.user_id,
            "created_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hset(f"workflow:{workflow_id}", mapping={
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in workflow_data.items()
        })
        await redis_client.expire(f"workflow:{workflow_id}", 86400 * 7)  # 7 days TTL
        
        # Start workflow execution
        background_tasks.add_task(execute_workflow, workflow_id)
        
        return WorkflowResponse(
            workflow_id=workflow_id,
            workflow_type=workflow_request.workflow_type,
            status=WorkflowStatus.PENDING,
            progress=0.0,
            steps_completed=0,
            total_steps=workflow_data["total_steps"],
            result_data={},
            execution_logs=[],
            tenant_id=current_user.tenant_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Create workflow error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create workflow"
        )

def get_workflow_steps_count(workflow_type: str) -> int:
    """Get number of steps for workflow type"""
    
    step_counts = {
        "client_onboarding": 5,
        "campaign_development": 7,
        "comprehensive_audit": 8,
        "seo_optimization": 6,
        "content_marketing": 4,
        "self_marketing": 3
    }
    
    return step_counts.get(workflow_type, 5)

async def execute_workflow(workflow_id: str):
    """Background task to execute multi-agent workflow"""
    
    try:
        # Get workflow data
        workflow_data_raw = await redis_client.hgetall(f"workflow:{workflow_id}")
        if not workflow_data_raw:
            logger.error(f"Workflow not found: {workflow_id}")
            return
        
        # Parse workflow data
        workflow_data = {
            k: json.loads(v) if k in ["company_data", "objectives", "config", "result_data", "execution_logs"] else v
            for k, v in workflow_data_raw.items()
        }
        
        workflow_type = workflow_data["workflow_type"]
        
        # Update status to running
        await update_workflow_status(workflow_id, WorkflowStatus.RUNNING, 0)
        
        # Execute workflow based on type
        if hierarchical_orchestrator and workflow_type in ["client_onboarding", "campaign_development"]:
            result = await execute_hierarchical_workflow(workflow_id, workflow_data)
        else:
            result = await execute_custom_workflow(workflow_id, workflow_data)
        
        # Update final status
        if result["success"]:
            await update_workflow_status(workflow_id, WorkflowStatus.COMPLETED, 100, result["data"])
        else:
            await update_workflow_status(workflow_id, WorkflowStatus.FAILED, workflow_data.get("progress", 0))
        
    except Exception as e:
        logger.error(f"Execute workflow error: {e}")
        await update_workflow_status(workflow_id, WorkflowStatus.FAILED, 0)

async def execute_hierarchical_workflow(workflow_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute workflow using hierarchical crew orchestrator"""
    
    try:
        workflow_type = workflow_data["workflow_type"]
        company_data = workflow_data["company_data"]
        
        if workflow_type == "client_onboarding":
            # Simulate hierarchical crew execution
            await asyncio.sleep(5)  # Simulate processing time
            
            result_data = {
                "onboarding_complete": True,
                "recommendations": [
                    "Set up Google Ads account with proper tracking",
                    "Implement conversion tracking across all channels",
                    "Create branded social media profiles",
                    "Develop content calendar for next 30 days"
                ],
                "next_steps": [
                    "Campaign strategy development",
                    "Content creation workflow setup",
                    "Analytics dashboard configuration"
                ]
            }
            
            await update_workflow_progress(workflow_id, 100, 5, result_data)
            
            return {"success": True, "data": result_data}
            
        elif workflow_type == "campaign_development":
            # Simulate campaign development workflow
            steps = [
                ("Market research", 15),
                ("Competitor analysis", 30),
                ("Strategy development", 50),
                ("Creative brief creation", 70),
                ("Budget allocation", 85),
                ("Campaign setup", 95),
                ("Final review", 100)
            ]
            
            for i, (step_name, progress) in enumerate(steps):
                await asyncio.sleep(2)  # Simulate work
                
                step_result = {
                    "step": step_name,
                    "completed_at": datetime.utcnow().isoformat(),
                    "data": f"Completed {step_name.lower()}"
                }
                
                await update_workflow_progress(workflow_id, progress, i + 1, {"current_step": step_result})
            
            final_result = {
                "campaign_strategy": {
                    "primary_channels": ["Google Ads", "Facebook Ads", "LinkedIn Ads"],
                    "budget_allocation": {
                        "google_ads": 50,
                        "facebook_ads": 30,
                        "linkedin_ads": 20
                    },
                    "target_audience": "Business owners aged 35-55",
                    "key_messages": ["Grow your business with AI", "Automate your marketing"]
                },
                "success_metrics": {
                    "target_roas": 4.0,
                    "cpa_target": 75.0,
                    "conversion_rate_target": 3.5
                }
            }
            
            return {"success": True, "data": final_result}
        
        return {"success": False, "error": "Unsupported workflow type"}
        
    except Exception as e:
        logger.error(f"Execute hierarchical workflow error: {e}")
        return {"success": False, "error": str(e)}

async def execute_custom_workflow(workflow_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute custom workflow steps"""
    
    try:
        workflow_type = workflow_data["workflow_type"]
        
        if workflow_type == "comprehensive_audit":
            return await execute_audit_workflow(workflow_id, workflow_data)
        elif workflow_type == "seo_optimization":
            return await execute_seo_workflow(workflow_id, workflow_data)
        elif workflow_type == "self_marketing":
            return await execute_self_marketing_workflow(workflow_id, workflow_data)
        else:
            # Generic workflow execution
            for i in range(5):
                await asyncio.sleep(1)
                progress = (i + 1) * 20
                await update_workflow_progress(workflow_id, progress, i + 1, {"step": f"Step {i + 1} completed"})
            
            return {"success": True, "data": {"message": "Generic workflow completed"}}
        
    except Exception as e:
        logger.error(f"Execute custom workflow error: {e}")
        return {"success": False, "error": str(e)}

async def execute_audit_workflow(workflow_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute comprehensive audit workflow"""
    
    audit_steps = [
        ("Website technical audit", 12),
        ("SEO analysis", 25),
        ("Social media audit", 40),
        ("Competitor analysis", 55),
        ("Content audit", 70),
        ("Performance analysis", 85),
        ("Recommendations generation", 95),
        ("Report compilation", 100)
    ]
    
    audit_results = {}
    
    for i, (step_name, progress) in enumerate(audit_steps):
        await asyncio.sleep(2)  # Simulate processing time
        
        # Generate step-specific results
        if "SEO" in step_name:
            step_result = {
                "seo_score": 75,
                "issues_found": 12,
                "opportunities": 8,
                "critical_fixes": ["Fix broken internal links", "Optimize meta descriptions"]
            }
        elif "Social media" in step_name:
            step_result = {
                "platforms_analyzed": ["Facebook", "Twitter", "LinkedIn", "Instagram"],
                "engagement_rate": 2.3,
                "follower_growth": -0.5,
                "recommendations": ["Increase posting frequency", "Improve content quality"]
            }
        else:
            step_result = {"status": "completed", "data": f"Results for {step_name.lower()}"}
        
        audit_results[step_name.lower().replace(" ", "_")] = step_result
        await update_workflow_progress(workflow_id, progress, i + 1, {"current_audit": step_result})
    
    return {"success": True, "data": audit_results}

async def execute_seo_workflow(workflow_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute SEO optimization workflow"""
    
    seo_steps = [
        ("Keyword research", 15),
        ("Technical SEO audit", 35),
        ("Content optimization", 55),
        ("Link building analysis", 75),
        ("Performance tracking setup", 90),
        ("Recommendations finalization", 100)
    ]
    
    seo_results = {}
    
    for i, (step_name, progress) in enumerate(seo_steps):
        await asyncio.sleep(2)
        
        if "Keyword" in step_name:
            step_result = {
                "primary_keywords": ["marketing automation", "AI marketing tools"],
                "long_tail_keywords": ["best AI marketing automation software", "marketing AI tools for small business"],
                "difficulty_score": 65,
                "opportunity_score": 82
            }
        else:
            step_result = {"status": "completed", "improvements_identified": i + 2}
        
        seo_results[step_name.lower().replace(" ", "_")] = step_result
        await update_workflow_progress(workflow_id, progress, i + 1, {"current_seo": step_result})
    
    return {"success": True, "data": seo_results}

async def execute_self_marketing_workflow(workflow_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute self-marketing workflow"""
    
    marketing_steps = [
        ("Content strategy development", 35),
        ("Automated content generation", 70),
        ("Social media automation setup", 100)
    ]
    
    marketing_results = {}
    
    for i, (step_name, progress) in enumerate(marketing_steps):
        await asyncio.sleep(3)
        
        step_result = {
            "status": "completed",
            "content_created": 5 + i * 3,
            "automation_rules": i + 1
        }
        
        marketing_results[step_name.lower().replace(" ", "_")] = step_result
        await update_workflow_progress(workflow_id, progress, i + 1, {"current_marketing": step_result})
    
    return {"success": True, "data": marketing_results}

async def update_workflow_status(workflow_id: str, status: WorkflowStatus, progress: float, result_data: Dict[str, Any] = None):
    """Update workflow status in Redis"""
    
    try:
        updates = {
            "status": status.value,
            "progress": str(progress),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        if result_data:
            updates["result_data"] = json.dumps(result_data)
        
        await redis_client.hset(f"workflow:{workflow_id}", mapping=updates)
        
    except Exception as e:
        logger.error(f"Update workflow status error: {e}")

async def update_workflow_progress(workflow_id: str, progress: float, steps_completed: int, step_data: Dict[str, Any]):
    """Update workflow progress and add execution log"""
    
    try:
        # Get current execution logs
        current_logs_raw = await redis_client.hget(f"workflow:{workflow_id}", "execution_logs")
        current_logs = json.loads(current_logs_raw) if current_logs_raw else []
        
        # Add new log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "progress": progress,
            "step": steps_completed,
            "data": step_data
        }
        current_logs.append(log_entry)
        
        # Update workflow
        updates = {
            "progress": str(progress),
            "steps_completed": str(steps_completed),
            "execution_logs": json.dumps(current_logs),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hset(f"workflow:{workflow_id}", mapping=updates)
        
    except Exception as e:
        logger.error(f"Update workflow progress error: {e}")

# Background task processor
async def process_agent_tasks():
    """Background task processor for agent queues"""
    
    while True:
        try:
            # Process high priority tasks first
            for priority in ["urgent", "high", "normal", "low"]:
                queue_name = f"agent_queue:{priority}"
                
                # Get task from queue
                task_id = await redis_client.brpop(queue_name, timeout=1)
                
                if task_id:
                    task_id = task_id[1]  # brpop returns (queue_name, task_id)
                    await process_single_task(task_id)
                    break  # Process one task at a time
            
            # If no tasks, wait a bit
            if not task_id:
                await asyncio.sleep(5)
                
        except Exception as e:
            logger.error(f"Process agent tasks error: {e}")
            await asyncio.sleep(10)

async def process_single_task(task_id: str):
    """Process a single agent task"""
    
    try:
        # Get task data
        task_data = await redis_client.hgetall(f"agent_task:{task_id}")
        if not task_data:
            logger.error(f"Task not found: {task_id}")
            return
        
        # Update status to running
        await redis_client.hset(f"agent_task:{task_id}", mapping={
            "status": WorkflowStatus.RUNNING.value,
            "updated_at": datetime.utcnow().isoformat()
        })
        
        start_time = datetime.utcnow()
        
        # Execute task based on agent type
        agent_type = task_data["agent_type"]
        input_data = json.loads(task_data["input_data"])
        
        if digital_audit_crew and agent_type == AgentType.DIGITAL_AUDITOR.value:
            result = await execute_digital_audit_task(input_data)
        elif workflow_engine and agent_type == AgentType.CAMPAIGN_OPTIMIZER.value:
            result = await execute_campaign_optimization_task(input_data)
        elif marketing_strategist and agent_type == AgentType.CONTENT_CREATOR.value:
            result = await execute_content_creation_task(input_data)
        elif agent_type == AgentType.EMAIL_MARKETING_SPECIALIST.value:
            result = await execute_email_marketing_task(input_data)
        elif agent_type in refined_agent_registry:
            # Use the unified execution method from BaseAgent
            from agents.base_agent import AgentTaskRequest as BaseAgentTaskRequest
            refined_agent = refined_agent_registry[agent_type]
            
            # Prepare task request for refined agent
            from agents.base_agent import AgentTaskRequest
            refined_request = AgentTaskRequest(
                task_id=task_id,
                tenant_id=task_data.get("tenant_id", "default"),
                agent_name=refined_agent.agent_name,
                task_type=task_data.get("task_type", "general"),
                task_description=task_data.get("task_description", "Task execution"),
                input_data=input_data,
                metadata=json.loads(task_data.get("metadata", "{}")),
                config=json.loads(task_data.get("config", "{}"))
            )


            
            try:
                agent_result = await refined_agent.execute_task(refined_request)
                result = {"success": True, "data": agent_result, "cost": 0.50}
            except Exception as e:
                logger.error(f"Refined agent execution failed: {e}")
                result = {"success": False, "error": str(e), "data": {}}
        else:
            result = await execute_mock_task(agent_type, input_data)
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Update task with results
        updates = {
            "status": WorkflowStatus.COMPLETED.value if result["success"] else WorkflowStatus.FAILED.value,
            "result_data": json.dumps(result["data"]),
            "execution_time_seconds": str(execution_time),
            "cost_estimate": str(result.get("cost", 0.0)),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        if not result["success"]:
            updates["error_message"] = result.get("error", "Unknown error")
        
        await redis_client.hset(f"agent_task:{task_id}", mapping=updates)
        
        # Publish task completed event
        if result["success"]:
            event = EventFactory.agent_task_completed(
                tenant_id=task_data["tenant_id"],
                task_id=task_id,
                agent_name=agent_type,
                result_data=result["data"]
            )
        else:
            event = EventFactory.agent_task_failed(
                tenant_id=task_data["tenant_id"],
                task_id=task_id,
                agent_name=agent_type,
                error_data={"error": result.get("error", "Unknown error")}
            )
        
        await event_bus.publish(event)
        
    except Exception as e:
        logger.error(f"Process single task error: {e}")
        
        # Update task as failed
        try:
            await redis_client.hset(f"agent_task:{task_id}", mapping={
                "status": WorkflowStatus.FAILED.value,
                "error_message": str(e),
                "updated_at": datetime.utcnow().isoformat()
            })
        except Exception as update_error:
            logger.error(f"Failed to update task status: {update_error}")

async def execute_digital_audit_task(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute digital audit using CrewAI agents"""
    
    try:
        # Simulate CrewAI execution
        await asyncio.sleep(8)  # Simulate processing time
        
        audit_result = {
            "company": input_data.get("company", "Unknown Company"),
            "website": input_data.get("website", ""),
            "audit_score": 73,
            "critical_issues": [
                "Website loading speed is slow (4.2s)",
                "Missing meta descriptions on 12 pages",
                "No Google Analytics tracking detected",
                "Social media profiles not properly linked"
            ],
            "recommendations": [
                "Optimize images and implement caching",
                "Add meta descriptions for better SEO",
                "Set up proper analytics tracking",
                "Create consistent social media branding",
                "Implement SSL certificate",
                "Improve mobile responsiveness"
            ],
            "seo_analysis": {
                "technical_seo_score": 68,
                "content_seo_score": 75,
                "backlink_profile_score": 45,
                "local_seo_score": 82
            },
            "social_media_audit": {
                "facebook_score": 60,
                "linkedin_score": 45,
                "twitter_score": 30,
                "instagram_score": 0
            },
            "competitor_analysis": [
                {
                    "competitor": "Competitor A",
                    "strengths": ["Strong social media presence", "Fast website"],
                    "weaknesses": ["Limited content marketing", "Poor mobile experience"]
                }
            ]
        }
        
        return {"success": True, "data": audit_result, "cost": 0.60}
        
    except Exception as e:
        logger.error(f"Execute digital audit task error: {e}")
        return {"success": False, "error": str(e), "data": {}}

async def execute_campaign_optimization_task(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute campaign optimization using AI agents"""
    
    try:
        await asyncio.sleep(5)
        
        optimization_result = {
            "campaign_name": input_data.get("campaign_data", {}).get("name", "Campaign"),
            "current_performance": input_data.get("current_performance", {}),
            "optimizations": [
                {
                    "area": "Budget Allocation",
                    "current": "Equal across all ad groups",
                    "recommended": "60% to high-performing keywords, 40% to testing",
                    "expected_improvement": "25% increase in conversions"
                },
                {
                    "area": "Bidding Strategy",
                    "current": "Manual CPC",
                    "recommended": "Target ROAS bidding",
                    "expected_improvement": "15% better ROAS"
                },
                {
                    "area": "Ad Copy",
                    "current": "Generic messaging",
                    "recommended": "Personalized ads with dynamic keywords",
                    "expected_improvement": "20% higher CTR"
                }
            ],
            "projected_results": {
                "current_roas": 2.4,
                "projected_roas": 3.2,
                "improvement_percentage": 33.3
            }
        }
        
        return {"success": True, "data": optimization_result, "cost": 0.30}
        
    except Exception as e:
        logger.error(f"Execute campaign optimization task error: {e}")
        return {"success": False, "error": str(e), "data": {}}

async def execute_content_creation_task(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute content creation using AI agents"""
    
    try:
        await asyncio.sleep(4)
        
        content_type = input_data.get("content_type", "blog_post")
        topic = input_data.get("topic", "Marketing")
        
        if content_type == "blog_post":
            content = f"""
            # {topic}: A Comprehensive Guide
            
            ## Introduction
            
            In today's digital landscape, {topic.lower()} has become essential for businesses looking to grow and compete effectively. This comprehensive guide will explore the key strategies and best practices that can help you succeed.
            
            ## Key Strategies
            
            1. **Data-Driven Approach**: Use analytics to inform your decisions
            2. **Customer-Centric Focus**: Always prioritize customer needs
            3. **Continuous Optimization**: Regularly test and improve your strategies
            
            ## Best Practices
            
            - Start with clear objectives and KPIs
            - Implement proper tracking and measurement
            - Stay updated with industry trends
            - Invest in quality tools and platforms
            
            ## Conclusion
            
            Success in {topic.lower()} requires dedication, strategic thinking, and continuous learning. By following these guidelines, you'll be well-positioned to achieve your goals.
            """
        
        elif content_type == "ad_copy":
            content = f"""
            Headline: Transform Your {topic} Strategy Today
            
            Description: Discover how leading businesses are using AI-powered {topic.lower()} to increase conversions by 300%. Get started with our proven system.
            
            Call-to-Action: Start Your Free Trial
            
            Additional Variants:
            - "Revolutionize Your {topic} in 30 Days"
            - "The {topic} Solution That Actually Works"
            - "Join 10,000+ Companies Using Smart {topic}"
            """
        
        else:
            content = f"Generated {content_type} content about {topic}"
        
        result = {
            "content_type": content_type,
            "topic": topic,
            "generated_content": content,
            "word_count": len(content.split()),
            "seo_keywords": input_data.get("keywords", []),
            "target_audience": input_data.get("target_audience", "General"),
            "tone": input_data.get("tone", "professional"),
            "optimization_suggestions": [
                "Add more specific examples",
                "Include relevant statistics",
                "Optimize for target keywords",
                "Add call-to-action elements"
            ]
        }
        
        return {"success": True, "data": result, "cost": 0.25}
        
    except Exception as e:
        logger.error(f"Execute content creation task error: {e}")
        return {"success": False, "error": str(e), "data": {}}

async def execute_email_marketing_task(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute Email Marketing Specialist task with Mautic integration"""
    
    try:
        await asyncio.sleep(6)  # Simulate AI processing time
        
        campaign_type = input_data.get("campaign_type", "nurture")
        target_audience = input_data.get("target_audience", "General")
        email_objective = input_data.get("email_objective", "Engagement")
        subject_line_count = input_data.get("subject_line_count", 5)
        content_length = input_data.get("content_length", "medium")
        personalization_level = input_data.get("personalization_level", "high")
        funnel_stage = input_data.get("funnel_stage")
        brand_voice = input_data.get("brand_voice", "professional")
        
        # Generate subject lines
        subject_lines = []
        if campaign_type == "welcome":
            subject_lines = [
                "Welcome to {company_name}! Your journey starts here",
                "You're in! Here's what to expect from {company_name}",
                "Thanks for joining us, {first_name}!",
                "Your {company_name} account is ready to go",
                "Welcome aboard! Let's achieve great things together"
            ]
        elif campaign_type == "nurture":
            subject_lines = [
                "The secret to {goal} that {industry} leaders don't want you to know",
                "{first_name}, are you making this common {industry} mistake?",
                "How {company_name} helped {customer_name} increase {metric} by {percentage}%",
                "The ultimate guide to {topic} for {target_audience}",
                "Your competitors are already doing this - are you?"
            ]
        elif campaign_type == "promotional":
            subject_lines = [
                "Exclusive offer: {discount}% off ends tonight",
                "{first_name}, don't miss out on this limited-time deal",
                "Flash sale: Save {amount} on {product_name}",
                "Last chance: {offer_name} expires in 24 hours",
                "Your VIP discount is waiting inside"
            ]
        elif campaign_type == "funnel_integration":
            subject_lines = [
                "Ready for the next step in your {goal} journey?",
                "Your personalized {solution} strategy is here",
                "Time to level up your {focus_area}",
                "{first_name}, your success roadmap awaits",
                "The missing piece to your {objective} puzzle"
            ]
        else:
            subject_lines = [
                f"Important update about your {campaign_type}",
                f"{campaign_type.title()} insights you need to know",
                f"Your {campaign_type} performance summary",
                f"New {campaign_type} opportunities available",
                f"{campaign_type.title()} best practices revealed"
            ]
        
        # Generate email content based on campaign type and length
        if campaign_type == "funnel_integration":
            email_content = generate_funnel_email_content(input_data)
        else:
            email_content = generate_campaign_email_content(campaign_type, target_audience, email_objective, content_length, brand_voice)
        
        # Generate automation triggers and workflows
        automation_workflows = []
        if campaign_type == "welcome":
            automation_workflows = [
                {
                    "trigger": "form_submitted",
                    "delay_hours": 0,
                    "action": "send_welcome_email",
                    "conditions": ["new_subscriber"]
                },
                {
                    "trigger": "email_opened",
                    "delay_hours": 24,
                    "action": "send_getting_started_email",
                    "conditions": ["opened_welcome_email"]
                },
                {
                    "trigger": "time_delay",
                    "delay_hours": 72,
                    "action": "send_value_proposition_email",
                    "conditions": ["no_product_interaction"]
                }
            ]
        elif campaign_type == "nurture":
            automation_workflows = [
                {
                    "trigger": "lead_score_reached",
                    "delay_hours": 0,
                    "action": "send_nurture_email",
                    "conditions": ["score_above_50"]
                },
                {
                    "trigger": "email_clicked",
                    "delay_hours": 48,
                    "action": "send_case_study_email",
                    "conditions": ["clicked_cta"]
                },
                {
                    "trigger": "page_visited",
                    "delay_hours": 24,
                    "action": "send_retargeting_email",
                    "conditions": ["visited_pricing_page"]
                }
            ]
        elif campaign_type == "funnel_integration":
            funnel_id = input_data.get("funnel_id")
            automation_workflows = [
                {
                    "trigger": "funnel_stage_entry",
                    "delay_hours": 0,
                    "action": "send_stage_specific_email",
                    "conditions": [f"entered_stage"],
                    "funnel_id": funnel_id
                },
                {
                    "trigger": "behavioral_action",
                    "delay_hours": 12,
                    "action": "send_followup_email",
                    "conditions": ["high_engagement"]
                }
            ]
        
        # Generate A/B testing recommendations
        ab_testing_recommendations = [
            {
                "test_element": "subject_line",
                "variants": subject_lines[:2],
                "success_metric": "open_rate",
                "test_duration": "7_days",
                "minimum_sample_size": 1000
            },
            {
                "test_element": "email_content",
                "variants": ["benefit_focused", "feature_focused"],
                "success_metric": "click_rate",
                "test_duration": "14_days",
                "minimum_sample_size": 2000
            },
            {
                "test_element": "call_to_action",
                "variants": ["Get Started Now", "Learn More", "Try It Free"],
                "success_metric": "conversion_rate",
                "test_duration": "10_days",
                "minimum_sample_size": 1500
            }
        ]
        
        # Generate personalization recommendations
        personalization_strategies = [
            {
                "field": "first_name",
                "usage": "subject_line_and_greeting",
                "impact": "15-25% increase in open rates"
            },
            {
                "field": "company_name",
                "usage": "throughout_content",
                "impact": "20-30% increase in relevance score"
            },
            {
                "field": "industry",
                "usage": "case_studies_and_examples",
                "impact": "35-45% increase in engagement"
            },
            {
                "field": "past_behavior",
                "usage": "content_recommendations",
                "impact": "40-60% increase in click-through rates"
            }
        ]
        
        # Generate deliverability optimization tips
        deliverability_optimization = [
            {
                "area": "sender_reputation",
                "recommendations": [
                    "Use consistent sender name and email address",
                    "Implement SPF, DKIM, and DMARC records",
                    "Monitor sender reputation scores regularly"
                ]
            },
            {
                "area": "content_optimization",
                "recommendations": [
                    "Maintain balanced text-to-image ratio (80:20)",
                    "Avoid spam trigger words and excessive punctuation",
                    "Include clear unsubscribe link",
                    "Use alt text for all images"
                ]
            },
            {
                "area": "list_hygiene",
                "recommendations": [
                    "Remove inactive subscribers quarterly",
                    "Implement double opt-in process",
                    "Segment lists based on engagement levels",
                    "Monitor bounce rates and complaint rates"
                ]
            }
        ]
        
        # Create Mautic integration configuration
        mautic_integration = {
            "campaign_name": f"{campaign_type.title()} Campaign - {target_audience}",
            "email_templates": [
                {
                    "name": f"{campaign_type.title()} Email Template",
                    "subject": subject_lines[0],
                    "html_content": email_content["html"],
                    "text_content": email_content["text"],
                    "template_variables": email_content["variables"]
                }
            ],
            "automation_rules": automation_workflows,
            "segments": [
                {
                    "name": f"{target_audience} - {campaign_type.title()}",
                    "filters": email_content["segmentation_filters"]
                }
            ],
            "tracking_configuration": {
                "open_tracking": True,
                "click_tracking": True,
                "conversion_tracking": True,
                "utm_parameters": {
                    "utm_source": "email",
                    "utm_medium": "email_marketing",
                    "utm_campaign": f"{campaign_type}_{target_audience.lower().replace(' ', '_')}"
                }
            }
        }
        
        result = {
            "campaign_type": campaign_type,
            "target_audience": target_audience,
            "email_objective": email_objective,
            "subject_lines": subject_lines[:subject_line_count],
            "email_content": email_content,
            "automation_workflows": automation_workflows,
            "ab_testing_recommendations": ab_testing_recommendations,
            "personalization_strategies": personalization_strategies,
            "deliverability_optimization": deliverability_optimization,
            "mautic_integration": mautic_integration,
            "performance_predictions": {
                "expected_open_rate": f"{18 + (5 if personalization_level == 'high' else 0)}%",
                "expected_click_rate": f"{2.5 + (1.5 if content_length == 'medium' else 0)}%",
                "expected_conversion_rate": f"{0.8 + (0.4 if campaign_type == 'promotional' else 0.2)}%"
            },
            "optimization_score": 87,
            "recommendations": [
                "Implement dynamic content based on user behavior",
                "Set up abandoned cart recovery sequences",
                "Use countdown timers for urgency in promotional emails",
                "Optimize send times based on audience time zones",
                "Implement re-engagement campaigns for inactive subscribers"
            ]
        }
        
        return {"success": True, "data": result, "cost": 0.35}
        
    except Exception as e:
        logger.error(f"Execute email marketing task error: {e}")
        return {"success": False, "error": str(e), "data": {}}

def generate_funnel_email_content(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate email content specifically for sales funnel integration"""
    
    funnel_id = input_data.get("funnel_id", "unknown")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Your Next Step Awaits</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f8f9fa;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 40px 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <img src="{{{{company_logo}}}}" alt="{{{{company_name}}}}" style="height: 50px;">
            </div>
            
            <h1 style="color: #2c3e50; font-size: 24px; text-align: center; margin-bottom: 20px;">
                Hi {{{{first_name}}}}, Ready for Your Next Step?
            </h1>
            
            <p style="color: #34495e; font-size: 16px; line-height: 1.6; margin-bottom: 20px;">
                Based on your interest in {{{{topic}}}}, I wanted to personally reach out with some insights that could help you achieve your goals faster.
            </p>
            
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
                <h3 style="color: #2c3e50; font-size: 18px; margin-bottom: 15px;">Here's what successful {{{{industry}}}} businesses are doing:</h3>
                <ul style="color: #34495e; margin: 0; padding-left: 20px;">
                    <li style="margin-bottom: 10px;">Implementing automated {{{{solution_type}}}} workflows that save 15+ hours per week</li>
                    <li style="margin-bottom: 10px;">Using AI-powered insights to increase {{{{key_metric}}}} by 40%</li>
                    <li style="margin-bottom: 10px;">Leveraging personalized customer experiences to boost retention by 25%</li>
                </ul>
            </div>
            
            <p style="color: #34495e; font-size: 16px; line-height: 1.6; margin-bottom: 25px;">
                I've created a personalized strategy guide specifically for {{{{company_name}}}} that shows exactly how you can implement these same tactics.
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{{{{personalized_strategy_url}}}}" style="background-color: #3498db; color: #ffffff; text-decoration: none; padding: 15px 30px; border-radius: 5px; font-size: 18px; font-weight: bold; display: inline-block;">Get My Personalized Strategy</a>
            </div>
            
            <p style="color: #7f8c8d; font-size: 14px; line-height: 1.5; margin-bottom: 20px;">
                This strategy guide is completely free and tailored specifically to your {{{{industry}}}} business. It includes step-by-step implementation plans and expected ROI calculations.
            </p>
            
            <div style="border-top: 2px solid #ecf0f1; padding-top: 20px; margin-top: 30px;">
                <p style="color: #34495e; font-size: 16px; margin-bottom: 10px;">Best regards,</p>
                <p style="color: #2c3e50; font-size: 16px; font-weight: bold; margin: 0;">{{{{sender_name}}}}</p>
                <p style="color: #7f8c8d; font-size: 14px; margin: 5px 0 0 0;">{{{{sender_title}}}} at {{{{company_name}}}}</p>
            </div>
        </div>
        
        <!-- Tracking pixel -->
        <img src="{{{{tracking_pixel_url}}}}" width="1" height="1" style="display: none;">
    </body>
    </html>
    """
    
    text_content = f"""
    Hi {{{{first_name}}}},
    
    Ready for Your Next Step?
    
    Based on your interest in {{{{topic}}}}, I wanted to personally reach out with some insights that could help you achieve your goals faster.
    
    Here's what successful {{{{industry}}}} businesses are doing:
    
    * Implementing automated {{{{solution_type}}}} workflows that save 15+ hours per week
    * Using AI-powered insights to increase {{{{key_metric}}}} by 40%
    * Leveraging personalized customer experiences to boost retention by 25%
    
    I've created a personalized strategy guide specifically for {{{{company_name}}}} that shows exactly how you can implement these same tactics.
    
    Get your personalized strategy here: {{{{personalized_strategy_url}}}}
    
    This strategy guide is completely free and tailored specifically to your {{{{industry}}}} business. It includes step-by-step implementation plans and expected ROI calculations.
    
    Best regards,
    {{{{sender_name}}}}
    {{{{sender_title}}}} at {{{{company_name}}}}
    
    Unsubscribe: {{{{unsubscribe_url}}}}
    """
    
    return {
        "html": html_content,
        "text": text_content,
        "variables": [
            "first_name", "company_name", "company_logo", "topic", "industry",
            "solution_type", "key_metric", "personalized_strategy_url", "sender_name",
            "sender_title", "tracking_pixel_url", "unsubscribe_url"
        ],
        "segmentation_filters": [
            {"field": "funnel_stage", "operator": "equals", "value": input_data.get("funnel_stage", "awareness")},
            {"field": "engagement_score", "operator": "greater_than", "value": 30}
        ]
    }

def generate_campaign_email_content(campaign_type: str, target_audience: str, email_objective: str, content_length: str, brand_voice: str) -> Dict[str, Any]:
    """Generate email content for different campaign types"""
    
    # Base HTML template structure
    html_base = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{{{{subject_line}}}}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f8f9fa;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 40px 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <img src="{{{{company_logo}}}}" alt="{{{{company_name}}}}" style="height: 50px;">
            </div>
            
            {{{{email_body}}}}
            
            <div style="border-top: 2px solid #ecf0f1; padding-top: 20px; margin-top: 30px;">
                <p style="color: #7f8c8d; font-size: 14px; text-align: center;">
                    {{{{company_name}}}} | {{{{company_address}}}}<br>
                    <a href="{{{{unsubscribe_url}}}}" style="color: #7f8c8d;">Unsubscribe</a> | 
                    <a href="{{{{preference_center_url}}}}" style="color: #7f8c8d;">Update Preferences</a>
                </p>
            </div>
        </div>
        
        <img src="{{{{tracking_pixel_url}}}}" width="1" height="1" style="display: none;">
    </body>
    </html>
    """
    
    # Generate content based on campaign type
    if campaign_type == "welcome":
        email_body = f"""
        <h1 style="color: #2c3e50; font-size: 24px; text-align: center; margin-bottom: 20px;">
            Welcome to {{{{company_name}}}}, {{{{first_name}}}}!
        </h1>
        
        <p style="color: #34495e; font-size: 16px; line-height: 1.6; margin-bottom: 20px;">
            We're thrilled to have you join our community of {{{{target_audience}}}} who are already transforming their {email_objective.lower()}.
        </p>
        
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
            <h3 style="color: #2c3e50; font-size: 18px; margin-bottom: 15px;">Here's what you can expect:</h3>
            <ul style="color: #34495e; margin: 0; padding-left: 20px;">
                <li style="margin-bottom: 10px;">Weekly insights and actionable tips</li>
                <li style="margin-bottom: 10px;">Exclusive access to premium resources</li>
                <li style="margin-bottom: 10px;">Personalized recommendations based on your goals</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{{{getting_started_url}}}}" style="background-color: #3498db; color: #ffffff; text-decoration: none; padding: 15px 30px; border-radius: 5px; font-size: 18px; font-weight: bold; display: inline-block;">Get Started Now</a>
        </div>
        """
        
    elif campaign_type == "nurture":
        email_body = f"""
        <h1 style="color: #2c3e50; font-size: 24px; text-align: center; margin-bottom: 20px;">
            {{{{first_name}}}}, Are You Making This Common Mistake?
        </h1>
        
        <p style="color: #34495e; font-size: 16px; line-height: 1.6; margin-bottom: 20px;">
            Most {target_audience.lower()} struggle with {email_objective.lower()} because they're missing one crucial element...
        </p>
        
        <p style="color: #34495e; font-size: 16px; line-height: 1.6; margin-bottom: 25px;">
            After working with hundreds of businesses like {{{{company_name}}}}, I've identified the #1 factor that separates those who succeed from those who struggle.
        </p>
        
        <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 20px; border-radius: 8px; margin: 25px 0;">
            <p style="color: #856404; font-size: 16px; font-weight: bold; margin: 0 0 10px 0;">The Secret:</p>
            <p style="color: #856404; font-size: 16px; margin: 0;">Successful businesses focus on [specific insight] rather than [common mistake].</p>
        </div>
        
        <p style="color: #34495e; font-size: 16px; line-height: 1.6; margin-bottom: 25px;">
            I've put together a detailed case study showing exactly how one client increased their {email_objective.lower()} by 250% using this approach.
        </p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{{{case_study_url}}}}" style="background-color: #e67e22; color: #ffffff; text-decoration: none; padding: 15px 30px; border-radius: 5px; font-size: 18px; font-weight: bold; display: inline-block;">Read the Case Study</a>
        </div>
        """
        
    elif campaign_type == "promotional":
        email_body = f"""
        <h1 style="color: #e74c3c; font-size: 28px; text-align: center; margin-bottom: 20px;">
            🔥 Flash Sale: 48 Hours Only!
        </h1>
        
        <p style="color: #2c3e50; font-size: 18px; text-align: center; font-weight: bold; margin-bottom: 20px;">
            Save {{{{discount_percentage}}}}% on Everything - No Code Needed
        </p>
        
        <div style="background-color: #d4edda; border: 2px solid #27ae60; padding: 20px; border-radius: 8px; margin: 25px 0; text-align: center;">
            <h2 style="color: #27ae60; font-size: 24px; margin: 0 0 10px 0;">Limited Time Offer</h2>
            <p style="color: #155724; font-size: 16px; margin: 0;">Ends {{{{sale_end_date}}}} at midnight</p>
        </div>
        
        <p style="color: #34495e; font-size: 16px; line-height: 1.6; margin-bottom: 25px;">
            {{{{first_name}}}}, this is the perfect time to invest in {email_objective.lower()} with our biggest discount of the year.
        </p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{{{shop_now_url}}}}" style="background-color: #e74c3c; color: #ffffff; text-decoration: none; padding: 20px 40px; border-radius: 5px; font-size: 20px; font-weight: bold; display: inline-block; box-shadow: 0 4px 8px rgba(231,76,60,0.3);">Shop Now - Save {{{{discount_percentage}}}}%</a>
        </div>
        
        <p style="color: #7f8c8d; font-size: 14px; text-align: center; margin-top: 20px;">
            *Offer valid until {{{{sale_end_date}}}}. Cannot be combined with other offers.
        </p>
        """
        
    else:  # Generic content
        email_body = f"""
        <h1 style="color: #2c3e50; font-size: 24px; text-align: center; margin-bottom: 20px;">
            Important Update for {{{{first_name}}}}
        </h1>
        
        <p style="color: #34495e; font-size: 16px; line-height: 1.6; margin-bottom: 20px;">
            We wanted to share some important information about {email_objective.lower()} that could benefit your {target_audience.lower()} business.
        </p>
        
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
            <p style="color: #34495e; font-size: 16px; line-height: 1.6; margin: 0;">
                Our latest research shows that businesses implementing these strategies are seeing significant improvements in their {email_objective.lower()}.
            </p>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{{{learn_more_url}}}}" style="background-color: #3498db; color: #ffffff; text-decoration: none; padding: 15px 30px; border-radius: 5px; font-size: 18px; font-weight: bold; display: inline-block;">Learn More</a>
        </div>
        """
    
    # Create text version
    text_content = f"""
    {{{{subject_line}}}}
    
    Hi {{{{first_name}}}},
    
    [Text version of email content based on campaign type]
    
    Best regards,
    {{{{company_name}}}} Team
    
    ---
    {{{{company_name}}}} | {{{{company_address}}}}
    Unsubscribe: {{{{unsubscribe_url}}}}
    Update Preferences: {{{{preference_center_url}}}}
    """
    
    return {
        "html": html_base.replace("{{{{email_body}}}}", email_body),
        "text": text_content,
        "variables": [
            "first_name", "company_name", "company_logo", "company_address",
            "subject_line", "tracking_pixel_url", "unsubscribe_url", "preference_center_url"
        ],
        "segmentation_filters": [
            {"field": "audience_type", "operator": "equals", "value": target_audience.lower()},
            {"field": "subscription_status", "operator": "equals", "value": "active"}
        ]
    }

async def execute_mock_task(agent_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute mock task for agents not yet implemented"""
    
    try:
        await asyncio.sleep(3)  # Simulate processing
        
        mock_result = {
            "agent_type": agent_type,
            "input_processed": True,
            "mock_output": f"Mock result for {agent_type} agent",
            "processing_time": "3 seconds",
            "status": "completed (mock)",
            "input_summary": {k: str(v)[:100] for k, v in input_data.items()}
        }
        
        return {"success": True, "data": mock_result, "cost": get_cost_estimate(AgentType(agent_type))}
        
    except Exception as e:
        logger.error(f"Execute mock task error: {e}")
        return {"success": False, "error": str(e), "data": {}}

# Event handlers
@event_handler(EventType.CAMPAIGN_STARTED)
async def handle_campaign_started(event):
    """Handle campaign started - could trigger optimization agent"""
    logger.info(f"Campaign started, considering AI optimization: {event.data}")

@event_handler(EventType.USER_CREATED)
async def handle_user_created(event):
    """Handle new user created - could trigger onboarding workflow"""
    logger.info(f"New user created, triggering onboarding workflow: {event.data}")

# Mount Chat API
if CHAT_API_AVAILABLE:
    # Mount the chat API endpoints
    app.mount("/chat", chat_app, name="chat")
    
    @app.get("/agents")
    async def list_all_agents():
        """Get all available AI agents for chat interface"""
        return agent_registry.list_all_agents()
    
    @app.get("/agents/categories/{category}")
    async def list_agents_by_category(category: str):
        """Get agents by category for chat interface"""
        from chat_api import AgentCategory
        try:
            cat = AgentCategory(category)
            return agent_registry.list_agents_by_category(cat)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    
    @app.get("/agents/search")
    async def search_agents(q: str):
        """Search agents by capabilities or description"""
        return agent_registry.search_agents(q)
    
    @app.get("/agents/{agent_name}")
    async def get_agent_info(agent_name: str):
        """Get specific agent information"""
        agent_info = agent_registry.get_agent_info(agent_name)
        if not agent_info:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent_info
    
    @app.post("/chat/sessions")
    async def create_chat_session(user_id: str, tenant_id: str, platform: str = "web"):
        """Create a new chat session"""
        return await chat_manager.create_session(user_id, tenant_id, platform)
    
    @app.get("/chat/sessions/{session_id}")
    async def get_chat_session(session_id: str):
        """Get chat session details"""
        session = await chat_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    
    @app.get("/chat/sessions/{session_id}/messages")
    async def get_session_messages(session_id: str, limit: int = 50):
        """Get messages for a chat session"""
        return await chat_manager.get_session_messages(session_id, limit)
    
    @app.post("/chat/message")
    async def send_chat_message(request: dict):
        """Send a message to an AI agent"""
        from chat_api import ChatRequest, ChatMessage, ChatMessageType
        
        # Parse request
        chat_request = ChatRequest(
            session_id=request["session_id"],
            message=request["message"],
            agent_name=request.get("agent_name"),
            platform=request.get("platform", "web")
        )
        
        # Add user message to session
        user_message = ChatMessage(
            session_id=chat_request.session_id,
            message_type=ChatMessageType.USER,
            content=chat_request.message,
            user_id="user"  # TODO: Get from auth context
        )
        await chat_manager.add_message(user_message)
        
        # Route to agent and get response
        return await chat_manager.route_message_to_agent(
            chat_request.session_id,
            chat_request.message,
            chat_request.agent_name
        )
    
    @app.get("/chat/health")
    async def chat_health_check():
        """Chat API health check"""
        return {
            "status": "healthy",
            "total_agents": len(agent_registry.agents),
            "active_sessions": len(chat_manager.active_sessions),
            "chat_api_available": True,
            "timestamp": datetime.now().isoformat()
        }
else:
    @app.get("/chat/health")
    async def chat_health_disabled():
        """Chat API disabled"""
        return {
            "status": "disabled",
            "chat_api_available": False,
            "reason": "Chat API dependencies not available",
            "timestamp": datetime.now().isoformat()
        }

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    metrics = {
        "service": "ai-agents",
        "metrics": {
            "total_tasks_executed": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "active_workflows": 0,
            "average_execution_time": 0.0,
            "total_cost_incurred": 0.0
        }
    }
    
    if CHAT_API_AVAILABLE:
        metrics["chat_metrics"] = {
            "total_agents": len(agent_registry.agents),
            "active_sessions": len(chat_manager.active_sessions),
            "total_messages": sum(len(messages) for messages in chat_manager.session_messages.values())
        }
    
    return metrics

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)