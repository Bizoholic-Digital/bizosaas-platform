# Deployment Fixes Required

## Critical: These fixes must be applied to the GitHub repository before services can deploy

### 1. Auth Service - Fix AsyncIO Driver Issue

**File**: `bizosaas-platform/backend/services/auth/requirements.txt`

**Problem**: Using sync driver `psycopg2` with async code

**Solution**: Replace psycopg2 with asyncpg

```diff
- psycopg2-binary==2.9.9
+ asyncpg==0.29.0
```

**Alternative**: If psycopg2 is required elsewhere:
```diff
+ psycopg[async]==3.1.18
```

---

### 2. Temporal Integration - Fix Non-Existent Package

**File**: `bizosaas-platform/backend/services/temporal/requirements.txt`

**Problem**: Package `python-decimal==0.1.1` doesn't exist in PyPI

**Solution**: Remove the line or replace with correct package

```diff
- python-decimal==0.1.1
```

If decimal functionality is needed, Python has built-in `decimal` module (no install required).

---

### 3. Business Directory - Fix Dependency Conflict

**File**: `bizosaas-platform/backend/services/crm/business-directory/requirements.txt`

**Problem**: `crewai==0.201.0` requires `pydantic-settings>=2.10.1`, but current version conflicts

**Solution**: Update pydantic-settings version

```diff
- pydantic-settings==2.0.0  # or whatever current version
+ pydantic-settings>=2.10.1
```

Or update crewai to latest version that's compatible with your pydantic-settings.

---

### 4. Client Portal - Add Missing Modules

**Directory**: `bizosaas-platform/frontend/apps/client-portal/`

**Problem**: Build fails due to missing modules

**Required Files to Create**:

#### `lib/utils.ts`
```typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

#### `lib/api.ts`
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function apiRequest(endpoint: string, options?: RequestInit) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }

  return response.json();
}

export const api = {
  get: (endpoint: string) => apiRequest(endpoint),
  post: (endpoint: string, data: any) => apiRequest(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  put: (endpoint: string, data: any) => apiRequest(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  delete: (endpoint: string) => apiRequest(endpoint, { method: 'DELETE' }),
};
```

#### `lib/hooks/useLeadsData.ts`
```typescript
import { useState, useEffect } from 'react';
import { api } from '../api';

export interface Lead {
  id: string;
  name: string;
  email: string;
  phone?: string;
  company?: string;
  status: 'new' | 'contacted' | 'qualified' | 'converted';
  createdAt: string;
}

export function useLeadsData() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function fetchLeads() {
      try {
        setLoading(true);
        const data = await api.get('/leads');
        setLeads(data);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    }

    fetchLeads();
  }, []);

  return { leads, loading, error };
}
```

#### `lib/hooks/useOrdersData.ts`
```typescript
import { useState, useEffect } from 'react';
import { api } from '../api';

export interface Order {
  id: string;
  orderNumber: string;
  customerName: string;
  amount: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  createdAt: string;
}

export function useOrdersData() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() {
    async function fetchOrders() {
      try {
        setLoading(true);
        const data = await api.get('/orders');
        setOrders(data);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    }

    fetchOrders();
  }, []);

  return { orders, loading, error };
}
```

---

### 5. ThrillRing Gaming - Create Application

**Directory**: `bizosaas-platform/frontend/apps/thrillring-gaming/`

**Problem**: Directory doesn't exist

**Solution**: Create a new Next.js application

```bash
# In your local development environment
cd bizosaas-platform/frontend/apps/
npx create-next-app@latest thrillring-gaming --typescript --tailwind --app --no-src-dir
```

**Or** use the same structure as other frontend apps and copy:
- `package.json` from another app
- `next.config.js`
- `tsconfig.json`
- Basic `app/` directory structure

---

## After Applying Fixes

### Redeploy Backend Services

```bash
cd /home/alagiri/projects/bizoholic

# Re-enable fixed services in dokploy-backend-staging.yml
# Uncomment: temporal-integration, business-directory-backend, auth-service

# Redeploy
docker-compose -f dokploy-backend-staging.yml up -d --build
```

### Deploy Frontend Services

```bash
# Re-enable fixed services in dokploy-frontend-staging.yml
# Uncomment: client-portal, thrillring-gaming

# Deploy
docker-compose -f dokploy-frontend-staging.yml up -d --build
```

---

## Quick Fix Script (Run in GitHub Repository)

```bash
#!/bin/bash
# fix-deployment-issues.sh

echo "Fixing Auth Service..."
cd bizosaas-platform/backend/services/auth
sed -i 's/psycopg2-binary==2.9.9/asyncpg==0.29.0/' requirements.txt

echo "Fixing Temporal Integration..."
cd ../temporal
sed -i '/python-decimal/d' requirements.txt

echo "Fixing Business Directory..."
cd ../crm/business-directory
sed -i 's/pydantic-settings==.*/pydantic-settings>=2.10.1/' requirements.txt

echo "Creating Client Portal modules..."
cd ../../../../frontend/apps/client-portal
mkdir -p lib/hooks
# Copy the TypeScript files shown above

echo "Done! Commit and push changes."
```

