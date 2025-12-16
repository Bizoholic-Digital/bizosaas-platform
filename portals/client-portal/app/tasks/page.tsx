'use client';

import React from 'react';
import DashboardLayout from '@/components/ui/dashboard-layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckSquare, Plus, Calendar, Clock, AlertCircle } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function TasksPage() {
    const router = useRouter();

    return (
        <DashboardLayout title="Tasks & Projects" description="Manage your team's work">
            <div className="p-6 space-y-6">
                <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold tracking-tight">Overview</h2>
                    <Button onClick={() => router.push('/tasks/new')}>
                        <Plus className="mr-2 h-4 w-4" /> New Task
                    </Button>
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">My Open Tasks</CardTitle>
                            <CheckSquare className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">12</div>
                            <p className="text-xs text-muted-foreground">3 due today</p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Active Projects</CardTitle>
                            <Clock className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">4</div>
                            <p className="text-xs text-muted-foreground">1 at risk</p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Team Workload</CardTitle>
                            <AlertCircle className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">85%</div>
                            <p className="text-xs text-muted-foreground">Capacity utilization</p>
                        </CardContent>
                    </Card>
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    <Card className="col-span-2">
                        <CardHeader>
                            <CardTitle>My Upcoming Tasks</CardTitle>
                            <CardDescription>Tasks due in the next 7 days</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                {[1, 2, 3].map((i) => (
                                    <div key={i} className="flex items-center justify-between border-b pb-2 last:border-0 last:pb-0">
                                        <div className="flex items-center gap-3">
                                            <div className="h-4 w-4 rounded border border-gray-300 dark:border-gray-600" />
                                            <div>
                                                <p className="test-sm font-medium">Update branding materials</p>
                                                <p className="text-xs text-muted-foreground">Marketing Project • Due Tomorrow</p>
                                            </div>
                                        </div>
                                        <Badge>High</Badge>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle>Quick Access</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-2">
                            <Button variant="outline" className="w-full justify-start" onClick={() => router.push('/tasks/my-tasks')}>
                                <CheckSquare className="mr-2 h-4 w-4" /> My Tasks
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

function Badge({ children }: { children: React.ReactNode }) {
    return (
        <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-primary text-primary-foreground hover:bg-primary/80 bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300">
            {children}
        </span>
    )
}
