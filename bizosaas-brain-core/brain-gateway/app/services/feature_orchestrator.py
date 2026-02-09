"""
Centralized Feature Orchestrator
Master control interface for managing features across Client Portal, Admin Portal, and Business Directory.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from enum import Enum
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class FeatureScope(str, Enum):
    """Scope of a feature"""
    CLIENT_PORTAL = "client_portal"
    ADMIN_PORTAL = "admin_portal"
    BUSINESS_DIRECTORY = "business_directory"
    PLATFORM_WIDE = "platform_wide"


class FeatureStatus(str, Enum):
    """Status of a feature"""
    ENABLED = "enabled"
    DISABLED = "disabled"
    BETA = "beta"
    DEPRECATED = "deprecated"


class FeatureDefinition(BaseModel):
    """Definition of a platform feature"""
    id: str
    name: str
    description: str
    scope: FeatureScope
    status: FeatureStatus
    dependencies: List[str] = []
    config: Dict[str, Any] = {}
    rollout_percentage: int = 100  # 0-100 for gradual rollout
    tenant_whitelist: List[str] = []  # Specific tenants for beta features
    tenant_blacklist: List[str] = []  # Tenants to exclude


class FeatureOrchestrator:
    """
    Centralized orchestrator for managing all platform features.
    Provides a single interface to control features across all portals.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.features: Dict[str, FeatureDefinition] = {}
        self._load_features()
    
    def _load_features(self):
        """
        Load all platform features.
        In production, this would load from database.
        """
        # Client Portal Features
        self.features["onboarding_wizard"] = FeatureDefinition(
            id="onboarding_wizard",
            name="AI-Powered Onboarding Wizard",
            description="Multi-step onboarding with AI tool selection and strategy generation",
            scope=FeatureScope.CLIENT_PORTAL,
            status=FeatureStatus.ENABLED,
            config={"steps": 6, "ai_enabled": True}
        )
        
        self.features["campaign_dashboard"] = FeatureDefinition(
            id="campaign_dashboard",
            name="Campaign Dashboard",
            description="Real-time campaign performance tracking",
            scope=FeatureScope.CLIENT_PORTAL,
            status=FeatureStatus.ENABLED,
            dependencies=["onboarding_wizard"]
        )
        
        self.features["ai_chat_assistant"] = FeatureDefinition(
            id="ai_chat_assistant",
            name="AI Chat Assistant",
            description="Conversational AI for campaign optimization",
            scope=FeatureScope.CLIENT_PORTAL,
            status=FeatureStatus.BETA,
            rollout_percentage=50
        )
        
        # Admin Portal Features
        self.features["workflow_governance"] = FeatureDefinition(
            id="workflow_governance",
            name="Workflow Governance",
            description="Approve/reject/refine agent-proposed workflows",
            scope=FeatureScope.ADMIN_PORTAL,
            status=FeatureStatus.ENABLED
        )
        
        self.features["admin_prime_copilot"] = FeatureDefinition(
            id="admin_prime_copilot",
            name="Admin Prime Copilot",
            description="AI-powered platform management assistant",
            scope=FeatureScope.ADMIN_PORTAL,
            status=FeatureStatus.ENABLED
        )
        
        self.features["tenant_analytics"] = FeatureDefinition(
            id="tenant_analytics",
            name="Advanced Tenant Analytics",
            description="Deep analytics on tenant behavior and performance",
            scope=FeatureScope.ADMIN_PORTAL,
            status=FeatureStatus.BETA,
            rollout_percentage=100
        )
        
        # Business Directory Features
        self.features["directory_listing"] = FeatureDefinition(
            id="directory_listing",
            name="Business Directory Listings",
            description="Public business directory with SEO optimization",
            scope=FeatureScope.BUSINESS_DIRECTORY,
            status=FeatureStatus.ENABLED
        )
        
        self.features["claim_verification"] = FeatureDefinition(
            id="claim_verification",
            name="Business Claim Verification",
            description="Automated verification for business claims",
            scope=FeatureScope.BUSINESS_DIRECTORY,
            status=FeatureStatus.ENABLED
        )
        
        # Platform-Wide Features
        self.features["agentic_workflows"] = FeatureDefinition(
            id="agentic_workflows",
            name="Autonomous Agentic Workflows",
            description="AI-driven workflow discovery and execution",
            scope=FeatureScope.PLATFORM_WIDE,
            status=FeatureStatus.ENABLED,
            dependencies=["workflow_governance"]
        )
        
        self.features["real_time_monitoring"] = FeatureDefinition(
            id="real_time_monitoring",
            name="Real-time Monitoring & Alerts",
            description="Live monitoring with WebSocket-based alerts",
            scope=FeatureScope.PLATFORM_WIDE,
            status=FeatureStatus.BETA,
            rollout_percentage=100
        )
    
    async def get_all_features(self, scope: Optional[FeatureScope] = None) -> List[FeatureDefinition]:
        """
        Get all features, optionally filtered by scope.
        """
        features = list(self.features.values())
        
        if scope:
            features = [f for f in features if f.scope == scope]
        
        return features
    
    async def get_feature(self, feature_id: str) -> Optional[FeatureDefinition]:
        """
        Get a specific feature by ID.
        """
        return self.features.get(feature_id)
    
    async def enable_feature(self, feature_id: str, admin_id: str) -> Dict[str, Any]:
        """
        Enable a feature.
        """
        feature = self.features.get(feature_id)
        if not feature:
            raise ValueError(f"Feature not found: {feature_id}")
        
        # Check dependencies
        for dep_id in feature.dependencies:
            dep = self.features.get(dep_id)
            if not dep or dep.status != FeatureStatus.ENABLED:
                raise ValueError(f"Dependency not met: {dep_id} must be enabled first")
        
        feature.status = FeatureStatus.ENABLED
        
        logger.info(f"Feature '{feature_id}' enabled by admin {admin_id}")
        
        # TODO: Persist to database
        # TODO: Trigger feature activation hooks
        
        return {
            "status": "success",
            "message": f"Feature '{feature.name}' enabled",
            "feature": feature.dict()
        }
    
    async def disable_feature(self, feature_id: str, admin_id: str) -> Dict[str, Any]:
        """
        Disable a feature.
        """
        feature = self.features.get(feature_id)
        if not feature:
            raise ValueError(f"Feature not found: {feature_id}")
        
        # Check if other features depend on this
        dependents = [f for f in self.features.values() if feature_id in f.dependencies and f.status == FeatureStatus.ENABLED]
        if dependents:
            dependent_names = [f.name for f in dependents]
            raise ValueError(f"Cannot disable: Features {dependent_names} depend on this feature")
        
        feature.status = FeatureStatus.DISABLED
        
        logger.info(f"Feature '{feature_id}' disabled by admin {admin_id}")
        
        # TODO: Persist to database
        # TODO: Trigger feature deactivation hooks
        
        return {
            "status": "success",
            "message": f"Feature '{feature.name}' disabled",
            "feature": feature.dict()
        }
    
    async def update_feature_config(
        self,
        feature_id: str,
        config: Dict[str, Any],
        admin_id: str
    ) -> Dict[str, Any]:
        """
        Update feature configuration.
        """
        feature = self.features.get(feature_id)
        if not feature:
            raise ValueError(f"Feature not found: {feature_id}")
        
        feature.config = {**feature.config, **config}
        
        logger.info(f"Feature '{feature_id}' config updated by admin {admin_id}")
        
        # TODO: Persist to database
        # TODO: Trigger config update hooks
        
        return {
            "status": "success",
            "message": f"Configuration updated for '{feature.name}'",
            "config": feature.config
        }
    
    async def set_rollout_percentage(
        self,
        feature_id: str,
        percentage: int,
        admin_id: str
    ) -> Dict[str, Any]:
        """
        Set gradual rollout percentage for a feature.
        """
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        
        feature = self.features.get(feature_id)
        if not feature:
            raise ValueError(f"Feature not found: {feature_id}")
        
        feature.rollout_percentage = percentage
        
        logger.info(f"Feature '{feature_id}' rollout set to {percentage}% by admin {admin_id}")
        
        return {
            "status": "success",
            "message": f"Rollout percentage set to {percentage}% for '{feature.name}'",
            "rollout_percentage": percentage
        }
    
    async def is_feature_enabled_for_tenant(
        self,
        feature_id: str,
        tenant_id: str
    ) -> bool:
        """
        Check if a feature is enabled for a specific tenant.
        Considers rollout percentage, whitelist, and blacklist.
        """
        feature = self.features.get(feature_id)
        if not feature:
            return False
        
        # Check status
        if feature.status == FeatureStatus.DISABLED:
            return False
        
        # Check blacklist
        if tenant_id in feature.tenant_blacklist:
            return False
        
        # Check whitelist (for beta features)
        if feature.status == FeatureStatus.BETA and feature.tenant_whitelist:
            return tenant_id in feature.tenant_whitelist
        
        # Check rollout percentage
        if feature.rollout_percentage < 100:
            # Use consistent hash to determine if tenant is in rollout
            tenant_hash = hash(tenant_id) % 100
            return tenant_hash < feature.rollout_percentage
        
        return True
    
    async def get_feature_dependencies(self, feature_id: str) -> List[FeatureDefinition]:
        """
        Get all dependencies for a feature.
        """
        feature = self.features.get(feature_id)
        if not feature:
            return []
        
        dependencies = []
        for dep_id in feature.dependencies:
            dep = self.features.get(dep_id)
            if dep:
                dependencies.append(dep)
        
        return dependencies
    
    async def get_feature_dependents(self, feature_id: str) -> List[FeatureDefinition]:
        """
        Get all features that depend on this feature.
        """
        return [f for f in self.features.values() if feature_id in f.dependencies]
    
    async def get_feature_matrix(self) -> Dict[str, Any]:
        """
        Get a comprehensive matrix of all features organized by scope.
        """
        matrix = {
            "client_portal": [],
            "admin_portal": [],
            "business_directory": [],
            "platform_wide": []
        }
        
        for feature in self.features.values():
            scope_key = feature.scope.value
            matrix[scope_key].append({
                "id": feature.id,
                "name": feature.name,
                "status": feature.status.value,
                "rollout_percentage": feature.rollout_percentage,
                "dependencies": feature.dependencies
            })
        
        return matrix


async def get_feature_orchestrator(db: Session) -> FeatureOrchestrator:
    """Helper to get feature orchestrator instance."""
    return FeatureOrchestrator(db)
