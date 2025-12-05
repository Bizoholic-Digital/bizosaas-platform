# BizOSaaS Platform - Claude Instructions

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

BizOSaaS Platform is a comprehensive AI-powered SaaS ecosystem built with a microservices architecture and **centralized FastAPI AI Agentic Hub**. The platform provides multi-tenant marketing agency and e-commerce solutions through unified frontend applications and intelligent backend orchestration.

## Core Architecture - CRITICAL

### **FastAPI AI Agentic Central Hub** (Port 8001)
**🔥 MANDATORY: ALL backend services are routed through the centralized FastAPI AI Agentic Hub**

```
Frontend Apps → FastAPI AI Central Hub (8001) → Backend Services
```

- **Hub URL**: `http://localhost:8001` (`NEXT_PUBLIC_API_BASE_URL`)
- **All API calls** use pattern: `/api/brain/{service}/{endpoint}`
- **No direct backend connections** - everything goes through the central hub
- **AI Integration**: Hub coordinates AI agents, workflows, and data processing

### Frontend Applications (All connect via Central Hub)

#### 1. **Bizoholic Frontend** (Port 3008) - Marketing Agency Website
- **Purpose**: Public marketing website for Bizoholic digital agency
- **Integration**: Wagtail CMS + Django CRM via `/api/brain/wagtail/` and `/api/brain/django-crm/`
- **Features**: Contact forms, blog, portfolio, pricing, lead generation

#### 2. **CorelDove Frontend** (Port 3007) - E-commerce Storefront  
- **Purpose**: E-commerce website for product sales
- **Integration**: Saleor e-commerce via `/api/brain/saleor/`
- **Features**: Product catalog, cart, checkout, orders, user management

#### 3. **Client Portal** (Port 3006) - Tenant Management
- **Purpose**: Client dashboard for managing their specific data
- **Integration**: Multi-tenant data via `/api/brain/` endpoints
- **Features**: CRM leads, content management, e-commerce orders (tenant-specific)

#### 4. **BizOSaaS Admin** (Port 3009) - Platform Administration
- **Purpose**: Super admin interface for platform management
- **Integration**: All services via `/api/brain/` endpoints  
- **Features**: User management, system monitoring, cross-tenant analytics

### Backend Services (All accessed via Central Hub)

#### 1. **Django CRM** - Customer Relationship Management
- **Access Pattern**: `/api/brain/django-crm/leads`, `/api/brain/django-crm/contacts`
- **Features**: Lead scoring, sales pipeline, customer tracking, automated workflows
- **Multi-tenant**: Row-level security, tenant isolation

#### 2. **Wagtail CMS** - Content Management System
- **Access Pattern**: `/api/brain/wagtail/pages`, `/api/brain/wagtail/contact`
- **Features**: Dynamic content, blog management, forms, SEO optimization
- **Multi-tenant**: Tenant-specific content trees

#### 3. **Saleor E-commerce** - E-commerce Engine  
- **Access Pattern**: `/api/brain/saleor/products`, `/api/brain/saleor/orders`
- **Features**: Product management, inventory, payments, shipping, discounts
- **Multi-tenant**: Tenant-specific stores and catalogs

## API Architecture Patterns

### Standard API Route Structure
```typescript
// ✅ CORRECT - All routes go through central hub
const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'
const response = await fetch(`${BRAIN_API_URL}/api/brain/django-crm/leads`, {
  headers: {
    'Content-Type': 'application/json',
    'Host': 'localhost:3000',
  },
  body: JSON.stringify(data)
})

// ❌ WRONG - Direct backend connections
const response = await fetch('http://localhost:8000/django-crm/leads')
```

### Fallback Pattern for Development
```typescript
// Always include fallback data for development
if (!response.ok) {
  console.error('FastAPI AI Central Hub error:', response.status)
  return NextResponse.json(fallbackData, { status: 200 })
}
```

## Key Integrations

### 1. **Contact Form Integration** (Bizoholic)
- **Dual Submission**: Wagtail CMS + Django CRM in parallel
- **Lead Scoring**: Automatic calculation (0-100 scale)
- **Automation**: Welcome emails, sales assignment, follow-up tasks

### 2. **E-commerce Integration** (CorelDove)
- **Complete Saleor API**: Products, cart, checkout, payment, orders, shipping, auth, addresses, wishlist
- **Multi-gateway Payments**: Stripe, PayPal integration via central hub
- **Inventory Management**: Real-time stock tracking

### 3. **Multi-tenant Architecture**
- **Tenant Isolation**: Row-level security across all services
- **Data Segregation**: Each client sees only their data
- **Unified Authentication**: Single sign-on across platforms

## Development Workflow

### Environment Variables
```bash
# Central Hub Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001

# Never use these direct URLs:
# DJANGO_URL=http://localhost:8000  ❌
# WAGTAIL_URL=http://localhost:8002 ❌  
# SALEOR_URL=http://localhost:8003  ❌
```

### Port Configuration
- **8001**: FastAPI AI Agentic Central Hub (MAIN)
- **3006**: Client Portal (tenant dashboards)
- **3007**: CorelDove Frontend (e-commerce)
- **3008**: Bizoholic Frontend (marketing)
- **3009**: BizOSaaS Admin (platform admin)

### Development Commands
```bash
# Start all frontend applications
cd /home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/bizoholic-frontend && npm run dev
cd /home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/coreldove-frontend && npm run dev  
cd /home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/client-portal && npm run dev
cd /home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/bizosaas-admin && npm run dev
```

## AI Integration Features

### 1. **Lead Scoring Algorithm**
- Automatic scoring based on: company info, contact details, budget, service interest, engagement
- Real-time scoring updates via central hub AI agents

### 2. **Content Personalization**
- Dynamic content delivery via Wagtail + AI recommendations
- Personalized product recommendations via Saleor + AI analysis

### 3. **Automated Workflows**
- Lead nurturing sequences via Django CRM + AI agents
- Inventory optimization via Saleor + AI predictions
- Content optimization via Wagtail + AI analysis

## Security Considerations

### 1. **Multi-tenant Security**
- Row-level security (RLS) on all database tables
- Tenant context propagated through central hub
- API key encryption for external integrations

### 2. **Authentication Flow**
- JWT tokens managed by central hub
- Single sign-on across all frontend applications  
- Role-based access control (RBAC)

### 3. **Data Privacy**
- GDPR compliance built into central hub
- Audit logging for all data access
- Encryption at rest and in transit

## Common Development Patterns

### 1. **API Route Creation**
```typescript
// frontend/apps/{app}/app/api/brain/{service}/{endpoint}/route.ts
export async function POST(request: NextRequest) {
  const response = await fetch(`${BRAIN_API_URL}/api/brain/{service}/{endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Host': 'localhost:3000',
    },
    body: JSON.stringify(await request.json())
  })
  
  if (!response.ok) {
    return NextResponse.json(fallbackData, { status: 200 })
  }
  
  return NextResponse.json(await response.json())
}
```

### 2. **Frontend API Consumption**
```typescript
// Always use relative URLs to frontend API routes
const response = await fetch('/api/brain/django-crm/leads', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(leadData)
})
```

### 3. **Error Handling**
```typescript
// Graceful degradation with fallback data
try {
  const response = await fetch(apiUrl)
  if (!response.ok) throw new Error()
  return await response.json()
} catch (error) {
  console.error('Central hub error:', error)
  return fallbackData // Always provide fallback
}
```

## Platform-Specific Notes

### Bizoholic Frontend (3008)
- **Primary Purpose**: Lead generation and marketing content
- **Key Features**: Contact forms, blog, case studies, pricing
- **Backend Integration**: Wagtail CMS + Django CRM

### CorelDove Frontend (3007)  
- **Primary Purpose**: E-commerce sales and customer management
- **Key Features**: Product catalog, shopping cart, order management
- **Backend Integration**: Saleor e-commerce platform

### Client Portal (3006)
- **Primary Purpose**: Tenant-specific data management
- **Key Features**: CRM leads, content editing, order tracking
- **Backend Integration**: Multi-tenant access to all services

### BizOSaaS Admin (3009)
- **Primary Purpose**: Platform administration and monitoring
- **Key Features**: User management, system analytics, tenant management  
- **Backend Integration**: Administrative access to all services

## Future Enhancements

### 1. **Amazon API Integration**
- Dropship product sourcing via `/api/brain/amazon/products`
- AI-powered product validation with HITL workflows
- Automated inventory synchronization

### 2. **Advanced AI Features**
- Predictive analytics for sales forecasting
- Automated content generation for marketing
- Intelligent customer segmentation

### 3. **Enterprise Features**
- White-label deployment options
- Advanced multi-tenant customization
- Enterprise SSO integration

---

## 🚨 CRITICAL REMINDERS

1. **NEVER** connect directly to backend services
2. **ALWAYS** route through FastAPI AI Central Hub (port 8001)
3. **ALL** API routes follow `/api/brain/{service}/` pattern
4. **INCLUDE** fallback data for development/testing
5. **MAINTAIN** multi-tenant isolation in all operations
6. **LOG** all central hub communications for debugging

This architecture ensures scalability, maintainability, and intelligent orchestration across the entire BizOSaaS ecosystem.