"""
CRM & Lead Management Service - Domain Service for Customer Relationship Management
FastAPI application handling leads, contacts, deals, and sales pipeline with AI integration
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import asyncio
import logging
from typing import List, Optional
import httpx

# Import shared models and configurations
import sys
import os
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas/shared')

from models.base import PaginatedResponse, SuccessResponse, ErrorResponse
from configs.settings import settings


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting CRM & Lead Management Service...")
    
    # Initialize database connections
    # await init_database()
    
    # Initialize AI orchestrator connection
    global ai_client
    ai_client = httpx.AsyncClient(
        base_url=os.getenv("AI_ORCHESTRATOR_URL", "http://localhost:8002"),
        timeout=30.0
    )
    
    logger.info("CRM service initialized successfully")
    
    yield
    
    # Cleanup
    await ai_client.aclose()
    logger.info("CRM & Lead Management Service shutdown complete")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="BizoSaaS CRM & Lead Management Service",
        description="Domain service for customer relationship management, leads, and sales pipeline",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "*.bizosaas.local", "*.bizosaas.com"]
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app


app = create_app()

# Global AI client
ai_client: httpx.AsyncClient = None


# Pydantic models for CRM
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from enum import Enum


class LeadStatus(str, Enum):
    NEW = "new"
    QUALIFIED = "qualified"
    CONTACTED = "contacted"
    OPPORTUNITY = "opportunity"
    CONVERTED = "converted"
    LOST = "lost"


class LeadSource(str, Enum):
    WEBSITE = "website"
    GOOGLE_ADS = "google_ads"
    META_ADS = "meta_ads"
    LINKEDIN_ADS = "linkedin_ads"
    EMAIL = "email"
    REFERRAL = "referral"
    ORGANIC = "organic"


class DealStage(str, Enum):
    PROSPECT = "prospect"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class LeadCreate(BaseModel):
    """Lead creation model"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=200)
    job_title: Optional[str] = Field(None, max_length=100)
    source: LeadSource
    notes: Optional[str] = Field(None, max_length=1000)
    tenant_id: int


class LeadUpdate(BaseModel):
    """Lead update model"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=200)
    job_title: Optional[str] = Field(None, max_length=100)
    status: Optional[LeadStatus] = None
    notes: Optional[str] = Field(None, max_length=1000)
    score: Optional[float] = Field(None, ge=0, le=100)


class Lead(BaseModel):
    """Lead model for API responses"""
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    status: LeadStatus = LeadStatus.NEW
    source: LeadSource
    score: Optional[float] = None  # AI-generated lead score
    notes: Optional[str] = None
    tenant_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class DealCreate(BaseModel):
    """Deal creation model"""
    title: str = Field(..., min_length=1, max_length=200)
    lead_id: Optional[int] = None
    amount: Optional[float] = Field(None, ge=0)
    stage: DealStage = DealStage.PROSPECT
    expected_close_date: Optional[datetime] = None
    probability: Optional[float] = Field(None, ge=0, le=100)
    notes: Optional[str] = Field(None, max_length=1000)
    tenant_id: int


class Deal(BaseModel):
    """Deal model for API responses"""
    id: int
    title: str
    lead_id: Optional[int] = None
    amount: Optional[float] = None
    stage: DealStage
    expected_close_date: Optional[datetime] = None
    probability: Optional[float] = None
    notes: Optional[str] = None
    tenant_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class AILeadScoreRequest(BaseModel):
    """Request for AI lead scoring"""
    lead_data: dict
    tenant_id: int


class PipelineAnalytics(BaseModel):
    """Sales pipeline analytics"""
    total_leads: int
    qualified_leads: int
    conversion_rate: float
    average_deal_size: float
    pipeline_value: float
    deals_by_stage: dict
    top_sources: List[dict]
    monthly_trend: List[dict]


# Health check
@app.get("/health")
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "service": "crm-lead-management",
        "version": "1.0.0",
        "ai_orchestrator_connected": ai_client is not None
    }


# Leads endpoints
@app.post("/leads", response_model=Lead)
async def create_lead(
    lead: LeadCreate,
    background_tasks: BackgroundTasks
):
    """Create a new lead with AI scoring"""
    try:
        # Mock lead creation (replace with database operations)
        new_lead = Lead(
            id=12345,  # Replace with actual DB ID
            first_name=lead.first_name,
            last_name=lead.last_name,
            email=lead.email,
            phone=lead.phone,
            company=lead.company,
            job_title=lead.job_title,
            status=LeadStatus.NEW,
            source=lead.source,
            notes=lead.notes,
            tenant_id=lead.tenant_id,
            created_at=datetime.utcnow()
        )
        
        # Schedule AI lead scoring in background
        background_tasks.add_task(
            score_lead_with_ai,
            new_lead.id,
            lead.dict(),
            lead.tenant_id
        )
        
        logger.info(f"Created new lead {new_lead.id} for tenant {lead.tenant_id}")
        return new_lead
        
    except Exception as e:
        logger.error(f"Failed to create lead: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create lead")


@app.get("/leads", response_model=PaginatedResponse)
async def get_leads(
    tenant_id: int,
    status: Optional[LeadStatus] = None,
    source: Optional[LeadSource] = None,
    page: int = 1,
    size: int = 50
):
    """Get leads with filtering and pagination"""
    try:
        # Mock data (replace with database query)
        mock_leads = [
            Lead(
                id=1,
                first_name="John",
                last_name="Doe", 
                email="john.doe@example.com",
                company="Tech Startup Inc",
                job_title="CEO",
                status=LeadStatus.QUALIFIED,
                source=LeadSource.GOOGLE_ADS,
                score=85.5,
                tenant_id=tenant_id,
                created_at=datetime.utcnow()
            ),
            Lead(
                id=2,
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@company.com",
                company="E-commerce Co",
                job_title="Marketing Manager",
                status=LeadStatus.CONTACTED,
                source=LeadSource.META_ADS,
                score=72.3,
                tenant_id=tenant_id,
                created_at=datetime.utcnow()
            )
        ]
        
        # Apply filters (mock implementation)
        filtered_leads = mock_leads
        if status:
            filtered_leads = [l for l in filtered_leads if l.status == status]
        if source:
            filtered_leads = [l for l in filtered_leads if l.source == source]
            
        total = len(filtered_leads)
        pages = (total + size - 1) // size
        
        return PaginatedResponse(
            items=filtered_leads,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
    except Exception as e:
        logger.error(f"Failed to get leads: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve leads")


@app.get("/leads/{lead_id}", response_model=Lead)
async def get_lead(lead_id: int, tenant_id: int):
    """Get a specific lead"""
    # Mock implementation
    return Lead(
        id=lead_id,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        company="Tech Startup Inc",
        status=LeadStatus.QUALIFIED,
        source=LeadSource.GOOGLE_ADS,
        score=85.5,
        tenant_id=tenant_id,
        created_at=datetime.utcnow()
    )


@app.put("/leads/{lead_id}", response_model=Lead)
async def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    tenant_id: int,
    background_tasks: BackgroundTasks
):
    """Update a lead"""
    try:
        # Mock update (replace with database operations)
        updated_lead = Lead(
            id=lead_id,
            first_name=lead_update.first_name or "John",
            last_name=lead_update.last_name or "Doe",
            email=lead_update.email or "john.doe@example.com",
            phone=lead_update.phone,
            company=lead_update.company or "Tech Startup Inc",
            job_title=lead_update.job_title,
            status=lead_update.status or LeadStatus.QUALIFIED,
            source=LeadSource.GOOGLE_ADS,
            score=lead_update.score or 85.5,
            notes=lead_update.notes,
            tenant_id=tenant_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Re-score if significant changes
        if any([lead_update.company, lead_update.job_title, lead_update.email]):
            background_tasks.add_task(
                score_lead_with_ai,
                lead_id,
                lead_update.dict(exclude_none=True),
                tenant_id
            )
        
        return updated_lead
        
    except Exception as e:
        logger.error(f"Failed to update lead {lead_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update lead")


# Deals endpoints
@app.post("/deals", response_model=Deal)
async def create_deal(deal: DealCreate):
    """Create a new deal"""
    new_deal = Deal(
        id=67890,  # Replace with actual DB ID
        title=deal.title,
        lead_id=deal.lead_id,
        amount=deal.amount,
        stage=deal.stage,
        expected_close_date=deal.expected_close_date,
        probability=deal.probability,
        notes=deal.notes,
        tenant_id=deal.tenant_id,
        created_at=datetime.utcnow()
    )
    
    logger.info(f"Created new deal {new_deal.id} for tenant {deal.tenant_id}")
    return new_deal


@app.get("/deals", response_model=PaginatedResponse)
async def get_deals(
    tenant_id: int,
    stage: Optional[DealStage] = None,
    page: int = 1,
    size: int = 50
):
    """Get deals with filtering and pagination"""
    # Mock data
    mock_deals = [
        Deal(
            id=1,
            title="Enterprise Software License",
            lead_id=1,
            amount=50000.0,
            stage=DealStage.PROPOSAL,
            probability=75.0,
            tenant_id=tenant_id,
            created_at=datetime.utcnow()
        )
    ]
    
    return PaginatedResponse(
        items=mock_deals,
        total=len(mock_deals),
        page=page,
        size=size,
        pages=1
    )


# Analytics endpoints
@app.get("/analytics/pipeline", response_model=PipelineAnalytics)
async def get_pipeline_analytics(tenant_id: int):
    """Get sales pipeline analytics"""
    return PipelineAnalytics(
        total_leads=247,
        qualified_leads=89,
        conversion_rate=18.5,
        average_deal_size=12500.0,
        pipeline_value=156000.0,
        deals_by_stage={
            "prospect": 45,
            "qualified": 23,
            "proposal": 12,
            "negotiation": 6,
            "closed_won": 3,
            "closed_lost": 8
        },
        top_sources=[
            {"source": "google_ads", "count": 98},
            {"source": "meta_ads", "count": 67},
            {"source": "linkedin_ads", "count": 45}
        ],
        monthly_trend=[
            {"month": "Jan", "leads": 45, "deals": 8},
            {"month": "Feb", "leads": 52, "deals": 12},
            {"month": "Mar", "leads": 61, "deals": 15}
        ]
    )


# AI Integration functions
async def score_lead_with_ai(lead_id: int, lead_data: dict, tenant_id: int):
    """Score lead using AI orchestrator"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{os.getenv('AI_ORCHESTRATOR_URL', 'http://localhost:8002')}/agents/execute-task",
                json={
                    "task_type": "lead_scoring",
                    "parameters": {
                        "lead_id": lead_id,
                        "lead_data": lead_data
                    },
                    "tenant_id": tenant_id,
                    "priority": "normal"
                }
            )
            
            if response.status_code == 200:
                logger.info(f"AI lead scoring initiated for lead {lead_id}")
            else:
                logger.warning(f"AI lead scoring failed for lead {lead_id}: {response.text}")
                
    except Exception as e:
        logger.error(f"Failed to score lead {lead_id} with AI: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)