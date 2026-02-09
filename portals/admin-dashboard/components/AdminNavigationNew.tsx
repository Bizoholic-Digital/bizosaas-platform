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
  LayoutDashboard, Layout, Workflow, Building2, Globe, AlertCircle,
  Bot, LogOut, Search, HardDrive, Gauge, ChevronUp, LifeBuoy, ShieldAlert
} from 'lucide-react';
import { useAuth } from '@/shared/components/AuthProvider';
import { getEffectivePermissions, UserRole } from '@/lib/rbac';

interface AdminDashboardProps {
  children?: React.ReactNode;
}

export default function AdminDashboard({ children }: AdminDashboardProps = {}) {
  const pathname = usePathname();
  const { user, logout } = useAuth();
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
  const [expandedSections, setExpandedSections] = useState<{ [key: string]: boolean }>({});
  const [notifications, setNotifications] = useState([
    { id: 1, title: 'New tenant registered', type: 'info', time: '2 min ago' },
    { id: 2, title: 'Server CPU usage high', type: 'warning', time: '5 min ago' },
    { id: 3, title: 'Backup completed successfully', type: 'success', time: '1 hour ago' }
  ]);

  interface NotificationItem {
    total: number;
    items: { [key: string]: number };
  }

  interface NotificationCounts {
    [key: string]: NotificationItem;
  }

  // Notification counts for sections and individual items
  const notificationCounts: NotificationCounts = {
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
    else if (pathname.startsWith('/directory')) setActiveTab('directory');
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
      children: [],
      permission: null
    },
    {
      id: 'management',
      icon: Users,
      label: 'Management',
      children: [
        { id: 'tenants', label: 'Tenant Management', icon: Building2, href: '/dashboard/tenants', permission: 'canManageTenants' },
        { id: 'users', label: 'User Management', icon: User, href: '/dashboard/users', permission: 'canManageUsers' },
        { id: 'directory', label: 'Business Directory', icon: Globe, href: '/dashboard/directory', permission: 'canAccessAdmin' },
        { id: 'domains', label: 'Domain Control Center', icon: Globe, href: '/dashboard/domains', permission: 'canAccessAdmin' },
        { id: 'cms-overwatch', label: 'CMS Overwatch', icon: Layout, href: '/dashboard/cms', permission: 'canAccessCMS' },
        { id: 'crm', label: 'Global CRM Monitor', icon: Target, href: '/dashboard/crm', permission: 'canAccessCRM' },
        { id: 'revenue', label: 'Revenue Analytics', icon: DollarSign, href: '/dashboard/revenue', permission: 'canAccessAnalytics' },
        { id: 'support', label: 'Support & Tickets', icon: LifeBuoy, href: '/dashboard/support', permission: 'canAccessAdmin' }
      ]
    },
    {
      id: 'ecommerce',
      icon: ShoppingCart,
      label: 'E-commerce',
      permission: 'canAccessEcommerce',
      children: [
        { id: 'dropshipping', label: 'Dropshipping', icon: Package, href: '/dashboard/dropshipping' },
        { id: 'products', label: 'Product Management', icon: Grid, href: '/dashboard/products' },
        { id: 'orders', label: 'Order Management', icon: FileText, href: '/dashboard/orders' }
      ]
    },
    {
      id: 'ai',
      icon: Bot,
      label: 'AI & Automation',
      permission: 'canAccessAdmin',
      children: [
        { id: 'workflows', label: 'Workflow Management', icon: Workflow, href: '/dashboard/workflows' },
        { id: 'ai-agents', label: 'AI Agent Monitor', icon: Activity, href: '/dashboard/ai-agents' },
        { id: 'mcp-marketplace', label: 'MCP Marketplace', icon: Package, href: '/dashboard/mcp-management' },
        { id: 'governance', label: 'AI Governance', icon: ShieldAlert, href: '/dashboard/governance' },
        { id: 'chat', label: 'AI Assistant', icon: MessageSquare, href: '/dashboard/chat' }
      ]
    },
    {
      id: 'monitoring',
      icon: BarChart3,
      label: 'Monitoring',
      permission: 'canViewSystemMetrics',
      children: [
        { id: 'system-health', label: 'System Health', icon: Gauge, href: '/dashboard/system-health' },
        { id: 'integrations', label: 'Integration Status', icon: Globe, href: '/dashboard/integrations' },
        { id: 'api-analytics', label: 'API Analytics', icon: TrendingUp, href: '/dashboard/api-analytics' }
      ]
    },
    {
      id: 'system',
      icon: Shield,
      label: 'System',
      permission: 'canAccessSettings',
      children: [
        { id: 'security', label: 'Security & Audit', icon: Shield, href: '/dashboard/security' },
        { id: 'sql-admin', label: 'SQL Admin', icon: Database, href: '/dashboard/admin' },
        { id: 'settings', label: 'System Settings', icon: Settings, href: '/dashboard/settings' }
      ]
    }
  ];

  // Calculate permissions
  const permissions = getEffectivePermissions(
    (user?.role as UserRole) || 'user',
    user?.plan_features || []
  );

  // Filter items based on permissions
  const filteredSidebarItems = sidebarItems.filter(item => {
    // If it's a top-level section with a permission check
    if (item.permission && !(permissions as any)[item.permission]) {
      return false;
    }

    // Filter children (if any)
    if (item.children && item.children.length > 0) {
      const originalChildren = [...item.children];
      const validChildren = originalChildren.filter((child: any) => {
        if (child.permission && !(permissions as any)[child.permission]) {
          return false;
        }
        return true;
      });
      // Only show section if it has children remaining or if it's the dashboard
      return item.children.length > 0 || item.id === 'dashboard';
    }

    return true;
  });

  const BottomNav = () => {
    if (isSidebarOpen && typeof window !== 'undefined' && window.innerWidth < 1024) return null;

    return (
      <div className="lg:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 px-6 py-2 flex justify-between items-center z-50 safe-area-bottom">
        <Link href="/" onClick={() => setActiveTab('dashboard')} className={cn("flex flex-col items-center p-2", activeTab === 'dashboard' ? "text-blue-600" : "text-gray-400")}>
          <Home className="h-5 w-5" />
          <span className="text-[10px] mt-1 font-medium">Home</span>
        </Link>
        <Link href="/dashboard/workflows" onClick={() => setActiveTab('workflows')} className={cn("flex flex-col items-center p-2", activeTab === 'workflows' ? "text-blue-600" : "text-gray-400")}>
          <Zap className="h-5 w-5" />
          <span className="text-[10px] mt-1 font-medium">Workflows</span>
        </Link>
        <Link href="/ai-agents" onClick={() => setActiveTab('ai-agents')} className={cn("flex flex-col items-center p-2", activeTab === 'ai-agents' ? "text-blue-600" : "text-gray-400")}>
          <Bot className="h-5 w-5" />
          <span className="text-[10px] mt-1 font-medium">Agents</span>
        </Link>
        <Link href="/system-health" onClick={() => setActiveTab('system-health')} className={cn("flex flex-col items-center p-2", activeTab === 'system-health' ? "text-blue-600" : "text-gray-400")}>
          <Activity className="h-5 w-5" />
          <span className="text-[10px] mt-1 font-medium">Monitor</span>
        </Link>
        <button onClick={() => setIsSidebarOpen(true)} className="flex flex-col items-center p-2 text-gray-400">
          <Menu className="h-5 w-5" />
          <span className="text-[10px] mt-1 font-medium">Menu</span>
        </button>
      </div>
    );
  };

  return (
    <div className={cn("min-h-screen", theme === "dark" ? "dark bg-gray-900" : "bg-gray-50")}>
      {/* Header */}
      <header className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md shadow-sm border-b border-gray-200 dark:border-gray-700 sticky top-0 z-40">
        <div className="flex items-center justify-between px-4 sm:px-6 lg:px-8 h-14">
          <div className="flex items-center">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
                <Database className="w-4 h-4 text-white" />
              </div>
              <span className="ml-3 text-lg font-black tracking-tighter text-gray-900 dark:text-white uppercase">Bizo Admin</span>
            </div>
          </div>

          <div className="flex items-center space-x-2 md:space-x-4">
            {/* Search */}
            <button className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-gray-700 rounded-xl transition-all">
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
          <nav className="flex-1 px-4 py-4 space-y-1 overflow-y-auto no-scrollbar">
            {filteredSidebarItems.map((item) => {
              const isExpanded = expandedSections[item.id];
              const children = (item as any)._filteredChildren || item.children || [];
              const hasChildren = children.length > 0;
              const isActive = activeTab === item.id || children.some((child: any) => activeTab === child.id);

              if (!hasChildren) {
                return (
                  <Link
                    key={item.id}
                    href={item.href || `/${item.id}`}
                    onClick={() => {
                      setActiveTab(item.id);
                      if (window.innerWidth < 1024) setIsSidebarOpen(false);
                    }}
                    className={cn(
                      "flex items-center w-full px-4 py-3 text-sm font-bold rounded-xl transition-all duration-200 mb-1",
                      isActive
                        ? "bg-blue-600 text-white shadow-lg shadow-blue-500/20"
                        : "text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700/50"
                    )}
                  >
                    <item.icon className={cn("h-5 w-5 mr-3 flex-shrink-0 transition-colors", isActive ? "text-white" : "text-gray-400")} />
                    {item.label}
                  </Link>
                );
              }

              return (
                <div key={item.id} className="mb-1">
                  <button
                    onClick={() => toggleSection(item.id)}
                    className={cn(
                      "flex items-center justify-between w-full px-4 py-3 text-sm font-bold rounded-xl transition-all duration-200",
                      isActive
                        ? "bg-blue-50 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400"
                        : "text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700/50"
                    )}
                  >
                    <div className="flex items-center">
                      <item.icon className={cn("h-5 w-5 mr-3 flex-shrink-0", isActive ? "text-blue-600" : "text-gray-400")} />
                      {item.label}
                    </div>
                    <div className="flex items-center space-x-2">
                      {!isExpanded && notificationCounts[item.id]?.total > 0 && (
                        <span className="inline-flex items-center justify-center h-5 w-5 text-[10px] font-black text-white bg-red-500 rounded-full scale-90">
                          {notificationCounts[item.id].total}
                        </span>
                      )}
                      {isExpanded ? <ChevronDown className="h-4 w-4 opacity-50" /> : <ChevronRight className="h-4 w-4 opacity-50" />}
                    </div>
                  </button>

                  {isExpanded && (
                    <div className="ml-4 mt-1 space-y-1 border-l-2 border-gray-100 dark:border-gray-700 pl-2">
                      {children.map((child: any) => (
                        <Link
                          key={child.id}
                          href={child.href}
                          onClick={() => {
                            setActiveTab(child.id);
                            if (window.innerWidth < 1024) setIsSidebarOpen(false);
                          }}
                          className={cn(
                            "flex items-center px-4 py-2.5 text-xs font-bold rounded-lg transition-all duration-200",
                            activeTab === child.id
                              ? "bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300"
                              : "text-gray-500 hover:bg-gray-50 dark:text-gray-400 dark:hover:bg-gray-800"
                          )}
                        >
                          <child.icon className={cn("h-4 w-4 mr-3", activeTab === child.id ? "text-blue-600" : "text-gray-400")} />
                          {child.label}
                          {notificationCounts[item.id]?.items[child.id] > 0 && (
                            <span className="ml-auto inline-flex items-center justify-center h-4 w-4 text-[9px] font-black text-white bg-red-400 rounded-full">
                              {notificationCounts[item.id].items[child.id]}
                            </span>
                          )}
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </nav>

          {/* User info */}
          <div className="border-t border-gray-200 dark:border-gray-700 p-4 pb-12">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-gray-300 dark:bg-gray-700 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-200">{user?.name || 'Super Admin'}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 truncate w-32">{user?.email || 'admin@bizosaas.com'}</p>
                </div>
              </div>
              <button
                onClick={() => logout()}
                className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                title="Sign Out"
              >
                <LogOut className="h-5 w-5" />
              </button>
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
      <BottomNav />
    </div>
  );
}