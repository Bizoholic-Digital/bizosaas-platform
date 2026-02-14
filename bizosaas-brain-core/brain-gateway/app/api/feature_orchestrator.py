"""
Feature Orchestrator API
Exposes centralized feature management to the Admin Portal.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.dependencies import get_db, require_role
from app.services.feature_orchestrator import FeatureOrchestrator, FeatureScope
from app.domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/features", tags=["feature-orchestrator"])


class FeatureConfigUpdate(BaseModel):
    """Request to update feature configuration"""
    config: dict


class RolloutUpdate(BaseModel):
    """Request to update rollout percentage"""
    percentage: int


@router.get("/matrix")
async def get_feature_matrix(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get the complete feature matrix organized by scope.
    """
    orchestrator = FeatureOrchestrator(db)
    matrix = await orchestrator.get_feature_matrix()
    
    return {
        "feature_matrix": matrix,
        "total_features": sum(len(features) for features in matrix.values())
    }


@router.get("/all")
async def get_all_features(
    scope: Optional[str] = None,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get all features, optionally filtered by scope.
    """
    orchestrator = FeatureOrchestrator(db)
    
    scope_enum = None
    if scope:
        try:
            scope_enum = FeatureScope(scope)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid scope: {scope}")
    
    features = await orchestrator.get_all_features(scope_enum)
    
    return {
        "total": len(features),
        "features": [f.dict() for f in features]
    }


@router.get("/{feature_id}")
async def get_feature(
    feature_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get details of a specific feature.
    """
    orchestrator = FeatureOrchestrator(db)
    feature = await orchestrator.get_feature(feature_id)
    
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    # Get dependencies and dependents
    dependencies = await orchestrator.get_feature_dependencies(feature_id)
    dependents = await orchestrator.get_feature_dependents(feature_id)
    
    return {
        "feature": feature.dict(),
        "dependencies": [d.dict() for d in dependencies],
        "dependents": [d.dict() for d in dependents]
    }


@router.post("/{feature_id}/enable")
async def enable_feature(
    feature_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Enable a feature.
    """
    orchestrator = FeatureOrchestrator(db)
    
    try:
        result = await orchestrator.enable_feature(feature_id, user.user_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{feature_id}/disable")
async def disable_feature(
    feature_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Disable a feature.
    """
    orchestrator = FeatureOrchestrator(db)
    
    try:
        result = await orchestrator.disable_feature(feature_id, user.user_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{feature_id}/config")
async def update_feature_config(
    feature_id: str,
    update: FeatureConfigUpdate,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Update feature configuration.
    """
    orchestrator = FeatureOrchestrator(db)
    
    try:
        result = await orchestrator.update_feature_config(
            feature_id,
            update.config,
            user.user_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{feature_id}/rollout")
async def set_rollout_percentage(
    feature_id: str,
    update: RolloutUpdate,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Set gradual rollout percentage for a feature.
    """
    orchestrator = FeatureOrchestrator(db)
    
    try:
        result = await orchestrator.set_rollout_percentage(
            feature_id,
            update.percentage,
            user.user_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{feature_id}/tenant/{tenant_id}/enabled")
async def check_feature_for_tenant(
    feature_id: str,
    tenant_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Check if a feature is enabled for a specific tenant.
    """
    orchestrator = FeatureOrchestrator(db)
    enabled = await orchestrator.is_feature_enabled_for_tenant(feature_id, tenant_id)
    
    return {
        "feature_id": feature_id,
        "tenant_id": tenant_id,
        "enabled": enabled
    }
