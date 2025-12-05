# Unified Dashboard with Role-Based Access Control (RBAC)

## 🎯 Proposal: Single Dashboard for All Users

Yes, **merging the dashboards is the recommended approach**! Here's why and how:

### ✅ Benefits of a Unified Dashboard

1. **Single Codebase** - Easier to maintain
2. **Consistent UX** - Same interface for all users
3. **Better Security** - Centralized permission management
4. **Easier Updates** - One place to add new features
5. **Simplified Architecture** - No need for separate portals

## 🔐 Role-Based Access Control (RBAC) Structure

### User Roles & Permissions

```typescript
enum UserRole {
  SUPER_ADMIN = 'super_admin',      // Full system access
  TENANT_ADMIN = 'tenant_admin',    // Manage their tenant
  ADMIN = 'admin',                  // Manage users & content
  CLIENT = 'client',                // Limited access
  USER = 'user'                     // Basic access
}
```

### Dashboard Tabs by Role

| Tab/Feature | Super Admin | Tenant Admin | Admin | Client | User |
|-------------|-------------|--------------|-------|--------|------|
| **Dashboard** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **CRM** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Content (CMS)** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **E-commerce** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Marketing** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Analytics** | ✅ | ✅ | ✅ | ✅ (limited) | ❌ |
| **Billing** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Team Management** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Integrations** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **System Settings** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Tenant Management** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **User Management** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **My Services** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Support** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **My Profile** | ✅ | ✅ | ✅ | ✅ | ✅ |

## 📋 Implementation Plan

### Step 1: Define Permission System

Create `/portals/client-portal/lib/permissions.ts`:

```typescript
export const PERMISSIONS = {
  // Dashboard
  VIEW_DASHBOARD: ['super_admin', 'tenant_admin', 'admin', 'client', 'user'],
  
  // CRM
  VIEW_CRM: ['super_admin', 'tenant_admin', 'admin'],
  MANAGE_LEADS: ['super_admin', 'tenant_admin', 'admin'],
  MANAGE_CONTACTS: ['super_admin', 'tenant_admin', 'admin'],
  MANAGE_DEALS: ['super_admin', 'tenant_admin', 'admin'],
  
  // Content
  VIEW_CMS: ['super_admin', 'tenant_admin', 'admin'],
  EDIT_CONTENT: ['super_admin', 'tenant_admin', 'admin'],
  PUBLISH_CONTENT: ['super_admin', 'tenant_admin', 'admin'],
  
  // E-commerce
  VIEW_ECOMMERCE: ['super_admin', 'tenant_admin', 'admin'],
  MANAGE_PRODUCTS: ['super_admin', 'tenant_admin', 'admin'],
  MANAGE_ORDERS: ['super_admin', 'tenant_admin', 'admin'],
  
  // Marketing
  VIEW_MARKETING: ['super_admin', 'tenant_admin', 'admin'],
  MANAGE_CAMPAIGNS: ['super_admin', 'tenant_admin', 'admin'],
  
  // Analytics
  VIEW_ANALYTICS: ['super_admin', 'tenant_admin', 'admin', 'client'],
  VIEW_FULL_ANALYTICS: ['super_admin', 'tenant_admin', 'admin'],
  
  // Billing
  VIEW_BILLING: ['super_admin', 'tenant_admin', 'admin', 'client'],
  MANAGE_BILLING: ['super_admin', 'tenant_admin', 'admin'],
  
  // Team
  VIEW_TEAM: ['super_admin', 'tenant_admin', 'admin'],
  MANAGE_TEAM: ['super_admin', 'tenant_admin', 'admin'],
  
  // System
  SYSTEM_SETTINGS: ['super_admin'],
  TENANT_MANAGEMENT: ['super_admin', 'tenant_admin'],
  USER_MANAGEMENT: ['super_admin', 'tenant_admin', 'admin'],
};

export function hasPermission(userRole: string, permission: keyof typeof PERMISSIONS): boolean {
  return PERMISSIONS[permission]?.includes(userRole) || false;
}
```

### Step 2: Update Sidebar Items with Permissions

Update `/portals/client-portal/app/page.tsx`:

```typescript
const sidebarItems = [
  {
    id: 'dashboard',
    icon: Home,
    label: 'Dashboard',
    permission: 'VIEW_DASHBOARD',
  },
  {
    id: 'crm',
    icon: Users,
    label: 'CRM',
    permission: 'VIEW_CRM',
    children: [
      { id: 'leads', label: 'Leads', permission: 'MANAGE_LEADS' },
      { id: 'contacts', label: 'Contacts', permission: 'MANAGE_CONTACTS' },
      { id: 'deals', label: 'Deals', permission: 'MANAGE_DEALS' },
    ]
  },
  {
    id: 'cms',
    icon: FileText,
    label: 'Content (CMS)',
    permission: 'VIEW_CMS',
  },
  // ... more items
];

// Filter sidebar items based on user role
const filteredSidebarItems = sidebarItems.filter(item => 
  hasPermission(userRole, item.permission)
);
```

### Step 3: Get User Role from Session

Update the dashboard to get the user's role from NextAuth session:

```typescript
import { useSession } from 'next-auth/react';

export default function ClientPortalDashboard() {
  const { data: session } = useSession();
  const userRole = session?.user?.role || 'user';
  
  // Use userRole to filter sidebar items
  const filteredSidebarItems = sidebarItems.filter(item => 
    hasPermission(userRole, item.permission)
  );
  
  // ...
}
```

### Step 4: Update NextAuth to Include Role

Update `/portals/client-portal/app/api/auth/[...nextauth]/route.ts`:

```typescript
callbacks: {
  async jwt({ token, user }) {
    if (user) {
      token.role = user.role;
      token.tenant_id = user.tenant_id;
    }
    return token;
  },
  async session({ session, token }) {
    if (session.user) {
      session.user.role = token.role;
      session.user.tenant_id = token.tenant_id;
    }
    return session;
  },
}
```

## 🎨 Dashboard Customization by Role

### Super Admin Dashboard
- System health monitoring
- All tenants overview
- Global analytics
- System configuration
- User management across all tenants

### Tenant Admin Dashboard
- Tenant-specific metrics
- Team management
- Billing & subscriptions
- Tenant settings

### Admin Dashboard
- Content management
- CRM tools
- Marketing campaigns
- Team collaboration

### Client Dashboard
- Service usage
- Billing information
- Support tickets
- Basic analytics

### User Dashboard
- Personal services
- Profile settings
- Support access

## 🚀 Migration Steps

1. **Create Permission System** (1-2 hours)
   - Define permissions
   - Create helper functions
   - Add role checks

2. **Update Sidebar** (2-3 hours)
   - Add permission checks to sidebar items
   - Filter based on user role
   - Test with different roles

3. **Update NextAuth** (1 hour)
   - Add role to JWT token
   - Include role in session
   - Update TypeScript types

4. **Test All Roles** (2-3 hours)
   - Login as each role
   - Verify correct tabs show
   - Test permissions

5. **Add Role-Specific Content** (3-4 hours)
   - Customize dashboard widgets per role
   - Add role-specific features
   - Implement data filtering

## 📝 Test Accounts (Already Created)

```
Super Admin:   superadmin@bizosaas.com / BizoSaaS2025!Admin
Tenant Admin:  administrator@bizosaas.com / Bizoholic2025!Admin
Admin:         admin@bizoholic.com / AdminDemo2024!
Client:        client@bizosaas.com / ClientDemo2024!
User:          user@bizosaas.com / Bizoholic2025!User
```

## ✅ Recommendation

**YES, merge the dashboards!** This will give you:
- ✅ Single, maintainable codebase
- ✅ Consistent user experience
- ✅ Easier to add new features
- ✅ Better security with centralized permissions
- ✅ Scalable architecture

The RBAC system will ensure each user only sees what they're allowed to access.

## 🎯 Next Steps

1. Fix the hydration error (✅ Done above)
2. Implement the permission system
3. Update sidebar with role-based filtering
4. Test with all user roles
5. Add role-specific dashboard widgets

Would you like me to implement the RBAC system now?
