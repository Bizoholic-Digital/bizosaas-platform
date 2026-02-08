# PostgreSQL Database Service - Infrastructure

## Service Identity
- **Name**: PostgreSQL Database
- **Type**: Infrastructure - Relational Database
- **Container**: `bizosaas-postgres-staging`
- **Image**: `postgres:15-alpine`
- **Port**: `5433:5432` (external:internal)
- **Network**: `dokploy-network`
- **Status**: ✅ Running (2+ days uptime)

## Purpose
Primary multi-tenant relational database for the entire BizOSaaS platform. Provides persistent storage for all backend services with pgvector extension for AI embeddings and vector similarity search.

## Architecture

### Multi-Tenant Design
```
Database: bizosaas_platform
├── Shared Schemas:
│   ├── public (pgvector extension)
│   ├── tenants (tenant registry)
│   └── auth (authentication)
└── Tenant-Specific Schemas:
    ├── tenant_<uuid>_data
    ├── tenant_<uuid>_campaigns
    └── tenant_<uuid>_analytics
```

### Key Features
- **PostgreSQL 15**: Latest stable version
- **pgvector Extension**: 384-dimensional vector storage for AI embeddings
- **Row-Level Security (RLS)**: Tenant data isolation
- **Multi-Tenancy**: Shared infrastructure, isolated data
- **Connection Pooling**: PgBouncer for connection management
- **Replication**: Streaming replication for high availability

## Dependencies

### Required By (Consumers)
- Brain API Gateway (port 8001)
- AI Agents Service (port 8008)
- Auth Service (port 8007)
- Wagtail CMS (port 8002)
- Saleor E-commerce (port 8000)
- Django CRM (port 8003)
- CorelDove Backend (port 8005)
- Amazon Sourcing (port 8009)
- Business Directory Backend (port 8004)
- QuantTrade Backend (port 8012)
- Temporal Server (workflow state)

### External Dependencies
- None (base infrastructure)

## Database Schema

### Core Tenancy Tables
```sql
-- Tenant Registry
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    domain VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    subscription_tier VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- User Management
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Vector Store (pgvector)
CREATE TABLE vector_store (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    content TEXT,
    embedding vector(384),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_vector_store_embedding ON vector_store
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### Row-Level Security Example
```sql
-- Enable RLS
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;

-- Tenant isolation policy
CREATE POLICY tenant_isolation_policy ON campaigns
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);
```

## Configuration

### Environment Variables
```bash
# Database Connection
POSTGRES_HOST=bizosaas-postgres-staging
POSTGRES_PORT=5432
POSTGRES_DB=bizosaas_platform
POSTGRES_USER=postgres
POSTGRES_PASSWORD=SharedInfra2024!SuperSecure

# Connection Pool
POSTGRES_MAX_CONNECTIONS=200
POSTGRES_POOL_SIZE=20
POSTGRES_POOL_TIMEOUT=30

# Extensions
POSTGRES_EXTENSIONS=pgvector,uuid-ossp,pg_trgm

# Replication
POSTGRES_REPLICATION_MODE=async
POSTGRES_REPLICATION_USER=replicator
```

### Docker Compose Configuration
```yaml
services:
  postgres:
    image: postgres:15-alpine
    container_name: bizosaas-postgres-staging
    environment:
      POSTGRES_DB: bizosaas_platform
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    ports:
      - "5433:5432"
    networks:
      - dokploy-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
```

## Initialization Scripts

### `init-scripts/01-extensions.sql`
```sql
-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "pgvector";

-- Verify extensions
SELECT * FROM pg_extension;
```

### `init-scripts/02-schema.sql`
```sql
-- Create base schemas
CREATE SCHEMA IF NOT EXISTS tenants;
CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Set search path
ALTER DATABASE bizosaas_platform SET search_path TO public, tenants, auth;
```

## API Endpoints

PostgreSQL exposes standard PostgreSQL protocol endpoints:

- **Primary Connection**: `postgres://postgres:password@bizosaas-postgres-staging:5432/bizosaas_platform`
- **Health Check**: `pg_isready -U postgres`
- **Admin Interface**: Not exposed directly (use pgAdmin or DBeaver)

## Health Checks

### Container Health Check
```bash
# Check PostgreSQL is accepting connections
docker exec bizosaas-postgres-staging pg_isready -U postgres

# Expected output: bizosaas-postgres-staging:5432 - accepting connections
```

### Database Connection Test
```python
import psycopg2

def check_postgres_health():
    try:
        conn = psycopg2.connect(
            host="bizosaas-postgres-staging",
            port=5432,
            database="bizosaas_platform",
            user="postgres",
            password="SharedInfra2024!SuperSecure"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] == 1
    except Exception as e:
        return False
```

### Vector Extension Check
```sql
-- Verify pgvector extension
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Test vector operations
SELECT '[1,2,3]'::vector <-> '[4,5,6]'::vector AS distance;
```

## Integration Points

### Brain API Gateway Integration
```python
# FastAPI database connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:SharedInfra2024!SuperSecure@bizosaas-postgres-staging:5432/bizosaas_platform"

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=40)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tenant context middleware
def set_tenant_context(tenant_id: str):
    with SessionLocal() as session:
        session.execute(f"SET app.current_tenant_id = '{tenant_id}'")
```

### AI Agents Vector Search
```python
# Vector similarity search for RAG
from pgvector.sqlalchemy import Vector

def search_similar_documents(query_embedding, limit=10):
    query = f"""
        SELECT content, metadata,
               embedding <-> '{query_embedding}'::vector AS distance
        FROM vector_store
        WHERE tenant_id = :tenant_id
        ORDER BY distance ASC
        LIMIT :limit
    """
    return session.execute(query, {"tenant_id": tenant_id, "limit": limit})
```

## Performance Tuning

### Connection Pooling
```python
# Use PgBouncer for connection pooling
# pgbouncer.ini
[databases]
bizosaas_platform = host=bizosaas-postgres-staging port=5432 dbname=bizosaas_platform

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
```

### Index Strategy
```sql
-- Tenant-scoped indexes
CREATE INDEX idx_campaigns_tenant_id ON campaigns(tenant_id);
CREATE INDEX idx_leads_tenant_created ON leads(tenant_id, created_at DESC);

-- Full-text search indexes
CREATE INDEX idx_content_search ON content USING gin(to_tsvector('english', content));

-- Vector indexes (IVFFlat for large datasets)
CREATE INDEX idx_vector_embeddings ON vector_store
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

## Backup & Recovery

### Backup Strategy
```bash
# Daily full backup
docker exec bizosaas-postgres-staging pg_dump -U postgres bizosaas_platform > backup_$(date +%Y%m%d).sql

# Continuous archiving (WAL)
# postgresql.conf
archive_mode = on
archive_command = 'cp %p /backups/wal/%f'
```

### Recovery Procedure
```bash
# Restore from backup
docker exec -i bizosaas-postgres-staging psql -U postgres bizosaas_platform < backup_20251015.sql

# Point-in-time recovery
pg_basebackup -h bizosaas-postgres-staging -U replicator -D /restore
```

## Monitoring

### Key Metrics
- **Connection Count**: `SELECT count(*) FROM pg_stat_activity;`
- **Database Size**: `SELECT pg_size_pretty(pg_database_size('bizosaas_platform'));`
- **Cache Hit Ratio**: `SELECT sum(blks_hit)*100/sum(blks_hit+blks_read) FROM pg_stat_database;`
- **Slow Queries**: `SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;`

### Alerting Thresholds
- Connection count > 180 (90% of max)
- Cache hit ratio < 95%
- Database size > 80% of disk
- Replication lag > 10 seconds

## Common Issues

### Issue 1: Connection Refused
**Symptom**: Services cannot connect to database
**Diagnosis**:
```bash
docker logs bizosaas-postgres-staging
docker exec bizosaas-postgres-staging pg_isready
```
**Solution**:
- Check container is running
- Verify network connectivity
- Check pg_hba.conf allows host connections

### Issue 2: Out of Connections
**Symptom**: `FATAL: sorry, too many clients already`
**Diagnosis**: `SELECT count(*) FROM pg_stat_activity;`
**Solution**:
- Increase `max_connections` in postgresql.conf
- Implement connection pooling (PgBouncer)
- Fix connection leaks in application code

### Issue 3: Slow Vector Search
**Symptom**: Vector similarity queries take > 2 seconds
**Diagnosis**: `EXPLAIN ANALYZE SELECT ... ORDER BY embedding <-> ...`
**Solution**:
- Create IVFFlat index with appropriate lists parameter
- Use approximate nearest neighbor (ANN) search
- Increase shared_buffers for index caching

### Issue 4: Replication Lag
**Symptom**: Standby server behind primary by > 10 seconds
**Diagnosis**: `SELECT * FROM pg_stat_replication;`
**Solution**:
- Check network bandwidth
- Increase wal_sender_timeout
- Verify standby has sufficient resources

## Security Considerations

### Access Control
```sql
-- Create read-only user for analytics
CREATE USER analytics_ro WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE bizosaas_platform TO analytics_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_ro;

-- Revoke public schema access
REVOKE ALL ON SCHEMA public FROM PUBLIC;
```

### Encryption
- **At Rest**: Enable PostgreSQL data encryption (pgcrypto)
- **In Transit**: Require SSL connections
- **Credentials**: Store in HashiCorp Vault

### Audit Logging
```sql
-- Enable audit logging
CREATE EXTENSION IF NOT EXISTS pgaudit;

-- Log all DDL and DML
ALTER SYSTEM SET pgaudit.log = 'ddl, write';
```

## Migration Strategy

### Schema Migrations (Alembic)
```python
# migrations/versions/001_initial_schema.py
def upgrade():
    op.create_table(
        'tenants',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
```

### Zero-Downtime Migrations
1. Add new column with default value
2. Backfill data in batches
3. Update application code to use new column
4. Remove old column after verification

## Testing

### Integration Tests
```python
import pytest
from sqlalchemy import create_engine

@pytest.fixture
def db_session():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        yield conn
        conn.execute("ROLLBACK")

def test_tenant_isolation(db_session):
    # Set tenant context
    db_session.execute("SET app.current_tenant_id = 'tenant-1'")

    # Verify only tenant-1 data is visible
    result = db_session.execute("SELECT * FROM campaigns")
    assert all(row.tenant_id == 'tenant-1' for row in result)
```

## Deployment Checklist

- [ ] PostgreSQL 15 container deployed
- [ ] pgvector extension installed
- [ ] Multi-tenant schema created
- [ ] Row-level security policies applied
- [ ] Connection pooling configured
- [ ] Backup automation set up
- [ ] Monitoring dashboards created
- [ ] Health checks passing
- [ ] All backend services connected successfully
- [ ] Vector search performance tested

## References
- [PostgreSQL 15 Documentation](https://www.postgresql.org/docs/15/)
- [pgvector Extension](https://github.com/pgvector/pgvector)
- [Multi-Tenancy Best Practices](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- BizOSaaS PRD: `/home/alagiri/projects/bizoholic/comprehensive_prd_06092025.md`

---
**Status**: ✅ Production-Ready
**Last Updated**: October 15, 2025
**Owner**: Infrastructure Team
