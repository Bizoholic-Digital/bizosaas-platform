// Role-Based Access Control Utilities
// Defines user roles and permissions for the Client Portal

// Role-Based Access Control Utilities
// Defines user roles and permissions for the Client Portal

// Matches Auth Service UserRole enum
export type UserRole = 'super_admin' | 'tenant_admin' | 'user' | 'readonly' | 'agent' | 'service_account';

export interface User {
    id: string;
    email: string;
    name: string;
    role: UserRole;
    tenant_id?: string;
    permissions?: string[];
}

export interface RolePermissions {
    canAccessAdmin: boolean;
    canAccessCRM: boolean;
    canAccessCMS: boolean;
    canAccessEcommerce: boolean;
    canAccessMarketing: boolean;
    canAccessAnalytics: boolean;
    canAccessBilling: boolean;
    canAccessIntegrations: boolean;
    canAccessSettings: boolean;
    canManageUsers: boolean;
    canManageTenants: boolean;
    canViewSystemMetrics: boolean;
}

// Role definitions with permissions
export const ROLE_PERMISSIONS: Record<UserRole, RolePermissions> = {
    super_admin: {
        canAccessAdmin: true,
        canAccessCRM: true,
        canAccessCMS: true,
        canAccessEcommerce: true,
        canAccessMarketing: true,
        canAccessAnalytics: true,
        canAccessBilling: true,
        canAccessIntegrations: true,
        canAccessSettings: true,
        canManageUsers: true,
        canManageTenants: true,
        canViewSystemMetrics: true,
    },
    tenant_admin: {
        canAccessAdmin: false,
        canAccessCRM: true,
        canAccessCMS: true,
        canAccessEcommerce: true,
        canAccessMarketing: true,
        canAccessAnalytics: true,
        canAccessBilling: true,
        canAccessIntegrations: true,
        canAccessSettings: true,
        canManageUsers: true,
        canManageTenants: false,
        canViewSystemMetrics: false,
    },
    user: {
        canAccessAdmin: false,
        canAccessCRM: true,
        canAccessCMS: false,
        canAccessEcommerce: false,
        canAccessMarketing: false,
        canAccessAnalytics: true,
        canAccessBilling: false,
        canAccessIntegrations: false,
        canAccessSettings: true,
        canManageUsers: false,
        canManageTenants: false,
        canViewSystemMetrics: false,
    },
    readonly: {
        canAccessAdmin: false,
        canAccessCRM: true, // Read-only logic handled in components
        canAccessCMS: true,
        canAccessEcommerce: true,
        canAccessMarketing: true,
        canAccessAnalytics: true,
        canAccessBilling: false,
        canAccessIntegrations: false,
        canAccessSettings: false,
        canManageUsers: false,
        canManageTenants: false,
        canViewSystemMetrics: false,
    },
    agent: {
        canAccessAdmin: false,
        canAccessCRM: true,
        canAccessCMS: false,
        canAccessEcommerce: false,
        canAccessMarketing: false,
        canAccessAnalytics: false,
        canAccessBilling: false,
        canAccessIntegrations: false,
        canAccessSettings: true,
        canManageUsers: false,
        canManageTenants: false,
        canViewSystemMetrics: false,
    },
    service_account: {
        canAccessAdmin: false,
        canAccessCRM: false,
        canAccessCMS: false,
        canAccessEcommerce: false,
        canAccessMarketing: false,
        canAccessAnalytics: false,
        canAccessBilling: false,
        canAccessIntegrations: false,
        canAccessSettings: false,
        canManageUsers: false,
        canManageTenants: false,
        canViewSystemMetrics: false,
    }
};

/**
 * Get permissions for a user role
 */
export function getPermissions(role: UserRole): RolePermissions {
    return ROLE_PERMISSIONS[role] || ROLE_PERMISSIONS['user'];
}

/**
 * Check if user has specific permission
 */
export function hasPermission(
    role: UserRole,
    permission: keyof RolePermissions
): boolean {
    const permissions = getPermissions(role);
    return permissions[permission];
}

/**
 * Filter menu items based on user permissions
 */
export function filterMenuByPermissions(
    menuItems: any[],
    permissions: RolePermissions
): any[] {
    return menuItems.filter((item) => {
        // Check if user has permission for this section
        switch (item.id) {
            case 'admin':
                return permissions.canAccessAdmin;
            case 'crm':
                return permissions.canAccessCRM;
            case 'cms':
                return permissions.canAccessCMS;
            case 'ecommerce':
                return permissions.canAccessEcommerce;
            case 'marketing':
                return permissions.canAccessMarketing;
            case 'analytics':
                return permissions.canAccessAnalytics;
            case 'billing':
                return permissions.canAccessBilling;
            case 'integrations':
                return permissions.canAccessIntegrations;
            case 'settings':
                return permissions.canAccessSettings;
            default:
                return true; // Show dashboard and other items by default
        }
    });
}

/**
 * Get user display info from Session
 */
export function getUserDisplayInfoFromSession(sessionUser: any): {
    role: UserRole;
    permissions: RolePermissions;
    tenantId: string | null;
    displayName: string;
} {
    // Default to 'tenant_admin' for development (shows all menu items)
    // In production, this should be more restrictive
    const role = (sessionUser?.role as UserRole) || 'tenant_admin';
    const permissions = getPermissions(role);
    const tenantId = sessionUser?.tenant_id || null;

    let displayName = sessionUser?.name || sessionUser?.email?.split('@')[0] || 'User';

    if (role === 'super_admin') displayName = '👑 ' + displayName;
    if (role === 'tenant_admin') displayName = '⭐ ' + displayName;

    return {
        role,
        permissions,
        tenantId,
        displayName,
    };
}

/**
 * Fallback: Get user display info from email (for testing/dev without full auth)
 */
export function getUserDisplayInfo(email: string): {
    role: UserRole;
    permissions: RolePermissions;
    tenantId: string | null;
    displayName: string;
} {
    let role: UserRole = 'user';

    if (email.includes('superadmin')) role = 'super_admin';
    else if (email.includes('admin')) role = 'tenant_admin';

    const permissions = getPermissions(role);

    let tenantId = null;
    if (email.includes('coreldove')) tenantId = 'coreldove';
    if (email.includes('thrillring')) tenantId = 'thrillring';
    if (email.includes('quanttrade')) tenantId = 'quanttrade';
    if (email.includes('bizoholic')) tenantId = 'bizoholic';

    let displayName = email.split('@')[0];
    if (role === 'super_admin') displayName = '👑 ' + displayName;
    if (role === 'tenant_admin') displayName = '⭐ ' + displayName;

    return {
        role,
        permissions,
        tenantId,
        displayName,
    };
}

