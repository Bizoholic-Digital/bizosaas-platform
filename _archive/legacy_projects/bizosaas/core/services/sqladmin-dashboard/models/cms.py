"""
CMS Data Models for SQLAdmin Dashboard
Handles pages, media, forms, collections, menus, and content management
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, UUID, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class PageStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    SCHEDULED = "scheduled"
    ARCHIVED = "archived"

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    OTHER = "other"

class FormStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

# CMS Pages
class PageAdmin(Base):
    __tablename__ = "cms_pages"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Page details
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    content = Column(Text)
    excerpt = Column(Text)
    
    # Page hierarchy
    parent_id = Column(UUID(as_uuid=True), ForeignKey("cms_pages.id"))
    sort_order = Column(Integer, default=0)
    depth = Column(Integer, default=0)
    
    # SEO and metadata
    meta_title = Column(String(255))
    meta_description = Column(Text)
    meta_keywords = Column(String(500))
    og_title = Column(String(255))
    og_description = Column(Text)
    og_image = Column(String(500))
    canonical_url = Column(String(500))
    
    # Content structure
    template = Column(String(100))  # Template file to use
    content_blocks = Column(JSON, default=[])  # Structured content blocks
    custom_fields = Column(JSON, default={})
    
    # Media
    featured_image = Column(String(500))
    gallery_images = Column(JSON, default=[])
    
    # Publication
    status = Column(Enum(PageStatus), default=PageStatus.DRAFT)
    published_at = Column(DateTime(timezone=True))
    scheduled_at = Column(DateTime(timezone=True))
    
    # Visibility and access
    is_visible_in_menu = Column(Boolean, default=True)
    is_searchable = Column(Boolean, default=True)
    requires_authentication = Column(Boolean, default=False)
    allowed_roles = Column(JSON, default=[])
    
    # Performance and analytics
    view_count = Column(Integer, default=0)
    last_viewed_at = Column(DateTime(timezone=True))
    search_keywords = Column(JSON, default=[])
    
    # Version control
    version = Column(Integer, default=1)
    revision_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    children = relationship("PageAdmin", remote_side=[id])
    page_versions = relationship("PageVersionAdmin", back_populates="page", cascade="all, delete-orphan")

# Page Version History
class PageVersionAdmin(Base):
    __tablename__ = "cms_page_versions"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    page_id = Column(UUID(as_uuid=True), ForeignKey("cms_pages.id"), nullable=False)
    
    # Version details
    version_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    content_blocks = Column(JSON, default=[])
    custom_fields = Column(JSON, default={})
    
    # Version metadata
    change_summary = Column(String(500))
    revision_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    page = relationship("PageAdmin", back_populates="page_versions")

# Media Library
class MediaAdmin(Base):
    __tablename__ = "cms_media"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # File details
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    url = Column(String(500), nullable=False)
    
    # File metadata
    file_size = Column(Integer)  # Size in bytes
    mime_type = Column(String(100))
    media_type = Column(Enum(MediaType))
    file_extension = Column(String(10))
    
    # Image-specific metadata
    width = Column(Integer)
    height = Column(Integer)
    alt_text = Column(String(255))
    caption = Column(Text)
    
    # Video/Audio-specific metadata
    duration = Column(Float)  # Duration in seconds
    
    # Organization
    folder = Column(String(255), default="/")
    tags = Column(JSON, default=[])
    categories = Column(JSON, default=[])
    
    # SEO
    title = Column(String(255))
    description = Column(Text)
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True))
    
    # CDN and optimization
    cdn_url = Column(String(500))
    thumbnails = Column(JSON, default={})  # Different sizes
    is_optimized = Column(Boolean, default=False)
    
    # Storage details
    storage_provider = Column(String(50), default="local")
    storage_bucket = Column(String(100))
    storage_key = Column(String(500))
    
    # Status
    is_public = Column(Boolean, default=True)
    is_archived = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Custom metadata
    metadata = Column(JSON, default={})

# Forms and Lead Capture
class FormAdmin(Base):
    __tablename__ = "cms_forms"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Form details
    name = Column(String(255), nullable=False)
    title = Column(String(255))
    description = Column(Text)
    
    # Form configuration
    fields = Column(JSON, nullable=False)  # Form field definitions
    validation_rules = Column(JSON, default={})
    success_message = Column(Text)
    error_message = Column(Text)
    
    # Behavior settings
    allow_multiple_submissions = Column(Boolean, default=True)
    requires_authentication = Column(Boolean, default=False)
    store_submissions = Column(Boolean, default=True)
    
    # Email notifications
    notification_emails = Column(JSON, default=[])
    email_template_id = Column(UUID(as_uuid=True))
    auto_responder_enabled = Column(Boolean, default=False)
    auto_responder_template_id = Column(UUID(as_uuid=True))
    
    # Integrations
    webhook_url = Column(String(500))
    integration_settings = Column(JSON, default={})
    
    # Analytics
    submission_count = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)
    
    # Status and visibility
    status = Column(Enum(FormStatus), default=FormStatus.ACTIVE)
    is_public = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    submissions = relationship("FormSubmissionAdmin", back_populates="form", cascade="all, delete-orphan")

# Form Submissions
class FormSubmissionAdmin(Base):
    __tablename__ = "cms_form_submissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    form_id = Column(UUID(as_uuid=True), ForeignKey("cms_forms.id"), nullable=False)
    
    # Submission data
    data = Column(JSON, nullable=False)  # Form field values
    
    # Submitter information
    submitter_email = Column(String(255))
    submitter_name = Column(String(255))
    submitter_ip = Column(String(45))
    user_agent = Column(Text)
    
    # Tracking
    referrer = Column(String(500))
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    
    # Processing
    is_processed = Column(Boolean, default=False)
    processed_at = Column(DateTime(timezone=True))
    processed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Status
    is_spam = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    form = relationship("FormAdmin", back_populates="submissions")

# Content Collections (like blogs, portfolios, etc.)
class CollectionAdmin(Base):
    __tablename__ = "cms_collections"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Collection details
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    
    # Collection type
    collection_type = Column(String(50), default="articles")  # articles, portfolios, products, etc.
    
    # Display settings
    items_per_page = Column(Integer, default=10)
    sort_order = Column(String(50), default="created_at_desc")
    enable_comments = Column(Boolean, default=False)
    enable_ratings = Column(Boolean, default=False)
    
    # SEO
    meta_title = Column(String(255))
    meta_description = Column(Text)
    
    # Template and layout
    template = Column(String(100))
    layout_config = Column(JSON, default={})
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    items = relationship("CollectionItemAdmin", back_populates="collection", cascade="all, delete-orphan")

# Collection Items
class CollectionItemAdmin(Base):
    __tablename__ = "cms_collection_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    collection_id = Column(UUID(as_uuid=True), ForeignKey("cms_collections.id"), nullable=False)
    
    # Item details
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    content = Column(Text)
    excerpt = Column(Text)
    
    # Media
    featured_image = Column(String(500))
    gallery_images = Column(JSON, default=[])
    
    # Classification
    categories = Column(JSON, default=[])
    tags = Column(JSON, default=[])
    
    # SEO
    meta_title = Column(String(255))
    meta_description = Column(Text)
    
    # Publication
    status = Column(Enum(PageStatus), default=PageStatus.DRAFT)
    published_at = Column(DateTime(timezone=True))
    
    # Sorting and display
    sort_order = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    
    # Interaction
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    
    # Custom fields
    custom_fields = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    collection = relationship("CollectionAdmin", back_populates="items")

# Navigation Menus
class MenuAdmin(Base):
    __tablename__ = "cms_menus"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Menu details
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    
    # Menu configuration
    location = Column(String(50))  # header, footer, sidebar, etc.
    max_depth = Column(Integer, default=3)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    items = relationship("MenuItemAdmin", back_populates="menu", cascade="all, delete-orphan")

# Menu Items
class MenuItemAdmin(Base):
    __tablename__ = "cms_menu_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("cms_menus.id"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("cms_menu_items.id"))
    
    # Item details
    title = Column(String(255), nullable=False)
    url = Column(String(500))
    
    # Link types
    link_type = Column(String(50), default="custom")  # page, custom, collection, external
    page_id = Column(UUID(as_uuid=True), ForeignKey("cms_pages.id"))
    collection_id = Column(UUID(as_uuid=True), ForeignKey("cms_collections.id"))
    
    # Display settings
    css_class = Column(String(100))
    icon = Column(String(100))
    description = Column(String(255))
    
    # Behavior
    target = Column(String(20), default="_self")  # _self, _blank
    is_active = Column(Boolean, default=True)
    requires_authentication = Column(Boolean, default=False)
    allowed_roles = Column(JSON, default=[])
    
    # Hierarchy
    sort_order = Column(Integer, default=0)
    depth = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    menu = relationship("MenuAdmin", back_populates="items")
    children = relationship("MenuItemAdmin", remote_side=[id])

# Email Templates
class EmailTemplateAdmin(Base):
    __tablename__ = "cms_email_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Template details
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    
    # Email content
    subject = Column(String(255), nullable=False)
    html_content = Column(Text)
    text_content = Column(Text)
    
    # Template settings
    from_email = Column(String(255))
    from_name = Column(String(255))
    reply_to = Column(String(255))
    
    # Template variables
    variables = Column(JSON, default=[])  # Available template variables
    sample_data = Column(JSON, default={})  # Sample data for preview
    
    # Categories and tags
    category = Column(String(100))
    tags = Column(JSON, default=[])
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True))
    
    # Status
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# Widgets for dynamic content
class WidgetAdmin(Base):
    __tablename__ = "cms_widgets"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Widget details
    name = Column(String(255), nullable=False)
    widget_type = Column(String(100), nullable=False)  # text, image, form, carousel, etc.
    title = Column(String(255))
    content = Column(Text)
    
    # Configuration
    settings = Column(JSON, default={})
    data_source = Column(JSON, default={})  # Where to get dynamic data
    
    # Placement
    placement_zones = Column(JSON, default=[])  # Where widget can be placed
    
    # Display conditions
    display_conditions = Column(JSON, default={})
    device_targeting = Column(JSON, default=[])  # mobile, tablet, desktop
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))