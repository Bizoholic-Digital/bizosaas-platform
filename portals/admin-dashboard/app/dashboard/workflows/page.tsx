'use client';

import { useState, useEffect } from 'react';
import { adminApi } from '@/lib/api/admin';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
    Activity,
    CheckCircle2,
    AlertCircle,
    Clock,
    Play,
    Pause,
    Settings,
    RefreshCw,
    Server,
    ShieldCheck,
    Users,
    Cpu,
    ExternalLink,
    Terminal,
    ChevronRight,
    Search
} from 'lucide-react';
import { Input } from '@/components/ui/input';
import { toast } from 'sonner';

const PLATFORM_WORKFLOWS = [
    {
        id: 'billing-cycle-001',
        name: 'Monthly Billing & Payouts',
        status: 'running',
        type: 'Financial',
        lastRun: '2 hours ago',
        successRate: '100%',
        description: 'Aggregates usage from all tenants, calculates Lago invoices, and processes Stripe payments.',
        hitlPending: false,
        category: 'infrastructure'
    },
    {
        id: 'agent-nurturing-005',
        name: 'AI Smart Lead Nurturing',
        status: 'proposed',
        type: 'Agentic',
        lastRun: 'Never',
        successRate: 'N/A',
        description: 'AI-personalized follow-up sequence across Email/WhatsApp identified by Growth Agent.',
        hitlPending: true,
        category: 'hitl'
    },
    {
        id: 'inventory-sync-006',
        name: 'Universal Inventory Recon',
        status: 'required',
        type: 'Operations',
        lastRun: 'Never',
        successRate: 'N/A',
        description: 'Identified requirement: Coordinate inventory levels between Shopify, WooCommerce, and Amazon.',
        hitlPending: false,
        category: 'infrastructure'
    },
    {
        id: 'partner-sync-002',
        name: 'AI Partner Assignment',
        status: 'paused',
        type: 'Orchestration',
        lastRun: '5 hours ago',
        successRate: '98.5%',
        description: 'Evaluates partner capacity and automatically assigns new client accounts based on skill matching.',
        hitlPending: true,
        category: 'hitl'
    },
    {
        id: 'system-scale-003',
        name: 'Autonomous Infrastructure Scaling',
        status: 'running',
        type: 'Infrastructure',
        lastRun: '15 mins ago',
        successRate: '100%',
        description: 'Monitors CPU/Memory load across all brand clusters and scales Docker containers via Temporal.',
        hitlPending: false,
        category: 'infrastructure'
    },
    {
        id: 'seo-monitor-007',
        name: 'SEO Health Guardian',
        status: 'running',
        type: 'Agentic',
        lastRun: '1 hour ago',
        successRate: '99.5%',
        description: 'Continuous technical SEO scan and automated fix suggestion generator.',
        hitlPending: false,
        category: 'all'
    },
    {
        id: 'security-audit-004',
        name: 'Platform Wide Security Audit',
        status: 'scheduled',
        type: 'Security',
        lastRun: 'Yesterday',
        successRate: '99.9%',
        description: 'Scans all connected APIs and databases for credential leaks and unusual access patterns.',
        hitlPending: false,
        category: 'infrastructure'
    }
];

export default function AdminWorkflowsPage() {
    const [workflows, setWorkflows] = useState(PLATFORM_WORKFLOWS);
    const [proposals, setProposals] = useState<any[]>([]);
    const [approvals, setApprovals] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
            try {
                const [propRes, appRes] = await Promise.all([
                    adminApi.getProposals(),
                    adminApi.getApprovals()
                ]);

                if (propRes.data) setProposals(propRes.data);
                if (appRes.data) setApprovals(appRes.data);
            } catch (error) {
                console.error('Failed to load data:', error);
            } finally {
                setIsLoading(false);
            }
        };
        loadData();
    }, []);

    const handleToggleStatus = (id: string) => {
        setWorkflows(prev => prev.map(wf => {
            if (wf.id === id) {
                const newStatus = wf.status === 'running' ? 'paused' : 'running';
                toast.success(`Platform workflow ${newStatus === 'running' ? 'resumed' : 'paused'}`);
                return { ...wf, status: newStatus };
            }
            return wf;
        }));
    };

    const handleProposalAction = async (propId: string, action: 'approve' | 'reject') => {
        try {
            await adminApi.handleProposal(propId, action);
            setProposals(prev => prev.filter(p => p.id !== propId));
            toast.success(`Proposal ${action}ed successfully`);
        } catch (error) {
            toast.error('Failed to handle proposal');
        }
    };

    const handleApprovalAction = async (taskId: string, action: 'approve' | 'reject') => {
        try {
            await adminApi.handleApprovalTask(taskId, action);
            setApprovals(prev => prev.filter(a => a.id !== taskId));
            toast.success(`Task ${action}ed successfully`);
        } catch (error) {
            toast.error('Failed to handle approval task');
        }
    };

    return (
        <div className="p-6 space-y-6 max-w-7xl mx-auto">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold flex items-center gap-2">
                        <Activity className="w-8 h-8 text-indigo-600" />
                        Platform Orchestration
                    </h1>
                    <p className="text-muted-foreground">Global Temporal workflow management and system-wide automation control.</p>
                </div>
                <div className="flex items-center gap-3">
                    <Button variant="outline" className="gap-2">
                        <Terminal className="w-4 h-4" />
                        Console
                    </Button>
                    <Button className="bg-indigo-600 hover:bg-indigo-700 gap-2">
                        <ExternalLink className="w-4 h-4" />
                        Temporal UI
                    </Button>
                </div>
            </div>

            {/* Platform Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card className="bg-slate-900 text-white">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <Cpu className="w-4 h-4 text-slate-400" />
                            <Badge variant="outline" className="text-slate-400 border-slate-700">Healthy</Badge>
                        </div>
                        <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">Active Workflows</p>
                        <h3 className="text-2xl font-bold">128</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <CheckCircle2 className="w-4 h-4 text-green-600" />
                            <span className="text-xs text-green-600 font-bold">+0.2%</span>
                        </div>
                        <p className="text-xs text-muted-foreground font-medium uppercase tracking-wider">Success Rate</p>
                        <h3 className="text-2xl font-bold">99.85%</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <AlertCircle className="w-4 h-4 text-amber-600" />
                            <Badge variant="secondary" className="bg-amber-100 text-amber-700">Action Required</Badge>
                        </div>
                        <p className="text-xs text-muted-foreground font-medium uppercase tracking-wider">HITL Requests</p>
                        <h3 className="text-2xl font-bold">12</h3>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <Clock className="w-4 h-4 text-blue-600" />
                            <span className="text-xs text-muted-foreground">Avg. Latency</span>
                        </div>
                        <p className="text-xs text-muted-foreground font-medium uppercase tracking-wider">Mean Execution</p>
                        <h3 className="text-2xl font-bold">420ms</h3>
                    </CardContent>
                </Card>
            </div>

            <Tabs defaultValue="all" className="space-y-6">
                <div className="flex items-center justify-between bg-white dark:bg-slate-900 p-2 rounded-lg border">
                    <TabsList className="bg-transparent">
                        <TabsTrigger value="all" className="data-[state=active]:bg-slate-100 dark:data-[state=active]:bg-slate-800">All Workflows</TabsTrigger>
                        <TabsTrigger value="hitl" className="data-[state=active]:bg-slate-100 dark:data-[state=active]:bg-slate-800 flex items-center gap-2">
                            Approvals
                            <Badge className="h-5 w-5 p-0 flex items-center justify-center bg-amber-500">12</Badge>
                        </TabsTrigger>
                        <TabsTrigger value="infrastructure" className="data-[state=active]:bg-slate-100 dark:data-[state=active]:bg-slate-800">System Tasks</TabsTrigger>
                    </TabsList>
                    <div className="relative w-64 hidden md:block">
                        <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                        <Input placeholder="Search global workflows..." className="pl-8 h-9" />
                    </div>
                </div>

                <TabsContent value="all" className="space-y-4">
                    {workflows.filter(wf => wf.category === 'all' || wf.category === 'infrastructure' || wf.category === 'hitl').map(wf => (
                        <Card key={wf.id} className="group hover:border-slate-300 transition-all overflow-hidden border-l-4"
                            style={{ borderLeftColor: wf.status === 'running' ? '#10b981' : wf.status === 'paused' ? '#f59e0b' : '#64748b' }}>
                            <CardContent className="p-0">
                                <div className="flex items-center justify-between p-6">
                                    <div className="flex items-center gap-4">
                                        <div className={`p-3 rounded-xl bg-slate-50 dark:bg-slate-800`}>
                                            {wf.type === 'Financial' && <Server className="w-6 h-6 text-blue-600" />}
                                            {wf.type === 'Orchestration' && <Users className="w-6 h-6 text-purple-600" />}
                                            {wf.type === 'Infrastructure' && <Cpu className="w-6 h-6 text-emerald-600" />}
                                            {wf.type === 'Security' && <ShieldCheck className="w-6 h-6 text-red-600" />}
                                        </div>
                                        <div>
                                            <div className="flex items-center gap-2">
                                                <h3 className="font-bold text-lg">{wf.name}</h3>
                                                <Badge variant="outline" className="text-[10px] uppercase">{wf.type}</Badge>
                                                {wf.status === 'proposed' && (
                                                    <Badge className="bg-amber-100 text-amber-700 border-amber-200">Agent Identified</Badge>
                                                )}
                                                {wf.status === 'required' && (
                                                    <Badge className="bg-indigo-100 text-indigo-700 border-indigo-200">Platform Goal</Badge>
                                                )}
                                                {wf.hitlPending && (
                                                    <Badge className="bg-red-100 text-red-700 border-red-200 animate-pulse">Needs Approval</Badge>
                                                )}
                                            </div>
                                            <p className="text-sm text-muted-foreground mt-1 max-w-xl">{wf.description}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-8">
                                        <div className="text-right hidden lg:block">
                                            <p className="text-xs text-muted-foreground uppercase">Success Rate</p>
                                            <p className="font-bold">{wf.successRate}</p>
                                        </div>
                                        <div className="text-right hidden md:block">
                                            <p className="text-xs text-muted-foreground uppercase">Last Activity</p>
                                            <p className="text-sm font-medium">{wf.lastRun}</p>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <Button variant="ghost" size="icon" onClick={() => handleToggleStatus(wf.id)}>
                                                {wf.status === 'running' ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 text-green-600" />}
                                            </Button>
                                            <Button variant="ghost" size="icon">
                                                <Settings className="w-4 h-4" />
                                            </Button>
                                            <ChevronRight className="w-5 h-5 text-slate-300" />
                                        </div>
                                    </div>
                                </div>
                                <div className="bg-slate-50 dark:bg-slate-900/50 px-6 py-2 border-t flex items-center justify-between text-[11px] text-muted-foreground uppercase tracking-widest">
                                    <span>Temporal Task ID: {wf.id}</span>
                                    <span>Worker Group: global-platform-pool</span>
                                </div>
                            </CardContent>
                        </Card>
                    ))}

                    <Card className="border-dashed border-2 bg-slate-50/50 dark:bg-slate-900/20 py-8 flex flex-col items-center justify-center text-center">
                        <RefreshCw className="w-8 h-8 text-slate-300 mb-2" />
                        <h3 className="font-medium text-slate-600">Sync with Worker State</h3>
                        <p className="text-xs text-slate-400 mt-1">Manual synchronization is required for ad-hoc distributed workflows.</p>
                        <Button variant="outline" size="sm" className="mt-4">Refresh State</Button>
                    </Card>
                </TabsContent>

                <TabsContent value="hitl" className="space-y-4">
                    {/* Agent Workflow Proposals */}
                    {proposals.length > 0 && (
                        <div className="space-y-4">
                            <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider px-1">Agent Identified Workflows</h2>
                            {proposals.map(wf => (
                                <Card key={wf.id} className="group hover:border-indigo-300 transition-all overflow-hidden border-l-4 border-l-indigo-500">
                                    <CardContent className="p-6">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-4">
                                                <div className="p-3 rounded-xl bg-indigo-50 dark:bg-indigo-900/20">
                                                    <Cpu className="w-6 h-6 text-indigo-600" />
                                                </div>
                                                <div>
                                                    <div className="flex items-center gap-2">
                                                        <h3 className="font-bold text-lg">{wf.name}</h3>
                                                        <Badge className="bg-indigo-100 text-indigo-700 border-indigo-200">New Optimization</Badge>
                                                        <Badge variant="outline">{wf.type}</Badge>
                                                    </div>
                                                    <p className="text-sm text-muted-foreground mt-1">{wf.description}</p>
                                                    <p className="text-[10px] font-black uppercase text-indigo-600 mt-2 tracking-widest">Agent: {wf.discoveredBy}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <Button className="bg-indigo-600 hover:bg-indigo-700" onClick={() => handleProposalAction(wf.id, 'approve')}>Approve & Deploy</Button>
                                                <Button variant="outline">Analyze Defintion</Button>
                                                <Button variant="ghost" className="text-red-600" onClick={() => handleProposalAction(wf.id, 'reject')}>Reject</Button>
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    )}

                    {/* Human-in-the-loop Action Approvals */}
                    {approvals.length > 0 && (
                        <div className="space-y-4">
                            <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider px-1">Action Approval Required</h2>
                            {approvals.map(task => (
                                <Card key={task.id} className="group hover:border-amber-300 transition-all overflow-hidden border-l-4 border-l-amber-500">
                                    <CardContent className="p-6">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-4">
                                                <div className="p-3 rounded-xl bg-amber-50 dark:bg-amber-900/20">
                                                    <AlertCircle className="w-6 h-6 text-amber-600" />
                                                </div>
                                                <div>
                                                    <div className="flex items-center gap-2">
                                                        <h3 className="font-bold text-lg">{task.title}</h3>
                                                        <Badge className={`bg-${task.priority === 'high' ? 'red' : 'amber'}-100 text-${task.priority === 'high' ? 'red' : 'amber'}-700 border-${task.priority === 'high' ? 'red' : 'amber'}-200`}>
                                                            {task.priority.toUpperCase()} PRIORITY
                                                        </Badge>
                                                        <Badge variant="outline">{task.type}</Badge>
                                                    </div>
                                                    <p className="text-sm text-muted-foreground mt-1">{task.description}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <Button className="bg-green-600 hover:bg-green-700" onClick={() => handleApprovalAction(task.id, 'approve')}>Execute Action</Button>
                                                <Button variant="outline">View Data</Button>
                                                <Button variant="ghost" className="text-red-600" onClick={() => handleApprovalAction(task.id, 'reject')}>Deny</Button>
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    )}

                    {proposals.length === 0 && approvals.length === 0 && (
                        <div className="text-center py-12">
                            <div className="max-w-md mx-auto">
                                <CheckCircle2 className="w-12 h-12 text-green-500 mx-auto mb-4" />
                                <h3 className="text-xl font-bold">All Clear</h3>
                                <p className="text-muted-foreground mt-2">No workflows or actions are currently awaiting human intervention.</p>
                            </div>
                        </div>
                    )}
                </TabsContent>

                <TabsContent value="infrastructure" className="space-y-4">
                    {workflows.filter(wf => wf.category === 'infrastructure').map(wf => (
                        <Card key={wf.id} className="group hover:border-slate-300 transition-all overflow-hidden border-l-4"
                            style={{ borderLeftColor: wf.status === 'running' ? '#10b981' : wf.status === 'paused' ? '#f59e0b' : '#64748b' }}>
                            <CardContent className="p-0">
                                <div className="flex items-center justify-between p-6">
                                    <div className="flex items-center gap-4">
                                        <div className={`p-3 rounded-xl bg-slate-50 dark:bg-slate-800`}>
                                            {wf.type === 'Financial' && <Server className="w-6 h-6 text-blue-600" />}
                                            {wf.type === 'Infrastructure' && <Cpu className="w-6 h-6 text-emerald-600" />}
                                            {wf.type === 'Security' && <ShieldCheck className="w-6 h-6 text-red-600" />}
                                            {wf.type === 'Operations' && <RefreshCw className="w-6 h-6 text-purple-600" />}
                                        </div>
                                        <div>
                                            <div className="flex items-center gap-2">
                                                <h3 className="font-bold text-lg">{wf.name}</h3>
                                                <Badge variant="outline" className="text-[10px] uppercase">{wf.type}</Badge>
                                            </div>
                                            <p className="text-sm text-muted-foreground mt-1 max-w-xl">{wf.description}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-8">
                                        <div className="text-right">
                                            <p className="text-xs text-muted-foreground uppercase">Success Rate</p>
                                            <p className="font-bold">{wf.successRate}</p>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <Button variant="ghost" size="icon" onClick={() => handleToggleStatus(wf.id)}>
                                                {wf.status === 'running' ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 text-green-600" />}
                                            </Button>
                                            <Button variant="ghost" size="icon">
                                                <Settings className="w-4 h-4" />
                                            </Button>
                                        </div>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </TabsContent>
            </Tabs>
        </div>
    );
}
