"""
Main FastAPI application for Domain Repository Service

This module provides the main FastAPI application with all routes,
middleware, and initialization logic.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog
import uvicorn

from config import get_settings
from database import init_database, close_database, get_database_manager, create_test_data
from infrastructure.event_bus_integration import EventBusIntegration, EventBusConfig
from infrastructure.repositories import LeadRepository, CustomerRepository, CampaignRepository
from application.services import DomainRepositoryService
from api.dependencies import set_domain_service, set_event_bus_integration, set_database_session
from api.routers import lead_router, customer_router, campaign_router, health_router
from api.models import ErrorResponse

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    
    settings = get_settings()
    
    try:
        logger.info("Starting Domain Repository Service", version=settings.version)
        
        # Initialize database
        await init_database()
        logger.info("Database initialized")
        
        # Initialize event bus integration
        event_bus_config = EventBusConfig(
            base_url=settings.event_bus_url,
            service_name="domain-repository",
            enable_publishing=settings.enable_event_publishing
        )
        
        event_bus_integration = EventBusIntegration(event_bus_config)
        await event_bus_integration.start()
        logger.info("Event Bus integration initialized")
        
        # Initialize repositories and services
        db_manager = await get_database_manager()
        session = await db_manager.get_session()
        
        lead_repository = LeadRepository(session, event_bus_integration.get_publisher())
        customer_repository = CustomerRepository(session, event_bus_integration.get_publisher())
        campaign_repository = CampaignRepository(session, event_bus_integration.get_publisher())
        
        domain_service = DomainRepositoryService(
            lead_repository=lead_repository,
            customer_repository=customer_repository,
            campaign_repository=campaign_repository
        )
        
        # Set dependencies
        set_domain_service(domain_service)
        set_event_bus_integration(event_bus_integration)
        set_database_session(session)
        
        # Create test data in development
        if settings.environment == "development":
            try:
                await create_test_data()
                logger.info("Test data created")
            except Exception as e:
                logger.warning("Failed to create test data", error=str(e))
        
        logger.info("Domain Repository Service started successfully")
        
        yield
        
    except Exception as e:
        logger.error("Failed to start Domain Repository Service", error=str(e))
        raise
    finally:
        # Cleanup
        try:
            await event_bus_integration.stop()
            await close_database()
            logger.info("Domain Repository Service stopped")
        except Exception as e:
            logger.error("Error during cleanup", error=str(e))


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description="Domain Repository Service for BizOSaaS Platform - Manages business domain aggregates with DDD patterns",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    # Add routers
    app.include_router(health_router)
    app.include_router(lead_router, prefix="/api/v1")
    app.include_router(customer_router, prefix="/api/v1")
    app.include_router(campaign_router, prefix="/api/v1")
    
    return app


# Create the FastAPI app
app = create_app()


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="HTTP_EXCEPTION",
            message=exc.detail
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    
    logger.error(
        "Unhandled exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="INTERNAL_SERVER_ERROR",
            message="An internal server error occurred"
        ).dict()
    )


# Root endpoint
@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint with service information"""
    
    settings = get_settings()
    
    return {
        "service": settings.app_name,
        "version": settings.version,
        "status": "healthy",
        "environment": settings.environment,
        "docs_url": "/docs" if settings.debug else None,
        "redoc_url": "/redoc" if settings.debug else None,
        "api_endpoints": {
            "leads": "/api/v1/leads",
            "customers": "/api/v1/customers",
            "campaigns": "/api/v1/campaigns",
            "health": "/health"
        },
        "features": {
            "domain_driven_design": True,
            "event_bus_integration": True,
            "multi_tenant_support": True,
            "optimistic_concurrency": True,
            "business_rule_enforcement": True
        }
    }


# Health check endpoint (simplified version at root level)
@app.get("/health")
async def simple_health_check():
    """Simple health check endpoint"""
    
    try:
        from database import check_database_health
        
        db_healthy = await check_database_health()
        
        return {
            "status": "healthy" if db_healthy else "degraded",
            "database": "healthy" if db_healthy else "unhealthy",
            "timestamp": "2025-01-10T00:00:00Z"  # Will be replaced with actual timestamp
        }
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


if __name__ == "__main__":
    settings = get_settings()
    
    # Configure logging based on environment
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": settings.log_level,
            "handlers": ["default"],
        },
    }
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload and settings.debug,
        log_config=log_config,
        access_log=settings.debug,
        workers=1  # Single worker for async app with shared state
    )