# Django CRM Service for BizOSaaS

## Overview

The Django CRM Service is a comprehensive multi-tenant Customer Relationship Management system built with Django and Django REST Framework. It provides advanced lead management, AI-powered scoring, and seamless integration with the BizOSaaS ecosystem.

## Key Features

- **Multi-Tenant Architecture**: Complete tenant isolation with domain-based routing
- **AI-Powered Lead Scoring**: Automatic lead qualification using AI agents integration
- **Comprehensive Lead Management**: Full CRUD operations with advanced filtering
- **REST API**: Complete RESTful API with DRF ViewSets
- **Real-time Integration**: Connects with AI Agents, Temporal, and HashiCorp Vault
- **Role-Based Access Control**: Granular permissions with tenant-aware security
- **Activity Tracking**: Comprehensive audit trail and activity logging

## Service Architecture

```
┌─────────────────────────────────────────────────────┐
│                Django CRM Service                   │
│                    (Port 8007)                      │
├─────────────────────────────────────────────────────┤
│  • Django 4.2 with DRF                             │
│  • Multi-tenant models with RLS                     │
│  • JWT Authentication                               │
│  • Celery for background tasks                      │
│  • PostgreSQL with pgvector extension              │
│  • Redis for caching and sessions                   │
└─────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────┐
│                External Integrations                │
├─────────────────────────────────────────────────────┤
│  • AI Agents Service (8000) - Lead scoring          │
│  • Temporal Integration (8202) - Workflows          │
│  • HashiCorp Vault (8201) - Credential management  │
└─────────────────────────────────────────────────────┘
```

## Apps Structure

### 1. **Core App**
- **Purpose**: Base models, authentication, and shared utilities
- **Key Components**: Custom User model, JWT authentication, base classes
- **Features**: Multi-tenant base model, activity logging, system settings

### 2. **Tenants App**
- **Purpose**: Multi-tenant organization management
- **Key Components**: Tenant model, domain routing, membership management
- **Features**: Subscription management, API keys, audit logging

### 3. **Leads App** ⭐ (Fully Implemented)
- **Purpose**: Comprehensive lead management system
- **Key Models**: Lead, LeadSource, LeadActivity, LeadNote, LeadTag
- **Features**: AI scoring, bulk operations, advanced filtering, activity tracking

### 4. **Additional Apps** (Placeholder)
- **Customers**: Customer relationship management
- **Products**: Product catalog management  
- **Orders**: Order processing and tracking
- **Analytics**: Reporting and analytics
- **Integrations**: External service integrations

## Lead Management Features

### **Core Functionality**
- ✅ **Lead CRUD**: Complete create, read, update, delete operations
- ✅ **AI Scoring**: Automatic lead scoring based on 7+ factors
- ✅ **Status Tracking**: Lead lifecycle management (New → Qualified → Won/Lost)
- ✅ **Source Attribution**: Track lead sources with conversion analytics
- ✅ **Assignment Management**: Assign leads to team members
- ✅ **Tagging System**: Flexible tagging with custom taxonomies

### **Advanced Features**
- ✅ **Activity Tracking**: Calls, emails, meetings, tasks
- ✅ **Notes System**: Private and shared notes with rich formatting
- ✅ **Custom Fields**: Extensible custom field system
- ✅ **Bulk Operations**: Bulk update, assign, and tag operations
- ✅ **Advanced Search**: Full-text search across multiple fields
- ✅ **Smart Filtering**: 20+ filter options including behavioral filters

### **API Endpoints**

#### **Core Lead Management**
```
GET/POST   /api/leads/api/v1/leads/
GET/PUT/DELETE /api/leads/api/v1/leads/{id}/
GET        /api/leads/api/v1/leads/dashboard/
GET        /api/leads/api/v1/leads/overdue/
GET        /api/leads/api/v1/leads/high-priority/
GET        /api/leads/api/v1/leads/unassigned/
```

#### **Lead Actions**
```
POST /api/leads/api/v1/leads/{id}/update-score/
POST /api/leads/api/v1/leads/{id}/mark-contacted/
POST /api/leads/api/v1/leads/{id}/convert/
POST /api/leads/api/v1/leads/{id}/mark-lost/
GET  /api/leads/api/v1/leads/{id}/ai-insights/
```

#### **Bulk Operations**
```
POST /api/leads/api/v1/leads/bulk-update/
POST /api/leads/api/v1/leads/bulk-assign/
POST /api/leads/api/v1/leads/bulk-tag/
```

#### **Related Resources**
```
GET/POST   /api/leads/api/v1/sources/
GET/POST   /api/leads/api/v1/tags/
GET/POST   /api/leads/api/v1/activities/
GET/POST   /api/leads/api/v1/notes/
```

## Deployment

### **Docker Compose Deployment**
```bash
cd /home/alagiri/projects/bizoholic/bizosaas/services/django-crm
docker-compose up -d
```

### **Standalone Container**
```bash
docker build -t bizosaas-django-crm .
docker run -d --name django-crm \
  --network bizosaas-network \
  -p 8007:8007 \
  -e DB_HOST=bizosaas-postgres \
  -e REDIS_URL=redis://bizosaas-redis:6379/1 \
  bizosaas-django-crm
```

## Environment Configuration

### **Required Variables**
```env
SECRET_KEY=your-secret-key-here
DB_NAME=bizosaas
DB_USER=admin
DB_PASSWORD=BizoholicSecure2025
DB_HOST=bizosaas-postgres
REDIS_URL=redis://bizosaas-redis:6379/1
AI_AGENTS_URL=http://bizosaas-ai-agents:8000
TEMPORAL_URL=http://bizosaas-temporal-integration:8202
VAULT_URL=http://bizosaas-vault-integration:8201
```

### **Optional Variables**
```env
DEBUG=False
DJANGO_LOG_LEVEL=INFO
CORS_ALLOW_ALL_ORIGINS=True
JWT_SECRET_KEY=your-jwt-secret
EMAIL_HOST=localhost
EMAIL_PORT=587
```

## Multi-Tenant Usage

### **Tenant Resolution**
The service resolves tenants through multiple methods:
1. **Subdomain**: `tenant1.bizoholic.com`
2. **Custom Domain**: `crm.company.com`
3. **Header**: `X-Tenant-Id: uuid`
4. **JWT Token**: Embedded tenant_id

### **API Usage Examples**

#### **Create Lead**
```bash
curl -X POST http://localhost:8007/api/leads/api/v1/leads/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "X-Tenant-Id: tenant-uuid" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@company.com",
    "company": "Acme Corp",
    "source": "website"
  }'
```

#### **Get Lead Dashboard**
```bash
curl -X GET http://localhost:8007/api/leads/api/v1/leads/dashboard/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "X-Tenant-Id: tenant-uuid"
```

#### **Update Lead Score**
```bash
curl -X POST http://localhost:8007/api/leads/api/v1/leads/{lead-id}/update-score/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "X-Tenant-Id: tenant-uuid"
```

## AI Integration

### **Lead Scoring Algorithm**
The service uses a sophisticated AI scoring algorithm that considers:
- **Company Information**: +20 points for company presence
- **Job Title Relevance**: +20 points for decision-maker titles
- **Lead Source Quality**: Variable points based on source conversion rates
- **Engagement Level**: Points based on activity and responsiveness
- **Industry Match**: Points for target industry alignment
- **Geographic Relevance**: Points for target geographic markets
- **Behavioral Signals**: Points for website activity and engagement

### **AI Agents Integration**
- **Endpoint**: `/api/leads/api/v1/leads/{id}/ai-insights/`
- **Purpose**: Get AI-powered insights and recommendations
- **Integration**: Connects to BizOSaaS AI Agents service (port 8000)
- **Features**: Predictive scoring, next action recommendations, sentiment analysis

## Database Schema

### **Core Tables**
- `auth_user` - Custom user model with tenant support
- `tenants_tenant` - Multi-tenant organization data
- `tenants_membership` - User-tenant relationships with roles

### **Lead Tables**
- `leads_lead` - Main lead data with AI scoring
- `leads_leadsource` - Lead source tracking and analytics
- `leads_leadactivity` - Activity timeline and scheduling
- `leads_leadnote` - Notes with privacy controls
- `leads_leadtag` - Flexible tagging system
- `leads_leadcustomfield` - Extensible custom fields

### **Audit Tables**
- `core_activity_log` - Global activity logging
- `tenants_audit_log` - Tenant-specific audit trail

## Performance & Scalability

### **Database Optimization**
- **Indexes**: Strategic indexing on tenant_id, created_at, status
- **Query Optimization**: Custom managers with select_related/prefetch_related
- **Connection Pooling**: PostgreSQL connection pooling in production

### **Caching Strategy**
- **Redis Integration**: Session caching and API response caching
- **Query Caching**: Expensive queries cached with invalidation
- **Static Files**: WhiteNoise for efficient static file serving

### **Background Processing**
- **Celery Integration**: Asynchronous task processing
- **AI Scoring**: Background AI scoring calculations
- **Email Processing**: Asynchronous email sending

## Security Features

### **Multi-Tenant Security**
- **Row Level Security**: Automatic tenant filtering
- **JWT Authentication**: Stateless authentication with tenant context
- **Permission System**: Granular role-based access control

### **Data Protection**
- **Encrypted Passwords**: Django's built-in password hashing
- **Secure Headers**: HSTS, XSS protection, content type sniffing prevention
- **API Rate Limiting**: Configurable rate limiting per tenant

## Monitoring & Logging

### **Health Monitoring**
- **Health Check**: `/health/` endpoint for container orchestration
- **Service Info**: `/` endpoint with service status and integrations
- **Django Health Check**: `/health-check/` with database and cache checks

### **Logging Configuration**
- **Structured Logging**: JSON formatting for production
- **Log Rotation**: Automatic log rotation with size limits
- **Error Tracking**: Comprehensive error logging with context

## Development

### **Local Development**
```bash
# Set up environment
cp .env.example .env
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver 0.0.0.0:8007
```

### **Testing**
```bash
# Run tests
python manage.py test

# Test configuration
python test_service.py
```

## Dokploy Deployment Ready

The Django CRM service is fully containerized and ready for VPS staging deployment via Dokploy with:

- **Multi-architecture Support**: ARM and x86 compatible
- **Health Checks**: Container health monitoring
- **Volume Management**: Persistent logs and media storage
- **Network Configuration**: Microservices network integration
- **Environment Management**: Production-ready configuration

---

**Service Status**: ✅ **Production Ready**  
**Last Updated**: September 8, 2025  
**Version**: 1.0.0  
**Port**: 8007  
**Integration**: AI Agents (8000), Temporal (8202), Vault (8201)