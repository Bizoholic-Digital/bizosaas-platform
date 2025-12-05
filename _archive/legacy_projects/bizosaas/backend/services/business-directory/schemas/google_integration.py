"""
Google Business Profile Integration Schemas
Pydantic schemas for Google Business Profile API integration
"""

from pydantic import BaseModel, Field, validator, HttpUrl
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from uuid import UUID
from enum import Enum

from .common import BaseResponseSchema, TimestampSchema, LocationSchema, ContactSchema


class GoogleAccountStatus(str, Enum):
    """Google account connection status"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    EXPIRED = "expired"
    ERROR = "error"
    REVOKED = "revoked"


class SyncStatus(str, Enum):
    """Synchronization status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ConflictResolutionStrategy(str, Enum):
    """Conflict resolution strategy"""
    GOOGLE_PRIORITY = "google_priority"
    LOCAL_PRIORITY = "local_priority"
    MANUAL = "manual"
    MERGE = "merge"


# Request Schemas
class GoogleAuthUrlSchema(BaseModel):
    """Schema for Google authorization URL request"""
    state: Optional[str] = Field(None, description="Optional state parameter for CSRF protection")
    redirect_uri: Optional[HttpUrl] = Field(None, description="Custom redirect URI")


class GoogleCallbackSchema(BaseModel):
    """Schema for Google OAuth callback"""
    code: str = Field(description="Authorization code from Google")
    state: str = Field(description="State parameter for CSRF protection")
    error: Optional[str] = Field(None, description="Error parameter if OAuth failed")


class LocationSyncSchema(BaseModel):
    """Schema for location synchronization request"""
    location_ids: Optional[List[str]] = Field(None, description="Specific location IDs to sync")
    force_refresh: bool = Field(False, description="Force refresh from Google API")
    conflict_resolution: ConflictResolutionStrategy = Field(
        ConflictResolutionStrategy.GOOGLE_PRIORITY,
        description="How to resolve conflicts"
    )


class BulkLocationSyncSchema(BaseModel):
    """Schema for bulk location sync operation"""
    account_ids: Optional[List[UUID]] = Field(None, description="Specific account IDs to sync")
    location_ids: Optional[List[str]] = Field(None, description="Specific location IDs to sync")
    sync_reviews: bool = Field(True, description="Include review synchronization")
    sync_photos: bool = Field(True, description="Include photo synchronization")
    conflict_resolution: ConflictResolutionStrategy = Field(
        ConflictResolutionStrategy.GOOGLE_PRIORITY,
        description="How to resolve conflicts"
    )


class LocationManagementSchema(BaseModel):
    """Schema for location management operations"""
    name: Optional[str] = Field(None, max_length=255, description="Business name")
    description: Optional[str] = Field(None, max_length=1000, description="Business description")
    phone_number: Optional[str] = Field(None, description="Primary phone number")
    website_uri: Optional[HttpUrl] = Field(None, description="Business website")
    categories: Optional[List[str]] = Field(None, description="Business categories")
    location: Optional[LocationSchema] = Field(None, description="Location information")
    hours: Optional[Dict[str, Dict[str, str]]] = Field(None, description="Business hours")


class ConflictResolutionSchema(BaseModel):
    """Schema for conflict resolution"""
    conflict_id: UUID = Field(description="Conflict ID")
    resolution: ConflictResolutionStrategy = Field(description="Resolution strategy")
    manual_values: Optional[Dict[str, Any]] = Field(None, description="Manual resolution values")


# Response Schemas
class GoogleAuthUrlResponseSchema(BaseModel):
    """Schema for Google authorization URL response"""
    authorization_url: HttpUrl = Field(description="Google OAuth authorization URL")
    state: str = Field(description="State parameter for security")
    scopes: List[str] = Field(description="Requested OAuth scopes")


class GoogleAccountResponseSchema(BaseResponseSchema):
    """Schema for Google account response"""
    google_account_id: str = Field(description="Google account ID")
    email: str = Field(description="Google account email")
    display_name: Optional[str] = Field(None, description="Account display name")
    status: GoogleAccountStatus = Field(description="Account connection status")
    connected_at: datetime = Field(description="Connection timestamp")
    last_sync_at: Optional[datetime] = Field(None, description="Last synchronization timestamp")
    is_token_expired: bool = Field(description="Whether access token is expired")
    error_count: int = Field(default=0, description="Error count")
    last_error: Optional[str] = Field(None, description="Last error message")
    granted_scopes: List[str] = Field(default_factory=list, description="OAuth granted scopes")
    location_count: int = Field(default=0, description="Number of associated locations")


class GoogleLocationResponseSchema(BaseModel):
    """Schema for Google Business Location response"""
    google_location_id: str = Field(description="Google location ID")
    account_id: UUID = Field(description="Associated Google account ID")
    name: str = Field(description="Business name")
    description: Optional[str] = Field(None, description="Business description")
    phone_number: Optional[str] = Field(None, description="Phone number")
    website_uri: Optional[str] = Field(None, description="Website URL")
    categories: List[str] = Field(default_factory=list, description="Business categories")
    location: Optional[Dict[str, Any]] = Field(None, description="Location data")
    hours: Optional[Dict[str, Any]] = Field(None, description="Business hours")
    photos: List[str] = Field(default_factory=list, description="Photo URLs")
    reviews_summary: Optional[Dict[str, Any]] = Field(None, description="Reviews summary")
    sync_status: SyncStatus = Field(description="Synchronization status")
    last_sync_at: Optional[datetime] = Field(None, description="Last sync timestamp")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Update timestamp")


class SyncOperationResponseSchema(BaseModel):
    """Schema for sync operation response"""
    operation_id: UUID = Field(description="Sync operation ID")
    status: SyncStatus = Field(description="Operation status")
    started_at: datetime = Field(description="Operation start time")
    completed_at: Optional[datetime] = Field(None, description="Operation completion time")
    total_locations: int = Field(description="Total locations to sync")
    processed_locations: int = Field(description="Locations processed")
    successful_syncs: int = Field(description="Successful synchronizations")
    failed_syncs: int = Field(description="Failed synchronizations")
    conflicts_detected: int = Field(description="Number of conflicts detected")
    error_details: Optional[List[str]] = Field(None, description="Error details")


class LocationConflictResponseSchema(BaseModel):
    """Schema for location conflict response"""
    conflict_id: UUID = Field(description="Conflict ID")
    location_id: str = Field(description="Google location ID")
    field_name: str = Field(description="Conflicting field name")
    google_value: Any = Field(description="Value from Google")
    local_value: Any = Field(description="Local database value")
    last_modified_google: Optional[datetime] = Field(None, description="Last modified on Google")
    last_modified_local: Optional[datetime] = Field(None, description="Last modified locally")
    resolution_status: str = Field(default="pending", description="Resolution status")
    created_at: datetime = Field(description="Conflict detected timestamp")


class SyncStatsResponseSchema(BaseModel):
    """Schema for synchronization statistics"""
    total_accounts: int = Field(description="Total connected accounts")
    active_accounts: int = Field(description="Active accounts")
    expired_accounts: int = Field(description="Expired accounts")
    total_locations: int = Field(description="Total synchronized locations")
    locations_synced_today: int = Field(description="Locations synced today")
    pending_syncs: int = Field(description="Pending sync operations")
    sync_errors: int = Field(description="Sync errors in last 24h")
    last_full_sync: Optional[datetime] = Field(None, description="Last full sync timestamp")
    average_sync_time: Optional[float] = Field(None, description="Average sync time in seconds")


class GoogleBusinessInsightsSchema(BaseModel):
    """Schema for Google Business Profile insights"""
    location_id: str = Field(description="Google location ID")
    views: Optional[int] = Field(None, description="Profile views")
    searches: Optional[int] = Field(None, description="Search queries")
    actions: Optional[Dict[str, int]] = Field(None, description="Customer actions")
    photos: Optional[Dict[str, int]] = Field(None, description="Photo metrics")
    period_start: datetime = Field(description="Metrics period start")
    period_end: datetime = Field(description="Metrics period end")
    retrieved_at: datetime = Field(description="Data retrieval timestamp")


class BatchOperationResponseSchema(BaseModel):
    """Schema for batch operation response"""
    batch_id: UUID = Field(description="Batch operation ID")
    operation_type: str = Field(description="Type of batch operation")
    total_items: int = Field(description="Total items in batch")
    processed_items: int = Field(description="Items processed")
    successful_items: int = Field(description="Successfully processed items")
    failed_items: int = Field(description="Failed items")
    status: str = Field(description="Batch operation status")
    started_at: datetime = Field(description="Batch start time")
    completed_at: Optional[datetime] = Field(None, description="Batch completion time")
    errors: List[str] = Field(default_factory=list, description="Error messages")


class GoogleIntegrationHealthSchema(BaseModel):
    """Schema for Google integration health status"""
    status: str = Field(description="Overall integration health")
    api_connection: str = Field(description="Google API connection status")
    authentication: str = Field(description="OAuth authentication status")
    rate_limits: Dict[str, Any] = Field(description="Rate limit status")
    sync_performance: Dict[str, Any] = Field(description="Sync performance metrics")
    error_rates: Dict[str, float] = Field(description="Error rates by operation")
    last_check: datetime = Field(description="Last health check timestamp")