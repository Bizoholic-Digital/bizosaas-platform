# BizOSaaS Client Portal

A comprehensive multi-tenant client dashboard for the BizOSaaS platform, built with Next.js 14, TypeScript, and ShadCN UI components.

## Overview

The Client Portal provides tenant-specific access to business data through an integrated dashboard that connects to all BizOSaaS platform services via the Central Hub API (localhost:8001).

## Features

### Core Functionality
- **Multi-Tenant Dashboard**: Tenant-specific views of business metrics and data
- **CRM Integration**: Lead management through Django CRM API
- **Content Management**: Website content editing via Wagtail CMS API
- **E-commerce Orders**: Order tracking through Saleor API
- **AI Analytics**: Business insights powered by AI Agents

### User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Dark/Light Theme**: System preference detection with manual toggle
- **Real-time Updates**: Live data refreshing and notifications
- **Progressive Loading**: Skeleton screens and optimistic UI updates

### Technical Features
- **Central Hub Integration**: All API calls routed through localhost:8001
- **JWT Authentication**: Secure token-based authentication
- **Error Handling**: Graceful degradation when services are unavailable
- **Health Monitoring**: Docker health checks and service status monitoring

## Architecture

### Technology Stack
- **Frontend**: Next.js 14 with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS with ShadCN UI components
- **Charts**: Recharts for data visualization
- **State Management**: React hooks with Zustand for global state
- **HTTP Client**: Fetch API with custom service layer

### Project Structure
```
/app
  /api
    /health          # Health check endpoint for Docker
  /analytics         # AI-powered business insights
  /content          # Content management interface
  /leads            # CRM lead management
  /orders           # E-commerce order tracking
  /settings         # Account and tenant settings
  page.tsx          # Main dashboard overview
  layout.tsx        # App layout and providers
  globals.css       # Global styles and theme

/lib
  api.ts            # Central API service with Central Hub integration

/components
  ui/               # ShadCN UI components
  [existing]        # Legacy components (to be migrated)
```

### API Integration

All API calls are routed through the Central Hub at `localhost:8001` with the following patterns:

```typescript
// CRM Integration
GET /api/brain/django-crm/leads
POST /api/brain/django-crm/leads

// Content Management
GET /api/brain/wagtail/pages
POST /api/brain/wagtail/pages

// E-commerce
GET /api/brain/saleor/orders
GET /api/brain/saleor/products

// AI Analytics
GET /api/brain/agents/insights
POST /api/brain/agents/analyze
```

## Configuration

### Environment Variables
```bash
# Required
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
PORT=3000
NODE_ENV=development

# Optional
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret
NEXT_PUBLIC_DEBUG=false
NEXT_TELEMETRY_DISABLED=1
```

### Development Setup
```bash
# Install dependencies
npm install --legacy-peer-deps

# Copy environment file
cp .env.example .env.local

# Start development server
npm run dev
```

### Production Deployment
```bash
# Build for production
npm run build

# Start production server
npm start

# Or use Docker
docker build -t bizosaas-client-portal .
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_BASE_URL=http://localhost:8001 \
  -e NODE_ENV=production \
  bizosaas-client-portal
```

## Pages Overview

### Dashboard (`/`)
- **Key Metrics**: Total leads, conversion rates, revenue, active orders
- **Quick Actions**: Add lead, create content, view orders, AI insights
- **Performance Charts**: Traffic trends and conversion funnels
- **Recent Activity**: Real-time feed of business events
- **AI Insights Preview**: Highlighting opportunities and recommendations

### Leads (`/leads`)
- **Lead List**: Searchable and filterable lead database
- **Lead Details**: Complete lead information and interaction history
- **Status Management**: Lead pipeline and status updates
- **Bulk Actions**: Export, bulk status updates, assignments
- **Statistics**: Conversion rates, source analysis, performance metrics

### Content (`/content`)
- **Content Library**: All website pages, posts, and media
- **Content Editor**: Direct integration with Wagtail CMS
- **Publishing Workflow**: Draft, review, publish status management
- **Media Management**: Image and file uploads
- **SEO Tools**: Meta tags, social sharing, analytics integration

### Orders (`/orders`)
- **Order Management**: Complete order tracking and fulfillment
- **Customer Details**: Order history and customer information
- **Inventory Integration**: Real-time stock levels and product data
- **Payment Processing**: Payment status and transaction history
- **Shipping & Logistics**: Tracking numbers and delivery status

### Analytics (`/analytics`)
- **AI Insights**: Machine learning powered business recommendations
- **Performance Metrics**: Traffic, conversions, revenue analysis
- **Trend Analysis**: Historical data and forecasting
- **Custom Reports**: Configurable dashboards and data exports
- **Competitive Analysis**: Market positioning and opportunities

### Settings (`/settings`)
- **Profile Management**: User account and preferences
- **Company Settings**: Business information and branding
- **Notification Preferences**: Email, SMS, and in-app notifications
- **Security**: Password management and 2FA
- **API Keys**: Integration credentials and webhooks
- **Billing**: Subscription management and payment methods

## Development Guidelines

### Code Standards
- **TypeScript**: All new code must be typed
- **Components**: Use ShadCN UI components when available
- **Styling**: Tailwind CSS with consistent design tokens
- **Error Handling**: Implement graceful error states
- **Loading States**: Show skeleton screens during data fetching

### API Integration
- **Service Layer**: Use the centralized API service (`lib/api.ts`)
- **Error Handling**: Handle network errors and API failures gracefully
- **Mock Data**: Include fallback data for development
- **Caching**: Implement appropriate caching strategies
- **Rate Limiting**: Respect API rate limits and implement backoff

### Performance
- **Bundle Size**: Monitor and optimize bundle size
- **Image Optimization**: Use Next.js Image component
- **Lazy Loading**: Implement code splitting for routes
- **Caching**: Leverage Next.js caching strategies
- **Monitoring**: Include performance monitoring and health checks

## Testing

### Testing Strategy
- **Unit Tests**: Component logic and utility functions
- **Integration Tests**: API service and data flows
- **E2E Tests**: Critical user journeys
- **Visual Tests**: Component rendering and responsive design

### Running Tests
```bash
# Unit tests
npm test

# E2E tests
npm run test:e2e

# Coverage report
npm run test:coverage
```

## Deployment

### Docker Deployment
```bash
# Build image
docker build -t bizosaas-client-portal:latest .

# Run container
docker run -d \
  --name bizosaas-client-portal-3000 \
  --network bizosaas-platform-network \
  -p 3000:3000 \
  -e NODE_ENV=production \
  -e PORT=3000 \
  -e NEXT_PUBLIC_API_BASE_URL=http://localhost:8001 \
  bizosaas-client-portal:latest
```

### Health Checks
- **Endpoint**: `GET /api/health`
- **Docker**: Built-in health check with 30s interval
- **Monitoring**: Includes Central Hub connectivity status
- **Alerting**: 503 status when dependencies are unavailable

## Troubleshooting

### Common Issues
1. **API Connection Failures**: Check Central Hub status at localhost:8001
2. **Authentication Errors**: Verify JWT tokens and session management
3. **Build Failures**: Clear `.next` cache and node_modules
4. **Performance Issues**: Check bundle size and optimize imports

### Debug Mode
```bash
NEXT_PUBLIC_DEBUG=true npm run dev
```

### Logs
```bash
# Container logs
docker logs bizosaas-client-portal-3000

# Development logs
npm run dev 2>&1 | tee debug.log
```

## Contributing

### Development Workflow
1. Create feature branch from `main`
2. Implement changes with tests
3. Test integration with Central Hub
4. Update documentation
5. Submit pull request

### Code Review Checklist
- [ ] TypeScript types are properly defined
- [ ] Error handling is implemented
- [ ] Loading states are included
- [ ] Responsive design is tested
- [ ] API integration works correctly
- [ ] Tests pass and coverage is maintained

## Support

For technical support or questions:
- **Documentation**: Check inline code comments and README files
- **Issues**: Create GitHub issues for bugs and feature requests
- **API Status**: Monitor Central Hub health at localhost:8001/health

## License

This project is part of the BizOSaaS platform. All rights reserved.