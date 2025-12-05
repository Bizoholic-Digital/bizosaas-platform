"""
Startup Integrations for BizOSaaS Brain
Initializes LLM monitoring, Elasticsearch, and all monitoring routes
"""

import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("🚀 BizOSaaS Brain starting up...")

    try:
        # Initialize Elasticsearch
        from config import get_elasticsearch_manager
        es_manager = get_elasticsearch_manager()
        await es_manager.initialize()
        logger.info("✅ Elasticsearch initialized")
    except Exception as e:
        logger.warning(f"⚠️ Elasticsearch initialization failed: {e}")

    try:
        # Initialize smart router
        from smart_llm_router import SmartLLMRouter
        smart_router = SmartLLMRouter()
        logger.info(f"✅ Smart LLM Router initialized with {len(smart_router.providers)} providers")
    except Exception as e:
        logger.warning(f"⚠️ Smart LLM Router initialization failed: {e}")

    logger.info("✅ BizOSaaS Brain startup complete")

    yield

    # Shutdown
    logger.info("🔄 BizOSaaS Brain shutting down...")
    try:
        from config import get_elasticsearch_manager
        es_manager = get_elasticsearch_manager()
        await es_manager.close()
        logger.info("✅ Elasticsearch connections closed")
    except Exception as e:
        logger.warning(f"⚠️ Elasticsearch shutdown warning: {e}")


def include_llm_monitoring_routes(app: FastAPI):
    """Include LLM and monitoring routes in the app"""
    try:
        from llm_monitoring_routes import router as llm_router
        app.include_router(llm_router)
        logger.info("✅ LLM Monitoring routes included at /api/brain/llm/*")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to include LLM monitoring routes: {e}")
        return False


def add_monitoring_endpoints(app: FastAPI):
    """Add global monitoring endpoints"""

    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": "bizosaas-brain",
            "version": "2.0.0",
            "timestamp": "2025-10-06T14:00:00Z"
        }

    @app.get("/metrics")
    async def prometheus_metrics():
        """Prometheus metrics endpoint"""
        try:
            from prometheus_client import generate_latest
            from starlette.responses import Response
            return Response(
                content=generate_latest(),
                media_type="text/plain"
            )
        except Exception as e:
            logger.error(f"Metrics export error: {e}")
            return {"error": "Metrics not available"}

    @app.get("/api/brain/status")
    async def brain_status():
        """Brain API status with all integrations"""
        try:
            from smart_llm_router import SmartLLMRouter
            smart_router = SmartLLMRouter()

            # Count healthy providers
            healthy_count = sum(
                1 for p in smart_router.providers.values()
                if smart_router._calculate_health_score(p.get('name', ''))['is_healthy']
            )

            return {
                "success": True,
                "brain_api": "operational",
                "llm_providers": {
                    "total": len(smart_router.providers),
                    "healthy": healthy_count
                },
                "features": {
                    "smart_routing": True,
                    "rag": True,
                    "monitoring": True,
                    "elasticsearch": True,
                    "prometheus": True
                }
            }
        except Exception as e:
            logger.error(f"Status check error: {e}")
            return {
                "success": False,
                "brain_api": "operational",
                "error": str(e)
            }

    logger.info("✅ Global monitoring endpoints added")
