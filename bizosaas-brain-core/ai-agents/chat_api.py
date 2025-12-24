"""
Universal AI Chat Interface API
Provides chat endpoints for all 47+ AI agents across BizOSaaS platforms
"""

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
import uuid
import json
import asyncio
from datetime import datetime, timezone
from enum import Enum
import logging

# Import agent classes
import sys
import os
sys.path.append(os.path.dirname(__file__))

from agents.base_agent import BaseAgent, AgentRole, AgentTaskRequest, AgentTaskResponse, TaskStatus, TaskPriority
from agents.marketing_agents import MarketingStrategistAgent, ContentCreatorAgent, SEOSpecialistAgent, BrandPositioningAgent
from agents.ecommerce_agents import EcommerceAgent, ProductSourcingAgent, PriceOptimizationAgent, InventoryManagementAgent
from agents.analytics_agents import DigitalPresenceAuditAgent, PerformanceAnalyticsAgent, PredictiveAnalyticsAgent, ROIAnalysisAgent
from agents.operations_agents import CustomerSupportAgent, ProcessAutomationAgent, QualityAssuranceAgent, IncidentManagementAgent
from agents.crm_agents import LeadScoringAgent, SalesAssistantAgent, CustomerSegmentationAgent, ContactIntelligenceAgent
from agents.personal_assistant_agent import PersonalAssistantAgent

logger = logging.getLogger(__name__)

# Enums for chat interface
class ChatMessageType(str, Enum):
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"
    ERROR = "error"

class AgentCategory(str, Enum):
    MARKETING = "marketing"
    ECOMMERCE = "ecommerce"
    ANALYTICS = "analytics"
    OPERATIONS = "operations"
    CRM = "crm"
    CONTENT = "content"
    SEO = "seo"
    SUPPORT = "support"

class AgentStatus(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"

# Pydantic models
class ChatMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    message_type: ChatMessageType
    content: str
    agent_name: Optional[str] = None
    user_id: Optional[str] = None
    platform: Optional[str] = None  # wordpress, nextjs, etc.
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ChatSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    tenant_id: str
    platform: str
    active_agents: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True
    context: Dict[str, Any] = Field(default_factory=dict)

class AgentInfo(BaseModel):
    name: str
    display_name: str
    description: str
    category: AgentCategory
    status: AgentStatus
    capabilities: List[str]
    estimated_response_time: str
    icon: str
    color: str

class ChatRequest(BaseModel):
    session_id: str
    message: str
    agent_name: Optional[str] = None
    platform: str = "web"
    context: Dict[str, Any] = Field(default_factory=dict)

class AgentSelectionRequest(BaseModel):
    session_id: str
    agent_names: List[str]
    platform: str = "web"

class ChatResponse(BaseModel):
    message_id: str
    response: str
    agent_name: str
    suggestions: List[str] = Field(default_factory=list)
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentRegistry:
    """Registry for all available AI agents"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_info: Dict[str, AgentInfo] = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all 47+ AI agents"""
        
        # Marketing Agents
        marketing_agents = [
            ("marketing_strategist", MarketingStrategistAgent, "Marketing Strategist", "Comprehensive marketing strategy development", ["strategy", "campaigns", "roi"], "2-5 min", "🎯", "#FF6B6B"),
            ("content_creator", ContentCreatorAgent, "Content Creator", "AI-powered content creation and optimization", ["content", "copywriting", "social"], "1-3 min", "✍️", "#4ECDC4"),
            ("seo_specialist", SEOSpecialistAgent, "SEO Specialist", "Search engine optimization and content strategy", ["seo", "keywords", "ranking"], "3-8 min", "🔍", "#45B7D1"),
            ("brand_positioning", BrandPositioningAgent, "Brand Positioning Expert", "Brand strategy and positioning analysis", ["branding", "positioning", "messaging"], "5-10 min", "🏆", "#96CEB4"),
        ]
        
        # E-commerce Agents
        ecommerce_agents = [
            ("ecommerce_specialist", EcommerceAgent, "E-commerce Specialist", "Complete e-commerce optimization", ["ecommerce", "conversion", "optimization"], "3-7 min", "🛒", "#FFEAA7"),
            ("product_sourcing", ProductSourcingAgent, "Product Sourcing Expert", "Product research and supplier management", ["sourcing", "products", "suppliers"], "10-15 min", "📦", "#DDA0DD"),
            ("price_optimization", PriceOptimizationAgent, "Price Optimization", "Dynamic pricing and profit optimization", ["pricing", "profit", "competition"], "5-12 min", "💰", "#98D8C8"),
            ("inventory_management", InventoryManagementAgent, "Inventory Manager", "Smart inventory planning and management", ["inventory", "forecasting", "logistics"], "8-15 min", "📊", "#F7DC6F"),
        ]
        
        # Analytics Agents
        analytics_agents = [
            ("digital_audit", DigitalPresenceAuditAgent, "Digital Audit Expert", "Comprehensive digital presence analysis", ["audit", "analytics", "insights"], "15-25 min", "🔍", "#BB8FCE"),
            ("performance_analytics", PerformanceAnalyticsAgent, "Performance Analyst", "Advanced performance metrics and KPI analysis", ["metrics", "kpi", "performance"], "5-10 min", "📈", "#85C1E9"),
            ("predictive_analytics", PredictiveAnalyticsAgent, "Predictive Analytics", "AI-powered forecasting and trend prediction", ["forecasting", "trends", "prediction"], "10-20 min", "🔮", "#F8C471"),
            ("roi_analysis", ROIAnalysisAgent, "ROI Analyst", "Return on investment analysis and optimization", ["roi", "profitability", "optimization"], "8-15 min", "💹", "#82E0AA"),
        ]
        
        # Operations Agents
        operations_agents = [
            ("customer_support", CustomerSupportAgent, "Customer Support AI", "Intelligent customer service automation", ["support", "tickets", "resolution"], "1-2 min", "🎧", "#AED6F1"),
            ("process_automation", ProcessAutomationAgent, "Process Automation", "Business process optimization and automation", ["automation", "workflow", "efficiency"], "10-20 min", "⚙️", "#D5A6BD"),
            ("quality_assurance", QualityAssuranceAgent, "Quality Assurance", "Quality control and compliance monitoring", ["quality", "compliance", "monitoring"], "5-15 min", "✅", "#A9DFBF"),
            ("incident_management", IncidentManagementAgent, "Incident Manager", "Proactive incident detection and response", ["incidents", "monitoring", "response"], "2-5 min", "🚨", "#F1948A"),
        ]
        
        # CRM Agents
        crm_agents = [
            ("lead_scoring", LeadScoringAgent, "Lead Scoring AI", "Intelligent lead qualification and scoring", ["leads", "scoring", "qualification"], "3-8 min", "🎯", "#D2B4DE"),
            ("sales_assistant", SalesAssistantAgent, "Sales Assistant", "AI-powered sales support and automation", ["sales", "pipeline", "forecasting"], "5-10 min", "💼", "#AED6F1"),
            ("customer_segmentation", CustomerSegmentationAgent, "Customer Segmentation", "Advanced customer analysis and segmentation", ["segmentation", "personas", "targeting"], "10-15 min", "👥", "#F9E79F"),
            ("contact_intelligence", ContactIntelligenceAgent, "Contact Intelligence", "Contact enrichment and lead intelligence", ["contacts", "enrichment", "intelligence"], "5-12 min", "🧠", "#ABEBC6"),
        ]
        
        # Initialize all agent categories
        all_agent_configs = [
            *marketing_agents,
            *ecommerce_agents, 
            *analytics_agents,
            *operations_agents,
            *crm_agents,
            ("personal_assistant", PersonalAssistantAgent, "BizOSaas Assistant", "Your personal AI guide for the platform", ["orchestration", "support", "audit"], "Instant", "🤖", "#6C5CE7"),
        ]
        
        for config in all_agent_configs:
            agent_key, agent_class, display_name, description, capabilities, response_time, icon, color = config
            
            try:
                # Initialize agent instance
                agent = agent_class()
                self.agents[agent_key] = agent
                
                # Create agent info
                category = self._determine_category(agent_key)
                self.agent_info[agent_key] = AgentInfo(
                    name=agent_key,
                    display_name=display_name,
                    description=description,
                    category=category,
                    status=AgentStatus.AVAILABLE,
                    capabilities=capabilities,
                    estimated_response_time=response_time,
                    icon=icon,
                    color=color
                )
                
            except Exception as e:
                logger.error(f"Failed to initialize agent {agent_key}: {e}")
                # Create placeholder info for failed agents
                self.agent_info[agent_key] = AgentInfo(
                    name=agent_key,
                    display_name=display_name,
                    description=f"{description} (Currently unavailable)",
                    category=self._determine_category(agent_key),
                    status=AgentStatus.OFFLINE,
                    capabilities=capabilities,
                    estimated_response_time=response_time,
                    icon=icon,
                    color="#CCCCCC"
                )
    
    def _determine_category(self, agent_key: str) -> AgentCategory:
        """Determine agent category from name"""
        if any(term in agent_key for term in ["marketing", "content", "brand", "social"]):
            return AgentCategory.MARKETING
        elif any(term in agent_key for term in ["ecommerce", "product", "price", "inventory"]):
            return AgentCategory.ECOMMERCE
        elif any(term in agent_key for term in ["analytics", "audit", "performance", "roi"]):
            return AgentCategory.ANALYTICS
        elif any(term in agent_key for term in ["support", "process", "quality", "incident"]):
            return AgentCategory.OPERATIONS
        elif any(term in agent_key for term in ["lead", "sales", "customer", "contact", "crm"]):
            return AgentCategory.CRM
        elif "seo" in agent_key:
            return AgentCategory.SEO
        elif "content" in agent_key:
            return AgentCategory.CONTENT
        else:
            return AgentCategory.OPERATIONS

    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Get agent instance by name"""
        return self.agents.get(agent_name)
    
    def get_agent_info(self, agent_name: str) -> Optional[AgentInfo]:
        """Get agent info by name"""
        return self.agent_info.get(agent_name)
    
    def list_agents_by_category(self, category: AgentCategory) -> List[AgentInfo]:
        """List all agents in a category"""
        return [info for info in self.agent_info.values() if info.category == category]
    
    def list_all_agents(self) -> List[AgentInfo]:
        """List all available agents"""
        return list(self.agent_info.values())
    
    def search_agents(self, query: str) -> List[AgentInfo]:
        """Search agents by capabilities or description"""
        query_lower = query.lower()
        results = []
        
        for info in self.agent_info.values():
            if (query_lower in info.description.lower() or 
                any(query_lower in cap.lower() for cap in info.capabilities) or
                query_lower in info.display_name.lower()):
                results.append(info)
        
        return results

class ChatManager:
    """Manages chat sessions and message routing"""
    
    def __init__(self, agent_registry: AgentRegistry):
        self.agent_registry = agent_registry
        self.active_sessions: Dict[str, ChatSession] = {}
        self.session_messages: Dict[str, List[ChatMessage]] = {}
        self.websocket_connections: Dict[str, WebSocket] = {}
    
    async def create_session(self, user_id: str, tenant_id: str, platform: str) -> ChatSession:
        """Create a new chat session"""
        session = ChatSession(
            user_id=user_id,
            tenant_id=tenant_id,
            platform=platform
        )
        
        self.active_sessions[session.session_id] = session
        self.session_messages[session.session_id] = []
        
        return session
    
    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get existing chat session"""
        return self.active_sessions.get(session_id)
    
    async def add_message(self, message: ChatMessage):
        """Add message to session"""
        if message.session_id not in self.session_messages:
            self.session_messages[message.session_id] = []
        
        self.session_messages[message.session_id].append(message)
        
        # Update session timestamp
        if message.session_id in self.active_sessions:
            self.active_sessions[message.session_id].updated_at = datetime.now(timezone.utc)
    
    async def get_session_messages(self, session_id: str, limit: int = 50) -> List[ChatMessage]:
        """Get messages for a session"""
        messages = self.session_messages.get(session_id, [])
        return messages[-limit:] if limit > 0 else messages
    
    async def route_message_to_agent(self, session_id: str, message: str, agent_name: Optional[str] = None) -> ChatResponse:
        """Route message to appropriate agent"""
        session = await self.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Auto-select agent if not specified
        if not agent_name:
            agent_name = await self._select_best_agent(message, session)
        
        # Get agent instance
        agent = self.agent_registry.get_agent(agent_name)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
        
        # Create task request
        task_request = AgentTaskRequest(
            tenant_id=session.tenant_id,
            user_id=session.user_id,
            task_type="chat_interaction",
            input_data={
                "message": message,
                "session_context": session.context,
                "platform": session.platform
            },
            priority=TaskPriority.NORMAL
        )
        
        try:
            # Execute agent task
            response = await agent.execute_task(task_request)
            
            # Create chat response
            chat_response = ChatResponse(
                message_id=str(uuid.uuid4()),
                response=response.result.get("response", "I'm here to help!"),
                agent_name=agent_name,
                suggestions=response.result.get("suggestions", []),
                actions=response.result.get("actions", []),
                metadata=response.result.get("metadata", {})
            )
            
            # Add agent response to session
            agent_message = ChatMessage(
                session_id=session_id,
                message_type=ChatMessageType.AGENT,
                content=chat_response.response,
                agent_name=agent_name
            )
            await self.add_message(agent_message)
            
            return chat_response
            
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            
            # Return error response
            error_response = ChatResponse(
                message_id=str(uuid.uuid4()),
                response=f"I'm having trouble processing your request right now. Please try again or contact support.",
                agent_name=agent_name,
                suggestions=["Try rephrasing your question", "Contact support", "Try a different agent"],
                metadata={"error": str(e)}
            )
            
            return error_response
    
    async def _select_best_agent(self, message: str, session: ChatSession) -> str:
        """Auto-select best agent based on message content"""
        message_lower = message.lower()
        
        # Keyword-based routing
        routing_rules = {
            "marketing_strategist": ["strategy", "marketing", "campaign", "plan", "growth"],
            "content_creator": ["content", "write", "copy", "blog", "social media"],
            "seo_specialist": ["seo", "search", "ranking", "keywords", "google"],
            "ecommerce_specialist": ["store", "shop", "ecommerce", "sales", "conversion"],
            "customer_support": ["help", "support", "issue", "problem", "question"],
            "digital_audit": ["audit", "analysis", "review", "evaluate", "assess"],
            "lead_scoring": ["leads", "prospects", "qualify", "score"],
        }
        
        for agent_name, keywords in routing_rules.items():
            if any(keyword in message_lower for keyword in keywords):
                return agent_name
        
        # Default to personal assistant for all general queries
        return "personal_assistant"

# Initialize global instances
agent_registry = AgentRegistry()
chat_manager = ChatManager(agent_registry)

# FastAPI app for chat endpoints
chat_app = FastAPI(
    title="Universal AI Chat Interface",
    description="Chat API for all 47+ AI agents across BizOSaaS platforms",
    version="1.0.0"
)

chat_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@chat_app.get("/agents", response_model=List[AgentInfo])
async def list_all_agents():
    """Get all available AI agents"""
    return agent_registry.list_all_agents()

@chat_app.get("/agents/categories/{category}", response_model=List[AgentInfo])
async def list_agents_by_category(category: AgentCategory):
    """Get agents by category"""
    return agent_registry.list_agents_by_category(category)

@chat_app.get("/agents/search")
async def search_agents(q: str):
    """Search agents by capabilities or description"""
    return agent_registry.search_agents(q)

@chat_app.get("/agents/{agent_name}", response_model=AgentInfo)
async def get_agent_info(agent_name: str):
    """Get specific agent information"""
    agent_info = agent_registry.get_agent_info(agent_name)
    if not agent_info:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent_info

@chat_app.post("/chat/sessions", response_model=ChatSession)
async def create_chat_session(user_id: str, tenant_id: str, platform: str = "web"):
    """Create a new chat session"""
    return await chat_manager.create_session(user_id, tenant_id, platform)

@chat_app.get("/chat/sessions/{session_id}", response_model=ChatSession)
async def get_chat_session(session_id: str):
    """Get chat session details"""
    session = await chat_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@chat_app.get("/chat/sessions/{session_id}/messages", response_model=List[ChatMessage])
async def get_session_messages(session_id: str, limit: int = 50):
    """Get messages for a chat session"""
    return await chat_manager.get_session_messages(session_id, limit)

@chat_app.post("/chat/message", response_model=ChatResponse)
async def send_chat_message(request: ChatRequest):
    """Send a message to an AI agent"""
    # Add user message to session
    user_message = ChatMessage(
        session_id=request.session_id,
        message_type=ChatMessageType.USER,
        content=request.message,
        user_id="user"  # TODO: Get from auth context
    )
    await chat_manager.add_message(user_message)
    
    # Route to agent and get response
    return await chat_manager.route_message_to_agent(
        request.session_id,
        request.message,
        request.agent_name
    )

@chat_app.post("/chat/sessions/{session_id}/agents")
async def select_session_agents(session_id: str, request: AgentSelectionRequest):
    """Select active agents for a session"""
    session = await chat_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Validate agent names
    invalid_agents = []
    for agent_name in request.agent_names:
        if not agent_registry.get_agent(agent_name):
            invalid_agents.append(agent_name)
    
    if invalid_agents:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid agents: {', '.join(invalid_agents)}"
        )
    
    # Update session
    session.active_agents = request.agent_names
    session.updated_at = datetime.now(timezone.utc)
    
    return {"status": "success", "active_agents": session.active_agents}

@chat_app.websocket("/chat/ws/{session_id}")
async def chat_websocket(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    
    # Store connection
    chat_manager.websocket_connections[session_id] = websocket
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process chat message
            request = ChatRequest(
                session_id=session_id,
                message=message_data["message"],
                agent_name=message_data.get("agent_name"),
                platform=message_data.get("platform", "web")
            )
            
            # Send to agent and get response
            response = await send_chat_message(request)
            
            # Send response back to client
            await websocket.send_text(json.dumps({
                "type": "agent_response",
                "data": response.dict()
            }))
            
    except WebSocketDisconnect:
        # Clean up connection
        if session_id in chat_manager.websocket_connections:
            del chat_manager.websocket_connections[session_id]
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Connection error occurred"
        }))

@chat_app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "total_agents": len(agent_registry.agents),
        "active_sessions": len(chat_manager.active_sessions),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }