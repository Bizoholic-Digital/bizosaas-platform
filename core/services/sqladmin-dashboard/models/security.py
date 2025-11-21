"""
Security Data Models for SQLAdmin Dashboard
Handles audit logs, security events, permissions, and compliance
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, UUID, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class SecurityEventType(enum.Enum):
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    PASSWORD_CHANGE = "password_change"
    PERMISSION_CHANGE = "permission_change"
    DATA_ACCESS = "data_access"
    DATA_EXPORT = "data_export"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    BRUTE_FORCE_ATTEMPT = "brute_force_attempt"
    ACCOUNT_LOCKOUT = "account_lockout"
    API_KEY_CREATED = "api_key_created"
    API_KEY_REVOKED = "api_key_revoked"

class AuditActionType(enum.Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
    IMPORT = "import"
    LOGIN = "login"
    LOGOUT = "logout"

class RiskLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Security Events and Monitoring
class SecurityEventAdmin(Base):
    __tablename__ = "security_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Event details
    event_type = Column(Enum(SecurityEventType), nullable=False, index=True)
    event_category = Column(String(100), nullable=False)
    event_description = Column(Text, nullable=False)
    
    # Risk assessment
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.LOW)
    risk_score = Column(Float, default=0.0)
    
    # Context information
    ip_address = Column(String(45), index=True)
    user_agent = Column(Text)
    session_id = Column(String(255))
    
    # Geographic data
    country = Column(String(100))
    region = Column(String(100))
    city = Column(String(100))
    
    # Device information
    device_type = Column(String(50))
    device_fingerprint = Column(String(255))
    browser = Column(String(100))
    os = Column(String(100))
    
    # Additional metadata
    metadata = Column(JSON, default={})
    details = Column(JSON, default={})
    
    # Investigation status
    is_investigated = Column(Boolean, default=False)
    investigated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    investigated_at = Column(DateTime(timezone=True))
    investigation_notes = Column(Text)
    
    # Resolution
    is_resolved = Column(Boolean, default=False)
    resolution_action = Column(String(255))
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    resolved_at = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

# Comprehensive Audit Log
class AuditLogAdmin(Base):
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Action details
    action_type = Column(Enum(AuditActionType), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False, index=True)  # user, product, order, etc.
    resource_id = Column(UUID(as_uuid=True))
    resource_name = Column(String(255))
    
    # Change tracking
    old_values = Column(JSON)  # Previous state
    new_values = Column(JSON)  # New state
    changed_fields = Column(JSON, default=[])  # List of fields that changed
    
    # Request context
    ip_address = Column(String(45))
    user_agent = Column(Text)
    session_id = Column(String(255))
    request_id = Column(String(255))
    
    # API context
    endpoint = Column(String(500))
    method = Column(String(10))
    api_key_id = Column(UUID(as_uuid=True), ForeignKey("api_keys.id"))
    
    # Additional context
    description = Column(Text)
    metadata = Column(JSON, default={})
    
    # Success/failure
    is_successful = Column(Boolean, default=True)
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)

# Role-Based Access Control
class RoleAdmin(Base):
    __tablename__ = "roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))  # Nullable for system roles
    
    # Role details
    name = Column(String(100), nullable=False, index=True)
    display_name = Column(String(255))
    description = Column(Text)
    
    # Role hierarchy
    parent_role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    level = Column(Integer, default=0)
    
    # Role characteristics
    is_system_role = Column(Boolean, default=False)  # System-defined role
    is_default = Column(Boolean, default=False)  # Default role for new users
    is_assignable = Column(Boolean, default=True)  # Can be assigned to users
    
    # Permissions
    permissions = Column(JSON, default=[])  # List of permission names
    
    # Restrictions
    max_users = Column(Integer)  # Maximum users that can have this role
    expires_at = Column(DateTime(timezone=True))  # Role expiration
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    children = relationship("RoleAdmin", remote_side=[id])
    permissions_rel = relationship("PermissionAdmin", secondary="role_permissions", back_populates="roles")

# Granular Permissions
class PermissionAdmin(Base):
    __tablename__ = "permissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    
    # Permission details
    name = Column(String(100), unique=True, nullable=False, index=True)
    display_name = Column(String(255))
    description = Column(Text)
    
    # Permission categorization
    category = Column(String(100), nullable=False)  # user_management, billing, analytics, etc.
    resource_type = Column(String(100))  # What this permission applies to
    
    # Permission scope
    actions = Column(JSON, default=[])  # create, read, update, delete, export, etc.
    conditions = Column(JSON, default={})  # Conditional logic for permission
    
    # System information
    is_system_permission = Column(Boolean, default=False)
    is_dangerous = Column(Boolean, default=False)  # Requires special approval
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    roles = relationship("RoleAdmin", secondary="role_permissions", back_populates="permissions_rel")

# Role-Permission mapping table
class RolePermissionAdmin(Base):
    __tablename__ = "role_permissions"
    
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id"), primary_key=True)
    
    # Permission constraints
    conditions = Column(JSON, default={})  # Additional conditions for this specific assignment
    expires_at = Column(DateTime(timezone=True))  # Permission expiration
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# User-specific permission overrides
class UserPermissionAdmin(Base):
    __tablename__ = "user_permissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id"), nullable=False)
    
    # Override type
    is_granted = Column(Boolean, nullable=False)  # True = grant, False = revoke
    
    # Override constraints
    conditions = Column(JSON, default={})
    expires_at = Column(DateTime(timezone=True))
    
    # Justification
    reason = Column(Text)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# Data Access Tracking
class DataAccessLogAdmin(Base):
    __tablename__ = "data_access_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Access details
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(UUID(as_uuid=True))
    access_type = Column(String(50), nullable=False)  # view, download, export, etc.
    
    # Data sensitivity
    data_classification = Column(String(50))  # public, internal, confidential, restricted
    sensitive_fields = Column(JSON, default=[])  # List of sensitive fields accessed
    
    # Access context
    purpose = Column(String(255))  # Business purpose for access
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Query details (for database access)
    query = Column(Text)
    query_hash = Column(String(255))
    table_names = Column(JSON, default=[])
    row_count = Column(Integer)
    
    # File access (for file downloads/exports)
    file_path = Column(String(500))
    file_size = Column(Integer)
    
    # Approval workflow
    requires_approval = Column(Boolean, default=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)

# Security Compliance Reports
class ComplianceReportAdmin(Base):
    __tablename__ = "compliance_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Report details
    report_type = Column(String(100), nullable=False)  # gdpr, hipaa, sox, pci_dss, etc.
    report_period_start = Column(DateTime(timezone=True), nullable=False)
    report_period_end = Column(DateTime(timezone=True), nullable=False)
    
    # Compliance status
    overall_status = Column(String(50), nullable=False)  # compliant, non_compliant, pending
    compliance_score = Column(Float)  # 0-100 compliance score
    
    # Findings
    total_findings = Column(Integer, default=0)
    critical_findings = Column(Integer, default=0)
    high_findings = Column(Integer, default=0)
    medium_findings = Column(Integer, default=0)
    low_findings = Column(Integer, default=0)
    
    # Report data
    findings = Column(JSON, default=[])
    recommendations = Column(JSON, default=[])
    metrics = Column(JSON, default={})
    
    # Report metadata
    generated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Status tracking
    is_draft = Column(Boolean, default=True)
    is_final = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    finalized_at = Column(DateTime(timezone=True))

# Privacy and Data Protection
class DataRetentionPolicyAdmin(Base):
    __tablename__ = "data_retention_policies"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Policy details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Scope
    data_types = Column(JSON, nullable=False)  # Types of data this policy applies to
    resource_types = Column(JSON, default=[])  # Database tables, file types, etc.
    
    # Retention rules
    retention_period_days = Column(Integer, nullable=False)
    retention_conditions = Column(JSON, default={})
    
    # Actions
    expiration_action = Column(String(50), default="delete")  # delete, anonymize, archive
    notification_days_before = Column(Integer, default=30)
    
    # Legal basis (GDPR)
    legal_basis = Column(String(100))
    is_consent_based = Column(Boolean, default=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# Privacy Requests (GDPR, CCPA, etc.)
class PrivacyRequestAdmin(Base):
    __tablename__ = "privacy_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Request details
    request_type = Column(String(50), nullable=False)  # access, delete, portability, rectification
    status = Column(String(50), default="pending")  # pending, processing, completed, rejected
    
    # Requester information
    requester_email = Column(String(255), nullable=False)
    requester_name = Column(String(255))
    identity_verified = Column(Boolean, default=False)
    
    # Request scope
    data_types_requested = Column(JSON, default=[])
    specific_data = Column(Text)  # Specific data requested
    
    # Processing
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    processing_notes = Column(Text)
    verification_method = Column(String(100))
    
    # Response
    response_data = Column(JSON)  # Data provided in response
    response_method = Column(String(50))  # email, download, mail, etc.
    rejection_reason = Column(Text)
    
    # Compliance deadlines
    received_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    due_date = Column(DateTime(timezone=True))  # Legal deadline for response
    completed_at = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)