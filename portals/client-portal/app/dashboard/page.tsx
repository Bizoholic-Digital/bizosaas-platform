'use client';

import React, { useState, useEffect, Suspense } from 'react';
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
import { DashboardSidebar } from '@/components/DashboardSidebar';
import { useMobileSidebar } from '@/components/MobileSidebarContext';
import { CRMContent } from '@/components/CRMContent';
import { CMSContent } from '@/components/CMSContent';
import { EcommerceContent } from '@/components/EcommerceContent';
import { MarketingContent } from '@/components/MarketingContent';
import { AnalyticsContent } from '@/components/AnalyticsContent';
import { AdminContent } from '@/components/AdminContent';
import { AIChat } from '@/components/AIChat';
import { ConnectorsContent } from '@/components/ConnectorsContent';
import { ToolsContent } from '@/components/ToolsContent';
import { GetWebsiteContent } from '@/components/GetWebsiteContent';
import { PlatformOverview } from '@/components/PlatformOverview';
import { TenantManagement } from '@/components/TenantManagement';
import { BillingContent } from '@/components/BillingContent';
import { IntegrationsContent } from '@/components/IntegrationsContent';
import { SettingsContent } from '@/components/SettingsContent';
import { useSession } from 'next-auth/react';
import { getUserDisplayInfoFromSession, filterMenuByPermissions } from '@/utils/rbac';
import { ThemeToggle } from '@/components/theme-toggle';
import { ProjectTasksWidget } from '@/components/dashboard/widgets/ProjectTasksWidget';

function DashboardContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { data: session } = useSession();
  const [activeTab, setActiveTab] = useState('dashboard');
  const { isSidebarOpen, toggleSidebar, isMobile } = useMobileSidebar();
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [mounted, setMounted] = useState(false);
  const [expandedSections, setExpandedSections] = useState<{ [key: string]: boolean }>({});

  // Get user role and permissions
  const userInfo = getUserDisplayInfoFromSession(session?.user);
  const { role, permissions, tenantId, displayName } = userInfo;

  // Define menu items
  // Define menu items
  const allMenuItems = [
    // Overview
    {
      id: 'dashboard',
      icon: Home,
      label: 'Dashboard'
    },

    // AI & Tools
    {
      id: 'ai-assistant',
      icon: Sparkles,
      label: 'AI Agents',
      requiredPermissions: ['ai:use']
    },
    {
      id: 'connectors',
      icon: Plug,
      label: 'Connectors'
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
      id: 'tools',
      icon: Wrench,
      label: 'Tools'
    },
    {
      id: 'get-website',
      icon: Globe,
      label: 'Get Website'
    },

    // Content
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

    // Business
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

    // Account
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
    }
  ];

  const menuItems = filterMenuByPermissions(allMenuItems, permissions);

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

  // renderSidebarItem has been moved to DashboardSidebar component

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

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* GraphQL Powered Widget */}
            <ProjectTasksWidget tenantId={tenantId} />

            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Recent Activity</h3>
                <button className="text-sm text-blue-500 hover:underline">View All</button>
              </div>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 text-xs">AI</div>
                  <div>
                    <p className="text-sm font-medium">Agent "SEO Expert" generated a report</p>
                    <p className="text-xs text-gray-500">2 minutes ago</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-600 text-xs">CRM</div>
                  <div>
                    <p className="text-sm font-medium">New Lead via HubSpot</p>
                    <p className="text-xs text-gray-500">1 hour ago</p>
                  </div>
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
      return <ConnectorsContent />;
    }

    // Handle Tools section
    if (activeTab === 'tools') {
      return <ToolsContent />;
    }

    // Handle Get Website section
    if (activeTab === 'get-website') {
      return <GetWebsiteContent />;
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



    return (
      <div className="flex items-center justify-center h-96 text-gray-500 dark:text-gray-400">
        Content for {activeTab} is coming soon
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex">
      {/* Sidebar */}
      <DashboardSidebar
        menuItems={menuItems}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        userInfo={{ displayName }}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <header className="sticky top-0 z-50 bg-white shadow-sm border-b border-gray-200 dark:bg-gray-900 dark:border-gray-800 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {isMobile && (
                <button
                  onClick={toggleSidebar}
                  className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  <Menu className="w-5 h-5" />
                </button>
              )}
              <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
                {activeTab === 'dashboard' ? 'Dashboard' : activeTab.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </h1>
            </div>
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

export default function ClientPortalDashboard() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center">Loading Dashboard...</div>}>
      <DashboardContent />
    </Suspense>
  );
}