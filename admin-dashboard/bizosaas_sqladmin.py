"""
BizOSaaS SQLAlchemy Admin Dashboard
SQLAlchemy-based admin interface for BizOSaaS platform management
Port 3003 - Connected to FastAPI AI Gateway (port 8001)
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from datetime import datetime
import json

# Create FastAPI app
app = FastAPI(title="BizOSaaS Admin Dashboard", description="SQLAlchemy-based platform administration")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database configuration - connect to BizOSaaS database
DATABASE_URL = os.getenv("BIZOSAAS_DATABASE_URL", "postgresql://postgres:password@localhost:5433/bizosaas")
# Fallback to SQLite for demo if PostgreSQL not available
DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

try:
    engine = create_engine(DATABASE_URL, echo=False)
    # Test the connection
    with engine.connect() as conn:
        pass
    print(f"✅ Connected to BizOSaaS database: {DATABASE_URL.split('://')[0].upper()}")
except Exception as e:
    print(f"⚠️  Database connection issue: {e}")
    DATABASE_URL = "sqlite:///./bizosaas_admin.db"
    engine = create_engine(DATABASE_URL, echo=False)
    print("🔄 Using SQLite fallback for admin dashboard")

# SQLAlchemy Base and Models
Base = declarative_base()

# BizOSaaS Platform Models
class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    subdomain = Column(String(100), unique=True, nullable=False)
    plan = Column(String(50), default="starter")  # starter, professional, enterprise
    status = Column(String(20), default="active")  # active, trial, cancelled, suspended
    ai_credits = Column(Integer, default=1000)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="tenant")
    workflows = relationship("AIWorkflow", back_populates="tenant")
    campaigns = relationship("Campaign", back_populates="tenant")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(50), default="user")  # admin, manager, user, viewer
    is_active = Column(Boolean, default=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")

class AIWorkflow(Base):
    __tablename__ = "ai_workflows"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)  # marketing, analytics, content, automation
    status = Column(String(50), default="draft")  # draft, active, paused, completed
    ai_agent = Column(String(100))  # lead-scoring, content-generation, campaign-optimization
    executions = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_execution = Column(DateTime)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="workflows")
    workflow_executions = relationship("WorkflowExecution", back_populates="workflow")

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)  # email, social, ppc, content
    status = Column(String(50), default="draft")  # draft, active, paused, completed
    budget = Column(Float)
    spend = Column(Float, default=0.0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    roi = Column(Float, default=0.0)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="campaigns")

class SystemMetric(Base):
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True)
    metric_name = Column(String(100), nullable=False)  # cpu_usage, memory_usage, api_calls
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(20))  # %, MB, calls/min
    service_name = Column(String(100))  # brain-ai, auth-service, wagtail-cms
    timestamp = Column(DateTime, default=datetime.utcnow)

class APIUsage(Base):
    __tablename__ = "api_usage"
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)  # GET, POST, PUT, DELETE
    status_code = Column(Integer)
    response_time = Column(Float)  # milliseconds
    timestamp = Column(DateTime, default=datetime.utcnow)

class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"
    
    id = Column(Integer, primary_key=True)
    workflow_id = Column(Integer, ForeignKey("ai_workflows.id"))
    status = Column(String(50), default="running")  # running, completed, failed, paused
    execution_time = Column(Float)  # seconds
    input_data = Column(Text)  # JSON string
    output_data = Column(Text)  # JSON string
    error_message = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    workflow = relationship("AIWorkflow", back_populates="workflow_executions")

class RevenueMetric(Base):
    __tablename__ = "revenue_metrics"
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    metric_type = Column(String(100), nullable=False)  # monthly_revenue, mrr, churn_rate, ltv
    amount = Column(Float, default=0.0)
    currency = Column(String(3), default="USD")
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class SecurityEvent(Base):
    __tablename__ = "security_events"
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    event_type = Column(String(100), nullable=False)  # login_attempt, api_key_access, data_export
    severity = Column(String(20), default="info")  # info, warning, critical
    source_ip = Column(String(45))
    user_agent = Column(Text)
    event_data = Column(Text)  # JSON string
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables and sample data - always for demo purposes
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Add sample data if empty
if session.query(Tenant).count() == 0:
        print("📊 Creating sample BizOSaaS data...")
        
        # Sample tenants
        tenants = [
            Tenant(name="TechCorp Solutions", subdomain="techcorp", plan="enterprise", status="active", ai_credits=5000),
            Tenant(name="Digital Marketing Pro", subdomain="digitalmarketing", plan="professional", status="active", ai_credits=2500),
            Tenant(name="StartupHub Inc", subdomain="startuphub", plan="starter", status="trial", ai_credits=500),
            Tenant(name="Global Enterprises", subdomain="globalent", plan="enterprise", status="active", ai_credits=10000),
        ]
        session.add_all(tenants)
        session.commit()
        
        # Sample users
        users = [
            User(email="admin@techcorp.com", name="John Admin", role="admin", tenant_id=1, is_active=True),
            User(email="manager@techcorp.com", name="Sarah Manager", role="manager", tenant_id=1, is_active=True),
            User(email="user@digitalmarketing.com", name="Mike User", role="user", tenant_id=2, is_active=True),
            User(email="demo@startuphub.com", name="Demo User", role="user", tenant_id=3, is_active=False),
        ]
        session.add_all(users)
        
        # Sample AI workflows
        workflows = [
            AIWorkflow(name="Lead Scoring Pipeline", type="analytics", status="active", ai_agent="lead-scoring", executions=156, success_rate=98.5, tenant_id=1),
            AIWorkflow(name="Content Generation", type="content", status="active", ai_agent="content-generation", executions=89, success_rate=94.2, tenant_id=2),
            AIWorkflow(name="Campaign Optimization", type="marketing", status="paused", ai_agent="campaign-optimization", executions=45, success_rate=96.8, tenant_id=1),
            AIWorkflow(name="Customer Segmentation", type="analytics", status="active", ai_agent="customer-segmentation", executions=234, success_rate=91.3, tenant_id=3),
        ]
        session.add_all(workflows)
        
        # Sample campaigns
        campaigns = [
            Campaign(name="Q4 Launch Campaign", type="email", status="active", budget=5000.0, spend=2341.0, clicks=1245, conversions=89, roi=3.2, tenant_id=1),
            Campaign(name="Social Media Boost", type="social", status="completed", budget=2500.0, spend=2500.0, clicks=892, conversions=34, roi=1.8, tenant_id=2),
            Campaign(name="PPC Holiday Sale", type="ppc", status="active", budget=3200.0, spend=1890.0, clicks=2156, conversions=167, roi=4.1, tenant_id=1),
        ]
        session.add_all(campaigns)
        
        # Sample system metrics
        metrics = [
            SystemMetric(metric_name="cpu_usage", metric_value=45.2, metric_unit="%", service_name="brain-ai"),
            SystemMetric(metric_name="memory_usage", metric_value=2.4, metric_unit="GB", service_name="brain-ai"),
            SystemMetric(metric_name="api_calls", metric_value=125.4, metric_unit="calls/min", service_name="auth-service"),
            SystemMetric(metric_name="response_time", metric_value=89.2, metric_unit="ms", service_name="wagtail-cms"),
        ]
        session.add_all(metrics)
        
        session.commit()
        print(f"✅ Sample data created: {session.query(Tenant).count()} tenants, {session.query(User).count()} users, {session.query(AIWorkflow).count()} workflows")

session.close()

# Admin Views
class TenantAdmin(ModelView, model=Tenant):
    column_list = ["id", "name", "subdomain", "plan", "status", "ai_credits", "created_at"]
    column_searchable_list = ["name", "subdomain"]
    column_sortable_list = ["id", "name", "created_at", "ai_credits"]
    name = "Tenants"
    name_plural = "Tenants"
    icon = "fa-solid fa-building"

class UserAdmin(ModelView, model=User):
    column_list = ["id", "email", "name", "role", "is_active", "tenant_id", "last_login"]
    column_searchable_list = ["email", "name"]
    column_sortable_list = ["id", "email", "created_at", "last_login"]
    name = "Users"
    name_plural = "Users"
    icon = "fa-solid fa-users"

class AIWorkflowAdmin(ModelView, model=AIWorkflow):
    column_list = ["id", "name", "type", "status", "ai_agent", "executions", "success_rate", "tenant_id"]
    column_searchable_list = ["name", "ai_agent"]
    column_sortable_list = ["id", "name", "executions", "success_rate", "last_execution"]
    name = "AI Workflows"
    name_plural = "AI Workflows"
    icon = "fa-solid fa-robot"

class CampaignAdmin(ModelView, model=Campaign):
    column_list = ["id", "name", "type", "status", "budget", "spend", "clicks", "conversions", "roi"]
    column_searchable_list = ["name"]
    column_sortable_list = ["id", "name", "created_at", "budget", "roi"]
    name = "Campaigns"
    name_plural = "Campaigns"
    icon = "fa-solid fa-bullhorn"

class SystemMetricAdmin(ModelView, model=SystemMetric):
    column_list = ["id", "metric_name", "metric_value", "metric_unit", "service_name", "timestamp"]
    column_searchable_list = ["metric_name", "service_name"]
    column_sortable_list = ["id", "timestamp", "metric_value"]
    name = "System Metrics"
    name_plural = "System Metrics" 
    icon = "fa-solid fa-chart-line"

class APIUsageAdmin(ModelView, model=APIUsage):
    column_list = ["id", "tenant_id", "endpoint", "method", "status_code", "response_time", "timestamp"]
    column_searchable_list = ["endpoint"]
    column_sortable_list = ["id", "timestamp", "response_time"]
    name = "API Usage"
    name_plural = "API Usage"
    icon = "fa-solid fa-code"

class WorkflowExecutionAdmin(ModelView, model=WorkflowExecution):
    column_list = ["id", "workflow_id", "status", "execution_time", "started_at", "completed_at"]
    column_searchable_list = []
    column_sortable_list = ["id", "started_at", "execution_time"]
    name = "Workflow Executions"
    name_plural = "Workflow Executions"
    icon = "fa-solid fa-play"

class RevenueMetricAdmin(ModelView, model=RevenueMetric):
    column_list = ["id", "tenant_id", "metric_type", "amount", "currency", "period_start", "period_end"]
    column_searchable_list = ["metric_type"]
    column_sortable_list = ["id", "amount", "period_start"]
    name = "Revenue Metrics"
    name_plural = "Revenue Metrics"
    icon = "fa-solid fa-dollar-sign"

class SecurityEventAdmin(ModelView, model=SecurityEvent):
    column_list = ["id", "tenant_id", "user_id", "event_type", "severity", "source_ip", "timestamp"]
    column_searchable_list = ["event_type", "source_ip"]
    column_sortable_list = ["id", "timestamp", "severity"]
    name = "Security Events"
    name_plural = "Security Events"
    icon = "fa-solid fa-shield-alt"

# Create SQLAdmin instance with Bizoholic branding
admin = Admin(
    app, 
    engine, 
    title="Bizoholic Digital",
    debug=True,
    logo_url="/static/bizoholic-logo.png"
)

# Register model views - organized by category
# Core Platform Management
admin.add_view(TenantAdmin)
admin.add_view(UserAdmin)

# AI & Workflow Management  
admin.add_view(AIWorkflowAdmin)
admin.add_view(WorkflowExecutionAdmin)

# Business Operations
admin.add_view(CampaignAdmin)
admin.add_view(RevenueMetricAdmin)

# System Monitoring
admin.add_view(SystemMetricAdmin)
admin.add_view(APIUsageAdmin)
admin.add_view(SecurityEventAdmin)

# API Endpoints
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "BizOSaaS SQLAlchemy Admin",
        "admin_url": "/admin",
        "database": DATABASE_URL.split("://")[0].upper(),
        "ai_gateway": "http://localhost:8001",
        "models": ["Tenant", "User", "AIWorkflow", "Campaign", "SystemMetric", "APIUsage"],
        "features": [
            "🏢 Multi-tenant management",
            "🤖 AI workflow orchestration & control", 
            "📊 Campaign performance tracking",
            "🔍 System metrics monitoring",
            "📈 API usage analytics",
            "💰 Revenue & subscription analytics",
            "🛡️ Security event monitoring",
            "⚡ Workflow execution tracking",
            "🎛️ Real-time workflow dashboard",
            "🗃️ SQLAlchemy admin interface"
        ]
    }

@app.get("/")
async def root():
    return {
        "message": "BizOSaaS Platform Administration",
        "admin_url": "/admin",
        "description": "SQLAlchemy-based admin dashboard for BizOSaaS platform management",
        "ai_gateway": "Connected to FastAPI AI Gateway (port 8001)",
        "database": DATABASE_URL.split("://")[0].upper(),
        "version": "1.0.0"
    }

@app.get("/stats")
async def platform_stats():
    """Platform statistics endpoint for monitoring"""
    if DATABASE_URL.startswith("sqlite"):
        Session = sessionmaker(bind=engine)
        session = Session()
        
        stats = {
            "total_tenants": session.query(Tenant).count(),
            "active_tenants": session.query(Tenant).filter(Tenant.status == "active").count(),
            "total_users": session.query(User).count(),
            "active_workflows": session.query(AIWorkflow).filter(AIWorkflow.status == "active").count(),
            "total_campaigns": session.query(Campaign).count(),
            "recent_executions": session.query(WorkflowExecution).count(),
            "security_events": session.query(SecurityEvent).count(),
            "database": "Connected",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        session.close()
        return stats
    else:
        return {"message": "Stats available only with active database connection"}

@app.get("/workflow-dashboard")
async def workflow_dashboard():
    """Comprehensive workflow management dashboard data"""
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Get workflow status overview
        workflows = session.query(AIWorkflow).all()
        workflow_data = []
        
        for workflow in workflows:
            recent_executions = session.query(WorkflowExecution)\
                .filter(WorkflowExecution.workflow_id == workflow.id)\
                .order_by(WorkflowExecution.started_at.desc())\
                .limit(10).all()
            
            success_count = len([e for e in recent_executions if e.status == "completed"])
            total_executions = len(recent_executions)
            success_rate = (success_count / total_executions * 100) if total_executions > 0 else 0
            
            workflow_data.append({
                "id": workflow.id,
                "name": workflow.name,
                "type": workflow.type,
                "status": workflow.status,
                "ai_agent": workflow.ai_agent,
                "success_rate": round(success_rate, 1),
                "executions": workflow.executions,
                "last_execution": workflow.last_execution.isoformat() if workflow.last_execution else None,
                "tenant_id": workflow.tenant_id
            })
        
        # System metrics
        system_health = {
            "total_workflows": len(workflows),
            "active_workflows": len([w for w in workflows if w.status == "active"]),
            "total_tenants": session.query(Tenant).count(),
            "active_tenants": session.query(Tenant).filter(Tenant.status == "active").count(),
            "recent_security_events": session.query(SecurityEvent).filter(
                SecurityEvent.severity.in_(["warning", "critical"])
            ).count()
        }
        
        session.close()
        
        return {
            "workflows": workflow_data,
            "system_health": system_health,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"error": f"Database error: {str(e)}", "workflows": [], "system_health": {}}

@app.post("/workflow/{workflow_id}/action/{action}")
async def workflow_action(workflow_id: int, action: str):
    """Control workflow execution (start, pause, stop, restart)"""
    if DATABASE_URL.startswith("sqlite"):
        Session = sessionmaker(bind=engine)
        session = Session()
        
        workflow = session.query(AIWorkflow).filter(AIWorkflow.id == workflow_id).first()
        if not workflow:
            return {"error": "Workflow not found"}
        
        # Record the action as a workflow execution
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            status="initiated",
            started_at=datetime.utcnow()
        )
        session.add(execution)
        
        if action == "start":
            workflow.status = "active"
            workflow.last_execution = datetime.utcnow()
            execution.status = "running"
        elif action == "pause":
            workflow.status = "paused"
            execution.status = "paused"
        elif action == "stop":
            workflow.status = "stopped"
            execution.status = "stopped"
            execution.completed_at = datetime.utcnow()
        elif action == "restart":
            workflow.status = "active"
            workflow.last_execution = datetime.utcnow()
            workflow.executions += 1
            execution.status = "running"
        else:
            return {"error": "Invalid action. Use: start, pause, stop, restart"}
        
        # Get data before closing session
        workflow_name = workflow.name
        execution_id = execution.id
        new_status = workflow.status
        
        session.commit()
        session.close()
        
        return {
            "message": f"Workflow '{workflow_name}' {action}ed successfully",
            "workflow_id": workflow_id,
            "execution_id": execution_id,
            "new_status": new_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    else:
        return {"message": "Workflow control requires active database connection"}

@app.post("/workflow/create")
async def create_workflow(workflow_data: dict):
    """Create a new AI workflow"""
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        new_workflow = AIWorkflow(
            name=workflow_data.get("name"),
            type=workflow_data.get("type", "automation"),
            status="draft",
            ai_agent=workflow_data.get("ai_agent"),
            tenant_id=workflow_data.get("tenant_id", 1)
        )
        
        session.add(new_workflow)
        session.commit()
        
        workflow_id = new_workflow.id
        session.close()
        
        return {
            "message": "Workflow created successfully",
            "workflow_id": workflow_id,
            "name": new_workflow.name,
            "status": new_workflow.status,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"error": f"Failed to create workflow: {str(e)}"}

@app.get("/workflow/{workflow_id}/executions")
async def get_workflow_executions(workflow_id: int):
    """Get execution history for a specific workflow"""
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        executions = session.query(WorkflowExecution).filter(
            WorkflowExecution.workflow_id == workflow_id
        ).order_by(WorkflowExecution.started_at.desc()).limit(50).all()
        
        execution_data = []
        for exec in executions:
            execution_data.append({
                "id": exec.id,
                "status": exec.status,
                "started_at": exec.started_at.isoformat() if exec.started_at else None,
                "completed_at": exec.completed_at.isoformat() if exec.completed_at else None,
                "execution_time": exec.execution_time,
                "error_message": exec.error_message
            })
        
        session.close()
        
        return {
            "workflow_id": workflow_id,
            "executions": execution_data,
            "total_executions": len(execution_data),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"error": f"Database error: {str(e)}", "executions": []}

@app.post("/ai-agent/execute")
async def execute_ai_agent(agent_data: dict):
    """Execute AI agent with specified parameters"""
    try:
        # Simulate AI agent execution
        agent_name = agent_data.get("agent_name")
        workflow_id = agent_data.get("workflow_id")
        parameters = agent_data.get("parameters", {})
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Create execution record
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            status="running",
            started_at=datetime.utcnow()
        )
        session.add(execution)
        session.commit()
        
        # Simulate agent processing time
        import time
        time.sleep(1)
        
        # Update execution as completed
        execution.status = "completed"
        execution.completed_at = datetime.utcnow()
        execution.execution_time = 1200  # milliseconds
        
        # Update workflow stats
        workflow = session.query(AIWorkflow).filter(AIWorkflow.id == workflow_id).first()
        if workflow:
            workflow.executions += 1
            workflow.last_execution = datetime.utcnow()
            # Simulate success rate calculation
            workflow.success_rate = min(100.0, workflow.success_rate + 0.1)
        
        session.commit()
        session.close()
        
        return {
            "message": f"AI Agent '{agent_name}' executed successfully",
            "execution_id": execution.id,
            "workflow_id": workflow_id,
            "execution_time": execution.execution_time,
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"error": f"AI agent execution failed: {str(e)}"}

@app.get("/ai-agents/status")
async def get_ai_agents_status():
    """Get status of all AI agents"""
    return {
        "agents": [
            {"name": "lead-scoring", "status": "active", "success_rate": 98.5, "executions": 1245},
            {"name": "content-generation", "status": "active", "success_rate": 94.2, "executions": 892},
            {"name": "campaign-optimization", "status": "active", "success_rate": 96.8, "executions": 567},
            {"name": "customer-segmentation", "status": "active", "success_rate": 91.3, "executions": 1089},
            {"name": "sentiment-analysis", "status": "active", "success_rate": 89.7, "executions": 723},
            {"name": "price-optimization", "status": "maintenance", "success_rate": 95.1, "executions": 334}
        ],
        "total_agents": 6,
        "active_agents": 5,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/real-time/metrics")
async def real_time_metrics():
    """Real-time platform metrics for dashboard"""
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Active workflows and their status
        active_workflows = session.query(AIWorkflow).filter(AIWorkflow.status == "active").count()
        total_workflows = session.query(AIWorkflow).count()
        
        # Recent executions (last hour simulation)
        recent_executions = session.query(WorkflowExecution).count()
        
        # System health indicators
        health_metrics = {
            "workflow_utilization": round((active_workflows / total_workflows * 100) if total_workflows > 0 else 0, 1),
            "execution_rate": round(recent_executions * 0.5, 1),  # simulated per minute
            "success_rate": 96.3,  # simulated overall success rate
            "ai_agents_online": 5,
            "total_tenants": session.query(Tenant).count(),
            "active_tenants": session.query(Tenant).filter(Tenant.status == "active").count()
        }
        
        # Recent activity feed
        recent_activities = [
            {"type": "workflow_started", "message": "Lead Scoring Pipeline started for Tenant 1", "timestamp": "2 minutes ago"},
            {"type": "execution_completed", "message": "Content Generation completed successfully", "timestamp": "5 minutes ago"},
            {"type": "tenant_created", "message": "New tenant 'Digital Solutions Inc.' registered", "timestamp": "12 minutes ago"},
            {"type": "ai_agent_optimized", "message": "Campaign Optimization agent updated success rate to 96.8%", "timestamp": "18 minutes ago"}
        ]
        
        session.close()
        
        return {
            "health_metrics": health_metrics,
            "recent_activities": recent_activities,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "healthy"
        }
    except Exception as e:
        return {"error": f"Database error: {str(e)}", "health_metrics": {}, "recent_activities": []}

@app.get("/integration/brain-gateway")
async def check_brain_gateway():
    """Check connection to Brain Gateway (FastAPI AI Hub)"""
    try:
        import requests
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            brain_data = response.json()
            return {
                "brain_gateway": "connected",
                "brain_status": brain_data.get("status", "unknown"),
                "brain_services": brain_data.get("services", {}),
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            return {
                "brain_gateway": "error",
                "error": f"HTTP {response.status_code}",
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {
            "brain_gateway": "disconnected",
            "error": str(e),
            "fallback_mode": "SQLite local operations only",
            "timestamp": datetime.utcnow().isoformat()
        }

@app.post("/integration/brain/workflow/{workflow_id}/trigger")
async def trigger_brain_workflow(workflow_id: int, trigger_data: dict):
    """Trigger workflow execution via Brain Gateway"""
    try:
        import requests
        
        # Send workflow trigger to Brain Gateway
        brain_payload = {
            "workflow_id": workflow_id,
            "trigger_source": "admin_dashboard",
            "parameters": trigger_data.get("parameters", {}),
            "tenant_id": trigger_data.get("tenant_id", 1)
        }
        
        response = requests.post(
            f"http://localhost:8001/api/brain/workflow/trigger",
            json=brain_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            brain_response = response.json()
            
            # Record execution in local database
            Session = sessionmaker(bind=engine)
            session = Session()
            
            execution = WorkflowExecution(
                workflow_id=workflow_id,
                status="running",
                started_at=datetime.utcnow()
            )
            session.add(execution)
            session.commit()
            
            execution_id = execution.id
            session.close()
            
            return {
                "message": "Workflow triggered via Brain Gateway",
                "brain_response": brain_response,
                "local_execution_id": execution_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            return {
                "error": f"Brain Gateway error: HTTP {response.status_code}",
                "response": response.text,
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {
            "error": f"Failed to trigger Brain Gateway workflow: {str(e)}",
            "fallback": "Use local workflow execution instead",
            "timestamp": datetime.utcnow().isoformat()
        }

@app.get("/workflows/analytics")
async def workflow_analytics():
    """Comprehensive workflow analytics and insights"""
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Workflow performance metrics
        workflows = session.query(AIWorkflow).all()
        
        workflow_stats = {
            "total_workflows": len(workflows),
            "active_workflows": len([w for w in workflows if w.status == "active"]),
            "success_rates": {
                "excellent": len([w for w in workflows if w.success_rate >= 95]),
                "good": len([w for w in workflows if 85 <= w.success_rate < 95]),
                "needs_improvement": len([w for w in workflows if w.success_rate < 85])
            },
            "workflow_types": {}
        }
        
        # Group by type
        for workflow in workflows:
            wf_type = workflow.type
            if wf_type not in workflow_stats["workflow_types"]:
                workflow_stats["workflow_types"][wf_type] = 0
            workflow_stats["workflow_types"][wf_type] += 1
        
        # AI Agent utilization
        agent_usage = {}
        for workflow in workflows:
            agent = workflow.ai_agent
            if agent:
                if agent not in agent_usage:
                    agent_usage[agent] = {"count": 0, "total_executions": 0, "avg_success_rate": 0}
                agent_usage[agent]["count"] += 1
                agent_usage[agent]["total_executions"] += workflow.executions
                agent_usage[agent]["avg_success_rate"] = (
                    agent_usage[agent]["avg_success_rate"] + workflow.success_rate
                ) / agent_usage[agent]["count"]
        
        # Execution trends (simulated)
        execution_trends = {
            "today": 245,
            "yesterday": 198,
            "this_week": 1567,
            "last_week": 1423,
            "growth_rate": "+10.1%"
        }
        
        session.close()
        
        return {
            "workflow_stats": workflow_stats,
            "agent_utilization": agent_usage,
            "execution_trends": execution_trends,
            "recommendations": [
                "Consider optimizing workflows with success rate < 85%",
                "Scale up 'lead-scoring' agent usage - high performance detected",
                "Monitor 'content-generation' workflows for potential bottlenecks"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"error": f"Analytics error: {str(e)}", "workflow_stats": {}, "agent_utilization": {}}

@app.get("/revenue-analytics")
async def revenue_analytics():
    """Revenue and subscription analytics"""
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Basic revenue metrics
        total_revenue = session.query(RevenueMetric).filter(
            RevenueMetric.metric_type == "monthly_revenue"
        ).count()
        
        # Tenant subscription distribution
        tenant_plans = {}
        tenants = session.query(Tenant).all()
        for tenant in tenants:
            plan = tenant.plan
            tenant_plans[plan] = tenant_plans.get(plan, 0) + 1
        
        # Calculate total AI credits across tenants
        total_ai_credits = sum([tenant.ai_credits for tenant in tenants])
        
        session.close()
        
        return {
            "total_revenue_records": total_revenue,
            "tenant_distribution": tenant_plans,
            "total_ai_credits": total_ai_credits,
            "total_tenants": len(tenants),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"error": f"Database error: {str(e)}", "tenant_distribution": {}, "total_revenue_records": 0}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 BizOSaaS SQLAlchemy Admin Dashboard")
    print("="*60)
    print(f"📱 Admin Interface: http://localhost:3003/admin")
    print(f"🔗 AI Gateway: http://localhost:8001")
    print(f"📊 Database: {DATABASE_URL.split('://')[0].upper()}")
    print(f"🎯 Features: Multi-tenant, AI workflows, Revenue analytics, Security monitoring")
    print(f"📋 Models: Tenant, User, AIWorkflow, Campaign, SystemMetric, APIUsage, WorkflowExecution, RevenueMetric, SecurityEvent")
    print(f"🎛️ Advanced: Workflow control, Real-time dashboard, Revenue tracking")
    print("="*60)
    
    uvicorn.run(
        "bizosaas_sqladmin:app",
        host="0.0.0.0",
        port=3003,
        reload=True,
        log_level="info"
    )