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

  // Auto-expand sections based on current path
  useEffect(() => {
    const newExpanded = ['workspace'];

    if (pathname.includes('/tenants') || pathname.includes('/users')) {
      newExpanded.push('management');
    }
    if (pathname.includes('/status') || pathname.includes('/connectors')) {
      newExpanded.push('connectivity');
    }
    if (pathname.includes('/security') || pathname.includes('/settings')) {
      newExpanded.push('platform');
    }

    setExpandedSections(newExpanded);
  }, [pathname]);

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev =>
      prev.includes(sectionId)
        ? prev.filter(id => id !== sectionId)
        : [...prev, sectionId]
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
          active: pathname === '/dashboard/tenants'
        },
        {
          id: 'user-management',
          name: 'Global Users',
          href: '/dashboard/users',
          icon: <Users className="w-4 h-4" />,
          active: pathname === '/dashboard/users'
        },
        {
          id: 'plugin-analytics',
          name: 'Marketplace Demand',
          href: '/dashboard/plugin-analytics',
          icon: <BarChart3 className="w-4 h-4 text-emerald-500" />,
          badge: isCollapsed ? undefined : 'GROWTH',
          active: pathname === '/dashboard/plugin-analytics'
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
          active: pathname === '/dashboard/system-status'
        },
        {
          id: 'connectivity-hub',
          name: 'Connectivity Hub',
          href: '/dashboard/connectors',
          icon: <RefreshCw className="w-4 h-4 text-emerald-500" />,
          active: pathname === '/dashboard/connectors'
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
          active: pathname === '/dashboard/security'
        },
        {
          id: 'settings',
          name: 'Platform Settings',
          href: '/dashboard/settings',
          icon: <Settings className="w-4 h-4" />,
          active: pathname === '/dashboard/settings'
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