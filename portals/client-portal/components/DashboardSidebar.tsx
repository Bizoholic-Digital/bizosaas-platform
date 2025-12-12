'use client';

import React, { useState } from 'react';
import { LogOut, ChevronDown, ChevronRight, X, Menu, LucideIcon } from 'lucide-react';
import { signOut } from "next-auth/react";
import { useMobileSidebar } from './MobileSidebarContext';

interface MenuItem {
    id: string;
    icon: any; // LucideIcon
    label: string;
    children?: MenuItem[];
    hidden?: boolean;
}

interface DashboardSidebarProps {
    menuItems: MenuItem[];
    activeTab: string;
    setActiveTab: (id: string) => void;
    userInfo: {
        displayName: string;
    };
}

export function DashboardSidebar({
    menuItems,
    activeTab,
    setActiveTab,
    userInfo
}: DashboardSidebarProps) {
    const { isSidebarOpen, toggleSidebar, closeSidebar, isMobile, isTablet, isDesktop } = useMobileSidebar();
    const [expandedSections, setExpandedSections] = useState<{ [key: string]: boolean }>({});

    const toggleSection = (sectionId: string) => {
        setExpandedSections(prev => ({
            ...prev,
            [sectionId]: !prev[sectionId]
        }));
    };

    // Determine actual display state
    // Mobile: drawer behavior (fixed overlay)
    // Desktop/Tablet: relative behavior

    const sidebarClasses = `
    flex flex-col h-full bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 transition-all duration-300
    ${isMobile
            ? `fixed inset-y-0 left-0 z-50 w-64 shadow-xl transform ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}`
            : `${isSidebarOpen ? 'w-64' : 'w-16'} sticky top-0 h-screen`
        }
  `;

    const renderSidebarItem = (item: MenuItem) => {
        const Icon = item.icon;
        const isActive = activeTab === item.id || activeTab.startsWith(item.id + '-');
        const hasChildren = item.children && item.children.length > 0;
        const isExpanded = expandedSections[item.id];

        // In collapsed mode (desktop/tablet only), checking isSidebarOpen
        const isCollapsed = !isMobile && !isSidebarOpen;

        if (item.hidden) return null;

        return (
            <div key={item.id} className="mb-1">
                <button
                    onClick={() => {
                        if (isCollapsed) {
                            // In collapsed mode, clicking main item should probably open sidebar or switch tab?
                            // For now, let's open sidebar if it has children, or switch tab if leaf
                            if (hasChildren) {
                                toggleSidebar(); // Expand sidebar to show children
                                toggleSection(item.id);
                            } else {
                                setActiveTab(item.id);
                            }
                        } else {
                            if (hasChildren) {
                                toggleSection(item.id);
                            } else {
                                setActiveTab(item.id);
                                if (isMobile) closeSidebar();
                            }
                        }
                    }}
                    className={`w-full flex items-center justify-between p-2 rounded-lg transition-colors 
            ${isActive
                            ? 'bg-purple-50 text-purple-600 dark:bg-purple-900/20 dark:text-purple-400'
                            : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                        }
            ${isCollapsed ? 'justify-center' : ''}
          `}
                    title={isCollapsed ? item.label : undefined}
                >
                    <div className={`flex items-center ${isCollapsed ? '' : 'space-x-3'}`}>
                        <Icon className="w-5 h-5 shrink-0" />
                        {!isCollapsed && <span>{item.label}</span>}
                    </div>
                    {!isCollapsed && hasChildren && (
                        isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />
                    )}
                </button>

                {!isCollapsed && hasChildren && isExpanded && (
                    <div className="ml-9 mt-1 space-y-1">
                        {item.children?.map((child: MenuItem) => (
                            <button
                                key={child.id}
                                onClick={() => {
                                    setActiveTab(child.id);
                                    if (isMobile) closeSidebar();
                                }}
                                className={`w-full flex items-center p-2 rounded-lg text-sm transition-colors ${activeTab === child.id
                                    ? 'text-purple-600 dark:text-purple-400 font-medium'
                                    : 'text-gray-500 dark:text-gray-500 hover:text-gray-900 dark:hover:text-gray-300'
                                    }`}
                            >
                                <div className="w-1.5 h-1.5 rounded-full bg-current mr-3 shrink-0" />
                                {child.label}
                            </button>
                        ))}
                    </div>
                )}
            </div>
        );
    };

    return (
        <>
            {/* Mobile Overlay */}
            {isMobile && isSidebarOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-40 backdrop-blur-sm"
                    onClick={closeSidebar}
                />
            )}

            <div className={sidebarClasses}>
                {/* Header */}
                <div className="p-4 border-b border-gray-200 dark:border-gray-800 shrink-0 flex items-center justify-between h-16">
                    {(!isMobile && !isSidebarOpen) ? (
                        <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center mx-auto">
                            <span className="text-white font-bold text-xs">CP</span>
                        </div>
                    ) : (
                        <div className="flex items-center space-x-2">
                            <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                                <span className="text-white font-bold text-sm">CP</span>
                            </div>
                            <div className="min-w-0">
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white truncate">Client Portal</h3>
                                <p className="text-sm text-gray-600 dark:text-gray-400 truncate">BizOSaaS Platform</p>
                            </div>
                        </div>
                    )}

                    {/* Toggle Button - Visible only if NOT mobile (mobile has header toggle) or if sidebar is open on mobile */}
                    {(!isMobile || isSidebarOpen) && (
                        <button
                            onClick={toggleSidebar}
                            className={`p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 ${isMobile ? 'absolute top-4 right-4' : ''}`}
                        >
                            {isSidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
                        </button>
                    )}
                </div>

                {/* Navigation */}
                <nav className="flex-1 p-3 space-y-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-200 dark:scrollbar-thumb-gray-800">
                    {menuItems.map((item) => renderSidebarItem(item))}
                </nav>

                {/* User Info */}
                <div className="p-4 border-t border-gray-200 dark:border-gray-800 shrink-0">
                    {(isMobile || isSidebarOpen) ? (
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3 min-w-0">
                                <div className="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center shrink-0">
                                    <span className="text-white text-sm font-medium">{userInfo.displayName?.[0] || 'U'}</span>
                                </div>
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                                        {userInfo.displayName || 'User'}
                                    </p>
                                    <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                                        Premium Plan
                                    </p>
                                </div>
                            </div>
                            <button
                                onClick={() => signOut({ callbackUrl: '/login' })}
                                className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                                title="Logout"
                            >
                                <LogOut className="w-5 h-5" />
                            </button>
                        </div>
                    ) : (
                        <button
                            onClick={() => signOut({ callbackUrl: '/login' })}
                            className="w-full p-2 flex justify-center text-gray-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                            title="Logout"
                        >
                            <LogOut className="w-5 h-5" />
                        </button>
                    )}
                </div>
            </div>
        </>
    );
}
