"""
Prometheus Metrics Exporter for BizOSaaS Platform
Exports LLM provider metrics, RAG analytics, and system performance
"""

from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest
from typing import Dict, Any
import time
from functools import wraps


# LLM Provider Metrics
llm_requests_total = Counter(
    'llm_requests_total',
    'Total LLM requests',
    ['provider', 'task_type', 'status', 'tenant_id']
)

llm_response_time_seconds = Histogram(
    'llm_response_time_seconds',
    'LLM response time in seconds',
    ['provider', 'task_type'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

llm_tokens_total = Counter(
    'llm_tokens_total',
    'Total tokens processed',
    ['provider', 'task_type', 'token_type']  # token_type: input, output
)

llm_cost_dollars = Counter(
    'llm_cost_dollars',
    'Total cost in USD',
    ['provider', 'task_type', 'tenant_id']
)

llm_gpt4_equivalent_cost = Counter(
    'llm_gpt4_equivalent_cost',
    'Equivalent GPT-4 cost for comparison',
    ['provider', 'task_type', 'tenant_id']
)

llm_provider_health = Gauge(
    'llm_provider_health',
    'Provider health status (1=healthy, 0=unhealthy)',
    ['provider', 'success_rate', 'avg_response_time']
)

llm_consecutive_failures = Gauge(
    'llm_consecutive_failures',
    'Consecutive failures for provider',
    ['provider']
)

# RAG Metrics
rag_queries_total = Counter(
    'rag_queries_total',
    'Total RAG queries',
    ['tenant_id', 'status']
)

rag_retrieval_latency_seconds = Histogram(
    'rag_retrieval_latency_seconds',
    'RAG retrieval latency in seconds',
    ['provider'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0]
)

rag_rerank_latency_seconds = Histogram(
    'rag_rerank_latency_seconds',
    'RAG rerank latency in seconds',
    ['provider'],
    buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0]
)

rag_total_latency_seconds = Histogram(
    'rag_total_latency_seconds',
    'Total RAG latency in seconds',
    buckets=[0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
)

rag_documents_retrieved = Histogram(
    'rag_documents_retrieved',
    'Number of documents retrieved',
    buckets=[1, 3, 5, 10, 20, 50, 100]
)

rag_avg_relevance_score = Gauge(
    'rag_avg_relevance_score',
    'Average relevance score',
    ['tenant_id']
)

rag_top_relevance_score = Gauge(
    'rag_top_relevance_score',
    'Top relevance score',
    ['tenant_id']
)

# Elasticsearch Metrics
elasticsearch_cluster_health_status = Gauge(
    'elasticsearch_cluster_health_status',
    'Elasticsearch cluster health (0=red, 1=yellow, 2=green)'
)

elasticsearch_indices_docs_total = Gauge(
    'elasticsearch_indices_docs_total',
    'Total documents in Elasticsearch',
    ['index']
)

elasticsearch_indices_store_size_bytes = Gauge(
    'elasticsearch_indices_store_size_bytes',
    'Index store size in bytes',
    ['index']
)

elasticsearch_indices_search_query_total = Counter(
    'elasticsearch_indices_search_query_total',
    'Total search queries',
    ['index']
)

# Cohere Specific Metrics
cohere_rerank_requests_total = Counter(
    'cohere_rerank_requests_total',
    'Total Cohere rerank requests',
    ['tenant_id', 'status']
)

cohere_rerank_latency_seconds = Histogram(
    'cohere_rerank_latency_seconds',
    'Cohere rerank latency in seconds',
    buckets=[0.1, 0.25, 0.5, 1.0, 2.0, 5.0]
)

cohere_embedding_requests_total = Counter(
    'cohere_embedding_requests_total',
    'Total Cohere embedding requests',
    ['tenant_id', 'model']
)

# System Metrics
bizosaas_info = Info(
    'bizosaas_platform',
    'BizOSaaS Platform information'
)


class MetricsCollector:
    """Collects and exports metrics for Prometheus"""

    def __init__(self):
        self.start_time = time.time()
        bizosaas_info.info({
            'version': '1.0.0',
            'environment': 'production',
            'llm_providers': '12'
        })

    def track_llm_request(self, provider: str, task_type: str, tenant_id: str):
        """Decorator to track LLM requests"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                status = 'success'

                try:
                    result = await func(*args, **kwargs)

                    # Extract metrics from result
                    if isinstance(result, dict):
                        # Track tokens
                        if 'usage' in result:
                            usage = result['usage']
                            if 'prompt_tokens' in usage:
                                llm_tokens_total.labels(
                                    provider=provider,
                                    task_type=task_type,
                                    token_type='input'
                                ).inc(usage['prompt_tokens'])
                            if 'completion_tokens' in usage:
                                llm_tokens_total.labels(
                                    provider=provider,
                                    task_type=task_type,
                                    token_type='output'
                                ).inc(usage['completion_tokens'])

                        # Track cost
                        if 'cost_analysis' in result:
                            cost = result['cost_analysis'].get('total_cost', 0)
                            llm_cost_dollars.labels(
                                provider=provider,
                                task_type=task_type,
                                tenant_id=tenant_id
                            ).inc(cost)

                            # Track GPT-4 equivalent cost
                            gpt4_cost = result['cost_analysis'].get('gpt4_equivalent_cost', 0)
                            if gpt4_cost > 0:
                                llm_gpt4_equivalent_cost.labels(
                                    provider=provider,
                                    task_type=task_type,
                                    tenant_id=tenant_id
                                ).inc(gpt4_cost)

                    return result

                except Exception as e:
                    status = 'error'
                    raise

                finally:
                    # Track request
                    llm_requests_total.labels(
                        provider=provider,
                        task_type=task_type,
                        status=status,
                        tenant_id=tenant_id
                    ).inc()

                    # Track response time
                    duration = time.time() - start_time
                    llm_response_time_seconds.labels(
                        provider=provider,
                        task_type=task_type
                    ).observe(duration)

            return wrapper
        return decorator

    def track_rag_query(self, tenant_id: str):
        """Decorator to track RAG queries"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                status = 'success'

                try:
                    result = await func(*args, **kwargs)

                    if isinstance(result, dict) and result.get('success'):
                        # Track retrieval latency
                        if 'retrieval_latency_ms' in result:
                            rag_retrieval_latency_seconds.labels(
                                provider='elasticsearch'
                            ).observe(result['retrieval_latency_ms'] / 1000)

                        # Track rerank latency
                        if 'rerank_latency_ms' in result:
                            rag_rerank_latency_seconds.labels(
                                provider='cohere'
                            ).observe(result['rerank_latency_ms'] / 1000)

                        # Track total latency
                        if 'total_latency_ms' in result:
                            rag_total_latency_seconds.observe(
                                result['total_latency_ms'] / 1000
                            )

                        # Track documents retrieved
                        if 'documents' in result:
                            rag_documents_retrieved.observe(len(result['documents']))

                            # Track relevance scores
                            if result['documents']:
                                scores = [d.get('rerank_score', 0) for d in result['documents']]
                                if scores:
                                    rag_avg_relevance_score.labels(
                                        tenant_id=tenant_id
                                    ).set(sum(scores) / len(scores))
                                    rag_top_relevance_score.labels(
                                        tenant_id=tenant_id
                                    ).set(max(scores))
                    else:
                        status = 'error'

                    return result

                except Exception as e:
                    status = 'error'
                    raise

                finally:
                    # Track query
                    rag_queries_total.labels(
                        tenant_id=tenant_id,
                        status=status
                    ).inc()

            return wrapper
        return decorator

    def update_provider_health(self, provider: str, success_rate: float, avg_response_time: float):
        """Update provider health metrics"""
        health_status = 1 if success_rate >= 0.90 else 0
        llm_provider_health.labels(
            provider=provider,
            success_rate=f"{success_rate:.2f}",
            avg_response_time=f"{avg_response_time:.2f}"
        ).set(health_status)

    def update_consecutive_failures(self, provider: str, failures: int):
        """Update consecutive failure count"""
        llm_consecutive_failures.labels(provider=provider).set(failures)

    def update_elasticsearch_health(self, status: str):
        """Update Elasticsearch cluster health"""
        status_map = {'red': 0, 'yellow': 1, 'green': 2}
        elasticsearch_cluster_health_status.set(status_map.get(status, 0))

    def update_elasticsearch_index_stats(self, index: str, doc_count: int, size_bytes: int):
        """Update Elasticsearch index statistics"""
        elasticsearch_indices_docs_total.labels(index=index).set(doc_count)
        elasticsearch_indices_store_size_bytes.labels(index=index).set(size_bytes)

    def track_elasticsearch_query(self, index: str):
        """Track Elasticsearch query"""
        elasticsearch_indices_search_query_total.labels(index=index).inc()

    def track_cohere_rerank(self, tenant_id: str):
        """Decorator to track Cohere rerank requests"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                status = 'success'

                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    status = 'error'
                    raise
                finally:
                    cohere_rerank_requests_total.labels(
                        tenant_id=tenant_id,
                        status=status
                    ).inc()

                    duration = time.time() - start_time
                    cohere_rerank_latency_seconds.observe(duration)

            return wrapper
        return decorator

    def export_metrics(self) -> bytes:
        """Export metrics in Prometheus format"""
        return generate_latest()


# Global metrics collector instance
metrics_collector = MetricsCollector()
