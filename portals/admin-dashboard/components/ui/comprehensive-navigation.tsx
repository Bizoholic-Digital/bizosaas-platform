'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useSearchParams } from 'next/navigation';
import { useSystemStatus } from '@/lib/hooks/useSystemStatus';
import {
  Home, Users, FileText, ShoppingCart, Building2, BarChart3,
  Settings, User, Brain, Zap, Target, TrendingUp, Database,
  Globe, Search, MessageSquare, Phone, Mail, Calendar,
  Package, CreditCard, UserCheck, Shield, Bell, Download,
  BookOpen, Image, Video, Newspaper, Tag, Filter,
  PieChart, Activity, LineChart, TrendingDown, AlertCircle,
  ChevronDown, ChevronRight, Menu, X, RefreshCw, Bot,
  Sparkles, ShieldCheck, Layers, Link2
} from 'lucide-react';
import { useAuth } from '@/shared/components/AuthProvider';
import { getEffectivePermissions, RolePermissions } from '@/lib/rbac';

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface NavigationItem {
  id: string;
  name: string;
  href: string;
  icon: React.ReactNode;
  badge?: string;
  active?: boolean;
  subItems?: NavigationItem[];
  show?: boolean;
}

interface NavigationProps {
  onNavigate?: (path: string) => void;
  isCollapsed?: boolean;
}

const ComprehensiveNavigation: React.FC<NavigationProps> = ({ onNavigate, isCollapsed }) => {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [expandedSections, setExpandedSections] = useState<string[]>(['dashboard', 'management']);
  const { metrics } = useSystemStatus();
  const { user } = useAuth();

  const effectivePermissions = getEffectivePermissions(
    (user?.role as any) || 'user',
    user?.plan_features || []
  );

  // Auto-expand sections based on current path
  useEffect(() => {
    let activeSection = 'workspace'; // Default

    if (pathname.includes('/tenants') || pathname.includes('/users') || pathname.includes('/directory') || pathname.includes('/dashboard/tools') || pathname === '/dashboard/partner' || pathname === '/dashboard/plugin-analytics') {
      activeSection = 'management';
    } else if (pathname.includes('/system-status') || pathname.includes('/connectors')) {
      activeSection = 'connectivity';
    } else if (pathname.includes('/security') || pathname.includes('/settings')) {
      activeSection = 'platform';
    } else if (pathname === '/dashboard' || pathname === '/dashboard/ai-assistant' || pathname === '/dashboard/agent-management') {
      activeSection = 'workspace';
    }

    setExpandedSections([activeSection]);
  }, [pathname]);

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev =>
      prev.includes(sectionId) ? [] : [sectionId]
    );
  };

  const navigationItems: NavigationItem[] = [
    {
      id: 'workspace',
      name: isCollapsed ? 'Home' : 'Workspace',
      href: '#',
      icon: <Home className="w-5 h-5 text-gray-500" />,
      subItems: [
        {
          id: 'dashboard',
          name: 'Admin Overview',
          href: '/dashboard',
          icon: <Home className="w-4 h-4" />,
          active: pathname === '/dashboard' || pathname === '/'
        },
        {
          id: 'ai-assistant',
          name: 'AI Admin Assistant',
          href: '/dashboard/ai-assistant',
          icon: <Sparkles className="w-4 h-4 text-indigo-500" />,
          badge: isCollapsed ? undefined : 'AI',
          active: pathname === '/dashboard/ai-assistant'
        },
        {
          id: 'agent-management',
          name: 'Agent Management',
          href: '/dashboard/agent-management',
          icon: <Bot className="w-4 h-4 text-blue-500" />,
          active: pathname === '/dashboard/agent-management'
        }
      ]
    },
    {
      id: 'management',
      name: isCollapsed ? 'Manage' : 'Platform Management',
      href: '#',
      icon: <Layers className="w-5 h-5 text-gray-500" />,
      subItems: [
        {
          id: 'tenant-management',
          name: 'Tenant Management',
          href: '/dashboard/tenants',
          icon: <Building2 className="w-4 h-4" />,
          active: pathname === '/dashboard/tenants',
          show: effectivePermissions.canManageTenants
        },
        {
          id: 'user-management',
          name: 'Global Users',
          href: '/dashboard/users',
          icon: <Users className="w-4 h-4" />,
          active: pathname === '/dashboard/users',
          show: effectivePermissions.canManageUsers
        },
        {
          id: 'business-directory',
          name: 'Business Directory',
          href: '/dashboard/directory',
          icon: <Globe className="w-4 h-4 text-emerald-500" />,
          active: pathname === '/dashboard/directory'
        },
        {
          id: 'partner-program',
          name: 'Partner Program',
          href: '/dashboard/partner',
          icon: <Target className="w-4 h-4 text-purple-500" />,
          active: pathname === '/dashboard/partner'
        },
        {
          id: 'plugin-analytics',
          name: 'Marketplace Demand',
          href: '/dashboard/plugin-analytics',
          icon: <BarChart3 className="w-4 h-4 text-emerald-500" />,
          badge: isCollapsed ? undefined : 'GROWTH',
          active: pathname === '/dashboard/plugin-analytics',
          show: effectivePermissions.canAccessAnalytics
        },
        {
          id: 'tool-registry',
          name: 'Tool Registry',
          href: '/dashboard/tools',
          icon: <Package className="w-4 h-4 text-blue-500" />,
          active: pathname === '/dashboard/tools',
          show: effectivePermissions.canAccessIntegrations
        }
      ]
    },
    {
      id: 'connectivity',
      name: isCollapsed ? 'System' : 'System & Connectivity',
      href: '#',
      icon: <Activity className="w-5 h-5 text-gray-500" />,
      subItems: [
        {
          id: 'system-health',
          name: 'Real-time Health',
          href: '/dashboard/system-status',
          icon: <Activity className="w-4 h-4" />,
          active: pathname === '/dashboard/system-status',
          show: effectivePermissions.canViewSystemMetrics
        },
        {
          id: 'connectivity-hub',
          name: 'Connectivity Hub',
          href: '/dashboard/connectors',
          icon: <RefreshCw className="w-4 h-4 text-emerald-500" />,
          active: pathname === '/dashboard/connectors',
          show: effectivePermissions.canAccessIntegrations
        }
      ]
    },
    {
      id: 'platform',
      name: isCollapsed ? 'Admin' : 'Infrastructure & Admin',
      href: '#',
      icon: <Settings className="w-5 h-5 text-gray-500" />,
      subItems: [
        {
          id: 'security-audit',
          name: 'Security & Audit',
          href: '/dashboard/security',
          icon: <Shield className="w-4 h-4 text-red-500" />,
          active: pathname === '/dashboard/security',
          show: effectivePermissions.canAccessAdmin
        },
        {
          id: 'settings',
          name: 'Platform Settings',
          href: '/dashboard/settings',
          icon: <Settings className="w-4 h-4" />,
          active: pathname === '/dashboard/settings',
          show: effectivePermissions.canAccessSettings
        }
      ]
    }
  ];

  const renderNavigationItem = (item: NavigationItem, depth = 0) => {
    const hasSubItems = item.subItems && item.subItems.length > 0;
    const isExpanded = expandedSections.includes(item.id);
    const paddingClass = depth === 0 ? 'pl-3' : 'pl-8';

    const itemContent = (
      <div className={`flex items-center gap-3 flex-1 ${isCollapsed ? 'justify-center' : ''}`}>
        <div className="flex-shrink-0">{item.icon}</div>
        {!isCollapsed && (
          <span className="font-medium text-sm truncate">
            {item.name}
          </span>
        )}
        {!isCollapsed && item.badge && (
          <span className="px-1.5 py-0.5 text-[10px] rounded-full font-bold bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300">
            {item.badge}
          </span>
        )}
      </div>
    );

    const commonClasses = `flex items-center gap-3 w-full px-3 py-2.5 rounded-xl transition-all duration-200 ${item.active
      ? 'bg-blue-600 text-white shadow-md shadow-blue-200 dark:shadow-none'
      : 'text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800'
      } ${paddingClass} ${isCollapsed ? 'justify-center px-2' : ''}`;

    if (isCollapsed && hasSubItems && depth === 0) {
      return (
        <div key={item.id} className="mb-1">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className={commonClasses} title={item.name}>
                <div className="flex-shrink-0">{item.icon}</div>
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent side="right" align="start" className="w-48 ml-2">
              <div className="px-2 py-1.5 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                {item.name}
              </div>
              <DropdownMenuSeparator />
              {item.subItems?.filter(subItem => subItem.show !== false).map(subItem => (
                <DropdownMenuItem key={subItem.id} onClick={() => onNavigate?.(subItem.href)} className="cursor-pointer">
                  <Link href={subItem.href} className="flex items-center gap-2 w-full">
                    {subItem.icon}
                    <span>{subItem.name}</span>
                  </Link>
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      );
    }

    return (
      <div key={item.id} className="mb-1">
        <div className="flex items-center">
          {hasSubItems ? (
            <button
              onClick={() => toggleSection(item.id)}
              className={commonClasses}
              title={isCollapsed ? item.name : undefined}
            >
              {itemContent}
              {!isCollapsed && (
                <div className="flex-shrink-0">
                  {isExpanded ? <ChevronDown className="w-4 h-4 opacity-50" /> : <ChevronRight className="w-4 h-4 opacity-50" />}
                </div>
              )}
            </button>
          ) : (
            <Link
              href={item.href}
              onClick={() => onNavigate?.(item.href)}
              className={commonClasses}
              title={isCollapsed ? item.name : undefined}
            >
              {itemContent}
            </Link>
          )}
        </div>

        {hasSubItems && isExpanded && !isCollapsed && (
          <div className="mt-1 space-y-1">
            {item.subItems?.map(subItem => renderNavigationItem(subItem, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  return (
    <nav className="space-y-1 px-2">
      {navigationItems.filter(item => item.show !== false).map(item => renderNavigationItem(item))}
    </nav>
  );
};

export default ComprehensiveNavigation;