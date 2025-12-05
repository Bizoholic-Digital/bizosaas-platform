
import { getUserDisplayInfoFromSession, filterMenuByPermissions, ROLE_PERMISSIONS } from './utils/rbac';

// Mock session users
const superAdminSession = {
    role: 'super_admin',
    name: 'Super Admin',
    email: 'superadmin@bizosaas.com',
    tenant_id: 'system'
};

const tenantAdminSession = {
    role: 'tenant_admin',
    name: 'Tenant Admin',
    email: 'admin@coreldove.com',
    tenant_id: 'coreldove'
};

const userSession = {
    role: 'user',
    name: 'Regular User',
    email: 'user@coreldove.com',
    tenant_id: 'coreldove'
};

// Mock menu items
const menuItems = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'admin', label: 'Admin' },
    { id: 'crm', label: 'CRM' },
    { id: 'settings', label: 'Settings' }
];

console.log('--- RBAC Test ---');

// Test Super Admin
const superAdminInfo = getUserDisplayInfoFromSession(superAdminSession);
console.log('Super Admin Role:', superAdminInfo.role);
console.log('Super Admin Display Name:', superAdminInfo.displayName);
const superAdminMenu = filterMenuByPermissions(menuItems, superAdminInfo.permissions);
console.log('Super Admin Menu:', superAdminMenu.map(i => i.id));

// Test Tenant Admin
const tenantAdminInfo = getUserDisplayInfoFromSession(tenantAdminSession);
console.log('\nTenant Admin Role:', tenantAdminInfo.role);
console.log('Tenant Admin Display Name:', tenantAdminInfo.displayName);
const tenantAdminMenu = filterMenuByPermissions(menuItems, tenantAdminInfo.permissions);
console.log('Tenant Admin Menu:', tenantAdminMenu.map(i => i.id));

// Test Regular User
const userInfo = getUserDisplayInfoFromSession(userSession);
console.log('\nUser Role:', userInfo.role);
console.log('User Display Name:', userInfo.displayName);
const userMenu = filterMenuByPermissions(menuItems, userInfo.permissions);
console.log('User Menu:', userMenu.map(i => i.id));
