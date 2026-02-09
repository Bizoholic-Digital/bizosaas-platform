'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import DashboardLayout from '../ui/dashboard-layout';
import { User, Bell, Lock, Palette, Globe, Key, ChevronLeft } from 'lucide-react';

interface SettingsLayoutProps {
    children: React.ReactNode;
    title: string;
    description: string;
}

const SettingsLayout: React.FC<SettingsLayoutProps> = ({ children, title, description }) => {
    const pathname = usePathname();

    const tabs = [
        { id: 'profile', label: 'Profile', href: '/settings/profile', icon: <User className="w-4 h-4" /> },
        { id: 'notifications', label: 'Notifications', href: '/settings/notifications', icon: <Bell className="w-4 h-4" /> },
        { id: 'security', label: 'Security', href: '/settings/security', icon: <Lock className="w-4 h-4" /> },
        { id: 'appearance', label: 'Appearance', href: '/settings/appearance', icon: <Palette className="w-4 h-4" /> },
        { id: 'localization', label: 'Localization', href: '/settings/localization', icon: <Globe className="w-4 h-4" /> },
        { id: 'integrations', label: 'Advanced', href: '/settings/integrations', icon: <Key className="w-4 h-4" /> },
    ];

    return (
        <DashboardLayout title="Settings" description="Manage your account and preferences">
            <div className="p-4 md:p-6 max-w-6xl mx-auto">
                <div className="mb-6 flex items-center justify-between">
                    <div>
                        <Link href="/settings" className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1 mb-2">
                            <ChevronLeft className="w-4 h-4" />
                            Back to Settings
                        </Link>
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{title}</h2>
                        <p className="text-gray-500 dark:text-gray-400">{description}</p>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                    {/* Sidebar Tabs */}
                    <div className="md:col-span-1 space-y-1">
                        {tabs.map((tab) => (
                            <Link
                                key={tab.id}
                                href={tab.href}
                                className={`flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg transition-colors ${pathname === tab.href
                                        ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 border border-blue-100 dark:border-blue-800'
                                        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'
                                    }`}
                            >
                                {tab.icon}
                                {tab.label}
                            </Link>
                        ))}
                    </div>

                    {/* Content Area */}
                    <div className="md:col-span-3 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
                        {children}
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
};

export default SettingsLayout;
