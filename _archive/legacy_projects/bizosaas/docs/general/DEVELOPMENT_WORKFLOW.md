# BizOSaaS Development Workflow Guide

## Overview

This guide outlines the optimized development workflow for the BizOSaaS platform, focusing on efficient frontend-Brain API integration and streamlined development processes.

## Quick Start

### 🚀 Start Development Environment

```bash
# Method 1: Using npm scripts (recommended)
npm run dev        # Start both frontend and Brain API
npm run status     # Check service status
npm run test       # Test integration
npm run stop       # Stop all services

# Method 2: Using the script directly  
./start-dev-environment.sh start
./start-dev-environment.sh status
```

### 📊 Monitor Services

```bash
npm run status
```

**Output:**
```
📊 Service Status
=================
Brain API:  Running (Port 8001, PID: 12345)
           Health: http://localhost:8001/health
Frontend:   Running (Port 3000, PID: 67890)
           URL: http://localhost:3000

🔗 Quick Links:
Frontend:        http://localhost:3000
Brain API Docs:  http://localhost:8001/docs
Health Check:    http://localhost:8001/health
```

## Architecture Overview

### Current Active Services

- **Frontend**: Next.js 14 application on port 3000 (`/frontend` directory)
- **Brain API**: FastAPI service on port 8001 (`/services/bizosaas-brain` directory)
- **Integration**: Next.js API routes proxy `/api/brain/*` to Brain API

### Service Communication

```
Frontend (3000) → Next.js API Routes → Brain API (8001)
     ↓                    ↓                    ↓
User Interface    Proxy & Fallback     Business Logic
```

## Development Commands

### Core Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development environment |
| `npm run status` | Check service status |
| `npm run test` | Test frontend-Brain API integration |
| `npm run stop` | Stop all services |
| `npm run restart` | Restart all services |
| `npm run logs <service>` | View service logs (brain\|frontend) |

### Individual Service Commands

```bash
# Frontend only
npm run dev:frontend
cd frontend && npm run dev

# Brain API only  
npm run dev:brain
cd services/bizosaas-brain && python3 simple_api.py

# Other frontends (monorepo structure)
npm run dev:bizoholic   # Bizoholic marketing frontend
npm run dev:coreldove   # CoreLDove e-commerce frontend
npm run dev:bizosaas    # BizOSaaS admin dashboard
```

### Build & Deploy Commands

```bash
npm run build          # Build all workspaces
npm run build:all      # Build all workspace packages
npm run lint           # Lint all code
npm run type-check     # TypeScript type checking
npm run clean          # Clean build artifacts
```

## Integration Testing

### Automated Integration Tests

The development script includes built-in integration testing:

```bash
npm run test
```

**Tests performed:**
1. ✅ Brain API health check (HTTP 200)
2. ✅ Frontend-Brain API proxy (HTTP 200)
3. ✅ Data flow validation

### Manual Testing

```bash
# Test Brain API directly
curl http://localhost:8001/health
curl http://localhost:8001/docs

# Test frontend proxy
curl http://localhost:3000/api/brain/wagtail/homepage
curl http://localhost:3000/api/brain/saleor/products
```

## Troubleshooting

### Common Issues

**1. Port Conflicts**
```bash
# Check what's using ports
lsof -i :3000
lsof -i :8001

# Stop services cleanly
npm run stop
```

**2. Next.js Cache Issues**
```bash
# Development script automatically clears cache
npm run restart

# Manual cache clearing
cd frontend && rm -rf .next && npm run dev
```

**3. Process Management**
```bash
# Check running processes
npm run status

# Clean stop all services
npm run stop

# Kill any remaining processes
pkill -f "simple_api.py"
pkill -f "npm run dev"
```

### Logs and Debugging

```bash
# View service logs
npm run logs brain      # Brain API logs
npm run logs frontend   # Frontend logs

# Log files location
tail -f /tmp/brain-api.log
tail -f /tmp/frontend.log
```

## Environment Configuration

### Frontend Environment (.env.local)

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
TENANT_TYPE=bizosaas
```

### Brain API Configuration

- **Port**: 8001 (configurable in script)
- **Health endpoint**: `/health`
- **API docs**: `/docs`
- **Wagtail endpoints**: `/api/brain/wagtail/*`
- **Saleor endpoints**: `/api/brain/saleor/*`

## Workspace Structure

```
bizosaas/
├── frontend/                    # 🎯 Current active frontend
│   ├── app/api/brain/          # Proxy routes to Brain API
│   ├── components/chat/        # AI interface components  
│   └── package.json
├── services/bizosaas-brain/     # 🧠 Brain API service
│   ├── simple_api.py           # FastAPI application
│   └── requirements.txt
├── apps/                        # 📱 Multi-tenant frontends
│   ├── bizoholic-frontend/     # Marketing platform
│   └── coreldove-frontend/     # E-commerce platform
├── packages/                    # 📦 Shared packages
│   └── shared-ui/              # Shared components
├── start-dev-environment.sh     # 🛠 Development script
├── package.json                # Root workspace config
└── turbo.json                  # Build system config
```

## Best Practices

### Development Workflow

1. **Always use the development script** - `npm run dev`
2. **Check status before making changes** - `npm run status`
3. **Test integration after changes** - `npm run test`
4. **Clean shutdown when switching contexts** - `npm run stop`

### Code Organization

- **Frontend logic**: Keep in `/frontend` directory
- **API logic**: Keep in `/services/bizosaas-brain`
- **Shared components**: Use `/packages/shared-ui`
- **Multi-tenant apps**: Use `/apps` structure

### Performance Optimization

- Development script automatically clears Next.js cache
- Services are monitored for health and restarted if needed
- Background processes are properly managed with PID files

## Integration Endpoints

### Wagtail CMS Integration (Bizoholic)

```bash
# Homepage content
GET /api/brain/wagtail/homepage

# Service pages
GET /api/brain/wagtail/services

# Blog posts
GET /api/brain/wagtail/blog
```

### Saleor E-commerce Integration (CoreLDove)

```bash
# Product catalog
GET /api/brain/saleor/products

# Categories
GET /api/brain/saleor/categories

# Collections
GET /api/brain/saleor/collections
```

## Next Steps

1. **Testing Setup**: Implement automated testing with Jest
2. **CI/CD Pipeline**: Set up GitHub Actions
3. **Monorepo Migration**: Consolidate duplicate frontend apps
4. **Shared UI**: Expand shared component library
5. **Performance Monitoring**: Add application performance monitoring

## Getting Help

- **Service Status**: `npm run status`
- **Integration Test**: `npm run test`  
- **View Logs**: `npm run logs <service>`
- **Health Checks**: Visit http://localhost:8001/health

For development issues, check the logs and ensure both services are running healthy before debugging application-specific problems.