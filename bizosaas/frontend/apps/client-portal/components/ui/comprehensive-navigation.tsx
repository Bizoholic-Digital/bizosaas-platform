'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
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
      href: '/',
      icon: <Home className="w-5 h-5" />,
      badge: 'NEW',
      active: pathname === '/'
    },
    {
      id: 'leads',
      name: 'Leads',
      href: '/leads',
      icon: <Target className="w-5 h-5" />,
      badge: metrics.leads > 0 ? metrics.leads.toString() : '47',
      active: pathname === '/leads'
    },
    {
      id: 'orders',
      name: 'Orders',
      href: '/orders',
      icon: <ShoppingCart className="w-5 h-5" />,
      badge: metrics.orders > 0 ? metrics.orders.toString() : '12',
      active: pathname === '/orders'
    },
    {
      id: 'crm',
      name: 'CRM Management',
      href: '/crm',
      icon: <Users className="w-5 h-5" />,
      badge: '!',
      active: pathname.startsWith('/crm'),
      subItems: [
        {
          id: 'crm-leads',
          name: 'Leads',
          href: '/leads',
          icon: <Target className="w-4 h-4" />,
          badge: '47',
          active: pathname === '/leads'
        },
        {
          id: 'crm-contacts',
          name: 'Contacts',
          href: '/crm/contacts', 
          icon: <Users className="w-4 h-4" />,
          badge: '234',
          active: pathname === '/crm/contacts'
        },
        {
          id: 'crm-campaigns',
          name: 'Campaigns',
          href: '/crm/campaigns',
          icon: <Zap className="w-4 h-4" />,
          badge: '8',
          active: pathname === '/crm/campaigns'
        },
        {
          id: 'crm-reports',
          name: 'Reports',
          href: '/crm/reports',
          icon: <BarChart3 className="w-4 h-4" />,
          badge: 'NEW',
          active: pathname === '/crm/reports'
        }
      ]
    },
    {
      id: 'content',
      name: 'Content Management',
      href: '/content',
      icon: <FileText className="w-5 h-5" />,
      badge: '!',
      active: pathname.startsWith('/content'),
      subItems: [
        {
          id: 'content-pages',
          name: 'Pages',
          href: '/content/pages',
          icon: <FileText className="w-4 h-4" />,
          badge: '24',
          active: pathname === '/content/pages'
        },
        {
          id: 'content-blog',
          name: 'Blog Posts',
          href: '/content/blog',
          icon: <Newspaper className="w-4 h-4" />,
          badge: '15',
          active: pathname === '/content/blog'
        },
        {
          id: 'content-media',
          name: 'Media',
          href: '/content/media',
          icon: <Image className="w-4 h-4" />,
          badge: '156',
          active: pathname === '/content/media'
        },
        {
          id: 'content-forms',
          name: 'Forms',
          href: '/content/forms',
          icon: <MessageSquare className="w-4 h-4" />,
          badge: '!',
          active: pathname === '/content/forms'
        }
      ]
    },
    {
      id: 'ecommerce',
      name: 'E-commerce',
      href: '/ecommerce',
      icon: <ShoppingCart className="w-5 h-5" />,
      badge: '7',
      active: pathname.startsWith('/ecommerce'),
      subItems: [
        {
          id: 'ecommerce-products',
          name: 'Products',
          href: '/ecommerce/products',
          icon: <Package className="w-4 h-4" />,
          badge: '89',
          active: pathname === '/ecommerce/products'
        },
        {
          id: 'ecommerce-orders',
          name: 'Orders',
          href: '/orders',
          icon: <ShoppingCart className="w-4 h-4" />,
          badge: '12',
          active: pathname === '/orders'
        },
        {
          id: 'ecommerce-customers',
          name: 'Customers',
          href: '/ecommerce/customers',
          icon: <Users className="w-4 h-4" />,
          badge: '234',
          active: pathname === '/ecommerce/customers'
        },
        {
          id: 'ecommerce-inventory',
          name: 'Inventory',
          href: '/ecommerce/inventory',
          icon: <Database className="w-4 h-4" />,
          badge: '!',
          active: pathname === '/ecommerce/inventory'
        }
      ]
    },
    {
      id: 'directory',
      name: 'Business Directory',
      href: '/directory',
      icon: <Building2 className="w-5 h-5" />,
      badge: 'NEW',
      active: pathname.startsWith('/directory'),
      subItems: [
        {
          id: 'directory-businesses',
          name: 'Businesses',
          href: '/directory/businesses',
          icon: <Building2 className="w-4 h-4" />,
          badge: '142',
          active: pathname === '/directory/businesses'
        },
        {
          id: 'directory-categories',
          name: 'Categories',
          href: '/directory/categories',
          icon: <Tag className="w-4 h-4" />,
          badge: '28',
          active: pathname === '/directory/categories'
        },
        {
          id: 'directory-reviews',
          name: 'Reviews',
          href: '/directory/reviews',
          icon: <MessageSquare className="w-4 h-4" />,
          badge: '56',
          active: pathname === '/directory/reviews'
        },
        {
          id: 'directory-analytics',
          name: 'Directory Analytics',
          href: '/directory/analytics',
          icon: <TrendingUp className="w-4 h-4" />,
          badge: 'HOT',
          active: pathname === '/directory/analytics'
        }
      ]
    },
    {
      id: 'analytics',
      name: 'Analytics & Insights',
      href: '/analytics',
      icon: <BarChart3 className="w-5 h-5" />,
      badge: 'HOT',
      active: pathname.startsWith('/analytics'),
      subItems: [
        {
          id: 'analytics-performance',
          name: 'Performance',
          href: '/analytics/performance',
          icon: <TrendingUp className="w-4 h-4" />,
          badge: '95%',
          active: pathname === '/analytics/performance'
        },
        {
          id: 'analytics-traffic',
          name: 'Traffic',
          href: '/analytics/traffic',
          icon: <Activity className="w-4 h-4" />,
          badge: '2.3K',
          active: pathname === '/analytics/traffic'
        },
        {
          id: 'analytics-conversions',
          name: 'Conversions',
          href: '/analytics/conversions',
          icon: <Target className="w-4 h-4" />,
          badge: '!',
          active: pathname === '/analytics/conversions'
        },
        {
          id: 'analytics-reports',
          name: 'Reports',
          href: '/analytics/reports',
          icon: <FileText className="w-4 h-4" />,
          badge: '18',
          active: pathname === '/analytics/reports'
        },
        {
          id: 'analytics-ai-insights',
          name: 'AI Insights',
          href: '/analytics/ai-insights',
          icon: <Brain className="w-4 h-4" />,
          badge: 'AI',
          active: pathname === '/analytics/ai-insights'
        }
      ]
    },
    {
      id: 'users',
      name: 'User Management',
      href: '/users',
      icon: <UserCheck className="w-5 h-5" />,
      badge: '3',
      active: pathname.startsWith('/users'),
      subItems: [
        {
          id: 'users-roles',
          name: 'Roles',
          href: '/users/roles',
          icon: <Shield className="w-4 h-4" />,
          badge: '7',
          active: pathname === '/users/roles'
        },
        {
          id: 'users-permissions',
          name: 'Permissions',
          href: '/users/permissions',
          icon: <UserCheck className="w-4 h-4" />,
          badge: 'NEW',
          active: pathname === '/users/permissions'
        },
        {
          id: 'users-activity',
          name: 'Activity',
          href: '/users/activity',
          icon: <Activity className="w-4 h-4" />,
          badge: '24',
          active: pathname === '/users/activity'
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
      href: '/settings',
      icon: <Settings className="w-5 h-5" />,
      badge: '!',
      active: pathname.startsWith('/settings'),
      subItems: [
        {
          id: 'settings-integrations',
          name: 'Integrations',
          href: '/settings/integrations',
          icon: <Globe className="w-4 h-4" />,
          badge: '!',
          active: pathname === '/settings/integrations'
        },
        {
          id: 'settings-billing',
          name: 'Billing',
          href: '/settings/billing',
          icon: <CreditCard className="w-4 h-4" />,
          badge: 'DUE',
          active: pathname === '/settings/billing'
        },
        {
          id: 'settings-security',
          name: 'Security',
          href: '/settings/security',
          icon: <Shield className="w-4 h-4" />,
          badge: '!',
          active: pathname === '/settings/security'
        },
        {
          id: 'settings-notifications',
          name: 'Notifications',
          href: '/settings/notifications',
          icon: <Bell className="w-4 h-4" />,
          badge: '15',
          active: pathname === '/settings/notifications'
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
              className={`flex items-center gap-3 w-full px-3 py-2 rounded-lg transition-colors ${
                item.active
                  ? 'bg-blue-50 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
                  : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
              } ${paddingClass}`}
            >
              <div className="flex items-center gap-3 flex-1">
                {item.icon}
                <span className="font-medium">{item.name}</span>
                {item.badge && (
                  <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${
                    item.badge === '!' 
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
              className={`flex items-center gap-3 w-full px-3 py-2 rounded-lg transition-colors ${
                item.active
                  ? 'bg-blue-50 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
                  : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
              } ${paddingClass}`}
            >
              <div className="flex items-center gap-3 flex-1">
                {item.icon}
                <span className="font-medium">{item.name}</span>
                {item.badge && (
                  <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${
                    item.badge === '!' 
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