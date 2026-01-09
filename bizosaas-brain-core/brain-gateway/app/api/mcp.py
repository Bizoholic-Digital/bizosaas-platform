from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_identity_port, get_current_user
from app.models.mcp import McpRegistry, McpCategory, UserMcpInstallation
from domain.ports.identity_port import IdentityPort, AuthenticatedUser
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

# Pydantic Models
class CategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str]
    icon: Optional[str]

    model_config = {"from_attributes": True}

class McpResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str]
    capabilities: List[str]
    is_official: bool
    rating: int
    install_count: int
    category_id: UUID

    model_config = {"from_attributes": True}

class InstallationRequest(BaseModel):
    mcp_slug: str
    config: Optional[dict] = None

# Routes
@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(McpCategory).order_by(McpCategory.sort_order).all()

@router.get("/registry", response_model=List[McpResponse])
def get_registry(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(McpRegistry)
    if category:
        query = query.join(McpCategory).filter(McpCategory.slug == category)
    return query.all()

@router.get("/installed")
def get_installed(
    db: Session = Depends(get_db),
    identity: IdentityPort = Depends(get_identity_port),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Get processed list of installed MCPs for the current user."""
    installations = db.query(UserMcpInstallation).filter(
        UserMcpInstallation.user_id == current_user.id
    ).all()
    
    # Return enriched data
    return [{
        "id": str(inst.id),
        "status": inst.status,
        "mcp": {
            "name": inst.mcp.name,
            "slug": inst.mcp.slug,
            "category": inst.mcp.category.slug,
            "icon": inst.mcp.category.icon
        }
    } for inst in installations]

@router.post("/install")
async def install_mcp(
    request: InstallationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    identity: IdentityPort = Depends(get_identity_port),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    mcp = db.query(McpRegistry).filter(McpRegistry.slug == request.mcp_slug).first()
    if not mcp:
        raise HTTPException(status_code=404, detail="MCP not found")
        
    # Check if already installed
    existing = db.query(UserMcpInstallation).filter(
        UserMcpInstallation.user_id == current_user.id,
        UserMcpInstallation.mcp_id == mcp.id
    ).first()
    
    if existing:
        return {"status": "already_installed", "id": str(existing.id)}
        
    # Create installation
    installation = UserMcpInstallation(
        user_id=current_user.id,
        mcp_id=mcp.id,
        status="pending",
        config=request.config or {}
    )
    db.add(installation)
    db.commit()
    db.refresh(installation) # Ensure we have the ID available
    
    # Trigger Provisioning Workflow
    from app.services.mcp_orchestrator import McpOrchestrator
    background_tasks.add_task(McpOrchestrator.provision_mcp, installation.id)
    
    return {"status": "pending", "id": str(installation.id), "message": "Installation started"}


# --- Migration Endpoints ---

class MigrationRequest(BaseModel):
    source_slug: str
    target_slug: str

@router.post("/migrate/preview")
async def preview_migration(req: MigrationRequest, current_user: AuthenticatedUser = Depends(get_current_user)):
    from app.services.migration_engine import MigrationService
    try:
        plan = await MigrationService.create_plan(req.source_slug, req.target_slug)
        return plan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/migrate/execute")
async def execute_migration(
    req: MigrationRequest, 
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    from app.services.migration_engine import MigrationService
    try:
        plan = await MigrationService.create_plan(req.source_slug, req.target_slug)
        
        # Execute in background
        background_tasks.add_task(MigrationService.execute_migration, plan, str(current_user.id))
        
        return {"status": "started", "plan": plan, "message": "Migration started in background"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
