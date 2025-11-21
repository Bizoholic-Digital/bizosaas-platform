'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
  Menu, X, Home, Users, ShoppingCart, BarChart3, 
  Settings, Bell, CreditCard, FileText, LinkIcon, 
  ChevronDown, ChevronRight, Moon, Sun, TrendingUp,
  DollarSign, User, Target, Calendar, Package,
  Mail, MessageSquare, Share2, Activity, Zap,
  Lightbulb, Key, Shield, Terminal, Database, Grid, Code,
  LayoutDashboard, Workflow, Building2, Globe, AlertCircle,
  Bot, LogOut, Search, HardDrive, Gauge, ChevronUp
} from 'lucide-react';

interface AdminDashboardProps {
  children?: React.ReactNode;
}

export default function AdminDashboard({ children }: AdminDashboardProps = {}) {
  const pathname = usePathname();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [theme, setTheme] = useState(() => {
    if (typeof window === "undefined") return "light";
    try {
      return localStorage.getItem("theme") || "light";
    } catch {
      return "light";
    }
  });
  const [expandedSections, setExpandedSections] = useState<{[key: string]: boolean}>({});
  const [notifications, setNotifications] = useState([
    { id: 1, title: 'New tenant registered', type: 'info', time: '2 min ago' },
    { id: 2, title: 'Server CPU usage high', type: 'warning', time: '5 min ago' },
    { id: 3, title: 'Backup completed successfully', type: 'success', time: '1 hour ago' }
  ]);

  // Notification counts for sections and individual items
  const notificationCounts = {
    'management': { total: 3, items: { 'tenants': 2, 'users': 1, 'revenue': 0 } },
    'ecommerce': { total: 1, items: { 'dropshipping': 1, 'products': 0, 'orders': 0 } },
    'ai': { total: 2, items: { 'workflows': 1, 'ai-agents': 1, 'chat': 0 } },
    'monitoring': { total: 4, items: { 'system-health': 2, 'integrations': 1, 'api-analytics': 1 } },
    'system': { total: 2, items: { 'security': 1, 'sql-admin': 0, 'settings': 1 } }
  };

  useEffect(() => {
    if (typeof window === "undefined") return;
    
    try {
      document.documentElement.classList.toggle("dark", theme === "dark");
    } catch (e) {
      console.warn("Cannot set theme class");
    }
    
    // Initialize expanded sections
    setExpandedSections({
      "management": false,
      "monitoring": false,
      "system": false,
      "ecommerce": false,
      "ai": false
    });

    // Set active tab based on current pathname
    if (pathname === '/') setActiveTab('dashboard');
    else if (pathname.startsWith('/tenants')) setActiveTab('tenants');
    else if (pathname.startsWith('/users')) setActiveTab('users');
    else if (pathname.startsWith('/workflows')) setActiveTab('workflows');
    else if (pathname.startsWith('/dropshipping')) setActiveTab('dropshipping');
    else if (pathname.startsWith('/ai-agents')) setActiveTab('ai-agents');
    else if (pathname.startsWith('/system-health')) setActiveTab('system-health');
    else if (pathname.startsWith('/security')) setActiveTab('security');
    else if (pathname.startsWith('/settings')) setActiveTab('settings');
    else setActiveTab(pathname.slice(1));
  }, [theme, pathname]);

  const toggleTheme = useCallback(() => {
    const newTheme = theme === "light" ? "dark" : "light";
    setTheme(newTheme);
    try {
      localStorage.setItem("theme", newTheme);
      document.documentElement.classList.toggle("dark", newTheme === "dark");
    } catch (e) {
      console.warn("localStorage not available");
    }
  }, [theme]);

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionId]: !prev[sectionId]
    }));
  };

  const sidebarItems = [
    {
      id: 'dashboard',
      icon: LayoutDashboard,
      label: 'Dashboard',
      href: '/',
      children: []
    },
    {
      id: 'management',
      icon: Users,
      label: 'Management',
      children: [
        { id: 'tenants', label: 'Tenant Management', icon: Building2, href: '/tenants' },
        { id: 'users', label: 'User Management', icon: User, href: '/users' },
        { id: 'revenue', label: 'Revenue Analytics', icon: DollarSign, href: '/revenue' }
      ]
    },
    {
      id: 'ecommerce',
      icon: ShoppingCart,
      label: 'E-commerce',
      children: [
        { id: 'dropshipping', label: 'Dropshipping', icon: Package, href: '/dropshipping' },
        { id: 'products', label: 'Product Management', icon: Grid, href: '/products' },
        { id: 'orders', label: 'Order Management', icon: FileText, href: '/orders' }
      ]
    },
    {
      id: 'ai',
      icon: Bot,
      label: 'AI & Automation',
      children: [
        { id: 'workflows', label: 'Workflow Management', icon: Workflow, href: '/workflows' },
        { id: 'ai-agents', label: 'AI Agent Monitor', icon: Activity, href: '/ai-agents' },
        { id: 'chat', label: 'AI Assistant', icon: MessageSquare, href: '/chat' }
      ]
    },
    {
      id: 'monitoring',
      icon: BarChart3,
      label: 'Monitoring',
      children: [
        { id: 'system-health', label: 'System Health', icon: Gauge, href: '/system-health' },
        { id: 'integrations', label: 'Integration Status', icon: Globe, href: '/integrations' },
        { id: 'api-analytics', label: 'API Analytics', icon: TrendingUp, href: '/api-analytics' }
      ]
    },
    {
      id: 'system',
      icon: Shield,
      label: 'System',
      children: [
        { id: 'security', label: 'Security & Audit', icon: Shield, href: '/security' },
        { id: 'sql-admin', label: 'SQL Admin', icon: Database, href: '/admin' },
        { id: 'settings', label: 'System Settings', icon: Settings, href: '/settings' }
      ]
    }
  ];

  const renderSidebarItem = (item: any) => {
    const isExpanded = expandedSections[item.id];
    const hasChildren = item.children && item.children.length > 0;
    const isActive = activeTab === item.id || item.children?.some((child: any) => activeTab === child.id);

    if (!hasChildren) {
      return (
        <Link
          key={item.id}
          href={item.href || `/${item.id}`}
          onClick={() => setActiveTab(item.id)}
          className={cn(
            "flex items-center w-full text-left px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200",
            isActive
              ? "bg-blue-50 text-blue-700 border-r-4 border-blue-500"
              : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
          )}
        >
          <item.icon className="h-5 w-5 mr-3 flex-shrink-0" />
          {item.label}
        </Link>
      );
    }

    return (
      <div key={item.id}>
        <button
          onClick={() => toggleSection(item.id)}
          className={cn(
            "flex items-center justify-between w-full text-left px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200",
            isActive
              ? "bg-blue-50 text-blue-700"
              : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
          )}
        >
          <div className="flex items-center">
            <item.icon className="h-5 w-5 mr-3 flex-shrink-0" />
            {item.label}
          </div>
          <div className="flex items-center space-x-2">
            {/* Show total notifications when collapsed, or individual when expanded */}
            {!isExpanded && notificationCounts[item.id]?.total > 0 && (
              <span className="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-red-500 rounded-full">
                {notificationCounts[item.id].total}
              </span>
            )}
            {isExpanded ? (
              <ChevronDown className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
          </div>
        </button>
        
        {isExpanded && (
          <div className="ml-6 mt-2 space-y-1">
            {item.children.map((child: any) => (
              <Link
                key={child.id}
                href={child.href}
                onClick={() => setActiveTab(child.id)}
                className={cn(
                  "flex items-center px-4 py-2 text-sm rounded-lg transition-all duration-200",
                  activeTab === child.id
                    ? "bg-blue-100 text-blue-800 font-medium"
                    : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                )}
              >
                <child.icon className="h-4 w-4 mr-3 flex-shrink-0" />
                {child.label}
                {/* Show individual notification counts */}
                {notificationCounts[item.id]?.items[child.id] > 0 && (
                  <span className="ml-auto inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-red-500 rounded-full">
                    {notificationCounts[item.id].items[child.id]}
                  </span>
                )}
              </Link>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className={cn("min-h-screen", theme === "dark" ? "dark bg-gray-900" : "bg-gray-50")}>
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 sticky top-0 z-40">
        <div className="flex items-center justify-between px-4 sm:px-6 lg:px-8 h-16">
          <div className="flex items-center">
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 lg:hidden"
            >
              <Menu className="h-6 w-6" />
            </button>
            <div className="flex items-center ml-4 lg:ml-0">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Database className="w-5 h-5 text-white" />
              </div>
              <span className="ml-3 text-xl font-bold text-gray-900 dark:text-white">BizOSaaS Admin</span>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {/* Search */}
            <button className="p-2 text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">
              <Search className="h-5 w-5" />
            </button>

            {/* Notifications */}
            <div className="relative">
              <button className="p-2 text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">
                <Bell className="h-5 w-5" />
                {notifications.length > 0 && (
                  <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400 ring-2 ring-white"></span>
                )}
              </button>
            </div>

            {/* Theme toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md"
            >
              {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </button>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <div className={cn(
          "fixed inset-y-0 left-0 z-30 w-64 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static",
          isSidebarOpen ? "translate-x-0" : "-translate-x-full"
        )}>
          {/* Mobile close button */}
          <div className="flex items-center justify-end h-16 px-4 border-b border-gray-200 dark:border-gray-700 lg:hidden">
            <button
              onClick={() => setIsSidebarOpen(false)}
              className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <X className="h-6 w-6" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-4 space-y-2 overflow-y-auto">
            {sidebarItems.map(renderSidebarItem)}
          </nav>

          {/* User info */}
          <div className="border-t border-gray-200 dark:border-gray-700 p-4">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                <User className="w-4 h-4 text-gray-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-700 dark:text-gray-200">Super Admin</p>
                <p className="text-xs text-gray-500 dark:text-gray-400">admin@bizosaas.com</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main content */}
        <main className="flex-1 min-h-screen bg-gray-50 dark:bg-gray-900">
          {children || (
            <div className="p-6">
              <div className="text-center text-gray-500 dark:text-gray-400">
                <p>Content will be rendered here based on active tab: {activeTab}</p>
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Mobile sidebar overlay */}
      {isSidebarOpen && (
        <div
          className="fixed inset-0 bg-gray-600 bg-opacity-75 z-20 lg:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}
    </div>
  );
}