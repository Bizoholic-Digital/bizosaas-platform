# BizOSaaS Platform - Architecture Component Reference
## Complete System Architecture Documentation for Restart & Maintenance

**Created**: September 16, 2025  
**Purpose**: Comprehensive component reference for architecture understanding and system restart  
**Version**: Unified Platform Flow Integration v2.0

---

## 🎯 Executive Architecture Summary

### Platform Ecosystem Overview
BizOSaaS is a unified multi-platform ecosystem with seamless authentication and cross-platform navigation, integrating:
- **Bizoholic** (Marketing Platform) - Port 3000
- **BizOSaaS Admin** (Central Management) - Port 3001  
- **CoreLDove** (E-commerce Platform) - Port 3002
- **AI Chat Service** (Universal Assistant) - Port 3003
- **Business Directory** (Data Management) - Port 8003
- **SQL Admin** (Infrastructure Management) - Port 5000

### Core Architecture Principles
1. **Unified Authentication**: Single sign-on across all platforms via Auth Service v2
2. **Role-Based Access**: Hierarchical permissions with platform-specific access control
3. **Direct Login Portal**: localhost:3002 as primary authentication entry point
4. **Cross-Platform Navigation**: Seamless switching without re-authentication
5. **Real-Time Monitoring**: Live platform health status and performance metrics

---

## 🏗️ System Architecture Components

### Frontend Layer (Ports 3000-3003)

#### 1. Bizoholic Marketing Platform (Port 3000)
**Location**: `/home/alagiri/projects/bizoholic/bizosaas-platform/marketing/services/bizoholic-frontend/`
**Technology**: Next.js 14 + TypeScript + TailwindCSS
**Purpose**: AI-powered marketing campaigns and automation
**Features**:
- Marketing campaign management
- AI agent orchestration for social media
- Client portal and reporting
- Lead generation and qualification
- Multi-channel analytics

**Key Files**:
- `app/page.tsx` - Homepage with marketing tools
- `app/dashboard/page.tsx` - Campaign dashboard
- `components/campaign/` - Campaign management components
- `lib/api/` - API integration layer

#### 2. BizOSaaS Admin Dashboard (Port 3001) 
**Location**: `/home/alagiri/projects/bizoholic/bizosaas-platform/core/services/tailadmin-dashboard/`
**Technology**: FastAPI + TailAdmin v2 + Alpine.js
**Purpose**: Central administration and multi-tenant management
**Features**:
- Multi-platform navigation tabs
- 88 AI agents management
- System health monitoring
- User and role management
- Cross-platform analytics

**Key Files**:
- `main_unified.py` - FastAPI backend with authentication
- `html/index.html` - TailAdmin v2 interface
- `html/platform-switcher.html` - Multi-platform navigation
- `Dockerfile.unified` - Container configuration

#### 3. CoreLDove E-commerce Platform (Port 3002)
**Location**: `/home/alagiri/projects/bizoholic/bizosaas-platform/ecommerce/services/coreldove-frontend/`
**Technology**: Next.js 14 + TypeScript + Saleor GraphQL
**Purpose**: AI-powered e-commerce and product sourcing
**Features**:
- Product sourcing automation
- E-commerce store management
- Multi-gateway payment processing
- Inventory and order management
- Supplier network integration

**Key Files**:
- `app/page.tsx` - Homepage (modified for direct login redirect)
- `app/auth/login/page.tsx` - Login page with dashboard redirect
- `app/dashboard/page.tsx` - Consolidated dashboard with TailAdmin v2
- `components/products/` - Product management components
- `lib/saleor/` - Saleor GraphQL integration

#### 4. AI Chat Service (Port 3003)
**Location**: `/home/alagiri/projects/bizoholic/bizosaas-platform/ai/services/ai-chat-service/`
**Technology**: FastAPI + WebSocket + LangChain + pgvector
**Purpose**: Universal AI assistant for all platforms
**Features**:
- Multi-modal AI chat interface
- Real-time WebSocket communication
- File upload and processing
- Context-aware responses
- Cross-platform intelligence

**Key Files**:
- `main.py` - FastAPI backend with WebSocket
- `chat_service.py` - AI chat orchestration
- `models/` - Database models for chat history
- `static/` - Frontend chat interface

### API Gateway Layer (Port 8002/8080)

#### Brain API Gateway
**Location**: `/home/alagiri/projects/bizoholic/bizosaas-platform/ai/services/bizosaas-brain/`
**Technology**: FastAPI + Apache Superset + Redis
**Purpose**: Central coordination hub for all platform services
**Features**:
- 88 AI agents orchestration
- Cross-platform event routing
- Analytics and insights generation
- Session validation middleware
- Health monitoring coordination

**Key Files**:
- `main.py` - Main API gateway
- `agents/` - CrewAI agent definitions
- `analytics/` - Superset integration
- `middleware/` - Authentication and validation
- `health/` - Platform health monitoring

### Backend Services Layer

#### 1. Authentication Service v2 (Port 8007)
**Location**: `/home/alagiri/projects/bizoholic/bizosaas-platform/core/services/auth-service-v2/`
**Technology**: FastAPI + FastAPI-Users + JWT + PostgreSQL
**Purpose**: Unified authentication and authorization
**Features**:
- JWT token management
- Role-based access control
- Multi-tenant user management
- Session validation
- 2FA/MFA support

**Key Files**:
- `main.py` - Authentication API
- `auth_security.py` - Role and permission definitions
- `models/` - User and role models
- `middleware/` - Authentication middleware

#### 2. AI Agents Orchestration (Port 8001)
**Location**: `/home/alagiri/projects/bizoholic/bizosaas-platform/ai/services/ai-agents/`
**Technology**: CrewAI + LangChain + FastAPI + Redis
**Purpose**: Orchestration of 88 specialized AI agents
**Features**:
- Pattern-specific agent architecture
- Multi-tenant agent execution
- Real-time agent monitoring
- Cross-agent communication
- Performance optimization

**Key Files**:
- `main.py` - Agent orchestration API
- `crews/` - CrewAI agent definitions
- `patterns/` - Agent pattern implementations
- `monitoring/` - Agent health monitoring

#### 3. Business Directory Service (Port 8003)
**Location**: `/home/alagiri/projects/bizoholic/bizosaas-platform/crm/services/business-directory/`
**Technology**: FastAPI + PostgreSQL + Multi-tenant architecture
**Purpose**: Multi-tenant business data management
**Features**:
- Business listing management
- Directory synchronization
- Local SEO optimization
- Lead generation integration
- Multi-tenant data isolation

#### 4. Analytics AI Service (Port 8009)
**Location**: `/home/alagiri/projects/bizoholic/bizosaas-platform/ai/services/analytics-ai-service/`
**Technology**: CrewAI + Apache Superset + ClickHouse
**Purpose**: AI-powered analytics and insights
**Features**:
- Cross-platform analytics
- AI-generated insights
- Real-time dashboard updates
- Multi-tenant analytics
- Performance benchmarking

### Data Layer

#### 1. PostgreSQL Database (Port 5432)
**Purpose**: Primary data store with multi-tenant architecture
**Features**:
- pgvector extension for AI embeddings
- Row-level security (RLS) for tenants
- Multi-tenant schema design
- Vector similarity search
- ACID compliance

**Key Schemas**:
- `tenants` - Multi-tenant configuration
- `users` - User management with roles
- `ai_insights` - AI-generated analytics
- `vector_store` - Embeddings and similarity
- `business_directory` - Business data

#### 2. Redis Cache (Port 6379)
**Purpose**: High-performance caching and session storage
**Features**:
- Session management
- API response caching
- Real-time event streaming
- Cross-platform data sharing
- Performance optimization

#### 3. Apache Superset (Port 8088)
**Purpose**: Analytics and business intelligence
**Features**:
- Multi-tenant analytics dashboards
- Real-time data visualization
- SQL-based report generation
- Role-based analytics access
- Integration with AI insights

---

## 🔐 Authentication & Security Architecture

### Unified Authentication Flow
```
User Request → Platform Entry → Auth Service v2 → JWT Generation → Platform Access
```

### Role Hierarchy & Permissions
```
Super Admin (Global Access)
├── All platforms access
├── Infrastructure management
├── System configuration
└── User role assignment

Tenant Admin (Business Access)
├── Tenant-specific platforms
├── User management within tenant
├── Business operations
└── Analytics access

Manager (Platform Access)
├── Operational platforms
├── Campaign management
├── E-commerce operations
└── AI assistant access

Client (Limited Access)
├── AI assistant only
├── Limited portal views
├── Account management
└── Basic support features
```

### Security Implementation
- **JWT Token Management**: Secure token generation and validation
- **Session Security**: HTTP-only cookies with CSRF protection
- **Cross-Platform Sessions**: Shared authentication state
- **Role-Based Access**: Fine-grained permission control
- **Multi-Tenant Isolation**: Data separation at database level

---

## 🌐 Network & Service Discovery

### Port Allocation
```
Frontend Services:
├── 3000: Bizoholic Marketing Platform
├── 3001: BizOSaaS Admin Dashboard
├── 3002: CoreLDove E-commerce Platform (Primary Login Portal)
└── 3003: AI Chat Service

Backend Services:
├── 8001: AI Agents Orchestration
├── 8002/8080: Brain API Gateway
├── 8003: Business Directory Service
├── 8007: Authentication Service v2
├── 8009: Analytics AI Service
└── 8088: Apache Superset

Infrastructure:
├── 5000: SQL Admin Dashboard
├── 5432: PostgreSQL Database
├── 6379: Redis Cache
└── 9000: ClickHouse Analytics
```

### Service Communication
- **Container-to-Container**: `host.docker.internal` for backend communication
- **Browser Access**: `localhost` URLs for frontend access
- **API Gateway**: Central routing through Brain API Gateway
- **Health Checks**: Automated service health monitoring
- **Load Balancing**: Traffic distribution across service instances

---

## 🚀 Deployment Architecture

### Development Environment
```
Docker Compose Setup:
├── docker-compose.yml - Main service orchestration
├── docker-compose.project.yml - Project-specific services
├── .env - Environment configuration
└── start-project.sh - Automated startup script
```

### Container Configuration
- **Unified Authentication**: Integrated across all services
- **Shared Networks**: Docker network for service communication
- **Volume Mounts**: Persistent data storage
- **Health Checks**: Service availability monitoring
- **Auto-Restart**: Automatic service recovery

### Production Deployment
```
Domain Architecture:
├── bizosaas.com (Primary Login Portal)
├── admin.bizosaas.com (BizOSaaS Admin)
├── bizoholic.bizosaas.com (Marketing Platform)
├── chat.bizosaas.com (AI Assistant)
├── directory.bizosaas.com (Business Directory)
└── sql.bizosaas.com (Infrastructure Admin)
```

---

## 🔧 Configuration Management

### Environment Variables
```bash
# Authentication Configuration
UNIFIED_AUTH_URL=http://host.docker.internal:8007
UNIFIED_AUTH_BROWSER_URL=http://localhost:3002
JWT_SECRET=your-jwt-secret-key

# Platform URLs
BIZOHOLIC_URL=http://localhost:3000
CORELDOVE_URL=http://localhost:3002
AI_CHAT_URL=http://localhost:3003
DIRECTORY_API_URL=http://localhost:8003

# Database Configuration
POSTGRES_URL=postgresql://user:pass@localhost:5432/bizosaas
REDIS_URL=redis://localhost:6379/0

# API Keys (BYOK Model)
OPENAI_API_KEY=user-provided
ANTHROPIC_API_KEY=user-provided
GOOGLE_API_KEY=user-provided
```

### Service Dependencies
```
Startup Order:
1. PostgreSQL + Redis (Data layer)
2. Authentication Service v2 (Security layer)
3. Brain API Gateway (Coordination layer)
4. Backend Services (Business logic)
5. Frontend Services (User interface)
```

---

## 📊 Monitoring & Observability

### Health Monitoring
- **Platform Health Checks**: Real-time status monitoring
- **Service Discovery**: Automatic service registration
- **Performance Metrics**: Response time and throughput
- **Error Tracking**: Centralized error logging
- **Alert System**: Automated notifications

### Analytics & Insights
- **Cross-Platform Analytics**: User journey tracking
- **AI Performance Metrics**: Agent execution monitoring
- **Business Intelligence**: Revenue and engagement analytics
- **Real-Time Dashboards**: Live performance updates
- **Predictive Analytics**: AI-powered forecasting

---

## 🔄 Data Flow Architecture

### Cross-Platform Data Synchronization
```
User Action → Platform Service → Brain API Gateway → Event Bus → Data Store
├── Real-time updates across platforms
├── Event-driven architecture
├── Multi-tenant data isolation
└── Audit trail maintenance
```

### AI Agent Communication
```
Agent Request → Agent Orchestration → Cross-Agent Communication → Result Aggregation
├── Pattern-specific agent coordination
├── Context sharing between agents
├── Performance optimization
└── Multi-tenant execution
```

---

## 🛠️ Maintenance & Troubleshooting

### Common Issues & Solutions
1. **Authentication Problems**: Check Auth Service v2 connectivity
2. **Platform Access Issues**: Verify role permissions and JWT tokens
3. **Cross-Platform Navigation**: Ensure session validation working
4. **Service Communication**: Check Docker network connectivity
5. **Performance Issues**: Monitor Redis cache and database queries

### Restart Procedures
1. **Full System Restart**: `docker-compose down && docker-compose up -d`
2. **Service-Specific Restart**: `docker-compose restart <service-name>`
3. **Development Mode**: `npm run start:shared` (with shared infrastructure)
4. **Health Verification**: Check all platform health endpoints

### Log Locations
- **Application Logs**: `docker-compose logs <service-name>`
- **Authentication Logs**: Auth Service v2 container logs
- **API Gateway Logs**: Brain API Gateway container logs
- **Database Logs**: PostgreSQL container logs
- **Cache Logs**: Redis container logs

---

## 📝 Key Implementation Files

### Critical Configuration Files
- `/home/alagiri/projects/bizoholic/bizosaas-platform/UNIFIED_PLATFORM_FLOW_ARCHITECTURE.md`
- `/home/alagiri/projects/bizoholic/bizosaas-platform/AUTHENTICATION_FLOW_IMPLEMENTATION.md`
- `/home/alagiri/projects/bizoholic/comprehensive_implementation_task_plan_06092025.md`
- `/home/alagiri/projects/bizoholic/comprehensive_prd_06092025.md`

### Main Service Files
- `core/services/tailadmin-dashboard/main_unified.py` - BizOSaaS Admin backend
- `ecommerce/services/coreldove-frontend/app/page.tsx` - CoreLDove homepage
- `ecommerce/services/coreldove-frontend/app/dashboard/page.tsx` - Consolidated dashboard
- `core/services/auth-service-v2/auth_security.py` - Authentication & RBAC
- `ai/services/bizosaas-brain/main.py` - Brain API Gateway

### Shared Components
- `core/services/shared-ui/platform-tabs.tsx` - React navigation component
- `core/services/tailadmin-dashboard/html/platform-switcher.html` - HTML navigation

---

*This comprehensive architecture reference ensures complete understanding of the BizOSaaS unified platform system for maintenance, troubleshooting, and future development.*