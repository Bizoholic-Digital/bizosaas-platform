'use client';

import React from 'react';
import DashboardLayout from '@/components/ui/dashboard-layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus, FolderKanban, MoreHorizontal } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function ProjectsPage() {
    return (
        <DashboardLayout title="Projects" description="Manage all active projects">
            <div className="p-6 space-y-6">
                <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold tracking-tight">All Projects</h2>
                    <Button>
                        <Plus className="mr-2 h-4 w-4" /> New Project
                    </Button>
                </div>

                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                    {[1, 2, 3, 4].map((i) => (
                        <Card key={i} className="cursor-pointer hover:shadow-md transition-shadow">
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <Badge variant="outline">In Progress</Badge>
                                <Button variant="ghost" size="icon" className="h-8 w-8">
                                    <MoreHorizontal className="h-4 w-4" />
                                </Button>
                            </CardHeader>
                            <CardContent className="pt-4">
                                <div className="flex items-center gap-3 mb-3">
                                    <div className="h-10 w-10 rounded bg-blue-100 flex items-center justify-center text-blue-600 dark:bg-blue-900 dark:text-blue-300">
                                        <FolderKanban className="h-5 w-5" />
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-lg">Website Redesign</h3>
                                        <p className="text-sm text-muted-foreground">Marketing Team</p>
                                    </div>
                                </div>

                                <div className="space-y-4">
                                    <div>
                                        <div className="flex items-center justify-between text-sm mb-1">
                                            <span className="text-muted-foreground">Progress</span>
                                            <span className="font-medium">65%</span>
                                        </div>
                                        <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                                            <div className="h-full bg-blue-600 w-[65%]" />
                                        </div>
                                    </div>

                                    <div className="flex items-center justify-between text-sm">
                                        <div className="flex -space-x-2">
                                            <div className="h-6 w-6 rounded-full bg-gray-200 border-2 border-white dark:border-gray-800" />
                                            <div className="h-6 w-6 rounded-full bg-gray-300 border-2 border-white dark:border-gray-800" />
                                            <div className="h-6 w-6 rounded-full bg-gray-400 border-2 border-white dark:border-gray-800" />
                                        </div>
                                        <span className="text-muted-foreground">Due Oct 24</span>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        </DashboardLayout>
    );
}
