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
    plan_features?: string[];
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

// Map Permission Keys to Lago Plan Feature Slugs
export const PERMISSION_FEATURE_MAP: Partial<Record<keyof RolePermissions, string>> = {
    canAccessCRM: 'crm',
    canAccessCMS: 'cms',
    canAccessEcommerce: 'ecommerce',
    canAccessMarketing: 'marketing',
    canAccessAnalytics: 'analytics',
    canAccessBilling: 'billing',
    canAccessIntegrations: 'api_access',
};

/**
 * Get base permissions for a role
 */
export function getPermissions(role: UserRole): RolePermissions {
    return ROLE_PERMISSIONS[role] || ROLE_PERMISSIONS['user'];
}

/**
 * Calculate effective permissions based on Role and Plan Features
 */
export function getEffectivePermissions(
    role: UserRole,
    planFeatures: string[] = []
): RolePermissions {
    const basePermissions = ROLE_PERMISSIONS[role] || ROLE_PERMISSIONS['user'];

    // Create a copy to modify
    const effective: RolePermissions = { ...basePermissions };

    // Intersect with plan features for relevant keys
    (Object.keys(PERMISSION_FEATURE_MAP) as Array<keyof RolePermissions>).forEach((key) => {
        const featureSlug = PERMISSION_FEATURE_MAP[key];
        if (featureSlug) {
            // Permission is only granted if BOTH role allows it AND plan includes the feature
            effective[key] = basePermissions[key] && planFeatures.includes(featureSlug);
        }
    });

    return effective;
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
 * Get user display info from Session (including Lago Plan Entitlements)
 */
export function getUserDisplayInfoFromSession(sessionUser: any): {
    role: UserRole;
    permissions: RolePermissions;
    tenantId: string | null;
    displayName: string;
} {
    const role = (sessionUser?.role as UserRole) || 'user';
    const planFeatures = sessionUser?.plan_features || [];
    const permissions = getEffectivePermissions(role, planFeatures);
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

