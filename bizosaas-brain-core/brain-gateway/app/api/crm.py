from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.middleware.auth import get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.store import active_connectors
from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorType, ConnectorStatus
from app.connectors.ports.crm_port import CRMPort

router = APIRouter()

class ContactMessage(BaseModel):
    id: str
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    email: str
    phone: Optional[str] = ""
    company: Optional[str] = ""
    status: Optional[str] = "active"
    tags: Optional[List[str]] = []
    source: Optional[str] = "api"
    created_at: Optional[datetime] = None

async def get_active_crm_connector(tenant_id: str) -> CRMPort:
    # 1. Get all CRM connector types
    configs = [c for c in ConnectorRegistry.get_all_configs() if c.type == ConnectorType.CRM]
    
    # 2. Check connections
    for config in configs:
        key = f"{tenant_id}:{config.id}"
        if key in active_connectors:
            data = active_connectors[key]
            connector = ConnectorRegistry.create_connector(config.id, tenant_id, data["credentials"])
            return connector
            
    raise HTTPException(status_code=404, detail="No CRM connector configured.")

@router.get("/contacts", response_model=List[ContactMessage])
async def list_contacts(
    user: AuthenticatedUser = Depends(get_current_user)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_crm_connector(tenant_id)
    
    try:
        contacts = await connector.get_contacts()
        return [
            ContactMessage(
                id=c.id,
                first_name=c.first_name,
                last_name=c.last_name,
                email=c.email,
                phone=c.phone,
                status=c.status,
                tags=c.tags,
                created_at=datetime.now() # TODO: Contact needs dates
            ) for c in contacts
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CRM Error: {str(e)}")

@router.post("/contacts", response_model=ContactMessage)
async def create_contact(
    contact: ContactMessage,
    user: AuthenticatedUser = Depends(get_current_user)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_crm_connector(tenant_id)
    
    try:
        # Convert Pydantic model to dict for port
        payload = contact.dict(exclude={"id", "created_at"})
        result = await connector.create_contact(payload)
        
        return ContactMessage(
             id=result.id,
             first_name=result.first_name,
             last_name=result.last_name,
             email=result.email,
             phone=result.phone,
             status=result.status,
             tags=result.tags,
             created_at=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CRM Error: {str(e)}")
