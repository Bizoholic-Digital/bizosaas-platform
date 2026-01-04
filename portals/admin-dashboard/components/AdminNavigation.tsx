'use client';

import React, { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  Users,
  Settings,
  Database,
  Shield,
  Zap,
  Activity,
  BarChart3,
  Menu,
  X,
  Search,
  Bell,
  AlertCircle,
  LogOut,
  ChevronRight,
  Globe,
  Cpu,
  History,
  MessageCircle,
  FileText
} from 'lucide-react';
import { ThemeToggle } from '@/components/theme-toggle';
import { useAuth } from '../shared/components/AuthProvider';

interface NavigationItem {
  name: string;
  href: string;
  icon: any;
  description: string;
  category: 'main' | 'management' | 'automation' | 'integrations' | 'system';
}

const navigation: NavigationItem[] = [
  {
    name: 'Admin Overview',
    href: '/',
    icon: LayoutDashboard,
    description: 'Platform key performance indicators',
    category: 'main'
  },
  {
    name: 'AI Monitor',
    href: '/monitor',
    icon: Activity,
    description: 'Cross-tenant AI agent activity & health',
    category: 'main'
  },
  {
    name: 'Tenants',
    href: '/tenants',
    icon: Globe,
    description: 'Organization and subscription management',
    category: 'management'
  },
  {
    name: 'Users & Roles',
    href: '/users',
    icon: Users,
    description: 'Administrative and tenant user control',
    category: 'management'
  },
  {
    name: 'Subscriptions',
    href: '/revenue',
    icon: BarChart3,
    description: 'Platform MRR and billing analytics',
    category: 'management'
  },
  {
    name: 'Orchestration',
    href: '/workflows',
    icon: Zap,
    description: 'Temporal workflow monitoring',
    category: 'automation'
  },
  {
    name: 'Model Management',
    href: '/agents',
    icon: Cpu,
    description: 'LLM performance & routing control',
    category: 'automation'
  },
  {
    name: 'Platform Integrations',
    href: '/connectors',
    icon: Database,
    description: 'Infrastructure & platform connectors',
    category: 'integrations'
  },
  {
    name: 'API Analytics',
    href: '/integrations',
    icon: Activity,
    description: 'Third-party API health & usage',
    category: 'integrations'
  },
  {
    name: 'Infrastructure Hub',
    href: '/system',
    icon: Database,
    description: 'Server & core service configuration',
    category: 'system'
  },
  {
    name: 'Security & Audit',
    href: '/security',
    icon: Shield,
    description: 'Access logs and security oversight',
    category: 'system'
  },
  {
    name: 'Compliance Center',
    href: '/security/compliance',
    icon: Shield,
    description: 'Regulatory status (SOC2, HIPAA, GDPR)',
    category: 'system'
  },
  {
    name: 'System Settings',
    href: '/settings',
    icon: Settings,
    description: 'Platform configuration and settings',
    category: 'system'
  }
];

const categoryLabels = {
  main: 'Dashboard',
  management: 'Platform Management',
  automation: 'AI & Automation',
  integrations: 'Intelligence & Integrations',
  system: 'System Administration'
};

const PLATFORM_VERSION = 'v5.0.3-PREMIUM';

interface AdminNavigationProps {
  children: React.ReactNode;
}

export function AdminNavigation({ children }: AdminNavigationProps) {
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout } = useAuth();

  // Auto-close sidebar on mobile when navigating
  useEffect(() => {
    setSidebarOpen(false);
  }, [pathname]);

  // Hide sidebar/header on login and unauthorized pages
  if (pathname === '/login' || pathname === '/unauthorized') {
    return <>{children}</>;
  }

  const isActiveLink = (href: string) => {
    if (href === '/') return pathname === '/';
    return pathname.startsWith(href);
  };

  const groupedNavigation = navigation.reduce((acc, item) => {
    if (!acc[item.category]) {
      acc[item.category] = [];
    }
    acc[item.category].push(item);
    return acc;
  }, {} as Record<string, NavigationItem[]>);

  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-950 overflow-hidden w-full">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-gray-600 bg-opacity-75 lg:hidden z-40"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={cn(
        "fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-900 shadow-xl transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 border-r border-gray-200 dark:border-gray-800 flex flex-col",
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Database className="w-5 h-5 text-white" />
            </div>
            <div className="ml-3 flex flex-col">
              <span className="text-sm font-black text-gray-900 dark:text-white leading-none tracking-tight underline decoration-blue-500 decoration-2">BizOSaaS</span>
              <span className="text-[9px] text-blue-600 dark:text-blue-400 font-bold mt-1 uppercase tracking-widest">{PLATFORM_VERSION}</span>
            </div>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden p-1 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation Section */}
        <nav className="flex-1 px-4 py-6 space-y-6 overflow-y-auto scrollbar-hide">
          {Object.entries(groupedNavigation).map(([category, items]) => (
            <div key={category}>
              <h3 className="px-2 text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-[2px]">
                {categoryLabels[category as keyof typeof categoryLabels]}
              </h3>
              <div className="mt-4 space-y-1">
                {items.map((item) => {
                  const isActive = isActiveLink(item.href);
                  const isExternal = item.href.startsWith('http');

                  const linkContent = (
                    <div className={cn(
                      "group flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-all duration-200",
                      isActive
                        ? "bg-blue-50 text-blue-700 dark:bg-blue-900/40 dark:text-blue-100 shadow-sm border border-blue-100 dark:border-blue-800/50"
                        : "text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50 hover:text-gray-900 dark:hover:text-white"
                    )}>
                      <item.icon className={cn(
                        "mr-3 h-4 w-4 flex-shrink-0 transition-transform duration-200 group-hover:scale-110",
                        isActive ? "text-blue-600" : "text-gray-400 group-hover:text-blue-500"
                      )} />
                      <div className="flex-1 truncate">{item.name}</div>
                      {isActive && <ChevronRight className="w-3 h-3 text-blue-400 animate-in slide-in-from-left-2" />}
                    </div>
                  );

                  if (isExternal) {
                    return (
                      <a
                        key={item.name}
                        href={item.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="block"
                      >
                        {linkContent}
                      </a>
                    );
                  }

                  return (
                    <Link key={item.name} href={item.href} className="block">
                      {linkContent}
                    </Link>
                  );
                })}
              </div>
            </div>
          ))}
        </nav>

        {/* Improved Premium Footer */}
        <div className="border-t border-gray-200 dark:border-gray-800 p-4 bg-gray-50/50 dark:bg-gray-900/50">
          <div className="flex items-center space-x-3 mb-4">
            <div className="relative">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center border border-white dark:border-gray-800 shadow-md">
                <span className="text-white font-bold text-sm">{user?.name?.[0] || 'A'}</span>
              </div>
              <span className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-green-500 border-2 border-white dark:border-gray-900 rounded-full"></span>
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-sm font-bold text-gray-900 dark:text-white truncate">{user?.name || 'Admin User'}</div>
              <div className="text-[10px] text-gray-500 dark:text-gray-400 uppercase tracking-wider font-semibold truncate leading-tight mt-0.5">
                {user?.role?.replace('_', ' ') || 'Super Admin'}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={() => logout()}
              className="flex items-center justify-center gap-2 py-2 px-3 text-xs font-bold text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg border border-red-100 dark:border-red-900/30 transition-all hover:shadow-sm active:scale-95"
            >
              <LogOut className="w-3.5 h-3.5" />
              Sign Out
            </button>
            <Link
              href="/settings"
              className="flex items-center justify-center gap-2 py-2 px-3 text-xs font-bold text-gray-700 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 transition-all shadow-sm active:scale-95"
            >
              <Settings className="w-3.5 h-3.5" />
              Setup
            </Link>
          </div>
        </div>
      </div>

      {/* Main content area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        {/* Top navigation */}
        <header className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-800 z-10">
          <div className="flex items-center justify-between h-16 px-6">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                aria-label="Toggle Sidebar"
              >
                <Menu className="w-6 h-6 text-gray-600 dark:text-gray-400" />
              </button>
              <div className="hidden lg:block">
                <h1 className="text-xl font-black text-gray-900 dark:text-white tracking-tight flex items-center">
                  <span className="text-blue-500 bg-blue-50 dark:bg-blue-900/30 px-2 py-1 rounded inline-flex items-center justify-center mr-3 scale-90">/</span>
                  PLATFORM CORE
                  <span className="mx-3 h-4 w-px bg-gray-200 dark:bg-gray-700"></span>
                  <span className="text-gray-400 dark:text-gray-500 font-medium text-sm">Administration</span>
                </h1>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <div className="relative hidden md:block group">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                <input
                  type="text"
                  placeholder="Global Search..."
                  className="pl-10 pr-4 py-2 text-sm border border-gray-200 dark:border-gray-700 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white transition-all w-64"
                />
              </div>
              <ThemeToggle />
              <button className="p-2.5 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 relative transition-colors">
                <Bell className="w-5 h-5 text-gray-500" />
                <span className="absolute top-2 right-2.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white dark:border-gray-900"></span>
              </button>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto bg-[#F9FAFB] dark:bg-[#0B0E14] scroll-smooth p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}