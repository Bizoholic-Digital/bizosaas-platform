from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_identity_port, get_current_user, require_role, require_feature
from app.models.mcp import McpRegistry, McpCategory, UserMcpInstallation
from domain.ports.identity_port import IdentityPort, AuthenticatedUser
from typing import List, Optional
from datetime import datetime
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
    is_recommended: bool
    rating: int
    install_count: int
    category_id: UUID
    
    # Source & Quality
    source_type: str
    source_url: Optional[str] = None
    package_name: Optional[str] = None
    hosted_url: Optional[str] = None
    quality_score: int
    github_stars: int
    tags: List[str] = []
    
    # Business & Management
    vendor_name: Optional[str] = None
    affiliate_link: Optional[str] = None
    sort_order: int = 0
    is_featured: bool = False

    model_config = {"from_attributes": True}

class McpApprovalCreateRequest(BaseModel):
    request_type: str
    mcp_name: str
    mcp_repository_url: Optional[str] = None
    mcp_description: Optional[str] = None
    mcp_category: Optional[str] = None
    use_case_description: Optional[str] = None

class McpApprovalResponse(BaseModel):
    id: UUID
    request_type: str
    mcp_name: str
    status: str
    requested_by_agent: Optional[str]
    requested_by_user: Optional[str]
    recommendation: Optional[str]
    quality_score: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}

class McpUpdateRequest(BaseModel):
    vendor_name: Optional[str] = None
    affiliate_link: Optional[str] = None
    sort_order: Optional[int] = None
    is_featured: Optional[bool] = None
    description: Optional[str] = None

class McpCreateRequest(BaseModel):
    name: str
    slug: str
    category_id: UUID
    description: Optional[str] = None
    capabilities: List[str] = []
    mcp_config: dict
    vendor_name: Optional[str] = None
    affiliate_link: Optional[str] = None
    is_official: bool = False
    sort_order: int = 0
    is_featured: bool = False


class InstallationRequest(BaseModel):
    mcp_slug: str
    config: Optional[dict] = None

class ToolCallRequest(BaseModel):
    mcp_slug: str
    tool_name: str
    arguments: dict

# Routes
@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(McpCategory).order_by(McpCategory.sort_order).all()

@router.get("/registry", response_model=List[McpResponse])
def get_registry(
    category: Optional[str] = None, 
    recommended_only: bool = False,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(McpRegistry)
    
    if category:
        query = query.join(McpCategory).filter(McpCategory.slug == category)
    
    if recommended_only:
        query = query.filter(McpRegistry.is_recommended == True)
        
    if search:
        query = query.filter(
            (McpRegistry.name.ilike(f"%{search}%")) | 
            (McpRegistry.description.ilike(f"%{search}%")) |
            (McpRegistry.tags.cast(String).ilike(f"%{search}%"))
        )
        
    return query.order_by(McpRegistry.sort_order.asc(), McpRegistry.name.asc()).all()

@router.post("/", response_model=McpResponse, status_code=status.HTTP_201_CREATED)
def create_mcp(
    request: McpCreateRequest,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Admin only: Create a new MCP in the global registry."""
    # Check if slug exists
    if db.query(McpRegistry).filter(McpRegistry.slug == request.slug).first():
        raise HTTPException(status_code=400, detail="MCP with this slug already exists")
    
    mcp_data = request.model_dump()
    mcp = McpRegistry(**mcp_data)
    
    # Calculate quality score and auto-tag
    from app.services.mcp_curator import McpCuratorService
    McpCuratorService.classify_and_tag(mcp)
    
    db.add(mcp)
    db.commit()
    db.refresh(mcp)
    return mcp

@router.delete("/{mcp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mcp(
    mcp_id: UUID,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Admin only: Remove an MCP from the registry."""
    mcp = db.query(McpRegistry).filter(McpRegistry.id == mcp_id).first()
    if not mcp:
        raise HTTPException(status_code=404, detail="MCP not found")
        
    db.delete(mcp)
    db.commit()
    return None

@router.patch("/{mcp_id}", response_model=McpResponse)
def update_mcp(
    mcp_id: UUID,
    update_data: McpUpdateRequest,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Admin only: Update an existing MCP's details."""
    mcp = db.query(McpRegistry).filter(McpRegistry.id == mcp_id).first()
    if not mcp:
        raise HTTPException(status_code=404, detail="MCP not found")
        
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(mcp, key, value)
        
    # Recalculate quality score and tags
    from app.services.mcp_curator import McpCuratorService
    McpCuratorService.classify_and_tag(mcp)
        
    db.commit()
    db.refresh(mcp)
    return mcp

# --- Approval Workflow Endpoints ---

@router.get("/approvals", response_model=List[McpApprovalResponse])
def list_approvals(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Admin only: List pending/processed approval requests."""
    from app.models.mcp import McpApprovalRequest
    query = db.query(McpApprovalRequest)
    if status:
        query = query.filter(McpApprovalRequest.status == status)
    return query.order_by(McpApprovalRequest.created_at.desc()).all()

@router.post("/approvals", response_model=McpApprovalResponse)
def create_approval_request(
    request: McpApprovalCreateRequest,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Submit a new MCP for approval (can be called by agents via internal API)."""
    from app.models.mcp import McpApprovalRequest
    
    approval = McpApprovalRequest(
        **request.model_dump(),
        requested_by_user=str(current_user.id)
    )
    
    # If the user is an agent (detected by role or metadata), mark accordingly
    # For now, we use a simple check or allow agents to pass their ID
    
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval

@router.post("/approvals/{approval_id}/review")
def review_approval(
    approval_id: UUID,
    status: str, # 'approved', 'rejected'
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Admin only: Approve or reject an MCP request."""
    from app.models.mcp import McpApprovalRequest
    approval = db.query(McpApprovalRequest).filter(McpApprovalRequest.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")
        
    approval.status = status
    approval.review_notes = notes
    approval.reviewed_by = str(current_user.id)
    approval.reviewed_at = datetime.utcnow()
    
    db.commit()
    return {"status": "updated", "id": str(approval.id)}

# --- Agent Access Endpoints ---

@router.get("/agent/available", response_model=List[McpResponse])
def agent_get_available(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Accessible by AI agents: List all available MCPs in the registry."""
    query = db.query(McpRegistry).filter(McpRegistry.status == 'available')
    if category:
        query = query.join(McpCategory).filter(McpCategory.slug == category)
    return query.all()

@router.get("/agent/installed", response_model=List[McpResponse])
def agent_get_installed(
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Accessible by AI agents: List currently installed MCPs for the context."""
    installations = db.query(UserMcpInstallation).filter(
        UserMcpInstallation.user_id == current_user.id,
        UserMcpInstallation.status == 'active'
    ).all()
    return [inst.mcp for inst in installations]

@router.post("/agent/request", response_model=McpApprovalResponse)
def agent_request_mcp(
    request: McpApprovalCreateRequest,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(require_feature("tools"))
):
    """AI agents call this to request a new MCP if they find a gap in their toolkit."""
    from app.models.mcp import McpApprovalRequest
    
    # Logic to check if a similar request already exists
    existing = db.query(McpApprovalRequest).filter(
        McpApprovalRequest.mcp_name == request.mcp_name,
        McpApprovalRequest.status == 'pending'
    ).first()
    
    if existing:
        return existing
        
    approval = McpApprovalRequest(
        **request.model_dump(),
        requested_by_user=str(current_user.id),
        requested_by_agent="Agent-Prime" # Replace with actual agent ID if available
    )
    
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval

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
    current_user: AuthenticatedUser = Depends(require_feature("tools"))
):
    from app.services.mcp_installation_service import McpInstallationService
    
    try:
        # Use our secure installation service instead of manual DB code
        installation = await McpInstallationService.install_with_vault(
            db=db,
            user_id=str(current_user.id),
            mcp_slug=request.mcp_slug,
            config=request.config or {}
        )
        
        # Trigger Provisioning Workflow
        from app.services.mcp_orchestrator import McpOrchestrator
        background_tasks.add_task(McpOrchestrator.provision_mcp, installation.id)
        
        return {"status": "pending", "id": str(installation.id), "message": "Installation started"}
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Installation failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during installation")


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

# --- Tool Execution Endpoints ---

@router.get("/tools")
async def list_available_tools(
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """List all tools across all active MCPs for the current user."""
    from app.services.mcp_gateway import MCPGateway
    gateway = MCPGateway(db)
    return await gateway.list_tools(str(current_user.id))

@router.post("/tools/call")
async def call_mcp_tool(
    request: ToolCallRequest,
    db: Session = Depends(get_db),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """Call a specific tool on an installed MCP."""
    from app.services.mcp_gateway import MCPGateway
    gateway = MCPGateway(db)
    try:
        result = await gateway.call_tool(
            user_id=str(current_user.id),
            mcp_slug=request.mcp_slug,
            tool_name=request.tool_name,
            arguments=request.arguments
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
