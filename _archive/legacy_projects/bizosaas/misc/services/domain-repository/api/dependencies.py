"""
FastAPI Dependencies for Domain Repository Service

This module provides dependency injection for the FastAPI application.
"""

from typing import Optional
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .application.services import DomainRepositoryService
from .infrastructure.repositories import LeadRepository, CustomerRepository, CampaignRepository
from .infrastructure.event_bus_integration import EventBusIntegration, EventBusConfig, DomainEventPublisher
from .config import get_settings


# Global instances (will be initialized in main.py)
_domain_service: Optional[DomainRepositoryService] = None
_event_bus_integration: Optional[EventBusIntegration] = None
_database_session: Optional[AsyncSession] = None


def set_domain_service(service: DomainRepositoryService) -> None:
    """Set the global domain service instance"""
    global _domain_service
    _domain_service = service


def set_event_bus_integration(integration: EventBusIntegration) -> None:
    """Set the global event bus integration instance"""
    global _event_bus_integration
    _event_bus_integration = integration


def set_database_session(session: AsyncSession) -> None:
    """Set the global database session"""
    global _database_session
    _database_session = session


async def get_domain_service() -> DomainRepositoryService:
    """Get the domain service instance"""
    if _domain_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Domain service not initialized"
        )
    return _domain_service


async def get_event_bus_integration() -> EventBusIntegration:
    """Get the event bus integration instance"""
    if _event_bus_integration is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Event bus integration not initialized"
        )
    return _event_bus_integration


async def get_database_session() -> AsyncSession:
    """Get the database session"""
    if _database_session is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database session not initialized"
        )
    return _database_session


async def get_tenant_context(
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID")
) -> UUID:
    """Extract tenant ID from request headers"""
    
    if not x_tenant_id:
        # Default tenant for development/testing
        return UUID("00000000-0000-4000-8000-000000000001")
    
    try:
        return UUID(x_tenant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid tenant ID format"
        )


async def get_user_context(
    x_user_id: Optional[str] = Header(None, alias="X-User-ID")
) -> Optional[UUID]:
    """Extract user ID from request headers (optional)"""
    
    if not x_user_id:
        return None
    
    try:
        return UUID(x_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )


def validate_tenant_access(tenant_id: UUID) -> bool:
    """Validate if the current request has access to the tenant"""
    # In a production system, this would validate against user permissions
    # For now, we'll allow all access
    return True


async def require_tenant_access(tenant_id: UUID = Depends(get_tenant_context)) -> UUID:
    """Require valid tenant access"""
    
    if not validate_tenant_access(tenant_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to tenant"
        )
    
    return tenant_id


async def get_authenticated_user(
    user_id: Optional[UUID] = Depends(get_user_context)
) -> Optional[UUID]:
    """Get authenticated user (if any)"""
    # In a production system, this would validate authentication tokens
    return user_id


async def require_authenticated_user(
    user_id: Optional[UUID] = Depends(get_user_context)
) -> UUID:
    """Require authenticated user"""
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    return user_id


# Repository Dependencies
async def get_lead_repository(
    session: AsyncSession = Depends(get_database_session),
    event_bus: EventBusIntegration = Depends(get_event_bus_integration)
) -> LeadRepository:
    """Get lead repository instance"""
    return LeadRepository(session, event_bus.get_publisher())


async def get_customer_repository(
    session: AsyncSession = Depends(get_database_session),
    event_bus: EventBusIntegration = Depends(get_event_bus_integration)
) -> CustomerRepository:
    """Get customer repository instance"""
    return CustomerRepository(session, event_bus.get_publisher())


async def get_campaign_repository(
    session: AsyncSession = Depends(get_database_session),
    event_bus: EventBusIntegration = Depends(get_event_bus_integration)
) -> CampaignRepository:
    """Get campaign repository instance"""
    return CampaignRepository(session, event_bus.get_publisher())


# Service Dependencies
async def get_lead_service(
    lead_repo: LeadRepository = Depends(get_lead_repository),
    customer_repo: CustomerRepository = Depends(get_customer_repository)
):
    """Get lead service instance"""
    from .application.services import LeadService
    return LeadService(lead_repo, customer_repo)


async def get_customer_service(
    customer_repo: CustomerRepository = Depends(get_customer_repository)
):
    """Get customer service instance"""
    from .application.services import CustomerService
    return CustomerService(customer_repo)


async def get_campaign_service(
    campaign_repo: CampaignRepository = Depends(get_campaign_repository)
):
    """Get campaign service instance"""
    from .application.services import CampaignService
    return CampaignService(campaign_repo)


# Configuration Dependencies
def get_event_bus_config() -> EventBusConfig:
    """Get event bus configuration"""
    settings = get_settings()
    return EventBusConfig(
        base_url=settings.event_bus_url,
        service_name="domain-repository",
        enable_publishing=settings.enable_event_publishing
    )