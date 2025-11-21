# 🏗️ BizoSaaS Architecture Documentation

## 📋 Executive Summary
BizoSaaS is an autonomous AI-first marketing platform built with Domain-Driven Design (DDD) principles, containerized microservices, and shared AI infrastructure. The platform enables fully autonomous marketing operations through intelligent agents powered by Claude AI and CrewAI.

## 🎯 Design Principles

### Why Domain-Driven Design (DDD)?
- **Complex Business Domain**: Marketing automation requires intricate business rules and workflows
- **Multi-Tenant SaaS**: Clear bounded contexts for tenant isolation and feature segmentation  
- **Team Scalability**: Independent teams can own specific domains (Identity, CRM, Campaigns, Analytics)
- **Evolution & Maintenance**: Domain boundaries align with business capabilities

### Architecture Decisions
- **FastAPI + CrewAI + Next.js**: Modern, performant, AI-native stack
- **K3s Orchestration**: Lightweight Kubernetes for container management
- **Shared AI Resources**: Official PyTorch/TensorFlow containers with model volume sharing
- **PostgreSQL + pgvector**: Vector database for AI embeddings and traditional data

## 🧩 System Architecture

```yaml
BizoSaaS Autonomous AI Marketing Platform (Containerized Microservices)
├─────────────────────────────────────────────────────────────────────────────┐
│                    Presentation Layer (Next.js 14)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Client      │  │ Campaign    │  │ Analytics   │  │ Admin       │        │
│  │ Dashboard   │  │ Management  │  │ Reports     │  │ Portal      │        │
│  │ (React)     │  │ (React)     │  │ (Charts)    │  │ (React)     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────────────────────┤
│                      API Gateway & Authentication                           │
│           (Traefik + JWT + Multi-Tenant Routing)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                       Domain Services (Microservices)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Identity &  │  │ Campaign    │  │ CRM &       │  │ Analytics & │        │
│  │ Billing     │  │ Management  │  │ Lead Mgmt   │  │ Reporting   │        │
│  │ Service     │  │ Service     │  │ Service     │  │ Service     │        │
│  │ (FastAPI)   │  │ (FastAPI)   │  │ (FastAPI)   │  │ (FastAPI)   │        │
│  │ Port 8001   │  │ Port 8003   │  │ Port 8004   │  │ Port 8005   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────────────────────┤
│                    Shared AI Infrastructure                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ AI          │  │ Vector      │  │ LangChain   │  │ ML Pipeline │        │
│  │ Orchestrator│  │ Store       │  │ RAG         │  │ Service     │        │
│  │ (CrewAI)    │  │ (pgvector)  │  │ (Official)  │  │ (PyTorch)   │        │
│  │ Port 8002   │  │             │  │             │  │             │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────────────────────┤
│                         Data Layer                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ PostgreSQL  │  │ Redis       │  │ MinIO       │  │ Neo4j       │        │
│  │ +pgvector   │  │ Cache       │  │ Object      │  │ Knowledge   │        │
│  │ (Primary)   │  │ (Sessions)  │  │ Storage     │  │ Graph       │        │
│  │ Port 5432   │  │ Port 6379   │  │ Port 9000   │  │ Port 7474   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────────────────────┤
│                    Infrastructure & Monitoring                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ K3s         │  │ Prometheus  │  │ HashiCorp   │  │ Traefik     │        │
│  │ Orchestr.   │  │ + Grafana   │  │ Vault       │  │ Gateway     │        │
│  │ (Container) │  │ (Monitoring)│  │ (Secrets)   │  │ (SSL/LB)    │        │
│  │             │  │ Port 9090   │  │ Port 8200   │  │ Port 80/443 │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────────────────────┤
│                      External Integrations                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Google Ads  │  │ Meta Ads    │  │ LinkedIn    │  │ Stripe      │        │
│  │ API         │  │ API         │  │ Marketing   │  │ Billing     │        │
│  │ (Direct)    │  │ (Direct)    │  │ API         │  │ (Webhook)   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🔧 Service Boundaries & Responsibilities

### 1. Identity & Billing Service (Port 8001)
**Bounded Context**: User Authentication, Authorization, Billing
- **Responsibilities**:
  - JWT token generation and validation
  - Multi-tenant user management
  - Subscription and billing management (Stripe)
  - Rate limiting and API quotas
  - Audit logging for security events

### 2. AI Orchestrator Service (Port 8002)  
**Bounded Context**: AI Agent Coordination and Task Execution
- **Responsibilities**:
  - CrewAI agent lifecycle management
  - Task queue processing with Celery
  - LangChain RAG operations
  - Vector search and semantic analysis
  - AI model serving and inference

### 3. Campaign Management Service (Port 8003)
**Bounded Context**: Marketing Campaign Operations
- **Responsibilities**:
  - Campaign creation, scheduling, execution
  - Multi-channel ad platform integration
  - A/B testing and optimization
  - Budget management and bidding
  - Performance tracking and alerts

### 4. CRM & Lead Management Service (Port 8004)
**Bounded Context**: Customer Relationship and Sales Pipeline
- **Responsibilities**:
  - Lead capture and enrichment
  - Contact and account management
  - Sales pipeline and deal tracking
  - AI-powered lead scoring
  - Communication history and notes

### 5. Analytics & Reporting Service (Port 8005)
**Bounded Context**: Data Analysis and Business Intelligence
- **Responsibilities**:
  - Multi-channel performance metrics
  - ROI analysis and attribution
  - Custom report generation
  - Real-time dashboard data
  - Predictive analytics and insights

## 🤖 AI Agent Architecture

### Claude Agent Modules (CrewAI Framework)

| Agent | Primary Function | Inputs | Outputs |
|-------|------------------|--------|---------|
| **OnboardingAgent** | Personalized setup and funnel mapping | Business info, goals, budget | Setup recommendations, funnel strategy |
| **AuditAgent** | Site/product analysis with actionable insights | Website URL, business type | Audit report, improvement recommendations |
| **StrategyAgent** | AI-driven marketing strategy generation | Business context, market data | Marketing strategy, channel recommendations |
| **CampaignAgent** | Multi-channel campaign execution | Strategy, budget, targets | Campaign configs, ad creatives |
| **OptimizationAgent** | Performance tuning and A/B testing | Campaign data, performance metrics | Optimization recommendations, test plans |
| **ReportingAgent** | Automated report generation | Performance data, business KPIs | Visual reports, executive summaries |
| **CommunityAgent** | Sentiment analysis and engagement | Social data, community feedback | Sentiment reports, engagement strategies |
| **IntegrationAgent** | Third-party API orchestration | API credentials, data requirements | Integration status, data sync reports |
| **MonitoringAgent** | System health and fallback logic | System metrics, error logs | Health reports, incident responses |

## 🗄️ Data Architecture

### Multi-Tenant Database Design
```sql
-- Tenant isolation through row-level security
CREATE TABLE tenants (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE,
    settings JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- All business entities include tenant_id for isolation
CREATE TABLE users (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    email VARCHAR(255) NOT NULL,
    -- Additional fields...
    CONSTRAINT unique_email_per_tenant UNIQUE(tenant_id, email)
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON users FOR ALL TO authenticated_user
    USING (tenant_id = current_setting('app.current_tenant')::UUID);
```

### Vector Storage for AI
```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Store embeddings for semantic search
CREATE TABLE document_embeddings (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    document_type VARCHAR(100),
    content TEXT,
    embedding vector(1536),  -- OpenAI embeddings dimension
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create HNSW index for fast similarity search
CREATE INDEX ON document_embeddings 
USING hnsw (embedding vector_cosine_ops);
```

## 🚀 Containerization Strategy

### Base Images (Gold Standard)
```yaml
AI Services: 
  - pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime (Official PyTorch)
  - tensorflow/tensorflow:2.14.0-gpu (Official TensorFlow) 
  - huggingface/transformers-pytorch-gpu:4.35.0

Application Services:
  - python:3.11-slim-bullseye (Official Python)
  - node:18-alpine (Official Node.js)
  - nginx:1.25-alpine (Official Nginx)

Data Services:
  - postgres:15-alpine (Official PostgreSQL)
  - redis:7-alpine (Official Redis)
  - neo4j:5.13-community (Official Neo4j)
```

### Shared Volumes Strategy
```yaml
Shared Volumes:
  - /shared/models: Pre-trained AI models (PyTorch, TensorFlow)
  - /shared/embeddings: Vector embeddings and indexes
  - /shared/configs: Common configuration files
  - /shared/logs: Centralized log directory

Benefits:
  - Model sharing between containers (no duplication)
  - Layer caching for faster builds
  - Multi-stage builds to minimize image size
  - Health checks and graceful shutdowns
```

## 🔒 Security Architecture

### Authentication Flow
1. **User Login**: Credentials validated against Identity Service
2. **JWT Generation**: Signed token with tenant context and permissions
3. **Request Authorization**: Each service validates JWT and extracts tenant_id
4. **Row-Level Security**: Database enforces tenant isolation automatically

### Secrets Management
- **Development**: Environment variables and .env files
- **Production**: HashiCorp Vault with dynamic secrets
- **API Keys**: Encrypted storage in tenant_integrations table
- **Certificates**: Let's Encrypt with automatic renewal

## 📊 Performance Targets

### Technical Performance
- **API Response Time**: <50ms (P95) vs 500ms+ WordPress
- **Database Query Time**: <10ms (P95) with proper indexing
- **AI Agent Response**: <2 seconds for complex analysis
- **Frontend Load Time**: <1.5 seconds (First Contentful Paint)
- **Container Startup**: <30 seconds for AI services
- **Memory Usage**: <8GB total for all services

### Business Metrics
- **Development Velocity**: 8 weeks to production (vs 20+ weeks)
- **Deployment Frequency**: Daily deployments with zero downtime
- **Error Rate**: <0.1% for critical user journeys
- **Scalability**: 10,000+ concurrent users per $100/month
- **Cost Efficiency**: 60% reduction vs monolithic WordPress

## 🔄 Communication Patterns

### Synchronous Communication (HTTP/REST)
- **Client ↔ API Gateway**: Frontend interactions
- **Gateway ↔ Services**: Request routing and response aggregation
- **Inter-Service**: Real-time data queries and validation

### Asynchronous Communication (Events)
- **Redis Pub/Sub**: Fast, ephemeral event notifications
- **Kafka**: Durable event streaming for audit trails
- **WebSockets**: Real-time UI updates for dashboards

### Data Consistency
- **Eventual Consistency**: Saga pattern for cross-service transactions
- **Strong Consistency**: Within service boundaries using ACID transactions
- **Conflict Resolution**: Last-writer-wins with timestamp ordering

## 🔍 Monitoring & Observability

### Metrics Collection (Prometheus)
- **Business Metrics**: Campaign performance, conversion rates, revenue
- **Technical Metrics**: Response times, error rates, resource usage
- **AI Metrics**: Agent execution times, model accuracy, token usage

### Logging (ELK Stack)
- **Application Logs**: Structured JSON logs from all services
- **Audit Logs**: Security events, data changes, user actions
- **Error Tracking**: Exception details with stack traces and context

### Distributed Tracing (Jaeger)
- **Request Flow**: Track requests across service boundaries
- **Performance Bottlenecks**: Identify slow components in request chain
- **Dependency Mapping**: Visualize service interactions

## 🚀 Deployment Architecture

### Development Environment
- **Local K3s**: Single-node cluster for development
- **Hot Reloading**: File watching for rapid development cycles
- **Service Mesh**: Istio for advanced traffic management (optional)

### Production Environment  
- **Multi-Node K3s**: High availability with 3+ nodes
- **Blue-Green Deployment**: Zero-downtime releases
- **Auto-Scaling**: HPA based on CPU/memory and custom metrics
- **Disaster Recovery**: Automated backups and cross-region replication

This architecture ensures scalability, maintainability, and autonomous AI operation while providing clear service boundaries and optimal performance characteristics.