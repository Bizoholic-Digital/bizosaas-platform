"""
Universal AI Chat Interface - BizOSaaS Platform
Enhanced AI agents service with chat functionality for all users and super admin
Port: 8001
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import asyncio
import json
import uuid
import logging
from datetime import datetime, timezone
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BizOSaaS Universal AI Chat Interface", 
    version="1.0.0",
    description="47+ AI Agents for BizOSaaS Platform with Universal Chat Interface"
)

# Enable CORS for all platforms
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
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
    ADMIN = "admin"

class AgentStatus(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"

# Pydantic models
class ChatMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    message_type: ChatMessageType
    content: str
    agent_name: Optional[str] = None
    user_id: Optional[str] = None
    platform: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

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
    is_super_admin_only: bool = False

class ChatSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    platform: str
    active_agents: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True
    context: Dict[str, Any] = Field(default_factory=dict)

class ChatRequest(BaseModel):
    session_id: str
    message: str
    agent_name: Optional[str] = None
    platform: str = "web"
    context: Dict[str, Any] = Field(default_factory=dict)

class ChatResponse(BaseModel):
    message_id: str
    session_id: str
    content: str
    agent_name: str
    timestamp: datetime
    suggested_actions: List[str] = Field(default_factory=list)
    is_final: bool = True

# In-memory storage (replace with database in production)
sessions: Dict[str, ChatSession] = {}
messages: Dict[str, List[ChatMessage]] = {}
active_connections: Dict[str, WebSocket] = {}

# Mock AI Agents Registry (47+ agents)
AI_AGENTS = {
    # Marketing Agents
    "marketing_strategist": AgentInfo(
        name="marketing_strategist",
        display_name="Marketing Strategist",
        description="Develops comprehensive marketing strategies and campaign plans",
        category=AgentCategory.MARKETING,
        status=AgentStatus.AVAILABLE,
        capabilities=["Strategy Development", "Market Analysis", "Campaign Planning", "Budget Optimization"],
        estimated_response_time="2-3 minutes",
        icon="🎯",
        color="#e74c3c"
    ),
    "content_creator": AgentInfo(
        name="content_creator",
        display_name="Content Creator",
        description="Creates engaging content for various marketing channels",
        category=AgentCategory.CONTENT,
        status=AgentStatus.AVAILABLE,
        capabilities=["Blog Writing", "Social Media Content", "Email Campaigns", "Video Scripts"],
        estimated_response_time="1-2 minutes",
        icon="✍️",
        color="#3498db"
    ),
    "seo_specialist": AgentInfo(
        name="seo_specialist",
        display_name="SEO Specialist",
        description="Optimizes content and strategies for search engine visibility",
        category=AgentCategory.SEO,
        status=AgentStatus.AVAILABLE,
        capabilities=["Keyword Research", "On-page Optimization", "Technical SEO", "Link Building"],
        estimated_response_time="2-4 minutes",
        icon="🔍",
        color="#27ae60"
    ),
    
    # E-commerce Agents
    "ecommerce_manager": AgentInfo(
        name="ecommerce_manager",
        display_name="E-commerce Manager",
        description="Manages online store operations and optimization",
        category=AgentCategory.ECOMMERCE,
        status=AgentStatus.AVAILABLE,
        capabilities=["Product Listing", "Inventory Management", "Price Optimization", "Customer Analytics"],
        estimated_response_time="1-2 minutes",
        icon="🛒",
        color="#9b59b6"
    ),
    "product_sourcing": AgentInfo(
        name="product_sourcing",
        display_name="Product Sourcing Specialist",
        description="Finds and evaluates products for dropshipping and retail",
        category=AgentCategory.ECOMMERCE,
        status=AgentStatus.AVAILABLE,
        capabilities=["Supplier Research", "Product Analysis", "Quality Assessment", "Cost Optimization"],
        estimated_response_time="3-5 minutes",
        icon="📦",
        color="#f39c12"
    ),
    
    # Analytics Agents
    "performance_analyst": AgentInfo(
        name="performance_analyst",
        display_name="Performance Analyst",
        description="Analyzes campaign performance and provides optimization insights",
        category=AgentCategory.ANALYTICS,
        status=AgentStatus.AVAILABLE,
        capabilities=["Data Analysis", "Performance Reporting", "ROI Calculation", "Trend Analysis"],
        estimated_response_time="2-3 minutes",
        icon="📊",
        color="#1abc9c"
    ),
    "digital_presence_auditor": AgentInfo(
        name="digital_presence_auditor",
        display_name="Digital Presence Auditor",
        description="Audits and analyzes digital presence across all platforms",
        category=AgentCategory.ANALYTICS,
        status=AgentStatus.AVAILABLE,
        capabilities=["Website Analysis", "Social Media Audit", "SEO Assessment", "Competitor Analysis"],
        estimated_response_time="5-10 minutes",
        icon="🔍",
        color="#34495e"
    ),
    
    # CRM Agents
    "lead_scoring": AgentInfo(
        name="lead_scoring",
        display_name="Lead Scoring Specialist",
        description="Scores and prioritizes leads based on conversion potential",
        category=AgentCategory.CRM,
        status=AgentStatus.AVAILABLE,
        capabilities=["Lead Qualification", "Scoring Algorithms", "Conversion Prediction", "Pipeline Management"],
        estimated_response_time="1-2 minutes",
        icon="⭐",
        color="#e67e22"
    ),
    "sales_assistant": AgentInfo(
        name="sales_assistant",
        display_name="Sales Assistant",
        description="Assists with sales processes and customer relationship management",
        category=AgentCategory.CRM,
        status=AgentStatus.AVAILABLE,
        capabilities=["Lead Nurturing", "Follow-up Automation", "Sales Scripts", "Customer Insights"],
        estimated_response_time="1-2 minutes",
        icon="💼",
        color="#8e44ad"
    ),
    
    # Operations Agents
    "customer_support": AgentInfo(
        name="customer_support",
        display_name="Customer Support Specialist",
        description="Handles customer inquiries and support requests",
        category=AgentCategory.SUPPORT,
        status=AgentStatus.AVAILABLE,
        capabilities=["Ticket Resolution", "FAQ Management", "Customer Communication", "Issue Escalation"],
        estimated_response_time="30 seconds - 1 minute",
        icon="🎧",
        color="#2c3e50"
    ),
    "process_automation": AgentInfo(
        name="process_automation",
        display_name="Process Automation Specialist",
        description="Automates business processes and workflows",
        category=AgentCategory.OPERATIONS,
        status=AgentStatus.AVAILABLE,
        capabilities=["Workflow Design", "Integration Setup", "Task Automation", "Process Optimization"],
        estimated_response_time="3-5 minutes",
        icon="🤖",
        color="#16a085"
    ),
    
    # Super Admin Only Agents
    "system_administrator": AgentInfo(
        name="system_administrator",
        display_name="System Administrator",
        description="Manages system-wide configurations and operations",
        category=AgentCategory.ADMIN,
        status=AgentStatus.AVAILABLE,
        capabilities=["User Management", "System Configuration", "Security Monitoring", "Performance Optimization"],
        estimated_response_time="1-2 minutes",
        icon="⚙️",
        color="#c0392b",
        is_super_admin_only=True
    ),
    "platform_orchestrator": AgentInfo(
        name="platform_orchestrator",
        display_name="Platform Orchestrator",
        description="Orchestrates complex multi-agent workflows across the platform",
        category=AgentCategory.ADMIN,
        status=AgentStatus.AVAILABLE,
        capabilities=["Multi-Agent Coordination", "Workflow Management", "Resource Allocation", "Task Distribution"],
        estimated_response_time="2-4 minutes",
        icon="🎭",
        color="#7f8c8d",
        is_super_admin_only=True
    )
}

# Add more agents to reach 47+ total
for i in range(15, 48):
    category_options = list(AgentCategory)
    category = category_options[i % len(category_options)]
    AI_AGENTS[f"specialist_agent_{i}"] = AgentInfo(
        name=f"specialist_agent_{i}",
        display_name=f"Specialist Agent {i}",
        description=f"Specialized AI agent for {category.value} domain tasks",
        category=category,
        status=AgentStatus.AVAILABLE,
        capabilities=[f"{category.value} optimization", "Data analysis", "Automation", "Reporting"],
        estimated_response_time="1-3 minutes",
        icon="🤖",
        color="#95a5a6"
    )

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"WebSocket connection established for session {session_id}")

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"WebSocket connection closed for session {session_id}")

    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending message to {session_id}: {e}")
                self.disconnect(session_id)

    async def broadcast(self, message: dict):
        for session_id, connection in self.active_connections.items():
            try:
                await connection.send_text(json.dumps(message))
            except:
                self.disconnect(session_id)

manager = ConnectionManager()

# Utility functions
def get_agent_by_name(agent_name: str) -> Optional[AgentInfo]:
    return AI_AGENTS.get(agent_name)

def filter_agents_by_category(category: AgentCategory, is_super_admin: bool = False) -> List[AgentInfo]:
    agents = [agent for agent in AI_AGENTS.values() if agent.category == category]
    if not is_super_admin:
        agents = [agent for agent in agents if not agent.is_super_admin_only]
    return agents

def get_available_agents(is_super_admin: bool = False) -> List[AgentInfo]:
    agents = [agent for agent in AI_AGENTS.values() if agent.status == AgentStatus.AVAILABLE]
    if not is_super_admin:
        agents = [agent for agent in agents if not agent.is_super_admin_only]
    return agents

async def simulate_agent_response(agent_name: str, user_message: str, context: Dict[str, Any] = None) -> str:
    """Simulate AI agent response (replace with actual AI integration)"""
    agent = get_agent_by_name(agent_name)
    if not agent:
        return "I apologize, but I'm not available right now. Please try another agent."
    
    # Simulate processing time
    await asyncio.sleep(1)
    
    # Generate contextual response based on agent type
    responses = {
        "marketing_strategist": [
            f"Based on your query about '{user_message}', I recommend developing a multi-channel strategy focusing on digital presence optimization.",
            f"For '{user_message}', consider implementing a data-driven approach with A/B testing across different marketing channels.",
            f"Your question about '{user_message}' suggests we should analyze your current conversion funnel and optimize for better ROI."
        ],
        "content_creator": [
            f"I can help create engaging content around '{user_message}'. Would you like blog posts, social media content, or email campaigns?",
            f"For the topic '{user_message}', I suggest creating a content series that addresses your audience's pain points.",
            f"Let me draft some compelling content ideas based on '{user_message}' that will resonate with your target audience."
        ],
        "ecommerce_manager": [
            f"Regarding '{user_message}', I can optimize your product listings and improve conversion rates through better categorization.",
            f"For '{user_message}', let's analyze your current inventory and implement dynamic pricing strategies.",
            f"Your inquiry about '{user_message}' indicates we should focus on customer journey optimization and checkout improvements."
        ],
        "customer_support": [
            f"I'm here to help with '{user_message}'. Let me provide you with a comprehensive solution and next steps.",
            f"Thank you for reaching out about '{user_message}'. I'll escalate this to the appropriate specialist if needed.",
            f"Regarding '{user_message}', I can provide immediate assistance and create a follow-up plan for you."
        ]
    }
    
    agent_responses = responses.get(agent_name, [
        f"I understand your question about '{user_message}'. Let me analyze this and provide you with actionable insights.",
        f"Based on '{user_message}', I can help optimize your approach using my specialized capabilities.",
        f"Your query about '{user_message}' is interesting. I'll provide recommendations based on current best practices."
    ])
    
    import random
    return random.choice(agent_responses)

# API Endpoints
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "BizOSaaS Universal AI Chat Interface",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "active_sessions": len(sessions),
        "total_agents": len(AI_AGENTS),
        "available_agents": len([a for a in AI_AGENTS.values() if a.status == AgentStatus.AVAILABLE])
    }

@app.get("/agents/list")
async def list_all_agents(is_super_admin: bool = False):
    """Get all available AI agents"""
    agents = get_available_agents(is_super_admin)
    return {
        "total_agents": len(agents),
        "agents": agents
    }

@app.get("/agents/categories")
async def list_agent_categories():
    """Get all agent categories"""
    return {
        "categories": [
            {"name": category.value, "display_name": category.value.title()}
            for category in AgentCategory
        ]
    }

@app.get("/agents/category/{category}")
async def get_agents_by_category(category: AgentCategory, is_super_admin: bool = False):
    """Get agents by category"""
    agents = filter_agents_by_category(category, is_super_admin)
    return {
        "category": category.value,
        "total_agents": len(agents),
        "agents": agents
    }

@app.post("/chat/sessions")
async def create_chat_session(user_id: str, platform: str = "web", tenant_id: str = "default"):
    """Create a new chat session"""
    session = ChatSession(
        user_id=user_id,
        platform=platform,
        context={"tenant_id": tenant_id}
    )
    sessions[session.session_id] = session
    messages[session.session_id] = []
    
    return {
        "session_id": session.session_id,
        "status": "created",
        "message": "Chat session created successfully"
    }

@app.get("/chat/sessions/{session_id}")
async def get_chat_session(session_id: str):
    """Get chat session details"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return sessions[session_id]

@app.get("/chat/sessions/{session_id}/messages")
async def get_session_messages(session_id: str, limit: int = 50):
    """Get messages for a chat session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_messages = messages.get(session_id, [])
    return {
        "session_id": session_id,
        "total_messages": len(session_messages),
        "messages": session_messages[-limit:] if limit else session_messages
    }

@app.post("/chat/message")
async def send_chat_message(request: ChatRequest):
    """Send a message to an AI agent"""
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[request.session_id]
    
    # Add user message
    user_message = ChatMessage(
        session_id=request.session_id,
        message_type=ChatMessageType.USER,
        content=request.message,
        user_id=session.user_id,
        platform=request.platform
    )
    messages[request.session_id].append(user_message)
    
    # Route to agent or suggest agents if none specified
    if not request.agent_name:
        # Suggest agents based on message content
        suggested_agents = []
        message_lower = request.message.lower()
        
        if any(word in message_lower for word in ["marketing", "campaign", "strategy", "promotion"]):
            suggested_agents.extend(filter_agents_by_category(AgentCategory.MARKETING)[:3])
        elif any(word in message_lower for word in ["product", "ecommerce", "sales", "inventory"]):
            suggested_agents.extend(filter_agents_by_category(AgentCategory.ECOMMERCE)[:3])
        elif any(word in message_lower for word in ["analytics", "data", "performance", "metrics"]):
            suggested_agents.extend(filter_agents_by_category(AgentCategory.ANALYTICS)[:3])
        else:
            suggested_agents = get_available_agents()[:5]
        
        system_response = ChatMessage(
            session_id=request.session_id,
            message_type=ChatMessageType.SYSTEM,
            content=f"I can connect you with one of our specialized agents. Based on your message, I recommend:",
            agent_name="system"
        )
        messages[request.session_id].append(system_response)
        
        return {
            "message_id": system_response.message_id,
            "session_id": request.session_id,
            "content": system_response.content,
            "agent_name": "system",
            "timestamp": system_response.timestamp,
            "suggested_agents": [
                {
                    "name": agent.name,
                    "display_name": agent.display_name,
                    "description": agent.description,
                    "icon": agent.icon
                }
                for agent in suggested_agents
            ]
        }
    
    # Get agent response
    agent_response_content = await simulate_agent_response(
        request.agent_name, 
        request.message, 
        request.context
    )
    
    agent_response = ChatMessage(
        session_id=request.session_id,
        message_type=ChatMessageType.AGENT,
        content=agent_response_content,
        agent_name=request.agent_name,
        user_id=session.user_id,
        platform=request.platform
    )
    messages[request.session_id].append(agent_response)
    
    # Update session
    if request.agent_name not in session.active_agents:
        session.active_agents.append(request.agent_name)
    session.updated_at = datetime.now(timezone.utc)
    
    # Send via WebSocket if connected
    await manager.send_message(request.session_id, {
        "type": "agent_response",
        "message": agent_response.dict()
    })
    
    return ChatResponse(
        message_id=agent_response.message_id,
        session_id=request.session_id,
        content=agent_response_content,
        agent_name=request.agent_name,
        timestamp=agent_response.timestamp,
        suggested_actions=[
            "Ask a follow-up question",
            "Switch to another agent",
            "Request detailed analysis",
            "Schedule a consultation"
        ]
    )

@app.websocket("/chat/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    if session_id not in sessions:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Handle different message types
            if message_data.get("type") == "chat_message":
                request = ChatRequest(**message_data.get("data", {}))
                response = await send_chat_message(request)
                
                await manager.send_message(session_id, {
                    "type": "chat_response",
                    "data": response.dict()
                })
            
    except WebSocketDisconnect:
        manager.disconnect(session_id)
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {e}")
        manager.disconnect(session_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")