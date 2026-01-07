'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import {
  Menu, X, Bell, Moon, Sun, Search,
  Wifi, AlertCircle, CheckCircle, Clock,
  Settings, LogOut, Activity
} from 'lucide-react';
import ComprehensiveNavigation from './comprehensive-navigation';
import { useSystemStatus } from '../../lib/hooks/useSystemStatus';
import { useAuth } from '../auth/AuthProvider';
import { useTheme } from 'next-themes';


interface DashboardLayoutProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
}

const StatusIcon = ({ status }: { status?: string }) => {
  if (status === 'down') return <AlertCircle className="w-3 h-3 text-red-500" />;
  if (status === 'degraded') return <Activity className="w-3 h-3 text-yellow-500" />;
  if (status === 'healthy') return <CheckCircle className="w-3 h-3 text-green-500" />;
  return <Clock className="w-3 h-3 text-gray-400" />;
};

const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  title,
  description
}) => {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);

  const {
    metrics,
  } = useSystemStatus();

  // Initialize theme on client side
  useEffect(() => {
    setMounted(true);
    // Set sidebar open by default on desktop
    if (typeof window !== 'undefined' && window.innerWidth >= 1024) {
      setIsSidebarOpen(true);
    }
  }, []);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };


  const toggleSidebar = () => {
    if (window.innerWidth >= 1024) {
      setIsCollapsed(!isCollapsed);
    } else {
      setIsSidebarOpen(!isSidebarOpen);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="flex h-screen overflow-hidden">
        {/* Mobile Overlay */}
        {isSidebarOpen && (
          <div
            className="fixed inset-0 bg-black/50 z-20 lg:hidden"
            onClick={() => setIsSidebarOpen(false)}
          />
        )}

        {/* Sidebar */}
        <div
          className={`
            fixed inset-y-0 left-0 z-30 bg-white dark:bg-gray-800 shadow-lg transition-all duration-300 transform 
            lg:static lg:transform-none flex flex-col
            ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
            ${isCollapsed ? 'lg:w-20' : 'w-80'}
          `}
        >
          <div className={`p-6 border-b border-gray-200 dark:border-gray-700 ${isCollapsed ? 'px-2 flex flex-col items-center' : ''}`}>
            <div className={`flex items-center justify-between mb-6 ${isCollapsed ? 'flex-col gap-4' : ''}`}>
              {!isCollapsed && (
                <div>
                  <h1 className="font-bold text-xl text-gray-900 dark:text-white truncate">BizOSaaS</h1>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Portal Control</p>
                </div>
              )}
              {isCollapsed && (
                <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                  B
                </div>
              )}
              <button
                onClick={toggleSidebar}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                title={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
              >
                {isSidebarOpen || !isCollapsed ? <X className="w-5 h-5 text-gray-600 dark:text-gray-300 lg:hidden" /> : null}
                <Menu className={`w-5 h-5 text-gray-600 dark:text-gray-300 ${isSidebarOpen || !isCollapsed ? 'hidden lg:block' : 'block'}`} />
              </button>
            </div>

            {!isCollapsed && (
              <div className="mb-4">
                <button
                  onClick={() => router.push('/dashboard/system-status')}
                  className="w-full text-left hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg p-2 transition-colors group"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <Activity className="w-4 h-4 text-gray-400 group-hover:text-blue-500 transition-colors" />
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">System Status</span>
                    </div>
                    <div className={`w-2 h-2 rounded-full ${metrics?.status === 'down' ? 'bg-red-500' :
                      metrics?.status === 'degraded' ? 'bg-yellow-500' :
                        'bg-green-500'
                      }`} />
                  </div>
                </button>
              </div>
            )}
          </div>

          <div className={`flex-1 overflow-y-auto p-4 ${isCollapsed ? 'px-2' : 'p-6'}`}>
            <Suspense fallback={
              <div className="animate-pulse space-y-2">
                {[...Array(8)].map((_, i) => (
                  <div key={i} className={`h-10 bg-gray-200 dark:bg-gray-700 rounded ${isCollapsed ? 'w-10 mx-auto' : ''}`}></div>
                ))}
              </div>
            }>
              <ComprehensiveNavigation
                isCollapsed={isCollapsed}
                onNavigate={() => {
                  if (window.innerWidth < 1024) {
                    setIsSidebarOpen(false);
                  }
                }}
              />
            </Suspense>
          </div>

          <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/50">
            <div className={`flex flex-col gap-4 ${isCollapsed ? 'items-center' : ''}`}>
              <div className={`flex items-center justify-between w-full ${isCollapsed ? 'flex-col gap-2' : ''}`}>
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-10 h-10 rounded-full bg-blue-600 flex-shrink-0 flex items-center justify-center text-white font-bold shadow-sm border-2 border-white dark:border-gray-700">
                    {user?.name?.[0] || user?.email?.[0]?.toUpperCase() || 'B'}
                  </div>
                  {!isCollapsed && (
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-bold text-gray-900 dark:text-white truncate leading-tight">
                        {user?.name || "Bizoholic Digital"}
                      </p>
                      <p className="text-[11px] text-gray-500 dark:text-gray-400 truncate mt-0.5">
                        {user?.email || "bizoholic.digital@gmail.com"}
                      </p>
                    </div>
                  )}
                </div>

                {!isCollapsed && (
                  <div className="flex flex-shrink-0 items-center gap-1.5 px-2 py-1 rounded-full bg-green-50 dark:bg-green-900/20 border border-green-100 dark:border-green-900/30">
                    <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                    <span className="text-[10px] font-bold text-green-700 dark:text-green-400 uppercase tracking-widest">Online</span>
                  </div>
                )}
              </div>

              <button
                onClick={() => logout()}
                className={`flex items-center justify-center gap-2 text-sm font-semibold transition-all duration-200
                  ${isCollapsed
                    ? 'p-2.5 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/10 rounded-xl'
                    : 'w-full px-4 py-2.5 text-red-600 bg-red-50 hover:bg-red-100 dark:bg-red-900/10 dark:hover:bg-red-900/20 rounded-xl border border-red-100 dark:border-red-900/20'
                  }`}
                title={isCollapsed ? "Sign Out" : ""}
              >
                <LogOut className={isCollapsed ? "w-5 h-5" : "w-4 h-4"} />
                {!isCollapsed && <span>Sign Out</span>}
              </button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
          <div className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <button
                  onClick={toggleSidebar}
                  className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors lg:hidden"
                >
                  <Menu className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                </button>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900 dark:text-white truncate">{title}</h1>
                  {description && (
                    <p className="text-gray-600 dark:text-gray-300 mt-1 hidden sm:block">{description}</p>
                  )}
                </div>
              </div>

              <div className="flex items-center gap-2 sm:gap-4">
                <div className="relative hidden sm:block">
                  <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                  <input
                    type="text"
                    placeholder="Search..."
                    className="pl-10 pr-4 py-2 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent w-40 lg:w-60"
                  />
                </div>

                <button
                  onClick={toggleTheme}
                  className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  {mounted && theme === 'dark' ? (
                    <Sun className="w-5 h-5 text-gray-300" />
                  ) : (
                    <Moon className="w-5 h-5 text-gray-600" />
                  )}
                </button>

                {/* Header Actions */}
                <div className="flex items-center gap-2">
                  <button className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors relative">
                    <Bell className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                    <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white dark:border-gray-800" />
                  </button>
                  <button className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                    <Settings className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto w-full">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;
