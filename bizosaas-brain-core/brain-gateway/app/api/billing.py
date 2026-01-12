from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from app.middleware.auth import get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.store import active_connectors
from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorType
from app.services.billing_service import BillingService
from app.api.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# --- Response Models ---
class PlanMessage(BaseModel):
    id: str
    name: str
    slug: str
    amount: float
    currency: str
    interval: str
    description: Optional[str] = None

class SubscriptionMessage(BaseModel):
    id: str
    plan_slug: str
    status: str
    current_period_end: datetime

class InvoiceMessage(BaseModel):
    id: str
    amount: float
    currency: str
    status: str
    created_at: datetime
    paid_at: Optional[datetime] = None
    pdf_url: Optional[str] = None

# --- Endpoints ---

@router.get("/plans", response_model=List[PlanMessage])
async def list_plans(
    db: Session = Depends(get_db)
):
    service = BillingService(db)
    plans = await service.get_plans()
    
    results = []
    for p in plans:
        # Handle both internal model and PortPlan
        p_id = getattr(p, "id", None)
        p_name = getattr(p, "name", None)
        p_slug = getattr(p, "slug", getattr(p, "code", None))
        p_amount = getattr(p, "price", getattr(p, "amount", 0.0))
        p_curr = getattr(p, "currency", "USD")
        p_interval = getattr(p, "interval", "monthly")
        p_desc = getattr(p, "description", None)
        
        results.append(PlanMessage(
            id=str(p_id),
            name=p_name,
            slug=p_slug,
            amount=float(p_amount),
            currency=p_curr,
            interval=p_interval,
            description=p_desc
        ))
    return results

@router.get("/subscription", response_model=Optional[SubscriptionMessage])
async def get_subscription(
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = BillingService(db)
    sub = await service.get_tenant_subscription(user.tenant_id)
    if not sub:
        return None
    
    # Handle both internal model and PortSubscription
    plan_slug = None
    if hasattr(sub, "plan"):
        plan_slug = sub.plan.slug
    else:
        plan_slug = getattr(sub, "plan_id", "unknown")
        
    return SubscriptionMessage(
        id=str(sub.id),
        plan_slug=plan_slug,
        status=getattr(sub, "status", "active"),
        current_period_end=sub.current_period_end
    )

@router.post("/subscribe", response_model=SubscriptionMessage)
async def create_subscription(
    plan_slug: str,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = BillingService(db)
    try:
        sub = await service.create_subscription(user.tenant_id, plan_slug)
        
        # Handle both internal model and PortSubscription
        res_plan_slug = plan_slug
        if hasattr(sub, "plan"):
             res_plan_slug = sub.plan.slug
        elif hasattr(sub, "plan_id"):
             res_plan_slug = sub.plan_id

        return SubscriptionMessage(
            id=str(sub.id),
            plan_slug=res_plan_slug,
            status=getattr(sub, "status", "active"),
            current_period_end=sub.current_period_end
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhooks/razorpay")
async def razorpay_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    json_data = await request.json()
    # Verify signature here
    # Handle events: subscription.charged, order.paid, etc.
    return {"status": "ok"}

@router.get("/invoices", response_model=List[InvoiceMessage])
async def list_invoices(
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = BillingService(db)
    invoices = await service.list_invoices(user.tenant_id)
    
    results = []
    for i in invoices:
        amount = getattr(i, "amount", getattr(i, "amount_due", 0.0))
        pdf_url = getattr(i, "pdf_url", getattr(i, "invoice_pdf_url", None))
        
        results.append(InvoiceMessage(
            id=str(i.id),
            amount=float(amount),
            currency=i.currency,
            status=i.status,
            created_at=i.created_at,
            paid_at=getattr(i, "paid_at", None),
            pdf_url=pdf_url
        ))
    return results
