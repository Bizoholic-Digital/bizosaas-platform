from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.domain.ports.identity_port import AuthenticatedUser
from app.models.prompt import PromptTemplate
from app.core.prompt_enhancer import prompt_enhancer

router = APIRouter(prefix="/api/prompts", tags=["prompts"])

class PromptTemplateCreate(BaseModel):
    name: str
    category: str = "instruction"
    template_text: str
    variables: Dict[str, Any] = {}
    strategy: str = "basic"
    is_default: bool = False
    tenant_id: Optional[str] = None
    version: str = "1.0.0"

class EnhanceTestRequest(BaseModel):
    agent_type: str
    task_description: str
    payload: Dict[str, Any] = {}
    tenant_id: Optional[str] = None

@router.get("/", response_model=List[Dict[str, Any]])
async def list_prompts(
    category: Optional[str] = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all available prompt templates."""
    query = db.query(PromptTemplate)
    if category:
        query = query.filter(PromptTemplate.category == category)
    
    # Non-admins only see global defaults or their own tenant templates
    if "Super Admin" not in current_user.roles:
        query = query.filter(
            (PromptTemplate.tenant_id == str(current_user.tenant_id)) | 
            (PromptTemplate.tenant_id == None)
        )
        
    templates = query.all()
    return [t.to_dict() for t in templates]

@router.post("/", status_code=201)
async def create_prompt_template(
    request: PromptTemplateCreate,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new prompt template."""
    # Only admins or specific roles can create templates
    if "Super Admin" not in current_user.roles and "Partner" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Insufficient permissions to create templates")

    # If tenant_id provided by non-admin, ensure it matches their own
    if request.tenant_id and "Super Admin" not in current_user.roles:
        if request.tenant_id != str(current_user.tenant_id):
             raise HTTPException(status_code=403, detail="Cannot create templates for other tenants")

    new_template = PromptTemplate(
        name=request.name,
        category=request.category,
        template_text=request.template_text,
        variables=request.variables,
        strategy=request.strategy,
        is_default=request.is_default,
        tenant_id=request.tenant_id,
        version=request.version
    )
    
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    
    return new_template.to_dict()

@router.post("/enhance-test")
async def test_enhancement(
    request: EnhanceTestRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Test the prompt enhancement logic without calling an AI agent."""
    tenant_id = request.tenant_id or str(current_user.tenant_id)
    
    # Ensure tenant access
    if "Super Admin" not in current_user.roles and tenant_id != str(current_user.tenant_id):
        raise HTTPException(status_code=403, detail="Access denied to requested tenant context")

    enhanced = await prompt_enhancer.enhance_prompt(
        agent_type=request.agent_type,
        task_description=request.task_description,
        input_data=request.payload,
        tenant_id=tenant_id
    )
    
    return enhanced
