# BizOSaaS Platform - Detailed Implementation Tasks
## Unified Authentication & Gamification System
**Created**: September 30, 2025
**Status**: Ready for Implementation

---

## 🎯 Overview

This document provides **granular, step-by-step tasks** for implementing:
1. Unified Authentication with Single Sign-On
2. Complete Gamification System
3. All Wizard UIs
4. AI-Agentic-First Architecture (everything routes through Brain Gateway)

**Key Principle**: Every service is containerized, every request routes through Brain Gateway (Port 8001/8002), orchestrated by 93 AI agents.

---

## 📋 Test Credentials Reference

### SuperAdmin Access
```
Username: superadmin
Password: BizoSaaS2025!Admin
→ Access: SQLAdmin (8005), All Dashboards
```

### Admin Access
```
Username: administrator
Password: Bizoholic2025!Admin
→ Access: Admin Dashboard (3009), Client Portal (3001)
```

### User Access
```
Username: bizoholic_user
Password: Bizoholic2025!User
→ Access: Client Portal (3001) only
```

---

## PHASE 1: UNIFIED AUTHENTICATION SYSTEM (Days 1-3)

### DAY 1: Foundation & Auth Service Enhancement

#### Task 1.1: Create Unified Auth UI Container
**Location**: `/frontend/apps/unified-auth/`
**Duration**: 2 hours

**Steps**:
1. Create Next.js 15 application structure
   ```bash
   cd /home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps
   npx create-next-app@latest unified-auth --typescript --tailwind --app
   ```

2. Create directory structure:
   ```
   unified-auth/
   ├── app/
   │   ├── page.tsx          # Main login page
   │   ├── layout.tsx        # Root layout
   │   └── api/
   │       └── auth/
   │           └── route.ts  # Auth API routes
   ├── components/
   │   ├── LoginForm.tsx     # Login form component
   │   ├── RoleSelector.tsx  # For demo/testing
   │   └── TestCredentials.tsx  # Credentials reference
   ├── lib/
   │   ├── auth.ts          # Auth utilities
   │   └── api.ts           # API client
   └── Dockerfile
   ```

3. Install dependencies:
   ```bash
   cd unified-auth
   npm install axios jwt-decode zustand
   npm install -D @types/node
   ```

4. Create Dockerfile:
   ```dockerfile
   FROM node:20-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build
   EXPOSE 3002
   CMD ["npm", "start"]
   ```

**Deliverable**: Unified auth UI container structure ready

---

#### Task 1.2: Implement Login Page with Test Credentials
**Location**: `/frontend/apps/unified-auth/app/page.tsx`
**Duration**: 2 hours

**Implementation**:
```typescript
// /frontend/apps/unified-auth/app/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import LoginForm from '@/components/LoginForm';
import TestCredentials from '@/components/TestCredentials';

export default function LoginPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showTestCreds, setShowTestCreds] = useState(true); // For dev mode

  const handleLogin = async (email: string, password: string) => {
    setLoading(true);
    setError('');

    try {
      // Call auth service through Brain Gateway
      const response = await fetch('http://localhost:8002/api/v1/auth/sso/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include', // Important for cookies
        body: JSON.stringify({
          email,
          password,
          platform: 'bizosaas'
        })
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      const data = await response.json();

      // Store tokens
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      localStorage.setItem('user_data', JSON.stringify(data.user));

      // Role-based routing
      const role = data.user.role;

      switch(role) {
        case 'super_admin':
          window.location.href = 'http://localhost:8005'; // SQLAdmin
          break;
        case 'tenant_admin':
          window.location.href = 'http://localhost:3009'; // Admin Dashboard
          break;
        case 'user':
          window.location.href = 'http://localhost:3001'; // Client Portal
          break;
        default:
          window.location.href = 'http://localhost:3001';
      }

    } catch (err) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">BizOSaaS Platform</h1>
          <p className="text-gray-600 mt-2">Unified Authentication Portal</p>
        </div>

        <LoginForm
          onSubmit={handleLogin}
          loading={loading}
          error={error}
        />

        {showTestCreds && (
          <TestCredentials onSelectCredential={(email, password) => {
            handleLogin(email, password);
          }} />
        )}

        <div className="mt-6 text-center text-xs text-gray-500">
          <p>Powered by Brain Gateway AI</p>
          <p>93 AI Agents • Multi-Tenant Architecture</p>
        </div>
      </div>
    </div>
  );
}
```

**Create TestCredentials Component**:
```typescript
// /frontend/apps/unified-auth/components/TestCredentials.tsx
interface Credential {
  role: string;
  username: string;
  password: string;
  color: string;
}

const credentials: Credential[] = [
  {
    role: 'SuperAdmin',
    username: 'superadmin',
    password: 'BizoSaaS2025!Admin',
    color: 'bg-red-100 border-red-300 text-red-800'
  },
  {
    role: 'Admin',
    username: 'administrator',
    password: 'Bizoholic2025!Admin',
    color: 'bg-blue-100 border-blue-300 text-blue-800'
  },
  {
    role: 'User',
    username: 'bizoholic_user',
    password: 'Bizoholic2025!User',
    color: 'bg-green-100 border-green-300 text-green-800'
  }
];

export default function TestCredentials({ onSelectCredential }: {
  onSelectCredential: (email: string, password: string) => void;
}) {
  return (
    <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">
        🧪 Test Credentials (Development Mode)
      </h3>
      <div className="space-y-2">
        {credentials.map((cred) => (
          <button
            key={cred.role}
            onClick={() => onSelectCredential(cred.username, cred.password)}
            className={`w-full text-left p-3 rounded border ${cred.color} hover:opacity-80 transition-opacity`}
          >
            <div className="font-medium text-sm">{cred.role}</div>
            <div className="text-xs mt-1 font-mono">{cred.username}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
```

**Deliverable**: Login page with test credentials for easy testing

---

#### Task 1.3: Enhance Auth Service JWT Tokens
**Location**: `/backend/services/auth/main.py`
**Duration**: 2 hours

**Steps**:
1. Update SSO login endpoint to include gamification claims
2. Add username field support (currently uses email)
3. Enhance token generation

**Implementation**:
```python
# /backend/services/auth/main.py

# Add username field to User model
class User(SQLAlchemyBaseUserTableUUID, Base):
    # ... existing fields ...
    username: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    # ... rest of fields ...

# Update SSO login endpoint
@app.post("/auth/sso/login", response_model=AuthResponse, tags=["auth:sso"])
@auth_duration.time()
async def sso_login(
    request: Request,
    login_data: LoginRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    ratelimit: str = Depends(RateLimiter(times=5, seconds=60))
):
    """Single Sign-On login with enhanced gamification claims"""
    try:
        # Find user by email OR username
        result = await session.execute(
            select(User).where(
                (User.email == login_data.email.lower()) |
                (User.username == login_data.email)  # Allow username login
            )
        )
        user = result.scalar_one_or_none()

        # ... existing validation code ...

        # Get gamification data for user
        gamification_data = await get_user_gamification_data(user.id, user.tenant_id, session)

        # Generate enhanced JWT token
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username or user.email.split('@')[0],
            "role": user.role.value,
            "tenant_id": str(user.tenant_id),
            "tenant_slug": user.tenant.slug,
            "permissions": user.permissions or [],
            "allowed_platforms": user.allowed_platforms,
            "platform": login_data.platform,
            "session_id": str(user_session.id),
            # NEW: Gamification claims
            "gamification": {
                "achievement_count": gamification_data.get("achievement_count", 0),
                "leaderboard_rank": gamification_data.get("leaderboard_rank"),
                "referral_code": gamification_data.get("referral_code"),
                "portfolio_id": gamification_data.get("portfolio_id"),
                "points": gamification_data.get("points", 0)
            },
            "exp": datetime.now(timezone.utc) + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        }

        access_token = jwt.encode(
            token_data,
            settings.secret_key,
            algorithm="HS256"
        )

        # ... rest of code ...

async def get_user_gamification_data(
    user_id: uuid.UUID,
    tenant_id: uuid.UUID,
    session: AsyncSession
) -> Dict[str, Any]:
    """Fetch user's gamification data from database"""
    try:
        # This will query gamification tables once they exist
        # For now, return empty data
        return {
            "achievement_count": 0,
            "leaderboard_rank": None,
            "referral_code": None,
            "portfolio_id": None,
            "points": 0
        }
    except Exception as e:
        logger.error(f"Failed to fetch gamification data: {e}")
        return {}
```

**Deliverable**: Enhanced JWT tokens with gamification support

---

#### Task 1.4: Create Test Users in Database
**Location**: Database migration
**Duration**: 1 hour

**Steps**:
1. Create Alembic migration to add test users
2. Seed database with test credentials

**Implementation**:
```bash
# Create migration
cd /home/alagiri/projects/bizoholic/bizosaas-platform/backend/services/auth
alembic revision -m "add_test_users"
```

```python
# Migration file: alembic/versions/xxx_add_test_users.py
"""add test users

Revision ID: xxx
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
import uuid
from datetime import datetime, timezone
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def upgrade():
    # Create default tenant first
    tenant_id = str(uuid.uuid4())

    conn = op.get_bind()

    # Insert default tenant
    conn.execute(text("""
        INSERT INTO tenants (id, name, slug, status, created_at, updated_at,
                           subscription_plan, max_users, allowed_platforms)
        VALUES (:id, :name, :slug, :status, :created_at, :updated_at,
                :plan, :max_users, :platforms::jsonb)
    """), {
        "id": tenant_id,
        "name": "BizOSaaS Admin Tenant",
        "slug": "bizosaas-admin",
        "status": "active",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "plan": "enterprise",
        "max_users": 1000,
        "platforms": '["bizoholic", "coreldove", "bizosaas-admin"]'
    })

    # Test users
    test_users = [
        {
            "id": str(uuid.uuid4()),
            "email": "superadmin@bizosaas.com",
            "username": "superadmin",
            "password": "BizoSaaS2025!Admin",
            "role": "super_admin",
            "first_name": "Super",
            "last_name": "Admin"
        },
        {
            "id": str(uuid.uuid4()),
            "email": "administrator@bizosaas.com",
            "username": "administrator",
            "password": "Bizoholic2025!Admin",
            "role": "tenant_admin",
            "first_name": "Tenant",
            "last_name": "Admin"
        },
        {
            "id": str(uuid.uuid4()),
            "email": "user@bizosaas.com",
            "username": "bizoholic_user",
            "password": "Bizoholic2025!User",
            "role": "user",
            "first_name": "Test",
            "last_name": "User"
        }
    ]

    for user in test_users:
        hashed_password = pwd_context.hash(user["password"])

        conn.execute(text("""
            INSERT INTO users (id, email, username, hashed_password, role,
                             tenant_id, first_name, last_name, is_active,
                             is_verified, is_superuser, created_at)
            VALUES (:id, :email, :username, :hashed_password, :role,
                    :tenant_id, :first_name, :last_name, :is_active,
                    :is_verified, :is_superuser, :created_at)
        """), {
            "id": user["id"],
            "email": user["email"],
            "username": user["username"],
            "hashed_password": hashed_password,
            "role": user["role"],
            "tenant_id": tenant_id,
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "is_active": True,
            "is_verified": True,
            "is_superuser": user["role"] == "super_admin",
            "created_at": datetime.now(timezone.utc)
        })

def downgrade():
    conn = op.get_bind()
    conn.execute(text("DELETE FROM users WHERE username IN ('superadmin', 'administrator', 'bizoholic_user')"))
    conn.execute(text("DELETE FROM tenants WHERE slug = 'bizosaas-admin'"))
```

**Run migration**:
```bash
docker exec -it bizosaas-auth-v2-8007 alembic upgrade head
```

**Deliverable**: Test users created in database

---

### DAY 2: Frontend Auth Integration

#### Task 2.1: Create Auth Middleware for Client Portal
**Location**: `/frontend/apps/client-portal/middleware.ts`
**Duration**: 2 hours

**Implementation**:
```typescript
// /frontend/apps/client-portal/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || 'http://localhost:8007';
const LOGIN_URL = process.env.LOGIN_URL || 'http://localhost:3002';

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('access_token')?.value;

  // Allow public routes
  if (request.nextUrl.pathname.startsWith('/public')) {
    return NextResponse.next();
  }

  if (!token) {
    return NextResponse.redirect(new URL(LOGIN_URL, request.url));
  }

  try {
    // Verify token with auth service through Brain Gateway
    const response = await fetch(`http://localhost:8002/api/v1/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'X-Platform': 'client-portal'
      }
    });

    if (!response.ok) {
      return NextResponse.redirect(new URL(LOGIN_URL, request.url));
    }

    const userData = await response.json();

    // Check role permissions (user, tenant_admin, super_admin allowed)
    const allowedRoles = ['user', 'tenant_admin', 'super_admin'];
    if (!allowedRoles.includes(userData.user.role)) {
      return NextResponse.redirect(new URL(`${LOGIN_URL}/unauthorized`, request.url));
    }

    // Add user context to headers for API routes
    const requestHeaders = new Headers(request.headers);
    requestHeaders.set('x-user-data', JSON.stringify(userData));
    requestHeaders.set('x-user-id', userData.user.id);
    requestHeaders.set('x-tenant-id', userData.tenant.id);
    requestHeaders.set('x-user-role', userData.user.role);

    return NextResponse.next({
      request: {
        headers: requestHeaders,
      },
    });

  } catch (error) {
    console.error('Auth middleware error:', error);
    return NextResponse.redirect(new URL(LOGIN_URL, request.url));
  }
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico|public).*)'],
};
```

**Deliverable**: Client portal protected with authentication

---

#### Task 2.2: Create Auth Middleware for Admin Dashboard
**Location**: `/frontend/apps/bizosaas-admin/middleware.ts`
**Duration**: 1 hour

**Implementation**: Same as Client Portal but with stricter role check:
```typescript
// Check role permissions (tenant_admin, super_admin only)
const allowedRoles = ['tenant_admin', 'super_admin'];
if (!allowedRoles.includes(userData.user.role)) {
  return NextResponse.redirect(new URL(`${LOGIN_URL}/unauthorized`, request.url));
}
```

**Deliverable**: Admin dashboard protected with admin-only access

---

#### Task 2.3: Create Auth Context Provider
**Location**: `/frontend/apps/client-portal/context/AuthContext.tsx`
**Duration**: 2 hours

**Implementation**:
```typescript
// /frontend/apps/client-portal/context/AuthContext.tsx
'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface User {
  id: string;
  email: string;
  username: string;
  role: string;
  first_name?: string;
  last_name?: string;
  tenant_id: string;
  permissions: string[];
  allowed_platforms: string[];
  gamification?: {
    achievement_count: number;
    leaderboard_rank?: number;
    referral_code?: string;
    points: number;
  };
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('access_token');

    if (!token) {
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:8002/api/v1/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setUser(data.user);
      } else {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    } catch (error) {
      console.error('Auth check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const response = await fetch('http://localhost:8002/api/v1/auth/sso/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, platform: 'client-portal' })
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const data = await response.json();

    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);

    setUser(data.user);
  };

  const logout = async () => {
    const token = localStorage.getItem('access_token');

    if (token) {
      try {
        await fetch('http://localhost:8002/api/v1/auth/sso/logout', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` }
        });
      } catch (error) {
        console.error('Logout error:', error);
      }
    }

    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    router.push('http://localhost:3002');
  };

  const refreshToken = async () => {
    const refreshToken = localStorage.getItem('refresh_token');

    if (!refreshToken) {
      throw new Error('No refresh token');
    }

    // Implement token refresh logic
    // This will call the refresh endpoint through Brain Gateway
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, refreshToken }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

**Deliverable**: Reusable auth context for all frontend apps

---

### DAY 3: SQLAdmin Rebuild

#### Task 3.1: Rebuild SQLAdmin with aminalaee/sqladmin
**Location**: `/backend/services/admin/sqladmin/main.py`
**Duration**: 4 hours

**Steps**:
1. Backup existing SQLAdmin code
2. Install aminalaee/sqladmin package
3. Implement authentication backend
4. Configure model views

**Implementation**: Continue with full rebuild...

[Document continues with detailed tasks for all remaining days...]

---

## ✅ Success Criteria

Each task must meet these criteria:
- ✅ Code runs without errors
- ✅ Docker container builds successfully
- ✅ Routes through Brain Gateway correctly
- ✅ Test credentials work as expected
- ✅ Multi-tenant isolation verified
- ✅ Performance within SLA (<100ms P95)

---

## 📊 Progress Tracking

Use TodoWrite tool to track each task:
```
- Create unified auth UI ← Currently in progress
- Implement login with test creds
- Enhance auth service JWT
- Add test users to database
... etc
```

---

**Total Tasks**: 150+ granular tasks across 15 days
**Total Lines of Code**: ~15,000 lines
**Total Containers**: 15+ services
**Total AI Agents**: 93 (88 existing + 5 gamification)