'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import {
  Menu, X, Bell, Moon, Sun, Search,
  Wifi, AlertCircle, CheckCircle, Clock,
  Settings, LogOut, Activity, Home, Zap, Bot, BarChart
} from 'lucide-react';
import ComprehensiveNavigation from './comprehensive-navigation';
import { useSystemStatus } from '../../lib/hooks/useSystemStatus';
import { useAuth } from '../auth/AuthProvider';

import { useTheme } from 'next-themes';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

import { useHeader } from '../../lib/contexts/HeaderContext';

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
  title: propTitle,
  description: propDescription
}) => {
  const { title: contextTitle, description: contextDescription } = useHeader();
  const title = propTitle || contextTitle;
  const description = propDescription || contextDescription;
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout, isLoading } = useAuth();
  // const { user: clerkUser, isLoaded: clerkLoaded } = useUser();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);

  const {
    metrics,
  } = useSystemStatus();

  // Onboarding enforcement - TODO: Re-enable with Authentik
  /*
  useEffect(() => {
    if (!isLoading && user) {
      const onboarded = user.onboarded;
      if (!onboarded && pathname !== '/onboarding') {
        router.replace('/onboarding');
      }
    }
  }, [user, isLoading, pathname, router]);
  */

  // Initialize theme on client side
  useEffect(() => {
    setMounted(true);
    // Set sidebar open by default on tablet/desktop
    if (typeof window !== 'undefined' && window.innerWidth >= 768) {
      setIsSidebarOpen(true);
    }
  }, []);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };


  const toggleSidebar = () => {
    if (window.innerWidth >= 768) {
      setIsCollapsed(!isCollapsed);
    } else {
      setIsSidebarOpen(!isSidebarOpen);
    }
  };

  const BottomNav = () => {
    if (isSidebarOpen && typeof window !== 'undefined' && window.innerWidth < 768) return null;

    return (
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 px-6 py-2 flex justify-between items-center z-50 safe-area-bottom shadow-lg animate-in slide-in-from-bottom duration-300">
        <button onClick={() => router.push('/dashboard')} className={cn("flex flex-col items-center p-2 transition-all", pathname === '/dashboard' ? "text-blue-600 scale-110" : "text-gray-400 hover:text-gray-600")}>
          <Home className="h-5 w-5" />
          <span className="text-[10px] mt-1 font-black uppercase tracking-tighter">Home</span>
        </button>
        <button onClick={() => router.push('/dashboard/workflows')} className={cn("flex flex-col items-center p-2 transition-all", pathname === '/dashboard/workflows' ? "text-blue-600 scale-110" : "text-gray-400 hover:text-gray-600")}>
          <Zap className="h-5 w-5" />
          <span className="text-[10px] mt-1 font-black uppercase tracking-tighter">Work</span>
        </button>
        <button onClick={() => router.push('/dashboard/marketing')} className={cn("flex flex-col items-center p-2 transition-all", pathname === '/dashboard/marketing' ? "text-blue-600 scale-110" : "text-gray-400 hover:text-gray-600")}>
          <BarChart className="h-5 w-5" />
          <span className="text-[10px] mt-1 font-black uppercase tracking-tighter">Growth</span>
        </button>
        <button onClick={() => router.push('/dashboard/ai-assistant')} className={cn("flex flex-col items-center p-2 transition-all", pathname === '/dashboard/ai-assistant' ? "text-blue-600 scale-110" : "text-gray-400 hover:text-gray-600")}>
          <Bot className="h-5 w-5" />
          <span className="text-[10px] mt-1 font-black uppercase tracking-tighter">AI</span>
        </button>
        <button onClick={toggleSidebar} className="flex flex-col items-center p-2 text-gray-400 active:text-blue-600 transition-all">
          <Menu className="h-5 w-5" />
          <span className="text-[10px] mt-1 font-black uppercase tracking-tighter">Menu</span>
        </button>
      </div>
    );
  };

  const cn = (...classes: any[]) => classes.filter(Boolean).join(' ');

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="flex h-screen overflow-hidden">
        {/* Mobile Overlay */}
        {isSidebarOpen && (
          <div
            className="fixed inset-0 bg-black/50 z-20 md:hidden"
            onClick={() => setIsSidebarOpen(false)}
          />
        )}

        {/* Sidebar */}
        <div
          className={`
            fixed inset-y-0 left-0 z-30 bg-white dark:bg-gray-800 shadow-lg transition-all duration-300 transform 
            md:static md:transform-none flex flex-col
            ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
            ${isCollapsed ? 'md:w-20' : 'w-80'}
          `}
        >
          <div className={`p-4 border-b border-gray-200 dark:border-gray-700 ${isCollapsed ? 'px-2 flex flex-col items-center' : ''}`}>
            <div className={`flex items-center justify-between mb-4 ${isCollapsed ? 'flex-col gap-4' : ''}`}>
              {!isCollapsed && (
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/20">
                    <span className="text-white font-black text-xs">B</span>
                  </div>
                  <div className="flex flex-col">
                    <h1 className="font-black text-sm text-gray-900 dark:text-white truncate tracking-tighter uppercase">Bizo Portal</h1>
                    <p className="text-[9px] font-bold text-gray-500 dark:text-gray-400 leading-none">Control v5</p>
                  </div>
                </div>
              )}
              {isCollapsed && (
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-lg flex items-center justify-center text-white font-black text-xl shadow-lg shadow-blue-500/20">
                  B
                </div>
              )}
              <button
                onClick={toggleSidebar}
                className="p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                title={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
              >
                <Menu className={`w-5 h-5 text-gray-600 dark:text-gray-300 ${isSidebarOpen || !isCollapsed ? 'hidden md:block' : 'block'}`} />
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
                  if (window.innerWidth < 768) {
                    setIsSidebarOpen(false);
                  }
                }}
              />
            </Suspense>
          </div>

          <div className="p-4 pb-8 border-t border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/50">
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
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md shadow-sm border-b border-gray-200 dark:border-gray-700 px-4 py-3 z-10">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <button
                  onClick={toggleSidebar}
                  className="p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors md:hidden active:scale-90"
                >
                  <Menu className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                </button>
                <div className="min-w-0">
                  <h1 className="text-base md:text-xl font-black text-gray-900 dark:text-white truncate tracking-tight uppercase">{title}</h1>
                  {description && (
                    <p className="text-[10px] md:text-xs font-bold text-gray-500 dark:text-gray-400 mt-0.5 hidden sm:block line-clamp-1">{description}</p>
                  )}
                </div>
              </div>

              <div className="flex items-center gap-2 sm:gap-4">
                <div className="relative hidden sm:block">
                  <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                  <input
                    type="text"
                    placeholder="Search..."
                    className="pl-10 pr-4 py-2 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent w-40 md:w-60"
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
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <button className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors relative">
                        <Bell className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                        <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white dark:border-gray-800" />
                      </button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-80">
                      <DropdownMenuLabel>Notifications</DropdownMenuLabel>
                      <DropdownMenuSeparator />
                      <div className="max-h-[300px] overflow-y-auto">
                        <DropdownMenuItem className="flex flex-col items-start gap-1 p-4 cursor-pointer">
                          <div className="flex w-full items-center justify-between font-bold">
                            <span className="text-blue-600">New Connector Available</span>
                            <span className="text-[10px] text-muted-foreground">Just now</span>
                          </div>
                          <p className="text-xs text-muted-foreground">"HubSpot CRM" integration is now available for your tier.</p>
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem className="flex flex-col items-start gap-1 p-4 cursor-pointer">
                          <div className="flex w-full items-center justify-between font-bold">
                            <span className="text-green-600">Task Completed</span>
                            <span className="text-[10px] text-muted-foreground">1h ago</span>
                          </div>
                          <p className="text-xs text-muted-foreground">"Q1 Marketing Plan" has been marked as complete.</p>
                        </DropdownMenuItem>
                      </div>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="w-full text-center justify-center font-bold text-blue-600" onClick={() => router.push('/dashboard/support')}>
                        View All
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                  <button
                    onClick={() => router.push('/settings')}
                    className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    <Settings className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto w-full pb-20 md:pb-0">
            {children}
          </div>
          <BottomNav />
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;
