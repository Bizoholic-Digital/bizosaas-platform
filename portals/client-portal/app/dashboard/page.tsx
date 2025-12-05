'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import {
  Menu, X, Home, Users, ShoppingCart, BarChart3,
  Settings, Bell, CreditCard, FileText, LinkIcon,
  ChevronDown, ChevronRight, Moon, Sun, TrendingUp,
  DollarSign, User, Target, Calendar, Package,
  Mail, MessageSquare, Share2, Activity, Zap,
  Lightbulb, Key, Shield, Terminal, Database, Grid, Code, LogOut, Server,
  CheckCircle, Image, Layout, Sparkles, Gauge, Plug, Wrench, Globe, Building
} from 'lucide-react';
import { signOut } from "next-auth/react";
import { CRMContent } from '@/components/CRMContent';
import { CMSContent } from '@/components/CMSContent';
import { EcommerceContent } from '@/components/EcommerceContent';
import { MarketingContent } from '@/components/MarketingContent';
import { AnalyticsContent } from '@/components/AnalyticsContent';
import { AdminContent } from '@/components/AdminContent';
import { AIChat } from '@/components/AIChat';
import { PlatformOverview } from '@/components/PlatformOverview';
import { TenantManagement } from '@/components/TenantManagement';
import { BillingContent } from '@/components/BillingContent';
import { IntegrationsContent } from '@/components/IntegrationsContent';
import { SettingsContent } from '@/components/SettingsContent';
import { useSession } from 'next-auth/react';
import { getUserDisplayInfoFromSession, filterMenuByPermissions } from '@/utils/rbac';
import ConnectorsPage from './connectors/page';
import ToolsPage from './tools/page';
import GetWebsitePage from './get-website/page';
import { ThemeToggle } from '@/components/theme-toggle';

export default function ClientPortalDashboard() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { data: session } = useSession();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [mounted, setMounted] = useState(false);
  const [expandedSections, setExpandedSections] = useState<{ [key: string]: boolean }>({});

  // Get user role and permissions
  // Get user role and permissions from session
  const userInfo = getUserDisplayInfoFromSession(session?.user);
  const { role, permissions, tenantId, displayName } = userInfo;



  // ... (keep existing imports)

  // Define menu items
  const allMenuItems = [
    {
      id: 'dashboard',
      icon: Home,
      label: 'Dashboard'
    },
    {
      id: 'connectors',
      icon: Plug,
      label: 'Connectors'
    },
    {
      id: 'ai-assistant',
      icon: Sparkles,
      label: 'AI Agents',
      requiredPermissions: ['ai:use']
    },
    {
      id: 'cms',
      icon: Layout,
      label: 'CMS',
      children: [
        { id: 'cms-pages', label: 'Pages', icon: FileText },
        { id: 'cms-posts', label: 'Blog Posts', icon: FileText },
        { id: 'cms-media', label: 'Media Library', icon: Image },
        { id: 'cms-menus', label: 'Menus', icon: Layout }
      ]
    },
    {
      id: 'crm',
      icon: Users,
      label: 'CRM',
      children: [
        { id: 'crm-contacts', label: 'Contacts', icon: Users },
        { id: 'crm-companies', label: 'Companies', icon: Building },
        { id: 'crm-deals', label: 'Deals', icon: DollarSign },
        { id: 'crm-tasks', label: 'Tasks', icon: CheckCircle }
      ]
    },
    {
      id: 'ecommerce',
      icon: ShoppingCart,
      label: 'E-commerce',
      children: [
        { id: 'ecommerce-products', label: 'Products', icon: Package },
        { id: 'ecommerce-orders', label: 'Orders', icon: ShoppingCart },
        { id: 'ecommerce-customers', label: 'Customers', icon: Users },
        { id: 'ecommerce-analytics', label: 'Analytics', icon: BarChart3 }
      ]
    },
    {
      id: 'marketing',
      icon: Target,
      label: 'Marketing',
      children: [
        { id: 'marketing-campaigns', label: 'Campaigns', icon: Target },
        { id: 'marketing-email', label: 'Email Marketing', icon: Mail },
        { id: 'marketing-social', label: 'Social Media', icon: Share2 },
        { id: 'marketing-automation', label: 'Automation', icon: Zap },
        { id: 'marketing-leads', label: 'Lead Generation', icon: Users },
        { id: 'marketing-seo', label: 'SEO Tools', icon: TrendingUp }
      ]
    },
    {
      id: 'analytics',
      icon: BarChart3,
      label: 'Analytics',
      children: [
        { id: 'analytics-overview', label: 'Overview', icon: BarChart3 },
        { id: 'analytics-traffic', label: 'Traffic', icon: TrendingUp },
        { id: 'analytics-conversions', label: 'Conversions', icon: Target },
        { id: 'analytics-performance', label: 'Performance', icon: Activity },
        { id: 'analytics-goals', label: 'Goals', icon: Target },
        { id: 'analytics-insights', label: 'AI Insights', icon: Lightbulb },
        { id: 'analytics-real-time', label: 'Real-time', icon: Activity },
        { id: 'analytics-custom', label: 'Custom Reports', icon: Settings }
      ]
    },
    {
      id: 'tools',
      icon: Wrench,
      label: 'Tools'
    },
    {
      id: 'get-website',
      icon: Globe,
      label: 'Get Website'
    },
    {
      id: 'billing',
      icon: CreditCard,
      label: 'Billing',
      children: [
        { id: 'billing-overview', label: 'Overview', icon: BarChart3 },
        { id: 'billing-subscriptions', label: 'Subscriptions', icon: CreditCard },
        { id: 'billing-invoices', label: 'Invoices', icon: FileText },
        { id: 'billing-payment-methods', label: 'Payment Methods', icon: CreditCard },
        { id: 'billing-usage', label: 'Usage & Limits', icon: Activity },
        { id: 'billing-history', label: 'Billing History', icon: Activity },
        { id: 'billing-tax', label: 'Tax Settings', icon: Settings }
      ]
    },
    {
      id: 'integrations',
      icon: LinkIcon,
      label: 'Integrations',
      children: [
        { id: 'integrations-overview', label: 'Overview', icon: LinkIcon },
        { id: 'integrations-webhooks', label: 'Webhooks', icon: Activity },
        { id: 'integrations-api-keys', label: 'API Keys', icon: Key },
        { id: 'integrations-third-party', label: 'Third-party Apps', icon: Grid },
        { id: 'integrations-automation', label: 'Automation Rules', icon: Zap },
        { id: 'integrations-logs', label: 'Logs', icon: FileText },
        { id: 'integrations-marketplace', label: 'Marketplace', icon: ShoppingCart }
      ]
    },
    {
      id: 'super-admin',
      icon: Gauge,
      label: 'Super Admin',
      requiredRole: 'super_admin',
      children: [
        { id: 'super-admin-platform', label: 'Platform Overview', icon: Gauge },
        { id: 'super-admin-tenants', label: 'Tenant Management', icon: Users },
        { id: 'super-admin-users', label: 'User Management', icon: User },
        { id: 'super-admin-system', label: 'System Health', icon: Server },
        { id: 'super-admin-analytics', label: 'Analytics', icon: BarChart3 },
        { id: 'super-admin-config', label: 'Configuration', icon: Settings }
      ]
    },
    {
      id: 'admin',
      icon: Shield,
      label: 'Admin',
      children: [
        { id: 'admin-services', label: 'Service Status', icon: Server },
        { id: 'admin-metrics', label: 'System Metrics', icon: BarChart3 },
        { id: 'admin-users', label: 'User Management', icon: Users },
        { id: 'admin-settings', label: 'Admin Settings', icon: Settings }
      ]
    },
    {
      id: 'settings',
      icon: Settings,
      label: 'Settings',
      children: [
        { id: 'settings-general', label: 'General', icon: Settings },
        { id: 'settings-notifications', label: 'Notifications', icon: Bell },
        { id: 'settings-security', label: 'Security', icon: Shield },
        { id: 'settings-team', label: 'Team Management', icon: Users },
        { id: 'settings-preferences', label: 'Preferences', icon: User },
        { id: 'settings-advanced', label: 'Advanced', icon: Code },
        { id: 'settings-backup', label: 'Backup & Restore', icon: Database },
        { id: 'settings-api', label: 'API Configuration', icon: Terminal }
      ]
    }
  ];

  const menuItems = filterMenuByPermissions(allMenuItems, permissions);

  // ... (keep existing code)

  // Helper functions
  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.classList.toggle('dark');
  };

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionId]: !prev[sectionId]
    }));
  };

  const renderSidebarItem = (item: any) => {
    const Icon = item.icon;
    const isActive = activeTab === item.id || activeTab.startsWith(item.id + '-');
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedSections[item.id];

    if (item.hidden) return null;

    return (
      <div key={item.id}>
        <button
          onClick={() => {
            if (hasChildren) {
              toggleSection(item.id);
            } else {
              setActiveTab(item.id);
              if (window.innerWidth < 1024) setIsSidebarOpen(false);
            }
          }}
          className={`w-full flex items-center justify-between p-2 rounded-lg transition-colors ${isActive
            ? 'bg-purple-50 text-purple-600 dark:bg-purple-900/20 dark:text-purple-400'
            : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
        >
          <div className="flex items-center space-x-3">
            <Icon className="w-5 h-5" />
            {isSidebarOpen && <span>{item.label}</span>}
          </div>
          {isSidebarOpen && hasChildren && (
            isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />
          )}
        </button>

        {isSidebarOpen && hasChildren && isExpanded && (
          <div className="ml-9 mt-1 space-y-1">
            {item.children.map((child: any) => (
              <button
                key={child.id}
                onClick={() => {
                  setActiveTab(child.id);
                  if (window.innerWidth < 1024) setIsSidebarOpen(false);
                }}
                className={`w-full flex items-center p-2 rounded-lg text-sm transition-colors ${activeTab === child.id
                  ? 'text-purple-600 dark:text-purple-400 font-medium'
                  : 'text-gray-500 dark:text-gray-500 hover:text-gray-900 dark:hover:text-gray-300'
                  }`}
              >
                <div className="w-1.5 h-1.5 rounded-full bg-current mr-3" />
                {child.label}
              </button>
            ))}
          </div>
        )}
      </div>
    );
  };

  const renderContent = () => {
    if (activeTab === 'dashboard') {
      return (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                  <Plug className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Active Connectors</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">3</p>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-green-600 dark:text-green-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">AI Tasks</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">128</p>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                  <BarChart3 className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Traffic</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">12.5k</p>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-orange-600 dark:text-orange-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Conversions</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">4.2%</p>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Welcome to BizOSaaS</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Your central hub for managing your digital presence. Connect your existing platforms, leverage AI agents, and grow your business.
            </p>
          </div>
        </div>
      );
    }

    // Handle Connectors section
    if (activeTab === 'connectors') {
      return <ConnectorsPage />;
    }

    // Handle Tools section
    if (activeTab === 'tools') {
      return <ToolsPage />;
    }

    // Handle Get Website section
    if (activeTab === 'get-website') {
      return <GetWebsitePage />;
    }

    // Handle CMS section
    if (activeTab.startsWith('cms')) {
      return <CMSContent activeTab={activeTab} />;
    }

    // Handle CRM section
    if (activeTab.startsWith('crm')) {
      return <CRMContent activeTab={activeTab} />;
    }

    // Handle E-commerce section
    if (activeTab.startsWith('ecommerce')) {
      return <EcommerceContent activeTab={activeTab} />;
    }

    // Handle Marketing section
    if (activeTab.startsWith('marketing')) {
      return <MarketingContent activeTab={activeTab} />;
    }

    // Handle Analytics section
    if (activeTab.startsWith('analytics')) {
      return <AnalyticsContent activeTab={activeTab} />;
    }

    // Handle Billing section
    if (activeTab.startsWith('billing')) {
      return <BillingContent activeTab={activeTab} />;
    }

    // Handle Integrations section
    if (activeTab.startsWith('integrations')) {
      return <IntegrationsContent activeTab={activeTab} />;
    }

    // Handle Settings section
    if (activeTab.startsWith('settings')) {
      return <SettingsContent activeTab={activeTab} />;
    }

    // Handle Admin section
    if (activeTab.startsWith('admin')) {
      return <AdminContent activeTab={activeTab} />;
    }

    // Handle AI Assistant
    if (activeTab === 'ai-assistant') {
      return <AIChat activeTab={activeTab} />;
    }

    // Handle Super Admin section
    if (activeTab.startsWith('super-admin')) {
      if (activeTab === 'super-admin-platform') {
        return <PlatformOverview />;
      }
      if (activeTab === 'super-admin-tenants') {
        return <TenantManagement />;
      }
      return (
        <div className="flex items-center justify-center h-96 text-gray-500 dark:text-gray-400">
          Super Admin module: {activeTab.replace('super-admin-', '')} coming soon
        </div>
      );
    }

    return (
      <div className="flex items-center justify-center h-96 text-gray-500 dark:text-gray-400">
        Content for {activeTab} is coming soon
      </div>
    );
  };


  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex">
      {/* Sidebar */}
      {/* Sidebar */}
      <div className={`${isSidebarOpen ? 'w-64' : 'w-16'} transition-all duration-300 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col h-screen sticky top-0`}>
        {/* Header */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-800 shrink-0">
          <div className="flex items-center justify-between">
            {isSidebarOpen && (
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">CP</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Client Portal</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">BizOSaaS Platform</p>
                </div>
              </div>
            )}
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              {isSidebarOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {menuItems.map((item) => renderSidebarItem(item))}
        </nav>

        {/* User Info */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-800 shrink-0">
          {isSidebarOpen ? (
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm font-medium">AC</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                    Acme Corporation
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    Premium Plan
                  </p>
                </div>
              </div>
              <button
                onClick={() => signOut({ callbackUrl: '/login' })}
                className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          ) : (
            <button
              onClick={() => signOut({ callbackUrl: '/login' })}
              className="w-full p-2 flex justify-center text-gray-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
              title="Logout"
            >
              <LogOut className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <header className="sticky top-0 z-50 bg-white shadow-sm border-b border-gray-200 dark:bg-gray-900 dark:border-gray-800 p-4">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
              {activeTab === 'dashboard' ? 'Dashboard' : activeTab.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </h1>
            <div className="flex items-center space-x-4">
              <ThemeToggle />

              <button
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors relative"
                title="Notifications"
              >
                <Bell className="w-5 h-5" />
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full text-xs flex items-center justify-center">
                  <span className="w-2 h-2 bg-white rounded-full"></span>
                </span>
              </button>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 p-6">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}