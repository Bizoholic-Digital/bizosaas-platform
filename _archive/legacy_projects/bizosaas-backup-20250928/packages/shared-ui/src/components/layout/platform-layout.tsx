'use client';

import React, { useState } from 'react';
import { Menu, X, Bell, User, Settings, LogOut } from 'lucide-react';
import { PlatformBranding } from '../branding/platform-branding';
import { PlatformNavigation } from '../navigation/platform-navigation';
import { useAuth } from '../../lib/auth/auth-context';
import type { PlatformBrand } from '../../lib/constants/branding';

interface PlatformLayoutProps {
  platform: PlatformBrand;
  children: React.ReactNode;
  showSidebar?: boolean;
  sidebarCollapsed?: boolean;
  onSidebarToggle?: () => void;
}

export function PlatformLayout({
  platform,
  children,
  showSidebar = true,
  sidebarCollapsed = false,
  onSidebarToggle
}: PlatformLayoutProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const { user, logout } = useAuth();

  const handleSidebarToggle = () => {
    if (onSidebarToggle) {
      onSidebarToggle();
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      {/* Mobile menu backdrop */}
      {mobileMenuOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      {showSidebar && (
        <>
          {/* Desktop sidebar */}
          <div className={`
            fixed left-0 top-0 z-50 h-full bg-white shadow-lg border-r border-gray-200 transition-all duration-300 dark:bg-gray-900 dark:border-gray-800
            ${sidebarCollapsed ? 'w-16' : 'w-64'}
            hidden lg:block
          `}>
            <div className="flex h-full flex-col">
              {/* Sidebar header */}
              <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800">
                <PlatformBranding 
                  platform={platform} 
                  variant={sidebarCollapsed ? 'logo' : 'full'}
                  size="md"
                />
                {!sidebarCollapsed && (
                  <button
                    onClick={handleSidebarToggle}
                    className="p-1 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800"
                  >
                    <Menu className="w-5 h-5" />
                  </button>
                )}
              </div>

              {/* Navigation */}
              <div className="flex-1 overflow-y-auto">
                <PlatformNavigation 
                  platform={platform} 
                  collapsed={sidebarCollapsed}
                  onItemClick={() => setMobileMenuOpen(false)}
                />
              </div>

              {/* User info (if not collapsed) */}
              {!sidebarCollapsed && user && (
                <div className="p-4 border-t border-gray-200 dark:border-gray-800">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                      <User className="w-4 h-4 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                        {user.firstName} {user.lastName}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                        {user.email}
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Mobile sidebar */}
          <div className={`
            fixed left-0 top-0 z-50 h-full w-64 bg-white shadow-lg border-r border-gray-200 transition-transform duration-300 dark:bg-gray-900 dark:border-gray-800
            ${mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
            lg:hidden
          `}>
            <div className="flex h-full flex-col">
              {/* Mobile sidebar header */}
              <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800">
                <PlatformBranding platform={platform} variant="full" size="md" />
                <button
                  onClick={() => setMobileMenuOpen(false)}
                  className="p-1 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Mobile navigation */}
              <div className="flex-1 overflow-y-auto">
                <PlatformNavigation 
                  platform={platform} 
                  onItemClick={() => setMobileMenuOpen(false)}
                />
              </div>
            </div>
          </div>
        </>
      )}

      {/* Main content */}
      <div className={`
        ${showSidebar 
          ? sidebarCollapsed 
            ? 'lg:ml-16' 
            : 'lg:ml-64' 
          : ''
        }
      `}>
        {/* Top header */}
        <header className="sticky top-0 z-30 bg-white/80 backdrop-blur-md border-b border-gray-200 dark:bg-gray-900/80 dark:border-gray-800">
          <div className="px-4 sm:px-6 lg:px-8">
            <div className="flex h-16 items-center justify-between">
              {/* Left side */}
              <div className="flex items-center space-x-4">
                {/* Mobile menu button */}
                {showSidebar && (
                  <button
                    onClick={() => setMobileMenuOpen(true)}
                    className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 lg:hidden"
                  >
                    <Menu className="w-5 h-5" />
                  </button>
                )}

                {/* Desktop collapse button */}
                {showSidebar && (
                  <button
                    onClick={handleSidebarToggle}
                    className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 hidden lg:block"
                  >
                    <Menu className="w-5 h-5" />
                  </button>
                )}

                {/* Platform branding for no-sidebar layouts */}
                {!showSidebar && (
                  <PlatformBranding platform={platform} variant="full" size="md" />
                )}
              </div>

              {/* Right side */}
              <div className="flex items-center space-x-4">
                {/* Notifications */}
                <button className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
                  <Bell className="w-5 h-5" />
                </button>

                {/* User menu */}
                {user && (
                  <div className="relative">
                    <button
                      onClick={() => setUserMenuOpen(!userMenuOpen)}
                      className="flex items-center space-x-2 p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800"
                    >
                      <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                        <User className="w-4 h-4 text-white" />
                      </div>
                      <span className="hidden sm:block text-sm font-medium">
                        {user.firstName}
                      </span>
                    </button>

                    {/* User dropdown */}
                    {userMenuOpen && (
                      <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 dark:bg-gray-800 dark:border-gray-700">
                        <div className="py-1">
                          <button className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700">
                            <Settings className="w-4 h-4 mr-3" />
                            Settings
                          </button>
                          <button 
                            onClick={handleLogout}
                            className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
                          >
                            <LogOut className="w-4 h-4 mr-3" />
                            Sign out
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </header>

        {/* Main content area */}
        <main className="flex-1">
          {children}
        </main>
      </div>
    </div>
  );
}