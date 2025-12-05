"""
Business Directory Schemas Package
Exports all Pydantic schemas for request/response validation
"""

from .common import (
    TimestampSchema,
    TenantSchema,
    BaseResponseSchema,
    PaginationSchema,
    SortSchema,
    SearchSchema,
    LocationSchema,
    ContactSchema,
    MediaSchema,
    RatingSchema,
    SEOSchema,
    BusinessHoursSchema,
    ErrorSchema,
    SuccessSchema,
    HealthCheckSchema,
    PaginatedResponseSchema,
    FilterSchema,
    BulkOperationSchema,
    FileUploadSchema
)

from .business import (
    # Category schemas
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
    
    # Business schemas
    BusinessCreateSchema,
    BusinessUpdateSchema,
    BusinessResponseSchema,
    BusinessSearchSchema,
    BusinessClaimSchema,
    
    # Review schemas
    ReviewCreateSchema,
    ReviewUpdateSchema,
    ReviewResponseSchema,
    
    # Event schemas
    EventCreateSchema,
    EventUpdateSchema,
    EventResponseSchema,
    
    # Product schemas
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductResponseSchema,
    
    # Coupon schemas
    CouponCreateSchema,
    CouponUpdateSchema,
    CouponResponseSchema,
    
    # Analytics schemas
    BusinessAnalyticsSchema,
    BusinessAnalyticsResponseSchema
)

from .google_integration import (
    # Google OAuth schemas
    GoogleAuthUrlSchema,
    GoogleAuthUrlResponseSchema,
    GoogleCallbackSchema,
    
    # Google Account schemas
    GoogleAccountResponseSchema,
    
    # Google Location schemas
    GoogleLocationResponseSchema,
    LocationSyncSchema,
    BulkLocationSyncSchema,
    LocationManagementSchema,
    
    # Conflict Resolution schemas
    ConflictResolutionSchema,
    LocationConflictResponseSchema,
    
    # Sync Operation schemas
    SyncOperationResponseSchema,
    BatchOperationResponseSchema,
    
    # Analytics and Stats schemas
    SyncStatsResponseSchema,
    GoogleBusinessInsightsSchema,
    GoogleIntegrationHealthSchema
)

# Export all schemas
__all__ = [
    # Common schemas
    "TimestampSchema",
    "TenantSchema", 
    "BaseResponseSchema",
    "PaginationSchema",
    "SortSchema",
    "SearchSchema",
    "LocationSchema",
    "ContactSchema",
    "MediaSchema",
    "RatingSchema",
    "SEOSchema",
    "BusinessHoursSchema",
    "ErrorSchema",
    "SuccessSchema",
    "HealthCheckSchema",
    "PaginatedResponseSchema",
    "FilterSchema",
    "BulkOperationSchema",
    "FileUploadSchema",
    
    # Business Category schemas
    "CategoryCreateSchema",
    "CategoryUpdateSchema", 
    "CategoryResponseSchema",
    
    # Business Listing schemas
    "BusinessCreateSchema",
    "BusinessUpdateSchema",
    "BusinessResponseSchema",
    "BusinessSearchSchema",
    "BusinessClaimSchema",
    
    # Review schemas
    "ReviewCreateSchema",
    "ReviewUpdateSchema",
    "ReviewResponseSchema",
    
    # Event schemas
    "EventCreateSchema",
    "EventUpdateSchema",
    "EventResponseSchema",
    
    # Product schemas
    "ProductCreateSchema",
    "ProductUpdateSchema",
    "ProductResponseSchema",
    
    # Coupon schemas
    "CouponCreateSchema",
    "CouponUpdateSchema",
    "CouponResponseSchema",
    
    # Analytics schemas
    "BusinessAnalyticsSchema",
    "BusinessAnalyticsResponseSchema",
    
    # Google Integration schemas
    "GoogleAuthUrlSchema",
    "GoogleAuthUrlResponseSchema",
    "GoogleCallbackSchema",
    "GoogleAccountResponseSchema",
    "GoogleLocationResponseSchema",
    "LocationSyncSchema",
    "BulkLocationSyncSchema",
    "LocationManagementSchema",
    "ConflictResolutionSchema",
    "LocationConflictResponseSchema",
    "SyncOperationResponseSchema",
    "BatchOperationResponseSchema",
    "SyncStatsResponseSchema",
    "GoogleBusinessInsightsSchema",
    "GoogleIntegrationHealthSchema"
]

# Schema metadata for API documentation
SCHEMA_METADATA = {
    "create_schemas": [
        "CategoryCreateSchema",
        "BusinessCreateSchema", 
        "ReviewCreateSchema",
        "EventCreateSchema",
        "ProductCreateSchema",
        "CouponCreateSchema"
    ],
    "update_schemas": [
        "CategoryUpdateSchema",
        "BusinessUpdateSchema",
        "ReviewUpdateSchema", 
        "EventUpdateSchema",
        "ProductUpdateSchema",
        "CouponUpdateSchema"
    ],
    "response_schemas": [
        "CategoryResponseSchema",
        "BusinessResponseSchema",
        "ReviewResponseSchema",
        "EventResponseSchema", 
        "ProductResponseSchema",
        "CouponResponseSchema"
    ],
    "search_schemas": [
        "BusinessSearchSchema",
        "SearchSchema"
    ],
    "google_integration_schemas": [
        "GoogleAuthUrlSchema",
        "GoogleCallbackSchema",
        "LocationSyncSchema",
        "BulkLocationSyncSchema",
        "LocationManagementSchema",
        "ConflictResolutionSchema"
    ],
    "google_response_schemas": [
        "GoogleAuthUrlResponseSchema",
        "GoogleAccountResponseSchema",
        "GoogleLocationResponseSchema",
        "LocationConflictResponseSchema",
        "SyncOperationResponseSchema",
        "BatchOperationResponseSchema",
        "SyncStatsResponseSchema",
        "GoogleBusinessInsightsSchema",
        "GoogleIntegrationHealthSchema"
    ],
    "utility_schemas": [
        "PaginationSchema",
        "SortSchema",
        "FilterSchema",
        "ErrorSchema",
        "SuccessSchema"
    ]
}

# Validation rules for schemas
VALIDATION_RULES = {
    "business_name": {
        "min_length": 1,
        "max_length": 255,
        "required": True
    },
    "email": {
        "format": "email",
        "max_length": 255
    },
    "phone": {
        "pattern": r"^[\+]?[1-9]?\d{1,15}$",
        "max_length": 50
    },
    "rating": {
        "min_value": 1,
        "max_value": 5,
        "type": "integer"
    },
    "coordinates": {
        "latitude": {"min": -90, "max": 90},
        "longitude": {"min": -180, "max": 180}
    },
    "pagination": {
        "max_page_size": 100,
        "default_page_size": 20
    }
}