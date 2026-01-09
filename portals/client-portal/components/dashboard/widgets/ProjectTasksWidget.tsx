'use client';

import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Plus, ExternalLink, Calendar, ListTodo } from 'lucide-react';

interface Project {
    id: string;
    name: string;
    identifier: string;
    state: string;
    description?: string;
}

export function ProjectTasksWidget({ tenantId = "default-tenant" }: { tenantId?: string }) {
    const [projects, setProjects] = useState<Project[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [viewMode, setViewMode] = useState<'list' | 'calendar'>('list');

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                setLoading(true);
                // Call our internal proxy which handles the Plane API auth securely
                const res = await fetch('/api/brain/plane');

                if (!res.ok) {
                    throw new Error(`Failed to load projects: ${res.statusText}`);
                }

                const data = await res.json();
                // Handle different Plane API response structures (results array or direct array)
                const projectList = Array.isArray(data) ? data : (data.results || []);
                setProjects(projectList);
                setError(null);
            } catch (err: any) {
                console.error("Plane widget error:", err);
                // Fallback to empty state rather than scary error if it's just connectivity
                setError("Could not sync with Project Management system.");
            } finally {
                setLoading(false);
            }
        };

        if (tenantId) {
            fetchProjects();
        }
    }, [tenantId]);

    if (!tenantId) {
        return (
            <Card className="h-full">
                <CardContent className="pt-6 flex flex-col items-center justify-center h-full gap-4">
                    <p className="text-sm text-muted-foreground">Please log in to view projects.</p>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card className="col-span-1 border-gray-200 dark:border-gray-800 h-full flex flex-col">
            <CardHeader className="flex flex-row items-center justify-between pb-2 border-b border-gray-100 dark:border-gray-800">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <ListTodo className="w-4 h-4 text-blue-500" />
                    My Projects
                </CardTitle>
                <div className="flex items-center gap-1">
                    {/* Calendar view toggle placeholder */}
                    <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={() => setViewMode(viewMode === 'list' ? 'calendar' : 'list')}
                        title={viewMode === 'list' ? "Switch to Calendar" : "Switch to List"}
                    >
                        <Calendar className="w-4 h-4 text-gray-400" />
                    </Button>
                    <Badge variant="outline" className="text-xs font-normal">
                        {projects.length} Active
                    </Badge>
                </div>
            </CardHeader>
            <CardContent className="flex-1 overflow-y-auto p-0">
                {loading ? (
                    <div className="p-4 space-y-3">
                        {[1, 2, 3].map(i => (
                            <div key={i} className="h-10 bg-gray-100 dark:bg-gray-800 rounded animate-pulse" />
                        ))}
                    </div>
                ) : error ? (
                    <div className="p-4 text-center">
                        <p className="text-xs text-red-500 mb-2">{error}</p>
                        <Button variant="outline" size="sm" onClick={() => window.location.reload()}>Retry</Button>
                    </div>
                ) : projects.length === 0 ? (
                    <div className="p-8 text-center text-muted-foreground">
                        <p className="text-sm">No active projects found.</p>
                        <Button variant="link" size="sm" className="mt-2 text-blue-600">
                            <Plus className="w-3 h-3 mr-1" /> Create Project
                        </Button>
                    </div>
                ) : (
                    <div className="divide-y divide-gray-100 dark:divide-gray-800">
                        {viewMode === 'calendar' ? (
                            <div className="p-8 text-center text-muted-foreground">
                                <Calendar className="w-8 h-8 mx-auto mb-2 opacity-50" />
                                <p className="text-sm">Timeline view requires Plane Premium.</p>
                                <Button variant="link" size="sm" onClick={() => setViewMode('list')}>Back to List</Button>
                            </div>
                        ) : (
                            projects.map((project) => (
                                <div key={project.id} className="p-3 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors group">
                                    <div className="flex items-start justify-between mb-1">
                                        <h4 className="text-sm font-medium text-gray-900 dark:text-white group-hover:text-blue-600 transition-colors">
                                            {project.name}
                                        </h4>
                                        <Badge variant="secondary" className="text-[10px] m-0">
                                            {project.identifier}
                                        </Badge>
                                    </div>
                                    <div className="flex items-center justify-between mt-2">
                                        <Badge
                                            variant={project.state === 'Completed' ? 'default' : 'outline'}
                                            className={`text-[10px] px-1.5 py-0 h-5 ${project.state === 'In Progress' ? 'border-blue-200 bg-blue-50 text-blue-700 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-800' :
                                                project.state === 'Completed' ? 'border-green-200 bg-green-50 text-green-700 dark:bg-green-900/20 dark:text-green-300 dark:border-green-800' : ''
                                                }`}
                                        >
                                            {project.state || 'Active'}
                                        </Badge>
                                        <Button variant="ghost" size="icon" className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <ExternalLink className="w-3 h-3 text-gray-400" />
                                        </Button>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                )}
            </CardContent>
            <div className="p-4 border-t border-gray-100 dark:border-gray-800">
                <Button variant="outline" className="w-full text-xs h-8" asChild>
                    <a href="/tasks">View All Tasks & Projects</a>
                </Button>
            </div>
        </Card>
    );
}
