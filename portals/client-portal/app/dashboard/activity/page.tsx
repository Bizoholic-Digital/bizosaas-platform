'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Search, Activity, Clock, Shield, Bot, Plug, Mail } from 'lucide-react';

const MOCK_LOGS = [
    {
        id: 1,
        type: 'agent',
        title: 'Agent "SEO Expert" generated a report',
        description: 'Analyzed 45 keywords for bizoholic.com',
        timestamp: '2 minutes ago',
        status: 'success',
        icon: Bot,
        color: 'text-blue-500',
        bg: 'bg-blue-50 dark:bg-blue-900/20'
    },
    {
        id: 2,
        type: 'connector',
        title: 'New Lead via HubSpot',
        description: 'John Doe (john@example.com) synced from HubSpot',
        timestamp: '1 hour ago',
        status: 'success',
        icon: Plug,
        color: 'text-orange-500',
        bg: 'bg-orange-50 dark:bg-orange-900/20'
    },
    {
        id: 3,
        type: 'security',
        title: 'Login attempt from new location',
        description: 'San Francisco, CA (192.168.1.1)',
        timestamp: '3 hours ago',
        status: 'warning',
        icon: Shield,
        color: 'text-yellow-500',
        bg: 'bg-yellow-50 dark:bg-yellow-900/20'
    },
    {
        id: 4,
        type: 'marketing',
        title: 'Campaign "New Year Sale" sent',
        description: 'Sent to 1,200 contacts via FluentCRM',
        timestamp: '5 hours ago',
        status: 'success',
        icon: Mail,
        color: 'text-green-500',
        bg: 'bg-green-50 dark:bg-green-900/20'
    },
    {
        id: 5,
        type: 'system',
        title: 'WordPress sync completed',
        description: 'Synchronized 12 new posts and 4 media items',
        timestamp: 'Yesterday',
        status: 'success',
        icon: Activity,
        color: 'text-purple-500',
        bg: 'bg-purple-50 dark:bg-purple-900/20'
    }
];

export default function ActivityLogsPage() {
    return (
        <div className="p-6 space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Recent Activity</h1>
                    <p className="text-muted-foreground mt-1">
                        Track everything happening across your workspace.
                    </p>
                </div>
                <div className="relative w-full md:w-64">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <Input placeholder="Search logs..." className="pl-10" />
                </div>
            </div>

            <Card className="border-gray-200 dark:border-gray-800">
                <CardHeader>
                    <CardTitle className="text-lg font-semibold flex items-center gap-2">
                        <Clock className="w-5 h-5 text-blue-500" />
                        Activity History
                    </CardTitle>
                    <CardDescription>
                        A chronological record of all actions and automated tasks.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="space-y-6">
                        {MOCK_LOGS.map((log) => (
                            <div key={log.id} className="flex gap-4 group">
                                <div className="flex flex-col items-center">
                                    <div className={`p-2 rounded-full ${log.bg} ${log.color}`}>
                                        <log.icon className="w-5 h-5" />
                                    </div>
                                    <div className="w-0.5 h-full bg-gray-100 dark:bg-gray-800 my-2 group-last:hidden" />
                                </div>
                                <div className="pb-6 flex-1">
                                    <div className="flex items-center justify-between mb-1">
                                        <h4 className="text-sm font-semibold">{log.title}</h4>
                                        <span className="text-xs text-muted-foreground">{log.timestamp}</span>
                                    </div>
                                    <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                                        {log.description}
                                    </p>
                                    <div className="flex items-center gap-2">
                                        <Badge variant="outline" className="text-[10px] uppercase font-bold tracking-tight">
                                            {log.type}
                                        </Badge>
                                        <Badge variant="outline" className={`text-[10px] uppercase font-bold tracking-tight ${log.status === 'success' ? 'text-green-600 border-green-100 bg-green-50' :
                                                log.status === 'warning' ? 'text-yellow-600 border-yellow-100 bg-yellow-50' :
                                                    'text-red-600 border-red-100 bg-red-50'
                                            }`}>
                                            {log.status}
                                        </Badge>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
