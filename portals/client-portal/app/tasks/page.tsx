
'use client';

import React, { useEffect, useState } from 'react';
import DashboardLayout from '@/components/ui/dashboard-layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckSquare, Plus, Calendar, Clock, AlertCircle, RefreshCw } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function TasksPage() {
    const router = useRouter();
    const [tasks, setTasks] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState({
        open: 0,
        projects: 0,
        utilization: '0%'
    });

    const fetchTasks = async () => {
        setLoading(true);
        try {
            const response = await fetch('/api/brain/plane?type=issues');
            if (response.ok) {
                const data = await response.json();
                const issues = data.results || [];
                setTasks(issues.slice(0, 5)); // Just show recent 5
                setStats({
                    open: issues.filter((i: any) => i.state_detail?.group !== 'completed').length,
                    projects: 1, // Assume 1 for now or fetch projects too
                    utilization: '85%'
                });
            }
        } catch (error) {
            console.error('Failed to fetch tasks:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTasks();
    }, []);

    return (
        <DashboardLayout title="Tasks & Projects" description="Manage your team's work">
            <div className="p-6 space-y-6">
                <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold tracking-tight">Overview</h2>
                    <div className="flex gap-2">
                        <Button variant="outline" size="sm" onClick={fetchTasks} disabled={loading}>
                            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                        </Button>
                        <Button onClick={() => router.push('/tasks/new')}>
                            <Plus className="mr-2 h-4 w-4" /> New Task
                        </Button>
                    </div>
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">My Open Tasks</CardTitle>
                            <CheckSquare className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{loading ? '...' : stats.open}</div>
                            <p className="text-xs text-muted-foreground">Action items on Plane.so</p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Active Projects</CardTitle>
                            <Clock className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{stats.projects}</div>
                            <p className="text-xs text-muted-foreground">BizOSaaS Main Project</p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Team Workload</CardTitle>
                            <AlertCircle className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{stats.utilization}</div>
                            <p className="text-xs text-muted-foreground">Capacity utilization</p>
                        </CardContent>
                    </Card>
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    <Card className="col-span-2">
                        <CardHeader>
                            <CardTitle>Recent Tasks from Plane</CardTitle>
                            <CardDescription>Live synchronization with your Plane project</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                {loading ? (
                                    <p className="text-sm text-muted-foreground">Loading tasks...</p>
                                ) : tasks.length > 0 ? (
                                    tasks.map((task: any) => (
                                        <div key={task.id} className="flex items-center justify-between border-b pb-2 last:border-0 last:pb-0">
                                            <div className="flex items-center gap-3">
                                                <div className={`h-4 w-4 rounded border ${task.state_detail?.group === 'completed' ? 'bg-green-500 border-green-500' : 'border-gray-300'}`} />
                                                <div>
                                                    <p className="text-sm font-medium">{task.name}</p>
                                                    <p className="text-xs text-muted-foreground">
                                                        {task.project_detail?.name || 'Project'} • {task.state_detail?.name || 'Todo'}
                                                    </p>
                                                </div>
                                            </div>
                                            <Badge priority={task.priority}>{task.priority}</Badge>
                                        </div>
                                    ))
                                ) : (
                                    <p className="text-sm text-muted-foreground">No tasks found in project.</p>
                                )}
                            </div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle>Quick Access</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-2">
                            <Button variant="outline" className="w-full justify-start" onClick={() => window.open('https://app.plane.so/bizosaas/projects/031b7a9e-ee6d-46f5-99da-8e9e911ae71d/issues/', '_blank')}>
                                <CheckSquare className="mr-2 h-4 w-4" /> Open Plane UI
                            </Button>
                            <Button variant="outline" className="w-full justify-start" onClick={() => router.push('/tasks/projects')}>
                                <Clock className="mr-2 h-4 w-4" /> All Projects
                            </Button>
                            <Button variant="outline" className="w-full justify-start" onClick={() => router.push('/tasks/calendar')}>
                                <Calendar className="mr-2 h-4 w-4" /> Calendar
                            </Button>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </DashboardLayout>
    );
}

function Badge({ children, priority }: { children: React.ReactNode, priority: string }) {
    const colors: Record<string, string> = {
        urgent: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
        high: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300',
        medium: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
        low: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
    };

    const colorClass = colors[priority.toLowerCase()] || colors.medium;

    return (
        <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold uppercase ${colorClass} border-transparent`}>
            {children}
        </span>
    )
}
