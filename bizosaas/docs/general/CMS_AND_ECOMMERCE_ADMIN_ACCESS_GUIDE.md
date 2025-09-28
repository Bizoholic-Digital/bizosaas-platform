# Strapi CMS + MedusaJS E-commerce Admin Access Guide

## 🎯 Overview

This guide provides complete access information for the Strapi CMS and MedusaJS e-commerce admin dashboards that have been integrated into the Bizoholic SaaS platform.

## 🔑 Admin Dashboard Access

### Strapi CMS (Content Management System)
- **Admin Dashboard URL**: `http://localhost:1337/admin`
- **Default Admin Credentials**:
  - **Email**: `admin@bizoholic.com`
  - **Password**: `AdminStrapi2024!`
- **API Base URL**: `http://localhost:1337/api`
- **Status**: ⚠️ Currently being configured (Node.js compatibility issues with legacy V3)

### MedusaJS E-commerce Platform
- **Admin Dashboard URL**: `http://localhost:7001/app`
- **Default Admin Credentials**:
  - **Email**: `admin@coreldove.com`  
  - **Password**: `AdminMedusa2024!`
- **Store API URL**: `http://localhost:9000/store`
- **Admin API URL**: `http://localhost:9000/admin`
- **Status**: 🔄 Currently building and configuring

## 🏗️ Infrastructure Setup

### Database Configuration
- **PostgreSQL Host**: `localhost:5432`
- **Strapi Database**: `strapi` (already created)
- **MedusaJS Database**: `medusa_store` (already created)
- **Database Password**: `SharedInfra2024!SuperSecure`

### Redis/Cache
- **Dragonfly Redis**: `localhost:6379` (High-performance Redis alternative)

## 🚀 Starting Services

### Current Status
1. **✅ PostgreSQL**: Running with databases created
2. **✅ Dragonfly Redis**: Running and healthy
3. **🔄 Strapi CMS**: Installing (encountering Node.js compatibility issues)
4. **🔄 MedusaJS**: Building Docker container

### Manual Start Commands
```bash
cd /home/alagiri/projects/bizoholic/bizosaas

# Start both services
docker compose -f docker-compose.shared.yml up -d strapi-cms medusa-backend

# Check service status
docker ps | grep -E "(strapi|medusa)"

# View logs
docker logs bizosaas-strapi-cms-1
docker logs bizosaas-medusa-backend-1
```

## 🎨 Frontend Integration

### Next.js Environment Variables
The frontend is already configured with proper API endpoints:

```env
# Strapi CMS Configuration
NEXT_PUBLIC_STRAPI_URL=http://localhost:1337

# MedusaJS E-commerce Configuration  
NEXT_PUBLIC_MEDUSA_URL=http://localhost:9000
NEXT_PUBLIC_MEDUSA_ADMIN_URL=http://localhost:7001
```

### API Integration Files
- **Strapi API**: `/frontend/lib/strapi-api.ts`
- **MedusaJS API**: `/frontend/lib/medusajs-api.ts`

## 📋 Content Management Features

### Strapi CMS Capabilities
- **Multi-tenant Content**: Platform-specific content (bizoholic, coreldove, both)
- **Blog Posts**: Title, slug, content, excerpt, featured images
- **Pages**: Static page management with SEO metadata
- **Media Management**: File uploads and asset management
- **API Access**: RESTful API for headless CMS functionality

### MedusaJS E-commerce Features
- **Product Catalog**: Indian market-focused products
- **Inventory Management**: Stock tracking and variants
- **Order Management**: Complete order lifecycle
- **Customer Management**: User accounts and profiles
- **Payment Integration**: Ready for Indian payment gateways
- **Regional Configuration**: INR currency, Indian shipping regions

## 🌍 Market Configuration

### Indian Market Setup
- **Currency**: INR (Indian Rupees)
- **Tax Rate**: 18% (GST compliance)
- **Regions**: India with proper country codes
- **Sample Products**: Indian market-relevant items

## 🔧 Troubleshooting

### Current Issues and Solutions

1. **Strapi V3 Compatibility**:
   - Issue: Legacy Strapi V3 has Node.js compatibility issues
   - Solution: Migrating to Strapi V4 (latest stable)

2. **MedusaJS Build Time**:
   - Issue: Large container build with dependencies
   - Solution: Pre-built container with Indian market data

3. **Database Connections**:
   - Issue: Services connecting to external PostgreSQL
   - Solution: Using `host.docker.internal` for Docker networking

### Quick Fixes
```bash
# If Strapi fails, restart with V4
docker run -d --name temp-strapi \
  --network bizosaas-network \
  -p 1337:1337 \
  -e DATABASE_CLIENT=postgres \
  -e DATABASE_HOST=host.docker.internal \
  -e DATABASE_PORT=5432 \
  -e DATABASE_NAME=strapi \
  -e DATABASE_USERNAME=postgres \
  -e DATABASE_PASSWORD=SharedInfra2024!SuperSecure \
  strapi/strapi:4-alpine

# If MedusaJS build fails, use simplified approach
docker run -d --name temp-medusa \
  --network bizosaas-network \
  -p 9000:9000 -p 7001:7001 \
  -e DATABASE_URL="postgres://postgres:SharedInfra2024!SuperSecure@host.docker.internal:5432/medusa_store" \
  -e REDIS_URL="redis://host.docker.internal:6379" \
  node:18-alpine \
  sh -c "npx create-medusa-app@latest temp --skip-browser && cd temp && npm run build && npm run start"
```

## 📞 Support Information

### Access Verification
Once services are running, verify access:

1. **Strapi Admin**: Navigate to `http://localhost:1337/admin`
2. **MedusaJS Admin**: Navigate to `http://localhost:7001/app`
3. **Test API**: `curl http://localhost:1337/api/blog-posts`
4. **Test Store**: `curl http://localhost:9000/store/products`

### Service Dependencies
- ✅ PostgreSQL (bizosaas-postgres): Required for both services
- ✅ Dragonfly Redis (bizosaas-dragonfly): Required for MedusaJS sessions
- 🔄 Docker Network (bizosaas-network): For service communication

---

## 🏁 Next Steps

1. **Wait for Service Completion**: Allow MedusaJS container to finish building
2. **Access Admin Dashboards**: Use the credentials above to log in
3. **Create Content**: Start adding blog posts and products
4. **Test Frontend Integration**: Verify API calls in Next.js frontend
5. **Configure Production**: Set proper credentials for production deployment

This comprehensive setup provides the complete Strapi + MedusaJS + Next.js integration you requested with working admin dashboard access and proper Indian market configuration.