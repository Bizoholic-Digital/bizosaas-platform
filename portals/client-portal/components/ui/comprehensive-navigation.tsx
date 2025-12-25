'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useSearchParams } from 'next/navigation';
import { useSystemStatus } from '../../lib/hooks/useSystemStatus';
import {
  Home, Users, FileText, ShoppingCart, Building2, BarChart3,
  Settings, User, Brain, Zap, Target, TrendingUp, Database,
  Globe, Search, MessageSquare, Phone, Mail, Calendar,
  Package, CreditCard, UserCheck, Shield, Bell, Download,
  BookOpen, Image, Video, Newspaper, Tag, Filter,
  PieChart, Activity, LineChart, TrendingDown, AlertCircle,
  ChevronDown, ChevronRight, Menu, X, RefreshCw, Bot,
  CheckSquare, ListChecks, FolderKanban, Sparkles
} from 'lucide-react';
import { useAuth } from '@/components/auth/AuthProvider';

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
  const [expandedSections, setExpandedSections] = useState<string[]>(['dashboard']);
  const { metrics } = useSystemStatus();
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin' || user?.role === 'super_admin';

  // Auto-expand sections based on current path
  useEffect(() => {
    const pathSections = pathname.split('/').filter(Boolean);
    const newExpanded = ['dashboard'];

    if (pathname.startsWith('/crm')) newExpanded.push('crm');
    if (pathname.startsWith('/content')) newExpanded.push('content');
    if (pathname.startsWith('/ecommerce')) newExpanded.push('ecommerce');
    if (pathname.startsWith('/directory')) newExpanded.push('directory');
    if (pathname.startsWith('/analytics')) newExpanded.push('analytics');
    if (pathname.startsWith('/users')) newExpanded.push('users');
    if (pathname.startsWith('/settings')) newExpanded.push('settings');

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
      id: 'dashboard',
      name: isCollapsed ? 'Home' : 'Business Overview',
      href: '/dashboard',
      icon: <Home className="w-5 h-5" />,
      active: pathname === '/dashboard' || pathname === '/'
    },
    {
      id: 'ai-assistant',
      name: isCollapsed ? 'AI' : 'AI Assistant',
      href: '/dashboard/ai-assistant',
      icon: <Sparkles className="w-5 h-5 text-indigo-500" />,
      badge: isCollapsed ? undefined : 'AI',
      active: pathname === '/dashboard/ai-assistant'
    },
    {
      id: 'agent-studio',
      name: isCollapsed ? 'Studio' : 'Agent Studio',
      href: '/ai-agents',
      icon: <Bot className="w-5 h-5" />,
      badge: isCollapsed ? undefined : 'NEW',
      active: pathname.startsWith('/ai-agents')
    },
    {
      id: 'crm',
      name: isCollapsed ? 'CRM' : 'CRM & Growth',
      href: '/crm',
      icon: <Users className="w-5 h-5" />,
      active: pathname.startsWith('/crm'),
      subItems: [
        {
          id: 'crm-contacts',
          name: 'Lead Management',
          href: '/crm/contacts',
          icon: <Users className="w-4 h-4" />,
          active: pathname === '/crm/contacts'
        },
        {
          id: 'crm-campaigns',
          name: 'Marketing Campaigns',
          href: '/crm/campaigns',
          icon: <Target className="w-4 h-4" />,
          active: pathname === '/crm/campaigns'
        },
        {
          id: 'crm-reports',
          name: 'Performance Reports',
          href: '/crm/reports',
          icon: <BarChart3 className="w-4 h-4" />,
          active: pathname === '/crm/reports'
        }
      ]
    },
    {
      id: 'content',
      name: isCollapsed ? 'Content' : 'Content & CMS',
      href: '/content',
      icon: <FileText className="w-5 h-5" />,
      active: pathname.startsWith('/content'),
    },
    {
      id: 'ecommerce',
      name: isCollapsed ? 'Shop' : 'E-commerce Shop',
      href: '/ecommerce',
      icon: <ShoppingCart className="w-5 h-5" />,
      active: pathname.startsWith('/ecommerce')
    },
    {
      id: 'analytics',
      name: isCollapsed ? 'Stats' : 'Business Intelligence',
      href: '/analytics',
      icon: <BarChart3 className="w-5 h-5" />,
      active: pathname.startsWith('/analytics')
    },
    {
      id: 'tasks',
      name: isCollapsed ? 'Tasks' : 'Projects & Tasks',
      href: '/tasks',
      icon: <CheckSquare className="w-5 h-5" />,
      active: pathname.startsWith('/tasks'),
    },
    {
      id: 'connectors',
      name: isCollapsed ? 'Connect' : 'Connectors',
      href: '/dashboard/connectors',
      icon: <RefreshCw className="w-5 h-5 text-emerald-500" />,
      active: pathname === '/dashboard/connectors'
    },
    {
      id: 'settings',
      name: isCollapsed ? 'Settings' : 'Portal Settings',
      href: '/settings',
      icon: <Settings className="w-5 h-5" />,
      active: pathname.startsWith('/settings')
    },
    {
      id: 'admin-dash',
      name: isCollapsed ? 'Admin' : 'Platform Admin',
      href: 'https://admin.bizoholic.net',
      icon: <Shield className="w-5 h-5 text-amber-500" />,
      active: false,
      show: isAdmin
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