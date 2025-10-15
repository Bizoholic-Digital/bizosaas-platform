# Backend Services API Reference
## BizOSaaS Platform - Phase 2 Services

### Quick Navigation
- [Brain API (8001)](#brain-api-port-8001)
- [Wagtail CMS (8002)](#wagtail-cms-port-8002)
- [Django CRM (8003)](#django-crm-port-8003)
- [Directory API (8004)](#directory-api-port-8004)
- [CorelDove Backend (8005)](#coreldove-backend-port-8005)
- [AI Agents (8010)](#ai-agents-service-port-8010)
- [Amazon Sourcing (8085)](#amazon-sourcing-api-port-8085)
- [Saleor E-commerce (8000)](#saleor-e-commerce-port-8000)

---

## Brain API (Port 8001)
**Main API coordinator and router**

### Base URL
```
http://194.238.16.237:8001
```

### Health Check
```bash
GET /health
Response: 200 OK
{
  "status": "healthy",
  "services": {
    "postgres": "connected",
    "redis": "connected",
    "vault": "accessible",
    "temporal": "connected"
  },
  "version": "1.0.0",
  "uptime": "24h 15m"
}
```

### Core Endpoints

#### Service Status
```bash
GET /api/status
Response: 200 OK
{
  "brain_api": "operational",
  "connected_services": 7,
  "active_requests": 42,
  "cache_hit_rate": 0.87
}
```

#### Route Information
```bash
GET /api/routes
Response: 200 OK
{
  "routes": [
    {"path": "/api/cms", "target": "wagtail-cms:8002"},
    {"path": "/api/crm", "target": "django-crm:8003"},
    {"path": "/api/directory", "target": "directory-api:8004"},
    {"path": "/api/commerce", "target": "coreldove-backend:8005"},
    {"path": "/api/ai", "target": "ai-agents:8010"},
    {"path": "/api/sourcing", "target": "amazon-sourcing:8085"},
    {"path": "/api/saleor", "target": "saleor-api:8000"}
  ]
}
```

#### Version Information
```bash
GET /version
Response: 200 OK
{
  "service": "brain-api",
  "version": "1.0.0",
  "build": "2025-10-10",
  "environment": "staging"
}
```

### Request Routing

All frontend requests should go through Brain API which routes to appropriate backend services:

```bash
# CMS requests
GET http://194.238.16.237:8001/api/cms/pages → routed to Wagtail

# CRM requests
GET http://194.238.16.237:8001/api/crm/clients → routed to Django CRM

# Commerce requests
POST http://194.238.16.237:8001/api/commerce/orders → routed to CorelDove

# AI requests
POST http://194.238.16.237:8001/api/ai/generate → routed to AI Agents
```

---

## Wagtail CMS (Port 8002)
**Headless content management system**

### Base URL
```
http://194.238.16.237:8002
```

### Health Check
```bash
GET /health/
Response: 200 OK
{
  "status": "ok",
  "database": "connected"
}
```

### Core Endpoints

#### Pages API (Wagtail API v2)
```bash
GET /api/v2/pages/
Response: 200 OK
{
  "meta": {
    "total_count": 42
  },
  "items": [
    {
      "id": 1,
      "title": "Home Page",
      "slug": "home",
      "url": "/home/"
    }
  ]
}
```

#### Page Detail
```bash
GET /api/v2/pages/:id/
Response: 200 OK
{
  "id": 1,
  "title": "Home Page",
  "slug": "home",
  "body": "...",
  "meta": {
    "type": "home.HomePage",
    "detail_url": "http://194.238.16.237:8002/api/v2/pages/1/"
  }
}
```

#### Documents API
```bash
GET /api/v2/documents/
Response: 200 OK
{
  "meta": {
    "total_count": 15
  },
  "items": [
    {
      "id": 1,
      "title": "Document.pdf",
      "download_url": "/documents/1/document.pdf"
    }
  ]
}
```

#### Images API
```bash
GET /api/v2/images/
Response: 200 OK
{
  "meta": {
    "total_count": 87
  },
  "items": [
    {
      "id": 1,
      "title": "Image.jpg",
      "width": 1920,
      "height": 1080
    }
  ]
}
```

### Admin Interface
```
http://194.238.16.237:8002/admin/
Credentials: Set during deployment
```

---

## Django CRM (Port 8003)
**Customer relationship management**

### Base URL
```
http://194.238.16.237:8003
```

### Health Check
```bash
GET /health/
Response: 200 OK
{
  "status": "healthy",
  "database": "connected",
  "cache": "operational"
}
```

### Core Endpoints

#### Clients List
```bash
GET /api/clients/
Response: 200 OK
{
  "count": 142,
  "results": [
    {
      "id": 1,
      "name": "Acme Corp",
      "email": "contact@acme.com",
      "status": "active",
      "created_at": "2025-10-01T10:00:00Z"
    }
  ]
}
```

#### Client Detail
```bash
GET /api/clients/:id/
Response: 200 OK
{
  "id": 1,
  "name": "Acme Corp",
  "email": "contact@acme.com",
  "phone": "+1234567890",
  "status": "active",
  "total_orders": 15,
  "lifetime_value": 25000.00
}
```

#### Leads List
```bash
GET /api/leads/
Response: 200 OK
{
  "count": 78,
  "results": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "status": "qualified",
      "score": 85,
      "created_at": "2025-10-09T15:30:00Z"
    }
  ]
}
```

#### Create Lead
```bash
POST /api/leads/
Content-Type: application/json

{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "source": "website",
  "notes": "Interested in enterprise plan"
}

Response: 201 Created
{
  "id": 79,
  "name": "Jane Smith",
  "status": "new",
  "score": 0,
  "created_at": "2025-10-10T12:00:00Z"
}
```

#### Contacts List
```bash
GET /api/contacts/
Response: 200 OK
{
  "count": 324,
  "results": [...]
}
```

### Admin Interface
```
http://194.238.16.237:8003/admin/
```

---

## Directory API (Port 8004)
**Business directory management**

### Base URL
```
http://194.238.16.237:8004
```

### Health Check
```bash
GET /health
Response: 200 OK
{
  "status": "ok",
  "version": "1.0.0"
}
```

### Core Endpoints

#### Businesses List
```bash
GET /api/businesses
Response: 200 OK
{
  "total": 1847,
  "page": 1,
  "per_page": 20,
  "businesses": [
    {
      "id": 1,
      "name": "Tech Solutions Inc",
      "category": "Technology",
      "location": "New York, NY",
      "rating": 4.5,
      "verified": true
    }
  ]
}
```

#### Business Detail
```bash
GET /api/businesses/:id
Response: 200 OK
{
  "id": 1,
  "name": "Tech Solutions Inc",
  "description": "...",
  "category": "Technology",
  "subcategory": "Software Development",
  "address": "123 Main St, New York, NY 10001",
  "phone": "+1234567890",
  "email": "info@techsolutions.com",
  "website": "https://techsolutions.com",
  "rating": 4.5,
  "reviews_count": 87,
  "verified": true,
  "hours": {
    "monday": "9:00-17:00",
    "tuesday": "9:00-17:00"
  }
}
```

#### Search Businesses
```bash
GET /api/businesses/search?q=tech&category=Technology&location=New York
Response: 200 OK
{
  "query": "tech",
  "results": 42,
  "businesses": [...]
}
```

#### Categories List
```bash
GET /api/categories
Response: 200 OK
{
  "categories": [
    {
      "id": 1,
      "name": "Technology",
      "count": 487,
      "subcategories": ["Software", "Hardware", "IT Services"]
    }
  ]
}
```

#### Business Reviews
```bash
GET /api/businesses/:id/reviews
Response: 200 OK
{
  "business_id": 1,
  "average_rating": 4.5,
  "total_reviews": 87,
  "reviews": [
    {
      "id": 1,
      "author": "John Doe",
      "rating": 5,
      "comment": "Great service!",
      "date": "2025-10-01"
    }
  ]
}
```

---

## CorelDove Backend (Port 8005)
**E-commerce API with payment processing**

### Base URL
```
http://194.238.16.237:8005
```

### Health Check
```bash
GET /health
Response: 200 OK
{
  "status": "healthy",
  "database": "connected",
  "stripe": "configured",
  "paypal": "configured"
}
```

### Core Endpoints

#### Products List
```bash
GET /api/products
Response: 200 OK
{
  "total": 1247,
  "page": 1,
  "products": [
    {
      "id": 1,
      "name": "Product Name",
      "price": 29.99,
      "currency": "USD",
      "in_stock": true,
      "images": ["url1", "url2"]
    }
  ]
}
```

#### Product Detail
```bash
GET /api/products/:id
Response: 200 OK
{
  "id": 1,
  "name": "Product Name",
  "description": "...",
  "price": 29.99,
  "sale_price": 24.99,
  "currency": "USD",
  "sku": "PROD-001",
  "in_stock": true,
  "quantity": 150,
  "images": [...],
  "specifications": {...},
  "reviews": {...}
}
```

#### Shopping Cart
```bash
GET /api/cart/:session_id
Response: 200 OK
{
  "session_id": "abc123",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 29.99,
      "subtotal": 59.98
    }
  ],
  "total": 59.98,
  "currency": "USD"
}

POST /api/cart
{
  "session_id": "abc123",
  "product_id": 1,
  "quantity": 2
}
Response: 201 Created
```

#### Orders
```bash
POST /api/orders
Content-Type: application/json

{
  "customer": {
    "name": "John Doe",
    "email": "john@example.com",
    "address": {...}
  },
  "items": [
    {"product_id": 1, "quantity": 2}
  ],
  "payment_method": "stripe"
}

Response: 201 Created
{
  "order_id": "ORD-12345",
  "status": "pending",
  "total": 59.98,
  "payment_url": "https://checkout.stripe.com/..."
}
```

#### Payment Processing (Stripe)
```bash
POST /api/payments/stripe/checkout
{
  "order_id": "ORD-12345",
  "return_url": "https://coreldove.com/success"
}

Response: 200 OK
{
  "checkout_session_id": "cs_test_...",
  "checkout_url": "https://checkout.stripe.com/..."
}
```

#### Payment Processing (PayPal)
```bash
POST /api/payments/paypal/create-order
{
  "order_id": "ORD-12345",
  "return_url": "https://coreldove.com/success"
}

Response: 200 OK
{
  "paypal_order_id": "PAYPAL-123",
  "approval_url": "https://paypal.com/checkoutnow?..."
}
```

---

## AI Agents Service (Port 8010)
**Multi-model AI coordination**

### Base URL
```
http://194.238.16.237:8010
```

### Health Check
```bash
GET /health
Response: 200 OK
{
  "status": "healthy",
  "ai_models": "ready",
  "openrouter": "connected",
  "temporal": "connected"
}
```

### Core Endpoints

#### Generate Content
```bash
POST /api/generate
Content-Type: application/json

{
  "model": "gpt-4",
  "prompt": "Write a product description for...",
  "max_tokens": 500,
  "temperature": 0.7
}

Response: 200 OK
{
  "generated_text": "...",
  "model_used": "openai/gpt-4",
  "tokens_used": 287,
  "cost": 0.00861
}
```

#### Available Models
```bash
GET /api/models
Response: 200 OK
{
  "models": [
    {
      "id": "openai/gpt-4",
      "name": "GPT-4",
      "provider": "OpenAI",
      "cost_per_1k_tokens": 0.03
    },
    {
      "id": "anthropic/claude-3-sonnet",
      "name": "Claude 3 Sonnet",
      "provider": "Anthropic",
      "cost_per_1k_tokens": 0.015
    }
  ]
}
```

#### Agent Task
```bash
POST /api/agents/task
{
  "agent_type": "marketing",
  "task": "Create social media campaign",
  "parameters": {
    "product": "New Widget",
    "target_audience": "Tech enthusiasts"
  }
}

Response: 202 Accepted
{
  "task_id": "task-123",
  "status": "processing",
  "estimated_time": "30 seconds"
}
```

#### Task Status
```bash
GET /api/agents/task/:task_id
Response: 200 OK
{
  "task_id": "task-123",
  "status": "completed",
  "result": {
    "campaign": {...},
    "posts": [...]
  }
}
```

---

## Amazon Sourcing API (Port 8085)
**Product sourcing integration**

### Base URL
```
http://194.238.16.237:8085
```

### Health Check
```bash
GET /health
Response: 200 OK
{
  "status": "ok",
  "amazon_api": "connected"
}
```

### Core Endpoints

#### Search Products
```bash
GET /api/search?q=laptop&category=Electronics&min_price=500&max_price=2000
Response: 200 OK
{
  "query": "laptop",
  "total_results": 1847,
  "products": [
    {
      "asin": "B08N5WRWNW",
      "title": "Laptop Model XYZ",
      "price": 899.99,
      "rating": 4.5,
      "reviews_count": 3241,
      "image_url": "...",
      "prime": true
    }
  ]
}
```

#### Product Details
```bash
GET /api/products/:asin
Response: 200 OK
{
  "asin": "B08N5WRWNW",
  "title": "Laptop Model XYZ",
  "description": "...",
  "price": 899.99,
  "currency": "USD",
  "availability": "in_stock",
  "rating": 4.5,
  "reviews_count": 3241,
  "images": [...],
  "features": [...],
  "specifications": {...}
}
```

#### Price History
```bash
GET /api/products/:asin/price-history
Response: 200 OK
{
  "asin": "B08N5WRWNW",
  "current_price": 899.99,
  "lowest_price_30d": 849.99,
  "highest_price_30d": 949.99,
  "average_price": 889.99,
  "history": [
    {"date": "2025-10-01", "price": 899.99},
    {"date": "2025-10-02", "price": 889.99}
  ]
}
```

#### Bulk Import
```bash
POST /api/import
Content-Type: application/json

{
  "asins": ["B08N5WRWNW", "B07X5LNTKV", "B09JQKB7QC"],
  "target_store": "coreldove"
}

Response: 202 Accepted
{
  "job_id": "import-123",
  "status": "processing",
  "asins_count": 3
}
```

---

## Saleor E-commerce (Port 8000)
**Advanced e-commerce engine with GraphQL**

### Base URL
```
http://194.238.16.237:8000
```

### Health Check
```bash
GET /health/
Response: 200 OK
{
  "status": "ok"
}
```

### GraphQL Endpoint
```
http://194.238.16.237:8000/graphql/
```

### GraphQL Examples

#### Get Products
```graphql
query {
  products(first: 10) {
    edges {
      node {
        id
        name
        description
        pricing {
          priceRange {
            start {
              gross {
                amount
                currency
              }
            }
          }
        }
        thumbnail {
          url
        }
      }
    }
  }
}
```

#### Get Product Detail
```graphql
query {
  product(id: "UHJvZHVjdDox") {
    id
    name
    description
    variants {
      id
      name
      pricing {
        price {
          gross {
            amount
            currency
          }
        }
      }
      quantityAvailable
    }
    images {
      url
    }
  }
}
```

#### Create Checkout
```graphql
mutation {
  checkoutCreate(input: {
    lines: [
      {
        quantity: 1
        variantId: "UHJvZHVjdFZhcmlhbnQ6MQ=="
      }
    ]
  }) {
    checkout {
      id
      totalPrice {
        gross {
          amount
          currency
        }
      }
    }
    errors {
      message
    }
  }
}
```

#### Complete Order
```graphql
mutation {
  checkoutComplete(
    checkoutId: "Q2hlY2tvdXQ6MQ=="
  ) {
    order {
      id
      number
      status
    }
    errors {
      message
    }
  }
}
```

### GraphQL Playground
```
http://194.238.16.237:8000/graphql/
Interactive playground for testing queries
```

### Admin Dashboard
```
http://194.238.16.237:8000/dashboard/
Saleor admin interface for order management
```

---

## Authentication & Security

### API Key Authentication
Most endpoints require API key authentication:

```bash
# In request headers
Authorization: Bearer <your-api-key>
```

### Rate Limiting
- **Standard tier**: 1000 requests/hour
- **Premium tier**: 10,000 requests/hour
- **Rate limit headers**:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

### CORS Configuration
Staging environment allows:
- `https://stg.bizoholic.com`
- `https://stg.coreldove.com`
- `http://localhost:3000` (development)

---

## Error Handling

### Standard Error Response
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {...},
    "timestamp": "2025-10-10T12:00:00Z"
  }
}
```

### Common HTTP Status Codes
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily down

---

## Testing All Endpoints

### Quick Health Check Script
```bash
#!/bin/bash
services=(
  "8001:/health:Brain API"
  "8002:/health/:Wagtail CMS"
  "8003:/health/:Django CRM"
  "8004:/health:Directory API"
  "8005:/health:CorelDove"
  "8010:/health:AI Agents"
  "8085:/health:Amazon Sourcing"
  "8000:/health/:Saleor"
)

for service in "${services[@]}"; do
  IFS=':' read -r port endpoint name <<< "$service"
  echo -n "$name: "
  curl -s -o /dev/null -w "%{http_code}" http://194.238.16.237:$port$endpoint
  echo ""
done
```

---

## Support & Documentation

### API Documentation Links
- **Wagtail API**: http://194.238.16.237:8002/api/v2/
- **Saleor GraphQL**: http://194.238.16.237:8000/graphql/
- **Brain API Docs**: http://194.238.16.237:8001/docs

### Postman Collection
Available at: `./postman/bizosaas-backend-staging.json`

### OpenAPI Specs
- Brain API: `http://194.238.16.237:8001/openapi.json`
- Directory API: `http://194.238.16.237:8004/openapi.json`
- CorelDove: `http://194.238.16.237:8005/openapi.json`

---

**Document Version**: 1.0
**Last Updated**: October 10, 2025
**Environment**: Staging
**VPS**: 194.238.16.237
