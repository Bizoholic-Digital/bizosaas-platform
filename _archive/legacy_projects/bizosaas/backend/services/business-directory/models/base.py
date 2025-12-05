"""
Base Model Classes
Provides common functionality for all database models including tenant isolation,
audit fields, soft delete, and vector search capabilities
"""

from sqlalchemy import Column, String, DateTime, Boolean, text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from datetime import datetime
from typing import Optional
import uuid

# Base class with metadata configuration
Base = declarative_base()


class TimestampMixin:
    """
    Mixin for automatic timestamp management
    """
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Record creation timestamp"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Record last update timestamp"
    )


class TenantMixin:
    """
    Mixin for multi-tenant support with row-level security
    """
    tenant_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        doc="Tenant identifier for multi-tenant isolation"
    )
    
    @declared_attr
    def __table_args__(cls):
        """Add tenant_id index for performance"""
        return (
            Index(f'ix_{cls.__tablename__}_tenant_id', 'tenant_id'),
        )


class SoftDeleteMixin:
    """
    Mixin for soft delete functionality
    """
    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Soft delete flag"
    )
    
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="Soft delete timestamp"
    )
    
    def soft_delete(self):
        """Mark record as deleted"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
    
    def restore(self):
        """Restore soft deleted record"""
        self.is_deleted = False
        self.deleted_at = None


class AuditMixin:
    """
    Mixin for audit trail functionality
    """
    created_by = Column(
        UUID(as_uuid=True),
        nullable=True,
        doc="User who created the record"
    )
    
    updated_by = Column(
        UUID(as_uuid=True),
        nullable=True,
        doc="User who last updated the record"
    )
    
    version = Column(
        "version",
        String(50),
        nullable=True,
        doc="Record version for optimistic locking"
    )


class GeospatialMixin:
    """
    Mixin for geospatial data support
    """
    latitude = Column(
        "latitude",
        String(20),
        nullable=True,
        doc="Latitude coordinate"
    )
    
    longitude = Column(
        "longitude", 
        String(20),
        nullable=True,
        doc="Longitude coordinate"
    )
    
    @declared_attr
    def location_point(cls):
        """PostGIS point column for spatial queries"""
        # Note: This requires PostGIS extension
        # return Column(Geometry('POINT', srid=4326), nullable=True)
        pass
    
    @property
    def coordinates(self) -> Optional[tuple]:
        """Get coordinates as tuple"""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None


class VectorSearchMixin:
    """
    Mixin for AI vector search capabilities using pgvector
    """
    
    @declared_attr
    def search_vector(cls):
        """Vector embedding for semantic search"""
        return Column(
            Vector(384),  # Dimension for all-MiniLM-L6-v2 model
            nullable=True,
            doc="Vector embedding for semantic search"
        )
    
    @declared_attr
    def search_content(cls):
        """Searchable text content"""
        return Column(
            String,
            nullable=True,
            doc="Concatenated searchable content for vector generation"
        )
    
    @declared_attr
    def __table_args__(cls):
        """Add vector search index"""
        base_args = getattr(super(), '__table_args__', ())
        if isinstance(base_args, tuple):
            return base_args + (
                Index(f'ix_{cls.__tablename__}_search_vector', 'search_vector', 
                      postgresql_using='ivfflat', postgresql_ops={'search_vector': 'vector_cosine_ops'}),
            )
        return base_args


class BaseModel(Base, TimestampMixin, TenantMixin, SoftDeleteMixin, AuditMixin):
    """
    Base model class with all common functionality
    """
    __abstract__ = True
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        doc="Primary key identifier"
    )
    
    @declared_attr
    def __tablename__(cls):
        """Auto-generate table name from class name"""
        return cls.__name__.lower()
    
    def __repr__(self):
        """String representation of the model"""
        return f"<{self.__class__.__name__}(id={self.id})>"
    
    def to_dict(self, include_deleted: bool = False) -> dict:
        """Convert model to dictionary"""
        if self.is_deleted and not include_deleted:
            return {}
        
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            elif isinstance(value, uuid.UUID):
                result[column.name] = str(value)
            else:
                result[column.name] = value
        return result
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create model instance from dictionary"""
        # Filter out non-column keys
        column_names = {c.name for c in cls.__table__.columns}
        filtered_data = {k: v for k, v in data.items() if k in column_names}
        return cls(**filtered_data)


class BusinessBaseModel(BaseModel, GeospatialMixin, VectorSearchMixin):
    """
    Base model for business-related entities with geospatial and vector search
    """
    __abstract__ = True
    
    # Common business fields
    status = Column(
        String(20),
        default="active",
        nullable=False,
        index=True,
        doc="Entity status (active, inactive, pending, suspended)"
    )
    
    # SEO and metadata fields
    slug = Column(
        String(255),
        nullable=True,
        index=True,
        doc="URL-friendly slug for SEO"
    )
    
    meta_title = Column(
        String(255),
        nullable=True,
        doc="SEO meta title"
    )
    
    meta_description = Column(
        String(500),
        nullable=True,
        doc="SEO meta description"
    )
    
    # Feature flags
    is_featured = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Featured entity flag"
    )
    
    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Verification status"
    )
    
    # Performance tracking
    view_count = Column(
        "view_count",
        String(10),
        default="0",
        nullable=False,
        doc="View count for analytics"
    )
    
    @declared_attr
    def __table_args__(cls):
        """Add additional indexes for business models"""
        base_args = super().__table_args__
        if isinstance(base_args, tuple):
            return base_args + (
                Index(f'ix_{cls.__tablename__}_status_tenant', 'status', 'tenant_id'),
                Index(f'ix_{cls.__tablename__}_featured_tenant', 'is_featured', 'tenant_id'),
                Index(f'ix_{cls.__tablename__}_verified_tenant', 'is_verified', 'tenant_id'),
            )
        return base_args
    
    def update_search_content(self):
        """Update the search_content field for vector generation"""
        # This method should be overridden in subclasses
        # to create appropriate search content
        pass
    
    def increment_view_count(self):
        """Increment view count"""
        try:
            current_count = int(self.view_count or "0")
            self.view_count = str(current_count + 1)
        except (ValueError, TypeError):
            self.view_count = "1"


class CategoryBaseModel(BaseModel):
    """
    Base model for hierarchical category structures
    """
    __abstract__ = True
    
    name = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Category name"
    )
    
    description = Column(
        String(500),
        nullable=True,
        doc="Category description"
    )
    
    parent_id = Column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
        doc="Parent category for hierarchical structure"
    )
    
    sort_order = Column(
        "sort_order",
        String(10),
        default="0",
        nullable=False,
        doc="Sort order for display"
    )
    
    icon = Column(
        String(255),
        nullable=True,
        doc="Category icon or image URL"
    )
    
    color = Column(
        String(7),
        nullable=True,
        doc="Category color code (hex)"
    )
    
    @declared_attr
    def __table_args__(cls):
        """Add category-specific indexes"""
        base_args = super().__table_args__
        if isinstance(base_args, tuple):
            return base_args + (
                Index(f'ix_{cls.__tablename__}_parent_tenant', 'parent_id', 'tenant_id'),
                Index(f'ix_{cls.__tablename__}_sort_tenant', 'sort_order', 'tenant_id'),
            )
        return base_args


class RatingMixin:
    """
    Mixin for entities that can be rated
    """
    rating_average = Column(
        "rating_average",
        String(5),
        default="0.0",
        nullable=False,
        doc="Average rating score"
    )
    
    rating_count = Column(
        "rating_count",
        String(10),
        default="0",
        nullable=False,
        doc="Total number of ratings"
    )
    
    def update_rating(self, new_rating: float):
        """Update average rating with new rating"""
        try:
            current_avg = float(self.rating_average or "0.0")
            current_count = int(self.rating_count or "0")
            
            # Calculate new average
            total_score = current_avg * current_count + new_rating
            new_count = current_count + 1
            new_average = total_score / new_count
            
            self.rating_average = str(round(new_average, 2))
            self.rating_count = str(new_count)
        except (ValueError, TypeError, ZeroDivisionError):
            self.rating_average = str(new_rating)
            self.rating_count = "1"


class MediaMixin:
    """
    Mixin for entities with media attachments
    """
    primary_image = Column(
        String(500),
        nullable=True,
        doc="Primary image URL"
    )
    
    images = Column(
        String,
        nullable=True,
        doc="JSON array of image URLs"
    )
    
    videos = Column(
        String,
        nullable=True,
        doc="JSON array of video URLs"
    )
    
    @property
    def image_list(self) -> list:
        """Get images as list"""
        import json
        try:
            return json.loads(self.images) if self.images else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    @property
    def video_list(self) -> list:
        """Get videos as list"""
        import json
        try:
            return json.loads(self.videos) if self.videos else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    def add_image(self, image_url: str):
        """Add image to the collection"""
        import json
        images = self.image_list
        if image_url not in images:
            images.append(image_url)
            self.images = json.dumps(images)
            
            # Set as primary if first image
            if not self.primary_image:
                self.primary_image = image_url
    
    def remove_image(self, image_url: str):
        """Remove image from the collection"""
        import json
        images = self.image_list
        if image_url in images:
            images.remove(image_url)
            self.images = json.dumps(images)
            
            # Update primary image if removed
            if self.primary_image == image_url:
                self.primary_image = images[0] if images else None


# Model registry for dynamic model discovery
MODEL_REGISTRY = {}


def register_model(model_class):
    """Register model in the global registry"""
    MODEL_REGISTRY[model_class.__name__] = model_class
    return model_class