from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.middleware.auth import get_current_user
from app.domain.ports.identity_port import AuthenticatedUser
from app.store import active_connectors
from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorType, ConnectorStatus
from app.ports.crm_port import CRMPort
from app.dependencies import get_secret_service
from app.domain.services.secret_service import SecretService

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

class DealMessage(BaseModel):
    id: Optional[str] = None
    title: str
    value: float
    currency: str = "USD"
    stage: str
    pipeline: Optional[str] = None
    contact_ids: List[str] = []
    close_date: Optional[str] = None

async def get_active_crm_connector(tenant_id: str, secret_service: SecretService) -> CRMPort:
    # 1. Get all CRM connector types
    configs = [c for c in ConnectorRegistry.get_all_configs() if c.type == ConnectorType.CRM]
    
    # 2. Check in-memory store first
    for config in configs:
        key = f"{tenant_id}:{config.id}"
        if key in active_connectors:
            data = active_connectors[key]
            connector = ConnectorRegistry.create_connector(config.id, tenant_id, data["credentials"])
            return connector
            
    # 3. Check secret service (persistent)
    for config in configs:
        credentials = await secret_service.get_connector_credentials(tenant_id, config.id)
        if credentials:
            connector = ConnectorRegistry.create_connector(config.id, tenant_id, credentials)
            active_connectors[f"{tenant_id}:{config.id}"] = {"credentials": credentials}
            return connector
            
    raise HTTPException(status_code=404, detail="No CRM connector configured.")

@router.get("/status")
async def get_crm_status(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Check connectivity to the active CRM"""
    tenant_id = user.tenant_id or "default_tenant"
    try:
        connector = await get_active_crm_connector(tenant_id, secret_service)
        is_valid = await connector.validate_credentials()
        
        return {
            "connected": is_valid,
            "platform": connector.config.name if hasattr(connector, 'config') else "FluentCRM",
            "version": "Unknown" 
        }
    except HTTPException:
        return {"connected": False}
    except Exception as e:
         return {"connected": False, "error": str(e)}

@router.get("/stats")
async def get_crm_stats(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Get CRM statistics"""
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_crm_connector(tenant_id, secret_service)
    
    try:
        stats = await connector.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats Error: {str(e)}")

@router.get("/contacts", response_model=List[ContactMessage])
async def list_contacts(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_crm_connector(tenant_id, secret_service)
    
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
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_crm_connector(tenant_id, secret_service)
    
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

@router.put("/contacts/{contact_id}", response_model=ContactMessage)
async def update_contact(
    contact_id: str,
    contact: ContactMessage,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_crm_connector(tenant_id, secret_service)
    
    try:
        payload = contact.dict(exclude={"id", "created_at"})
        result = await connector.update_contact(contact_id, payload)
        
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

@router.delete("/contacts/{contact_id}")
async def delete_contact(
    contact_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_crm_connector(tenant_id, secret_service)
    
    try:
        await connector.delete_contact(contact_id)
        return {"status": "success", "id": contact_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CRM Error: {str(e)}")

@router.get("/deals", response_model=List[DealMessage])
async def list_deals(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_crm_connector(tenant_id, secret_service)
    
    try:
        deals = await connector.get_deals()
        return [
            DealMessage(
                id=d.id,
                title=d.title,
                value=d.value,
                currency=d.currency,
                stage=d.stage,
                pipeline=d.pipeline,
                contact_ids=d.contact_ids,
                close_date=d.close_date
            ) for d in deals
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CRM Error: {str(e)}")

@router.post("/deals", response_model=DealMessage)
async def create_deal(
    deal: DealMessage,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_crm_connector(tenant_id, secret_service)
    
    try:
        payload = deal.dict(exclude={"id"})
        result = await connector.create_deal(payload)
        return DealMessage(**result.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CRM Error: {str(e)}")

@router.put("/deals/{deal_id}", response_model=DealMessage)
async def update_deal(
    deal_id: str,
    deal: DealMessage,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_crm_connector(tenant_id, secret_service)
    
    try:
        payload = deal.dict(exclude={"id"})
        result = await connector.update_deal(deal_id, payload)
        return DealMessage(**result.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CRM Error: {str(e)}")

@router.delete("/deals/{deal_id}")
async def delete_deal(
    deal_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    tenant_id = user.tenant_id or "default_tenant"
    connector = await get_active_crm_connector(tenant_id, secret_service)
    
    try:
        success = await connector.delete_deal(deal_id)
        if not success:
             raise HTTPException(status_code=400, detail="Failed to delete deal")
        return {"status": "success", "id": deal_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CRM Error: {str(e)}")
