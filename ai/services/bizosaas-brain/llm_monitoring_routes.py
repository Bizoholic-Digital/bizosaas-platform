"""
LLM Monitoring Routes for BizOSaaS Brain API Gateway
Provides centralized endpoints for all LLM and monitoring functionality
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import logging

from metrics_exporter import metrics_collector
from smart_llm_router import SmartLLMRouter, TaskType, BudgetTier, Region
from routing_analytics import RoutingAnalytics
from elasticsearch_rag_setup import ElasticsearchRAGManager, CohereElasticsearchRAG

# Initialize router
router = APIRouter(prefix="/api/brain/llm", tags=["LLM & Monitoring"])
logger = logging.getLogger(__name__)

# Initialize components
smart_router = SmartLLMRouter()
routing_analytics = RoutingAnalytics()


# ==================== REQUEST MODELS ====================

class ChatCompletionRequest(BaseModel):
    tenant_id: str
    messages: List[Dict[str, str]]
    task_type: str = "chat"
    budget_tier: str = "medium"
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000


class RAGQueryRequest(BaseModel):
    tenant_id: str
    query: str
    top_k: int = 10
    rerank_top_n: int = 3
    document_type: Optional[str] = None
    tags: Optional[List[str]] = None


class DocumentIndexRequest(BaseModel):
    tenant_id: str
    document_id: str
    title: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    document_type: str = "general"
    source: str = "manual"
    tags: Optional[List[str]] = None


# ==================== LLM ROUTING ENDPOINTS ====================

@router.post("/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    """
    Smart LLM chat completion with automatic provider routing
    Routes through /api/brain/llm/chat/completions
    """
    try:
        # Get routing decision
        routing_decision = await smart_router.route_request(
            task_type=TaskType(request.task_type),
            budget=BudgetTier(request.budget_tier),
            context_size=sum(len(m.get('content', '')) for m in request.messages),
            region=Region.GLOBAL
        )

        provider = routing_decision['primary_provider']
        logger.info(f"Routing chat request to provider: {provider}")

        # Import the appropriate provider
        result = await _execute_provider_request(
            provider=provider,
            tenant_id=request.tenant_id,
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        # Log routing decision
        routing_analytics.log_routing_decision(
            tenant_id=request.tenant_id,
            task_type=request.task_type,
            selected_provider=provider,
            routing_reason=routing_decision['routing_strategy'],
            success=True
        )

        return {
            "success": True,
            "provider": provider,
            "routing_decision": routing_decision,
            "result": result
        }

    except Exception as e:
        logger.error(f"Chat completion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers/health")
async def get_providers_health():
    """
    Get health status of all LLM providers
    Routes through /api/brain/llm/providers/health
    """
    try:
        health_status = {}

        for provider_name, provider_data in smart_router.providers.items():
            health_metrics = smart_router._calculate_health_score(provider_name)

            health_status[provider_name] = {
                "name": provider_data.get("name"),
                "status": "healthy" if health_metrics['is_healthy'] else "unhealthy",
                "success_rate": health_metrics['success_rate'],
                "avg_response_time": health_metrics['avg_response_time'],
                "consecutive_failures": health_metrics['consecutive_failures'],
                "cost_per_million": provider_data.get("cost_per_million_tokens"),
                "capabilities": provider_data.get("capabilities", [])
            }

        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "providers": health_status
        }

    except Exception as e:
        logger.error(f"Provider health check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/routing/analytics")
async def get_routing_analytics(
    tenant_id: Optional[str] = None,
    days: int = 7
):
    """
    Get routing analytics and recommendations
    Routes through /api/brain/llm/routing/analytics
    """
    try:
        # Get analytics summary
        summary = routing_analytics.get_summary(days=days)

        # Get recommendations
        recommendations = routing_analytics.generate_recommendations()

        # Filter by tenant if specified
        if tenant_id:
            summary = routing_analytics.get_tenant_summary(tenant_id, days)

        return {
            "success": True,
            "period_days": days,
            "tenant_id": tenant_id,
            "summary": summary,
            "recommendations": recommendations
        }

    except Exception as e:
        logger.error(f"Routing analytics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/costs/summary")
async def get_cost_summary(
    tenant_id: Optional[str] = None,
    days: int = 30
):
    """
    Get cost summary and savings analysis
    Routes through /api/brain/llm/costs/summary
    """
    try:
        cost_data = routing_analytics.get_cost_summary(
            tenant_id=tenant_id,
            days=days
        )

        return {
            "success": True,
            "period_days": days,
            "tenant_id": tenant_id,
            **cost_data
        }

    except Exception as e:
        logger.error(f"Cost summary error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== RAG ENDPOINTS ====================

@router.post("/rag/query")
async def query_rag_documents(request: RAGQueryRequest):
    """
    Query documents with RAG (Elasticsearch + Cohere rerank)
    Routes through /api/brain/llm/rag/query
    """
    try:
        # Initialize RAG system (should be initialized once at startup)
        from config import get_elasticsearch_manager, get_cohere_api_key

        es_manager = get_elasticsearch_manager()
        cohere_key = get_cohere_api_key()

        rag_system = CohereElasticsearchRAG(
            es_manager=es_manager,
            cohere_api_key=cohere_key
        )

        # Execute RAG query
        result = await rag_system.retrieve_and_rerank(
            tenant_id=request.tenant_id,
            query=request.query,
            top_k=request.top_k,
            rerank_top_n=request.rerank_top_n
        )

        return {
            "success": True,
            "tenant_id": request.tenant_id,
            **result
        }

    except Exception as e:
        logger.error(f"RAG query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rag/documents")
async def index_document(request: DocumentIndexRequest):
    """
    Index a document for RAG retrieval
    Routes through /api/brain/llm/rag/documents
    """
    try:
        from config import get_elasticsearch_manager

        es_manager = get_elasticsearch_manager()

        result = await es_manager.index_document(
            tenant_id=request.tenant_id,
            document_id=request.document_id,
            title=request.title,
            content=request.content,
            metadata=request.metadata,
            document_type=request.document_type,
            source=request.source,
            tags=request.tags
        )

        return {
            "success": True,
            "tenant_id": request.tenant_id,
            **result
        }

    except Exception as e:
        logger.error(f"Document indexing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rag/analytics")
async def get_rag_analytics(
    tenant_id: Optional[str] = None,
    days: int = 7
):
    """
    Get RAG performance analytics
    Routes through /api/brain/llm/rag/analytics
    """
    try:
        from config import get_elasticsearch_manager

        es_manager = get_elasticsearch_manager()

        if tenant_id:
            summary = await es_manager.get_analytics_summary(
                tenant_id=tenant_id,
                days=days
            )
        else:
            # Get platform-wide analytics
            summary = await es_manager.get_analytics_summary(
                tenant_id="*",
                days=days
            )

        return {
            "success": True,
            "period_days": days,
            "tenant_id": tenant_id,
            **summary
        }

    except Exception as e:
        logger.error(f"RAG analytics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== MONITORING ENDPOINTS ====================

@router.get("/metrics")
async def get_prometheus_metrics():
    """
    Prometheus metrics endpoint
    Routes through /api/brain/llm/metrics
    """
    from prometheus_client import generate_latest
    from starlette.responses import Response

    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )


@router.get("/monitoring/dashboard")
async def get_monitoring_dashboard(
    tenant_id: Optional[str] = None,
    hours: int = 24
):
    """
    Get monitoring dashboard data
    Routes through /api/brain/llm/monitoring/dashboard
    """
    try:
        # Get provider health
        health_response = await get_providers_health()

        # Get routing analytics
        analytics_response = await get_routing_analytics(tenant_id, days=1)

        # Get cost summary
        cost_response = await get_cost_summary(tenant_id, days=1)

        # Get RAG analytics
        rag_response = await get_rag_analytics(tenant_id, days=1)

        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "period_hours": hours,
            "tenant_id": tenant_id,
            "provider_health": health_response['providers'],
            "routing_analytics": analytics_response['summary'],
            "cost_summary": cost_response,
            "rag_analytics": rag_response,
            "recommendations": analytics_response['recommendations']
        }

    except Exception as e:
        logger.error(f"Monitoring dashboard error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== HELPER FUNCTIONS ====================

async def _execute_provider_request(
    provider: str,
    tenant_id: str,
    messages: List[Dict[str, str]],
    temperature: float,
    max_tokens: int
) -> Dict[str, Any]:
    """Execute request with specific provider"""

    # Import provider modules dynamically
    provider_module_map = {
        "deepseek": "deepseek_api_integration",
        "mistral": "mistral_api_integration",
        "cohere": "cohere_api_integration",
        "openrouter": "openrouter_integration",
        "anthropic": "anthropic_integration",
        "openai": "openai_integration",
        "gemini": "gemini_integration",
        "bedrock": "amazon_bedrock_integration",
        "azure-openai": "azure_openai_integration",
        "vertex-ai": "google_vertex_ai_integration",
        "perplexity": "perplexity_api_integration",
        "huggingface": "huggingface_inference_integration"
    }

    module_name = provider_module_map.get(provider)
    if not module_name:
        raise ValueError(f"Unknown provider: {provider}")

    # Import and execute
    module = __import__(module_name)

    # Get the chat agent class (convention: {Provider}ChatAgent)
    provider_name = provider.replace("-", "").title().replace("Ai", "AI")
    agent_class_name = f"{provider_name}ChatAgent"
    agent_class = getattr(module, agent_class_name)

    # Initialize agent (requires API key from config)
    from config import get_provider_api_key
    api_key = get_provider_api_key(provider)

    agent = agent_class(api_key=api_key)

    # Execute with metrics tracking
    @metrics_collector.track_llm_request(
        provider=provider,
        task_type="chat",
        tenant_id=tenant_id
    )
    async def execute():
        return await agent.generate_completion(
            tenant_id=tenant_id,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

    result = await execute()
    return result
