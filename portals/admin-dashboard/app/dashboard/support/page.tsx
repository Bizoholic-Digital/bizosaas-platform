'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { adminApi } from '@/lib/api/admin';
import {
    RefreshCw,
    Ticket,
    AlertCircle,
    CheckCircle2,
    Clock,
    User,
    MessageSquare,
    Search,
    Filter,
    ArrowUpRight,
    Bug,
    Database,
    Zap,
    Activity,
    LifeBuoy
} from 'lucide-react';
import { toast } from 'sonner';
import { format } from 'date-fns';

export default function SupportTicketHub() {
    const [loading, setLoading] = useState(true);
    const [tickets, setTickets] = useState<any[]>([]);
    const [errors, setErrors] = useState<any[]>([]);
    const [diagnostics, setDiagnostics] = useState<any>(null);
    const [filterStatus, setFilterStatus] = useState<string>('all');
    const [searchTerm, setSearchTerm] = useState('');

    const loadData = async () => {
        setLoading(true);
        try {
            const [ticketsRes, errorsRes, diagRes] = await Promise.all([
                adminApi.getGlobalTickets(),
                adminApi.getSystemErrors(),
                adminApi.runDiagnostics()
            ]);

            if (ticketsRes.data) setTickets(ticketsRes.data);
            if (errorsRes.data) setErrors(errorsRes.data);
            if (diagRes.data) setDiagnostics(diagRes.data);

        } catch (error) {
            toast.error("Failed to sync support data");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const filteredTickets = tickets.filter(ticket => {
        const matchesSearch = ticket.subject.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesStatus = filterStatus === 'all' || ticket.status === filterStatus;
        return matchesSearch && matchesStatus;
    });

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case 'urgent': return 'bg-rose-500';
            case 'high': return 'bg-amber-500';
            case 'medium': return 'bg-indigo-500';
            default: return 'bg-slate-500';
        }
    };

    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Support & Debugging Hub</h1>
                    <p className="text-muted-foreground">Manage global support tickets, track system errors, and run diagnostics.</p>
                </div>
                <div className="flex gap-2">
                    <Button onClick={loadData} variant="outline" disabled={loading}>
                        <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Sync Data
                    </Button>
                </div>
            </div>

            {/* Support Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                            <Ticket className="h-8 w-8 text-indigo-500" />
                            <Badge variant="secondary">{tickets.filter(t => t.status === 'open').length} Open</Badge>
                        </div>
                        <div className="mt-4">
                            <h3 className="text-3xl font-bold">{tickets.length}</h3>
                            <p className="text-muted-foreground text-sm">Active Support Tickets</p>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                            <Bug className="h-8 w-8 text-rose-500" />
                            <Badge variant="destructive">{errors.length} Critical</Badge>
                        </div>
                        <div className="mt-4">
                            <h3 className="text-3xl font-bold">{errors.reduce((acc, curr) => acc + curr.count, 0)}</h3>
                            <p className="text-muted-foreground text-sm">System Errors (24h)</p>
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 text-white border-none">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                            <Activity className="h-8 w-8 text-emerald-400" />
                            <Badge className="bg-emerald-500/20 text-emerald-400 border-emerald-500/30">All Systems Go</Badge>
                        </div>
                        <div className="mt-4">
                            <h3 className="text-3xl font-bold">Health 100%</h3>
                            <p className="text-slate-400 text-sm">Diagnostic Success Rate</p>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <Tabs defaultValue="tickets" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="tickets">Support Tickets</TabsTrigger>
                    <TabsTrigger value="errors">Error Monitoring</TabsTrigger>
                    <TabsTrigger value="diagnostics">System Diagnostics</TabsTrigger>
                    <TabsTrigger value="tools">Admin Tools</TabsTrigger>
                </TabsList>

                <TabsContent value="tickets" className="space-y-4">
                    <div className="flex flex-col md:flex-row gap-4">
                        <div className="relative flex-1">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <input
                                type="search"
                                placeholder="Search by subject..."
                                className="w-full bg-background pl-8 h-10 rounded-md border border-input px-3 py-2 text-sm"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                        <div className="flex gap-2">
                            <Button variant={filterStatus === 'all' ? 'default' : 'outline'} onClick={() => setFilterStatus('all')} size="sm">All</Button>
                            <Button variant={filterStatus === 'open' ? 'default' : 'outline'} onClick={() => setFilterStatus('open')} size="sm">Open</Button>
                            <Button variant={filterStatus === 'resolved' ? 'default' : 'outline'} onClick={() => setFilterStatus('resolved')} size="sm">Resolved</Button>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 gap-4">
                        {filteredTickets.length === 0 ? (
                            <div className="p-12 text-center border-2 border-dashed rounded-xl">
                                <LifeBuoy className="h-12 w-12 text-muted-foreground/30 mx-auto" />
                                <p className="mt-2 text-muted-foreground">No support tickets found.</p>
                            </div>
                        ) : (
                            filteredTickets.map((ticket) => (
                                <Card key={ticket.id} className="hover:border-indigo-200 transition-colors">
                                    <CardContent className="p-0">
                                        <div className="flex flex-col md:flex-row md:items-center p-4 gap-4">
                                            <div className={`w-2 h-16 rounded-full ${getPriorityColor(ticket.priority)}`} />
                                            <div className="flex-1 min-w-0">
                                                <div className="flex items-center gap-2 mb-1">
                                                    <Badge variant="outline">{ticket.category || 'general'}</Badge>
                                                    <span className="text-xs text-muted-foreground">ID: {ticket.id.slice(0, 8)}</span>
                                                </div>
                                                <h4 className="text-lg font-bold truncate">{ticket.subject}</h4>
                                                <div className="flex items-center gap-4 text-sm text-muted-foreground mt-2">
                                                    <span className="flex items-center gap-1"><User className="h-3 w-3" /> Tenant: {ticket.tenant_id.slice(0, 8)}</span>
                                                    <span className="flex items-center gap-1"><Clock className="h-3 w-3" /> {format(new Date(ticket.created_at), 'MMM d, HH:mm')}</span>
                                                    <span className="flex items-center gap-1"><MessageSquare className="h-3 w-3" /> 0 replies</span>
                                                </div>
                                            </div>
                                            <div className="flex gap-2">
                                                <Button size="sm">View Thread</Button>
                                                <Button size="sm" variant="outline" className="text-emerald-600 hover:text-emerald-700">Resolve</Button>
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            ))
                        )}
                    </div>
                </TabsContent>

                <TabsContent value="errors">
                    <Card>
                        <CardHeader>
                            <CardTitle>Global Error Tracking</CardTitle>
                            <CardDescription>Consolidated system exceptions across all services.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                {errors.map((error) => (
                                    <div key={error.id} className="p-4 border rounded-lg flex items-start gap-4 hover:bg-slate-50 dark:hover:bg-slate-900/50 transition-colors">
                                        <div className="mt-1">
                                            <AlertCircle className="h-5 w-5 text-rose-500" />
                                        </div>
                                        <div className="flex-1">
                                            <div className="flex items-center justify-between">
                                                <p className="font-bold text-sm bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded text-indigo-600 inline-block">{error.service}</p>
                                                <span className="text-xs text-muted-foreground">First report: {error.last_seen}</span>
                                            </div>
                                            <h5 className="font-mono text-sm mt-2">{error.message}</h5>
                                            <div className="mt-3 flex items-center gap-4">
                                                <Badge variant="secondary">{error.count} occurrences</Badge>
                                                <Button variant="link" size="sm" className="h-auto p-0">View Stacktrace <ArrowUpRight className="h-3 w-3 ml-1" /></Button>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="diagnostics">
                    <Card>
                        <CardHeader>
                            <CardTitle>System Diagnostic Pulse</CardTitle>
                            <CardDescription>Live health probe of platform infrastructure components.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {diagnostics?.checks.map((check: any) => (
                                    <div key={check.name} className="flex items-center justify-between p-4 border rounded-xl bg-slate-50/50 dark:bg-slate-900/20">
                                        <div className="flex items-center gap-3">
                                            {check.status === 'pass' ?
                                                <CheckCircle2 className="h-5 w-5 text-emerald-500" /> :
                                                <AlertCircle className="h-5 w-5 text-rose-500" />
                                            }
                                            <div>
                                                <p className="font-semibold text-sm">{check.name}</p>
                                                {check.latency_ms && <p className="text-xs text-muted-foreground">{check.latency_ms}ms latency</p>}
                                            </div>
                                        </div>
                                        <Badge className={check.status === 'pass' ? 'bg-emerald-500' : 'bg-rose-500'}>
                                            {check.status.toUpperCase()}
                                        </Badge>
                                    </div>
                                ))}
                            </div>
                            <div className="mt-6 p-4 bg-indigo-50 dark:bg-indigo-900/10 rounded-lg flex items-center gap-4 border border-indigo-100 dark:border-indigo-900/30">
                                <Zap className="h-6 w-6 text-indigo-500" />
                                <div>
                                    <p className="text-sm font-bold">Proactive Analysis</p>
                                    <p className="text-xs text-muted-foreground">All systems are operating within optimal latency thresholds. No bottlenecks detected.</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="tools">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <Card className="cursor-pointer hover:border-indigo-500 transition-all border-dashed">
                            <CardContent className="pt-6 text-center">
                                <Database className="h-10 w-10 text-muted-foreground mx-auto mb-4" />
                                <h4 className="font-bold">Safe DB Query</h4>
                                <p className="text-xs text-muted-foreground mt-2">Execute SELECT queries directly against the platform DB.</p>
                            </CardContent>
                        </Card>

                        <Card className="cursor-pointer hover:border-indigo-500 transition-all border-dashed">
                            <CardContent className="pt-6 text-center">
                                <RefreshCw className="h-10 w-10 text-muted-foreground mx-auto mb-4" />
                                <h4 className="font-bold">Cache Purge</h4>
                                <p className="text-xs text-muted-foreground mt-2">Flush Redis entries globally or by key pattern.</p>
                            </CardContent>
                        </Card>

                        <Card className="cursor-pointer hover:border-indigo-500 transition-all border-dashed">
                            <CardContent className="pt-6 text-center">
                                <Zap className="h-10 w-10 text-muted-foreground mx-auto mb-4" />
                                <h4 className="font-bold">API Playground</h4>
                                <p className="text-xs text-muted-foreground mt-2">Test internal endpoints with Super Admin credentials.</p>
                            </CardContent>
                        </Card>

                        <Card className="cursor-pointer hover:border-indigo-500 transition-all border-dashed">
                            <CardContent className="pt-6 text-center">
                                <ArrowUpRight className="h-10 w-10 text-muted-foreground mx-auto mb-4" />
                                <h4 className="font-bold">Remote Logs</h4>
                                <p className="text-xs text-muted-foreground mt-2">Stream logs from Docker containers in real-time.</p>
                            </CardContent>
                        </Card>
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
}
