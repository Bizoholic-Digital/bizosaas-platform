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
  ChevronDown, ChevronRight, Menu, X, RefreshCw, Bot
} from 'lucide-react';

interface NavigationItem {
  id: string;
  name: string;
  href: string;
  icon: React.ReactNode;
  badge?: string;
  active?: boolean;
  subItems?: NavigationItem[];
}

interface NavigationProps {
  onNavigate?: (path: string) => void;
}

const ComprehensiveNavigation: React.FC<NavigationProps> = ({ onNavigate }) => {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [expandedSections, setExpandedSections] = useState<string[]>(['dashboard']);
  const { metrics } = useSystemStatus();

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
      href: '/?tab=dashboard',
      icon: <Home className="w-5 h-5" />,
      badge: 'NEW',
      active: pathname === '/' && (!searchParams?.get('tab') || searchParams?.get('tab') === 'dashboard')
    },
    {
      id: 'leads',
      name: 'Leads',
      href: '/?tab=leads',
      icon: <Target className="w-5 h-5" />,
      badge: metrics.leads > 0 ? metrics.leads.toString() : '47',
      active: searchParams?.get('tab') === 'leads'
    },
    {
      id: 'orders',
      name: 'Orders',
      href: '/?tab=orders',
      icon: <ShoppingCart className="w-5 h-5" />,
      badge: metrics.orders > 0 ? metrics.orders.toString() : '12',
      active: searchParams?.get('tab') === 'orders'
    },
    {
      id: 'crm',
      name: 'CRM Management',
      href: '/?tab=crm',
      icon: <Users className="w-5 h-5" />,
      badge: '!',
      active: searchParams?.get('tab') === 'crm',
      subItems: [
        {
          id: 'crm-leads',
          name: 'Leads',
          href: '/?tab=crm-leads',
          icon: <Target className="w-4 h-4" />,
          badge: '47',
          active: searchParams?.get('tab') === 'crm-leads'
        },
        {
          id: 'crm-contacts',
          name: 'Contacts',
          href: '/?tab=crm-contacts',
          icon: <Users className="w-4 h-4" />,
          badge: '234',
          active: searchParams?.get('tab') === 'crm-contacts'
        },
        {
          id: 'crm-campaigns',
          name: 'Campaigns',
          href: '/?tab=crm-campaigns',
          icon: <Zap className="w-4 h-4" />,
          badge: '8',
          active: searchParams?.get('tab') === 'crm-campaigns'
        },
        {
          id: 'crm-reports',
          name: 'Reports',
          href: '/?tab=crm-reports',
          icon: <BarChart3 className="w-4 h-4" />,
          badge: 'NEW',
          active: searchParams?.get('tab') === 'crm-reports'
        }
      ]
    },
    {
      id: 'content',
      name: 'Content Management',
      href: '/?tab=cms',
      icon: <FileText className="w-5 h-5" />,
      badge: '!',
      active: searchParams?.get('tab') === 'cms',
      subItems: [
        {
          id: 'content-pages',
          name: 'Pages',
          href: '/?tab=cms-pages',
          icon: <FileText className="w-4 h-4" />,
          badge: '24',
          active: searchParams?.get('tab') === 'cms-pages'
        },
        {
          id: 'content-blog',
          name: 'Blog Posts',
          href: '/?tab=cms-posts',
          icon: <Newspaper className="w-4 h-4" />,
          badge: '15',
          active: searchParams?.get('tab') === 'cms-posts'
        },
        {
          id: 'content-media',
          name: 'Media',
          href: '/?tab=cms-media',
          icon: <Image className="w-4 h-4" />,
          badge: '156',
          active: searchParams?.get('tab') === 'cms-media'
        },
        {
          id: 'content-forms',
          name: 'Forms',
          href: '/?tab=cms-forms',
          icon: <MessageSquare className="w-4 h-4" />,
          badge: '!',
          active: searchParams?.get('tab') === 'cms-forms'
        }
      ]
    },
    {
      id: 'ecommerce',
      name: 'E-commerce',
      href: '/?tab=ecommerce',
      icon: <ShoppingCart className="w-5 h-5" />,
      badge: '7',
      active: searchParams?.get('tab') === 'ecommerce',
      subItems: [
        {
          id: 'ecommerce-products',
          name: 'Products',
          href: '/?tab=ecom-products',
          icon: <Package className="w-4 h-4" />,
          badge: '89',
          active: searchParams?.get('tab') === 'ecom-products'
        },
        {
          id: 'ecommerce-orders',
          name: 'Orders',
          href: '/?tab=ecom-orders',
          icon: <ShoppingCart className="w-4 h-4" />,
          badge: '12',
          active: searchParams?.get('tab') === 'ecom-orders'
        },
        {
          id: 'ecommerce-customers',
          name: 'Customers',
          href: '/?tab=ecom-customers',
          icon: <Users className="w-4 h-4" />,
          badge: '234',
          active: searchParams?.get('tab') === 'ecom-customers'
        },
        {
          id: 'ecommerce-inventory',
          name: 'Inventory',
          href: '/?tab=ecom-inventory',
          icon: <Database className="w-4 h-4" />,
          badge: '!',
          active: searchParams?.get('tab') === 'ecom-inventory'
        }
      ]
    },
    {
      id: 'directory',
      name: 'Business Directory',
      href: '/?tab=directory',
      icon: <Building2 className="w-5 h-5" />,
      badge: 'NEW',
      active: searchParams?.get('tab') === 'directory',
      subItems: [
        {
          id: 'directory-businesses',
          name: 'Businesses',
          href: '/?tab=directory-businesses',
          icon: <Building2 className="w-4 h-4" />,
          badge: '142',
          active: searchParams?.get('tab') === 'directory-businesses'
        },
        {
          id: 'directory-categories',
          name: 'Categories',
          href: '/?tab=directory-categories',
          icon: <Tag className="w-4 h-4" />,
          badge: '28',
          active: searchParams?.get('tab') === 'directory-categories'
        },
        {
          id: 'directory-reviews',
          name: 'Reviews',
          href: '/?tab=directory-reviews',
          icon: <MessageSquare className="w-4 h-4" />,
          badge: '56',
          active: searchParams?.get('tab') === 'directory-reviews'
        },
        {
          id: 'directory-analytics',
          name: 'Directory Analytics',
          href: '/?tab=directory-analytics',
          icon: <TrendingUp className="w-4 h-4" />,
          badge: 'HOT',
          active: searchParams?.get('tab') === 'directory-analytics'
        }
      ]
    },
    {
      id: 'analytics',
      name: 'Analytics & Insights',
      href: '/?tab=analytics',
      icon: <BarChart3 className="w-5 h-5" />,
      badge: 'HOT',
      active: searchParams?.get('tab') === 'analytics',
      subItems: [
        {
          id: 'analytics-performance',
          name: 'Performance',
          href: '/?tab=analytics-performance',
          icon: <TrendingUp className="w-4 h-4" />,
          badge: '95%',
          active: searchParams?.get('tab') === 'analytics-performance'
        },
        {
          id: 'analytics-traffic',
          name: 'Traffic',
          href: '/?tab=analytics-traffic',
          icon: <Activity className="w-4 h-4" />,
          badge: '2.3K',
          active: searchParams?.get('tab') === 'analytics-traffic'
        },
        {
          id: 'analytics-conversions',
          name: 'Conversions',
          href: '/?tab=analytics-conversions',
          icon: <Target className="w-4 h-4" />,
          badge: '!',
          active: searchParams?.get('tab') === 'analytics-conversions'
        },
        {
          id: 'analytics-reports',
          name: 'Reports',
          href: '/?tab=analytics-reports',
          icon: <FileText className="w-4 h-4" />,
          badge: '18',
          active: searchParams?.get('tab') === 'analytics-reports'
        },
        {
          id: 'analytics-ai-insights',
          name: 'AI Insights',
          href: '/?tab=analytics-ai-insights',
          icon: <Brain className="w-4 h-4" />,
          badge: 'AI',
          active: searchParams?.get('tab') === 'analytics-ai-insights'
        }
      ]
    },
    {
      id: 'users',
      name: 'User Management',
      href: '/?tab=users',
      icon: <UserCheck className="w-5 h-5" />,
      badge: '3',
      active: searchParams?.get('tab') === 'users',
      subItems: [
        {
          id: 'users-roles',
          name: 'Roles',
          href: '/?tab=users-roles',
          icon: <Shield className="w-4 h-4" />,
          badge: '7',
          active: searchParams?.get('tab') === 'users-roles'
        },
        {
          id: 'users-permissions',
          name: 'Permissions',
          href: '/?tab=users-permissions',
          icon: <UserCheck className="w-4 h-4" />,
          badge: 'NEW',
          active: searchParams?.get('tab') === 'users-permissions'
        },
        {
          id: 'users-activity',
          name: 'Activity',
          href: '/?tab=users-activity',
          icon: <Activity className="w-4 h-4" />,
          badge: '24',
          active: searchParams?.get('tab') === 'users-activity'
        }
      ]
    },
    {
      id: 'chat',
      name: 'AI Assistant',
      href: '/chat',
      icon: <Bot className="w-5 h-5" />,
      badge: 'AI',
      active: pathname === '/chat'
    },
    {
      id: 'settings',
      name: 'System Settings',
      href: '/?tab=settings',
      icon: <Settings className="w-5 h-5" />,
      badge: '!',
      active: searchParams?.get('tab') === 'settings',
      subItems: [
        {
          id: 'settings-integrations',
          name: 'Integrations',
          href: '/?tab=settings-integrations',
          icon: <Globe className="w-4 h-4" />,
          badge: '!',
          active: searchParams?.get('tab') === 'settings-integrations'
        },
        {
          id: 'settings-billing',
          name: 'Billing',
          href: '/?tab=settings-billing',
          icon: <CreditCard className="w-4 h-4" />,
          badge: 'DUE',
          active: searchParams?.get('tab') === 'settings-billing'
        },
        {
          id: 'settings-security',
          name: 'Security',
          href: '/?tab=settings-security',
          icon: <Shield className="w-4 h-4" />,
          badge: '!',
          active: searchParams?.get('tab') === 'settings-security'
        },
        {
          id: 'settings-notifications',
          name: 'Notifications',
          href: '/?tab=settings-notifications',
          icon: <Bell className="w-4 h-4" />,
          badge: '15',
          active: searchParams?.get('tab') === 'settings-notifications'
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
      {navigationItems.map(item => renderNavigationItem(item))}
    </nav>
  );
};

export default ComprehensiveNavigation;