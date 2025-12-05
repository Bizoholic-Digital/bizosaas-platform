"""
Common Pydantic Schemas
Shared data models and validation schemas for the Business Directory service
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from uuid import UUID
import re


class TimestampSchema(BaseModel):
    """Base schema with timestamp fields"""
    created_at: datetime
    updated_at: datetime


class TenantSchema(BaseModel):
    """Base schema with tenant information"""
    tenant_id: UUID


class BaseResponseSchema(TimestampSchema, TenantSchema):
    """Base response schema with common fields"""
    id: UUID
    status: str = "active"
    is_deleted: bool = False
    
    class Config:
        from_attributes = True


class PaginationSchema(BaseModel):
    """Pagination parameters schema"""
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Items per page")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries"""
        return (self.page - 1) * self.size


class SortSchema(BaseModel):
    """Sorting parameters schema"""
    sort_by: str = Field(default="created_at", description="Field to sort by")
    sort_order: str = Field(default="desc", regex="^(asc|desc)$", description="Sort order")


class SearchSchema(BaseModel):
    """Search parameters schema"""
    query: Optional[str] = Field(None, min_length=1, max_length=500, description="Search query")
    search_type: str = Field(default="hybrid", regex="^(semantic|keyword|hybrid)$", description="Search type")
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Similarity threshold for semantic search")


class LocationSchema(BaseModel):
    """Location information schema"""
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude coordinate")
    address_line_1: Optional[str] = Field(None, max_length=255, description="Primary address line")
    address_line_2: Optional[str] = Field(None, max_length=255, description="Secondary address line")
    city: Optional[str] = Field(None, max_length=100, description="City")
    state: Optional[str] = Field(None, max_length=100, description="State or province")
    postal_code: Optional[str] = Field(None, max_length=20, description="Postal or ZIP code")
    country: Optional[str] = Field(None, max_length=100, description="Country")
    
    @validator('postal_code')
    def validate_postal_code(cls, v):
        """Validate postal code format"""
        if v:
            # Basic validation - alphanumeric with optional spaces/hyphens
            if not re.match(r'^[A-Za-z0-9\s\-]{3,20}$', v):
                raise ValueError('Invalid postal code format')
        return v
    
    @property
    def full_address(self) -> str:
        """Get formatted full address"""
        parts = [
            self.address_line_1,
            self.address_line_2, 
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ", ".join(filter(None, parts))
    
    @property
    def coordinates(self) -> Optional[tuple]:
        """Get coordinates as tuple"""
        if self.latitude is not None and self.longitude is not None:
            return (self.latitude, self.longitude)
        return None


class ContactSchema(BaseModel):
    """Contact information schema"""
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    website: Optional[str] = Field(None, max_length=500, description="Website URL")
    
    @validator('website')
    def validate_website(cls, v):
        """Validate and normalize website URL"""
        if v:
            # Add protocol if missing
            if not v.startswith(('http://', 'https://')):
                v = f"https://{v}"
            
            # Basic URL validation
            url_pattern = r'^https?://(?:[-\w.])+(?::[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
            if not re.match(url_pattern, v):
                raise ValueError('Invalid website URL format')
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format"""
        if v:
            # Remove all non-digit characters for validation
            digits_only = re.sub(r'\D', '', v)
            if len(digits_only) < 7 or len(digits_only) > 15:
                raise ValueError('Phone number must be between 7 and 15 digits')
        return v


class MediaSchema(BaseModel):
    """Media attachments schema"""
    primary_image: Optional[str] = Field(None, max_length=500, description="Primary image URL")
    images: List[str] = Field(default_factory=list, description="Additional image URLs")
    videos: List[str] = Field(default_factory=list, description="Video URLs")
    
    @validator('images', 'videos', pre=True)
    def validate_media_lists(cls, v):
        """Validate media URL lists"""
        if isinstance(v, str):
            try:
                import json
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v or []
    
    @validator('primary_image', 'images', 'videos')
    def validate_urls(cls, v):
        """Validate URL format"""
        urls = [v] if isinstance(v, str) else v
        url_pattern = r'^https?://(?:[-\w.])+(?::[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
        
        for url in urls:
            if url and not re.match(url_pattern, url):
                raise ValueError(f'Invalid URL format: {url}')
        
        return v


class RatingSchema(BaseModel):
    """Rating information schema"""
    rating_average: float = Field(default=0.0, ge=0.0, le=5.0, description="Average rating")
    rating_count: int = Field(default=0, ge=0, description="Total number of ratings")


class SEOSchema(BaseModel):
    """SEO metadata schema"""
    slug: Optional[str] = Field(None, max_length=255, description="URL-friendly slug")
    meta_title: Optional[str] = Field(None, max_length=255, description="SEO meta title")
    meta_description: Optional[str] = Field(None, max_length=500, description="SEO meta description")
    keywords: Optional[str] = Field(None, max_length=500, description="SEO keywords")
    
    @validator('slug')
    def validate_slug(cls, v):
        """Validate slug format"""
        if v:
            # Convert to lowercase and replace spaces/special chars with hyphens
            v = re.sub(r'[^\w\s-]', '', v.lower())
            v = re.sub(r'[\s_]+', '-', v).strip('-')
            
            if not re.match(r'^[a-z0-9-]+$', v):
                raise ValueError('Slug must contain only lowercase letters, numbers, and hyphens')
        return v


class BusinessHoursSchema(BaseModel):
    """Business hours schema"""
    monday: Optional[Dict[str, str]] = Field(None, description="Monday hours")
    tuesday: Optional[Dict[str, str]] = Field(None, description="Tuesday hours")
    wednesday: Optional[Dict[str, str]] = Field(None, description="Wednesday hours")
    thursday: Optional[Dict[str, str]] = Field(None, description="Thursday hours")
    friday: Optional[Dict[str, str]] = Field(None, description="Friday hours")
    saturday: Optional[Dict[str, str]] = Field(None, description="Saturday hours")
    sunday: Optional[Dict[str, str]] = Field(None, description="Sunday hours")
    
    @validator('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    def validate_hours(cls, v):
        """Validate hours format"""
        if v:
            required_keys = {'open', 'close'}
            if not isinstance(v, dict) or not required_keys.issubset(v.keys()):
                raise ValueError('Hours must include "open" and "close" times')
            
            # Validate time format (HH:MM)
            time_pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
            for time_value in v.values():
                if time_value and not re.match(time_pattern, time_value):
                    raise ValueError('Time must be in HH:MM format')
        return v


class ErrorSchema(BaseModel):
    """Error response schema"""
    error: str = Field(description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    code: Optional[str] = Field(None, description="Error code")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")


class SuccessSchema(BaseModel):
    """Success response schema"""
    success: bool = Field(True, description="Success status")
    message: str = Field(description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data")


class HealthCheckSchema(BaseModel):
    """Health check response schema"""
    status: str = Field(description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")
    version: str = Field(description="Service version")
    dependencies: Dict[str, str] = Field(description="Dependency statuses")
    performance: Optional[Dict[str, Any]] = Field(None, description="Performance metrics")


class PaginatedResponseSchema(BaseModel):
    """Paginated response schema"""
    items: List[Any] = Field(description="List of items")
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    size: int = Field(description="Items per page")
    pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Whether there are more pages")
    has_prev: bool = Field(description="Whether there are previous pages")
    
    @validator('pages')
    def calculate_pages(cls, v, values):
        """Calculate total pages"""
        total = values.get('total', 0)
        size = values.get('size', 20)
        return (total + size - 1) // size if total > 0 else 0
    
    @validator('has_next')
    def calculate_has_next(cls, v, values):
        """Calculate if there are more pages"""
        page = values.get('page', 1)
        pages = values.get('pages', 0)
        return page < pages
    
    @validator('has_prev')
    def calculate_has_prev(cls, v, values):
        """Calculate if there are previous pages"""
        page = values.get('page', 1)
        return page > 1


class FilterSchema(BaseModel):
    """Generic filter schema"""
    field: str = Field(description="Field to filter by")
    operator: str = Field(default="eq", regex="^(eq|ne|gt|gte|lt|lte|in|nin|contains|startswith|endswith)$", description="Filter operator")
    value: Union[str, int, float, bool, List[Any]] = Field(description="Filter value")
    
    @validator('value')
    def validate_filter_value(cls, v, values):
        """Validate filter value based on operator"""
        operator = values.get('operator')
        
        if operator in ['in', 'nin'] and not isinstance(v, list):
            raise ValueError(f'Operator "{operator}" requires a list value')
        
        if operator in ['gt', 'gte', 'lt', 'lte'] and not isinstance(v, (int, float)):
            raise ValueError(f'Operator "{operator}" requires a numeric value')
        
        return v


class BulkOperationSchema(BaseModel):
    """Bulk operation schema"""
    operation: str = Field(regex="^(create|update|delete)$", description="Bulk operation type")
    items: List[Dict[str, Any]] = Field(description="Items to process")
    
    @validator('items')
    def validate_items_not_empty(cls, v):
        """Validate items list is not empty"""
        if not v:
            raise ValueError('Items list cannot be empty')
        return v


class FileUploadSchema(BaseModel):
    """File upload metadata schema"""
    filename: str = Field(description="Original filename")
    content_type: str = Field(description="File content type")
    size: int = Field(description="File size in bytes")
    url: str = Field(description="Uploaded file URL")
    
    @validator('content_type')
    def validate_content_type(cls, v):
        """Validate file content type"""
        allowed_types = [
            'image/jpeg', 'image/png', 'image/webp', 'image/gif',
            'video/mp4', 'video/webm', 'video/quicktime'
        ]
        if v not in allowed_types:
            raise ValueError(f'Content type "{v}" not allowed')
        return v
    
    @validator('size')
    def validate_file_size(cls, v):
        """Validate file size"""
        max_size = 10 * 1024 * 1024  # 10MB
        if v > max_size:
            raise ValueError(f'File size {v} exceeds maximum allowed size {max_size}')
        return v