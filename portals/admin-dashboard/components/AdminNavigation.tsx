'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  Settings,
  Workflow,
  Users,
  Building2,
  Activity,
  DollarSign,
  Shield,
  Database,
  Globe,
  TrendingUp,
  AlertCircle,
  Bell,
  Search,
  LogOut,
  Menu,
  X,
  Bot,
  MessageCircle,
  FileText
} from 'lucide-react';
import { useState } from 'react';
import { ThemeToggle } from '@/components/theme-toggle';
import { useAuth } from '../shared/components/AuthProvider';

interface NavigationItem {
  name: string;
  href: string;
  icon: React.ComponentType<any>;
  description: string;
  category: 'main' | 'management' | 'monitoring' | 'system';
}

const navigation: NavigationItem[] = [
  // Platform Overview
  {
    name: 'Admin Overview',
    href: '/',
    icon: LayoutDashboard,
    description: 'Platform status and global metrics',
    category: 'main'
  },
  {
    name: 'System Health',
    href: '/system-health',
    icon: Activity,
    description: 'Infrastructure and performance monitoring',
    category: 'main'
  },

  // Platform Management
  {
    name: 'Tenant Management',
    href: '/tenants',
    icon: Building2,
    description: 'Manage all tenant organizations',
    category: 'management'
  },
  {
    name: 'Global User Management',
    href: '/users',
    icon: Users,
    description: 'Platform-wide user administration',
    category: 'management'
  },
  {
    name: 'Unified CMS',
    href: '/cms',
    icon: FileText,
    description: 'Global content management system',
    category: 'management'
  },

  // AI & Automation
  {
    name: 'AI Agent Monitor',
    href: '/ai-agents',
    icon: Bot,
    description: 'Real-time AI agent execution tracking',
    category: 'monitoring'
  },
  {
    name: 'Workflow Orchestration',
    href: '/dashboard/workflows',
    icon: Workflow,
    description: 'AI workflows and automation control',
    category: 'monitoring'
  },
  {
    name: 'Connectivity Hub',
    href: '/integrations',
    icon: Globe,
    description: 'Third-party integration monitoring',
    category: 'monitoring'
  },
  {
    name: 'API Analytics',
    href: '/api-analytics',
    icon: TrendingUp,
    description: 'API usage and rate limiting dashboard',
    category: 'monitoring'
  },

  // System
  {
    name: 'Security & Audit',
    href: '/security',
    icon: Shield,
    description: 'Security monitoring and audit logs',
    category: 'system'
  },
  {
    name: 'SQL Admin',
    href: 'http://localhost:3009/admin',
    icon: Database,
    description: 'Direct database administration interface',
    category: 'system'
  },
  {
    name: 'AI Assistant',
    href: '/chat',
    icon: Bot,
    description: 'AI-powered platform assistance and automation',
    category: 'main'
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
  main: 'Main Dashboard',
  management: 'Management',
  monitoring: 'Monitoring',
  system: 'System Administration'
};

interface AdminNavigationProps {
  children: React.ReactNode;
}

export function AdminNavigation({ children }: AdminNavigationProps) {
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user } = useAuth();

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
    <div className="flex h-screen bg-gray-100 dark:bg-gray-950">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-gray-600 bg-opacity-75 lg:hidden z-40"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={cn(
        "fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-900 shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 border-r border-gray-200 dark:border-gray-800",
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <Database className="w-5 h-5 text-white" />
            </div>
            <span className="ml-2 text-lg font-bold text-gray-900 dark:text-white">Bizo Admin</span>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden p-1 rounded-md hover:bg-gray-100"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-6 overflow-y-auto">
          {Object.entries(groupedNavigation).map(([category, items]) => (
            <div key={category}>
              <h3 className="px-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                {categoryLabels[category as keyof typeof categoryLabels]}
              </h3>
              <div className="mt-2 space-y-1">
                {items.map((item) => {
                  const isActive = isActiveLink(item.href);
                  const isExternal = item.href.startsWith('http');

                  const linkContent = (
                    <div className={cn(
                      "group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors duration-200",
                      isActive
                        ? "bg-blue-100 text-blue-900 dark:bg-blue-900/30 dark:text-blue-100 border-r-2 border-blue-600"
                        : "text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white"
                    )}>
                      <item.icon className={cn(
                        "mr-3 h-5 w-5 flex-shrink-0",
                        isActive ? "text-blue-600" : "text-gray-400 group-hover:text-gray-500"
                      )} />
                      <div className="flex-1">
                        <div>{item.name}</div>
                      </div>
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

        {/* Footer */}
        <div className="border-t border-gray-200 dark:border-gray-800 p-4">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gray-300 dark:bg-gray-700 rounded-full flex items-center justify-center">
              <Users className="w-4 h-4 text-gray-600" />
            </div>
            <div className="flex-1">
              <div className="flex-1">
                <div className="text-sm font-medium text-gray-900 dark:text-white">{user?.name || 'Admin User'}</div>
                <div className="text-xs text-gray-500 dark:text-gray-400 capitalize">{user?.role?.replace('_', ' ') || 'Administrator'}</div>
              </div>
            </div>
            <button className="p-1 rounded-md hover:bg-gray-100">
              <LogOut className="w-4 h-4 text-gray-500" />
            </button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top navigation */}
        <header className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between h-16 px-6">
            <div className="flex items-center">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden p-1 rounded-md hover:bg-gray-100"
              >
                <Menu className="w-6 h-6" />
              </button>
              <div className="hidden lg:block">
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Platform Administration
                </h1>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search..."
                  className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
              </div>
              <ThemeToggle />
              <button className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 relative">
                <Bell className="w-5 h-5 text-gray-600" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>
              <button className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
                <AlertCircle className="w-5 h-5 text-gray-600 dark:text-gray-400" />
              </button>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}