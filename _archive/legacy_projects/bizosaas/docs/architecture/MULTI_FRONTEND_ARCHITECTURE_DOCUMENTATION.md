# BizOSaaS Multi-Frontend Architecture

## Architecture Overview

The BizOSaaS platform implements a comprehensive multi-frontend architecture that provides specialized, optimized user experiences for each platform while maintaining code reusability and consistency.

## Frontend Applications

### 1. BizOSaaS Admin Frontend (`/apps/bizosaas-admin`)
- **Port**: 3005
- **Purpose**: Super admin dashboard and platform management
- **Target Users**: Platform administrators, system operators
- **Key Features**:
  - Tenant management and provisioning
  - User administration across all tenants
  - AI agent deployment and monitoring
  - System analytics and health monitoring
  - Platform-wide settings and configuration

### 2. Bizoholic Marketing Frontend (`/apps/bizoholic-frontend`)
- **Port**: 3000
- **Purpose**: AI-powered marketing automation and client management
- **Target Users**: Marketing managers, campaign specialists
- **Key Features**:
  - Campaign creation and management
  - Lead generation and scoring
  - Client relationship management
  - Marketing analytics and reporting
  - AI-driven campaign optimization

### 3. CoreLDove E-commerce Frontend (`/apps/coreldove-frontend`)
- **Port**: 3001
- **Purpose**: E-commerce intelligence and product sourcing
- **Target Users**: E-commerce managers, product sourcing specialists
- **Key Features**:
  - Product catalog management
  - Intelligent product sourcing
  - Inventory management
  - Supplier relationship management
  - E-commerce analytics

### 4. Client Portal Frontend (`/apps/client-portal`)
- **Port**: 3006
- **Purpose**: Multi-tenant client access and self-service
- **Target Users**: End clients, business users
- **Key Features**:
  - Client-specific dashboards
  - Service subscription management
  - Billing and invoice access
  - Support ticket creation
  - Usage analytics and reporting

### 5. Legacy BizOSaaS Frontend (`/services/frontend-nextjs`)
- **Port**: 3002
- **Purpose**: Original unified dashboard (being phased out)
- **Status**: Maintained for backward compatibility

## Shared Component Library (`/packages/shared-ui`)

### Core Components
- **Branding System**: Platform-specific branding and theming
- **Authentication**: Unified auth service and context providers
- **Navigation**: Platform-aware navigation components
- **Layout**: Responsive layout components
- **UI Components**: Radix UI-based component library

### Key Features
- **Design Tokens**: Centralized color, typography, and spacing system
- **Platform Theming**: Automatic branding based on platform context
- **Authentication**: Shared JWT-based authentication with role-based access
- **API Integration**: Unified API client with retry logic and error handling
- **Permission System**: Granular permission-based UI rendering

## Architecture Patterns

### 1. Monorepo Structure
```
bizosaas/
├── packages/
│   └── shared-ui/              # Shared component library
├── apps/
│   ├── bizosaas-admin/         # Super admin dashboard
│   ├── bizoholic-frontend/     # Marketing automation
│   ├── coreldove-frontend/     # E-commerce intelligence
│   └── client-portal/          # Multi-tenant client portal
└── services/
    └── frontend-nextjs/        # Legacy unified dashboard
```

### 2. Shared Authentication
- **Single Sign-On**: Users can access multiple frontends with one login
- **JWT Tokens**: Stateless authentication with refresh token rotation
- **Role-Based Access**: Granular permissions across all platforms
- **Tenant Context**: Multi-tenant support with tenant switching

### 3. Unified API Layer
- **Brain API Gateway**: Central API aggregation point (port 8001)
- **Platform-Specific APIs**: Specialized endpoints for each platform
- **WebSocket Support**: Real-time updates across all frontends
- **Error Handling**: Consistent error handling and retry logic

### 4. Design System
- **Platform Branding**: Each frontend has distinct visual identity
- **Shared Components**: Reusable UI components across all platforms
- **Responsive Design**: Mobile-first approach with consistent breakpoints
- **Dark Mode**: System-wide theme support

## Technology Stack

### Frontend Technologies
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Radix UI**: Accessible component primitives
- **Zustand**: Lightweight state management
- **React Query**: Server state management

### Build Tools
- **Turbo**: Monorepo build system
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **TypeScript**: Type checking

## Development Workflow

### Setup Commands
```bash
# Install dependencies for all packages
npm install

# Start all frontend applications
npm run start:all

# Start specific frontends only
npm run start:frontends

# Individual frontend development
npm run dev:admin      # BizOSaaS Admin (port 3005)
npm run dev:bizoholic  # Bizoholic Marketing (port 3000)
npm run dev:coreldove  # CoreLDove E-commerce (port 3001)
npm run dev:portal     # Client Portal (port 3006)
npm run dev:bizosaas   # Legacy Dashboard (port 3002)
```

### Development Guidelines
1. **Shared Components**: Use `@bizosaas/shared-ui` for common functionality
2. **Platform Theming**: Leverage platform-specific branding constants
3. **Authentication**: Use shared auth context and guards
4. **API Calls**: Use unified API client for consistency
5. **Permissions**: Implement permission-based UI rendering

## Deployment Strategy

### Environment Variables
Each frontend requires these environment variables:
```env
NEXT_PUBLIC_BRAIN_API_URL=http://localhost:8001
NEXT_PUBLIC_BIZOHOLIC_API_URL=http://localhost:8002
NEXT_PUBLIC_CORELDOVE_API_URL=http://localhost:8003
NEXT_PUBLIC_CLIENT_PORTAL_API_URL=http://localhost:8004
```

### Production Deployment
- **Containerization**: Each frontend builds to a separate Docker container
- **Load Balancing**: Nginx proxy routes traffic to appropriate frontend
- **CDN**: Static assets served from CDN for performance
- **SSL**: HTTPS termination at load balancer level

### Domain Routing
```
admin.bizosaas.com     → BizOSaaS Admin Frontend
app.bizoholic.com      → Bizoholic Marketing Frontend
app.coreldove.com      → CoreLDove E-commerce Frontend
portal.bizosaas.com    → Client Portal Frontend
legacy.bizosaas.com    → Legacy Dashboard (deprecation planned)
```

## Security Considerations

### Authentication & Authorization
- **JWT Tokens**: Short-lived access tokens with refresh rotation
- **Role-Based Access**: Granular permissions per platform
- **Tenant Isolation**: Multi-tenant data separation
- **Session Management**: Secure session handling across frontends

### API Security
- **CORS**: Configured for frontend domains only
- **Rate Limiting**: API call rate limits per user/tenant
- **Input Validation**: Client and server-side validation
- **Error Handling**: No sensitive data exposure in error messages

## Performance Optimization

### Frontend Performance
- **Code Splitting**: Automatic route-based code splitting
- **Tree Shaking**: Dead code elimination
- **Image Optimization**: Next.js automatic image optimization
- **Bundle Analysis**: Regular bundle size monitoring

### Shared Libraries
- **Component Reuse**: High reusability reduces bundle size
- **Design Tokens**: CSS custom properties for theme switching
- **API Caching**: React Query for intelligent data caching
- **Lazy Loading**: Components and routes loaded on demand

## Migration Strategy

### From Legacy to Multi-Frontend
1. **Phase 1**: Parallel development of specialized frontends
2. **Phase 2**: Gradual user migration to appropriate frontends
3. **Phase 3**: Legacy frontend deprecation and removal
4. **Phase 4**: Feature enhancements in specialized frontends

### User Experience Transition
- **Seamless Login**: Single sign-on across all platforms
- **Consistent Branding**: Familiar UI patterns with platform-specific styling
- **Feature Parity**: All legacy features available in new frontends
- **Progressive Enhancement**: New features exclusive to specialized frontends

## Monitoring & Analytics

### Frontend Monitoring
- **Error Tracking**: Client-side error monitoring
- **Performance Metrics**: Core Web Vitals tracking
- **User Analytics**: Usage patterns per frontend
- **A/B Testing**: Feature flag support for gradual rollouts

### Business Metrics
- **User Engagement**: Time spent per frontend
- **Feature Adoption**: Usage of platform-specific features
- **Conversion Rates**: Platform-specific conversion tracking
- **Support Metrics**: Reduced support tickets due to specialized UX

## Future Enhancements

### Short-term Roadmap
- **Mobile Apps**: React Native apps using shared components
- **Offline Support**: Progressive Web App capabilities
- **Real-time Collaboration**: Multi-user real-time features
- **Advanced Analytics**: Enhanced dashboard customization

### Long-term Vision
- **Micro-frontends**: Further decomposition for scalability
- **Edge Computing**: CDN-based frontend delivery
- **AI-Powered UX**: Personalized user interfaces
- **White-label Solutions**: Customer-branded frontends

## Best Practices

### Code Organization
- Keep platform-specific logic in respective frontend apps
- Use shared components for common functionality
- Maintain consistent file structure across frontends
- Document component APIs and usage patterns

### State Management
- Use React Query for server state
- Minimize client state complexity
- Share auth state through context
- Avoid prop drilling with proper component composition

### Performance
- Implement proper loading states
- Use React.memo for expensive components
- Optimize bundle sizes regularly
- Monitor Core Web Vitals

### Testing
- Unit tests for shared components
- Integration tests for auth flows
- E2E tests for critical user journeys
- Visual regression testing for design consistency

This multi-frontend architecture provides specialized user experiences while maintaining code reusability, security, and performance across the entire BizOSaaS ecosystem.