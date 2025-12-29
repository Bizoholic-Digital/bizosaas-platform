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
  CheckSquare, ListChecks, FolderKanban, Sparkles, Layers
} from 'lucide-react';
import { useAuth as useClerkAuth } from '@clerk/nextjs';
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
    const newExpanded = ['workspace'];

    if (pathname.startsWith('/crm') || pathname.startsWith('/content') || pathname.startsWith('/ecommerce') || pathname.startsWith('/directory')) {
      newExpanded.push('business-suite');
    }
    if (pathname.startsWith('/ai-agents') || pathname.startsWith('/analytics')) {
      newExpanded.push('automation');
    }
    if (pathname.startsWith('/tasks') || pathname.includes('/connectors')) {
      newExpanded.push('operations');
    }
    if (pathname.startsWith('/settings')) {
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

  /* Dynamic Sidebar Logic */
  const { getToken } = useClerkAuth();
  const [installedMcps, setInstalledMcps] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchInstalled = async () => {
      try {
        const { brainApi } = await import('../../lib/brain-api');
        const token = await getToken();
        const data = await brainApi.mcp.getInstalled(token || undefined);
        if (Array.isArray(data)) {
          setInstalledMcps(data);
        } else {
          console.warn('getInstalled returned non-array:', data);
          setInstalledMcps([]);
        }
      } catch (err) {
        console.error('Failed to fetch installed MCPs:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchInstalled();
  }, [getToken]);

  const hasCategory = (catSlug: string) => {
    if (loading || !Array.isArray(installedMcps)) return true; // optimistic
    return installedMcps.some(inst => inst?.mcp?.category === catSlug);
  };

  const getLink = (catSlug: string, defaultHref: string) => {
    return hasCategory(catSlug) ? defaultHref : `/dashboard/connectors?category=${catSlug}`;
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
          name: 'Business Overview',
          href: '/dashboard',
          icon: <Home className="w-4 h-4" />,
          active: pathname === '/dashboard' || pathname === '/'
        },
        {
          id: 'ai-assistant',
          name: 'AI Assistant',
          href: '/dashboard/ai-assistant',
          icon: <Sparkles className="w-4 h-4 text-indigo-500" />,
          badge: isCollapsed ? undefined : 'AI',
          active: pathname === '/dashboard/ai-assistant'
        }
      ]
    },
    {
      id: 'business-suite',
      name: isCollapsed ? 'Suite' : 'Business Suite',
      href: '#',
      icon: <Layers className="w-5 h-5 text-gray-500" />,
      subItems: [
        {
          id: 'crm',
          name: 'CRM & Contacts',
          href: '/dashboard/crm',
          icon: <Users className="w-4 h-4" />,
          active: pathname.startsWith('/dashboard/crm'),
        },
        {
          id: 'cms',
          name: 'Content & CMS',
          href: '/dashboard/cms',
          icon: <FileText className="w-4 h-4" />,
          active: pathname.startsWith('/dashboard/cms'),
        },
        {
          id: 'ecommerce',
          name: 'E-commerce',
          href: '/dashboard/ecommerce',
          icon: <ShoppingCart className="w-4 h-4" />,
          active: pathname.startsWith('/dashboard/ecommerce')
        },
        {
          id: 'marketing',
          name: 'Marketing',
          href: '/dashboard/marketing',
          icon: <Mail className="w-4 h-4" />,
          active: pathname.startsWith('/dashboard/marketing')
        }
      ]
    },
    {
      id: 'automation',
      name: isCollapsed ? 'Auto' : 'Automation & Intel',
      href: '#',
      icon: <Zap className="w-5 h-5 text-gray-500" />,
      subItems: [
        {
          id: 'agent-studio',
          name: 'Agent Studio',
          href: '/dashboard/ai-agents',
          icon: <Bot className="w-4 h-4" />,
          badge: isCollapsed ? undefined : 'NEW',
          active: pathname.startsWith('/ai-agents')
        },
        {
          id: 'analytics',
          name: 'Business Intelligence',
          href: getLink('analytics', '/analytics'),
          icon: <BarChart3 className={`w-4 h-4 ${hasCategory('analytics') ? '' : 'text-gray-400'}`} />,
          active: pathname.startsWith('/analytics')
        }
      ]
    },
    {
      id: 'operations',
      name: isCollapsed ? 'Ops' : 'Operations',
      href: '#',
      icon: <Activity className="w-5 h-5 text-gray-500" />,
      subItems: [
        {
          id: 'tasks',
          name: 'Projects & Tasks',
          href: '/tasks',
          icon: <CheckSquare className="w-4 h-4" />,
          active: pathname.startsWith('/tasks'),
        },
        {
          id: 'connectors',
          name: 'Connectivity Hub',
          href: '/dashboard/connectors',
          icon: <RefreshCw className="w-4 h-4 text-emerald-500" />,
          active: pathname === '/dashboard/connectors'
        }
      ]
    },
    {
      id: 'platform',
      name: isCollapsed ? 'System' : 'Settings & Admin',
      href: '#',
      icon: <Settings className="w-5 h-5 text-gray-500" />,
      subItems: [
        {
          id: 'settings',
          name: 'Portal Settings',
          href: '/settings',
          icon: <Settings className="w-4 h-4" />,
          active: pathname.startsWith('/settings')
        },
        {
          id: 'admin-dash',
          name: 'Platform Admin',
          href: 'https://admin.bizoholic.net',
          icon: <Shield className="w-4 h-4 text-amber-500" />,
          active: false,
          show: isAdmin
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