"""
Business Directory Platform Settings Models
Additional models for platform-level configuration and settings management
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid
import enum

# Import the base models from Business Directory
import sys
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas-platform/backend/services/business-directory')
from models.base import BaseModel, register_model


# Enums for platform settings
class ModerationMode(str, enum.Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic" 
    AI_POWERED = "ai_powered"


class IntegrationStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    ERROR = "error"


class NotificationEvent(str, enum.Enum):
    NEW_BUSINESS = "new_business"
    NEW_REVIEW = "new_review"
    CLAIM_REQUEST = "claim_request"
    REPORT_SPAM = "report_spam"
    INTEGRATION_ERROR = "integration_error"


@register_model
class DirectoryPlatformSettings(BaseModel):
    """
    Platform-wide settings for Business Directory
    """
    __tablename__ = "directory_platform_settings"
    
    # Auto-approval settings
    auto_approval_enabled = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Enable automatic approval of listings"
    )
    
    auto_approval_threshold = Column(
        String(5),
        default="4.0",
        nullable=False,
        doc="Minimum rating for auto-approval"
    )
    
    # Review moderation
    review_moderation_mode = Column(
        SQLEnum(ModerationMode),
        default=ModerationMode.MANUAL,
        nullable=False,
        doc="Review moderation mode"
    )
    
    spam_detection_enabled = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Enable AI spam detection"
    )
    
    # Listing limits
    featured_listing_limit = Column(
        Integer,
        default=10,
        nullable=False,
        doc="Maximum number of featured listings"
    )
    
    free_listing_limit_per_user = Column(
        Integer,
        default=1,
        nullable=False,
        doc="Free listings per user"
    )
    
    # Search and display
    search_results_per_page = Column(
        Integer,
        default=20,
        nullable=False,
        doc="Search results per page"
    )
    
    enable_radius_search = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Enable location-based radius search"
    )
    
    default_search_radius_km = Column(
        Integer,
        default=25,
        nullable=False,
        doc="Default search radius in kilometers"
    )
    
    # Image and media settings
    max_images_per_listing = Column(
        Integer,
        default=10,
        nullable=False,
        doc="Maximum images per business listing"
    )
    
    max_image_size_mb = Column(
        Integer,
        default=5,
        nullable=False,
        doc="Maximum image size in MB"
    )
    
    allowed_image_types = Column(
        JSONB,
        default=lambda: ["jpg", "jpeg", "png", "webp"],
        nullable=False,
        doc="Allowed image file types"
    )
    
    # SEO and content
    meta_title_template = Column(
        Text,
        default="{business_name} - {category} in {city} | Business Directory",
        nullable=True,
        doc="Meta title template for SEO"
    )
    
    meta_description_template = Column(
        Text,
        default="Find {business_name} in {city}. {description}",
        nullable=True,
        doc="Meta description template for SEO"
    )
    
    # API rate limiting
    api_rate_limit_per_hour = Column(
        Integer,
        default=1000,
        nullable=False,
        doc="API requests per hour per user"
    )
    
    # Additional settings
    additional_settings = Column(
        JSONB,
        default=dict,
        nullable=True,
        doc="Additional platform settings in JSON format"
    )
    
    def __repr__(self):
        return f"<DirectoryPlatformSettings(id='{self.id}')>"


@register_model
class DirectoryIntegrationConfig(BaseModel):
    """
    External service integration configurations
    """
    __tablename__ = "directory_integration_configs"
    
    # Integration details
    service_name = Column(
        String(100),
        nullable=False,
        index=True,
        doc="External service name (google, yelp, facebook, etc.)"
    )
    
    service_display_name = Column(
        String(255),
        nullable=False,
        doc="Human-readable service name"
    )
    
    status = Column(
        SQLEnum(IntegrationStatus),
        default=IntegrationStatus.INACTIVE,
        nullable=False,
        index=True,
        doc="Integration status"
    )
    
    # API configuration
    api_endpoint = Column(
        String(500),
        nullable=True,
        doc="Base API endpoint URL"
    )
    
    api_key = Column(
        Text,
        nullable=True,
        doc="Encrypted API key"
    )
    
    api_secret = Column(
        Text,
        nullable=True,
        doc="Encrypted API secret"
    )
    
    # Sync settings
    auto_sync_enabled = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Enable automatic synchronization"
    )
    
    sync_interval_hours = Column(
        Integer,
        default=24,
        nullable=False,
        doc="Sync interval in hours"
    )
    
    last_sync_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="Last successful sync timestamp"
    )
    
    last_sync_status = Column(
        String(50),
        default="never",
        nullable=False,
        doc="Last sync status"
    )
    
    # Sync statistics
    total_syncs = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Total number of syncs performed"
    )
    
    successful_syncs = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of successful syncs"
    )
    
    failed_syncs = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of failed syncs"
    )
    
    # Configuration options
    sync_options = Column(
        JSONB,
        default=dict,
        nullable=True,
        doc="Integration-specific sync options"
    )
    
    # Rate limiting
    rate_limit_per_hour = Column(
        Integer,
        default=1000,
        nullable=True,
        doc="API rate limit per hour"
    )
    
    # Error handling
    error_log = Column(
        JSONB,
        default=list,
        nullable=True,
        doc="Recent error logs"
    )
    
    def __repr__(self):
        return f"<DirectoryIntegrationConfig(service='{self.service_name}', status='{self.status}')>"
    
    def add_error_log(self, error_message: str, error_details: Dict = None):
        """Add error to the error log"""
        if not self.error_log:
            self.error_log = []
        
        error_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": error_message,
            "details": error_details or {}
        }
        
        # Keep only last 50 errors
        self.error_log = ([error_entry] + self.error_log)[:50]
    
    def update_sync_stats(self, success: bool):
        """Update sync statistics"""
        self.total_syncs += 1
        if success:
            self.successful_syncs += 1
            self.last_sync_at = datetime.utcnow()
            self.last_sync_status = "success"
        else:
            self.failed_syncs += 1
            self.last_sync_status = "failed"


@register_model
class DirectoryNotificationSettings(BaseModel):
    """
    Notification settings for platform events
    """
    __tablename__ = "directory_notification_settings"
    
    # Notification details
    event_type = Column(
        SQLEnum(NotificationEvent),
        nullable=False,
        index=True,
        doc="Type of event to notify about"
    )
    
    is_enabled = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Whether notifications are enabled for this event"
    )
    
    # Email notifications
    email_enabled = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Send email notifications"
    )
    
    email_template = Column(
        Text,
        nullable=True,
        doc="Custom email template for this notification type"
    )
    
    email_recipients = Column(
        JSONB,
        default=list,
        nullable=True,
        doc="List of email addresses to notify"
    )
    
    # Webhook notifications
    webhook_enabled = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Send webhook notifications"
    )
    
    webhook_url = Column(
        String(500),
        nullable=True,
        doc="Webhook endpoint URL"
    )
    
    webhook_headers = Column(
        JSONB,
        default=dict,
        nullable=True,
        doc="Custom headers for webhook requests"
    )
    
    # Slack notifications
    slack_enabled = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Send Slack notifications"
    )
    
    slack_webhook_url = Column(
        String(500),
        nullable=True,
        doc="Slack webhook URL"
    )
    
    slack_channel = Column(
        String(100),
        nullable=True,
        doc="Slack channel name"
    )
    
    # Additional settings
    notification_settings = Column(
        JSONB,
        default=dict,
        nullable=True,
        doc="Additional notification settings"
    )
    
    def __repr__(self):
        return f"<DirectoryNotificationSettings(event='{self.event_type}', enabled={self.is_enabled})>"


@register_model
class DirectoryModerationQueue(BaseModel):
    """
    Moderation queue for pending approvals
    """
    __tablename__ = "directory_moderation_queue"
    
    # Item details
    item_type = Column(
        String(50),
        nullable=False,
        index=True,
        doc="Type of item (business, review, event, etc.)"
    )
    
    item_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        doc="ID of the item being moderated"
    )
    
    # Moderation details
    priority = Column(
        String(20),
        default="normal",
        nullable=False,
        index=True,
        doc="Moderation priority (low, normal, high, urgent)"
    )
    
    status = Column(
        String(20),
        default="pending",
        nullable=False,
        index=True,
        doc="Moderation status (pending, approved, rejected, escalated)"
    )
    
    assigned_to = Column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
        doc="ID of moderator assigned to this item"
    )
    
    # Moderation notes
    submission_notes = Column(
        Text,
        nullable=True,
        doc="Notes from the submitter"
    )
    
    moderation_notes = Column(
        Text,
        nullable=True,
        doc="Internal moderation notes"
    )
    
    rejection_reason = Column(
        Text,
        nullable=True,
        doc="Reason for rejection if applicable"
    )
    
    # AI analysis
    ai_score = Column(
        String(5),
        nullable=True,
        doc="AI spam/quality score (0.0-1.0)"
    )
    
    ai_flags = Column(
        JSONB,
        default=list,
        nullable=True,
        doc="AI-detected flags or issues"
    )
    
    # Timing
    submitted_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="When item was submitted for moderation"
    )
    
    reviewed_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="When item was reviewed by moderator"
    )
    
    sla_deadline = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="SLA deadline for moderation"
    )
    
    # Additional data
    item_data = Column(
        JSONB,
        nullable=True,
        doc="Snapshot of item data at submission time"
    )
    
    def __repr__(self):
        return f"<DirectoryModerationQueue(item_type='{self.item_type}', status='{self.status}')>"
    
    @property
    def is_overdue(self) -> bool:
        """Check if item is past SLA deadline"""
        if not self.sla_deadline:
            return False
        return datetime.utcnow() > self.sla_deadline
    
    def approve(self, moderator_id: str, notes: str = None):
        """Approve the moderated item"""
        self.status = "approved"
        self.assigned_to = uuid.UUID(moderator_id)
        self.reviewed_at = datetime.utcnow()
        if notes:
            self.moderation_notes = notes
    
    def reject(self, moderator_id: str, reason: str, notes: str = None):
        """Reject the moderated item"""
        self.status = "rejected"
        self.assigned_to = uuid.UUID(moderator_id)
        self.reviewed_at = datetime.utcnow()
        self.rejection_reason = reason
        if notes:
            self.moderation_notes = notes


@register_model
class DirectoryAnalyticsMetrics(BaseModel):
    """
    Platform-wide analytics metrics
    """
    __tablename__ = "directory_analytics_metrics"
    
    # Metric details
    metric_name = Column(
        String(100),
        nullable=False,
        index=True,
        doc="Name of the metric"
    )
    
    metric_category = Column(
        String(50),
        nullable=False,
        index=True,
        doc="Category of metric (listings, reviews, users, etc.)"
    )
    
    # Time period
    date = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        doc="Date for this metric snapshot"
    )
    
    period_type = Column(
        String(20),
        nullable=False,
        doc="Period type (hourly, daily, weekly, monthly)"
    )
    
    # Metric values
    metric_value = Column(
        String(50),
        nullable=False,
        doc="Primary metric value"
    )
    
    previous_value = Column(
        String(50),
        nullable=True,
        doc="Previous period value for comparison"
    )
    
    change_percent = Column(
        String(10),
        nullable=True,
        doc="Percentage change from previous period"
    )
    
    # Additional data
    breakdown_data = Column(
        JSONB,
        nullable=True,
        doc="Detailed breakdown of the metric"
    )
    
    dimensions = Column(
        JSONB,
        nullable=True,
        doc="Metric dimensions (location, category, etc.)"
    )
    
    def __repr__(self):
        return f"<DirectoryAnalyticsMetrics(metric='{self.metric_name}', date='{self.date}')>"


@register_model
class DirectoryContentFilter(BaseModel):
    """
    Content filtering rules and spam detection
    """
    __tablename__ = "directory_content_filters"
    
    # Filter details
    filter_name = Column(
        String(100),
        nullable=False,
        doc="Name of the content filter"
    )
    
    filter_type = Column(
        String(50),
        nullable=False,
        index=True,
        doc="Type of filter (keyword, regex, ml_model, etc.)"
    )
    
    target_content = Column(
        String(50),
        nullable=False,
        index=True,
        doc="What content to filter (business_name, description, reviews, etc.)"
    )
    
    # Filter configuration
    filter_pattern = Column(
        Text,
        nullable=False,
        doc="Filter pattern or rule"
    )
    
    action = Column(
        String(30),
        nullable=False,
        doc="Action to take (block, flag, moderate, score)"
    )
    
    severity = Column(
        String(20),
        default="medium",
        nullable=False,
        doc="Severity level (low, medium, high, critical)"
    )
    
    # Status and configuration
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        doc="Whether filter is active"
    )
    
    is_case_sensitive = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Whether filter is case sensitive"
    )
    
    # Statistics
    match_count = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of times filter has matched"
    )
    
    false_positive_count = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of false positives reported"
    )
    
    last_match_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="When filter last matched content"
    )
    
    # Additional settings
    filter_config = Column(
        JSONB,
        default=dict,
        nullable=True,
        doc="Additional filter configuration"
    )
    
    def __repr__(self):
        return f"<DirectoryContentFilter(name='{self.filter_name}', type='{self.filter_type}')>"
    
    def increment_match_count(self):
        """Increment the match count"""
        self.match_count += 1
        self.last_match_at = datetime.utcnow()
    
    def report_false_positive(self):
        """Report a false positive"""
        self.false_positive_count += 1


# Export all models
__all__ = [
    'DirectoryPlatformSettings',
    'DirectoryIntegrationConfig', 
    'DirectoryNotificationSettings',
    'DirectoryModerationQueue',
    'DirectoryAnalyticsMetrics',
    'DirectoryContentFilter',
    'ModerationMode',
    'IntegrationStatus',
    'NotificationEvent'
]