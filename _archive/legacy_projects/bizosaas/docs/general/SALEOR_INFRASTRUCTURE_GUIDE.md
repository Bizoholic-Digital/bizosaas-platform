# Saleor Infrastructure Setup Guide

## Overview

This guide provides complete setup and management instructions for the Saleor e-commerce infrastructure that supports the CoreLDove storefront at localhost:3001. The backend runs at localhost:8024 and provides GraphQL API access for the enhanced storefront.

## Architecture

### Core Services
- **Saleor API**: GraphQL API server (localhost:8024)
- **Saleor Dashboard**: Admin interface (localhost:9001)
- **Redis**: Caching and Celery message broker
- **Celery Worker**: Background task processing
- **Celery Beat**: Scheduled task management
- **PostgreSQL**: Primary database (shared with BizOSaaS)

### Service Dependencies
```
PostgreSQL (host) ←── Saleor API ←── Storefront (localhost:3001)
                  ↓
Redis ←── Celery Worker ←── Saleor API
      ←── Celery Beat
```

## Quick Start

### 1. Prerequisites
- PostgreSQL running on localhost:5432
- Docker and Docker Compose
- Sufficient system resources (4GB RAM minimum)

### 2. Start Complete Infrastructure
```bash
cd /home/alagiri/projects/bizoholic/bizosaas
./scripts/start-saleor-complete.sh
```

This script will:
- ✅ Check prerequisites
- ✅ Setup PostgreSQL database
- ✅ Start all Saleor services
- ✅ Initialize with sample data
- ✅ Verify all endpoints

### 3. Verify Setup
```bash
./scripts/monitor-saleor-health.sh
```

### 4. Test Storefront Connection
```bash
cd services/saleor-storefront
pnpm run generate  # Generate GraphQL schema
pnpm dev          # Start storefront at localhost:3001
```

## Service Access Points

| Service | URL | Description |
|---------|-----|-------------|
| GraphQL API | http://localhost:8024/graphql/ | Main API endpoint |
| GraphQL Playground | http://localhost:8024/graphql/ | Interactive query tool |
| Health Check | http://localhost:8024/health/ | Service health status |
| Admin Dashboard | http://localhost:9001/ | Saleor management UI |
| Redis | localhost:6379 | Cache and message broker |

## Authentication

### Default Admin Credentials
- **Email**: admin@example.com  
- **Password**: admin

### API Authentication
The GraphQL API supports:
- Anonymous queries (public data)
- JWT token authentication (user sessions)
- App tokens (service-to-service)

## Configuration

### Environment Variables
Located in `docker-compose.saleor-complete.yml`:

```yaml
# Core Configuration
DEBUG: True (development only)
SECRET_KEY: saleor-coreldove-secret-key-2025

# Database
DATABASE_URL: postgresql://admin:BizoholicSecure2025@host.docker.internal:5432/saleor_coreldove

# Redis
REDIS_URL: redis://redis-saleor:6379/0
CELERY_BROKER_URL: redis://redis-saleor:6379/1

# CORS (for storefront)
ALLOWED_CLIENT_HOSTS: http://localhost:3001,http://127.0.0.1:3001
CORS_ALLOWED_ORIGINS: http://localhost:3001,http://127.0.0.1:3001
```

### Storefront Configuration
In `services/saleor-storefront/.env.local`:

```bash
NEXT_PUBLIC_SALEOR_API_URL=http://localhost:8024/graphql/
NEXT_PUBLIC_STOREFRONT_URL=http://localhost:3001
```

## Database Management

### Database Schema
- **Name**: `saleor_coreldove`
- **Owner**: `admin`
- **Extensions**: uuid-ossp, btree_gin, btree_gist, pg_trgm, hstore

### Common Operations

#### Reset Database
```bash
# Stop services
docker-compose -f docker-compose.saleor-complete.yml down

# Drop and recreate database
PGPASSWORD="BizoholicSecure2025" psql -h localhost -U admin -d postgres -c "DROP DATABASE IF EXISTS saleor_coreldove;"
PGPASSWORD="BizoholicSecure2025" psql -h localhost -U admin -d postgres -c "CREATE DATABASE saleor_coreldove OWNER admin;"

# Restart and reinitialize
./scripts/start-saleor-complete.sh
```

#### Backup Database
```bash
PGPASSWORD="BizoholicSecure2025" pg_dump -h localhost -U admin saleor_coreldove > saleor_backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Restore Database
```bash
PGPASSWORD="BizoholicSecure2025" psql -h localhost -U admin saleor_coreldove < saleor_backup.sql
```

## Development Workflow

### 1. Daily Development
```bash
# Start infrastructure
./scripts/start-saleor-complete.sh

# Monitor health
./scripts/monitor-saleor-health.sh

# Develop storefront
cd services/saleor-storefront
pnpm dev
```

### 2. Schema Changes
When Saleor schema changes, regenerate storefront types:
```bash
cd services/saleor-storefront
pnpm run generate
```

### 3. Adding Sample Data
```bash
docker exec saleor-api python manage.py populatedb --createsuperuser
```

### 4. Clearing Cache
```bash
docker exec saleor-redis redis-cli FLUSHALL
```

## GraphQL Operations

### Test Queries

#### Basic Shop Info
```graphql
query {
  shop {
    name
    description
    defaultCountry {
      code
      country
    }
  }
}
```

#### Product Catalog
```graphql
query {
  products(first: 10) {
    edges {
      node {
        id
        name
        slug
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
      }
    }
  }
}
```

#### Categories
```graphql
query {
  categories(first: 10) {
    edges {
      node {
        id
        name
        slug
        products {
          totalCount
        }
      }
    }
  }
}
```

### cURL Examples

```bash
# Test basic connectivity
curl -X POST http://localhost:8024/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query":"{ shop { name } }"}'

# Get products
curl -X POST http://localhost:8024/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query":"{ products(first: 5) { edges { node { name } } } }"}'
```

## Troubleshooting

### Common Issues

#### 1. Port 8024 Already in Use
```bash
# Check what's using the port
ss -tlnp | grep :8024

# Stop conflicting service
docker stop $(docker ps -q --filter "publish=8024")
```

#### 2. Database Connection Failed
```bash
# Check PostgreSQL status
ss -tlnp | grep :5432

# Test connection
PGPASSWORD="BizoholicSecure2025" psql -h localhost -U admin -d postgres -c "\l"
```

#### 3. Redis Connection Failed
```bash
# Check Redis container
docker exec saleor-redis redis-cli ping

# Restart Redis if needed
docker restart saleor-redis
```

#### 4. GraphQL Schema Issues
```bash
# Check API logs
docker logs saleor-api --tail=50

# Restart API container
docker restart saleor-api
```

### Health Check Failures

#### Service Not Responding
1. Check container status: `docker ps`
2. Check logs: `docker logs <container-name>`
3. Restart service: `docker restart <container-name>`

#### Database Migration Issues
```bash
# Run migrations manually
docker exec saleor-api python manage.py migrate

# Check migration status
docker exec saleor-api python manage.py showmigrations
```

### Performance Optimization

#### Redis Memory Usage
```bash
# Check Redis memory usage
docker exec saleor-redis redis-cli info memory

# Set memory limit (already configured in compose)
# maxmemory 512mb
# maxmemory-policy allkeys-lru
```

#### Database Performance
```bash
# Check database connections
PGPASSWORD="BizoholicSecure2025" psql -h localhost -U admin -d saleor_coreldove -c "SELECT count(*) FROM pg_stat_activity;"

# Analyze query performance
docker exec saleor-api python manage.py sql_debug
```

## Monitoring and Logging

### Health Monitoring
```bash
# Continuous monitoring
./scripts/monitor-saleor-health.sh

# Container resource usage
docker stats saleor-api saleor-worker saleor-redis
```

### Log Access
```bash
# All services
docker-compose -f docker-compose.saleor-complete.yml logs -f

# Specific service
docker logs saleor-api -f
docker logs saleor-worker -f
docker logs saleor-redis -f
```

### Error Tracking
- API errors: Check `docker logs saleor-api`
- Worker errors: Check `docker logs saleor-worker`
- Redis errors: Check `docker logs saleor-redis`
- Database errors: Check PostgreSQL logs

## Production Considerations

### Security
- [ ] Change default admin credentials
- [ ] Use environment-specific secrets
- [ ] Enable HTTPS/SSL
- [ ] Configure proper CORS origins
- [ ] Set up rate limiting
- [ ] Enable audit logging

### Scalability
- [ ] Configure multiple worker instances
- [ ] Set up database connection pooling
- [ ] Implement Redis clustering
- [ ] Configure load balancing
- [ ] Set up horizontal pod autoscaling

### Backup Strategy
- [ ] Automated database backups
- [ ] Media file backups
- [ ] Configuration backups
- [ ] Disaster recovery procedures

## Integration with BizOSaaS

The Saleor infrastructure integrates with the broader BizOSaaS platform:

- **Shared PostgreSQL**: Uses same database server
- **Unified Authentication**: Can integrate with BizOSaaS auth
- **Common Monitoring**: Shared monitoring infrastructure
- **Cross-platform Analytics**: Data flows to central analytics

## Support and Maintenance

### Regular Tasks
- Monitor service health daily
- Update Docker images monthly
- Backup database weekly
- Review and rotate logs
- Security updates as needed

### Resources
- [Saleor Documentation](https://docs.saleor.io/)
- [GraphQL Documentation](https://graphql.org/learn/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

This infrastructure provides a robust foundation for the CoreLDove e-commerce platform with comprehensive monitoring, easy maintenance, and production-ready capabilities.