from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.dependencies import get_db, get_workflow_port, get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.models.user import Tenant

router = APIRouter(prefix="/api/persona", tags=["persona"])

class PersonaGenerateRequest(BaseModel):
    website_url: Optional[str] = None
    onboarding_data: Optional[Dict[str, Any]] = None

class PersonaUpdateRequest(BaseModel):
    core_persona: Dict[str, Any]
    platform_variants: Optional[Dict[str, Any]] = None

@router.post("/generate")
async def generate_persona(
    request: PersonaGenerateRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    workflow_port = Depends(get_workflow_port),
    db: Session = Depends(get_db)
):
    """Initiate the autonomous persona generation workflow."""
    tenant_id = str(current_user.tenant_id or current_user.id)
    workflow_id = f"persona-{tenant_id}-{datetime.now().strftime('%Y%m%d%H%M')}"
    
    # If onboarding data not provided, try to fetch from tenant settings
    onboarding_data = request.onboarding_data
    if not onboarding_data:
        tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
        if tenant and tenant.settings:
            onboarding_data = tenant.settings.get("business_profile")

    try:
        await workflow_port.start_workflow(
            workflow_name="PersonaGenerationWorkflow",
            workflow_id=workflow_id,
            task_queue="brain-tasks",
            args=[{
                "tenant_id": tenant_id,
                "website_url": request.website_url,
                "onboarding_data": onboarding_data
            }]
        )
        return {"status": "success", "workflow_id": workflow_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_persona(
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve the current brand persona stored in tenant settings."""
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    persona_data = (tenant.settings or {}).get("persona", {})
    return persona_data

@router.put("/")
async def update_persona(
    request: PersonaUpdateRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Manually update the brand persona."""
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    current_settings = tenant.settings or {}
    current_settings["persona"] = request.dict()
    tenant.settings = current_settings
    
    db.add(tenant)
    db.commit()
    
    return {"status": "success", "message": "Persona updated successfully."}
