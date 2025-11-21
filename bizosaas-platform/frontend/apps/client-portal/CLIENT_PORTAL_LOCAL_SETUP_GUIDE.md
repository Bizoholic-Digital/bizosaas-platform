# Client Portal - Local Setup & Testing Guide

**Date**: November 11, 2025
**Purpose**: Get Client Portal running locally for Amazon Sourcing integration

---

## Current Status

### ✅ What's Already Done

1. **Portal Fixed** - React hooks violations resolved (see CLIENT_PORTAL_FIX_SUMMARY.md)
2. **Architecture Reviewed** - Multi-tenant structure confirmed
3. **Environment Created** - `.env` file configured for local development
4. **Dependencies** - Currently installing (npm install running)

### 📋 Existing Portal Structure

```
client-portal/
├── app/
│   ├── analytics/         # Analytics dashboard
│   ├── billing/           # Billing & subscriptions
│   ├── crm/               # CRM features
│   ├── ecommerce/         # E-commerce management
│   ├── marketing/         # Marketing tools
│   ├── content/           # CMS features
│   └── sourcing/          # ← TO BE ADDED (Amazon sourcing)
├── components/
│   ├── auth/              # Authentication components
│   └── ui/                # Shared UI components
└── lib/                   # Utilities & helpers
```

---

## Setup Steps

### Step 1: Environment Configuration ✅

**File**: `.env` (created)

```bash
# Local Development
PORT=3000
NODE_ENV=development

# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
NEXT_PUBLIC_BRAIN_API_URL=http://localhost:8001

# Feature Flags
NEXT_PUBLIC_ENABLE_SOURCING=true

# Amazon Sourcing (will connect to Dokploy service)
NEXT_PUBLIC_AMAZON_SOURCING_API_URL=http://backend-amazon-sourcing:8080
```

### Step 2: Install Dependencies

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas-platform/frontend/apps/client-portal

# Install (currently running)
npm install

# Expected time: 2-3 minutes
```

### Step 3: Check for Build Errors

```bash
# Type check
npm run type-check

# If errors found, they'll be listed here
# Common issues to fix:
# 1. Missing imports
# 2. Type mismatches
# 3. Deprecated API usage
```

### Step 4: Start Development Server

```bash
# Start local server
npm run dev

# Expected output:
# ✓ Ready on http://localhost:3000
# ○ Compiling /...
```

### Step 5: Verify Portal Loads

```bash
# Test in browser or with curl
curl http://localhost:3000

# Should return HTML without errors
```

---

## Known Issues & Fixes

### Issue 1: Port Already in Use

**Error**: `Port 3000 is already in use`

**Fix**:
```bash
# Find process using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use different port
PORT=3001 npm run dev
```

### Issue 2: Missing Dependencies

**Error**: `Cannot find module...`

**Fix**:
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

### Issue 3: TypeScript Errors

**Error**: `Type 'X' is not assignable to type 'Y'`

**Fix**:
```bash
# Check specific errors
npm run type-check

# Common fixes:
# - Add proper type imports
# - Update component prop types
# - Fix any/unknown types
```

### Issue 4: Next.js Cache Issues

**Error**: Build fails or shows old code

**Fix**:
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

---

## Testing Checklist

### Basic Functionality

- [ ] **Portal loads** at http://localhost:3000
- [ ] **No console errors** in browser DevTools
- [ ] **Sidebar navigation** works
- [ ] **Dark/Light theme** toggle works
- [ ] **Page routing** functions correctly

### Feature Verification

- [ ] **Dashboard** loads with widgets
- [ ] **CRM** section accessible
- [ ] **E-commerce** section shows correctly
- [ ] **Analytics** displays data/placeholders
- [ ] **Settings** page functional

### API Integration

- [ ] **Health check** endpoint works
- [ ] **Auth provider** initializes
- [ ] **API calls** structure correct

---

## Next Steps: Add Amazon Sourcing

Once portal is running, we'll add the sourcing module:

### File Structure to Create

```bash
app/sourcing/
├── layout.tsx              # Sourcing section layout
├── page.tsx                # Main sourcing dashboard
├── search/
│   └── page.tsx           # Amazon product search
├── import/
│   ├── page.tsx           # Bulk import interface
│   └── [jobId]/
│       └── page.tsx       # Import job status
├── history/
│   └── page.tsx           # Import history
└── components/
    ├── ProductCard.tsx    # Amazon product display
    ├── ImportWizard.tsx   # Step-by-step import
    └── UsageStats.tsx     # Usage metrics
```

### Implementation Plan

**Phase 1: Basic UI** (1-2 hours)
- Create sourcing directory
- Add main dashboard page
- Implement product search interface

**Phase 2: Backend Integration** (1-2 hours)
- Connect to Amazon sourcing service
- Implement search API calls
- Add import functionality

**Phase 3: Subscription Checks** (1 hour)
- Add plan-based access control
- Implement usage limits
- Create upgrade prompts

**Phase 4: Polish** (1 hour)
- Add loading states
- Implement error handling
- Create success notifications

---

## Development Workflow

### Local Development Loop

```bash
# 1. Make changes to code
# 2. Save file (Next.js auto-reloads)
# 3. Check browser (http://localhost:3000)
# 4. Fix any errors in terminal
# 5. Repeat
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/amazon-sourcing

# Make changes and commit
git add .
git commit -m "Add Amazon sourcing module to client portal"

# Push to remote
git push origin feature/amazon-sourcing
```

### Testing Before Deployment

```bash
# 1. Run type check
npm run type-check

# 2. Run linter
npm run lint

# 3. Build for production
npm run build

# 4. Test production build
npm run start

# 5. Verify at http://localhost:3000
```

---

## Deployment to Dokploy

### Prerequisites

- [ ] Portal builds successfully locally
- [ ] No TypeScript/linting errors
- [ ] All features tested locally
- [ ] Environment variables documented

### Dokploy Configuration

**Service Type**: Docker
**Build Method**: Dockerfile
**Port**: 3000

**Environment Variables** (Dokploy UI):
```bash
PORT=3000
NODE_ENV=production

NEXT_PUBLIC_API_BASE_URL=https://brain-gateway.bizoholic.com
NEXT_PUBLIC_BRAIN_API_URL=https://brain-gateway.bizoholic.com
NEXT_PUBLIC_AMAZON_SOURCING_API_URL=http://backend-amazon-sourcing:8080

NEXT_PUBLIC_APP_NAME=BizOSaaS Client Portal
NEXT_PUBLIC_ENABLE_SOURCING=true
NEXT_TELEMETRY_DISABLED=1
```

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Dokploy UI**
   - Go to Dokploy dashboard
   - Select "Client Portal" service
   - Click "Deploy"
   - Wait for build to complete

3. **Verify Deployment**
   ```bash
   # Test the deployed portal
   curl https://portal.bizoholic.com

   # Check logs
   # (via Dokploy UI → Logs)
   ```

4. **Test Live Features**
   - Login to portal
   - Navigate to /sourcing
   - Test product search
   - Verify import works

---

## Troubleshooting

### Portal Won't Start

**Symptoms**: `npm run dev` fails immediately

**Check**:
```bash
# 1. Node version
node --version  # Should be 18.x or higher

# 2. Package.json exists
ls -la package.json

# 3. Dependencies installed
ls -la node_modules

# 4. No syntax errors
npm run lint
```

### Build Fails

**Symptoms**: `npm run build` errors out

**Check**:
```bash
# 1. TypeScript errors
npm run type-check

# 2. Missing environment variables
cat .env

# 3. Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run build
```

### Runtime Errors

**Symptoms**: Portal loads but crashes on certain pages

**Check**:
```bash
# 1. Browser console (F12)
# Look for JavaScript errors

# 2. Network tab
# Check failed API calls

# 3. Server logs
# Check terminal for errors
```

---

## Quick Commands Reference

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Type check
npm run type-check

# Lint code
npm run lint

# Build for production
npm run build

# Start production server
npm run start

# Run tests
npm run test

# Clean everything
rm -rf .next node_modules package-lock.json && npm install
```

---

## Success Criteria

Portal is ready when:

- ✅ Builds without errors
- ✅ Starts on http://localhost:3000
- ✅ All pages load correctly
- ✅ No console errors
- ✅ Dark/light theme works
- ✅ Navigation is functional
- ✅ Ready for sourcing module addition

---

## Contact & Support

**Documentation**: See CLIENT_PORTAL_FIX_SUMMARY.md for resolved issues
**Architecture**: See AMAZON_SOURCING_FINAL_RECOMMENDATION.md for integration plan
**Deployment**: See Dokploy UI for production deployment

---

**Status**: Setup in progress
**Next Step**: Wait for npm install to complete, then start dev server
**ETA**: Portal running locally in ~15 minutes
