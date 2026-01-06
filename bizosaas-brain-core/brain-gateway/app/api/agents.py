from fastapi import APIRouter, HTTPException, Body, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.agent import Agent
from domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/agents", tags=["ai-agents"])

# Agent definitions
class AgentConfig(BaseModel):
    id: str
    name: str
    description: str
    role: str
    capabilities: List[str]
    tools: List[str]
    icon: str
    color: str

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    agent_id: str
    message: str
    suggestions: List[str] = []
    actions: List[Dict[str, Any]] = []

# Define the 7 specialized AI agents
AGENTS = [
    AgentConfig(
        id="marketing-strategist",
        name="Marketing Strategist",
        description="Analyzes campaigns, suggests improvements, and creates marketing strategies",
        role="Marketing & Growth Expert",
        capabilities=[
            "Campaign analysis",
            "A/B testing recommendations",
            "Audience segmentation",
            "Content strategy",
            "ROI optimization"
        ],
        tools=["google-ads", "facebook-ads", "google-analytics", "mailchimp"],
        icon="📊",
        color="#FF6B6B"
    ),
    AgentConfig(
        id="content-creator",
        name="Content Creator",
        description="Generates blog posts, social media content, and marketing copy",
        role="Content Generation Specialist",
        capabilities=[
            "Blog post writing",
            "Social media content",
            "Email campaigns",
            "SEO optimization",
            "Content calendars"
        ],
        tools=["wordpress", "mailchimp", "google-docs"],
        icon="✍️",
        color="#4ECDC4"
    ),
    AgentConfig(
        id="sales-assistant",
        name="Sales Assistant",
        description="Manages leads, tracks deals, and provides sales insights",
        role="Sales & CRM Expert",
        capabilities=[
            "Lead qualification",
            "Deal tracking",
            "Sales forecasting",
            "Pipeline management",
            "Follow-up automation"
        ],
        tools=["fluentcrm", "zoho-crm", "pipedrive"],
        icon="💼",
        color="#95E1D3"
    ),
    AgentConfig(
        id="customer-support",
        name="Customer Support",
        description="Handles customer inquiries and provides support recommendations",
        role="Customer Success Specialist",
        capabilities=[
            "Ticket triage",
            "Response suggestions",
            "Knowledge base search",
            "Sentiment analysis",
            "Escalation detection"
        ],
        tools=["zendesk", "intercom", "freshdesk"],
        icon="🎧",
        color="#A8E6CF"
    ),
    AgentConfig(
        id="data-analyst",
        name="Data Analyst",
        description="Analyzes business data and provides actionable insights",
        role="Business Intelligence Expert",
        capabilities=[
            "Data visualization",
            "Trend analysis",
            "Performance metrics",
            "Predictive analytics",
            "Custom reports"
        ],
        tools=["google-analytics", "google-sheets", "stripe"],
        icon="📈",
        color="#FFD93D"
    ),
    AgentConfig(
        id="ecommerce-optimizer",
        name="E-commerce Optimizer",
        description="Optimizes product listings, pricing, and inventory",
        role="E-commerce Specialist",
        capabilities=[
            "Product optimization",
            "Pricing strategies",
            "Inventory management",
            "Conversion optimization",
            "Abandoned cart recovery"
        ],
        tools=["woocommerce", "shopify", "stripe"],
        icon="🛒",
        color="#C7CEEA"
    ),
    AgentConfig(
        id="workflow-automator",
        name="Workflow Automator",
        description="Creates and manages automated workflows across platforms",
        role="Automation Specialist",
        capabilities=[
            "Workflow design",
            "Integration setup",
            "Task automation",
            "Trigger configuration",
            "Process optimization"
        ],
        tools=["zapier", "make", "n8n", "temporal"],
        icon="⚙️",
        color="#B4A7D6"
    )
]

# Mock conversation storage
conversations: Dict[str, List[ChatMessage]] = {}

@router.get("/", response_model=List[Dict[str, Any]])
async def list_agents(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List all available AI agents (System + Custom)"""
    tenant_id = user.tenant_id or "default_tenant"
    
    # Get custom agents from DB
    custom_agents = db.query(Agent).filter(Agent.tenant_id == tenant_id).all()
    custom_agents_dict = [a.to_dict() for a in custom_agents]
    
    # Combine with system agents
    system_agents_dict = [a.dict() for a in AGENTS]
    for sa in system_agents_dict:
        sa["is_system"] = True
        
    return system_agents_dict + custom_agents_dict

@router.post("/", response_model=Dict[str, Any])
async def create_agent(
    agent_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Create a new custom AI agent"""
    tenant_id = user.tenant_id or "default_tenant"
    
    new_agent = Agent(
        tenant_id=tenant_id,
        name=agent_data.get("name"),
        description=agent_data.get("description"),
        role=agent_data.get("role"),
        category=agent_data.get("category", "general"),
        capabilities=agent_data.get("capabilities", []),
        tools=agent_data.get("tools", []),
        icon=agent_data.get("icon", "🤖"),
        color=agent_data.get("color", "#4f46e5"),
        instructions=agent_data.get("instructions"),
        created_by=user.email
    )
    
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    
    return new_agent.to_dict()

@router.get("/{agent_id}")
async def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Get specific agent details"""
    # Check system agents first
    agent = next((a for a in AGENTS if a.id == agent_id), None)
    if agent:
        data = agent.dict()
        data["is_system"] = True
        return data
        
    # Check custom agents
    tenant_id = user.tenant_id or "default_tenant"
    custom_agent = db.query(Agent).filter(Agent.id == agent_id, Agent.tenant_id == tenant_id).first()
    if not custom_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    return custom_agent.to_dict()

@router.post("/{agent_id}/chat", response_model=ChatResponse)
async def chat_with_agent(
    agent_id: str,
    request: ChatRequest = Body(...)
):
    """Chat with a specific AI agent"""
    agent = next((a for a in AGENTS if a.id == agent_id), None)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Store user message
    conversation_id = f"user_default:{agent_id}"
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    
    conversations[conversation_id].append(ChatMessage(
        role="user",
        content=request.message,
        timestamp=datetime.utcnow()
    ))
    
    # Generate response based on agent type
    response_message = generate_agent_response(agent, request.message, request.context)
    
    conversations[conversation_id].append(ChatMessage(
        role="assistant",
        content=response_message,
        timestamp=datetime.utcnow()
    ))
    
    # Generate suggestions and actions
    suggestions = generate_suggestions(agent, request.message)
    actions = generate_actions(agent, request.message)
    
    return ChatResponse(
        agent_id=agent_id,
        message=response_message,
        suggestions=suggestions,
        actions=actions
    )

@router.get("/{agent_id}/history")
async def get_conversation_history(agent_id: str, user_id: str = "default"):
    """Get conversation history with an agent"""
    conversation_id = f"user_{user_id}:{agent_id}"
    if conversation_id not in conversations:
        return []
    return conversations[conversation_id]

@router.delete("/{agent_id}/history")
async def clear_conversation_history(agent_id: str, user_id: str = "default"):
    """Clear conversation history with an agent"""
    conversation_id = f"user_{user_id}:{agent_id}"
    if conversation_id in conversations:
        del conversations[conversation_id]
    return {"status": "cleared"}

from app.models.agent import Agent, AgentOptimization
from app.services.agent_service import AgentService

@router.get("/optimizations", response_model=List[Dict[str, Any]])
async def list_optimizations(
    agent_id: Optional[str] = None,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List all AI-suggested agent optimizations"""
    optimizations = AgentService.get_agent_optimizations(db, agent_id)
    return [opt.to_dict() for opt in optimizations]

@router.post("/{agent_id}/optimizations/generate", response_model=List[Dict[str, Any]])
async def generate_optimizations(
    agent_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Manually trigger agent optimization analysis (Mocked)"""
    new_optimizations = AgentService.create_mock_optimizations(db, agent_id)
    return [opt.to_dict() for opt in new_optimizations]

@router.post("/optimizations/{optimization_id}/approve", response_model=Dict[str, Any])
async def approve_optimization(
    optimization_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Approve an optimization for execution"""
    opt = AgentService.approve_optimization(db, optimization_id)
    if not opt:
        raise HTTPException(status_code=404, detail="Optimization not found")
    return opt.to_dict()

@router.post("/optimizations/{optimization_id}/toggle-auto", response_model=Dict[str, Any])
async def toggle_auto_optimization(
    optimization_id: str,
    enabled: bool = Body(..., embed=True),
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Enable/Disable auto-execution for an optimization"""
    opt = AgentService.toggle_auto_execute(db, optimization_id, enabled)
    if not opt:
        raise HTTPException(status_code=404, detail="Optimization not found")
    return opt.to_dict()

# Helper functions
def generate_agent_response(agent: AgentConfig, message: str, context: Optional[Dict] = None) -> str:
    """Generate contextual response based on agent type"""
    message_lower = message.lower()
    
    if agent.id == "marketing-strategist":
        if "campaign" in message_lower or "ads" in message_lower:
            return "I've analyzed your recent campaigns. I notice your Google Ads CTR is below industry average. I recommend testing new ad copy focusing on your unique value proposition and targeting more specific keywords."
        elif "strategy" in message_lower:
            return "Based on your business goals, I suggest a multi-channel approach: 1) Increase content marketing for SEO, 2) Launch retargeting campaigns for abandoned carts, 3) Implement email nurture sequences for leads."
        else:
            return f"I'm your Marketing Strategist. I can help you with campaign analysis, audience targeting, and growth strategies. What would you like to optimize today?"
    
    elif agent.id == "content-creator":
        if "blog" in message_lower or "post" in message_lower:
            return "I can help you create engaging blog content. What topic would you like to write about? I'll generate an SEO-optimized outline with keyword suggestions."
        elif "social" in message_lower:
            return "For social media, I recommend posting 3-5 times per week with a mix of educational content (40%), promotional (30%), and engaging/entertaining posts (30%). Would you like me to draft some posts?"
        else:
            return "I'm your Content Creator. I can generate blog posts, social media content, email campaigns, and more. What type of content do you need?"
    
    elif agent.id == "sales-assistant":
        if "lead" in message_lower:
            return "I've reviewed your leads. You have 15 hot leads that haven't been contacted in 3+ days. I recommend prioritizing follow-ups with leads who visited your pricing page multiple times."
        elif "deal" in message_lower or "pipeline" in message_lower:
            return "Your sales pipeline shows $45K in deals at proposal stage. I suggest sending personalized follow-ups to the 3 deals that have been stalled for over 2 weeks."
        else:
            return "I'm your Sales Assistant. I can help with lead management, deal tracking, and sales forecasting. How can I help boost your sales today?"
    
    elif agent.id == "customer-support":
        if "ticket" in message_lower:
            return "I've analyzed recent support tickets. Common issues: 1) Login problems (25%), 2) Billing questions (20%), 3) Feature requests (15%). I can draft responses for the urgent tickets."
        else:
            return "I'm your Customer Support specialist. I can help triage tickets, suggest responses, and identify trends in customer issues. What would you like to know?"
    
    elif agent.id == "data-analyst":
        if "report" in message_lower or "analytics" in message_lower:
            return "Based on your Google Analytics data: Traffic is up 15% this month, but bounce rate increased to 65%. I recommend improving page load speed and adding more internal links to keep visitors engaged."
        else:
            return "I'm your Data Analyst. I can analyze your business metrics, create reports, and provide actionable insights. What data would you like me to analyze?"
    
    elif agent.id == "ecommerce-optimizer":
        if "product" in message_lower:
            return "I've analyzed your product catalog. Top performers are in the 'Electronics' category. I recommend optimizing product descriptions with more keywords and adding customer reviews to boost conversions."
        elif "price" in message_lower or "pricing" in message_lower:
            return "Your pricing is competitive, but I notice 30% cart abandonment. Consider offering free shipping over $50 or a first-time buyer discount to improve conversion."
        else:
            return "I'm your E-commerce Optimizer. I can help with product optimization, pricing strategies, and conversion improvements. What aspect of your store would you like to optimize?"
    
    elif agent.id == "workflow-automator":
        if "automate" in message_lower or "workflow" in message_lower:
            return "I can help automate repetitive tasks. Common workflows: 1) Auto-add new leads to CRM, 2) Send welcome emails to new customers, 3) Sync orders to accounting software. Which would you like to set up?"
        else:
            return "I'm your Workflow Automator. I can create automated workflows across your connected platforms. What process would you like to automate?"
    
    return f"I'm {agent.name}. {agent.description}. How can I assist you today?"

def generate_suggestions(agent: AgentConfig, message: str) -> List[str]:
    """Generate contextual suggestions"""
    base_suggestions = [
        f"Show me {agent.name.lower()} insights",
        "What can you help me with?",
        "Analyze my recent data"
    ]
    
    if agent.id == "marketing-strategist":
        return ["Analyze my campaigns", "Suggest A/B tests", "Review my audience targeting"]
    elif agent.id == "content-creator":
        return ["Generate blog post ideas", "Create social media content", "Draft email campaign"]
    elif agent.id == "sales-assistant":
        return ["Show hot leads", "Review pipeline", "Forecast this month's sales"]
    elif agent.id == "data-analyst":
        return ["Create performance report", "Show key metrics", "Identify trends"]
    
    return base_suggestions

def generate_actions(agent: AgentConfig, message: str) -> List[Dict[str, Any]]:
    """Generate actionable items"""
    actions = []
    
    if "campaign" in message.lower():
        actions.append({
            "type": "create_campaign",
            "label": "Create New Campaign",
            "connector": "google-ads"
        })
    
    if "post" in message.lower() or "content" in message.lower():
        actions.append({
            "type": "create_post",
            "label": "Create Blog Post",
            "connector": "wordpress"
        })
    
    if "lead" in message.lower():
        actions.append({
            "type": "view_leads",
            "label": "View All Leads",
            "connector": "fluentcrm"
        })
    
    return actions
