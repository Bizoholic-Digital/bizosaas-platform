# BizOSaaS Platform Architecture - Two Applications

## 🏗️ Architecture Overview

You have **TWO separate Next.js applications** serving different purposes:

### 1. Bizoholic Frontend (Port 3001)
**Purpose**: Public Marketing Website  
**URL**: http://localhost:3001  
**Contains**:
- Homepage
- Services pages
- About page
- Blog
- Case studies
- Contact forms
- Public content

**Authentication**: None required (public website)

### 2. Client Portal (Port 3003)
**Purpose**: Authenticated Dashboard for Logged-in Users  
**URL**: http://localhost:3003  
**Contains**:
- Login page (`/login`)
- Dashboard (`/`)
- CRM features
- Content management
- Analytics
- Settings
- All authenticated features

**Authentication**: NextAuth + Auth Service (Hybrid)

## 🔄 How They Work Together

### User Journey:
1. User visits **Bizoholic Frontend** (3001) - sees marketing content
2. User clicks "Login" or "Dashboard" button
3. Gets redirected to **Client Portal** (3003/login)
4. After login, stays on **Client Portal** (3003) for all dashboard features

### Redirect Configuration:
The Bizoholic Frontend now has a redirect rule:
```javascript
// In brands/bizoholic/frontend/next.config.js
async redirects() {
  return [
    {
      source: '/portal/:path*',
      destination: 'http://localhost:3003/:path*',
      permanent: false,
    },
  ];
}
```

This means:
- `http://localhost:3001/portal/login` → Redirects to → `http://localhost:3003/login`
- `http://localhost:3001/portal/dashboard` → Redirects to → `http://localhost:3003/dashboard`

## ✅ Correct URLs

### For Public Content (Marketing):
- Homepage: `http://localhost:3001`
- Services: `http://localhost:3001/services`
- About: `http://localhost:3001/about`
- Blog: `http://localhost:3001/blog`

### For Authenticated Features (Dashboard):
- Login: `http://localhost:3003/login`
- Dashboard: `http://localhost:3003` or `http://localhost:3003/dashboard`
- CRM: `http://localhost:3003?tab=crm`
- Settings: `http://localhost:3003?tab=settings`

## 🚫 What NOT to Use

❌ **Don't use**: `http://localhost:3001/portal/login`  
✅ **Use instead**: `http://localhost:3003/login`

❌ **Don't use**: `http://localhost:3001/portal/dashboard`  
✅ **Use instead**: `http://localhost:3003`

## 🔐 Authentication Flow

```
User → Bizoholic (3001) → Clicks "Login" → Redirected to Client Portal (3003/login)
                                                    ↓
                                            NextAuth validates
                                                    ↓
                                            Calls Auth Service (8008)
                                                    ↓
                                            Creates session
                                                    ↓
                                            Redirects to Dashboard (3003/)
```

## 🛠️ Current Status

After running `./scripts/start-bizosaas-full.sh`:

| Service | Port | Status | Purpose |
|---------|------|--------|---------|
| Bizoholic Frontend | 3001 | ⚠️ Starting | Public marketing website |
| Client Portal | 3003 | ✅ Running | Authenticated dashboard |
| Brain Gateway | 8001 | ✅ Running | API proxy |
| Auth Service | 8008 | ✅ Running | Authentication |
| Postgres | 5432 | ✅ Running | Database |
| Redis | 6379 | ✅ Running | Cache/Sessions |

**Note**: Bizoholic Frontend (3001) takes longer to start because it's compiling Next.js pages. Give it 30-60 seconds after the script finishes.

## 📝 Next Steps

1. **Wait for Bizoholic Frontend to finish starting**:
   ```bash
   tail -f /tmp/bizoholic-frontend.log
   ```
   Wait until you see: `✓ Ready in XXXms`

2. **Test the redirect**:
   - Visit `http://localhost:3001/portal/login`
   - Should redirect to `http://localhost:3003/login`

3. **Login**:
   - Go to `http://localhost:3003/login`
   - Use: `admin@bizoholic.com / AdminDemo2024!`
   - Should redirect to dashboard at `http://localhost:3003`

## 🎯 Summary

- **Two separate apps** for different purposes
- **Bizoholic (3001)** = Public website
- **Client Portal (3003)** = Authenticated dashboard
- **Redirects configured** to send `/portal/*` from 3001 to 3003
- **Use Client Portal directly** for all authenticated features
