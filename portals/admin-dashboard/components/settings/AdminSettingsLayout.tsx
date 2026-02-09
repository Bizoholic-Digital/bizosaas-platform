'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    Settings,
    Shield,
    Database,
    Bell,
    Globe,
    Activity,
    Key,
    ChevronRight,
    Monitor,
    HardDrive,
    Users
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface AdminSettingsLayoutProps {
    children: React.ReactNode;
}

const sidebarItems = [
    {
        title: "General Platform",
        items: [
            { id: 'platform', name: 'Platform Settings', href: '/dashboard/settings', icon: Settings },
            { id: 'branding', name: 'Branding & UI', href: '/dashboard/settings/branding', icon: Monitor },
        ]
    },
    {
        title: "Security & Control",
        items: [
            { id: 'security', name: 'Security Policy', href: '/dashboard/settings/security', icon: Shield },
            { id: 'api-keys', name: 'Global API Keys', href: '/dashboard/settings/api-keys', icon: Key },
            { id: 'roles', name: 'Role Management', href: '/dashboard/settings/roles', icon: Users },
        ]
    },
    {
        title: "Core Infrastructure",
        items: [
            { id: 'database', name: 'Database Clusters', href: '/dashboard/settings/infrastructure', icon: Database },
            { id: 'storage', name: 'Storage Array', href: '/dashboard/settings/storage', icon: HardDrive },
            { id: 'nodes', name: 'Cluster Nodes', href: '/dashboard/settings/nodes', icon: Activity },
        ]
    },
    {
        title: "Communications",
        items: [
            { id: 'notifications', name: 'Global Alerts', href: '/dashboard/settings/notifications', icon: Bell },
            { id: 'smtp', name: 'SMTP Configuration', href: '/dashboard/settings/smtp', icon: Globe },
        ]
    }
];

export default function AdminSettingsLayout({ children }: AdminSettingsLayoutProps) {
    const pathname = usePathname();

    return (
        <div className="flex flex-col lg:flex-row min-h-full bg-slate-50 dark:bg-slate-950">
            {/* Sidebar */}
            <div className="w-full lg:w-72 border-b lg:border-b-0 lg:border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-y-auto">
                <div className="p-6">
                    <h2 className="text-xl font-black text-slate-900 dark:text-white uppercase italic tracking-tighter">
                        System <span className="text-indigo-600">Config</span>
                    </h2>
                    <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mt-1">Platform Orchestration</p>
                </div>

                <nav className="px-4 pb-20 lg:pb-8">
                    {sidebarItems.map((section, idx) => (
                        <div key={idx} className="mb-6">
                            <h3 className="px-3 mb-2 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">
                                {section.title}
                            </h3>
                            <div className="space-y-1">
                                {section.items.map((item) => {
                                    const isActive = pathname === item.href;
                                    return (
                                        <Link
                                            key={item.id}
                                            href={item.href}
                                            className={cn(
                                                "flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-bold transition-all duration-200 group",
                                                isActive
                                                    ? "bg-indigo-600 text-white shadow-lg shadow-indigo-500/20"
                                                    : "text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800"
                                            )}
                                        >
                                            <div className="flex items-center gap-3">
                                                <item.icon className={cn("w-4 h-4", isActive ? "text-white" : "text-slate-400 group-hover:text-indigo-500")} />
                                                <span>{item.name}</span>
                                            </div>
                                            <ChevronRight className={cn("w-4 h-4 transition-transform", isActive ? "translate-x-0" : "-translate-x-1 opacity-0 group-hover:translate-x-0 group-hover:opacity-100")} />
                                        </Link>
                                    );
                                })}
                            </div>
                        </div>
                    ))}
                </nav>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col min-w-0">
                <div className="flex-1 p-4 md:p-8 lg:p-12 max-w-5xl mx-auto w-full">
                    {children}
                </div>
            </div>
        </div>
    );
}
