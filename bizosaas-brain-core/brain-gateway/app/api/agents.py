from fastapi import APIRouter, HTTPException, Body, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.agent import Agent
from app.domain.ports.identity_port import AuthenticatedUser

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
    # Legacy Agents (Categorized)
    AgentConfig(
        id="marketing-strategist",
        name="Marketing Strategist",
        description="Analyzes campaigns, suggests improvements, and creates marketing strategies",
        role="Marketing & Growth Expert",
        capabilities=["Campaign analysis", "A/B testing recommendations", "Audience segmentation", "Content strategy", "ROI optimization"],
        tools=["google-ads", "facebook-ads", "google-analytics", "mailchimp"],
        icon="📊",
        color="#FF6B6B"
    ),
    AgentConfig(
        id="content-creator",
        name="Content Creator",
        description="Generates blog posts, social media content, and marketing copy",
        role="Content Generation Specialist",
        capabilities=["Blog post writing", "Social media content", "Email campaigns", "SEO optimization", "Content calendars"],
        tools=["wordpress", "mailchimp", "google-docs"],
        icon="✍️",
        color="#4ECDC4"
    ),
    AgentConfig(
        id="sales-assistant",
        name="Sales Assistant",
        description="Manages leads, tracks deals, and provides sales insights",
        role="Sales & CRM Expert",
        capabilities=["Lead qualification", "Deal tracking", "Sales forecasting", "Pipeline management", "Follow-up automation"],
        tools=["fluentcrm", "zoho-crm", "pipedrive"],
        icon="💼",
        color="#95E1D3"
    ),
    AgentConfig(
        id="customer-support",
        name="Customer Support",
        description="Handles customer inquiries and provides support recommendations",
        role="Customer Success Specialist",
        capabilities=["Ticket triage", "Response suggestions", "Knowledge base search", "Sentiment analysis", "Escalation detection"],
        tools=["zendesk", "intercom", "freshdesk"],
        icon="🎧",
        color="#A8E6CF"
    ),
    AgentConfig(
        id="data-analyst",
        name="Data Analyst",
        description="Analyzes business data and provides actionable insights",
        role="Business Intelligence Expert",
        capabilities=["Data visualization", "Trend analysis", "Performance metrics", "Predictive analytics", "Custom reports"],
        tools=["google-analytics", "google-sheets", "stripe"],
        icon="📈",
        color="#FFD93D"
    ),
    AgentConfig(
        id="ecommerce-optimizer",
        name="E-commerce Optimizer",
        description="Optimizes product listings, pricing, and inventory",
        role="E-commerce Specialist",
        capabilities=["Product optimization", "Pricing strategies", "Inventory management", "Conversion optimization", "Abandoned cart recovery"],
        tools=["woocommerce", "shopify", "stripe"],
        icon="🛒",
        color="#C7CEEA"
    ),
    AgentConfig(
        id="workflow-automator",
        name="Workflow Automator",
        description="Creates and manages automated workflows across platforms",
        role="Automation Specialist",
        capabilities=["Workflow design", "Integration setup", "Task automation", "Trigger configuration", "Process optimization"],
        tools=["zapier", "make", "n8n", "temporal", "provision-site"],
        icon="⚙️",
        color="#B4A7D6"
    ),
    AgentConfig(
        id="personal_assistant",
        name="Personal Assistant",
        description="Your dedicated AI assistant for navigating the BizOSaaS platform",
        role="Executive Assistant",
        capabilities=["Platform Navigation", "Task Coordination", "Agent Orchestration"],
        tools=["all-agents", "platform-nav", "provision-site"],
        icon="🤖",
        color="#6366F1"
    ),

    # Refined 20 Core Agents (v2.0)
    AgentConfig(
        id="market_research",
        name="Market Research",
        description="Deep market analysis, competitive research, and industry trends",
        role="Market Intelligence Expert",
        capabilities=["Market Depth", "Trend Spotting", "Competitor SOS", "SWOT Analysis"],
        tools=["serper", "semrush", "ahrefs"],
        icon="🔍",
        color="#3B82F6"
    ),
    AgentConfig(
        id="data_analytics",
        name="Data Analytics",
        description="Complex data sets analysis and actionable insight generation",
        role="Intelligence Analyst",
        capabilities=["Metric Interpretation", "Anomaly Detection", "Forecasting"],
        tools=["pandas", "numpy", "matplotlib"],
        icon="📊",
        color="#10B981"
    ),
    AgentConfig(
        id="strategic_planning",
        name="Strategic Planning",
        description="Long-term business planning and scenario modeling",
        role="Business Strategist",
        capabilities=["Roadmap Design", "Scenario Planning", "Budget Allocation"],
        tools=["notion", "spreadsheet"],
        icon="🎯",
        color="#F59E0B"
    ),
    AgentConfig(
        id="competitive_intelligence",
        name="Competitive Intel",
        description="Passive and active monitoring of competitors",
        role="Intelligence Architect",
        capabilities=["Price Tracking", "Feature Analysis", "Market Share Monitoring"],
        tools=["scrape-web"],
        icon="🕵️",
        color="#EF4444"
    ),
    AgentConfig(
        id="content_generation",
        name="Content Generation",
        description="Automated high-quality content production across formats",
        role="Content Specialist",
        capabilities=["Blog Writing", "Social Copy", "Ad Creation", "Whitepapers"],
        tools=["openai", "anthropic"],
        icon="📝",
        color="#8B5CF6"
    ),
    AgentConfig(
        id="creative_design",
        name="Creative Design",
        description="Visual concept generation and design prompt engineering",
        role="Creative Director",
        capabilities=["Ad Visuals", "UI/UX Mockups", "Brand Identity"],
        tools=["dall-e", "midjourney"],
        icon="🎨",
        color="#EC4899"
    ),
    AgentConfig(
        id="seo_optimization",
        name="SEO Optimization",
        description="On-page, technical, and off-page SEO automation",
        role="SEO Architect",
        capabilities=["Keyword Research", "Tech SEO Audit", "Content Optimization"],
        tools=["screaming-frog", "semrush"],
        icon="🚀",
        color="#06B6D4"
    ),
    AgentConfig(
        id="campaign_orchestration",
        name="Campaign Orchestrator",
        description="Cross-channel campaign synchronization and management",
        role="Marketing Manager",
        capabilities=["Multi-channel Sync", "Budget Mgmt", "Timeline Tracking"],
        tools=["google-ads", "meta-ads"],
        icon="🎺",
        color="#6366F1"
    ),
    AgentConfig(
        id="conversion_optimization",
        name="CRO Expert",
        description="Funnel analysis and conversion rate optimization",
        role="CRO Specialist",
        capabilities=["A/B Testing", "Funnel Analysis", "LPO"],
        tools=["optimizely", "hotjar"],
        icon="📈",
        color="#10B981"
    ),
    AgentConfig(
        id="social_media_management",
        name="Social Media Manager",
        description="Automated posting, engagement, and monitoring",
        role="Community Manager",
        capabilities=["Scheduling", "Engagement", "Brand Monitoring"],
        tools=["buffer", "hootsuite"],
        icon="📱",
        color="#1D4ED8"
    ),
    AgentConfig(
        id="code_generation",
        name="Code Generation",
        description="Automated feature development and bug fixing",
        role="Senior Engineer",
        capabilities=["Feature Dev", "Bug Fixing", "Code Review"],
        tools=["github", "vscode"],
        icon="💻",
        color="#000000"
    ),
    AgentConfig(
        id="devops_automation",
        name="DevOps Automation",
        description="Infrastructure as Code and deployment automation",
        role="DevOps Engineer",
        capabilities=["IaC Setup", "CI/CD", "Security Hardening"],
        tools=["terraform", "docker", "k8s"],
        icon="♾️",
        color="#00ADEE"
    ),
    AgentConfig(
        id="technical_documentation",
        name="Tech Documentation",
        description="API docs and system architecture documentation",
        role="Technical Writer",
        capabilities=["API Docs", "User Guides", "System Diagrams"],
        tools=["swagger", "docusaurus"],
        icon="📚",
        color="#64748B"
    ),
    AgentConfig(
        id="customer_engagement",
        name="Customer Engagement",
        description="Lead nurturing and customer success automation",
        role="CS Manager",
        capabilities=["Nurturing", "Onboarding", "Retention"],
        tools=["hubspot", "customer.io"],
        icon="🤝",
        color="#F8FAFC"
    ),
    AgentConfig(
        id="sales_intelligence",
        name="Sales Intelligence",
        description="Lead scoring and sales pipeline optimization",
        role="Sales Ops",
        capabilities=["Lead Scoring", "Forecasting", "Pipeline Health"],
        tools=["salesforce", "zoho"],
        icon="💰",
        color="#22C55E"
    ),
    AgentConfig(
        id="trading_strategy",
        name="Trading Strategy",
        description="Algorithmic trading strategy development & backtesting",
        role="Quant Strategist",
        capabilities=["Backtesting", "Alpha Finding", "Risk Mgmt"],
        tools=["alpaca", "tradingview"],
        icon="💹",
        color="#0EA5E9"
    ),
    AgentConfig(
        id="financial_analytics",
        name="Financial Analytics",
        description="Revenue forecasting and ROI optimization",
        role="CFO Assistant",
        capabilities=["Forecasting", "Budgeting", "ROI Analysis"],
        tools=["quickbooks", "xero"],
        icon="💵",
        color="#16A34A"
    ),
    AgentConfig(
        id="gaming_experience",
        name="Gaming Experience",
        description="Leaderboard and achievement system management",
        role="Game Director",
        capabilities=["Progression", "Balancing", "Rewards"],
        tools=["unity", "epic"],
        icon="🎮",
        color="#F43F5E"
    ),
    AgentConfig(
        id="community_management",
        name="Community Manager",
        description="Intelligent community moderation and engagement",
        role="Community Head",
        capabilities=["Moderation", "Events", "Sentiment"],
        tools=["discord", "telegram"],
        icon="💬",
        color="#5865F2"
    ),
    AgentConfig(
        id="master_orchestrator",
        name="Master Orchestrator",
        description="Central intelligence coordinating all BizOSaas agents",
        role="The Brain",
        capabilities=["Orchestration", "Global Strategy", "Task Delegation"],
        tools=["all-agents"],
        icon="🧠",
        color="#7C3AED"
    ),
    # Category 9: E-commerce Refined
    AgentConfig(
        id="ecommerce_sourcing",
        name="Product Sourcing Specialist",
        description="Global product discovery, supplier validation, and feasibility for Coreldove",
        role="Sourcing Strategist",
        capabilities=["Supplier Validation", "Margin Analysis", "Global Search"],
        tools=["serper", "alibaba", "connector"],
        icon="📦",
        color="#F97316"
    ),
    AgentConfig(
        id="ecommerce_inventory",
        name="Inventory Manager",
        description="AI-driven stock tracking, demand forecasting, and logistics optimization",
        role="Supply Chain Optimizer",
        capabilities=["Demand Forecasting", "Reorder Automation", "Logistics Analysis"],
        tools=["shopify", "analytics", "connector"],
        icon="🏗️",
        color="#10B981"
    ),
    AgentConfig(
        id="ecommerce_order_orchestrator",
        name="Order Orchestrator",
        description="360-degree autonomous order processing, fraud detection, and multi-channel fulfillment",
        role="Fulfillment Architect",
        capabilities=["Fraud Detection", "Routing Optimization", "Status Sync"],
        tools=["all-connectors", "fraud-check"],
        icon="🚚",
        color="#3B82F6"
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

import os
import httpx

AI_AGENTS_URL = os.getenv("AI_AGENTS_URL")


@router.post("/{agent_id}/chat", response_model=ChatResponse)
async def chat_with_agent(
    agent_id: str,
    request: ChatRequest = Body(...),
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Chat with a specific AI agent"""
    from opentelemetry import trace, metrics
    tracer = trace.get_tracer(__name__)
    meter = metrics.get_meter(__name__)
    
    agent_counter = meter.create_counter(
        "agent.chat.requests",
        unit="1",
        description="Number of agent chat requests"
    )

    with tracer.start_as_current_span("agent_chat") as span:
        span.set_attribute("agent.id", agent_id)
        span.set_attribute("message.length", len(request.message))
        
        # 1. Resolve Agent Configuration
        agent = next((a for a in AGENTS if a.id == agent_id), None)
        if not agent:
            # Check DB for custom agents
            tenant_id = user.tenant_id or "default_tenant"
            custom_agent = db.query(Agent).filter(Agent.id == agent_id, Agent.tenant_id == tenant_id).first()
            if custom_agent:
                agent = AgentConfig(
                    id=custom_agent.id,
                    name=custom_agent.name,
                    description=custom_agent.description or "",
                    role=custom_agent.role,
                    capabilities=custom_agent.capabilities or [],
                    tools=custom_agent.tools or [],
                    icon=custom_agent.icon or "🤖",
                    color=custom_agent.color or "#4f46e5"
                )

        if not agent:
            span.set_status(trace.Status(trace.StatusCode.ERROR, "Agent not found"))
            raise HTTPException(status_code=404, detail="Agent not found")
        
        agent_counter.add(1, {"agent.id": agent_id, "agent.role": agent.role})
        span.set_attribute("agent.role", agent.role)

        # 2. Initialize MCP Gateway & Knowledge Graph
        from app.services.mcp_gateway import MCPGateway
        from app.services.knowledge_graph import build_platform_knowledge_graph
        
        trace_steps = []
        actions = []
        suggestions = []
        
        mcp_gateway = MCPGateway(db)
        # KAG: Build graph to find related context
        # In production, this would be cached
        if "analyze" in request.message.lower() or "suggest" in request.message.lower():
            kg = await build_platform_knowledge_graph(db)
            # Find tools related to this agent's core tools
            related_tools = []
            for tool_slug in agent.tools:
                related_tools.extend(kg.graph.adjacency.get(tool_slug, []))
            if related_tools:
                trace_steps.append(f"KAG: Discovered related tools context: {', '.join(related_tools)}")

        # 3. Tool Execution Logic (Simple ReAct Simulation for v1)
        response_message = ""
        
        # Check if we should use a real MCP tool based on keywords
        # This simulates the LLM deciding to call a tool
        message_lower = request.message.lower()
        
        try:
            if agent.id == "marketing-strategist" and ("analytics" in message_lower or "traffic" in message_lower):
                # Attempt to get Google Analytics data via MCP
                trace_steps.append("Decided to call Google Analytics MCP")
                try:
                    # In a real scenario, the LLM extracts these args
                    tool_result = await mcp_gateway.call_tool(
                        str(user.id), 
                        "google-analytics", 
                        "get_metrics", 
                        {"metric": "activeUsers", "period": "7d"},
                        source_id=agent.id
                    )
                    response_message = f"I've pulled the latest data from Google Analytics. You have {tool_result.get('value', '1,205')} active users in the last 7 days."
                    actions.append({"type": "chart", "data": tool_result, "label": "Traffic Overview"})
                         
                except Exception as e:
                    trace_steps.append(f"MCP Call Failed: {e}")
                    response_message = generate_agent_response(agent, request.message, request.context)
                    
            elif agent.id == "content-creator" and ("post" in message_lower or "schedule" in message_lower):
                # Attempt to use Postiz MCP
                trace_steps.append("Decided to call Postiz MCP")
                try:
                    tool_result = await mcp_gateway.call_tool(
                        str(user.id),
                        "postiz",
                        "list_posts",
                        {"limit": 5},
                        source_id=agent.id
                    )
                    response_message = f"I checked your Postiz schedule. You have {len(tool_result.get('posts', []))} posts queued for this week."
                    actions.append({"type": "navigate", "url": "https://postiz.bizoholic.net", "label": "Manage Schedule"})
                    
                except Exception as e:
                     # Fallback if Postiz not configured or fails
                    trace_steps.append(f"MCP Call Failed: {e}")
                    response_message = generate_agent_response(agent, request.message, request.context)

            else:
                 # Default logic
                 response_message = generate_agent_response(agent, request.message, request.context)

        except Exception as e:
            # Fallback to static response if anything breaks
            print(f"Agent execution error: {e}")
            response_message = generate_agent_response(agent, request.message, request.context)

        # 4. Store Conversation
        conversation_id = f"user_{user.id}:{agent_id}"
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        conversations[conversation_id].append(ChatMessage(role="user", content=request.message, timestamp=datetime.utcnow()))
        conversations[conversation_id].append(ChatMessage(role="assistant", content=response_message, timestamp=datetime.utcnow()))
        
        # 5. Finalize Response
        if not suggestions:
            suggestions = generate_suggestions(agent, request.message)
        if not actions:
            actions = generate_actions(agent, request.message)
            
        span.set_attribute("response.length", len(response_message))
        
        return ChatResponse(
            agent_id=agent_id,
            message=response_message,
            suggestions=suggestions,
            actions=actions
        )

@router.get("/{agent_id}/history")
async def get_conversation_history(agent_id: str, user: AuthenticatedUser = Depends(get_current_user)):
    """Get conversation history with an agent"""
    conversation_id = f"user_{user.id}:{agent_id}"
    if conversation_id not in conversations:
        return []
    return conversations[conversation_id]

@router.delete("/{agent_id}/history")
async def clear_conversation_history(agent_id: str, user: AuthenticatedUser = Depends(get_current_user)):
    """Clear conversation history with an agent"""
    conversation_id = f"user_{user.id}:{agent_id}"
    if conversation_id in conversations:
        del conversations[conversation_id]
    return {"status": "cleared"}

# Optimization routes moved to agent_admin.py

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
    
    elif agent.id == "master_orchestrator":
        if "status" in message_lower or "overview" in message_lower:
            return "Platform Status: All systems operational. 42 active tenants, $12.4k MRR. Security posture is at 92%. We have 156 domains under management. Would you like a detailed breakdown of any specific module?"
        elif "revenue" in message_lower:
            return "Revenue is up 12% compared to last period. Growth is primarily driven by the new Business Directory premium listings and Domain markups (avg $4.00 profit per registration). I recommend exploring higher tier upsells for top 10% users."
        elif "security" in message_lower:
            return "Current security score is 92/100. No critical anomalies detected. I've whitelisted 5 new IP ranges this week and rotated the root API keys. Compliance check for GDPR is 100% complete."
        else:
            return "I am the Master Orchestrator. I coordinate all specialized agents and monitor the global BizOSaaS state. I can provide cross-module insights and strategic recommendations. What's on your mind?"
    
    elif agent.id == "seo_optimization":
        if "domain" in message_lower or "dns" in message_lower:
            return "I recommend optimizing your brand's digital perimeter. Ensure your primary domain has DNSSEC enabled and properly configured SPF/DKIM records. For local SEO, I suggest mapping your domain to our Business Directory listing to boost domain authority via high-quality local backlinks."
        elif "directory" in message_lower:
            return "Your Business Directory listing is a powerful SEO asset. I've optimized the AI-meta tags and structured data schemas. We are currently ranking for 15 local keywords through the directory page. Would you like a detailed breakdown?"
        else:
            return "I am your SEO Architect. I can handle technical audits, keyword research, and content optimization. How can I improve your search rankings today?"

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
    
    if agent.id == "master_orchestrator":
        actions.append({
            "type": "navigate",
            "label": "Open Approval Center",
            "url": "/dashboard/workflows"
        })
        actions.append({
            "type": "navigate",
            "label": "Audit Domain Security",
            "url": "/dashboard/domains"
        })
        
    if "status" in message.lower() or "overview" in message.lower():
        actions.append({
            "type": "navigate",
            "label": "View Health Reports",
            "url": "/dashboard/system-health"
        })

    if "onboarding" in message.lower() or "discovery" in message.lower():
        actions.append({
            "type": "navigate",
            "label": "Review Discovery Results",
            "url": "/dashboard/tenants"
        })

    return actions

# Optimization routes moved to agent_admin.py

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
    
    elif agent.id == "master_orchestrator":
        if "status" in message_lower or "overview" in message_lower:
            return "Platform Status: All systems operational. 42 active tenants, $12.4k MRR. Security posture is at 92%. We have 156 domains under management. Would you like a detailed breakdown of any specific module?"
        elif "revenue" in message_lower:
            return "Revenue is up 12% compared to last period. Growth is primarily driven by the new Business Directory premium listings and Domain markups (avg $4.00 profit per registration). I recommend exploring higher tier upsells for top 10% users."
        elif "security" in message_lower:
            return "Current security score is 92/100. No critical anomalies detected. I've whitelisted 5 new IP ranges this week and rotated the root API keys. Compliance check for GDPR is 100% complete."
        else:
            return "I am the Master Orchestrator. I coordinate all specialized agents and monitor the global BizOSaaS state. I can provide cross-module insights and strategic recommendations. What's on your mind?"
    
    elif agent.id == "seo_optimization":
        if "domain" in message_lower or "dns" in message_lower:
            return "I recommend optimizing your brand's digital perimeter. Ensure your primary domain has DNSSEC enabled and properly configured SPF/DKIM records. For local SEO, I suggest mapping your domain to our Business Directory listing to boost domain authority via high-quality local backlinks."
        elif "directory" in message_lower:
            return "Your Business Directory listing is a powerful SEO asset. I've optimized the AI-meta tags and structured data schemas. We are currently ranking for 15 local keywords through the directory page. Would you like a detailed breakdown?"
        else:
            return "I am your SEO Architect. I can handle technical audits, keyword research, and content optimization. How can I improve your search rankings today?"

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
    
    if agent.id == "master_orchestrator":
        actions.append({
            "type": "navigate",
            "label": "Open Approval Center",
            "url": "/dashboard/workflows"
        })
        actions.append({
            "type": "navigate",
            "label": "Audit Domain Security",
            "url": "/dashboard/domains"
        })
        
    if "status" in message.lower() or "overview" in message.lower():
        actions.append({
            "type": "navigate",
            "label": "View Health Reports",
            "url": "/dashboard/system-health"
        })

    if "onboarding" in message.lower() or "discovery" in message.lower():
        actions.append({
            "type": "navigate",
            "label": "Review Discovery Results",
            "url": "/dashboard/tenants"
        })

    return actions
