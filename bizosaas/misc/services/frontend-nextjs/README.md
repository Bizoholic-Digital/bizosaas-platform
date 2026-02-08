# BizOSaaS Unified Control Center

A comprehensive Next.js dashboard that integrates with all BizOSaaS platform services, providing a unified control center for autonomous AI agents, multi-tenant management, and real-time platform monitoring.

## 🚀 Features

### Core Dashboard Capabilities
- **Real-time System Monitoring**: Live updates from all 8 core services
- **AI Agent Orchestration**: Manage autonomous agents with task tracking
- **Multi-tenant Management**: Subscription tier-based access control
- **Performance Analytics**: Cross-platform metrics and reporting
- **Event Stream Integration**: Real-time updates via Server-Sent Events
- **Modern UI/UX**: Responsive design with ShadCN UI components

### Platform Integration
- **API Gateway** (Port 8080): Multi-tenant routing and access control
- **AI Agents** (Port 8001): Campaign optimization and lead scoring
- **Django CRM** (Port 8007): Customer relationship management
- **Wagtail CMS** (Port 8006): Content management system
- **Event Bus** (Port 8009): Domain event coordination
- **Domain Repository** (Port 8011): Business entity management
- **Vault Service** (Port 8201): Secrets management
- **Temporal Integration** (Port 8202): Workflow orchestration

## 🏗️ Architecture

### Frontend Stack
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS with ShadCN UI
- **State Management**: Zustand with persistence
- **Real-time**: Server-Sent Events (SSE)
- **Charts**: Recharts for data visualization
- **Icons**: Lucide React

### Key Components
```
lib/
├── types.ts           # TypeScript definitions
├── api-client.ts      # Unified API client
├── store.ts          # Zustand state management
└── utils.ts          # Utility functions

app/
├── layout.tsx        # Root layout
├── page.tsx         # Home redirect
├── globals.css      # Global styles
└── dashboard/       # Dashboard pages
    ├── page.tsx                 # Overview
    ├── ai-agents/page.tsx      # AI Agent management
    ├── leads/page.tsx          # Lead management
    ├── customers/page.tsx      # Customer portal
    ├── campaigns/page.tsx      # Campaign center
    ├── analytics/page.tsx      # Analytics dashboard
    ├── system/page.tsx         # System status
    └── settings/page.tsx       # Configuration

components/
├── ui/              # Reusable UI components
├── charts/          # Chart components
└── dashboard/       # Dashboard-specific components
```

## 🔧 Setup & Installation

### Prerequisites
- Node.js 18+ 
- npm or yarn
- BizOSaaS platform services running

### Installation
```bash
# Navigate to the frontend directory
cd /home/alagiri/projects/bizoholic/bizosaas/services/frontend-nextjs

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local

# Start development server
npm run dev
```

### Environment Configuration
```env
# BizOSaaS Service URLs
NEXT_PUBLIC_API_GATEWAY_URL=http://localhost:8080
NEXT_PUBLIC_AI_AGENTS_URL=http://localhost:8001
NEXT_PUBLIC_CRM_URL=http://localhost:8007
NEXT_PUBLIC_CMS_URL=http://localhost:8006
NEXT_PUBLIC_EVENT_BUS_URL=http://localhost:8009
NEXT_PUBLIC_DOMAIN_REPO_URL=http://localhost:8011
NEXT_PUBLIC_VAULT_URL=http://localhost:8201
NEXT_PUBLIC_TEMPORAL_URL=http://localhost:8202

# Dashboard Configuration
NEXT_PUBLIC_DASHBOARD_TITLE=BizOSaaS Control Center
NEXT_PUBLIC_COMPANY_NAME=BizOSaaS
NEXT_PUBLIC_ENABLE_REAL_TIME=true
```

## 📊 Dashboard Sections

### 1. Overview Dashboard
- **Key Metrics**: Campaigns, leads, revenue, AI efficiency
- **AI Agent Status**: Real-time agent monitoring
- **System Health**: Service availability overview
- **Quick Actions**: Common tasks and shortcuts

### 2. AI Agents Hub
- **Agent Management**: Start, stop, configure agents
- **Task Monitoring**: Track agent tasks and progress
- **Performance Metrics**: Efficiency scores and completion rates
- **Capability Matrix**: Agent skills and responsibilities

### 3. Lead Management
- **Lead Pipeline**: Intelligent lead scoring and tracking
- **AI Insights**: Conversion probability and recommendations
- **Batch Operations**: Bulk lead processing
- **Source Analytics**: Lead source performance

### 4. Customer Portal
- **Relationship Tracking**: Customer lifecycle management
- **Interaction History**: Communication timeline
- **Value Analytics**: Customer lifetime value
- **Segmentation**: Automated customer grouping

### 5. Campaign Center
- **Multi-Channel Campaigns**: Email, social, PPC coordination
- **AI Optimization**: Automated campaign improvements
- **Performance Tracking**: Real-time campaign metrics
- **A/B Testing**: Automated test management

### 6. Analytics Dashboard
- **Cross-Platform Metrics**: Unified analytics view
- **Predictive Analytics**: AI-powered forecasting
- **Custom Reports**: Automated report generation
- **Data Visualization**: Interactive charts and graphs

### 7. System Status
- **Service Health**: Real-time monitoring of all services
- **Performance Metrics**: Response times and uptime
- **Error Tracking**: Alert management and resolution
- **Infrastructure Overview**: Resource utilization

### 8. Settings & Configuration
- **Tenant Management**: Multi-tenant configuration
- **User Permissions**: Role-based access control
- **Integration Settings**: API and webhook configuration
- **Notification Preferences**: Alert and update settings

## 🔄 Real-time Features

### Event Stream Integration
The dashboard connects to the Event Bus service for real-time updates:

```typescript
// Example: Real-time agent status updates
const eventSource = apiClient.createEventStream(['agent_status', 'campaign_update']);

eventSource.onmessage = (event) => {
  const update = JSON.parse(event.data);
  // Update dashboard state in real-time
};
```

### Supported Event Types
- `agent_status`: AI agent state changes
- `campaign_update`: Campaign performance updates
- `new_lead`: New lead notifications
- `system_alert`: Service health alerts
- `workflow_progress`: Temporal workflow updates

## 🎨 UI/UX Design System

### Color Palette
- **Brand**: Blue (#0ea5e9) - Primary actions and navigation
- **Success**: Green (#22c55e) - Positive states and confirmations
- **Warning**: Yellow (#f59e0b) - Attention and caution states
- **Danger**: Red (#ef4444) - Error states and critical alerts
- **Gray Scale**: Modern neutral palette for backgrounds and text

### Typography
- **Primary Font**: Inter (Google Fonts)
- **Headings**: Semibold weights for hierarchy
- **Body Text**: Regular weight for readability
- **Code/Data**: Monospace for technical content

### Component Library
Built on ShadCN UI with custom extensions:
- **Metric Cards**: Key performance indicator displays
- **Status Badges**: Color-coded status indicators
- **Data Tables**: Sortable, filterable data displays
- **Progress Bars**: Task and loading progress
- **Real-time Indicators**: Live connection status

## 🔒 Security & Access Control

### Multi-tenant Architecture
- **Tenant Isolation**: Strict data separation per tenant
- **Subscription Tiers**: Feature access based on tier (tier_1, tier_2, tier_3)
- **Role-based Access**: Admin, manager, agent, viewer permissions

### Authentication Flow
```typescript
// Authentication with tenant context
const { user, tenant, token } = await apiClient.login(email, password);
apiClient.setAuth(token, tenant.id);

// All subsequent requests include tenant context
const leads = await apiClient.getLeads({ tenantId: tenant.id });
```

### Data Security
- **JWT Tokens**: Secure authentication
- **CORS Configuration**: Cross-origin request security
- **Input Validation**: Client and server-side validation
- **Audit Logging**: User action tracking

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px - Stacked layout, collapsible sidebar
- **Tablet**: 768px - 1024px - Adapted grid layouts
- **Desktop**: > 1024px - Full dashboard experience
- **Large Desktop**: > 1440px - Optimized spacing

### Mobile Optimizations
- **Touch-friendly**: Large tap targets and gestures
- **Offline Support**: Service worker for basic functionality
- **Performance**: Optimized bundle size and lazy loading
- **PWA Features**: App-like experience on mobile devices

## ⚡ Performance Optimization

### Bundle Optimization
- **Code Splitting**: Route-based and component-based splitting
- **Tree Shaking**: Unused code elimination
- **Dynamic Imports**: Lazy loading for non-critical components
- **Image Optimization**: Next.js image component with WebP support

### Caching Strategy
- **API Responses**: Client-side caching with Zustand persistence
- **Static Assets**: CDN caching for images and fonts
- **Service Worker**: Background sync and offline support

### Monitoring
- **Core Web Vitals**: Performance metric tracking
- **Error Boundaries**: Graceful error handling
- **Performance Budget**: Bundle size limits
- **Real User Monitoring**: Production performance tracking

## 🚀 Deployment

### Development
```bash
npm run dev
# Runs on http://localhost:3001
```

### Production Build
```bash
npm run build
npm run start
```

### Docker Deployment
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3001
CMD ["npm", "start"]
```

### Environment-specific Configurations
- **Development**: Mock data and debug mode
- **Staging**: Production-like with test data
- **Production**: Full integration with live services

## 🔧 Development Guidelines

### Code Organization
- **Feature-based Structure**: Group related functionality
- **Separation of Concerns**: UI, business logic, and data layers
- **Reusable Components**: DRY principle implementation
- **Type Safety**: Comprehensive TypeScript coverage

### Best Practices
- **Component Composition**: Prefer composition over inheritance
- **Performance**: React.memo, useMemo, useCallback optimization
- **Accessibility**: WCAG 2.1 compliance
- **Testing**: Unit tests for utilities, integration tests for components

### State Management Patterns
```typescript
// Example: Dashboard state with Zustand
const useDashboardStore = create<DashboardState>((set, get) => ({
  metrics: null,
  setMetrics: (metrics) => set({ metrics }),
  // Real-time updates
  updateMetric: (key, value) => {
    const current = get().metrics;
    if (current) {
      set({ metrics: { ...current, [key]: value } });
    }
  },
}));
```

## 📈 Monitoring & Analytics

### Application Monitoring
- **Error Tracking**: Sentry integration
- **Performance Monitoring**: Web Vitals tracking
- **User Analytics**: Privacy-focused user behavior
- **A/B Testing**: Feature flag integration

### Business Metrics
- **Dashboard Usage**: Page views and interaction tracking
- **Feature Adoption**: New feature usage metrics
- **User Satisfaction**: In-app feedback and surveys
- **Performance Impact**: Business metric correlation

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install dependencies: `npm install`
4. Start development server: `npm run dev`
5. Make changes and test thoroughly
6. Submit a pull request

### Code Standards
- **ESLint**: Code quality enforcement
- **Prettier**: Code formatting
- **TypeScript**: Type checking
- **Husky**: Pre-commit hooks

## 📚 API Documentation

The dashboard integrates with the BizOSaaS API Gateway which provides:
- **REST Endpoints**: Standard HTTP API access
- **GraphQL**: Advanced querying capabilities
- **WebSocket**: Real-time bidirectional communication
- **Server-Sent Events**: Real-time server-to-client updates

For detailed API documentation, see the API Gateway service documentation.

## 🛠️ Troubleshooting

### Common Issues
1. **Service Connection**: Check if all BizOSaaS services are running
2. **Port Conflicts**: Ensure no other services are using port 3001
3. **Environment Variables**: Verify all required env vars are set
4. **Network Issues**: Check firewall and proxy configurations

### Debug Mode
```bash
DEBUG=1 npm run dev
```

### Log Analysis
The dashboard provides comprehensive logging:
- **Client Errors**: Browser console and error boundaries
- **API Failures**: Network request logging
- **Performance Issues**: React DevTools Profiler
- **State Changes**: Zustand DevTools

## 📝 License

This project is part of the BizOSaaS platform and follows the same licensing terms.

---

**Built with ❤️ for the BizOSaaS Autonomous AI Agents Platform**