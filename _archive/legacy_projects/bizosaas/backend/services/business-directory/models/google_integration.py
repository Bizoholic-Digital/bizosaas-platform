"""
Google Business Profile Integration Models
Database models for managing Google My Business API integration and synchronization
"""

from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Index, DateTime, Integer, JSON, BigInteger
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from typing import Optional, List, Dict, Any
import json
import uuid
from datetime import datetime
from enum import Enum

from .base import BaseModel, TenantMixin, register_model


class GoogleAccountStatus(str, Enum):
    """Google account connection status"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    EXPIRED = "expired"
    ERROR = "error"
    REVOKED = "revoked"


class SyncStatus(str, Enum):
    """Synchronization status for various operations"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ConflictResolutionStrategy(str, Enum):
    """Strategy for resolving data conflicts"""
    GOOGLE_PRIORITY = "google_priority"
    LOCAL_PRIORITY = "local_priority"
    MANUAL = "manual"
    MERGE = "merge"


@register_model
class GoogleAccount(BaseModel):
    """
    Google account connection and OAuth credentials per tenant
    """
    __tablename__ = "google_accounts"
    
    # Account identification
    google_account_id = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Google account ID"
    )
    
    email = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Google account email"
    )
    
    display_name = Column(
        String(255),
        nullable=True,
        doc="Google account display name"
    )
    
    # OAuth credentials (encrypted)
    access_token = Column(
        Text,
        nullable=False,
        doc="Encrypted OAuth access token"
    )
    
    refresh_token = Column(
        Text,
        nullable=True,
        doc="Encrypted OAuth refresh token"
    )
    
    token_expires_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="Access token expiration time"
    )
    
    # Account status
    status = Column(
        String(20),
        nullable=False,
        default=GoogleAccountStatus.CONNECTED.value,
        index=True,
        doc="Account connection status"
    )
    
    last_sync_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="Last successful sync timestamp"
    )
    
    # Permissions and scopes
    granted_scopes = Column(
        JSONB,
        nullable=True,
        doc="OAuth scopes granted by user"
    )
    
    # Connection metadata
    connected_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        doc="When account was first connected"
    )
    
    last_error = Column(
        Text,
        nullable=True,
        doc="Last error message if any"
    )
    
    error_count = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Consecutive error count"
    )
    
    @validates('status')
    def validate_status(self, key, status):
        """Validate status is valid enum value"""
        valid_statuses = [s.value for s in GoogleAccountStatus]
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")
        return status
    
    def __repr__(self):
        return f"<GoogleAccount(email='{self.email}', tenant_id='{self.tenant_id}')>"
    
    @property
    def is_active(self) -> bool:
        """Check if account is actively connected"""
        return self.status == GoogleAccountStatus.CONNECTED.value
    
    @property
    def is_token_expired(self) -> bool:
        """Check if access token is expired"""
        if not self.token_expires_at:
            return False
        return datetime.utcnow() > self.token_expires_at
    
    def mark_error(self, error_message: str):
        """Mark account as having an error"""
        self.last_error = error_message
        self.error_count += 1
        if self.error_count >= 5:  # Too many consecutive errors
            self.status = GoogleAccountStatus.ERROR.value
    
    def clear_error(self):
        """Clear error state"""
        self.last_error = None
        self.error_count = 0
        if self.status == GoogleAccountStatus.ERROR.value:
            self.status = GoogleAccountStatus.CONNECTED.value


@register_model
class GoogleBusinessLocation(BaseModel):
    """
    Google My Business location data cache
    """
    __tablename__ = "google_business_locations"
    
    # Google location identification
    google_location_id = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        doc="Google My Business location ID"
    )
    
    google_account_id = Column(
        UUID(as_uuid=True),
        ForeignKey('google_accounts.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        doc="Associated Google account"
    )
    
    google_account = relationship("GoogleAccount", backref="locations")
    
    # Location data (cached from Google)
    location_name = Column(
        String(255),
        nullable=False,
        doc="Business name from Google"
    )
    
    primary_phone = Column(
        String(50),
        nullable=True,
        doc="Primary phone number"
    )
    
    primary_category = Column(
        String(255),
        nullable=True,
        doc="Primary Google business category"
    )
    
    # Address information
    address_lines = Column(
        JSONB,
        nullable=True,
        doc="Address lines array"
    )
    
    locality = Column(
        String(100),
        nullable=True,
        doc="City/locality"
    )
    
    administrative_area = Column(
        String(100),
        nullable=True,
        doc="State/province"
    )
    
    postal_code = Column(
        String(20),
        nullable=True,
        doc="Postal code"
    )
    
    country = Column(
        String(10),
        nullable=True,
        doc="Country code"
    )
    
    # Location metadata
    location_state = Column(
        String(50),
        nullable=True,
        doc="Google location state (e.g., VERIFIED, UNVERIFIED)"
    )
    
    store_code = Column(
        String(100),
        nullable=True,
        doc="Store code from Google"
    )
    
    website_url = Column(
        String(500),
        nullable=True,
        doc="Website URL"
    )
    
    # Business hours (Google format)
    regular_hours = Column(
        JSONB,
        nullable=True,
        doc="Regular business hours from Google"
    )
    
    special_hours = Column(
        JSONB,
        nullable=True,
        doc="Special hours (holidays, etc.)"
    )
    
    # Reviews and ratings
    google_rating = Column(
        String(10),
        nullable=True,
        doc="Average Google rating"
    )
    
    google_review_count = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of Google reviews"
    )
    
    # Location photos
    profile_photo_url = Column(
        String(500),
        nullable=True,
        doc="Profile photo URL from Google"
    )
    
    cover_photo_url = Column(
        String(500),
        nullable=True,
        doc="Cover photo URL from Google"
    )
    
    # Additional metadata from Google
    google_metadata = Column(
        JSONB,
        nullable=True,
        doc="Additional Google location data"
    )
    
    # Sync tracking
    last_synced_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="Last sync from Google API"
    )
    
    sync_version = Column(
        BigInteger,
        default=0,
        nullable=False,
        doc="Version counter for sync tracking"
    )
    
    def __repr__(self):
        return f"<GoogleBusinessLocation(name='{self.location_name}', google_id='{self.google_location_id}')>"
    
    @property
    def formatted_address(self) -> str:
        """Get formatted address string"""
        parts = []
        if self.address_lines:
            parts.extend(self.address_lines)
        if self.locality:
            parts.append(self.locality)
        if self.administrative_area:
            parts.append(self.administrative_area)
        if self.postal_code:
            parts.append(self.postal_code)
        return ", ".join(parts)


@register_model
class SyncMapping(BaseModel):
    """
    Mapping between Google locations and local business listings
    """
    __tablename__ = "google_sync_mappings"
    
    # Mapping relationships
    business_id = Column(
        UUID(as_uuid=True),
        ForeignKey('business_listings.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        doc="Local business listing ID"
    )
    
    google_location_id = Column(
        UUID(as_uuid=True),
        ForeignKey('google_business_locations.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        doc="Google business location ID"
    )
    
    business = relationship("BusinessListing", backref="google_mappings")
    google_location = relationship("GoogleBusinessLocation", backref="sync_mappings")
    
    # Sync configuration
    sync_enabled = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Whether sync is enabled for this mapping"
    )
    
    auto_sync_direction = Column(
        String(20),
        default="bidirectional",
        nullable=False,
        doc="Sync direction: bidirectional, to_google, from_google"
    )
    
    conflict_resolution = Column(
        String(20),
        default=ConflictResolutionStrategy.GOOGLE_PRIORITY.value,
        nullable=False,
        doc="How to resolve data conflicts"
    )
    
    # Field-specific sync settings
    sync_fields = Column(
        JSONB,
        nullable=True,
        doc="Per-field sync configuration"
    )
    
    # Mapping metadata
    mapped_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        doc="When mapping was created"
    )
    
    mapped_by = Column(
        UUID(as_uuid=True),
        nullable=True,
        doc="User who created the mapping"
    )
    
    last_sync_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="Last successful sync"
    )
    
    sync_count = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of successful syncs"
    )
    
    def __repr__(self):
        return f"<SyncMapping(business_id='{self.business_id}', google_location_id='{self.google_location_id}')>"
    
    @property
    def is_bidirectional(self) -> bool:
        """Check if sync is bidirectional"""
        return self.auto_sync_direction == "bidirectional"


@register_model
class SyncLog(BaseModel):
    """
    Audit log for all synchronization operations
    """
    __tablename__ = "google_sync_logs"
    
    # Sync identification
    sync_mapping_id = Column(
        UUID(as_uuid=True),
        ForeignKey('google_sync_mappings.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        doc="Associated sync mapping (if applicable)"
    )
    
    sync_mapping = relationship("SyncMapping", backref="sync_logs")
    
    operation_type = Column(
        String(50),
        nullable=False,
        index=True,
        doc="Type of sync operation"
    )
    
    direction = Column(
        String(20),
        nullable=False,
        doc="Sync direction: to_google, from_google"
    )
    
    # Operation details
    status = Column(
        String(20),
        nullable=False,
        default=SyncStatus.PENDING.value,
        index=True,
        doc="Sync operation status"
    )
    
    started_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        doc="When sync operation started"
    )
    
    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="When sync operation completed"
    )
    
    # Data tracking
    fields_synced = Column(
        JSONB,
        nullable=True,
        doc="List of fields that were synced"
    )
    
    changes_detected = Column(
        JSONB,
        nullable=True,
        doc="Changes that were detected and synced"
    )
    
    conflicts_found = Column(
        JSONB,
        nullable=True,
        doc="Data conflicts that were found"
    )
    
    # Results and errors
    error_message = Column(
        Text,
        nullable=True,
        doc="Error message if sync failed"
    )
    
    error_details = Column(
        JSONB,
        nullable=True,
        doc="Detailed error information"
    )
    
    records_processed = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of records processed"
    )
    
    records_updated = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of records updated"
    )
    
    # Performance metrics
    duration_seconds = Column(
        Integer,
        nullable=True,
        doc="Operation duration in seconds"
    )
    
    api_calls_made = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of Google API calls made"
    )
    
    def __repr__(self):
        return f"<SyncLog(operation='{self.operation_type}', status='{self.status}')>"
    
    def complete_success(self):
        """Mark sync operation as successful"""
        self.status = SyncStatus.COMPLETED.value
        self.completed_at = datetime.utcnow()
        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())
    
    def complete_failure(self, error: str, details: Dict[str, Any] = None):
        """Mark sync operation as failed"""
        self.status = SyncStatus.FAILED.value
        self.completed_at = datetime.utcnow()
        self.error_message = error
        if details:
            self.error_details = details
        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())


@register_model
class SyncConflict(BaseModel):
    """
    Data conflicts between Google and local data that require resolution
    """
    __tablename__ = "google_sync_conflicts"
    
    # Conflict identification
    sync_mapping_id = Column(
        UUID(as_uuid=True),
        ForeignKey('google_sync_mappings.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        doc="Associated sync mapping"
    )
    
    sync_mapping = relationship("SyncMapping", backref="conflicts")
    
    field_name = Column(
        String(100),
        nullable=False,
        index=True,
        doc="Name of the conflicting field"
    )
    
    # Conflict data
    local_value = Column(
        JSONB,
        nullable=True,
        doc="Value in local system"
    )
    
    google_value = Column(
        JSONB,
        nullable=True,
        doc="Value in Google system"
    )
    
    # Conflict metadata
    detected_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        doc="When conflict was detected"
    )
    
    resolved_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="When conflict was resolved"
    )
    
    resolution_strategy = Column(
        String(20),
        nullable=True,
        doc="How conflict was resolved"
    )
    
    resolved_value = Column(
        JSONB,
        nullable=True,
        doc="Final resolved value"
    )
    
    resolved_by = Column(
        UUID(as_uuid=True),
        nullable=True,
        doc="User who resolved the conflict"
    )
    
    # Conflict status
    is_resolved = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Whether conflict has been resolved"
    )
    
    requires_manual_review = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Whether conflict requires manual review"
    )
    
    notes = Column(
        Text,
        nullable=True,
        doc="Resolution notes"
    )
    
    def __repr__(self):
        return f"<SyncConflict(field='{self.field_name}', resolved={self.is_resolved})>"
    
    def resolve(self, strategy: str, value: Any, user_id: str = None, notes: str = None):
        """Resolve the conflict"""
        self.is_resolved = True
        self.resolved_at = datetime.utcnow()
        self.resolution_strategy = strategy
        self.resolved_value = value
        if user_id:
            self.resolved_by = uuid.UUID(user_id)
        if notes:
            self.notes = notes


@register_model
class GoogleCacheEntry(BaseModel):
    """
    Cache for Google API responses to reduce API calls
    """
    __tablename__ = "google_cache"
    
    # Cache key identification
    cache_key = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique cache key"
    )
    
    endpoint = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Google API endpoint"
    )
    
    # Cache data
    response_data = Column(
        JSONB,
        nullable=False,
        doc="Cached API response data"
    )
    
    # Cache metadata
    expires_at = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        doc="Cache expiration time"
    )
    
    request_params = Column(
        JSONB,
        nullable=True,
        doc="Original request parameters"
    )
    
    response_code = Column(
        Integer,
        default=200,
        nullable=False,
        doc="HTTP response code"
    )
    
    def __repr__(self):
        return f"<GoogleCacheEntry(key='{self.cache_key}', expires='{self.expires_at}')>"
    
    @property
    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        return datetime.utcnow() > self.expires_at


# Create composite indexes for performance
Index('ix_google_accounts_tenant_status', GoogleAccount.tenant_id, GoogleAccount.status)
Index('ix_google_locations_account_sync', GoogleBusinessLocation.google_account_id, GoogleBusinessLocation.last_synced_at)
Index('ix_sync_mappings_business_enabled', SyncMapping.business_id, SyncMapping.sync_enabled)
Index('ix_sync_logs_mapping_status', SyncLog.sync_mapping_id, SyncLog.status)
Index('ix_sync_conflicts_mapping_resolved', SyncConflict.sync_mapping_id, SyncConflict.is_resolved)
Index('ix_google_cache_endpoint_expires', GoogleCacheEntry.endpoint, GoogleCacheEntry.expires_at)