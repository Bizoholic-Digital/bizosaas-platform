'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  Users, 
  Building2, 
  Settings, 
  BarChart3,
  Zap,
  Target,
  Users2,
  Package,
  ShoppingCart,
  Truck,
  FileText,
  CreditCard,
  HelpCircle,
  Bell
} from 'lucide-react';
import { PLATFORM_BRANDS, type PlatformBrand } from '../../lib/constants/branding';
import { PermissionGate } from '../../lib/auth/auth-guard';
import { PERMISSIONS, ROLES } from '../../lib/constants/permissions';

interface NavigationItem {
  label: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  permission?: string;
  role?: string;
  children?: NavigationItem[];
}

interface PlatformNavigationProps {
  platform: PlatformBrand;
  collapsed?: boolean;
  onItemClick?: (href: string) => void;
}

const PLATFORM_NAVIGATION: Record<PlatformBrand, NavigationItem[]> = {
  BIZOSAAS: [
    {
      label: 'Dashboard',
      href: '/admin',
      icon: LayoutDashboard,
      permission: PERMISSIONS.SUPER_ADMIN.SYSTEM.METRICS
    },
    {
      label: 'Tenants',
      href: '/admin/tenants',
      icon: Building2,
      permission: PERMISSIONS.SUPER_ADMIN.TENANTS.READ,
      children: [
        {
          label: 'All Tenants',
          href: '/admin/tenants',
          icon: Building2,
          permission: PERMISSIONS.SUPER_ADMIN.TENANTS.READ
        },
        {
          label: 'Create Tenant',
          href: '/admin/tenants/create',
          icon: Building2,
          permission: PERMISSIONS.SUPER_ADMIN.TENANTS.CREATE
        }
      ]
    },
    {
      label: 'Users',
      href: '/admin/users',
      icon: Users,
      permission: PERMISSIONS.SUPER_ADMIN.USERS.READ,
      children: [
        {
          label: 'All Users',
          href: '/admin/users',
          icon: Users,
          permission: PERMISSIONS.SUPER_ADMIN.USERS.READ
        },
        {
          label: 'User Roles',
          href: '/admin/users/roles',
          icon: Users,
          permission: PERMISSIONS.SUPER_ADMIN.USERS.ROLES
        }
      ]
    },
    {
      label: 'AI Agents',
      href: '/admin/agents',
      icon: Zap,
      permission: PERMISSIONS.SUPER_ADMIN.AGENTS.READ,
      children: [
        {
          label: 'All Agents',
          href: '/admin/agents',
          icon: Zap,
          permission: PERMISSIONS.SUPER_ADMIN.AGENTS.READ
        },
        {
          label: 'Deploy Agent',
          href: '/admin/agents/deploy',
          icon: Zap,
          permission: PERMISSIONS.SUPER_ADMIN.AGENTS.DEPLOY
        },
        {
          label: 'Monitoring',
          href: '/admin/agents/monitoring',
          icon: BarChart3,
          permission: PERMISSIONS.SUPER_ADMIN.AGENTS.MONITOR
        }
      ]
    },
    {
      label: 'Analytics',
      href: '/admin/analytics',
      icon: BarChart3,
      permission: PERMISSIONS.SUPER_ADMIN.SYSTEM.METRICS
    },
    {
      label: 'Settings',
      href: '/admin/settings',
      icon: Settings,
      permission: PERMISSIONS.SUPER_ADMIN.SYSTEM.SETTINGS
    }
  ],

  BIZOHOLIC: [
    {
      label: 'Dashboard',
      href: '/dashboard',
      icon: LayoutDashboard
    },
    {
      label: 'Campaigns',
      href: '/campaigns',
      icon: Target,
      permission: PERMISSIONS.MARKETING_MANAGER.CAMPAIGNS.READ,
      children: [
        {
          label: 'All Campaigns',
          href: '/campaigns',
          icon: Target,
          permission: PERMISSIONS.MARKETING_MANAGER.CAMPAIGNS.READ
        },
        {
          label: 'Create Campaign',
          href: '/campaigns/create',
          icon: Target,
          permission: PERMISSIONS.MARKETING_MANAGER.CAMPAIGNS.CREATE
        },
        {
          label: 'Templates',
          href: '/campaigns/templates',
          icon: Target
        }
      ]
    },
    {
      label: 'Leads',
      href: '/leads',
      icon: Users2,
      permission: PERMISSIONS.MARKETING_MANAGER.LEADS.READ,
      children: [
        {
          label: 'All Leads',
          href: '/leads',
          icon: Users2,
          permission: PERMISSIONS.MARKETING_MANAGER.LEADS.READ
        },
        {
          label: 'Lead Scoring',
          href: '/leads/scoring',
          icon: Users2,
          permission: PERMISSIONS.MARKETING_MANAGER.LEADS.READ
        }
      ]
    },
    {
      label: 'Clients',
      href: '/clients',
      icon: Building2,
      permission: PERMISSIONS.MARKETING_MANAGER.CLIENTS.READ
    },
    {
      label: 'Analytics',
      href: '/analytics',
      icon: BarChart3,
      permission: PERMISSIONS.MARKETING_MANAGER.ANALYTICS.READ
    },
    {
      label: 'Reports',
      href: '/reports',
      icon: FileText,
      permission: PERMISSIONS.MARKETING_MANAGER.REPORTS.READ
    }
  ],

  CORELDOVE: [
    {
      label: 'Dashboard',
      href: '/dashboard',
      icon: LayoutDashboard
    },
    {
      label: 'Products',
      href: '/products',
      icon: Package,
      permission: PERMISSIONS.ECOMMERCE_MANAGER.PRODUCTS.READ,
      children: [
        {
          label: 'All Products',
          href: '/products',
          icon: Package,
          permission: PERMISSIONS.ECOMMERCE_MANAGER.PRODUCTS.READ
        },
        {
          label: 'Add Product',
          href: '/products/create',
          icon: Package,
          permission: PERMISSIONS.ECOMMERCE_MANAGER.PRODUCTS.CREATE
        },
        {
          label: 'Categories',
          href: '/products/categories',
          icon: Package
        }
      ]
    },
    {
      label: 'Sourcing',
      href: '/sourcing',
      icon: Truck,
      permission: PERMISSIONS.ECOMMERCE_MANAGER.SOURCING.SEARCH,
      children: [
        {
          label: 'Product Search',
          href: '/sourcing/search',
          icon: Truck,
          permission: PERMISSIONS.ECOMMERCE_MANAGER.SOURCING.SEARCH
        },
        {
          label: 'Suppliers',
          href: '/sourcing/suppliers',
          icon: Truck,
          permission: PERMISSIONS.ECOMMERCE_MANAGER.SUPPLIERS.READ
        },
        {
          label: 'Analytics',
          href: '/sourcing/analytics',
          icon: BarChart3,
          permission: PERMISSIONS.ECOMMERCE_MANAGER.SOURCING.ANALYZE
        }
      ]
    },
    {
      label: 'Inventory',
      href: '/inventory',
      icon: Package,
      permission: PERMISSIONS.ECOMMERCE_MANAGER.INVENTORY.READ
    },
    {
      label: 'Orders',
      href: '/orders',
      icon: ShoppingCart,
      permission: PERMISSIONS.ECOMMERCE_MANAGER.ORDERS.READ
    },
    {
      label: 'Analytics',
      href: '/analytics',
      icon: BarChart3
    }
  ],

  CLIENT_PORTAL: [
    {
      label: 'Dashboard',
      href: '/portal',
      icon: LayoutDashboard
    },
    {
      label: 'Services',
      href: '/portal/services',
      icon: Zap,
      permission: PERMISSIONS.CLIENT_USER.SERVICES.READ
    },
    {
      label: 'Billing',
      href: '/portal/billing',
      icon: CreditCard,
      permission: PERMISSIONS.CLIENT_USER.BILLING.READ,
      children: [
        {
          label: 'Invoices',
          href: '/portal/billing/invoices',
          icon: FileText,
          permission: PERMISSIONS.CLIENT_USER.BILLING.INVOICES
        },
        {
          label: 'Payment Methods',
          href: '/portal/billing/payments',
          icon: CreditCard,
          permission: PERMISSIONS.CLIENT_USER.BILLING.PAYMENTS
        }
      ]
    },
    {
      label: 'Support',
      href: '/portal/support',
      icon: HelpCircle,
      permission: PERMISSIONS.CLIENT_USER.SUPPORT.READ,
      children: [
        {
          label: 'Tickets',
          href: '/portal/support/tickets',
          icon: HelpCircle,
          permission: PERMISSIONS.CLIENT_USER.SUPPORT.READ
        },
        {
          label: 'Knowledge Base',
          href: '/portal/support/knowledge',
          icon: FileText
        }
      ]
    },
    {
      label: 'Reports',
      href: '/portal/reports',
      icon: BarChart3,
      permission: PERMISSIONS.CLIENT_USER.REPORTS.READ
    },
    {
      label: 'Settings',
      href: '/portal/settings',
      icon: Settings,
      permission: PERMISSIONS.CLIENT_USER.PROFILE.UPDATE
    }
  ]
};

export function PlatformNavigation({ 
  platform, 
  collapsed = false,
  onItemClick 
}: PlatformNavigationProps) {
  const pathname = usePathname();
  const navigationItems = PLATFORM_NAVIGATION[platform];
  const brandConfig = PLATFORM_BRANDS[platform];

  const isActiveRoute = (href: string) => {
    if (href === '/') return pathname === '/';
    return pathname.startsWith(href);
  };

  const renderNavigationItem = (item: NavigationItem, level = 0) => {
    const isActive = isActiveRoute(item.href);
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = hasChildren && item.children.some(child => isActiveRoute(child.href));

    const navigationContent = (
      <div className={`
        group flex items-center w-full px-3 py-2 text-sm font-medium rounded-md transition-colors
        ${isActive 
          ? 'bg-primary/10 text-primary border-r-2 border-primary' 
          : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-800 dark:hover:text-white'
        }
        ${level > 0 ? 'ml-4 pl-8' : ''}
      `}>
        <item.icon className={`
          ${collapsed ? 'h-6 w-6' : 'h-5 w-5 mr-3'} 
          ${isActive ? 'text-primary' : 'text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-300'}
        `} />
        {!collapsed && (
          <>
            <span className="truncate">{item.label}</span>
            {hasChildren && (
              <svg
                className={`ml-auto h-4 w-4 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            )}
          </>
        )}
      </div>
    );

    return (
      <div key={item.href}>
        <PermissionGate permission={item.permission} role={item.role as any}>
          <Link
            href={item.href}
            onClick={() => onItemClick?.(item.href)}
            className="block"
          >
            {navigationContent}
          </Link>
          
          {/* Render children if expanded and not collapsed */}
          {!collapsed && hasChildren && isExpanded && (
            <div className="mt-1">
              {item.children!.map(child => renderNavigationItem(child, level + 1))}
            </div>
          )}
        </PermissionGate>
      </div>
    );
  };

  return (
    <nav className="flex-1 space-y-1 px-2 py-4">
      {navigationItems.map(item => renderNavigationItem(item))}
    </nav>
  );
}