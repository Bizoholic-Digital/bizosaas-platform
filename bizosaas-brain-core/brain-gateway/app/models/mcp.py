from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .base import Base
from .utils import GUID

class McpCategory(Base):
    __tablename__ = "mcp_categories"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)  # Lucide icon name
    sort_order = Column(Integer, default=0)
    
    # Relationships
    mcps = relationship("McpRegistry", back_populates="category")

class McpRegistry(Base):
    __tablename__ = "mcp_registry"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    author = Column(String(100), nullable=True)
    homepage_url = Column(String(255), nullable=True)
    source_url = Column(String(255), nullable=True)
    
    # Source Classification
    source_type = Column(String(50), default='community')  # 'official', 'community', 'custom'
    package_name = Column(String(255), nullable=True)  # npm/pip package
    hosted_url = Column(String(500), nullable=True)  # If remotely hosted (e.g., mcp.saleor.app)
    documentation_url = Column(String(500), nullable=True)
    
    # Creator Info
    creator_name = Column(String(255), nullable=True)
    creator_org = Column(String(255), nullable=True)
    
    # Quality Metrics (GitHub-based)
    github_stars = Column(Integer, default=0)
    github_forks = Column(Integer, default=0)
    last_commit_date = Column(DateTime(timezone=True), nullable=True)
    is_maintained = Column(Boolean, default=True)
    security_audit_status = Column(String(50), default='not_required')  # 'passed', 'pending', 'failed', 'not_required'
    quality_score = Column(Integer, default=50)  # 0-100 computed score
    
    # Tags for filtering
    tags = Column(JSON, default=list)  # ['read-only', 'graphql', 'rest', etc.]
    
    # Business & Management
    affiliate_link = Column(String(255), nullable=True)
    vendor_name = Column(String(100), nullable=True)
    sort_order = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    is_recommended = Column(Boolean, default=False)  # Quality score >= 80
    
    # Configuration
    category_id = Column(GUID, ForeignKey("mcp_categories.id"), nullable=False, index=True)
    capabilities = Column(JSON, default=list)  # ["products", "orders", "analytics"]
    mcp_config = Column(JSON, nullable=False)  # { "type": "docker", "image": "...", "env": [...] }
    is_official = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    rating = Column(Integer, default=0, index=True)
    install_count = Column(Integer, default=0, index=True)
    
    # Sync Metadata
    external_id = Column(String(100), nullable=True) # ID in external market (mcpmarket.com)
    sync_metadata = Column(JSON, nullable=True) # { "version": "1.2.0", "upstream_repo": "..." }
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    category = relationship("McpCategory", back_populates="mcps")
    installations = relationship("UserMcpInstallation", back_populates="mcp")


class UserMcpInstallation(Base):
    __tablename__ = "user_mcp_installations"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False, index=True)  # Clerk user IDs are strings
    mcp_id = Column(GUID, ForeignKey("mcp_registry.id", ondelete="CASCADE"), nullable=False)
    
    status = Column(String(20), default="pending", nullable=False, index=True)  # pending, installed, configured, error, stopped
    config = Column(JSON, nullable=True)  # User-specific config overrides
    credentials_path = Column(String(255), nullable=True)  # Vault path
    error_message = Column(Text, nullable=True)
    
    last_health_check = Column(DateTime(timezone=True), nullable=True)
    is_healthy = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    # Note: user relationship removed - using Clerk user IDs which don't map to users table
    mcp = relationship("McpRegistry", back_populates="installations")

class MarketplaceProductMap(Base):
    __tablename__ = "marketplace_product_maps"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False, index=True)
    
    shopify_product_id = Column(String(100), nullable=False, index=True)
    shopify_variant_id = Column(String(100), nullable=True)
    
    marketplace_slug = Column(String(50), nullable=False, index=True) # e.g., 'flipkart', 'meesho'
    marketplace_product_id = Column(String(100), nullable=True, index=True)
    marketplace_sku = Column(String(100), nullable=True)
    
    sync_status = Column(String(20), default="synced") # synced, pending, error
    last_sync_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    metadata_json = Column(JSON, nullable=True) # Store marketplace-specific attributes
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class McpApprovalRequest(Base):
    """
    Tracks requests for installing, developing, or reviewing MCPs.
    Can be initiated by AI agents or human users.
    """
    __tablename__ = "mcp_approval_requests"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    
    # Request Type
    request_type = Column(String(50), nullable=False)  # 'install', 'develop_custom', 'security_review', 'use_boilerplate'
    
    # MCP Details
    mcp_name = Column(String(255), nullable=False)
    mcp_repository_url = Column(String(500), nullable=True)
    mcp_description = Column(Text, nullable=True)
    mcp_category = Column(String(100), nullable=True)
    
    # Requester (Agent or Human)
    requested_by_agent = Column(String(255), nullable=True)  # Agent ID if AI-initiated
    requested_by_user = Column(String(255), nullable=True)   # User ID if human-initiated
    
    # Analysis (AI-generated for custom builds)
    use_case_description = Column(Text, nullable=True)
    existing_alternatives = Column(Text, nullable=True)  # List of alternatives considered
    recommendation = Column(String(50), nullable=True)  # 'use_existing', 'use_as_boilerplate', 'build_from_scratch'
    security_assessment = Column(Text, nullable=True)
    estimated_effort = Column(String(50), nullable=True)  # 'small', 'medium', 'large'
    pros = Column(JSON, default=list)
    cons = Column(JSON, default=list)
    
    # Quality Assessment (for review requests)
    source_quality_score = Column(Integer, nullable=True)
    is_code_secure = Column(Boolean, nullable=True)
    follows_gold_standards = Column(Boolean, nullable=True)
    
    # Approval
    status = Column(String(50), default='pending')  # 'pending', 'approved', 'rejected', 'in_progress', 'completed'
    reviewed_by = Column(String(255), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    review_notes = Column(Text, nullable=True)
    
    # Development Assignment
    assigned_crew = Column(String(255), nullable=True)  # CrewAI team name
    development_status = Column(String(50), nullable=True)  # 'assigned', 'developing', 'testing', 'deployed'
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class KagRelationship(Base):
    """
    Stores persistent knowledge graph relationships for KAG.
    """
    __tablename__ = "kag_relationships"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    source_tool = Column(String(100), nullable=False, index=True) # MCP Slug
    target_tool = Column(String(100), nullable=False, index=True) # MCP Slug
    relationship_type = Column(String(50), nullable=False) # 'feeds_into', 'emergent_workflow', etc.
    strength = Column(Integer, default=10) # 0-100 (maps to 0.0-1.0)
    evidence_count = Column(Integer, default=1)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
