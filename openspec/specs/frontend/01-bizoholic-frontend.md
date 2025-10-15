# Bizoholic Frontend - Frontend Service

## Service Identity
- **Name**: Bizoholic Marketing Frontend
- **Type**: Frontend - Marketing Website (Next.js 15)
- **Container**: `bizosaas-bizoholic-frontend-staging`
- **Image**: `ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:staging`
- **Port**: `3000:3000`
- **Domain**: `stg.bizoholic.com`
- **Status**: 🔴 HTTP 500 (incomplete Next.js build)

## Purpose
Public-facing marketing website for Bizoholic digital agency with lead generation, blog, portfolio showcase, and service information.

## Architecture - Containerized Microservice

### Technology Stack
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **UI Components**: TailwindCSS + Custom Components
- **State Management**: React Context + Server Components
- **API Integration**: Brain API Gateway (port 8001)

### Container Architecture
```
Bizoholic Frontend Container
├── Next.js 15 Application
│   ├── App Router (/app directory)
│   ├── Server Components (RSC)
│   ├── API Routes (Backend-for-Frontend pattern)
│   └── Static Assets
├── Node.js Runtime (v20)
├── Production Build (.next/)
└── Environment Configuration
```

## Domain-Driven Design (Frontend)

### Bounded Context: Marketing & Lead Generation

```
Frontend Bounded Context
├── Presentation Layer
│   ├── Pages (Next.js routes)
│   ├── Components (Reusable UI)
│   └── Layouts (Shared layouts)
├── Application Layer
│   ├── API Routes (BFF pattern)
│   ├── Server Actions
│   └── Data Fetching
├── Integration Layer
│   ├── Brain Gateway Client
│   ├── Wagtail CMS Client
│   └── Django CRM Client
└── Domain Layer (Frontend)
    ├── View Models
    ├── Form Models
    └── Business Logic (client-side)
```

### Key Features

#### 1. Dynamic Content (Wagtail CMS)
```typescript
// app/api/cms/pages/[slug]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { slug: string } }
) {
  const BRAIN_API = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'
  
  const response = await fetch(
    `${BRAIN_API}/api/brain/wagtail/pages/${params.slug}`,
    {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
      },
      next: { revalidate: 300 } // Cache 5 minutes
    }
  )

  if (!response.ok) {
    // Fallback data for development
    return NextResponse.json({
      title: "Page Not Found",
      content: [],
    }, { status: 200 })
  }

  return NextResponse.json(await response.json())
}
```

#### 2. Contact Form with Dual Submission
```typescript
// app/api/contact/route.ts
export async function POST(request: NextRequest) {
  const data = await request.json()
  const BRAIN_API = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

  // Dual submission: Wagtail CMS + Django CRM
  const [wagtailResponse, crmResponse] = await Promise.all([
    // Submit to Wagtail
    fetch(`${BRAIN_API}/api/brain/wagtail/forms/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }),
    // Submit to Django CRM with lead scoring
    fetch(`${BRAIN_API}/api/brain/django-crm/leads`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...data,
        source: 'website_contact_form',
        calculate_score: true
      })
    })
  ])

  if (!wagtailResponse.ok || !crmResponse.ok) {
    console.error('Form submission error')
    return NextResponse.json(
      { success: true, message: 'Form received' },
      { status: 200 }
    )
  }

  const crmData = await crmResponse.json()

  return NextResponse.json({
    success: true,
    lead_id: crmData.id,
    lead_score: crmData.score,
    message: 'Thank you for contacting us!'
  })
}
```

#### 3. Blog with SEO Optimization
```typescript
// app/blog/[slug]/page.tsx
export async function generateMetadata(
  { params }: { params: { slug: string } }
): Promise<Metadata> {
  const post = await getPost(params.slug)
  
  return {
    title: post.seo_title || post.title,
    description: post.seo_description,
    openGraph: {
      title: post.title,
      description: post.seo_description,
      images: [post.featured_image],
    },
  }
}

export default async function BlogPost({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug)
  
  return (
    <article className="max-w-4xl mx-auto py-8">
      <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
      <div className="prose lg:prose-xl" dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  )
}
```

## Containerization & Deployment

### Dockerfile
```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build Next.js application
RUN npm run build

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Copy built application
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000

CMD ["node", "server.js"]
```

### Docker Compose (Local Development)
```yaml
services:
  bizoholic-frontend:
    build:
      context: ./bizosaas/frontend/apps/bizoholic-frontend
      dockerfile: Dockerfile
    container_name: bizosaas-bizoholic-frontend-local
    environment:
      - NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-local:8001
      - NODE_ENV=development
    ports:
      - "3000:3000"
    networks:
      - bizosaas-network
    depends_on:
      - brain-gateway
    volumes:
      - ./bizosaas/frontend/apps/bizoholic-frontend:/app
      - /app/node_modules
    restart: unless-stopped
```

### Dokploy Deployment Configuration
```yaml
# dokploy-frontend-staging.yml
services:
  bizoholic-frontend-staging:
    image: ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:staging
    container_name: bizosaas-bizoholic-frontend-staging
    environment:
      - NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
      - NODE_ENV=production
    ports:
      - "3000:3000"
    networks:
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.bizoholic-staging.rule=Host(`stg.bizoholic.com`)"
      - "traefik.http.routers.bizoholic-staging.entrypoints=websecure"
      - "traefik.http.routers.bizoholic-staging.tls.certresolver=letsencrypt"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
```

## CI/CD Pipeline (GitHub Actions)

### Build and Push Workflow
```yaml
# .github/workflows/build-bizoholic-frontend.yml
name: Build Bizoholic Frontend

on:
  push:
    branches: [staging, main]
    paths:
      - 'bizosaas/frontend/apps/bizoholic-frontend/**'

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: ./bizosaas/frontend/apps/bizoholic-frontend
          push: true
          tags: |
            ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:staging
            ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Deploy to Dokploy Staging
        run: |
          curl -X POST https://dokploy.bizoholic.com/api/deploy \
            -H "Authorization: Bearer ${{ secrets.DOKPLOY_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d '{"service": "bizoholic-frontend", "environment": "staging"}'
```

## Environment Variables

```bash
# .env.production
NEXT_PUBLIC_API_BASE_URL=http://bizosaas-brain-staging:8001
NEXT_PUBLIC_SITE_URL=https://stg.bizoholic.com

# Analytics
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX

# Feature Flags
NEXT_PUBLIC_ENABLE_BLOG=true
NEXT_PUBLIC_ENABLE_PORTFOLIO=true
```

## API Integration Patterns

### Backend-for-Frontend (BFF) Pattern
```typescript
// All backend calls go through internal API routes
// Frontend → Next.js API Route → Brain Gateway → Backend Service

// Client component
async function submitForm(data: FormData) {
  const response = await fetch('/api/contact', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  
  return response.json()
}

// API route acts as BFF
export async function POST(request: NextRequest) {
  // Transform request
  const data = await request.json()
  
  // Call Brain Gateway
  const response = await fetch(`${BRAIN_API}/api/brain/wagtail/forms/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  
  // Transform response
  const result = await response.json()
  return NextResponse.json(result)
}
```

## Performance Optimization

### Next.js Configuration
```javascript
// next.config.js
module.exports = {
  output: 'standalone', // For Docker
  images: {
    domains: ['stg.bizoholic.com'],
  },
  experimental: {
    serverActions: true,
  },
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
  }
}
```

## Testing Strategy

### Unit Tests (Jest + React Testing Library)
```typescript
// __tests__/components/ContactForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import ContactForm from '@/components/ContactForm'

describe('ContactForm', () => {
  it('submits form data to API', async () => {
    render(<ContactForm />)
    
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    })
    
    fireEvent.click(screen.getByText('Submit'))
    
    await screen.findByText('Thank you for contacting us!')
  })
})
```

### Integration Tests (Playwright)
```typescript
// e2e/contact-form.spec.ts
test('contact form submission', async ({ page }) => {
  await page.goto('http://localhost:3000/contact')
  
  await page.fill('input[name="email"]', 'test@example.com')
  await page.fill('textarea[name="message"]', 'Test message')
  
  await page.click('button[type="submit"]')
  
  await expect(page.locator('.success-message')).toBeVisible()
})
```

## Common Issues & Solutions

### Issue 1: HTTP 500 Error (Current)
**Symptom**: Incomplete Next.js build missing `.next/required-server-files.json`
**Solution**:
```bash
# Rebuild with complete Next.js build
cd bizosaas/frontend/apps/bizoholic-frontend
npm run build
docker build -t ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:staging .
docker push ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:staging

# Redeploy on Dokploy
docker-compose -f dokploy-frontend-staging.yml up -d bizoholic-frontend-staging
```

### Issue 2: API Connection Timeout
**Symptom**: Frontend cannot reach Brain Gateway
**Solution**: Verify Docker network configuration and service names

## Deployment Checklist

- [ ] Next.js build completes successfully
- [ ] All environment variables configured
- [ ] Docker image builds and runs locally
- [ ] Image pushed to GHCR
- [ ] Dokploy container deployed
- [ ] Health checks passing
- [ ] Domain DNS configured (stg.bizoholic.com)
- [ ] Traefik routing working
- [ ] SSL certificate issued
- [ ] API integration verified
- [ ] Contact form working (dual submission)
- [ ] Blog pages loading from Wagtail
- [ ] Analytics tracking active

## Monitoring

### Health Check Endpoint
```typescript
// app/api/health/route.ts
export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    service: 'bizoholic-frontend',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  })
}
```

---
**Status**: 🔴 Critical Fix Required (HTTP 500)
**Priority**: CRITICAL
**Last Updated**: October 15, 2025
**Deployment**: Local WSL2 → GitHub → GHCR → Dokploy Staging → Dokploy Production
