"""
Base Pydantic models for BizoSaaS platform
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict


class BaseModel(PydanticBaseModel):
    """Base model with common configurations"""
    model_config = ConfigDict(
        # Enable ORM mode for SQLAlchemy integration
        from_attributes=True,
        # Validate on assignment
        validate_assignment=True,
        # Use enum values instead of enum objects
        use_enum_values=True,
        # Exclude None values from dict
        exclude_none=True
    )


class TenantModel(BaseModel):
    """Base model for tenant-scoped resources"""
    tenant_id: int = Field(..., description="Tenant ID for multi-tenancy")


class TimestampedModel(BaseModel):
    """Model with created/updated timestamps"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class TenantTimestampedModel(TenantModel, TimestampedModel):
    """Combined tenant-scoped and timestamped model"""
    pass


# Common response models
class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool = True
    message: str = "Operation completed successfully"


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    error: str
    details: Optional[dict] = None


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    items: list
    total: int
    page: int = 1
    size: int = 50
    pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1