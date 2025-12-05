# BizOSaaS SQLAdmin Dashboard

A comprehensive FastAPI-based administrative interface for the BizOSaaS platform, providing complete CRUD operations, advanced filtering, analytics, and platform management capabilities.

## Features

### 🚀 **Platform Management**
- **Multi-tenant Architecture**: Complete tenant and organization management
- **User Management**: Advanced user roles, permissions, and session tracking
- **Security & Compliance**: Comprehensive audit logging, security events, and compliance reporting
- **API Management**: API key management, rate limiting, and usage tracking

### 📊 **Business Operations**
- **CRM Module**: Contacts, leads, deals, activities, and campaign management
- **E-commerce Module**: Products, orders, customers, inventory, and category management
- **CMS Module**: Pages, media, forms, collections, and menu management
- **Analytics Module**: Events, metrics, reports, and dashboard management

### 💰 **Financial Management**
- **Billing System**: Subscriptions, invoices, payments, and plan management
- **Revenue Analytics**: Financial reporting, revenue tracking, and customer metrics
- **Payment Processing**: Multi-gateway support with detailed transaction tracking

### 🔗 **Integration Hub**
- **External Services**: API integrations, webhook management, and data synchronization
- **Automation Rules**: Business process automation and workflow management
- **Data Export**: Advanced export capabilities with multiple formats

### 🔒 **Security & Compliance**
- **Role-Based Access Control (RBAC)**: Granular permission management
- **Audit Logging**: Complete action tracking and change history
- **Security Events**: Real-time security monitoring and threat detection
- **Privacy Management**: GDPR/CCPA compliance with data retention policies

## Architecture

### Components

1. **SQLAdmin Dashboard** - Main web interface for infrastructure management
2. **Monitoring Service** - Background metrics collection and processing
3. **Alert Manager** - Intelligent alerting and notification system
4. **Database Layer** - PostgreSQL with comprehensive monitoring tables
5. **Cache Layer** - Redis for real-time metrics and session storage

### Technology Stack

- **Backend**: FastAPI with SQLAdmin for admin interface
- **Database**: PostgreSQL 15 with pgvector extension
- **Cache**: Redis 7 with persistence
- **Monitoring**: Custom Python collectors with asyncio
- **Frontend**: Enhanced HTML/CSS/JavaScript with real-time updates
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose with health checks

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Access to BizOSaaS unified authentication system
- Super admin privileges in the platform

### 1. Environment Setup

```bash
# Clone or navigate to the SQLAdmin dashboard directory
cd /path/to/bizosaas-platform/core/services/sqladmin-dashboard

# Copy environment configuration
cp .env.example .env

# Edit environment variables
nano .env
```

### 2. Database Initialization

```bash
# Initialize monitoring database schema
docker-compose exec postgresql psql -U bizosaas -d bizosaas -f /docker-entrypoint-initdb.d/02-init-monitoring-db.sql
```

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f sqladmin-dashboard
```

### 4. Access Dashboard

- **SQLAdmin Interface**: http://localhost:5000/admin
- **Infrastructure Dashboard**: http://localhost:5000/dashboard-switcher
- **API Health Check**: http://localhost:5000/api/system/health
- **Monitoring Data**: http://localhost:5000/api/monitoring/dashboard

## Configuration

### Environment Variables

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://bizosaas:bizosaas@localhost:5432/bizosaas
DATABASE_SYNC_URL=postgresql://bizosaas:bizosaas@localhost:5432/bizosaas

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Authentication URLs
UNIFIED_AUTH_URL=http://localhost:3002
TAILADMIN_URL=http://localhost:3001

# Monitoring Configuration
MONITORING_INTERVAL=60                    # Collection interval in seconds
MONITORING_RETENTION_DAYS=30             # Data retention period
ENABLED_COLLECTORS=database,redis,containers,api_endpoints

# Alert Thresholds
CPU_WARNING_THRESHOLD=80.0               # CPU usage warning %
CPU_CRITICAL_THRESHOLD=95.0              # CPU usage critical %
MEMORY_WARNING_THRESHOLD=85.0            # Memory usage warning %
MEMORY_CRITICAL_THRESHOLD=95.0           # Memory usage critical %
RESPONSE_TIME_WARNING=2000               # Response time warning (ms)
RESPONSE_TIME_CRITICAL=5000              # Response time critical (ms)
ERROR_RATE_WARNING=5.0                   # Error rate warning %
ERROR_RATE_CRITICAL=10.0                 # Error rate critical %
CACHE_HIT_RATE_WARNING=80.0              # Cache hit rate warning %
```

### Alert Configuration

Configure alerting thresholds and notification channels:

```python
# Custom alert thresholds
ALERT_THRESHOLDS = {
    'database': {
        'cpu_usage_critical': 95.0,
        'memory_usage_critical': 90.0,
        'slow_queries_warning': 10,
        'connection_pool_critical': 90
    },
    'redis': {
        'memory_usage_critical': 90.0,
        'hit_rate_warning': 80.0,
        'evicted_keys_warning': 1000
    },
    'ai_agents': {
        'response_time_warning': 5000,
        'error_rate_critical': 10.0,
        'success_rate_warning': 95.0
    }
}
```

## Usage Guide

### Admin Interface

1. **Login**: Access requires SUPER_ADMIN role through unified authentication
2. **Navigation**: Use category-based navigation in the admin interface
3. **Data Views**: Each monitoring aspect has dedicated list and detail views
4. **Search & Filter**: Use built-in search and filtering capabilities
5. **Export**: Export data in various formats for analysis

### Dashboard Features

#### Infrastructure Dashboard
- Real-time system health overview
- Performance metrics visualization
- Active alerts management
- Service status monitoring

#### Monitoring Views
- **AI Monitoring**: Agent performance and workflow execution
- **Infrastructure**: Database, Redis, container, and API metrics
- **Business Operations**: Tenant activity and user analytics
- **Security**: Authentication logs and security events
- **Integration**: External API health and data sync status

### API Endpoints

#### System Health
```bash
# Get system health status
curl http://localhost:5000/api/system/health

# Get detailed system statistics
curl http://localhost:5000/api/system/stats

# Get real-time monitoring dashboard data
curl http://localhost:5000/api/monitoring/dashboard
```

#### Alert Management
```bash
# Acknowledge an alert
curl -X POST http://localhost:5000/api/alerts/{alert_id}/acknowledge

# Resolve an alert
curl -X POST http://localhost:5000/api/alerts/{alert_id}/resolve \
  -H "Content-Type: application/json" \
  -d '{"resolution_notes": "Issue resolved by restarting service"}'
```

#### Monitoring Control
```bash
# Start monitoring service
curl -X POST http://localhost:5000/api/monitoring/start

# Get monitoring configuration
curl http://localhost:5000/api/monitoring/config
```

## Monitoring Data Model

### Core Tables

- **ai_agent_monitoring**: AI agent performance metrics
- **workflow_executions**: Workflow execution tracking
- **database_health_metrics**: PostgreSQL health monitoring
- **redis_health_metrics**: Redis performance tracking
- **container_metrics**: Docker container monitoring
- **api_endpoint_metrics**: API performance tracking
- **security_event_logs**: Security event tracking
- **system_alerts**: Alert management
- **admin_action_audit**: Admin action audit trail

### Data Retention

- **Real-time metrics**: 24 hours
- **Hourly aggregates**: 7 days
- **Daily aggregates**: 30 days
- **Security logs**: 90 days
- **Audit logs**: 1 year

## Security

### Authentication
- Unified authentication integration
- SUPER_ADMIN role requirement
- Session management and validation
- Multi-factor authentication support

### Authorization
- Role-based access control
- Resource-level permissions
- Admin action auditing
- Compliance logging

### Data Protection
- Database encryption at rest
- Secure API communications
- Sensitive data masking
- GDPR compliance features

## Production Deployment

### Docker Compose (Recommended)
```bash
# Production configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

### Environment Considerations

1. **Database**: Use managed PostgreSQL with read replicas
2. **Cache**: Use Redis Cluster for high availability
3. **Monitoring**: Configure external monitoring (Prometheus/Grafana)
4. **Logging**: Centralized logging with ELK stack
5. **Backups**: Automated database and configuration backups

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check database connectivity
   docker-compose exec postgresql pg_isready -U bizosaas
   
   # Check database logs
   docker-compose logs postgresql
   ```

2. **Monitoring Data Missing**
   ```bash
   # Check monitoring collector
   docker-compose logs monitoring-collector
   
   # Verify collectors are enabled
   docker-compose exec sqladmin-dashboard env | grep ENABLED_COLLECTORS
   ```

3. **Authentication Issues**
   ```bash
   # Verify unified auth service
   curl http://localhost:3002/api/health
   
   # Check session cookies
   # Use browser developer tools
   ```

### Performance Optimization

1. **Database Optimization**
   - Regular VACUUM and ANALYZE operations
   - Index optimization for monitoring queries
   - Connection pool tuning

2. **Monitoring Efficiency**
   - Adjust collection intervals based on needs
   - Configure data retention policies
   - Enable selective collectors

3. **Alert Tuning**
   - Fine-tune alert thresholds
   - Implement alert correlation
   - Configure notification channels

## Support

For technical support and feature requests:

- **Documentation**: Comprehensive inline documentation
- **API Reference**: OpenAPI/Swagger documentation at `/docs`
- **Health Checks**: Built-in health monitoring endpoints
- **Logging**: Structured logging with correlation IDs

## License

This software is part of the BizOSaaS platform and is subject to the platform's licensing terms.