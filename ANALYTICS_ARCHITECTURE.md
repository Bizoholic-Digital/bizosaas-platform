# Analytics Architecture Strategy

## Question
*Should we use Redis Streams or ELK for the Analytics tab?*

## Recommendation: Redis Streams + Postgres (Aggregated)

For the **Client Portal Analytics Tab** (Traffic, Conversions, Performance), we recommend using **Redis Streams** for ingestion and **Postgres** for storage of aggregated metrics.

### Why not ELK?
*   **Resource Heavy**: ELK (Elasticsearch, Logstash, Kibana) requires significant RAM (4GB+ min for stability).
*   **Complexity**: Managing ES indices and shards is complex for a "SaaS Dashboard" use case.
*   **Use Case Mismatch**: ELK is best for *unstructured logs* and *full-text search*. Business metrics (e.g., "Daily Visitors = 500") are better stored in a structured relational DB.

### Why Redis Streams?
*   **High Throughput**: Can handle thousands of events/sec with sub-millisecond latency.
*   **Decoupled**: The API (Gateway) just pushes an event to Redis and responds immediately. It doesn't wait for DB writes.
*   **Scalable**: You can add more workers to process the stream as traffic grows.

### Proposed Data Flow

1.  **Ingestion Layer (Brain Gateway)**
    *   Endpoint: `POST /api/analytics/event`
    *   Action: Validates request -> Pushes JSON to Redis Stream `events:analytics`.
    *   Latency: < 10ms.

2.  **Processing Layer (Temporal Worker)**
    *   Trigger: Periodically (e.g., every 1 min) or Continuous Consumer.
    *   Action: Reads X events from Redis Stream.
    *   Logic: Aggregates data in memory (e.g., increments `visitor_count` for `tenant_id=X` at `hour=Y`).
    *   Write: Updates the `analytics_daily_metrics` table in Postgres.

3.  **Storage Layer (Postgres)**
    *   Table: `analytics_metrics`
    *   Columns: `tenant_id`, `metric_type`, `value`, `timestamp`, `dimension` (e.g., 'mobile', 'USA').
    *   Indexing: Optimized for time-range queries.

4.  **Presentation Layer (Client Portal)**
    *   Component: `<AnalyticsChart />`
    *   API Call: `GET /api/analytics?from=...&to=...`
    *   Library: `recharts` for slicing/dicing visuals.

### Future Scale
If Postgres becomes a bottleneck (millions of rows/day), we can easily switch the **Processing Layer** to write to **ClickHouse** or **Tinybird** without changing the Ingestion or Presentation layers.

## Implementation Steps
1.  **Backend**: Add `POST /analytics` endpoint to `brain-gateway` that writes to Redis using `xadd`.
2.  **Backend**: Create a Python worker (in `brain-gateway` or separate service) that consumes the stream and writes to DB.
3.  **Frontend**: Connect Dashboard cards to `GET /analytics` endpoints.
