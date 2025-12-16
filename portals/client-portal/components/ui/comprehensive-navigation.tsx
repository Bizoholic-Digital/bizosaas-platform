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
  CheckSquare, ListChecks, FolderKanban
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
}

const ComprehensiveNavigation: React.FC<NavigationProps> = ({ onNavigate }) => {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [expandedSections, setExpandedSections] = useState<string[]>(['dashboard']);
  const { metrics } = useSystemStatus();
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin' || user?.role === 'super_admin';

  // Auto-expand sections based on current path
  useEffect(() => {
    const pathSections = pathname.split('/').filter(Boolean);
    const newExpanded = ['dashboard']; // Always keep dashboard

    if (pathname.startsWith('/crm')) newExpanded.push('crm');
    if (pathname.startsWith('/content')) newExpanded.push('content');
    if (pathname.startsWith('/ecommerce')) newExpanded.push('ecommerce');
    if (pathname.startsWith('/directory')) newExpanded.push('directory');
    if (pathname.startsWith('/analytics')) newExpanded.push('analytics');
    if (pathname.startsWith('/users')) newExpanded.push('users');
    if (pathname.startsWith('/settings')) newExpanded.push('settings');

    setExpandedSections(newExpanded);
  }, [pathname]);

  // Debug logging
  useEffect(() => {
    console.log('ComprehensiveNavigation rendered:', { pathname, expandedSections, metrics });
  }, [pathname, expandedSections, metrics]);

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
      name: 'Dashboard',
      href: '/dashboard',
      icon: <Home className="w-5 h-5" />,
      active: pathname === '/dashboard' || pathname === '/'
    },
    {
      id: 'connectors',
      name: 'Connectors',
      href: '/dashboard/connectors',
      icon: <Zap className="w-5 h-5" />,
      active: pathname.startsWith('/dashboard/connectors')
    },
    {
      id: 'crm',
      name: 'CRM Management',
      href: '/crm',
      icon: <Users className="w-5 h-5" />,
      active: pathname.startsWith('/crm'),
      subItems: [
        {
          id: 'crm-contacts',
          name: 'Contacts',
          href: '/crm/contacts',
          icon: <Users className="w-4 h-4" />,
          active: pathname === '/crm/contacts'
        },
        {
          id: 'crm-campaigns',
          name: 'Campaigns',
          href: '/crm/campaigns',
          icon: <Target className="w-4 h-4" />,
          active: pathname === '/crm/campaigns'
        },
        {
          id: 'crm-reports',
          name: 'Reports',
          href: '/crm/reports',
          icon: <BarChart3 className="w-4 h-4" />,
          active: pathname === '/crm/reports'
        }
      ]
    },
    {
      id: 'content',
      name: 'Content Management',
      href: '/content',
      icon: <FileText className="w-5 h-5" />,
      active: pathname.startsWith('/content'),
      subItems: [
        {
          id: 'content-pages',
          name: 'Pages',
          href: '/content/pages',
          icon: <FileText className="w-4 h-4" />,
          active: pathname === '/content/pages'
        },
        {
          id: 'content-blog',
          name: 'Blog Posts',
          href: '/content/blog',
          icon: <Newspaper className="w-4 h-4" />,
          active: pathname === '/content/blog'
        },
        {
          id: 'content-forms',
          name: 'Forms',
          href: '/content/forms',
          icon: <MessageSquare className="w-4 h-4" />,
          active: pathname === '/content/forms'
        }
      ]
    },
    {
      id: 'ecommerce',
      name: 'E-commerce',
      href: '/ecommerce',
      icon: <ShoppingCart className="w-5 h-5" />,
      active: pathname.startsWith('/ecommerce')
    },
    {
      id: 'tools',
      name: 'Tools',
      href: '/dashboard/tools',
      icon: <Bot className="w-5 h-5" />,
      active: pathname.startsWith('/dashboard/tools')
    },
    {
      id: 'settings',
      name: 'Settings',
      href: '/settings',
      icon: <Settings className="w-5 h-5" />,
      active: pathname.startsWith('/settings')
    },
    {
      id: 'analytics',
      name: 'Analytics',
      href: '/analytics',
      icon: <BarChart3 className="w-5 h-5" />,
      active: pathname.startsWith('/analytics')
    },
    {
      id: 'ai-agents',
      name: 'AI Agents',
      href: '/ai-agents',
      icon: <Brain className="w-5 h-5" />,
      badge: '93',
      active: pathname.startsWith('/ai-agents'),
      show: isAdmin
    },
    {
      id: 'tasks',
      name: 'Tasks & Projects',
      href: '/tasks',
      icon: <CheckSquare className="w-5 h-5" />,
      active: pathname.startsWith('/tasks'),
      subItems: [
        {
          id: 'tasks-my-tasks',
          name: 'My Tasks',
          href: '/tasks/my-tasks',
          icon: <ListChecks className="w-4 h-4" />,
          active: pathname === '/tasks/my-tasks'
        },
        {
          id: 'tasks-projects',
          name: 'Projects',
          href: '/tasks/projects',
          icon: <FolderKanban className="w-4 h-4" />,
          active: pathname === '/tasks/projects'
        },
        {
          id: 'tasks-calendar',
          name: 'Calendar',
          href: '/tasks/calendar',
          icon: <Calendar className="w-4 h-4" />,
          active: pathname === '/tasks/calendar'
        }
      ]
    }
  ];

  const renderNavigationItem = (item: NavigationItem, depth = 0) => {
    const hasSubItems = item.subItems && item.subItems.length > 0;
    const isExpanded = expandedSections.includes(item.id);
    const paddingClass = depth === 0 ? 'pl-3' : 'pl-8';

    return (
      <div key={item.id} className="mb-1">
        <div className="flex items-center">
          {hasSubItems ? (
            <button
              onClick={() => toggleSection(item.id)}
              className={`flex items-center gap-3 w-full px-3 py-2 rounded-lg transition-colors ${item.active
                ? 'bg-blue-50 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
                : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                } ${paddingClass}`}
            >
              <div className="flex items-center gap-3 flex-1">
                {item.icon}
                <span className="font-medium">{item.name}</span>
                {item.badge && (
                  <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${item.badge === '!'
                    ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                    : item.badge === 'NEW'
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
                      : item.badge === 'HOT'
                        ? 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300'
                        : item.badge === 'DUE'
                          ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
                          : item.badge === 'AI'
                            ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300'
                            : /^\d+%$/.test(item.badge)
                              ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300'
                              : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
                    }`}>
                    {item.badge}
                  </span>
                )}
              </div>
              {isExpanded ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )}
            </button>
          ) : (
            <Link
              href={item.href}
              onClick={() => onNavigate?.(item.href)}
              className={`flex items-center gap-3 w-full px-3 py-2 rounded-lg transition-colors ${item.active
                ? 'bg-blue-50 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
                : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                } ${paddingClass}`}
            >
              <div className="flex items-center gap-3 flex-1">
                {item.icon}
                <span className="font-medium">{item.name}</span>
                {item.badge && (
                  <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${item.badge === '!'
                    ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                    : item.badge === 'NEW'
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
                      : item.badge === 'HOT'
                        ? 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300'
                        : item.badge === 'DUE'
                          ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
                          : item.badge === 'AI'
                            ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300'
                            : /^\d+%$/.test(item.badge)
                              ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300'
                              : /^\d+(\.\d+)?[KMB]?$/.test(item.badge)
                                ? 'bg-cyan-100 text-cyan-800 dark:bg-cyan-900 dark:text-cyan-300'
                                : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
                    }`}>
                    {item.badge}
                  </span>
                )}
              </div>
              <ChevronRight className="w-4 h-4 text-gray-400" />
            </Link>
          )}
        </div>

        {hasSubItems && isExpanded && (
          <div className="mt-1 space-y-1">
            {item.subItems?.map(subItem => renderNavigationItem(subItem, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  return (
    <nav className="space-y-2">
      {navigationItems.filter(item => item.show !== false).map(item => renderNavigationItem(item))}
    </nav>
  );
};

export default ComprehensiveNavigation;