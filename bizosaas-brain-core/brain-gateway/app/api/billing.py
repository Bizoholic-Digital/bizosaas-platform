from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from app.middleware.auth import get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.store import active_connectors
from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorType
from app.ports.billing_port import BillingPort, Customer, Subscription, SubscriptionPlan, Invoice

router = APIRouter()

# --- Response Models ---
class PlanMessage(BaseModel):
    id: str
    name: str
    code: str
    amount: float
    currency: str
    interval: str
    trial_period_days: Optional[int] = 0

class CustomerMessage(BaseModel):
    id: Optional[str] = None
    email: str
    name: Optional[str] = None
    currency: str = "USD"
    metadata: Dict[str, Any] = {}

class SubscriptionMessage(BaseModel):
    id: str
    plan_id: str
    status: str
    current_period_end: datetime

class InvoiceMessage(BaseModel):
    id: str
    amount_due: float
    currency: str
    status: str
    created_at: datetime
    pdf_url: Optional[str] = None

# --- Helpers ---
async def get_active_billing_connector(tenant_id: str) -> BillingPort:
    configs = [c for c in ConnectorRegistry.get_all_configs() if c.id == "lago" or c.type == ConnectorType.OTHER] # Check type logic
    
    for config in configs:
        key = f"{tenant_id}:{config.id}"
        if key in active_connectors:
            data = active_connectors[key]
            connector = ConnectorRegistry.create_connector(config.id, tenant_id, data["credentials"])
            if isinstance(connector, BillingPort):
                return connector
            
    # Fallback to checking specifically for 'lago' if type match isn't strict
    key = f"{tenant_id}:lago"
    if key in active_connectors:
         data = active_connectors[key]
         connector = ConnectorRegistry.create_connector("lago", tenant_id, data["credentials"])
         return connector
         
    raise HTTPException(status_code=404, detail="No billing connector configured.")

# --- Endpoints ---

@router.get("/status")
async def get_billing_status(
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Check connectivity to billing provider"""
    tenant_id = user.tenant_id or "default_tenant"
    try:
        connector = await get_active_billing_connector(tenant_id)
        # We can implement validate_credentials or similar on connector base
        is_valid = await connector.validate_credentials() if hasattr(connector, 'validate_credentials') else True
        return {
            "connected": is_valid,
            "platform": "lago" # Dynamic if needed
        }
    except HTTPException:
        return {"connected": False}
    except Exception:
        return {"connected": False}

@router.get("/plans", response_model=List[PlanMessage])
async def list_plans(
    user: AuthenticatedUser = Depends(get_current_user)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_billing_connector(tenant_id)
    
    try:
        plans = await connector.get_plans()
        return [
            PlanMessage(
                id=p.id,
                name=p.name,
                code=p.code,
                amount=p.amount,
                currency=p.currency,
                interval=p.interval,
                trial_period_days=p.trial_period_days
            ) for p in plans
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Billing Error: {str(e)}")

@router.post("/customers", response_model=CustomerMessage)
async def create_customer(
    customer: CustomerMessage,
    user: AuthenticatedUser = Depends(get_current_user)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_billing_connector(tenant_id)
    
    try:
        data = Customer(
            id=customer.id or user.id, # Use User ID as external ID if not provided
            email=customer.email,
            name=customer.name,
            currency=customer.currency,
            metadata=customer.metadata
        )
        result = await connector.create_customer(data)
        return CustomerMessage(
            id=result.id,
            email=result.email,
            name=result.name,
            currency=result.currency,
            metadata=result.metadata
        )
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Billing Error: {str(e)}")

@router.post("/subscriptions", response_model=SubscriptionMessage)
async def create_subscription(
    plan_code: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_billing_connector(tenant_id)
    
    try:
        # Assume user.id is the customer external_id
        sub = await connector.create_subscription(user.id, plan_code)
        return SubscriptionMessage(
            id=sub.id or "",
            plan_id=sub.plan_id,
            status=sub.status,
            current_period_end=sub.current_period_end
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Billing Error: {str(e)}")

@router.get("/subscriptions", response_model=List[SubscriptionMessage])
async def list_subscriptions(
     user: AuthenticatedUser = Depends(get_current_user)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_billing_connector(tenant_id)
    
    try:
        subs = await connector.get_customer_subscriptions(user.id)
        return [
            SubscriptionMessage(
                id=s.id or "",
                plan_id=s.plan_id,
                status=s.status,
                current_period_end=s.current_period_end
            ) for s in subs
        ]
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Billing Error: {str(e)}")

@router.get("/invoices", response_model=List[InvoiceMessage])
async def list_invoices(
    user: AuthenticatedUser = Depends(get_current_user)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_billing_connector(tenant_id)
    
    try:
        invoices = await connector.get_customer_invoices(user.id)
        return [
            InvoiceMessage(
                id=i.id,
                amount_due=i.amount_due,
                currency=i.currency,
                status=i.status,
                created_at=i.created_at,
                pdf_url=i.invoice_pdf_url
            ) for i in invoices
        ]
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Billing Error: {str(e)}")
