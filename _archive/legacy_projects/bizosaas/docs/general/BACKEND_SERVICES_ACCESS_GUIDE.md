# Backend Services Access Guide
## Bizoholic Digital Platform Infrastructure

🎯 **Platform Overview**: Complete AI Marketing SaaS with CMS, E-commerce, and CRM Integration  
📅 **Last Updated**: January 15, 2025  
🏗️ **Architecture**: Microservices with Docker Compose + Shared Infrastructure  

---

## 🚀 Quick Start Commands

### Start All Backend Services
```bash
# Navigate to BizoSaaS directory
cd /home/alagiri/projects/bizoholic/bizosaas

# Start complete development environment
docker-compose -f docker-compose.dev.yml up -d

# Or start specific services
docker-compose -f docker-compose.dev.yml up -d strapi postgres redis
```

### Health Check All Services
```bash
# Check all running services
docker-compose -f docker-compose.dev.yml ps

# View logs for specific service
docker-compose -f docker-compose.dev.yml logs -f strapi
```

---

## 📊 Service Overview & Access URLs

### 🎯 Core Frontend Services
| Service | URL | Port | Status | Purpose |
|---------|-----|------|--------|---------|
| **Bizoholic Website** | http://localhost:3000 | 3000 | ✅ Running | Main marketing site & BizoSaaS platform |
| **CoreLDove Store** | http://localhost:3001 | 3001 | ✅ Running | Dropshipping marketplace (existing) |

### 🗄️ Content Management & CMS
| Service | URL | Port | Credentials | Purpose |
|---------|-----|------|-------------|---------|
| **Strapi CMS** | http://localhost:1337 | 1337 | Admin setup required | Headless CMS for blog, services, content |
| **Strapi Admin** | http://localhost:1337/admin | 1337 | Create on first visit | Admin dashboard |

### 🛒 E-commerce & Marketplace
| Service | URL | Port | Credentials | Purpose |
|---------|-----|------|-------------|---------|
| **MedusaJS Store** | *To be deployed* | 9000 | TBD | Headless e-commerce backend |
| **MedusaJS Admin** | *To be deployed* | 7001 | TBD | E-commerce admin dashboard |
| **CoreLDove Integration** | Via port 3001 | 3001 | Existing setup | Live dropshipping platform |

### 👥 CRM & Customer Management
| Service | URL | Port | Credentials | Purpose |
|---------|-----|------|-------------|---------|
| **Mautic CRM** | http://localhost:8090 | 8090 | Setup on first visit | Sales funnel automation |
| **BizoSaaS CRM Service** | http://localhost:30304 | 30304 | API only | Customer relationship management |

### 🤖 AI & Automation Services
| Service | URL | Port | Purpose |
|---------|-----|------|---------|
| **AI Agents Service** | http://localhost:8000 | 8000 | CrewAI automation agents |
| **AI Orchestrator** | http://localhost:30203 | 30203 | AI task coordination |
| **Marketing AI** | http://localhost:30307 | 30307 | Marketing strategy generation |
| **Analytics AI** | http://localhost:30308 | 30308 | SEO analysis and reporting |

### 🔧 Development & Admin Tools
| Service | URL | Port | Credentials | Purpose |
|---------|-----|------|-------------|---------|
| **Adminer (DB Admin)** | http://localhost:8082 | 8082 | DB credentials below | PostgreSQL web interface |
| **Redis Commander** | http://localhost:8083 | 8083 | None | Redis data browser |
| **RabbitMQ Admin** | http://localhost:15672 | 15672 | `bizosaas` / `bizosaas_password` | Message queue management |

---

## 🗄️ Database Access Information

### PostgreSQL Database
```bash
Host: localhost
Port: 5432
Database: bizosaas
Username: bizosaas
Password: bizosaas_password

# Direct connection via command line
PGPASSWORD=bizosaas_password psql -h localhost -U bizosaas -d bizosaas

# Connection string
postgresql://bizosaas:bizosaas_password@localhost:5432/bizosaas
```

### Redis Cache
```bash
Host: localhost
Port: 6379
Password: None (development)

# Connect via CLI
redis-cli -h localhost -p 6379
```

---

## 🎛️ Strapi CMS Setup & Access

### First-Time Setup
1. **Start Strapi Service**:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d strapi postgres
   ```

2. **Access Admin Panel**: http://localhost:1337/admin
   - Create your admin account on first visit
   - Use your email and secure password

3. **Database Connection**: Automatically configured to PostgreSQL
   - Database: `strapi_bizosaas`
   - All content will be stored in PostgreSQL

### Content Management Features
- ✅ **Blog Posts**: Create and manage blog content
- ✅ **Service Pages**: Define service offerings
- ✅ **Team Members**: Staff profiles and information
- ✅ **Case Studies**: Customer success stories
- ✅ **Media Library**: Image and file management
- ✅ **API Generation**: Automatic REST and GraphQL APIs

### API Access
```bash
# Public API (no authentication required)
GET http://localhost:1337/api/blog-posts
GET http://localhost:1337/api/services
GET http://localhost:1337/api/team-members

# Admin API (requires authentication)
POST http://localhost:1337/admin/login
GET http://localhost:1337/admin/users
```

---

## 🛒 MedusaJS E-commerce Setup

### Deploy MedusaJS (Currently Configured but Not Running)
```bash
# Deploy MedusaJS for CoreLDove
kubectl apply -f k8s-coreldove-medusa.yaml

# Or start with docker-compose (create configuration)
# Will be integrated with existing CoreLDove on port 3001
```

### Expected Access URLs (When Deployed)
- **Medusa Backend**: http://localhost:9000
- **Medusa Admin**: http://localhost:7001
- **API Endpoints**: http://localhost:9000/store/* and http://localhost:9000/admin/*

### Features Available
- ✅ **Product Management**: Inventory and catalog
- ✅ **Order Processing**: Shopping cart and checkout
- ✅ **Customer Management**: User accounts and profiles
- ✅ **Payment Integration**: Stripe and other gateways
- ✅ **Inventory Tracking**: Stock levels and variants
- ✅ **Shipping**: Fulfillment and logistics

---

## 👥 CRM System Access

### Mautic CRM (Sales Funnel Automation)
1. **Access URL**: http://localhost:8090
2. **First Setup**: Create admin account on first visit
3. **Database**: Uses PostgreSQL database `mautic_bizosaas`

**Key Features**:
- Lead management and scoring
- Email marketing campaigns
- Landing page builder
- Automated workflows
- Customer journey tracking

### BizoSaaS CRM API
```bash
# Create lead
curl -X POST http://localhost:30304/leads \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "company": "Test Company",
    "source": "website"
  }'

# Get leads dashboard
curl "http://localhost:30304/leads/analytics/dashboard?tenant_id=1"
```

---

## 🤖 AI Services Integration

### CrewAI Agents Access
- **Service URL**: http://localhost:8000
- **Legacy Integration**: Existing CrewAI code mounted from `/home/alagiri/projects/bizoholic/n8n/crewai`
- **API Documentation**: Available at http://localhost:8000/docs

### Available AI Agents
1. **Digital Presence Audit**: Analyze company online presence
2. **Campaign Strategy**: Generate marketing strategies
3. **Campaign Optimization**: Improve existing campaigns
4. **Content Generation**: Create marketing materials
5. **SEO Analysis**: Website optimization recommendations

### Example API Usage
```bash
# Generate marketing strategy
curl -X POST http://localhost:8000/agents/campaign-strategy \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Corp",
    "industry": "e-commerce",
    "target_audience": "millennials",
    "budget": 10000
  }'

# Check agent status
curl http://localhost:8000/health
```

---

## 🔐 Authentication & Security

### Service Authentication
- **Strapi**: JWT tokens via admin panel
- **Mautic**: Session-based authentication
- **BizoSaaS APIs**: JWT tokens via auth service (port 30301)
- **MedusaJS**: API keys and session tokens

### Development Credentials
```bash
# Database
Username: bizosaas
Password: bizosaas_password

# RabbitMQ
Username: bizosaas
Password: bizosaas_password

# JWT Secret (development)
JWT_SECRET_KEY: your-super-secret-jwt-key-change-in-production
```

---

## 🚀 Integration Examples

### Frontend to Strapi Integration
```typescript
// In your Next.js components
const strapiUrl = "http://localhost:1337";

// Fetch blog posts
async function getBlogPosts() {
  const response = await fetch(`${strapiUrl}/api/blog-posts?populate=*`);
  return response.json();
}

// Fetch services
async function getServices() {
  const response = await fetch(`${strapiUrl}/api/services?populate=*`);
  return response.json();
}
```

### MedusaJS Integration
```typescript
// Connect to MedusaJS (when deployed)
const medusaUrl = "http://localhost:9000";

// Get products
async function getProducts() {
  const response = await fetch(`${medusaUrl}/store/products`);
  return response.json();
}

// Create cart
async function createCart() {
  const response = await fetch(`${medusaUrl}/store/carts`, {
    method: 'POST',
  });
  return response.json();
}
```

---

## 🔧 Troubleshooting

### Common Issues

1. **Services Won't Start**
   ```bash
   # Check if ports are in use
   netstat -tulpn | grep :1337
   
   # Stop conflicting services
   sudo fuser -k 1337/tcp
   ```

2. **Database Connection Issues**
   ```bash
   # Ensure PostgreSQL is running
   docker-compose -f docker-compose.dev.yml ps postgres
   
   # Check database logs
   docker-compose -f docker-compose.dev.yml logs postgres
   ```

3. **Strapi Admin Setup Issues**
   - Clear browser cache
   - Ensure PostgreSQL is accessible
   - Check Strapi logs: `docker-compose -f docker-compose.dev.yml logs strapi`

### Service Health Checks
```bash
# Check all services
docker-compose -f docker-compose.dev.yml ps

# Restart specific service
docker-compose -f docker-compose.dev.yml restart strapi

# View service logs
docker-compose -f docker-compose.dev.yml logs -f strapi
```

---

## 📋 Next Steps

### Immediate Actions Needed
1. ✅ **Start Strapi CMS**: `docker-compose -f docker-compose.dev.yml up -d strapi`
2. ✅ **Setup Strapi Admin**: Visit http://localhost:1337/admin
3. ⏳ **Deploy MedusaJS**: Apply Kubernetes configurations or create docker-compose setup
4. ⏳ **Configure Mautic**: Setup automation workflows
5. ⏳ **Connect Frontend**: Integrate Strapi API with Next.js frontend

### Development Workflow
1. **Content Management**: Use Strapi for all blog, services, team content
2. **E-commerce**: Integrate MedusaJS with CoreLDove for dropshipping
3. **Lead Management**: Use Mautic for email campaigns and lead nurturing
4. **AI Services**: Leverage CrewAI agents for automation and insights

---

**🎉 Status: Backend Infrastructure Ready for Integration**  
**📊 Services Available: Strapi CMS, Mautic CRM, AI Agents, Database Systems**  
**🔗 Frontend Integration: Ready for connection with localhost:3000**  
**🚀 Next Phase: Content Population and API Integration**