# 📋 Phase 1: Infrastructure & Deployment Fixes (Week 1)

## 🎯 Phase Objective
Fix current deployment issues, build proper Docker images, and ensure all services are accessible from the browser with proper health checks.

## ⚠️ Current Issues Identified
- Services failing in K3s (CrashLoopBackOff status)
- Containers building dependencies at runtime instead of using proper images
- Health check endpoints not responding (connection refused)
- Services not accessible from browser despite NodePort configuration

---

## 📦 Task 1.1: Container Image Building & Optimization

### 1.1.1 Identity Service Docker Image
- **Status**: 🔄 IN PROGRESS
- **Priority**: HIGH
- **Estimated Time**: 2 hours

**Tasks:**
- [ ] Fix Dockerfile to pre-install all Python dependencies
- [ ] Implement multi-stage build for optimization
- [ ] Add proper health check endpoint (`/health`)
- [ ] Configure service to bind to `0.0.0.0:8001` not localhost
- [ ] Test image locally before K8s deployment

**Acceptance Criteria:**
- Container starts successfully without CrashLoopBackOff
- Health check endpoint returns 200 OK
- Service accessible via `curl http://localhost:30101/health`

### 1.1.2 AI Orchestrator Service Docker Image
- **Status**: ⏳ PENDING
- **Priority**: HIGH  
- **Estimated Time**: 3 hours

**Tasks:**
- [ ] Create optimized Dockerfile with CrewAI dependencies
- [ ] Pre-install PyTorch and LangChain in image layers
- [ ] Configure shared model volume mounting
- [ ] Implement proper startup sequence with health checks
- [ ] Add graceful shutdown handling

**Acceptance Criteria:**
- CrewAI agents initialize successfully
- Model loading completes within 30 seconds
- Health endpoint responds with agent status
- Service accessible via `curl http://localhost:30102/health`

### 1.1.3 CRM Service Docker Image
- **Status**: ⏳ PENDING
- **Priority**: MEDIUM
- **Estimated Time**: 2 hours

**Tasks:**
- [ ] Build FastAPI CRM service image
- [ ] Include database migration scripts
- [ ] Configure PostgreSQL connection pooling
- [ ] Add lead scoring AI integration endpoints
- [ ] Implement proper error handling and logging

**Acceptance Criteria:**
- Database connection established successfully
- CRUD operations for leads/contacts working
- AI scoring endpoints responding
- Service accessible via `curl http://localhost:30104/health`

### 1.1.4 Analytics Service Docker Image
- **Status**: ⏳ PENDING
- **Priority**: MEDIUM
- **Estimated Time**: 2 hours

**Tasks:**
- [ ] Build analytics service with Porter Metrics templates
- [ ] Include report generation dependencies (Pandas, Matplotlib)
- [ ] Configure data pipeline connections
- [ ] Add real-time metrics endpoints
- [ ] Implement caching for dashboard queries

**Acceptance Criteria:**
- Report generation working (JSON, CSV, PDF)
- Dashboard metrics endpoints responding
- Data aggregation pipelines functional
- Service accessible via `curl http://localhost:30105/health`

### 1.1.5 Frontend Next.js Image
- **Status**: ⏳ PENDING
- **Priority**: HIGH
- **Estimated Time**: 1.5 hours

**Tasks:**
- [ ] Create production Next.js Docker image
- [ ] Configure environment variables for API endpoints
- [ ] Optimize image size with multi-stage build
- [ ] Add nginx serving for static assets (optional)
- [ ] Configure proper CORS and API routing

**Acceptance Criteria:**
- Frontend loads successfully in browser
- API connections to backend services working
- ShadCN UI components rendering correctly
- Accessible via `http://localhost:30100`

---

## 🛠️ Task 1.2: Service Configuration & Health Checks

### 1.2.1 Health Check Endpoint Implementation
- **Status**: ⏳ PENDING
- **Priority**: HIGH
- **Estimated Time**: 1 hour

**Tasks:**
- [ ] Implement `/health` endpoint for all FastAPI services
- [ ] Add dependency checks (database, Redis connections)
- [ ] Return service status, version, and uptime information
- [ ] Configure K8s liveness and readiness probes
- [ ] Add graceful degradation for partial failures

**Implementation:**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "identity-service",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "dependencies": {
            "database": "connected",
            "redis": "connected"
        }
    }
```

### 1.2.2 Service Binding Configuration
- **Status**: ⏳ PENDING
- **Priority**: HIGH
- **Estimated Time**: 30 minutes

**Tasks:**
- [ ] Configure all services to bind to `0.0.0.0` instead of `localhost`
- [ ] Update uvicorn/FastAPI host configuration
- [ ] Verify port bindings match K8s service definitions
- [ ] Test internal service-to-service communication
- [ ] Document service discovery patterns

**Configuration:**
```python
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Not localhost!
        port=8001,
        reload=False,
        workers=1
    )
```

### 1.2.3 Environment Variables & Secrets
- **Status**: ⏳ PENDING
- **Priority**: MEDIUM
- **Estimated Time**: 1 hour

**Tasks:**
- [ ] Create K8s ConfigMaps for non-sensitive configuration
- [ ] Create K8s Secrets for API keys and credentials
- [ ] Update service deployments to use ConfigMaps/Secrets
- [ ] Document required environment variables per service
- [ ] Add validation for required environment variables at startup

---

## 🗄️ Task 1.3: Database & Infrastructure Setup

### 1.3.1 PostgreSQL with pgvector Setup
- **Status**: ⏳ PENDING
- **Priority**: HIGH
- **Estimated Time**: 2 hours

**Tasks:**
- [ ] Verify pgvector extension is installed and enabled
- [ ] Create initial database schema with multi-tenant support
- [ ] Set up connection pooling configuration
- [ ] Create database migration system (Alembic)
- [ ] Add row-level security policies for tenant isolation

**Database Schema:**
```sql
-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Core tenant table
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Users with tenant isolation
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    email VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_email_per_tenant UNIQUE(tenant_id, email)
);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
```

### 1.3.2 Redis Configuration
- **Status**: ⏳ PENDING
- **Priority**: MEDIUM
- **Estimated Time**: 1 hour

**Tasks:**
- [ ] Configure Redis for session storage and caching
- [ ] Set up Redis pub/sub for inter-service communication
- [ ] Add Redis connection health checks to services
- [ ] Configure memory limits and eviction policies
- [ ] Document Redis key naming conventions

### 1.3.3 Service Discovery Setup
- **Status**: ⏳ PENDING
- **Priority**: MEDIUM
- **Estimated Time**: 1 hour

**Tasks:**
- [ ] Verify K8s service DNS resolution working
- [ ] Update service configurations to use K8s service names
- [ ] Test inter-service communication within cluster
- [ ] Document service endpoint URLs for development
- [ ] Add connection retry logic with exponential backoff

**Service URLs:**
```yaml
Internal Communication:
  - identity-service: http://bizosaas-identity.bizosaas-dev.svc.cluster.local:8001
  - ai-orchestrator: http://bizosaas-ai-orchestrator.bizosaas-dev.svc.cluster.local:8002
  - crm-service: http://bizosaas-crm.bizosaas-dev.svc.cluster.local:8004
  - analytics-service: http://bizosaas-analytics.bizosaas-dev.svc.cluster.local:8005

External Access (NodePorts):
  - frontend: http://localhost:30100
  - identity: http://localhost:30101
  - ai-orchestrator: http://localhost:30102
  - crm: http://localhost:30104
  - analytics: http://localhost:30105
```

---

## 🔍 Task 1.4: Testing & Validation

### 1.4.1 Service Health Validation
- **Status**: ⏳ PENDING
- **Priority**: HIGH
- **Estimated Time**: 1 hour

**Tasks:**
- [ ] Create automated health check script
- [ ] Test all service endpoints via NodePorts
- [ ] Verify inter-service communication
- [ ] Load test basic functionality
- [ ] Document any remaining issues

**Health Check Script:**
```bash
#!/bin/bash
services=(
    "http://localhost:30101/health:Identity"
    "http://localhost:30102/health:AI-Orchestrator"
    "http://localhost:30104/health:CRM"
    "http://localhost:30105/health:Analytics"
    "http://localhost:30100/:Frontend"
)

for service in "${services[@]}"; do
    url=$(echo $service | cut -d: -f1-3)
    name=$(echo $service | cut -d: -f4)
    
    if curl -f -s "$url" > /dev/null; then
        echo "✅ $name is healthy"
    else
        echo "❌ $name is not responding"
    fi
done
```

### 1.4.2 Browser Accessibility Testing
- **Status**: ⏳ PENDING
- **Priority**: HIGH
- **Estimated Time**: 30 minutes

**Tasks:**
- [ ] Test frontend loading in browser at `http://localhost:30100`
- [ ] Verify API endpoints accessible via browser network tools
- [ ] Test authentication flow (if implemented)
- [ ] Validate ShadCN UI components rendering
- [ ] Check responsive design on mobile/tablet

---

## 📊 Phase 1 Success Metrics

### Technical Metrics
- [ ] All services show "Running" status in K8s (no CrashLoopBackOff)
- [ ] All health endpoints return HTTP 200 OK
- [ ] Frontend accessible and fully functional in browser
- [ ] Database connections established and tested
- [ ] Inter-service communication working

### Performance Metrics
- [ ] Container startup time: <30 seconds
- [ ] Health check response time: <100ms
- [ ] Frontend load time: <3 seconds
- [ ] API response time: <200ms
- [ ] Database query time: <50ms

### Accessibility Metrics
- [ ] Frontend: ✅ `http://localhost:30100`
- [ ] Identity API: ✅ `http://localhost:30101/health`
- [ ] AI Orchestrator: ✅ `http://localhost:30102/health`
- [ ] CRM Service: ✅ `http://localhost:30104/health`
- [ ] Analytics Service: ✅ `http://localhost:30105/health`

---

## 🚀 Phase 1 Completion Criteria

### Must-Have (Blocking for Phase 2)
- [ ] All services accessible from browser
- [ ] No CrashLoopBackOff pods in K8s cluster
- [ ] Database and Redis connections working
- [ ] Health checks responding correctly
- [ ] Frontend loads and displays properly

### Nice-to-Have (Can defer to Phase 2)
- [ ] Performance optimization
- [ ] Advanced monitoring setup
- [ ] SSL/TLS configuration
- [ ] Automated testing suite
- [ ] Advanced logging configuration

### Deliverables
- [ ] Working Docker images for all services
- [ ] Updated K8s manifests with correct image references
- [ ] Database schema initialization scripts
- [ ] Service health validation script
- [ ] Updated documentation with deployment instructions

---

**Estimated Total Time: 16-18 hours**  
**Target Completion: End of Week 1**  
**Next Phase**: Core Backend Development (Phase 2)