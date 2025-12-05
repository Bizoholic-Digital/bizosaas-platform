"""
Business Directory Pydantic Schemas
Data validation and serialization schemas for business directory entities
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

from .common import (
    BaseResponseSchema,
    LocationSchema,
    ContactSchema,
    MediaSchema,
    RatingSchema,
    SEOSchema,
    BusinessHoursSchema,
    PaginationSchema,
    SortSchema,
    SearchSchema
)


# ============================================================================
# Business Category Schemas
# ============================================================================

class CategoryCreateSchema(BaseModel):
    """Schema for creating a new business category"""
    name: str = Field(min_length=1, max_length=255, description="Category name")
    description: Optional[str] = Field(None, max_length=500, description="Category description")
    parent_id: Optional[UUID] = Field(None, description="Parent category ID")
    sort_order: int = Field(default=0, ge=0, description="Sort order")
    icon: Optional[str] = Field(None, max_length=255, description="Category icon URL")
    color: Optional[str] = Field(None, regex="^#[0-9A-Fa-f]{6}$", description="Category color (hex)")
    keywords: Optional[str] = Field(None, max_length=500, description="SEO keywords")
    is_active: bool = Field(default=True, description="Category active status")


class CategoryUpdateSchema(BaseModel):
    """Schema for updating a business category"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Category name")
    description: Optional[str] = Field(None, max_length=500, description="Category description")
    parent_id: Optional[UUID] = Field(None, description="Parent category ID")
    sort_order: Optional[int] = Field(None, ge=0, description="Sort order")
    icon: Optional[str] = Field(None, max_length=255, description="Category icon URL")
    color: Optional[str] = Field(None, regex="^#[0-9A-Fa-f]{6}$", description="Category color (hex)")
    keywords: Optional[str] = Field(None, max_length=500, description="SEO keywords")
    is_active: Optional[bool] = Field(None, description="Category active status")


class CategoryResponseSchema(BaseResponseSchema, SEOSchema):
    """Schema for business category responses"""
    name: str
    description: Optional[str]
    parent_id: Optional[UUID]
    sort_order: int
    icon: Optional[str]
    color: Optional[str]
    keywords: Optional[str]
    is_active: bool
    business_count: int
    
    # Nested relationships
    parent: Optional['CategoryResponseSchema'] = None
    children: List['CategoryResponseSchema'] = []


# ============================================================================
# Business Listing Schemas
# ============================================================================

class BusinessCreateSchema(BaseModel, LocationSchema, ContactSchema, MediaSchema, SEOSchema):
    """Schema for creating a new business listing"""
    name: str = Field(min_length=1, max_length=255, description="Business name")
    description: Optional[str] = Field(None, description="Business description")
    short_description: Optional[str] = Field(None, max_length=500, description="Short description")
    category_id: Optional[UUID] = Field(None, description="Primary business category")
    
    # Business details
    business_hours: Optional[Dict[str, Dict[str, str]]] = Field(None, description="Business hours")
    social_media: Optional[Dict[str, str]] = Field(None, description="Social media links")
    amenities: Optional[List[str]] = Field(None, description="Business amenities")
    tags: Optional[List[str]] = Field(None, description="Business tags")
    price_range: Optional[str] = Field(None, regex="^\\$+$", description="Price range ($, $$, $$$, $$$$)")
    
    # Owner information
    owner_name: Optional[str] = Field(None, max_length=255, description="Business owner name")
    owner_email: Optional[str] = Field(None, description="Business owner email")
    
    @validator('tags', 'amenities', pre=True)
    def validate_string_lists(cls, v):
        """Convert string lists and validate"""
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v or []
    
    @validator('business_hours', 'social_media', pre=True)
    def validate_dicts(cls, v):
        """Convert string dicts and validate"""
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return {}
        return v or {}


class BusinessUpdateSchema(BaseModel):
    """Schema for updating a business listing"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Business name")
    description: Optional[str] = Field(None, description="Business description")
    short_description: Optional[str] = Field(None, max_length=500, description="Short description")
    category_id: Optional[UUID] = Field(None, description="Primary business category")
    
    # Contact and location
    email: Optional[str] = Field(None, description="Business email")
    phone: Optional[str] = Field(None, max_length=50, description="Business phone")
    website: Optional[str] = Field(None, max_length=500, description="Business website")
    
    # Address
    address_line_1: Optional[str] = Field(None, max_length=255, description="Primary address")
    address_line_2: Optional[str] = Field(None, max_length=255, description="Secondary address")
    city: Optional[str] = Field(None, max_length=100, description="City")
    state: Optional[str] = Field(None, max_length=100, description="State")
    postal_code: Optional[str] = Field(None, max_length=20, description="Postal code")
    country: Optional[str] = Field(None, max_length=100, description="Country")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude")
    
    # Business details
    business_hours: Optional[Dict[str, Dict[str, str]]] = Field(None, description="Business hours")
    social_media: Optional[Dict[str, str]] = Field(None, description="Social media links")
    amenities: Optional[List[str]] = Field(None, description="Business amenities")
    tags: Optional[List[str]] = Field(None, description="Business tags")
    price_range: Optional[str] = Field(None, regex="^\\$+$", description="Price range")
    
    # Media
    primary_image: Optional[str] = Field(None, max_length=500, description="Primary image URL")
    images: Optional[List[str]] = Field(None, description="Additional images")
    videos: Optional[List[str]] = Field(None, description="Video URLs")
    
    # SEO
    slug: Optional[str] = Field(None, max_length=255, description="URL slug")
    meta_title: Optional[str] = Field(None, max_length=255, description="Meta title")
    meta_description: Optional[str] = Field(None, max_length=500, description="Meta description")
    
    # Status
    status: Optional[str] = Field(None, regex="^(active|inactive|pending|suspended)$", description="Business status")
    is_featured: Optional[bool] = Field(None, description="Featured status")
    is_verified: Optional[bool] = Field(None, description="Verification status")


class BusinessResponseSchema(BaseResponseSchema, LocationSchema, ContactSchema, MediaSchema, RatingSchema, SEOSchema):
    """Schema for business listing responses"""
    name: str
    description: Optional[str]
    short_description: Optional[str]
    category_id: Optional[UUID]
    
    # Business details
    business_hours: Optional[Dict[str, Dict[str, str]]]
    social_media: Optional[Dict[str, str]]
    amenities: Optional[List[str]]
    tags: Optional[List[str]]
    price_range: Optional[str]
    
    # Business validation
    is_claimed: bool
    claimed_at: Optional[datetime]
    claimed_by: Optional[UUID]
    is_featured: bool
    is_verified: bool
    view_count: int
    
    # Owner information
    owner_name: Optional[str]
    owner_email: Optional[str]
    
    # Relationships
    category: Optional[CategoryResponseSchema] = None
    reviews_count: int = 0
    events_count: int = 0
    products_count: int = 0
    coupons_count: int = 0


class BusinessSearchSchema(SearchSchema, PaginationSchema, SortSchema):
    """Schema for business search parameters"""
    category_id: Optional[UUID] = Field(None, description="Filter by category")
    city: Optional[str] = Field(None, description="Filter by city")
    state: Optional[str] = Field(None, description="Filter by state")
    country: Optional[str] = Field(None, description="Filter by country")
    
    # Location-based search
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Search center latitude")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Search center longitude")
    radius: Optional[float] = Field(None, ge=0, le=100, description="Search radius in kilometers")
    
    # Filters
    is_verified: Optional[bool] = Field(None, description="Filter by verification status")
    is_featured: Optional[bool] = Field(None, description="Filter by featured status")
    price_range: Optional[List[str]] = Field(None, description="Filter by price range")
    amenities: Optional[List[str]] = Field(None, description="Filter by amenities")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    
    # Rating filter
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating")
    
    @validator('price_range', 'amenities', 'tags', pre=True)
    def validate_filter_lists(cls, v):
        """Validate filter lists"""
        if isinstance(v, str):
            return [item.strip() for item in v.split(',') if item.strip()]
        return v or []


# ============================================================================
# Business Review Schemas
# ============================================================================

class ReviewCreateSchema(BaseModel, MediaSchema):
    """Schema for creating a business review"""
    business_id: UUID = Field(description="Business being reviewed")
    title: Optional[str] = Field(None, max_length=255, description="Review title")
    content: Optional[str] = Field(None, description="Review content")
    rating: int = Field(ge=1, le=5, description="Rating (1-5)")
    reviewer_name: Optional[str] = Field(None, max_length=255, description="Reviewer name")
    reviewer_email: Optional[str] = Field(None, description="Reviewer email")
    visit_date: Optional[datetime] = Field(None, description="Visit date")


class ReviewUpdateSchema(BaseModel):
    """Schema for updating a review"""
    title: Optional[str] = Field(None, max_length=255, description="Review title")
    content: Optional[str] = Field(None, description="Review content")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating (1-5)")
    is_approved: Optional[bool] = Field(None, description="Approval status")
    is_featured: Optional[bool] = Field(None, description="Featured status")
    moderation_notes: Optional[str] = Field(None, description="Moderation notes")


class ReviewResponseSchema(BaseResponseSchema, MediaSchema):
    """Schema for review responses"""
    business_id: UUID
    title: Optional[str]
    content: Optional[str]
    rating: int
    reviewer_name: Optional[str]
    reviewer_email: Optional[str]
    reviewer_id: Optional[UUID]
    is_approved: bool
    is_featured: bool
    helpful_count: int
    visit_date: Optional[datetime]
    moderation_notes: Optional[str]
    
    # Nested business info
    business: Optional[Dict[str, Any]] = None


# ============================================================================
# Business Event Schemas
# ============================================================================

class EventCreateSchema(BaseModel, MediaSchema):
    """Schema for creating a business event"""
    business_id: UUID = Field(description="Business hosting the event")
    title: str = Field(min_length=1, max_length=255, description="Event title")
    description: Optional[str] = Field(None, description="Event description")
    start_date: datetime = Field(description="Event start date and time")
    end_date: Optional[datetime] = Field(None, description="Event end date and time")
    location: Optional[str] = Field(None, max_length=500, description="Event location")
    event_type: Optional[str] = Field(None, max_length=100, description="Event type")
    is_free: bool = Field(default=True, description="Is event free")
    price: Optional[str] = Field(None, max_length=50, description="Event price")
    max_attendees: Optional[int] = Field(None, ge=1, description="Maximum attendees")
    registration_url: Optional[str] = Field(None, max_length=500, description="Registration URL")
    is_published: bool = Field(default=False, description="Published status")


class EventUpdateSchema(BaseModel):
    """Schema for updating a business event"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Event title")
    description: Optional[str] = Field(None, description="Event description")
    start_date: Optional[datetime] = Field(None, description="Event start date and time")
    end_date: Optional[datetime] = Field(None, description="Event end date and time")
    location: Optional[str] = Field(None, max_length=500, description="Event location")
    event_type: Optional[str] = Field(None, max_length=100, description="Event type")
    is_free: Optional[bool] = Field(None, description="Is event free")
    price: Optional[str] = Field(None, max_length=50, description="Event price")
    max_attendees: Optional[int] = Field(None, ge=1, description="Maximum attendees")
    registration_url: Optional[str] = Field(None, max_length=500, description="Registration URL")
    is_published: Optional[bool] = Field(None, description="Published status")
    is_cancelled: Optional[bool] = Field(None, description="Cancelled status")


class EventResponseSchema(BaseResponseSchema, MediaSchema):
    """Schema for event responses"""
    business_id: UUID
    title: str
    description: Optional[str]
    start_date: datetime
    end_date: Optional[datetime]
    location: Optional[str]
    event_type: Optional[str]
    is_free: bool
    price: Optional[str]
    max_attendees: Optional[int]
    registration_url: Optional[str]
    is_published: bool
    is_cancelled: bool
    
    # Computed properties
    is_upcoming: bool = False
    is_ongoing: bool = False
    
    # Nested business info
    business: Optional[Dict[str, Any]] = None


# ============================================================================
# Business Product Schemas
# ============================================================================

class ProductCreateSchema(BaseModel, MediaSchema):
    """Schema for creating a business product"""
    business_id: UUID = Field(description="Business offering the product")
    name: str = Field(min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: Optional[str] = Field(None, max_length=100, description="Product category")
    price: Optional[str] = Field(None, max_length=50, description="Product price")
    price_currency: Optional[str] = Field(None, max_length=3, description="Price currency")
    sku: Optional[str] = Field(None, max_length=100, description="Product SKU")
    is_available: bool = Field(default=True, description="Product availability")
    specifications: Optional[Dict[str, Any]] = Field(None, description="Product specifications")


class ProductUpdateSchema(BaseModel):
    """Schema for updating a business product"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: Optional[str] = Field(None, max_length=100, description="Product category")
    price: Optional[str] = Field(None, max_length=50, description="Product price")
    price_currency: Optional[str] = Field(None, max_length=3, description="Price currency")
    sku: Optional[str] = Field(None, max_length=100, description="Product SKU")
    is_available: Optional[bool] = Field(None, description="Product availability")
    specifications: Optional[Dict[str, Any]] = Field(None, description="Product specifications")


class ProductResponseSchema(BaseResponseSchema, MediaSchema):
    """Schema for product responses"""
    business_id: UUID
    name: str
    description: Optional[str]
    category: Optional[str]
    price: Optional[str]
    price_currency: Optional[str]
    sku: Optional[str]
    is_available: bool
    specifications: Optional[Dict[str, Any]]
    
    # Nested business info
    business: Optional[Dict[str, Any]] = None


# ============================================================================
# Business Coupon Schemas
# ============================================================================

class CouponCreateSchema(BaseModel):
    """Schema for creating a business coupon"""
    business_id: UUID = Field(description="Business offering the coupon")
    title: str = Field(min_length=1, max_length=255, description="Coupon title")
    description: Optional[str] = Field(None, description="Coupon description")
    discount_type: str = Field(regex="^(percentage|fixed|bogo)$", description="Discount type")
    discount_value: str = Field(max_length=50, description="Discount value")
    valid_from: datetime = Field(description="Valid from date")
    valid_until: datetime = Field(description="Valid until date")
    usage_limit: Optional[int] = Field(None, ge=1, description="Usage limit")
    coupon_code: Optional[str] = Field(None, max_length=50, description="Coupon code")
    terms: Optional[str] = Field(None, description="Terms and conditions")
    is_active: bool = Field(default=True, description="Active status")


class CouponUpdateSchema(BaseModel):
    """Schema for updating a business coupon"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Coupon title")
    description: Optional[str] = Field(None, description="Coupon description")
    discount_type: Optional[str] = Field(None, regex="^(percentage|fixed|bogo)$", description="Discount type")
    discount_value: Optional[str] = Field(None, max_length=50, description="Discount value")
    valid_from: Optional[datetime] = Field(None, description="Valid from date")
    valid_until: Optional[datetime] = Field(None, description="Valid until date")
    usage_limit: Optional[int] = Field(None, ge=1, description="Usage limit")
    coupon_code: Optional[str] = Field(None, max_length=50, description="Coupon code")
    terms: Optional[str] = Field(None, description="Terms and conditions")
    is_active: Optional[bool] = Field(None, description="Active status")


class CouponResponseSchema(BaseResponseSchema):
    """Schema for coupon responses"""
    business_id: UUID
    title: str
    description: Optional[str]
    discount_type: str
    discount_value: str
    valid_from: datetime
    valid_until: datetime
    usage_limit: Optional[int]
    usage_count: int
    coupon_code: Optional[str]
    terms: Optional[str]
    is_active: bool
    
    # Computed properties
    is_valid: bool = False
    
    # Nested business info
    business: Optional[Dict[str, Any]] = None


# Enable forward references
CategoryResponseSchema.model_rebuild()


# ============================================================================
# Bulk Operations and Analytics
# ============================================================================

class BusinessClaimSchema(BaseModel):
    """Schema for claiming a business"""
    verification_documents: Optional[List[str]] = Field(None, description="Verification document URLs")
    message: Optional[str] = Field(None, max_length=1000, description="Claim message")


class BusinessAnalyticsSchema(BaseModel):
    """Schema for business analytics data"""
    date_from: datetime = Field(description="Analytics start date")
    date_to: datetime = Field(description="Analytics end date")
    metrics: List[str] = Field(default=["views", "clicks", "calls"], description="Metrics to include")


class BusinessAnalyticsResponseSchema(BaseModel):
    """Schema for business analytics responses"""
    business_id: UUID
    period: Dict[str, datetime]
    metrics: Dict[str, int]
    trends: Dict[str, float]
    comparisons: Optional[Dict[str, Any]] = None