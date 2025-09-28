"""
Database setup and configuration for Domain Repository Service

This module provides SQLAlchemy async database setup and session management.
"""

from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
import structlog

from config import get_settings
from domain.base import Base

logger = structlog.get_logger(__name__)


class DatabaseManager:
    """Database manager for handling connections and sessions"""
    
    def __init__(self, database_url: str, echo: bool = False):
        self.database_url = database_url
        self.echo = echo
        self.engine = None
        self.session_factory = None
        
    async def initialize(self) -> None:
        """Initialize database engine and session factory"""
        
        try:
            # Create async engine
            self.engine = create_async_engine(
                self.database_url,
                echo=self.echo,
                poolclass=NullPool,  # Use NullPool for async engines
                pool_pre_ping=True,
                future=True
            )
            
            # Create session factory
            self.session_factory = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=True,
                autocommit=False
            )
            
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize database", error=str(e))
            raise
    
    async def create_tables(self) -> None:
        """Create all database tables"""
        
        if not self.engine:
            raise RuntimeError("Database engine not initialized")
        
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            logger.info("Database tables created successfully")
            
        except Exception as e:
            logger.error("Failed to create database tables", error=str(e))
            raise
    
    async def drop_tables(self) -> None:
        """Drop all database tables (for testing)"""
        
        if not self.engine:
            raise RuntimeError("Database engine not initialized")
        
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            
            logger.info("Database tables dropped successfully")
            
        except Exception as e:
            logger.error("Failed to drop database tables", error=str(e))
            raise
    
    async def get_session(self) -> AsyncSession:
        """Get a new database session"""
        
        if not self.session_factory:
            raise RuntimeError("Session factory not initialized")
        
        return self.session_factory()
    
    async def close(self) -> None:
        """Close database connections"""
        
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connections closed")


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


async def get_database_manager() -> DatabaseManager:
    """Get the global database manager instance"""
    global _db_manager
    
    if _db_manager is None:
        settings = get_settings()
        _db_manager = DatabaseManager(
            database_url=settings.database_url,
            echo=settings.database_echo
        )
        await _db_manager.initialize()
    
    return _db_manager


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session (dependency injection)"""
    
    db_manager = await get_database_manager()
    session = await db_manager.get_session()
    
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def init_database() -> None:
    """Initialize database for the application"""
    
    try:
        db_manager = await get_database_manager()
        await db_manager.create_tables()
        
        logger.info("Database initialization completed")
        
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))
        raise


async def close_database() -> None:
    """Close database connections"""
    
    global _db_manager
    
    if _db_manager:
        await _db_manager.close()
        _db_manager = None


# Health check for database
async def check_database_health() -> bool:
    """Check if database is healthy"""
    
    try:
        db_manager = await get_database_manager()
        
        async with await db_manager.get_session() as session:
            # Simple query to check connectivity
            result = await session.execute("SELECT 1")
            return result.scalar() == 1
            
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return False


# Database utilities for testing
async def reset_database_for_testing() -> None:
    """Reset database for testing (drops and recreates all tables)"""
    
    try:
        db_manager = await get_database_manager()
        await db_manager.drop_tables()
        await db_manager.create_tables()
        
        logger.info("Database reset for testing completed")
        
    except Exception as e:
        logger.error("Database reset failed", error=str(e))
        raise


async def create_test_data() -> None:
    """Create sample test data for development"""
    
    from uuid import UUID
    from datetime import datetime
    from decimal import Decimal
    
    from domain.aggregates.lead import Lead, LeadSource, ContactInfo
    from domain.aggregates.customer import Customer, CustomerProfile, CustomerType
    from domain.aggregates.campaign import Campaign, CampaignType, CampaignObjective, CampaignBudget, CampaignSchedule
    from infrastructure.repositories import LeadRepository, CustomerRepository, CampaignRepository
    from infrastructure.event_bus_integration import EventBusIntegration, EventBusConfig
    
    try:
        # Initialize event bus (disabled for test data creation)
        event_bus_config = EventBusConfig(enable_publishing=False)
        async with EventBusIntegration(event_bus_config) as event_bus:
            
            db_manager = await get_database_manager()
            async with await db_manager.get_session() as session:
                
                # Create repositories
                lead_repo = LeadRepository(session, event_bus.get_publisher())
                customer_repo = CustomerRepository(session, event_bus.get_publisher())
                campaign_repo = CampaignRepository(session, event_bus.get_publisher())
                
                tenant_id = UUID("00000000-0000-4000-8000-000000000001")
                
                # Create sample lead
                lead_contact = ContactInfo(
                    email="john.doe@example.com",
                    first_name="John",
                    last_name="Doe",
                    company="Example Corp",
                    job_title="Marketing Manager"
                )
                
                sample_lead = Lead(
                    tenant_id=tenant_id,
                    contact_info=lead_contact,
                    source=LeadSource.WEBSITE_FORM,
                    utm_parameters={
                        "utm_source": "google",
                        "utm_medium": "cpc",
                        "utm_campaign": "test_campaign"
                    }
                )
                
                await lead_repo.save(sample_lead)
                
                # Create sample customer
                customer_profile = CustomerProfile(
                    email="jane.smith@example.com",
                    first_name="Jane",
                    last_name="Smith",
                    company_name="Smith Industries",
                    industry="Technology"
                )
                
                sample_customer = Customer(
                    tenant_id=tenant_id,
                    profile=customer_profile,
                    customer_type=CustomerType.SMALL_BUSINESS
                )
                
                await customer_repo.save(sample_customer)
                
                # Create sample campaign
                campaign_budget = CampaignBudget(
                    total_budget=Decimal("5000.00"),
                    daily_budget=Decimal("100.00")
                )
                
                campaign_schedule = CampaignSchedule(
                    start_date=datetime.utcnow(),
                    end_date=None
                )
                
                sample_campaign = Campaign(
                    tenant_id=tenant_id,
                    name="Test Marketing Campaign",
                    description="A sample campaign for testing",
                    campaign_type=CampaignType.EMAIL,
                    objective=CampaignObjective.LEAD_GENERATION,
                    budget=campaign_budget,
                    schedule=campaign_schedule
                )
                
                await campaign_repo.save(sample_campaign)
                
                await session.commit()
                
        logger.info("Test data created successfully")
        
    except Exception as e:
        logger.error("Failed to create test data", error=str(e))
        raise