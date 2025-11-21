# BizOSaaS Monorepo Workspace Setup

This document describes the monorepo structure and build system for the BizOSaaS multi-tenant platform.

## Architecture Overview

The BizOSaaS platform uses a monorepo structure with:
- **Multi-tenant frontend applications** for different brands
- **Shared UI component library** for consistency across tenants
- **Unified build and development system** with Turbo for performance

## Directory Structure

```
bizosaas/
├── apps/                          # Frontend applications
│   ├── bizoholic-frontend/        # Bizoholic marketing platform (port 3000)
│   └── coreldove-frontend/        # CoreLDove e-commerce platform (port 3001)
├── services/
│   └── frontend-nextjs/           # BizOSaaS admin dashboard (port 3001)
├── packages/                      # Shared packages
│   └── shared-ui/                 # Shared UI components and utilities
├── package.json                   # Root workspace configuration
├── turbo.json                     # Turbo build configuration
└── tsconfig.json                  # TypeScript workspace configuration
```

## Technology Stack

### Build System
- **Turbo**: High-performance build system with intelligent caching
- **npm workspaces**: Package management and dependency resolution
- **TypeScript**: Type safety across all applications
- **ESLint + Prettier**: Code quality and formatting

### Frontend Applications
- **Next.js 14**: React framework with App Router
- **Tailwind CSS**: Utility-first CSS framework
- **ShadCN UI**: Component library built on Radix UI
- **Zustand**: State management for client-side state
- **Lucide React**: Icon library

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm 9+

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Setup workspace**:
   ```bash
   npm run setup:workspace
   ```

## Development

### Start All Applications
```bash
# Start all applications in parallel
npm run start:all

# Or individually
npm run dev:bizoholic    # http://localhost:3000
npm run dev:coreldove    # http://localhost:3001  
npm run dev:bizosaas     # http://localhost:3001
```

### Build System
```bash
# Build all applications
npm run build

# Build specific workspace
npm run build --workspace=@bizosaas/bizoholic-frontend

# Development with Turbo (parallel execution)
npm run dev

# Lint all applications
npm run lint

# Type check all applications
npm run type-check
```

### Package Management

#### Adding Dependencies
```bash
# Add to root (dev tools, etc.)
npm install -w root <package>

# Add to specific workspace
npm install -w @bizosaas/shared-ui <package>

# Add to all frontend apps
npm install --workspaces <package>
```

#### Shared UI Development
```bash
# Work on shared components
cd packages/shared-ui
npm run dev

# Applications will automatically pick up changes
```

## Application Configuration

### Port Allocation
- **Bizoholic**: 3000 (Marketing platform)
- **CoreLDove**: 3001 (E-commerce platform)  
- **BizOSaaS**: 3001 (Admin dashboard)
- **Brain API**: 8001 (Backend services)

### Environment Variables
Each application has its own environment configuration:
- `apps/bizoholic-frontend/.env.local`
- `apps/coreldove-frontend/.env.local`
- `services/frontend-nextjs/.env.local`

### Tenant Configuration
Tenant-specific settings are managed in `packages/shared-ui/src/types/index.ts`:
- Brand colors and gradients
- Logo and favicon paths
- API endpoints
- Feature flags

## Shared Components

### Component Library Structure
```
packages/shared-ui/src/
├── components/           # Reusable UI components
│   ├── ui/              # Base UI components (Button, Card, etc.)
│   └── forms/           # Form components
├── lib/                 # Utilities and helpers
├── types/               # Shared TypeScript types
└── styles/              # Global styles and themes
```

### Usage in Applications
```tsx
import { Button, Card } from '@bizosaas/shared-ui'
import { TENANT_CONFIGS } from '@bizosaas/shared-ui/types'

// Components are automatically styled per tenant
const config = TENANT_CONFIGS['bizoholic']
```

## Brain API Integration

All frontend applications connect to the centralized Brain API:
- **URL**: `http://localhost:8001`
- **Proxy**: Next.js API routes proxy to Brain API
- **Authentication**: JWT tokens handled via Brain API
- **Multi-tenancy**: Tenant isolation at API level

### API Integration Pattern
```tsx
// Fetch data through Brain API proxy
const response = await fetch('/api/brain/saleor/products')
const products = await response.json()
```

## Docker Integration

### Development
```bash
# Build and run with Docker Compose
npm run docker:build
npm run docker:up
```

### Production Deployment
Each application has its own Dockerfile optimized for production:
- Multi-stage builds for minimal image size
- Next.js standalone output for efficiency
- Health checks and proper signal handling

## Performance Optimization

### Turbo Caching
- **Local cache**: `.turbo/` directory stores build artifacts
- **Remote cache**: Disabled by default, can be configured for team sharing
- **Intelligent rebuilds**: Only rebuilds changed packages and dependents

### Build Pipeline
```json
{
  "build": {
    "dependsOn": ["^build"],           // Build dependencies first
    "outputs": [".next/**", "dist/**"] // Cache these directories
  },
  "dev": {
    "cache": false,                    // Never cache dev servers
    "persistent": true                 // Keep running
  }
}
```

### Bundle Analysis
```bash
# Analyze bundle sizes
npm run build
npm run analyze --workspace=@bizosaas/bizoholic-frontend
```

## Monitoring and Debugging

### Development Tools
- **React DevTools**: Component debugging
- **Redux DevTools**: State management debugging  
- **Next.js built-in debugging**: Performance and bundle analysis

### Logging
- **Console**: Development logging
- **Sentry**: Production error tracking (configured per app)
- **Analytics**: Usage tracking via Brain API

## Deployment

### Production Build
```bash
# Build for production
npm run build

# Test production build locally
npm run start
```

### Environment Configuration
Production environments require:
- `NEXT_PUBLIC_BRAIN_API_URL`: Brain API endpoint
- `TENANT_TYPE`: Application tenant type
- Database and Redis connection strings (via Brain API)

## Troubleshooting

### Common Issues

1. **Port conflicts**: Check if ports 3000, 3001, 8001 are available
2. **Build failures**: Clear Turbo cache with `npm run clean`
3. **Type errors**: Run `npm run type-check` to identify issues
4. **Dependency conflicts**: Check workspace resolution with `npm ls`

### Performance Issues
- Use `npm run build` to check for bundle size issues
- Monitor memory usage during development
- Check Turbo cache effectiveness with `--summarize` flag

### Getting Help
- Check application logs: `npm run logs`
- Review Brain API connection: `curl http://localhost:8001/health`  
- Validate environment configuration per application

## Contributing

1. **Code Style**: Prettier and ESLint configured for consistent formatting
2. **Type Safety**: All code must pass TypeScript compilation
3. **Testing**: Add tests for new features and components
4. **Documentation**: Update this README when adding new applications or changing structure

## Next Steps

1. **Testing Setup**: Add Jest and testing-library configuration
2. **CI/CD Pipeline**: GitHub Actions for automated builds and deployment
3. **Storybook**: Component documentation and testing
4. **E2E Testing**: Playwright for cross-application testing