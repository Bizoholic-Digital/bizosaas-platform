# Elasticsearch + Monitoring Infrastructure Deployment Guide

## Overview

This guide covers deploying the complete monitoring stack for the BizOSaaS Platform, including:
- **Elasticsearch 8.11.0** for RAG document storage and retrieval
- **Kibana 8.11.0** for Elasticsearch visualization
- **Prometheus** for metrics collection
- **Grafana** for dashboards and alerts
- **Node Exporter** for system metrics
- **Elasticsearch Exporter** for Elasticsearch metrics

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     BizOSaaS Platform                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │ FastAPI Brain│─────▶│ Elasticsearch│◀─────│ Cohere API   │ │
│  │   (8001)     │      │   (9200)     │      │  (Rerank)    │ │
│  └──────────────┘      └──────────────┘      └──────────────┘ │
│         │                     │                                 │
│         │                     │                                 │
│         ▼                     ▼                                 │
│  ┌──────────────┐      ┌──────────────┐                       │
│  │  Prometheus  │      │    Kibana    │                       │
│  │   (9090)     │      │   (5601)     │                       │
│  └──────────────┘      └──────────────┘                       │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐                                             │
│  │   Grafana    │                                             │
│  │   (3030)     │                                             │
│  └──────────────┘                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Start Monitoring Infrastructure

```bash
cd /home/alagiri/projects/bizoholic/bizosaas/ai/services/bizosaas-brain

# Start all monitoring services
docker-compose -f docker-compose.monitoring.yml up -d

# Check status
docker-compose -f docker-compose.monitoring.yml ps
```

### 2. Verify Services

**Elasticsearch**: http://localhost:9200
```bash
curl http://localhost:9200/_cluster/health?pretty
```

**Kibana**: http://localhost:5601

**Prometheus**: http://localhost:9090

**Grafana**: http://localhost:3030
- Username: `admin`
- Password: `bizosaas2025`

### 3. Initialize Elasticsearch Indices

```python
from elasticsearch_rag_setup import ElasticsearchRAGManager

# Initialize manager
es_manager = ElasticsearchRAGManager(
    elasticsearch_url="http://localhost:9200",
    index_prefix="bizosaas"
)

# Create indices
await es_manager.initialize()
```

## Elasticsearch Configuration

### Indices Created

1. **bizosaas_documents** - RAG document storage
   - Fields: tenant_id, document_id, title, content, metadata, tags
   - Shards: 3, Replicas: 1
   - Full-text search on title and content

2. **bizosaas_conversations** - Conversation history
   - Fields: tenant_id, conversation_id, message, role, model, cost
   - Shards: 2, Replicas: 1

3. **bizosaas_rag_analytics** - RAG performance metrics
   - Fields: query, latency, success, scores
   - Shards: 2, Replicas: 1

### Document Indexing Example

```python
# Index a document for RAG
await es_manager.index_document(
    tenant_id="tenant-123",
    document_id="doc-001",
    title="Product Documentation",
    content="This is the full product documentation...",
    metadata={
        "author": "John Doe",
        "department": "Engineering"
    },
    document_type="documentation",
    tags=["product", "technical", "v1.0"]
)
```

### Searching Documents

```python
# Search documents
result = await es_manager.search_documents(
    tenant_id="tenant-123",
    query="how to install the product",
    size=10,
    document_type="documentation"
)

# Result includes: documents, total, latency_ms
for doc in result['documents']:
    print(f"{doc['title']}: {doc['score']}")
```

## Cohere + Elasticsearch RAG

### Integration Example

```python
from elasticsearch_rag_setup import CohereElasticsearchRAG

# Create RAG system
rag_system = CohereElasticsearchRAG(
    es_manager=es_manager,
    cohere_api_key="your-cohere-api-key"
)

# Retrieve and rerank
result = await rag_system.retrieve_and_rerank(
    tenant_id="tenant-123",
    query="product installation steps",
    top_k=10,           # Retrieve 10 documents from Elasticsearch
    rerank_top_n=3,     # Rerank top 3 with Cohere
    model="rerank-english-v3.0"
)

# Result includes reranked documents with scores
for doc in result['documents']:
    print(f"{doc['title']}: {doc['rerank_score']:.3f}")
```

### Performance Metrics

The system automatically tracks:
- **Retrieval latency**: Time to search Elasticsearch
- **Rerank latency**: Time to rerank with Cohere
- **Total latency**: End-to-end RAG query time
- **Relevance scores**: Average and top scores
- **Success rate**: Query success/failure rate

## Prometheus Metrics

### LLM Provider Metrics

```promql
# Request rate by provider
rate(llm_requests_total[5m])

# Average response time (p95)
histogram_quantile(0.95, rate(llm_response_time_seconds_bucket[5m]))

# Total cost in last hour
sum(increase(llm_cost_dollars[1h]))

# Cost savings vs GPT-4
(1 - sum(increase(llm_cost_dollars[1h])) / sum(increase(llm_gpt4_equivalent_cost[1h]))) * 100
```

### RAG Metrics

```promql
# RAG query rate
rate(rag_queries_total[5m])

# Average retrieval latency
histogram_quantile(0.95, rate(rag_retrieval_latency_seconds_bucket[5m]))

# Average relevance score
avg(rag_avg_relevance_score)

# Success rate
sum(rate(rag_queries_total{status="success"}[5m])) / sum(rate(rag_queries_total[5m])) * 100
```

### Elasticsearch Metrics

```promql
# Cluster health (0=red, 1=yellow, 2=green)
elasticsearch_cluster_health_status

# Total indexed documents
elasticsearch_indices_docs_total

# Index size
elasticsearch_indices_store_size_bytes

# Query rate
rate(elasticsearch_indices_search_query_total[5m])
```

## Grafana Dashboards

### 1. LLM Provider Performance Dashboard

**URL**: http://localhost:3030/d/llm-performance

**Panels**:
- Request rate by provider
- Response time (p95, p50)
- Success rate
- Cost analysis (total, by provider, savings vs GPT-4)
- Token usage
- Provider health status
- Response time heatmap

### 2. Elasticsearch RAG Dashboard

**URL**: http://localhost:3030/d/elasticsearch-rag

**Panels**:
- RAG query rate
- Retrieval + Rerank latency
- Average relevance score
- Documents retrieved
- Elasticsearch cluster health
- Cohere rerank performance
- Top queries by frequency
- Slowest queries
- Index size breakdown

## Integration with FastAPI Brain

### Add Metrics Endpoint

```python
# In your FastAPI app
from metrics_exporter import metrics_collector
from prometheus_client import generate_latest

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
```

### Track LLM Requests

```python
from metrics_exporter import metrics_collector

@metrics_collector.track_llm_request(
    provider="deepseek",
    task_type="chat",
    tenant_id="tenant-123"
)
async def generate_chat_completion(messages):
    # Your LLM logic here
    result = await deepseek_client.chat(messages)
    return result
```

### Track RAG Queries

```python
@metrics_collector.track_rag_query(tenant_id="tenant-123")
async def search_documents(query):
    # Your RAG logic here
    result = await rag_system.retrieve_and_rerank(
        tenant_id="tenant-123",
        query=query
    )
    return result
```

## Monitoring Best Practices

### 1. Health Checks

Set up automated health checks for all services:

```bash
# Elasticsearch
curl http://localhost:9200/_cluster/health

# Prometheus
curl http://localhost:9090/-/healthy

# Grafana
curl http://localhost:3030/api/health
```

### 2. Alerting Rules

Create Prometheus alerting rules for:

**LLM Provider Issues**:
- Provider success rate < 90%
- Consecutive failures > 3
- Average response time > 5s
- Daily cost > $100

**RAG Performance**:
- RAG query latency > 2s
- Retrieval success rate < 95%
- Elasticsearch cluster health = red

**System Resources**:
- CPU usage > 80%
- Memory usage > 90%
- Disk usage > 85%

### 3. Analytics Export

Elasticsearch analytics are automatically logged for:
- Every RAG query (success/failure, latency, scores)
- Every conversation message (tokens, cost)
- Provider performance (response time, errors)

Query analytics from Elasticsearch:

```python
# Get 7-day analytics summary
summary = await es_manager.get_analytics_summary(
    tenant_id="tenant-123",
    days=7
)

print(f"Total queries: {summary['total_queries']}")
print(f"Avg latency: {summary['avg_latency_ms']:.2f}ms")
print(f"Avg results: {summary['avg_results']:.1f}")
```

## Scaling Considerations

### Elasticsearch Scaling

**Vertical Scaling** (single node):
```yaml
environment:
  - "ES_JAVA_OPTS=-Xms2g -Xmx2g"  # Increase heap size
```

**Horizontal Scaling** (cluster):
```yaml
services:
  elasticsearch-node1:
    environment:
      - cluster.name=bizosaas-cluster
      - node.name=node1
      - discovery.seed_hosts=elasticsearch-node2,elasticsearch-node3

  elasticsearch-node2:
    environment:
      - cluster.name=bizosaas-cluster
      - node.name=node2
      - discovery.seed_hosts=elasticsearch-node1,elasticsearch-node3

  elasticsearch-node3:
    environment:
      - cluster.name=bizosaas-cluster
      - node.name=node3
      - discovery.seed_hosts=elasticsearch-node1,elasticsearch-node2
```

### Index Optimization

**Sharding Strategy**:
- Small indices (<10GB): 1-2 shards
- Medium indices (10-50GB): 3-5 shards
- Large indices (>50GB): 5-10 shards

**Replication**:
- Development: 0-1 replicas
- Production: 1-2 replicas
- High availability: 2+ replicas

## Backup and Recovery

### Elasticsearch Snapshots

```bash
# Configure snapshot repository
curl -X PUT "localhost:9200/_snapshot/bizosaas_backup" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/usr/share/elasticsearch/snapshots"
  }
}
'

# Create snapshot
curl -X PUT "localhost:9200/_snapshot/bizosaas_backup/snapshot_1?wait_for_completion=true"

# Restore snapshot
curl -X POST "localhost:9200/_snapshot/bizosaas_backup/snapshot_1/_restore"
```

### Prometheus Data Retention

Configure in `prometheus.yml`:
```yaml
global:
  scrape_interval: 15s
  storage.tsdb.retention.time: 30d  # Keep 30 days
  storage.tsdb.retention.size: 50GB # Max 50GB
```

## Troubleshooting

### Elasticsearch Issues

**Cluster health is yellow**:
- Check replica settings (may need to reduce replicas for single-node)
- Verify sufficient disk space

**High memory usage**:
- Reduce heap size in `ES_JAVA_OPTS`
- Optimize queries (use filters instead of queries where possible)

**Slow queries**:
- Check index mappings
- Add proper field types (keyword vs text)
- Use query profiling: `?profile=true`

### Grafana Issues

**Dashboards not loading**:
- Verify Prometheus datasource connection
- Check Prometheus is scraping metrics: http://localhost:9090/targets

**No data in graphs**:
- Verify metrics are being exported: http://localhost:8001/metrics
- Check Prometheus query syntax

### Prometheus Issues

**Missing metrics**:
- Verify scrape targets are reachable: http://localhost:9090/targets
- Check firewall rules
- Verify metric naming (use `/metrics` endpoint to see available metrics)

## Production Deployment

### Environment Variables

```bash
# Elasticsearch
ES_JAVA_OPTS=-Xms4g -Xmx4g
ES_CLUSTER_NAME=bizosaas-prod
ES_NODE_NAME=node-prod-1

# Grafana
GF_SECURITY_ADMIN_PASSWORD=<strong-password>
GF_SERVER_DOMAIN=grafana.bizosaas.com
GF_SERVER_ROOT_URL=https://grafana.bizosaas.com

# Prometheus
PROMETHEUS_RETENTION_TIME=90d
PROMETHEUS_RETENTION_SIZE=200GB
```

### SSL/TLS Configuration

**Elasticsearch with SSL**:
```yaml
environment:
  - xpack.security.enabled=true
  - xpack.security.http.ssl.enabled=true
  - xpack.security.transport.ssl.enabled=true
```

**Grafana with SSL**:
```yaml
environment:
  - GF_SERVER_PROTOCOL=https
  - GF_SERVER_CERT_FILE=/etc/grafana/ssl/cert.pem
  - GF_SERVER_CERT_KEY=/etc/grafana/ssl/key.pem
```

### Resource Limits

```yaml
services:
  elasticsearch:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G

  prometheus:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G

  grafana:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 2G
```

## Cost Optimization

### Elasticsearch

1. **Use appropriate shard counts** - Don't over-shard small indices
2. **Enable index lifecycle management (ILM)** - Auto-delete old data
3. **Use frozen indices** - For rarely accessed historical data
4. **Optimize mappings** - Disable unnecessary features

### Prometheus

1. **Adjust scrape intervals** - Use 30s-60s for non-critical metrics
2. **Set retention policies** - Keep only necessary history
3. **Use recording rules** - Pre-compute expensive queries

### Grafana

1. **Use query caching** - Enable dashboard caching
2. **Optimize queries** - Use recording rules for complex queries
3. **Limit concurrent users** - Set up authentication and quotas

## Next Steps

1. **Deploy Infrastructure**:
   ```bash
   docker-compose -f docker-compose.monitoring.yml up -d
   ```

2. **Initialize Elasticsearch**:
   ```python
   await es_manager.initialize()
   ```

3. **Configure Prometheus Scraping**:
   - Add `/metrics` endpoint to FastAPI Brain
   - Verify targets: http://localhost:9090/targets

4. **Access Grafana Dashboards**:
   - Login: http://localhost:3030
   - Explore pre-configured dashboards

5. **Test RAG System**:
   ```python
   # Index sample documents
   # Run test queries
   # Verify metrics in Grafana
   ```

6. **Set Up Alerts**:
   - Configure Prometheus alerting rules
   - Set up notification channels (email, Slack, PagerDuty)

7. **Monitor and Optimize**:
   - Review daily cost metrics
   - Optimize slow queries
   - Adjust resource allocations

## Support and Resources

- **Elasticsearch Docs**: https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
- **Prometheus Docs**: https://prometheus.io/docs/
- **Grafana Docs**: https://grafana.com/docs/
- **Cohere Rerank API**: https://docs.cohere.com/reference/rerank

---

**Deployment Status**: Ready for production deployment
**Infrastructure Components**: 6 services (Elasticsearch, Kibana, Prometheus, Grafana, Node Exporter, ES Exporter)
**Expected Resource Usage**: ~12GB RAM, ~4 CPU cores
**Estimated Cost**: $0 (all open-source)
