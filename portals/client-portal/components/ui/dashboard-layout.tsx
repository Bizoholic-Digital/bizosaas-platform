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

  // Auto-close sidebar on mobile when navigating
  useEffect(() => {
    if (window.innerWidth < 1024) {
      setIsSidebarOpen(false);
    }
  }, [pathname]);


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
                  <h1 className="font-black text-xl text-gray-900 dark:text-white truncate tracking-tight underline decoration-purple-500 decoration-2">BizOSaaS <span className="text-xs font-normal text-indigo-500 ml-1 no-underline decoration-0">(Premium)</span></h1>
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
              <ComprehensiveNavigation isCollapsed={isCollapsed} />
            </Suspense>
          </div>

          {/* Sidebar Footer with User Profile & Logout */}
          <div className={`p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/50 ${isCollapsed ? 'flex flex-col items-center' : ''}`}>
            {!isCollapsed ? (
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold border border-blue-400">
                    {user?.name?.[0] || 'G'}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-gray-900 dark:text-white truncate">{user?.name || "Guest User"}</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{user?.email || "Not signed in"}</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={() => router.push('/settings')}
                    className="flex items-center justify-center gap-2 py-2 px-3 text-xs font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md border border-gray-200 dark:border-gray-700 transition-colors"
                  >
                    <Settings className="w-3.5 h-3.5" />
                    Settings
                  </button>
                  <button
                    onClick={() => logout()}
                    className="flex items-center justify-center gap-2 py-2 px-3 text-xs font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-900/10 rounded-md border border-red-100 dark:border-red-900/10 transition-colors"
                  >
                    <LogOut className="w-3.5 h-3.5" />
                    Sign Out
                  </button>
                </div>
              </div>
            ) : (
              <button
                onClick={() => setIsCollapsed(false)}
                className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold border border-blue-400 hover:scale-105 transition-transform"
              >
                {user?.name?.[0] || 'G'}
              </button>
            )}

            {!isCollapsed && (
              <div className="mt-4 flex items-center gap-2 text-[10px] text-gray-400 dark:text-gray-500 uppercase tracking-widest font-bold">
                <Wifi className="w-3 h-3 text-green-500" />
                <span>System Online</span>
                <span className="text-gray-300 dark:text-gray-700">•</span>
                <span className="flex items-center gap-1 text-green-500">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                  </span>
                  Live API
                </span>
              </div>
            )}
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


                <button className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors relative">
                  <Bell className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                </button>

                {/* Action Buttons */}
              </div>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto w-full">
            <Suspense fallback={
              <div className="flex items-center justify-center h-full">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
            }>
              {children}
            </Suspense>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;
