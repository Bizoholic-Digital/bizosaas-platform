'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { usePathname } from 'next/navigation';
import {
  Menu, X, Bell, User, Moon, Sun, Search, RefreshCw,
  Wifi, WifiOff, AlertCircle, CheckCircle, Clock,
  Settings, LogOut, HelpCircle, Zap, Activity
} from 'lucide-react';
import ComprehensiveNavigation from './comprehensive-navigation';
import { AIAssistant } from '../ai-assistant/AIAssistant';
import ErrorBoundary from '../error-boundary';
import { useSystemStatus } from '../../lib/hooks/useSystemStatus';
import { useAuth } from '../auth/AuthProvider';

interface DashboardLayoutProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
}



const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  title,
  description
}) => {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [theme, setTheme] = useState(() => {
    if (typeof window === "undefined") return "light";
    try {
      return localStorage.getItem("theme") || "light";
    } catch {
      return "light";
    }
  });
  const [showUserMenu, setShowUserMenu] = useState(false);
  const {
    metrics,
    isLoading: statusLoading,
    error: statusError
  } = useSystemStatus();

  const refreshStatus = () => {
    // Trigger re-fetch by forcing component update
    window.location.reload();
  };
  const [isOnline, setIsOnline] = useState(true);

  // Close user menu when clicking outside

  // Initialize theme on client side
  useEffect(() => {
    if (typeof window === "undefined") return;

    const savedTheme = theme;
    try {
      document.documentElement.classList.toggle("dark", savedTheme === "dark");
    } catch (e) {
      console.warn("Cannot set theme class");
    }
  }, [theme]);



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

  const getPageTitle = () => {
    if (title) return title;

    const pathSegments = pathname.split('/').filter(Boolean);
    if (pathSegments.length === 0) return 'Dashboard';

    return pathSegments
      .map(segment => segment.charAt(0).toUpperCase() + segment.slice(1))
      .join(' › ');
  };


  // Debug logging

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex h-screen">
        <div className="dashboard-sidebar w-80 bg-white dark:bg-gray-800 shadow-lg transition-all duration-300 flex flex-col" style={{ minHeight: "100vh" }}>
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-6">
              <div className="false">
                <h1 className="font-bold text-xl text-gray-900 dark:text-white">BizOSaaS Portal</h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">Multi-Service Dashboard</p>
              </div>
              <button
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <Menu className="w-5 h-5 text-gray-600 dark:text-gray-300" />
              </button>
            </div>

            <div className="mb-4">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="w-4 h-4 text-gray-400 animate-pulse" />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">System Status</span>
                <button
                  onClick={refreshStatus}
                  className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <RefreshCw className="w-3 h-3 text-gray-500" />
                </button>
              </div>
              <div className="grid grid-cols-2 gap-1 text-xs">
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4 text-gray-400 animate-pulse" />
                  <span>Brain Hub</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4 text-gray-400 animate-pulse" />
                  <span>CRM</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4 text-gray-400 animate-pulse" />
                  <span>CMS</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4 text-gray-400 animate-pulse" />
                  <span>E-commerce</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-6">
            <Suspense fallback={
              <div className="animate-pulse space-y-2">
                {[...Array(8)].map((_, i) => (
                  <div key={i} className="h-10 bg-gray-200 dark:bg-gray-700 rounded"></div>
                ))}
              </div>
            }>
              <ComprehensiveNavigation />
            </Suspense>
          </div>

          <div className="p-6 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
              <Wifi className="w-3 h-3 text-green-500" />
              <span>Online</span>
              <span className="ml-auto">Updated: Loading...</span>
            </div>
          </div>
        </div>

        <div className="dashboard-main-content flex-1 flex flex-col overflow-hidden">
          <div className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{title}</h1>
                {description && (
                  <p className="text-gray-600 dark:text-gray-300 mt-1">{description}</p>
                )}
              </div>
              <div className="flex items-center gap-4">
                <div className="relative">
                  <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                  <input
                    type="text"
                    placeholder="Search..."
                    className="pl-10 pr-4 py-2 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {user?.name || "Loading..."}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        {user?.email || "user@bizosaas.com"}
                      </p>
                    </div>
                    <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                      <User className="w-4 h-4 text-white" />
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;
