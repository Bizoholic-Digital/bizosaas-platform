# BizOSaaS Infrastructure Architecture - Staging Environment

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DOKPLOY ORCHESTRATION PLATFORM                    │
│                        VPS: 194.238.16.237                           │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│              PROJECT: bizosaas-infrastructure-staging                │
│                  Network: bizosaas-staging-network                   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│   POSTGRESQL  │          │     REDIS     │          │     VAULT     │
│   DATABASE    │          │     CACHE     │          │   SECRETS     │
├───────────────┤          ├───────────────┤          ├───────────────┤
│ Port: 5432    │          │ Port: 6379    │          │ Port: 8200    │
│ Image: pg16   │          │ Image: redis  │          │ Image: vault  │
│ + pgvector    │          │ + appendonly  │          │ + dev mode    │
└───────┬───────┘          └───────────────┘          └───────────────┘
        │
        │ [DEPENDS ON POSTGRES]
        │
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│                       TEMPORAL ORCHESTRATION                          │
├───────────────┬───────────────────────────┬───────────────────────────┤
│               │                           │                           │
│  ┌────────────┴──────────┐   ┌───────────┴────────┐   ┌─────────────┴─────────┐
│  │  TEMPORAL SERVER      │   │   TEMPORAL UI      │   │  TEMPORAL INTEGRATION │
│  ├───────────────────────┤   ├────────────────────┤   ├───────────────────────┤
│  │ Port: 7233            │   │ Port: 8082         │   │ Port: 8009            │
│  │ Image: temporalio     │   │ Image: ui:2.21.0   │   │ Build: GitHub         │
│  │ + auto-setup          │   │ Web Interface      │   │ Custom Workflows      │
│  └───────────────────────┘   └────────────────────┘   └───────────────────────┘
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Service Layer Breakdown

### Foundation Layer (Independent)
```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ PostgreSQL  │   │    Redis    │   │    Vault    │
│             │   │             │   │             │
│  • pgvector │   │  • Cache    │   │  • Secrets  │
│  • 4 DBs    │   │  • Sessions │   │  • KV Store │
│  • RLS      │   │  • Persist  │   │  • Tokens   │
└─────────────┘   └─────────────┘   └─────────────┘
```

### Orchestration Layer (Depends on Foundation)
```
┌─────────────────────────────────────────────────┐
│           TEMPORAL WORKFLOW ENGINE              │
├──────────────┬──────────────┬───────────────────┤
│   Server     │      UI      │   Integration     │
│              │              │                   │
│ • Workflows  │ • Dashboard  │ • Custom Tasks    │
│ • Activities │ • Monitoring │ • API Gateway     │
│ • Schedules  │ • Analytics  │ • Event Handlers  │
└──────────────┴──────────────┴───────────────────┘
```

---

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    EXTERNAL ACCESS                        │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  http://194.238.16.237:8082  ───►  Temporal UI           │
│  http://194.238.16.237:8200  ───►  Vault UI              │
│  http://194.238.16.237:8009  ───►  Temporal Integration  │
│                                                           │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│              INTERNAL SERVICE NETWORK                     │
│          (bizosaas-staging-network)                       │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Temporal Server  ◄──►  PostgreSQL (temporal_staging)    │
│         │                                                 │
│         ├──────────────►  Redis (caching)                │
│         │                                                 │
│         └──────────────►  Temporal UI                     │
│                                                           │
│  Temporal Integration  ◄──►  Temporal Server             │
│         │                                                 │
│         ├──────────────►  PostgreSQL (bizosaas_staging)  │
│         │                                                 │
│         └──────────────►  Redis (sessions)               │
│                                                           │
│  Backend Services ◄────►  Vault (secrets)                │
│  (Future Phase 2)                                         │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## Database Architecture

```
┌─────────────────────────────────────────────────────────┐
│         PostgreSQL (bizosaas-postgres-staging)          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────┐  ┌─────────────────────────┐   │
│  │ bizosaas_staging   │  │  saleor_staging         │   │
│  │                    │  │                         │   │
│  │ • Main SaaS DB     │  │ • E-commerce DB         │   │
│  │ • Multi-tenant     │  │ • Product catalog       │   │
│  │ • pgvector         │  │ • Orders & payments     │   │
│  │ • UUID support     │  │                         │   │
│  └────────────────────┘  └─────────────────────────┘   │
│                                                          │
│  ┌────────────────────┐  ┌─────────────────────────┐   │
│  │ temporal_staging   │  │  vault_staging          │   │
│  │                    │  │                         │   │
│  │ • Workflows        │  │ • Secrets metadata      │   │
│  │ • Task queues      │  │ • Audit logs            │   │
│  │ • Event history    │  │                         │   │
│  └────────────────────┘  └─────────────────────────┘   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Volume Persistence

```
┌─────────────────────────────────────────────────────────┐
│                  DATA VOLUMES (Docker)                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  postgres_staging_data                                   │
│  ├── /var/lib/postgresql/data                           │
│  └── Contains: All database files, WAL logs             │
│                                                          │
│  redis_staging_data                                      │
│  ├── /data                                               │
│  └── Contains: RDB snapshots, AOF logs                  │
│                                                          │
│  vault_staging_data                                      │
│  ├── /vault/data                                         │
│  └── Contains: Encrypted secrets, audit logs            │
│                                                          │
│  temporal_staging_data                                   │
│  ├── /etc/temporal/config/dynamicconfig                 │
│  └── Contains: Temporal configuration                   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Port Mapping

```
┌─────────────────────────────────────────────────────────┐
│              VPS: 194.238.16.237                         │
├──────────────┬──────────────────────────────────────────┤
│ External     │ Internal Container                        │
│ Port         │ Service                                   │
├──────────────┼──────────────────────────────────────────┤
│ 5432         │ PostgreSQL                                │
│ 6379         │ Redis                                     │
│ 7233         │ Temporal Server                           │
│ 8009         │ Temporal Integration                      │
│ 8082         │ Temporal UI                               │
│ 8200         │ Vault                                     │
└──────────────┴──────────────────────────────────────────┘
```

---

## Service Dependencies

```
┌─────────────────────────────────────────────────────────┐
│                 STARTUP SEQUENCE                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. PostgreSQL  ───────┐                                │
│  2. Redis       ───────┼──► Foundation Ready            │
│  3. Vault       ───────┘                                │
│                         │                                │
│                         ▼                                │
│  4. Temporal Server ────┐                               │
│     (waits for PG)      │                               │
│                         ▼                                │
│  5. Temporal UI ────────┼──► Orchestration Ready        │
│  6. Temporal Integration┘                               │
│     (waits for all)                                      │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Health Check Strategy

```
┌─────────────────────────────────────────────────────────┐
│              HEALTH MONITORING                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  PostgreSQL:                                             │
│  └─► pg_isready -U admin -d bizosaas_staging            │
│      Interval: 30s │ Timeout: 10s │ Retries: 3          │
│                                                          │
│  Redis:                                                  │
│  └─► redis-cli ping                                     │
│      Interval: 30s │ Timeout: 10s │ Retries: 3          │
│                                                          │
│  Vault:                                                  │
│  └─► vault status                                       │
│      Interval: 30s │ Timeout: 10s │ Retries: 3          │
│                                                          │
│  Temporal Server:                                        │
│  └─► tctl workflow list                                 │
│      Interval: 30s │ Timeout: 10s │ Retries: 3          │
│                                                          │
│  Temporal UI:                                            │
│  └─► curl -f http://localhost:8080                      │
│      Interval: 30s │ Timeout: 10s │ Retries: 3          │
│                                                          │
│  Temporal Integration:                                   │
│  └─► curl -f http://localhost:8009/health               │
│      Interval: 30s │ Timeout: 10s │ Retries: 3          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Security Layers

```
┌─────────────────────────────────────────────────────────┐
│               SECURITY ARCHITECTURE                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Network Layer:                                          │
│  └─► Internal bridge network (bizosaas-staging-network) │
│      • Container isolation                               │
│      • DNS-based service discovery                       │
│                                                          │
│  Application Layer:                                      │
│  ├─► PostgreSQL: Password authentication                │
│  ├─► Redis: No auth (internal network only)             │
│  ├─► Vault: Root token + TLS                            │
│  └─► Temporal: mTLS support (configurable)              │
│                                                          │
│  Data Layer:                                             │
│  ├─► PostgreSQL: Encrypted volumes (optional)           │
│  ├─► Vault: Encrypted backend storage                   │
│  └─► Redis: AOF persistence with fsync                  │
│                                                          │
│  Access Layer:                                           │
│  └─► Public ports exposed for staging testing           │
│      • Production: Use Traefik reverse proxy            │
│      • SSL/TLS certificates via Let's Encrypt           │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Integration Points for Phase 2 (Backend Services)

```
┌─────────────────────────────────────────────────────────┐
│        READY FOR BACKEND INTEGRATION                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Brain API Gateway       ───►  PostgreSQL               │
│  (Port 8001)                   (bizosaas_staging)       │
│                                                          │
│  Django CRM             ───►  Redis                     │
│  (Port 8003)                  (cache/sessions)          │
│                                                          │
│  AI Agents              ───►  Vault                     │
│  (Port 8010)                  (API keys/secrets)        │
│                                                          │
│  All Backend Services   ───►  Temporal Server           │
│                               (workflow orchestration)  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Resource Allocation

```
┌─────────────────────────────────────────────────────────┐
│           EXPECTED RESOURCE USAGE                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  PostgreSQL:           512MB - 1GB RAM                   │
│  Redis:                128MB - 256MB RAM                 │
│  Vault:                128MB - 256MB RAM                 │
│  Temporal Server:      512MB - 1GB RAM                   │
│  Temporal UI:          256MB - 512MB RAM                 │
│  Temporal Integration: 256MB - 512MB RAM                 │
│                                                          │
│  ─────────────────────────────────────────────────       │
│  TOTAL:                ~2-4GB RAM                        │
│                        ~10GB Disk (with data growth)     │
│                        2-4 CPU cores                     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

**Infrastructure Architecture - Foundation for Multi-Tenant SaaS Platform**

*Designed for scalability, reliability, and rapid development*
