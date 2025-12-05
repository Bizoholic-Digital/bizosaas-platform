"""
Business Directory Models Package
Exports all database models for the Business Directory service
"""

from .base import (
    Base,
    BaseModel,
    BusinessBaseModel,
    CategoryBaseModel,
    TenantMixin,
    TimestampMixin,
    SoftDeleteMixin,
    AuditMixin,
    GeospatialMixin,
    VectorSearchMixin,
    RatingMixin,
    MediaMixin,
    MODEL_REGISTRY,
    register_model
)

from .business import (
    BusinessCategory,
    BusinessListing,
    BusinessReview,
    BusinessEvent,
    BusinessProduct,
    BusinessCoupon,
    BusinessAnalytics
)

from .google_integration import (
    GoogleAccount,
    GoogleBusinessLocation,
    SyncMapping,
    SyncLog,
    SyncConflict,
    GoogleCacheEntry,
    GoogleAccountStatus,
    SyncStatus,
    ConflictResolutionStrategy
)

# Export all models
__all__ = [
    # Base classes
    "Base",
    "BaseModel", 
    "BusinessBaseModel",
    "CategoryBaseModel",
    
    # Mixins
    "TenantMixin",
    "TimestampMixin", 
    "SoftDeleteMixin",
    "AuditMixin",
    "GeospatialMixin",
    "VectorSearchMixin",
    "RatingMixin",
    "MediaMixin",
    
    # Business models
    "BusinessCategory",
    "BusinessListing", 
    "BusinessReview",
    "BusinessEvent",
    "BusinessProduct",
    "BusinessCoupon",
    "BusinessAnalytics",
    
    # Google integration models
    "GoogleAccount",
    "GoogleBusinessLocation", 
    "SyncMapping",
    "SyncLog",
    "SyncConflict",
    "GoogleCacheEntry",
    
    # Enums
    "GoogleAccountStatus",
    "SyncStatus",
    "ConflictResolutionStrategy",
    
    # Utilities
    "MODEL_REGISTRY",
    "register_model"
]

# Model metadata for API documentation
MODEL_METADATA = {
    "BusinessCategory": {
        "description": "Hierarchical business categories",
        "endpoints": ["categories"],
        "permissions": ["business:read", "business:write", "business:admin"]
    },
    "BusinessListing": {
        "description": "Main business directory listings",
        "endpoints": ["businesses", "search"],
        "permissions": ["business:read", "business:write", "business:admin"]
    },
    "BusinessReview": {
        "description": "Business reviews and ratings",
        "endpoints": ["reviews"],
        "permissions": ["review:write", "business:read"]
    },
    "BusinessEvent": {
        "description": "Business events and announcements",
        "endpoints": ["events"],
        "permissions": ["business:write", "business:admin"]
    },
    "BusinessProduct": {
        "description": "Products and services offered by businesses",
        "endpoints": ["products"],
        "permissions": ["business:write", "business:admin"]
    },
    "BusinessCoupon": {
        "description": "Business coupons and promotions",
        "endpoints": ["coupons"],
        "permissions": ["business:write", "business:admin"]
    },
    "BusinessAnalytics": {
        "description": "Business performance analytics",
        "endpoints": ["analytics"],
        "permissions": ["analytics:read", "business:admin"]
    }
}

# Database relationship mapping
RELATIONSHIP_MAP = {
    "BusinessListing": {
        "category": "BusinessCategory",
        "reviews": "BusinessReview",
        "events": "BusinessEvent", 
        "products": "BusinessProduct",
        "coupons": "BusinessCoupon",
        "analytics": "BusinessAnalytics"
    },
    "BusinessCategory": {
        "businesses": "BusinessListing",
        "parent": "BusinessCategory",
        "children": "BusinessCategory"
    }
}

# Search configuration for models
SEARCH_CONFIG = {
    "BusinessListing": {
        "vector_fields": ["search_vector"],
        "text_fields": ["name", "description", "city", "state"],
        "filter_fields": ["category_id", "city", "state", "is_verified", "status"],
        "sort_fields": ["name", "rating_average", "created_at", "view_count"]
    },
    "BusinessCategory": {
        "text_fields": ["name", "description"],
        "filter_fields": ["parent_id", "is_active"],
        "sort_fields": ["name", "sort_order", "business_count"]
    },
    "BusinessReview": {
        "text_fields": ["title", "content"],
        "filter_fields": ["business_id", "rating", "is_approved"],
        "sort_fields": ["created_at", "rating", "helpful_count"]
    },
    "BusinessEvent": {
        "text_fields": ["title", "description"],
        "filter_fields": ["business_id", "event_type", "is_published"],
        "sort_fields": ["start_date", "created_at"]
    }
}