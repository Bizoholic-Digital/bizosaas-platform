'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useSearchParams } from 'next/navigation';
import { useSystemStatus } from '../../lib/hooks/useSystemStatus';
import {
  Home, Users,
  LifeBuoy,
  FileText, ShoppingCart, Building2, BarChart3,
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
  const [expandedSections, setExpandedSections] = useState<string[]>(['dashboard']);
  const { metrics } = useSystemStatus();
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin' || user?.role === 'super_admin';

  // Auto-expand sections based on current path
  useEffect(() => {
    let activeSection = 'workspace'; // Default

    const p = pathname;
    if (p.startsWith('/dashboard/crm') || p.startsWith('/dashboard/cms') || p.startsWith('/dashboard/ecommerce') || p.startsWith('/dashboard/support') || p.startsWith('/dashboard/marketing')) {
      activeSection = 'business-suite';
    } else if (p.startsWith('/dashboard/ai-agents') || p.startsWith('/ai-agents') || p.startsWith('/dashboard/bi') || p.startsWith('/dashboard/workflows')) {
      activeSection = 'automation';
    } else if (p.startsWith('/tasks') || p.includes('/connectors')) {
      activeSection = 'operations';
    } else if (p.startsWith('/settings')) {
      activeSection = 'platform';
    } else if (p === '/dashboard' || p === '/dashboard/ai-assistant') {
      activeSection = 'workspace';
    }

    setExpandedSections([activeSection]);
  }, [pathname]);

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev =>
      prev.includes(sectionId) ? [] : [sectionId]
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
          id: 'support',
          name: 'Help & Support',
          href: '/dashboard/support',
          icon: <LifeBuoy className="w-4 h-4 ml-1" />,
          active: pathname === '/dashboard/support'
        },
        {
          id: 'marketing',
          name: 'Marketing',
          href: '/dashboard/marketing',
          icon: <Mail className="w-4 h-4" />,
          active: pathname.startsWith('/dashboard/marketing')
        },
        {
          id: 'directory',
          name: 'Directory Listings',
          href: '/dashboard/directory',
          icon: <Building2 className="w-4 h-4" />,
          active: pathname.startsWith('/dashboard/directory'),
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
          href: '/dashboard/bi',
          icon: <BarChart3 className="w-4 h-4" />,
          active: pathname.startsWith('/dashboard/bi')
        },
        {
          id: 'workflows',
          name: 'Workflow Management',
          href: '/dashboard/workflows',
          icon: <RefreshCw className="w-4 h-4 text-purple-600" />,
          active: pathname.startsWith('/dashboard/workflows'),
          badge: 'DEMO'
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
        },
        {
          id: 'plugin-marketplace',
          name: 'Plugin Marketplace',
          href: '/dashboard/connectors?category=marketplace',
          icon: <ShoppingCart className="w-4 h-4 text-blue-500" />,
          active: searchParams.get('category') === 'marketplace'
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
            {item.subItems
              ?.filter(subItem => subItem.show !== false)
              .map(subItem => renderNavigationItem(subItem, depth + 1))}
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