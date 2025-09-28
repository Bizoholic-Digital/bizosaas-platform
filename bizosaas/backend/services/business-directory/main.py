"""
Business Directory Service - FastAPI Application
Main application entry point for the Business Directory microservice
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import structlog
import asyncio
from datetime import datetime

from .core.config import settings
from .core.database import init_db, cleanup_db, check_db_health
from .core.security import cleanup_security, check_security_health
from .services import search_service
from .api import businesses_router, categories_router, google_integration_router, multi_platform_api
from .schemas import HealthCheckSchema, ErrorSchema

# Import platform clients to register them
import services.platforms  # This registers all platform clients

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

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Business Directory Service", version=settings.APP_VERSION)
    
    try:
        # Initialize database
        await init_db()
        logger.info("Database initialized successfully")
        
        # Initialize search service
        await search_service.initialize()
        logger.info("Search service initialized successfully")
        
        # Service is ready
        logger.info("Business Directory Service started successfully", port=settings.PORT)
        
    except Exception as e:
        logger.error("Failed to start Business Directory Service", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Business Directory Service")
    
    try:
        # Cleanup database connections
        await cleanup_db()
        
        # Cleanup security resources
        await cleanup_security()
        
        # Cleanup search service
        await search_service.cleanup()
        
        logger.info("Business Directory Service shutdown completed")
        
    except Exception as e:
        logger.error("Error during shutdown", error=str(e))


# Create FastAPI application
app = FastAPI(
    **settings.get_docs_config(),
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["bizosaas.com", "*.bizosaas.com", "localhost"]
    )


# Global exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(
        "Unhandled exception",
        error=str(exc),
        path=request.url.path,
        method=request.method
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorSchema(
            error="Internal server error",
            detail="An unexpected error occurred"
        ).dict()
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorSchema(
            error="Validation error",
            detail=str(exc)
        ).dict()
    )


# Health check endpoints
@app.get(
    "/health",
    response_model=HealthCheckSchema,
    tags=["Health"],
    summary="Health Check",
    description="Check service health and dependencies"
)
async def health_check():
    """Comprehensive health check"""
    try:
        # Check database health
        db_health = await check_db_health()
        
        # Check security components health
        security_health = await check_security_health()
        
        # Determine overall status
        overall_status = "healthy"
        if (db_health.get("database") != "healthy" or 
            security_health.get("redis") != "healthy"):
            overall_status = "unhealthy"
        
        # Combine dependency statuses
        dependencies = {
            "database": db_health.get("database", "unknown"),
            "redis": security_health.get("redis", "unknown"),
            "search_service": "healthy" if search_service._model_loaded else "initializing"
        }
        
        return HealthCheckSchema(
            status=overall_status,
            version=settings.APP_VERSION,
            dependencies=dependencies,
            performance=db_health.get("performance")
        )
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return HealthCheckSchema(
            status="unhealthy",
            version=settings.APP_VERSION,
            dependencies={"error": str(e)}
        )


@app.get(
    "/ready",
    tags=["Health"],
    summary="Readiness Check",
    description="Check if service is ready to handle requests"
)
async def readiness_check():
    """Readiness probe for Kubernetes"""
    try:
        # Quick database connectivity check
        db_health = await check_db_health()
        
        if db_health.get("connection", False):
            return {"status": "ready"}
        else:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "not ready", "reason": "database not available"}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "reason": str(e)}
        )


@app.get(
    "/live",
    tags=["Health"],
    summary="Liveness Check",
    description="Check if service is alive"
)
async def liveness_check():
    """Liveness probe for Kubernetes"""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}


# Service information endpoint
@app.get(
    "/info",
    tags=["Service"],
    summary="Service Information",
    description="Get service information and configuration"
)
async def service_info():
    """Get service information"""
    return {
        "service": "Business Directory Service",
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "environment": settings.ENVIRONMENT,
        "api_prefix": settings.get_api_prefix(),
        "features": {
            "ai_search": bool(settings.OPENAI_API_KEY),
            "vector_search": True,
            "geospatial_search": True,
            "multi_tenant": True,
            "rate_limiting": True,
            "caching": True
        },
        "limits": {
            "max_page_size": settings.MAX_PAGE_SIZE,
            "default_page_size": settings.DEFAULT_PAGE_SIZE,
            "max_file_size": settings.MAX_FILE_SIZE,
            "rate_limit_per_minute": settings.RATE_LIMIT_REQUESTS_PER_MINUTE
        }
    }


# Include API routers
app.include_router(
    businesses_router,
    prefix=settings.get_api_prefix(),
    tags=["Business Directory"]
)

app.include_router(
    categories_router,
    prefix=settings.get_api_prefix(),
    tags=["Business Directory"]
)

app.include_router(
    google_integration_router,
    prefix=settings.get_api_prefix(),
    tags=["Google Business Profile"]
)

# Multi-Platform Directory Sync API
app.include_router(
    multi_platform_api.router,
    tags=["Multi-Platform Directory Sync"]
)


# Metrics endpoint (if enabled)
if settings.ENABLE_METRICS:
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    
    @app.get("/metrics", tags=["Monitoring"])
    async def metrics():
        """Prometheus metrics endpoint"""
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Custom middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    start_time = asyncio.get_event_loop().time()
    
    # Log request
    logger.info(
        "Request started",
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host
    )
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = asyncio.get_event_loop().time() - start_time
    
    # Log response
    logger.info(
        "Request completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        process_time=f"{process_time:.4f}s"
    )
    
    # Add timing header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Root endpoint
@app.get(
    "/",
    tags=["Root"],
    summary="Service Root",
    description="Business Directory Service root endpoint"
)
async def root():
    """Root endpoint"""
    return {
        "service": "BizOSaaS Business Directory Service",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs_url": "/docs" if not settings.is_production else None,
        "api_prefix": settings.get_api_prefix(),
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )