'use client'

import React from 'react'
import {
    Globe,
    Plus,
    Search,
    CheckCircle2,
    XCircle,
    AlertCircle,
    ShieldCheck,
    RefreshCw,
    MoreVertical,
    ArrowUpRight,
    Zap,
    Layout
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { useConnectedSites } from '@/lib/hooks/use-api'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"

export default function CMSAdminPage() {
    const { data: sitesData, isLoading } = useConnectedSites()
    const sites = sitesData?.sites || []

    return (
        <div className="p-8 space-y-8">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white flex items-center gap-3">
                        <Layout className="h-8 w-8 text-blue-600" />
                        Global CMS Administration
                    </h1>
                    <p className="text-gray-500 dark:text-gray-400 mt-2">
                        Oversight of all tenant WordPress sites and the BizoSaaS Connect plugin mesh.
                    </p>
                </div>
                <div className="flex gap-3">
                    <Button className="bg-blue-600 hover:bg-blue-700">
                        <ShieldCheck className="mr-2 h-4 w-4" /> Bulk Plugin Update
                    </Button>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                <Card className="bg-gradient-to-br from-blue-50 to-white dark:from-gray-900 dark:to-gray-800">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Connected Sites</CardTitle>
                        <Globe className="h-4 w-4 text-blue-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{sites.length}</div>
                        <p className="text-xs text-green-600 flex items-center mt-1">
                            <Zap className="h-3 w-3 mr-1" /> All Systems Active
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Healthy Connections</CardTitle>
                        <CheckCircle2 className="h-4 w-4 text-green-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{sites.filter((s: any) => s.status === 'connected').length}</div>
                        <p className="text-xs text-gray-500 mt-1">Plugin authentication verified</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Plugin Mesh Version</CardTitle>
                        <ShieldCheck className="h-4 w-4 text-purple-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">v2.4.1</div>
                        <p className="text-xs text-indigo-500 mt-1">Latest stable release</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Avg Page Speed</CardTitle>
                        <ArrowUpRight className="h-4 w-4 text-orange-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">94/100</div>
                        <p className="text-xs text-orange-500 mt-1">+2% from last week</p>
                    </CardContent>
                </Card>
            </div>

            {/* Sites Inventory */}
            <Card className="border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden">
                <CardHeader className="bg-gray-50/50 dark:bg-gray-800/50">
                    <div className="flex justify-between items-center">
                        <div>
                            <CardTitle>Tenant WordPress Inventory</CardTitle>
                            <CardDescription>Cross-tenant list of all sites connected to the brain gateway.</CardDescription>
                        </div>
                        <div className="relative">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-400" />
                            <Input placeholder="Search sites by domain or tenant..." className="pl-9 w-72 h-9 bg-white dark:bg-gray-900" />
                        </div>
                    </div>
                </CardHeader>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Tenant ID</TableHead>
                            <TableHead>Site Domain</TableHead>
                            <TableHead>Plugin Version</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Last Sync</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading ? (
                            <TableRow><TableCell colSpan={6} className="py-10 text-center text-gray-500">Scanning plugin mesh...</TableCell></TableRow>
                        ) : sites.length === 0 ? (
                            <TableRow><TableCell colSpan={6} className="py-10 text-center text-gray-500">No sites connected for any tenant.</TableCell></TableRow>
                        ) : sites.map((site: any) => (
                            <TableRow key={site.site_url}>
                                <TableCell className="font-mono text-[10px] text-gray-500">{site.tenant_id}</TableCell>
                                <TableCell>
                                    <div className="font-medium flex items-center gap-2">
                                        {site.site_url}
                                        <Button variant="ghost" size="sm" className="h-6 w-6 p-0" onClick={() => window.open(site.site_url, '_blank')}>
                                            <ArrowUpRight className="h-3 w-3" />
                                        </Button>
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <Badge variant="outline" className="font-mono">{site.plugin_version}</Badge>
                                </TableCell>
                                <TableCell>
                                    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${site.status === 'connected' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                        }`}>
                                        {site.status === 'connected' ? <CheckCircle2 className="mr-1 h-3 w-3" /> : <XCircle className="mr-1 h-3 w-3" />}
                                        {site.status}
                                    </span>
                                </TableCell>
                                <TableCell className="text-xs text-gray-500">{new Date(site.last_sync).toLocaleString()}</TableCell>
                                <TableCell className="text-right">
                                    <Button variant="ghost" size="sm">
                                        <MoreVertical className="h-4 w-4" />
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Card>

            {/* Global Plugin Management */}
            <Card className="border-indigo-100 bg-indigo-50/30 dark:bg-indigo-900/10">
                <CardHeader>
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-indigo-100 dark:bg-indigo-900/50 rounded-lg text-indigo-600 dark:text-indigo-400">
                            <Zap className="h-5 w-5" />
                        </div>
                        <div>
                            <CardTitle>BizoSaaS Connect Distribution</CardTitle>
                            <CardDescription>Manage the core WordPress plugin distributed to all tenants.</CardDescription>
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="flex items-center justify-between p-4 bg-white dark:bg-gray-900 rounded-lg border border-indigo-100">
                        <div>
                            <p className="font-semibold text-gray-900 dark:text-white">Current Master Version: v2.4.1</p>
                            <p className="text-sm text-gray-500">Released January 12, 2026. Includes AI SEO optimization fix.</p>
                        </div>
                        <div className="flex gap-2">
                            <Button variant="outline" size="sm">Download Zip</Button>
                            <Button className="bg-indigo-600 hover:bg-indigo-700" size="sm">Push to All Sites</Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
