# BizoholicSaaS - Domain-Driven Design Microservices Architecture

## 🚀 Complete AI Marketing Agency SaaS Platform

BizoholicSaaS is a comprehensive AI Marketing Agency SaaS platform built with Domain-Driven Design (DDD) principles and microservices architecture. The platform provides AI-powered marketing automation, campaign management, analytics, and client management services.

## 🏗️ Microservices Architecture

### Core Domain Services

1. **User Management Service** (Port 8001)
   - Authentication & Authorization (JWT, OAuth2)
   - Multi-tenant user management
   - Role-based access control (RBAC)
   - User profiles & preferences

2. **Campaign Management Service** (Port 8002)
   - Campaign lifecycle management
   - AI agent integration & orchestration
   - Campaign optimization & A/B testing
   - Performance tracking

3. **Analytics Service** (Port 8003)
   - Real-time metrics & KPI tracking
   - Custom dashboard generation
   - Report generation & scheduling
   - Data visualization & insights

4. **Integration Service** (Port 8004)
   - Third-party API management (Google Ads, Meta, LinkedIn)
   - Webhook handling & processing
   - Data synchronization
   - API rate limiting & error handling

5. **Notification Service** (Port 8005)
   - Multi-channel notifications (Email, SMS, In-app)
   - Template management
   - Delivery tracking & analytics
   - Preference management

6. **AI Agents Service** (Port 8000)
   - CrewAI orchestration & workflows
   - AI model management
   - Agent performance monitoring
   - Custom agent development

7. **API Gateway** (Port 8080)
   - Request routing & load balancing
   - Authentication & authorization
   - Rate limiting & throttling
   - Request/response transformation

### Supporting Services

- **Content Management**: Strapi CMS (Port 1337)
- **E-commerce**: Medusa.js (Ports 9000, 7001)
- **Sales Funnel**: Mautic (Port 8090)
- **Database**: PostgreSQL with schema-per-service
- **Cache**: Redis/Dragonfly
- **Message Queue**: RabbitMQ/NATS

## 📁 Project Structure

```
bizosaas/
├── services/
│   ├── user-management/         # Port 8001
│   ├── campaign-management/     # Port 8002
│   ├── analytics/              # Port 8003
│   ├── integration/            # Port 8004
│   ├── notification/           # Port 8005
│   ├── ai-agents/              # Port 8000
│   └── api-gateway/            # Port 8080
├── shared/
│   ├── database/               # Database models & connections
│   ├── events/                 # Event-driven communication
│   ├── auth/                   # JWT authentication
│   ├── monitoring/             # Health checks & metrics
│   └── utils/                  # Common utilities
├── k8s/
│   └── manifests/              # Kubernetes deployment files
├── docker-compose.dev.yml      # Development environment
├── docker-compose.prod.yml     # Production environment
├── requirements.txt            # Python dependencies
├── .env.example               # Environment configuration template
└── start-dev.sh               # Development startup script
```

## 🚀 Technology Stack

### Backend Services
- **Framework**: FastAPI 0.104+ with async/await
- **Database**: PostgreSQL 15+ with pgvector extension
- **ORM**: SQLAlchemy 2.0+ with Alembic migrations
- **Authentication**: JWT with FastAPI-Users
- **Background Tasks**: Celery + Redis

### AI Infrastructure
- **Agent Framework**: CrewAI with custom agents
- **LLM Integration**: LangChain + OpenRouter
- **Vector Database**: pgvector for semantic search
- **ML Framework**: PyTorch (official containers)
- **Knowledge Graphs**: Neo4j for advanced reasoning

### Frontend
- **Framework**: NextJS 14 with App Router
- **UI Library**: ShadCN/UI + Tailwind CSS
- **Forms**: React Hook Form + Zod validation
- **Charts**: Recharts for analytics
- **State Management**: Zustand/React Query

### Infrastructure
- **Orchestration**: K3s (lightweight Kubernetes)
- **Gateway**: Traefik with auto-SSL
- **Monitoring**: Prometheus + Grafana + ELK Stack
- **Secrets**: HashiCorp Vault
- **CI/CD**: GitHub Actions + ArgoCD

## 🛠️ Development Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- PostgreSQL 16+ with pgvector extension
- Redis 7+
- Git

### Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository>
   cd bizosaas
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start Development Environment**
   ```bash
   # Start all services
   ./start-dev.sh
   
   # Or manually
   docker-compose -f docker-compose.dev.yml up -d
   ```

3. **Service Endpoints**
   - **API Gateway**: http://localhost:8080
   - **User Management**: http://localhost:8001
   - **Campaign Management**: http://localhost:8002
   - **Analytics**: http://localhost:8003
   - **Integration**: http://localhost:8004
   - **Notification**: http://localhost:8005
   - **AI Agents**: http://localhost:8000
   - **Strapi CMS**: http://localhost:1337
   - **Mautic**: http://localhost:8090

### API Documentation
- API Gateway Docs: http://localhost:8080/docs
- User Management: http://localhost:8001/docs
- Campaign Management: http://localhost:8002/docs
- Analytics: http://localhost:8003/docs
- Integration: http://localhost:8004/docs
- Notification: http://localhost:8005/docs
- AI Agents: http://localhost:8000/docs

### Development Tools
- **Database Admin**: http://localhost:8082
- **Redis Commander**: http://localhost:8083

## 📋 Development Phases

- ✅ **Phase 1**: Core Backend Infrastructure (K3s + FastAPI)
- 🔄 **Phase 2**: Domain Services Development
- ⏳ **Phase 3**: Frontend & AI Enhancement
- ⏳ **Phase 4**: Production & Monitoring

## 🎯 Architecture Principles

- **Domain-Driven Design**: Clear bounded contexts for business domains
- **Microservices**: Independent deployable services
- **Shared Resources**: Efficient AI model sharing via volumes
- **API-First**: RESTful APIs with OpenAPI documentation
- **Event-Driven**: Async communication for scalability
- **Cloud-Native**: Container-first with K8s orchestration