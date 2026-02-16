'use client';

import React, { useState, useEffect, createContext, useContext } from 'react';
import {
  ChevronRight, ExternalLink, ArrowLeft, Home, Users, Target,
  ShoppingCart, FileText, BarChart3, Settings, Zap, Globe,
  ArrowUpRight, RefreshCw, CheckCircle, AlertCircle
} from 'lucide-react';

interface PlatformApp {
  id: string;
  name: string;
  description: string;
  url: string;
  port: number;
  icon: React.ComponentType<any>;
  color: string;
  status: 'healthy' | 'warning' | 'error' | 'loading';
  categories: string[];
  features: string[];
}

interface NavigationContext {
  currentApp: string;
  currentPath: string;
  dataContext: any;
  setDataContext: (data: any) => void;
  navigateToApp: (appId: string, path?: string, data?: any) => void;
}

interface DataFlowConnection {
  fromApp: string;
  toApp: string;
  dataType: string;
  status: 'active' | 'inactive' | 'error';
  lastSync: Date;
  recordCount: number;
}

const PLATFORM_APPS: PlatformApp[] = [
  {
    id: 'client-portal',
    name: 'Client Portal',
    description: 'Tenant-specific dashboard and campaign management',
    url: 'http://localhost:3006',
    port: 3006,
    icon: Users,
    color: '#3B82F6',
    status: 'healthy',
    categories: ['dashboard', 'campaigns', 'analytics'],
    features: ['Campaign Wizards', 'Analytics Dashboard', 'User Management']
  },
  {
    id: 'coreldove-frontend',
    name: 'CoreLDove E-commerce',
    description: 'E-commerce storefront and product management',
    url: 'http://localhost:3007',
    port: 3007,
    icon: ShoppingCart,
    color: '#10B981',
    status: 'healthy',
    categories: ['ecommerce', 'products', 'orders'],
    features: ['Product Catalog', 'Order Management', 'Inventory Tracking']
  },
  {
    id: 'bizoholic-frontend',
    name: 'Bizoholic Marketing',
    description: 'Marketing agency website and lead generation',
    url: 'http://localhost:3008',
    port: 3008,
    icon: Target,
    color: '#8B5CF6',
    status: 'healthy',
    categories: ['marketing', 'leads', 'content'],
    features: ['Lead Forms', 'Content Management', 'SEO Tools']
  },
  {
    id: 'bizosaas-admin',
    name: 'BizOSaaS Admin',
    description: 'Platform administration and monitoring',
    url: 'http://localhost:3009',
    port: 3009,
    icon: Settings,
    color: '#F59E0B',
    status: 'healthy',
    categories: ['admin', 'monitoring', 'system'],
    features: ['User Management', 'System Monitoring', 'Configuration']
  }
];

const DATA_FLOWS: DataFlowConnection[] = [
  {
    fromApp: 'bizoholic-frontend',
    toApp: 'client-portal',
    dataType: 'leads',
    status: 'active',
    lastSync: new Date(Date.now() - 5 * 60 * 1000), // 5 minutes ago
    recordCount: 156
  },
  {
    fromApp: 'client-portal',
    toApp: 'coreldove-frontend',
    dataType: 'campaigns',
    status: 'active',
    lastSync: new Date(Date.now() - 10 * 60 * 1000), // 10 minutes ago
    recordCount: 23
  },
  {
    fromApp: 'coreldove-frontend',
    toApp: 'client-portal',
    dataType: 'orders',
    status: 'active',
    lastSync: new Date(Date.now() - 2 * 60 * 1000), // 2 minutes ago
    recordCount: 89
  },
  {
    fromApp: 'client-portal',
    toApp: 'bizosaas-admin',
    dataType: 'analytics',
    status: 'active',
    lastSync: new Date(Date.now() - 1 * 60 * 1000), // 1 minute ago
    recordCount: 1247
  }
];

const NavigationContext = createContext<NavigationContext | null>(null);

export function useNavigation() {
  const context = useContext(NavigationContext);
  if (!context) {
    throw new Error('useNavigation must be used within a CrossPlatformNavigator');
  }
  return context;
}

interface CrossPlatformNavigatorProps {
  children: React.ReactNode;
  currentApp: string;
  currentPath: string;
}

export function CrossPlatformNavigator({ children, currentApp, currentPath }: CrossPlatformNavigatorProps) {
  const [dataContext, setDataContext] = useState<any>({});
  const [isNavigating, setIsNavigating] = useState(false);
  const [appStatuses, setAppStatuses] = useState<Record<string, string>>({});

  // Check app health status
  useEffect(() => {
    const checkAppStatus = async (app: PlatformApp) => {
      try {
        const response = await fetch(`${app.url}/api/health`, {
          method: 'GET',
          timeout: 3000
        });
        
        if (response.ok) {
          setAppStatuses(prev => ({ ...prev, [app.id]: 'healthy' }));
        } else {
          setAppStatuses(prev => ({ ...prev, [app.id]: 'warning' }));
        }
      } catch (error) {
        setAppStatuses(prev => ({ ...prev, [app.id]: 'error' }));
      }
    };

    // Check all apps on mount
    PLATFORM_APPS.forEach(app => {
      if (app.id !== currentApp) {
        checkAppStatus(app);
      } else {
        setAppStatuses(prev => ({ ...prev, [app.id]: 'healthy' }));
      }
    });

    // Set up periodic health checks
    const interval = setInterval(() => {
      PLATFORM_APPS.forEach(app => {
        if (app.id !== currentApp) {
          checkAppStatus(app);
        }
      });
    }, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, [currentApp]);

  const navigateToApp = async (appId: string, path: string = '/', data: any = {}) => {
    if (appId === currentApp) {
      // Same app navigation
      window.history.pushState({}, '', path);
      return;
    }

    setIsNavigating(true);

    try {
      const targetApp = PLATFORM_APPS.find(app => app.id === appId);
      if (!targetApp) {
        throw new Error(`App ${appId} not found`);
      }

      // Store navigation context in sessionStorage for cross-app persistence
      const navigationData = {
        sourceApp: currentApp,
        sourcePath: currentPath,
        targetApp: appId,
        targetPath: path,
        dataContext: { ...dataContext, ...data },
        timestamp: new Date().toISOString()
      };

      sessionStorage.setItem('crossPlatformNavigation', JSON.stringify(navigationData));

      // Build target URL with navigation context
      const targetUrl = new URL(path, targetApp.url);
      targetUrl.searchParams.set('nav', 'cross-platform');
      targetUrl.searchParams.set('source', currentApp);
      if (Object.keys(data).length > 0) {
        targetUrl.searchParams.set('data', btoa(JSON.stringify(data)));
      }

      // Navigate to target app
      window.location.href = targetUrl.toString();
    } catch (error) {
      console.error('Navigation failed:', error);
      alert('Navigation failed. Please try again.');
    } finally {
      setIsNavigating(false);
    }
  };

  const contextValue: NavigationContext = {
    currentApp,
    currentPath,
    dataContext,
    setDataContext,
    navigateToApp
  };

  return (
    <NavigationContext.Provider value={contextValue}>
      <div className="min-h-screen bg-gray-50">
        {/* Cross-Platform Navigation Bar */}
        <nav className="bg-white border-b border-gray-200 px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {/* Platform Logo */}
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <Zap className="text-white" size={16} />
                </div>
                <span className="font-semibold text-gray-900">BizOSaaS</span>
              </div>

              {/* Current App Indicator */}
              <div className="flex items-center space-x-1 text-sm text-gray-500">
                <span>Currently in:</span>
                <span className="font-medium text-gray-900">
                  {PLATFORM_APPS.find(app => app.id === currentApp)?.name || currentApp}
                </span>
              </div>
            </div>

            {/* Quick App Switcher */}
            <div className="flex items-center space-x-2">
              {PLATFORM_APPS.map(app => {
                const Icon = app.icon;
                const isActive = app.id === currentApp;
                const status = appStatuses[app.id] || app.status;

                return (
                  <button
                    key={app.id}
                    onClick={() => !isActive && navigateToApp(app.id)}
                    disabled={isActive || isNavigating}
                    className={`relative flex items-center space-x-2 px-3 py-2 rounded-lg transition-all ${
                      isActive
                        ? 'bg-blue-100 text-blue-700 cursor-default'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    } ${isNavigating ? 'opacity-50 cursor-wait' : ''}`}
                    title={app.description}
                  >
                    <Icon size={16} />
                    <span className="hidden md:inline text-sm">{app.name}</span>
                    
                    {/* Status Indicator */}
                    <div className={`absolute -top-1 -right-1 w-3 h-3 rounded-full border-2 border-white ${
                      status === 'healthy' ? 'bg-green-500' :
                      status === 'warning' ? 'bg-yellow-500' :
                      status === 'error' ? 'bg-red-500' : 'bg-gray-400'
                    }`} />
                  </button>
                );
              })}

              {/* External Link to Admin */}
              <button
                onClick={() => window.open('http://localhost:3009', '_blank')}
                className="flex items-center space-x-1 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-all"
                title="Open Admin in new tab"
              >
                <ExternalLink size={14} />
                <span className="hidden md:inline text-sm">Admin</span>
              </button>
            </div>
          </div>
        </nav>

        {/* Breadcrumb Navigation */}
        <div className="bg-gray-50 border-b border-gray-200 px-4 py-2">
          <div className="flex items-center space-x-2 text-sm">
            <Home size={14} className="text-gray-400" />
            <ChevronRight size={14} className="text-gray-400" />
            <span className="text-gray-600">
              {PLATFORM_APPS.find(app => app.id === currentApp)?.name}
            </span>
            {currentPath !== '/' && (
              <>
                <ChevronRight size={14} className="text-gray-400" />
                <span className="text-gray-900 font-medium">
                  {currentPath.split('/').filter(Boolean).join(' / ')}
                </span>
              </>
            )}
          </div>
        </div>

        {/* Main Content */}
        <main className="flex-1">
          {children}
        </main>

        {/* Cross-Platform Data Flow Status (when relevant) */}
        {Object.keys(dataContext).length > 0 && (
          <div className="fixed bottom-4 right-4 bg-white rounded-lg shadow-lg border border-gray-200 p-4 max-w-sm">
            <h4 className="font-medium text-gray-900 mb-2">Data Context</h4>
            <div className="space-y-1 text-sm">
              {Object.entries(dataContext).map(([key, value]) => (
                <div key={key} className="flex justify-between">
                  <span className="text-gray-600">{key}:</span>
                  <span className="text-gray-900 font-medium">
                    {typeof value === 'object' ? JSON.stringify(value).slice(0, 20) + '...' : String(value)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Navigation Loading Overlay */}
        {isNavigating && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 flex items-center space-x-3">
              <RefreshCw className="animate-spin text-blue-600" size={20} />
              <span className="text-gray-900">Navigating to app...</span>
            </div>
          </div>
        )}
      </div>
    </NavigationContext.Provider>
  );
}

// Data Flow Visualizer Component
export function DataFlowVisualizer() {
  const [selectedFlow, setSelectedFlow] = useState<string | null>(null);

  const getAppPosition = (appId: string): { x: number; y: number } => {
    const positions: Record<string, { x: number; y: number }> = {
      'bizoholic-frontend': { x: 100, y: 100 },
      'client-portal': { x: 300, y: 200 },
      'coreldove-frontend': { x: 500, y: 100 },
      'bizosaas-admin': { x: 300, y: 350 }
    };
    return positions[appId] || { x: 0, y: 0 };
  };

  const formatTimeAgo = (date: Date): string => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900">Cross-Platform Data Flow</h3>
        <div className="flex items-center space-x-4 text-sm text-gray-600">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span>Active</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <span>Error</span>
          </div>
        </div>
      </div>

      {/* Visual Flow Diagram */}
      <div className="relative h-96 mb-6 bg-gray-50 rounded-lg overflow-hidden">
        <svg className="w-full h-full">
          {/* Draw connections */}
          {DATA_FLOWS.map((flow, index) => {
            const fromPos = getAppPosition(flow.fromApp);
            const toPos = getAppPosition(flow.toApp);
            const isSelected = selectedFlow === `${flow.fromApp}-${flow.toApp}`;
            
            return (
              <g key={index}>
                <line
                  x1={fromPos.x + 40}
                  y1={fromPos.y + 20}
                  x2={toPos.x}
                  y2={toPos.y + 20}
                  stroke={flow.status === 'active' ? '#10B981' : '#EF4444'}
                  strokeWidth={isSelected ? 3 : 2}
                  strokeDasharray={flow.status === 'active' ? 'none' : '5,5'}
                  className="cursor-pointer"
                  onClick={() => setSelectedFlow(isSelected ? null : `${flow.fromApp}-${flow.toApp}`)}
                />
                <circle
                  cx={(fromPos.x + toPos.x + 40) / 2}
                  cy={(fromPos.y + toPos.y + 40) / 2}
                  r="4"
                  fill={flow.status === 'active' ? '#10B981' : '#EF4444'}
                  className="cursor-pointer"
                  onClick={() => setSelectedFlow(isSelected ? null : `${flow.fromApp}-${flow.toApp}`)}
                />
              </g>
            );
          })}
          
          {/* Draw apps */}
          {PLATFORM_APPS.map(app => {
            const pos = getAppPosition(app.id);
            const Icon = app.icon;
            
            return (
              <g key={app.id}>
                <rect
                  x={pos.x}
                  y={pos.y}
                  width="80"
                  height="40"
                  rx="8"
                  fill="white"
                  stroke={app.color}
                  strokeWidth="2"
                />
                <foreignObject x={pos.x + 8} y={pos.y + 8} width="24" height="24">
                  <Icon size={16} style={{ color: app.color }} />
                </foreignObject>
                <text
                  x={pos.x + 40}
                  y={pos.y + 28}
                  textAnchor="middle"
                  className="text-xs fill-gray-700"
                >
                  {app.name.split(' ')[0]}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Flow Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {DATA_FLOWS.map((flow, index) => {
          const fromApp = PLATFORM_APPS.find(app => app.id === flow.fromApp);
          const toApp = PLATFORM_APPS.find(app => app.id === flow.toApp);
          const isSelected = selectedFlow === `${flow.fromApp}-${flow.toApp}`;

          return (
            <div
              key={index}
              className={`border rounded-lg p-4 cursor-pointer transition-all ${
                isSelected ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => setSelectedFlow(isSelected ? null : `${flow.fromApp}-${flow.toApp}`)}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-900">{flow.dataType}</span>
                {flow.status === 'active' ? (
                  <CheckCircle size={16} className="text-green-500" />
                ) : (
                  <AlertCircle size={16} className="text-red-500" />
                )}
              </div>
              
              <div className="text-xs text-gray-600 mb-2">
                {fromApp?.name} → {toApp?.name}
              </div>
              
              <div className="space-y-1 text-xs text-gray-500">
                <div className="flex justify-between">
                  <span>Records:</span>
                  <span className="font-medium">{flow.recordCount.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span>Last sync:</span>
                  <span className="font-medium">{formatTimeAgo(flow.lastSync)}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// Quick Actions Component for Cross-Platform Operations
export function QuickActions() {
  const navigation = useNavigation();

  const quickActions = [
    {
      id: 'create-campaign',
      title: 'Create Campaign',
      description: 'Start a new marketing campaign',
      icon: Target,
      action: () => navigation.navigateToApp('client-portal', '/campaigns/new'),
      color: '#3B82F6'
    },
    {
      id: 'view-orders',
      title: 'View Orders',
      description: 'Check recent e-commerce orders',
      icon: ShoppingCart,
      action: () => navigation.navigateToApp('coreldove-frontend', '/orders'),
      color: '#10B981'
    },
    {
      id: 'manage-leads',
      title: 'Manage Leads',
      description: 'Review and process leads',
      icon: Users,
      action: () => navigation.navigateToApp('bizoholic-frontend', '/leads'),
      color: '#8B5CF6'
    },
    {
      id: 'view-analytics',
      title: 'View Analytics',
      description: 'Check platform performance',
      icon: BarChart3,
      action: () => navigation.navigateToApp('bizosaas-admin', '/analytics'),
      color: '#F59E0B'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {quickActions.map(action => {
        const Icon = action.icon;
        return (
          <button
            key={action.id}
            onClick={action.action}
            className="flex items-center space-x-3 p-4 bg-white border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all text-left"
          >
            <div 
              className="w-10 h-10 rounded-lg flex items-center justify-center"
              style={{ backgroundColor: action.color + '20' }}
            >
              <Icon size={20} style={{ color: action.color }} />
            </div>
            <div>
              <h4 className="font-medium text-gray-900">{action.title}</h4>
              <p className="text-sm text-gray-600">{action.description}</p>
            </div>
            <ArrowUpRight size={16} className="text-gray-400" />
          </button>
        );
      })}
    </div>
  );
}