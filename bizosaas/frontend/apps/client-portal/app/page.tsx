'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { 
  Menu, X, Home, Users, ShoppingCart, BarChart3, 
  Settings, Bell, CreditCard, FileText, LinkIcon, 
  ChevronDown, ChevronRight, Moon, Sun, TrendingUp,
  DollarSign, User, Target, Calendar, Package,
  Mail, MessageSquare, Share2, Activity, Zap,
  Lightbulb, Key, Shield, Terminal, Database, Grid, Code
} from 'lucide-react';
import { CRMContent } from '../components/CRMContent';

export default function ClientPortalDashboard() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [theme, setTheme] = useState(() => {
    // Server-safe theme initialization
    if (typeof window === "undefined") return "light";
    try {
      return localStorage.getItem("theme") || "light";
    } catch {
      return "light";
    }
  });
  const [expandedSections, setExpandedSections] = useState<{[key: string]: boolean}>({});

  useEffect(() => {
    // Only run on client side to prevent hydration issues
    if (typeof window === "undefined") return;
    
    try {
      document.documentElement.classList.toggle("dark", theme === "dark");
    } catch (e) {
      console.warn("Cannot set theme class");
    }
    
    setExpandedSections({
      "crm": false,
      "cms": false,
      "ecommerce": false,
      "marketing": false,
      "analytics": false,
      "billing": false,
      "integrations": false,
      "settings": false
    });
  }, [theme]);

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
      icon: Home,
      label: 'Dashboard',
      children: []
    },
    {
      id: 'crm',
      icon: Users,
      label: 'CRM',
      children: [
        { id: 'crm-leads', label: 'Leads', icon: Target },
        { id: 'crm-contacts', label: 'Contacts', icon: User },
        { id: 'crm-deals', label: 'Deals', icon: CreditCard },
        { id: 'crm-activities', label: 'Activities', icon: Calendar },
        { id: 'crm-tasks', label: 'Tasks', icon: Activity },
        { id: 'crm-opportunities', label: 'Opportunities', icon: TrendingUp },
        { id: 'crm-pipeline', label: 'Pipeline', icon: BarChart3 },
        { id: 'crm-reports', label: 'Reports', icon: FileText }
      ]
    },
    {
      id: 'cms',
      icon: FileText,
      label: 'CMS',
      children: [
        { id: 'cms-pages', label: 'Pages', icon: FileText },
        { id: 'cms-posts', label: 'Posts', icon: Package },
        { id: 'cms-media', label: 'Media', icon: Activity },
        { id: 'cms-forms', label: 'Forms', icon: Mail },
        { id: 'cms-templates', label: 'Templates', icon: Code }
      ]
    },
    {
      id: 'ecommerce',
      icon: ShoppingCart,
      label: 'E-commerce',
      children: [
        { id: 'ecom-products', label: 'Products', icon: Package },
        { id: 'ecom-orders', label: 'Orders', icon: ShoppingCart },
        { id: 'ecom-customers', label: 'Customers', icon: Users },
        { id: 'ecom-inventory', label: 'Inventory', icon: BarChart3 },
        { id: 'ecom-coupons', label: 'Coupons', icon: Target },
        { id: 'ecom-reviews', label: 'Reviews', icon: MessageSquare }
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

  const renderSidebarItem = (item: any, level = 0) => {
    const Icon = item.icon;
    const isActive = activeTab === item.id;
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedSections[item.id];

    return (
      <div key={item.id}>
        <button
          onClick={() => {
            if (hasChildren) {
              toggleSection(item.id);
              setActiveTab(item.id);
            } else {
              setActiveTab(item.id);
            }
          }}
          className={`w-full flex items-center px-3 py-2 text-left rounded-lg transition-colors ${
            isActive 
              ? 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400' 
              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
          } ${level > 0 ? 'ml-4' : ''}`}
        >
          <Icon className="w-4 h-4 mr-3 flex-shrink-0" />
          {isSidebarOpen && (
            <>
              <span className="flex-1">{item.label}</span>
              {hasChildren && (
                isExpanded 
                  ? <ChevronDown className="w-4 h-4" />
                  : <ChevronRight className="w-4 h-4" />
              )}
            </>
          )}
        </button>
        {hasChildren && isExpanded && isSidebarOpen && (
          <div className="mt-1 space-y-1">
            {item.children.map((child: any) => renderSidebarItem(child, level + 1))}
          </div>
        )}
      </div>
    );
  };

  // Content rendering functions (no hooks inside)
  const renderSimplePlaceholder = (title: string) => {
    return (
      <div className="text-center py-12">
        <div className="w-16 h-16 mx-auto bg-gray-200 dark:bg-gray-700 rounded-full flex items-center justify-center mb-4">
          <span className="text-gray-500 dark:text-gray-400 text-xl">⚡</span>
        </div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          {title}
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          Content for {title} will be implemented here via FastAPI AI Central Hub integration.
        </p>
      </div>
    );
  };

  const renderCRMContent = () => {
    return <CRMContent activeTab={activeTab} />;
  };

  const renderCMSContent = () => {
    return renderSimplePlaceholder('CMS Management');
  };

  const renderEcommerceContent = () => {
    return renderSimplePlaceholder('E-commerce');
  };

  const renderMarketingContent = () => {
    return renderSimplePlaceholder('Marketing');
  };

  const renderAnalyticsContent = () => {
    return renderSimplePlaceholder('Analytics');
  };

  const renderBillingContent = () => {
    return renderSimplePlaceholder('Billing');
  };

  const renderIntegrationsContent = () => {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Integrations</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                <LinkIcon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Google Analytics</h3>
                <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                  Connected
                </span>
              </div>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">Track website performance and user behavior</p>
            <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">Configure</button>
          </div>

          <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                <Mail className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Mailchimp</h3>
                <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800">
                  Not Connected
                </span>
              </div>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">Sync email marketing campaigns and subscribers</p>
            <button className="w-full bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 py-2 rounded hover:bg-gray-300 dark:hover:bg-gray-600">Connect</button>
          </div>

          <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                <CreditCard className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Stripe</h3>
                <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                  Connected
                </span>
              </div>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">Process payments and manage subscriptions</p>
            <button className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700">Manage</button>
          </div>
        </div>
      </div>
    );
  };

  const renderSettingsContent = () => {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Settings</h2>
        
        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">General Settings</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Company Name</label>
              <input 
                type="text" 
                defaultValue="Acme Corporation" 
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
              <input 
                type="email" 
                defaultValue="admin@acme.com" 
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Time Zone</label>
              <select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
                <option>UTC-5 (Eastern Time)</option>
                <option>UTC-8 (Pacific Time)</option>
                <option>UTC+0 (GMT)</option>
              </select>
            </div>
          </div>
          <div className="mt-6">
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
              Save Changes
            </button>
          </div>
        </div>
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
                  <Users className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Leads</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">1,234</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-green-600 dark:text-green-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Revenue</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">$45,231</p>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                  <ShoppingCart className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Orders</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">892</p>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-orange-600 dark:text-orange-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Growth</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">+12%</p>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Welcome to Your Client Portal</h3>
            <p className="text-gray-600 dark:text-gray-400">
              This is your centralized dashboard for managing all aspects of your business. Use the sidebar to navigate between different sections:
              CRM, E-commerce, Marketing, Analytics, and more. Each section provides powerful tools to help you grow your business.
            </p>
          </div>
        </div>
      );
    }

    // Handle CRM section
    if (activeTab.startsWith('crm')) {
      return renderCRMContent();
    }

    // Handle CMS section
    if (activeTab.startsWith('cms')) {
      return renderCMSContent();
    }

    // Handle E-commerce section
    if (activeTab.startsWith('ecommerce')) {
      return renderEcommerceContent();
    }

    // Handle Marketing section
    if (activeTab.startsWith('marketing')) {
      return renderMarketingContent();
    }

    // Handle Analytics section
    if (activeTab.startsWith('analytics')) {
      return renderAnalyticsContent();
    }

    // Handle Billing section
    if (activeTab.startsWith('billing')) {
      return renderBillingContent();
    }

    // Handle Integrations section
    if (activeTab.startsWith('integrations')) {
      return renderIntegrationsContent();
    }

    // Handle Settings section
    if (activeTab.startsWith('settings')) {
      return renderSettingsContent();
    }

    // For now, show a placeholder for other tabs
    return (
      <div className="text-center py-12">
        <div className="w-16 h-16 mx-auto bg-gray-200 dark:bg-gray-700 rounded-full flex items-center justify-center mb-4">
          <span className="text-gray-500 dark:text-gray-400 text-xl">⚡</span>
        </div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          {activeTab.charAt(0).toUpperCase() + activeTab.slice(1).replace('-', ' ')}
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          Content for {activeTab} will be implemented here via FastAPI AI Central Hub integration.
        </p>
        <div className="max-w-md mx-auto space-y-2">
          <div className="text-sm text-gray-500 dark:text-gray-400">
            API Routes will handle:
          </div>
          <div className="text-xs font-mono bg-gray-100 dark:bg-gray-800 p-2 rounded">
            GET /api/brain/{activeTab.split('-')[0]}/{activeTab.split('-')[1] || 'overview'}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex">
      {/* Sidebar */}
      <div className={`${isSidebarOpen ? 'w-64' : 'w-16'} transition-all duration-300 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col`}>
        {/* Header */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
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
        <nav className="flex-1 p-4 space-y-2">
          {sidebarItems.map((item) => renderSidebarItem(item))}
        </nav>

        {/* User Info */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-800">
          {isSidebarOpen && (
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
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <header className="bg-white shadow-sm border-b border-gray-200 dark:bg-gray-900 dark:border-gray-800 p-4">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
              {activeTab === 'dashboard' ? 'Dashboard' : activeTab.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </h1>
            <div className="flex items-center space-x-4">
              <button 
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors relative"
                title="Notifications"
              >
                <Bell className="w-5 h-5" />
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full text-xs flex items-center justify-center">
                  <span className="w-2 h-2 bg-white rounded-full"></span>
                </span>
              </button>
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
              >
                {theme === 'light' ? (
                  <Moon className="w-5 h-5" />
                ) : (
                  <Sun className="w-5 h-5" />
                )}
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