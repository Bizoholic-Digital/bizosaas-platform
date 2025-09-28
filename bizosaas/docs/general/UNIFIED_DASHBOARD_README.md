# BizOSaaS Unified Dashboard

## Overview

The BizOSaaS Unified Dashboard is a comprehensive command center for managing all platform services from a single interface. It provides real-time monitoring, service management, cross-service analytics, and AI agent coordination across the entire BizOSaaS ecosystem.

## Features

### 🎯 **Central Command Center**
- **Service Health Monitoring**: Real-time status monitoring of all 6 platform services
- **System Overview**: Unified view of users, revenue, AI tasks, and system health
- **Quick Actions**: One-click access to common management tasks
- **Real-time Updates**: Live data feeds with WebSocket connections

### 🔧 **Service Management**
- **Business Directory**: FastAPI backend (localhost:8000) + NextJS frontend (localhost:3002)
- **CoreLDove E-commerce**: Saleor API (localhost:8024) + Storefront (localhost:3001)
- **Wagtail CMS**: Content management (localhost:8006/admin)
- **Bizoholic Website**: Main marketing platform (localhost:3000)
- **CrewAI Agents**: 6 specialized AI agents (localhost:8002)
- **PostgreSQL Database**: Primary database with pgvector (localhost:5432)

### 📊 **Cross-Service Analytics**
- **Directory Performance**: Listings, views, leads, conversion rates
- **E-commerce Statistics**: Products, orders, revenue, customer metrics
- **Content Metrics**: Pages, posts, media, engagement scores
- **AI Performance**: Agent statistics, success rates, automation metrics
- **Growth Tracking**: Month-over-month performance indicators

### 🤖 **AI Agents Management**
- **Content Creator Agent**: Generates marketing content and blog posts
- **SEO Optimizer Agent**: Optimizes content for search engines
- **Social Media Agent**: Manages social media campaigns
- **Lead Generator Agent**: Identifies and qualifies leads
- **Campaign Analyzer Agent**: Analyzes campaign performance
- **Competitor Research Agent**: Monitors competitor activities

### 👥 **Client Management**
- **Multi-tenant Dashboard**: Per-client view of services and performance
- **Onboarding Workflows**: Automated client setup processes
- **Communication Hub**: Centralized client communications
- **Tier Management**: Enterprise, Pro, and Starter service tiers

## Architecture

### Frontend Stack
- **Framework**: Next.js 14 with App Router
- **UI Library**: ShadCN UI components with Tailwind CSS
- **State Management**: React hooks with real-time updates
- **Icons**: Lucide React icons
- **Charts**: Recharts for data visualization

### Backend Integration
- **API Layer**: RESTful APIs with GraphQL for e-commerce
- **Real-time**: WebSocket connections for live data
- **Authentication**: JWT-based auth with role-based access
- **Caching**: Redis for performance optimization

### Service Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Business       │    │  CoreLDove       │    │  Wagtail CMS    │
│  Directory      │    │  E-commerce      │    │  Content Mgmt   │
│  (8000/3002)    │    │  (8024/3001)     │    │  (8006)         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
            ┌─────────────────────┴─────────────────────┐
            │         Unified Dashboard                 │
            │         (localhost:3000)                  │
            └─────────────────────┬─────────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                       │                        │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  CrewAI Agents  │    │  PostgreSQL DB   │    │  Bizoholic      │
│  AI Workflows   │    │  Primary Store    │    │  Website        │
│  (8002)         │    │  (5432)          │    │  (3000)         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Installation & Setup

### Prerequisites
- Node.js 18+ and pnpm
- PostgreSQL with pgvector extension
- Redis (optional for caching)
- Docker (for containerized services)

### Quick Start

1. **Navigate to Frontend Directory**
   ```bash
   cd /home/alagiri/projects/bizoholic/bizosaas/frontend
   ```

2. **Install Dependencies**
   ```bash
   pnpm install
   ```

3. **Start Development Server**
   ```bash
   pnpm dev
   ```

4. **Access the Dashboard**
   - Main Dashboard: http://localhost:3000/dashboard
   - Unified Dashboard: http://localhost:3000/dashboard/unified

### Service Dependencies

Ensure these services are running for full functionality:

```bash
# Business Directory API
cd /path/to/business-directory && python -m uvicorn main:app --port 8000

# CoreLDove E-commerce (Saleor)
cd /path/to/saleor && python manage.py runserver localhost:8024

# Wagtail CMS
cd /path/to/wagtail-cms && python manage.py runserver localhost:8006

# CrewAI Agents
cd /path/to/crewai-agents && python main.py --port 8002
```

## Usage Guide

### Dashboard Navigation

The unified dashboard provides six main tabs:

1. **Overview**: System health, key metrics, and quick actions
2. **Services**: Real-time service monitoring and management
3. **Analytics**: Cross-service performance metrics
4. **Clients**: Multi-tenant client management
5. **AI Agents**: AI agent monitoring and configuration
6. **Settings**: Platform-wide configuration

### Service Health Monitoring

Each service card displays:
- **Status Indicator**: Green (operational), Yellow (degraded), Red (outage)
- **Uptime Percentage**: Historical uptime data
- **Response Time**: Current API response times
- **Last Check**: Timestamp of last health check
- **Quick Actions**: Direct links to frontend and admin interfaces

### Real-time Features

The dashboard automatically refreshes data every 30 seconds:
- Service health status
- User activity metrics
- Revenue tracking
- AI agent performance
- System resource usage

### AI Agent Management

Monitor and control 6 specialized AI agents:
- View agent status (Active, Working, Idle)
- Monitor performance metrics and success rates
- Review recent tasks and executions
- Configure agent parameters and schedules

### Cross-Service Analytics

Unified analytics across all services:
- **Directory**: Listings, categories, leads, conversions
- **E-commerce**: Products, orders, revenue, customers
- **Content**: Pages, posts, media, engagement
- **AI**: Agents, tasks, automation, insights

## API Integration

### Service Health Endpoints
```typescript
// Check service health
GET /api/services/health

// Get service metrics
GET /api/services/{serviceId}/metrics

// Restart service
POST /api/services/{serviceId}/restart
```

### Analytics Endpoints
```typescript
// Dashboard metrics
GET /api/analytics/dashboard?timeRange=7d

// Cross-service analytics
GET /api/analytics/cross-service

// Real-time metrics
WebSocket: /api/analytics/realtime
```

### AI Agents Endpoints
```typescript
// Get all agents
GET /api/agents

// Agent statistics
GET /api/agents/stats

// Control agent
POST /api/agents/{agentId}/start
POST /api/agents/{agentId}/stop
POST /api/agents/{agentId}/pause
```

## Customization

### Adding New Services

1. **Add Service Configuration**
   ```typescript
   const newService = {
     name: 'New Service',
     type: 'Custom Type',
     url: 'http://localhost:PORT',
     description: 'Service description'
   }
   ```

2. **Update Service Health Monitor**
   ```typescript
   setServices(prev => [...prev, newService])
   ```

3. **Add to Service Management**
   ```typescript
   const serviceActions = [
     { name: 'Action 1', icon: IconName },
     { name: 'Action 2', icon: IconName }
   ]
   ```

### Customizing Analytics

1. **Add New Metrics**
   ```typescript
   const customMetrics = {
     newMetric: {
       value: 1234,
       growth: '+15%',
       description: 'Custom metric description'
     }
   }
   ```

2. **Create Custom Charts**
   ```typescript
   const customChartData = {
     labels: ['Label 1', 'Label 2'],
     datasets: [{
       data: [100, 200],
       backgroundColor: ['#color1', '#color2']
     }]
   }
   ```

## Troubleshooting

### Common Issues

1. **Service Health Not Updating**
   - Check if service endpoints are accessible
   - Verify API credentials and permissions
   - Check browser console for network errors

2. **Real-time Data Not Working**
   - Ensure WebSocket connections are established
   - Check firewall and network configurations
   - Verify service URLs and ports

3. **Analytics Data Missing**
   - Confirm analytics API endpoints are working
   - Check data permissions and access tokens
   - Verify date ranges and filters

### Debug Mode

Enable debug logging:
```typescript
// In your browser console
localStorage.setItem('debug', 'bizosaas:*')
```

### Service Connectivity

Test service connectivity:
```bash
# Test Business Directory
curl http://localhost:8000/health

# Test E-commerce API
curl http://localhost:8024/graphql

# Test CMS
curl http://localhost:8006/admin/

# Test AI Agents
curl http://localhost:8002/agents
```

## Performance Optimization

### Frontend Optimization
- **Code Splitting**: Automatic route-based splitting
- **Image Optimization**: Next.js Image component
- **Bundle Analysis**: `pnpm build && pnpm analyze`
- **Caching**: SWR for API caching

### Backend Optimization
- **Database Indexing**: Ensure proper indexes on frequently queried tables
- **API Caching**: Redis for API response caching
- **Connection Pooling**: Database connection optimization
- **Load Balancing**: Distribute requests across service instances

## Security Considerations

### Authentication & Authorization
- JWT-based authentication with refresh tokens
- Role-based access control (Super Admin, Admin, Manager)
- API key management for service integrations
- Multi-tenant data isolation

### Data Protection
- HTTPS enforcement in production
- API rate limiting and throttling
- Input validation and sanitization
- SQL injection prevention
- XSS protection

## Deployment

### Production Deployment
```bash
# Build for production
pnpm build

# Start production server
pnpm start

# Deploy with PM2
pm2 start ecosystem.config.js
```

### Docker Deployment
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm build
EXPOSE 3000
CMD ["pnpm", "start"]
```

### Environment Variables
```bash
NEXT_PUBLIC_API_BASE_URL=https://api.bizosaas.com
NEXT_PUBLIC_WEBSOCKET_URL=wss://ws.bizosaas.com
DATABASE_URL=postgresql://user:pass@localhost:5432/bizosaas
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
```

## Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- **Documentation**: [BizOSaaS Docs](https://docs.bizosaas.com)
- **Issues**: [GitHub Issues](https://github.com/bizoholic/bizosaas/issues)
- **Email**: support@bizosaas.com
- **Discord**: [BizOSaaS Community](https://discord.gg/bizosaas)

---

**Built with ❤️ by the BizOSaaS Team**