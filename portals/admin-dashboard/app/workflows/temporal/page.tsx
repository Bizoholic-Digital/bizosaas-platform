'use client'

import React from 'react'
import {
    Network,
    Activity,
    CheckCircle,
    XCircle,
    Clock,
    Play,
    Pause,
    RefreshCw,
    Search,
    Filter,
    MoreHorizontal,
    ExternalLink,
    ChevronRight
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { useTemporalStatus, useTemporalExecutions } from '@/lib/hooks/use-api'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"

export default function TemporalAdminPage() {
    const { data: status, isLoading: statusLoading } = useTemporalStatus()
    const { data: executionsData, isLoading: executionsLoading } = useTemporalExecutions()

    const executions = executionsData?.executions || []

    return (
        <div className="p-8 space-y-8">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white flex items-center gap-3">
                        <Network className="h-8 w-8 text-indigo-600" />
                        Temporal Workflow Orchestration
                    </h1>
                    <p className="text-gray-500 dark:text-gray-400 mt-2">
                        Global oversight of long-running workflows and worker cluster health.
                    </p>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" onClick={() => window.open('https://temporal.bizoholic.net', '_blank')}>
                        <ExternalLink className="mr-2 h-4 w-4" /> Temporal UI
                    </Button>
                    <Button className="bg-indigo-600 hover:bg-indigo-700">
                        <RefreshCw className="mr-2 h-4 w-4" /> Refresh Status
                    </Button>
                </div>
            </div>

            {/* Health Overview */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-gray-500">Cluster Status</CardTitle>
                        <Activity className="h-4 w-4 text-green-500" />
                    </CardHeader>
                    <CardContent>
                        <div className={`text-2xl font-bold ${status?.status === 'connected' ? 'text-green-600' : 'text-red-600'}`}>
                            {status?.status?.toUpperCase() || 'OFFLINE'}
                        </div>
                        <p className="text-xs text-gray-500 mt-1">Host: {status?.host || 'localhost'}</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-gray-500">Namespace</CardTitle>
                        <Network className="h-4 w-4 text-indigo-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{status?.namespace || 'default'}</div>
                        <p className="text-xs text-gray-500 mt-1">Isolation Layer Active</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-gray-500">Active Executions</CardTitle>
                        <Play className="h-4 w-4 text-blue-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{executionsData?.total_active || 0}</div>
                        <p className="text-xs text-gray-500 mt-1">Currently processing</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-gray-500">Failed (24h)</CardTitle>
                        <XCircle className="h-4 w-4 text-red-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{executionsData?.total_failed_24h || 0}</div>
                        <p className="text-xs text-gray-500 mt-1">Require investigation</p>
                    </CardContent>
                </Card>
            </div>

            {/* Execution Monitor */}
            <Card className="rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden">
                <CardHeader className="border-b border-gray-100 dark:border-gray-800">
                    <div className="flex justify-between items-center">
                        <div>
                            <CardTitle>Workflow Execution Monitor</CardTitle>
                            <CardDescription>Real-time stream of platform-wide Temporal tasks.</CardDescription>
                        </div>
                        <div className="flex gap-2">
                            <div className="relative">
                                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-500" />
                                <Input placeholder="Search workflows..." className="pl-8 w-64" />
                            </div>
                            <Button variant="outline"><Filter className="mr-2 h-4 w-4" /> Filter</Button>
                        </div>
                    </div>
                </CardHeader>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Workflow ID</TableHead>
                            <TableHead>Type</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Start Time</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {executions.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={5} className="text-center py-10 text-gray-500 italic">
                                    No active executions found in the current namespace.
                                </TableCell>
                            </TableRow>
                        ) : (
                            executions.map((exe: any) => (
                                <TableRow key={exe.run_id}>
                                    <TableCell className="font-mono text-xs text-indigo-600">{exe.workflow_id}</TableCell>
                                    <TableCell className="font-semibold">{exe.type}</TableCell>
                                    <TableCell>
                                        <Badge className={
                                            exe.status === 'Running' ? 'bg-blue-100 text-blue-800' :
                                                exe.status === 'Completed' ? 'bg-green-100 text-green-800' :
                                                    exe.status === 'Failed' ? 'bg-red-100 text-red-800' :
                                                        'bg-gray-100 text-gray-800'
                                        }>
                                            {exe.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-xs text-gray-500">{new Date(exe.start_time).toLocaleString()}</TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                                            <MoreHorizontal className="h-4 w-4" />
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </Card>

            {/* Workflow Performance Analytics */}
            <div className="grid gap-6 md:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle>Success Rate Analysis</CardTitle>
                        <CardDescription>Workflow completion ratios over the last 30 days.</CardDescription>
                    </CardHeader>
                    <CardContent className="h-48 flex items-center justify-center border-t">
                        <div className="text-center">
                            <div className="text-4xl font-bold text-green-600">99.5%</div>
                            <p className="text-sm text-gray-400">Average Platform Success Rate</p>
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle>Latency Distribution</CardTitle>
                        <CardDescription>Average workflow execution duration by type.</CardDescription>
                    </CardHeader>
                    <CardContent className="p-0">
                        <div className="divide-y">
                            <div className="px-6 py-3 flex justify-between items-center">
                                <span className="text-sm font-medium">TenantProvisioning</span>
                                <span className="text-xs font-mono">12.4s avg</span>
                            </div>
                            <div className="px-6 py-3 flex justify-between items-center">
                                <span className="text-sm font-medium">AgentOrchestration</span>
                                <span className="text-xs font-mono">2.1s avg</span>
                            </div>
                            <div className="px-6 py-3 flex justify-between items-center">
                                <span className="text-sm font-medium">CRMSync</span>
                                <span className="text-xs font-mono">45.8s avg</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
