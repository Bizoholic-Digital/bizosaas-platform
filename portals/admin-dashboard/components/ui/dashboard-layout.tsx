'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import {
  Menu, X, Bell, User, Moon, Sun, Search, RefreshCw,
  Wifi, AlertCircle, CheckCircle, Clock,
  Settings, LogOut, Activity, Download, Bot, Sparkles
} from 'lucide-react';
import ComprehensiveNavigation from '@/components/ui/comprehensive-navigation';
import ErrorBoundary from '@/components/error-boundary';
import { useSystemStatus } from '@/lib/hooks/useSystemStatus';
import { useAuth } from '@/shared/components/AuthProvider';
import { useTheme } from 'next-themes';
import { usePWAInstall } from '@/components/PWAInstallPrompt';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';

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
  const router = useRouter();
  const { user, logout } = useAuth();
  const { showInstallButton, install } = usePWAInstall();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const {
    metrics,
    isLoading: statusLoading,
    error: statusError,
    refreshStatus,
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

  const BottomNav = () => (
    <div className="lg:hidden fixed bottom-0 left-0 right-0 bg-white/80 dark:bg-gray-800/80 backdrop-blur-md border-t border-gray-200 dark:border-gray-700 px-6 py-2 flex justify-between items-center z-50 safe-area-bottom shadow-lg">
      <button onClick={() => router.push('/dashboard')} className={cn("flex flex-col items-center p-2 transition-all", pathname === '/dashboard' ? "text-blue-600 scale-110" : "text-gray-400 hover:text-gray-600")}>
        <Activity className="h-5 w-5" />
        <span className="text-[10px] mt-1 font-black uppercase tracking-tighter">Status</span>
      </button>
      <button onClick={() => router.push('/dashboard/agent-management')} className={cn("flex flex-col items-center p-2 transition-all", pathname === '/dashboard/agent-management' ? "text-blue-600 scale-110" : "text-gray-400 hover:text-gray-600")}>
        <Bot className="h-5 w-5" />
        <span className="text-[10px] mt-1 font-black uppercase tracking-tighter">Agents</span>
      </button>
      <button onClick={() => router.push('/dashboard/ai-assistant')} className={cn("flex flex-col items-center p-2 transition-all", pathname === '/dashboard/ai-assistant' ? "text-blue-600 scale-110" : "text-gray-400 hover:text-gray-600")}>
        <Sparkles className="h-5 w-5" />
        <span className="text-[10px] mt-1 font-black uppercase tracking-tighter">AI</span>
      </button>
      <button onClick={() => router.push('/dashboard/settings')} className={cn("flex flex-col items-center p-2 transition-all", pathname === '/dashboard/settings' ? "text-blue-600 scale-110" : "text-gray-400 hover:text-gray-600")}>
        <Settings className="h-5 w-5" />
        <span className="text-[10px] mt-1 font-black uppercase tracking-tighter">Config</span>
      </button>
      <button onClick={toggleSidebar} className="flex flex-col items-center p-2 text-gray-400 active:text-blue-600 transition-all">
        <Menu className="h-5 w-5" />
        <span className="text-[10px] mt-1 font-black uppercase tracking-tighter">Menu</span>
      </button>
    </div>
  );

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
                  <h1 className="font-black text-2xl text-slate-900 dark:text-white truncate uppercase italic tracking-tighter">
                    BizOS <span className="text-indigo-600">Admin</span>
                  </h1>
                  <p className="text-[10px] text-slate-500 dark:text-slate-400 uppercase font-bold tracking-[0.2em] mt-0.5">Core Control System</p>
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
              <div className="mb-6 space-y-4">
                <button
                  onClick={() => router.push('/dashboard/infrastructure')}
                  className="w-full text-left bg-slate-50 dark:bg-slate-900/50 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 rounded-xl p-3 border border-slate-100 dark:border-slate-800 transition-all group"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <Activity className="w-4 h-4 text-indigo-500" />
                      <span className="text-xs font-black uppercase tracking-wider text-slate-700 dark:text-slate-300">Platform Health</span>
                    </div>
                    <div className={`w-2 h-2 rounded-full shadow-[0_0_8px_rgba(34,197,94,0.5)] ${metrics?.status === 'down' ? 'bg-red-500' :
                      metrics?.status === 'degraded' ? 'bg-yellow-500' :
                        'bg-green-500'
                      }`} />
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between items-center text-[10px] font-bold">
                      <span className="text-slate-500">CPU LOAD</span>
                      <span className="text-indigo-600 dark:text-indigo-400">{metrics?.cpu || 0}%</span>
                    </div>
                    <Progress value={metrics?.cpu || 0} className="h-1 bg-slate-200 dark:bg-slate-800" indicatorClassName="bg-indigo-600" />
                  </div>

                  <div className="grid grid-cols-2 gap-2 mt-4 pt-3 border-t border-slate-100 dark:border-slate-800">
                    <div className="flex items-center gap-1.5">
                      <div className="w-1.5 h-1.5 rounded-full bg-green-500" />
                      <span className="text-[9px] font-black uppercase text-slate-400">Gateway</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div className="w-1.5 h-1.5 rounded-full bg-green-500" />
                      <span className="text-[9px] font-black uppercase text-slate-400">Database</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                      <span className="text-[9px] font-black uppercase text-slate-400">AI Core</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div className="w-1.5 h-1.5 rounded-full bg-green-500" />
                      <span className="text-[9px] font-black uppercase text-slate-400">Vault</span>
                    </div>
                  </div>
                </button>
              </div>
            )}
          </div>

          <div className={`flex-1 overflow-y-auto ${isCollapsed ? 'px-2' : 'p-4'}`}>
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
                  <div className="w-10 h-10 rounded-full bg-indigo-600 flex-shrink-0 flex items-center justify-center text-white font-bold shadow-sm border-2 border-white dark:border-gray-700">
                    {user?.name?.[0] || user?.email?.[0]?.toUpperCase() || 'A'}
                  </div>
                  {!isCollapsed && (
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-bold text-gray-900 dark:text-white truncate leading-tight">
                        {user?.name || "Admin User"}
                      </p>
                      <p className="text-[11px] text-gray-500 dark:text-gray-400 truncate mt-0.5">
                        {user?.email || "admin@bizosaas.com"}
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
          <div className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 px-4 md:px-6 py-4">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-3 md:gap-4 min-w-0">
                <button
                  onClick={toggleSidebar}
                  className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors lg:hidden shrink-0"
                >
                  <Menu className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                </button>
                <div className="hidden lg:block min-w-0">
                  <h1 className="text-xl md:text-2xl font-bold text-gray-900 dark:text-white truncate">{title}</h1>
                  {description && (
                    <p className="text-gray-600 dark:text-gray-300 mt-1 hidden lg:block truncate">{description}</p>
                  )}
                </div>
              </div>

              <div className="flex items-center gap-2 sm:gap-4">
                {showInstallButton && (
                  <button
                    onClick={install}
                    className="flex items-center gap-2 px-3 py-2 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-lg transition-all hover:bg-blue-100 dark:hover:bg-blue-800/50 border border-blue-100 dark:border-blue-800/50 animate-pulse-subtle"
                    title="Install Application"
                  >
                    <Download className="w-5 h-5" />
                    <span className="text-sm font-bold hidden md:inline">Install App</span>
                  </button>
                )}

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

                <div className="flex items-center gap-2">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <button className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors relative">
                        <Bell className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                        <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white dark:border-gray-800" />
                      </button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-80">
                      <DropdownMenuLabel>System Notifications</DropdownMenuLabel>
                      <DropdownMenuSeparator />
                      <div className="max-h-[300px] overflow-y-auto">
                        <DropdownMenuItem className="flex flex-col items-start gap-1 p-4 cursor-pointer">
                          <div className="flex w-full items-center justify-between font-bold">
                            <span className="text-red-600">High CPU Load</span>
                            <span className="text-[10px] text-muted-foreground">Just now</span>
                          </div>
                          <p className="text-xs text-muted-foreground">KVM2 Server is experiencing high CPU usage on "ai-agents" container.</p>
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem className="flex flex-col items-start gap-1 p-4 cursor-pointer">
                          <div className="flex w-full items-center justify-between font-bold">
                            <span className="text-yellow-600">New Tenant Signup</span>
                            <span className="text-[10px] text-muted-foreground">15m ago</span>
                          </div>
                          <p className="text-xs text-muted-foreground">"Global Logistics Inc" has just finished onboarding.</p>
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem className="flex flex-col items-start gap-1 p-4 cursor-pointer">
                          <div className="flex w-full items-center justify-between font-bold">
                            <span className="text-green-600">Backup Successful</span>
                            <span className="text-[10px] text-muted-foreground">2h ago</span>
                          </div>
                          <p className="text-xs text-muted-foreground">Full platform backup has been completed and synced to S3.</p>
                        </DropdownMenuItem>
                      </div>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="w-full text-center justify-center font-bold text-indigo-600">
                        View Audit Log
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                  <button className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                    <Settings className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto w-full pb-20 lg:pb-0">
            {children}
          </div>
          <BottomNav />
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;
