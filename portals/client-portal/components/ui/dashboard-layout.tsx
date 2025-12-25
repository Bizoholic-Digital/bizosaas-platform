'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import {
  Menu, X, Bell, Moon, Search,
  Wifi, AlertCircle, CheckCircle, Clock,
  Settings, LogOut, Activity
} from 'lucide-react';
import ComprehensiveNavigation from './comprehensive-navigation';
import { useSystemStatus } from '../../lib/hooks/useSystemStatus';
import { useAuth } from '../auth/AuthProvider';

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
  const [theme, setTheme] = useState("light");
  const [showUserMenu, setShowUserMenu] = useState(false);
  const {
    metrics,
  } = useSystemStatus();

  // Initialize theme on client side
  useEffect(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("theme") || "light";
      setTheme(saved);
      document.documentElement.classList.toggle("dark", saved === "dark");
    }
    // Set sidebar open by default on desktop
    if (typeof window !== 'undefined' && window.innerWidth >= 1024) {
      setIsSidebarOpen(true);
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    try {
      localStorage.setItem('theme', newTheme);
      document.documentElement.classList.toggle('dark', newTheme === 'dark');
    } catch (e) {
      console.warn('localStorage not available');
    }
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
              <ComprehensiveNavigation isCollapsed={isCollapsed} />
            </Suspense>
          </div>

          <div className="p-6 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
              <Wifi className="w-3 h-3 text-green-500" />
              <span>Online</span>
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
                  <Moon className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                </button>

                <button className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors relative">
                  <Bell className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                </button>

                <div className="relative" data-user-menu>
                  <button
                    onClick={() => setShowUserMenu(!showUserMenu)}
                    className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    <div className="text-right hidden sm:block">
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {user?.name || "Guest User"}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        {user?.email || "Not signed in"}
                      </p>
                    </div>
                    <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                      {user?.name?.[0] || "G"}
                    </div>
                  </button>

                  {showUserMenu && (
                    <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-gray-800 rounded-lg shadow-lg py-1 border border-gray-200 dark:border-gray-700 z-50">
                      <div className="px-4 py-2 border-b border-gray-200 dark:border-gray-700">
                        <p className="text-sm font-medium text-gray-900 dark:text-white">{user?.name || 'Guest User'}</p>
                        <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{user?.email || 'Not signed in'}</p>
                      </div>
                      <button
                        onClick={() => router.push('/settings')}
                        className="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2"
                      >
                        <Settings className="w-4 h-4" />
                        Settings
                      </button>
                      <button
                        onClick={() => {
                          logout();
                          setShowUserMenu(false);
                        }}
                        className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/10 flex items-center gap-2"
                      >
                        <LogOut className="w-4 h-4" />
                        Sign Out
                      </button>
                    </div>
                  )}
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
