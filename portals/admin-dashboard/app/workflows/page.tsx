'use client';

import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Play,
  Pause,
  Square,
  RefreshCw,
  Settings,
  TrendingUp,
  Users,
  Activity,
  AlertCircle,
  CheckCircle,
  Clock,
  Zap,
  Database,
  Globe,
  Shield,
  DollarSign,
  Plus,
  Trash2,
  Copy,
  Key
} from 'lucide-react';
import { CardDescription } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

interface WorkflowStatus {
  id: string;
  name: string;
  type: 'ai-agent' | 'integration' | 'system' | 'user-management';
  status: 'running' | 'paused' | 'stopped' | 'error';
  lastRun: string;
  nextRun: string;
  successRate: number;
  executionCount: number;
  tenantCount: number;
  triggers?: any[];
}

interface SystemMetrics {
  totalWorkflows: number;
  activeWorkflows: number;
  successfulRuns: number;
  failedRuns: number;
  avgExecutionTime: number;
  totalTenants: number;
  activeUsers: number;
  apiRequests: number;
}

import { adminApi } from '@/lib/api/admin';
import { toast } from 'sonner';

// ... (imports)

export default function WorkflowManagementPage() {
  const [workflows, setWorkflows] = useState<WorkflowStatus[]>([]);
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [selectedWorkflow, setSelectedWorkflow] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [triggerModalOpen, setTriggerModalOpen] = useState(false);
  const [editingWorkflow, setEditingWorkflow] = useState<WorkflowStatus | null>(null);
  const [newTrigger, setNewTrigger] = useState<{
    type: 'webhook' | 'schedule' | 'event';
    path?: string;
    cron?: string;
    event_name?: string;
    secret_key?: string;
  }>({ type: 'webhook' });

  useEffect(() => {
    loadWorkflowData();
    const interval = setInterval(loadWorkflowData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadWorkflowData = async () => {
    try {
      setLoading(true);
      const [workflowsRes, analyticsRes, statsRes] = await Promise.all([
        adminApi.getWorkflows(),
        adminApi.getAnalytics(),
        adminApi.getStats()
      ]);

      if (workflowsRes.data) {
        const mapped: WorkflowStatus[] = workflowsRes.data.map((w: any) => ({
          id: w.id,
          name: w.name,
          type: (w.type?.toLowerCase() || 'system') as any,
          status: w.status,
          lastRun: w.lastRun ? new Date(w.lastRun).toLocaleString() : 'Never',
          nextRun: 'Scheduled',
          successRate: w.successRate || 100,
          executionCount: w.runsToday || 0,
          tenantCount: w.tenantCount || 1,
          triggers: w.triggers || []
        }));
        setWorkflows(mapped);

        // Process Analytics & Stats
        const analytics = analyticsRes.data || {};
        const stats = statsRes.data || { tenants: { total: 0 }, users: { total: 0 } };

        setMetrics({
          totalWorkflows: mapped.length,
          activeWorkflows: mapped.filter(w => w.status === 'running').length,
          successfulRuns: mapped.reduce((acc, w) => acc + (w.executionCount || 0), 0),
          failedRuns: Math.round(mapped.reduce((acc, w) => acc + (w.executionCount || 0), 0) * (analytics.error_rate || 0) / 100),
          avgExecutionTime: analytics.response_time_avg || 0,
          totalTenants: stats.tenants?.total || 1,
          activeUsers: stats.users?.total || 0,
          apiRequests: analytics.requests_per_minute || 0
        });
      }
    } catch (error) {
      console.error('Error loading workflow data:', error);
      toast.error('Failed to load operational data');
    } finally {
      setLoading(false);
    }
  };

  const handleWorkflowAction = async (workflowId: string, action: 'start' | 'pause' | 'stop') => {
    try {
      await adminApi.toggleWorkflow(workflowId);
      toast.success(`Workflow ${action}ed`); // simple grammar logic
      loadWorkflowData(); // Refresh list
    } catch (error) {
      console.error(`Error ${action}ing workflow:`, error);
      toast.error(`Failed to ${action} workflow`);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'paused': return <Clock className="w-4 h-4 text-yellow-500" />;
      case 'stopped': return <Square className="w-4 h-4 text-gray-500" />;
      case 'error': return <AlertCircle className="w-4 h-4 text-red-500" />;
      default: return <Activity className="w-4 h-4" />;
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'ai-agent': return <Zap className="w-4 h-4 text-purple-500" />;
      case 'integration': return <Globe className="w-4 h-4 text-blue-500" />;
      case 'system': return <Database className="w-4 h-4 text-gray-500" />;
      case 'user-management': return <Users className="w-4 h-4 text-green-500" />;
      default: return <Activity className="w-4 h-4" />;
    }
  };

  const handleSaveTriggers = async () => {
    if (!editingWorkflow) return;

    try {
      const updatedTriggers = [...(editingWorkflow.triggers || []), newTrigger];
      await adminApi.updateWorkflowTriggers(editingWorkflow.id, updatedTriggers);
      toast.success('Trigger added successfully');
      setTriggerModalOpen(false);
      loadWorkflowData();
    } catch (error) {
      toast.error('Failed to save trigger');
    }
  };

  const handleDeleteTrigger = async (workflow: WorkflowStatus, index: number) => {
    try {
      const updatedTriggers = workflow.triggers?.filter((_, i) => i !== index);
      await adminApi.updateWorkflowTriggers(workflow.id, updatedTriggers || []);
      toast.success('Trigger removed');
      loadWorkflowData();
    } catch (error) {
      toast.error('Failed to remove trigger');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin" />
        <span className="ml-2">Loading workflow data...</span>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Workflow Management</h1>
          <p className="text-gray-600 mt-1">Super Admin Dashboard - Platform Owner Controls</p>
        </div>
        <div className="flex space-x-2">
          <Button onClick={loadWorkflowData} variant="outline">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
          <Button>
            <Settings className="w-4 h-4 mr-2" />
            Configure
          </Button>
        </div>
      </div>

      {/* System Metrics Overview */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Active Workflows</p>
                  <p className="text-2xl font-bold text-green-600">{metrics.activeWorkflows}/{metrics.totalWorkflows}</p>
                </div>
                <Activity className="w-8 h-8 text-green-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Success Rate</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {((metrics.successfulRuns / (metrics.successfulRuns + metrics.failedRuns)) * 100).toFixed(1)}%
                  </p>
                </div>
                <TrendingUp className="w-8 h-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Tenants</p>
                  <p className="text-2xl font-bold text-purple-600">{metrics.totalTenants}</p>
                </div>
                <Users className="w-8 h-8 text-purple-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">API Requests</p>
                  <p className="text-2xl font-bold text-orange-600">{metrics.apiRequests.toLocaleString()}</p>
                </div>
                <Globe className="w-8 h-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Workflow Management Tabs */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="ai-agents">AI Agents</TabsTrigger>
          <TabsTrigger value="triggers">Autonomous Triggers</TabsTrigger>
          <TabsTrigger value="integrations">Integrations</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="triggers" className="space-y-4">
          <Card className="border-indigo-100 shadow-sm">
            <CardHeader className="bg-indigo-50/30 dark:bg-indigo-900/10">
              <div className="flex justify-between items-center">
                <div>
                  <CardTitle className="flex items-center gap-2">
                    <Zap className="w-5 h-5 text-yellow-500" />
                    Autonomous Trigger Mesh
                  </CardTitle>
                  <CardDescription>
                    Orchestrate self-initiating agent workflows via external signals and schedules.
                  </CardDescription>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" onClick={loadWorkflowData}>
                    <RefreshCw className="h-4 w-4 mr-2" /> Synced
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-6">
              <div className="space-y-6">
                {workflows.map(wf => (
                  <div key={wf.id} className="group relative p-5 border rounded-2xl bg-white dark:bg-gray-950 transition-all hover:border-indigo-300 hover:shadow-md">
                    <div className="flex justify-between items-start mb-5">
                      <div className="flex gap-4 items-center">
                        <div className="p-3 bg-indigo-50 dark:bg-indigo-900/30 rounded-xl">
                          {getTypeIcon(wf.type)}
                        </div>
                        <div>
                          <h3 className="font-bold text-lg text-gray-900 dark:text-gray-100 flex items-center gap-2">
                            {wf.name}
                            {wf.status === 'running' && <span className="flex h-2 w-2 rounded-full bg-green-500 animate-pulse" />}
                          </h3>
                          <p className="text-xs text-gray-400 font-mono">wf_{wf.id.substring(0, 8)}</p>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Badge variant="outline" className="bg-gray-50 dark:bg-gray-800 border-none px-3 py-1">
                          {wf.triggers?.length || 0} active signals
                        </Badge>
                        <Button
                          size="sm"
                          className="h-8 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-lg"
                          onClick={() => {
                            setEditingWorkflow(wf);
                            setTriggerModalOpen(true);
                          }}
                        >
                          <Plus className="h-4 w-4 mr-1.5" /> Add Signal
                        </Button>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {(wf.triggers || []).map((t, idx) => (
                        <div key={idx} className="group/item relative flex flex-col gap-3 p-4 bg-gray-50/50 dark:bg-white/[0.02] rounded-xl border border-gray-100 dark:border-gray-800 hover:bg-white dark:hover:bg-gray-900 transition-colors">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <div className="p-2 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-100 dark:border-gray-700">
                                {t.type === 'webhook' ? <Globe className="h-4 w-4 text-blue-500" /> :
                                  t.type === 'schedule' ? <Clock className="h-4 w-4 text-orange-500" /> :
                                    <Zap className="h-4 w-4 text-purple-500" />}
                              </div>
                              <span className="text-[10px] font-black uppercase text-gray-500 tracking-widest">{t.type}</span>
                            </div>
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-7 w-7 p-0 text-gray-300 hover:text-red-500 hover:bg-red-50"
                              onClick={() => handleDeleteTrigger(wf, idx)}
                            >
                              <Trash2 className="h-3.5 w-3.5" />
                            </Button>
                          </div>

                          <div className="space-y-2">
                            <div className="flex items-center gap-2">
                              <code className="flex-1 text-xs font-mono py-1 px-2 bg-white dark:bg-black/40 rounded border border-gray-100 dark:border-gray-800 truncate text-indigo-600 dark:text-indigo-400">
                                {t.path || t.cron || t.event_name}
                              </code>
                              {t.type === 'webhook' && (
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  className="h-7 w-7 p-0 hover:bg-indigo-50 text-gray-400 hover:text-indigo-600"
                                  onClick={() => {
                                    const url = `${process.env.NEXT_PUBLIC_API_URL || 'https://api.bizoholic.net'}/api/triggers/webhook${t.path}`;
                                    navigator.clipboard.writeText(url);
                                    toast.success('Webhook URL copied');
                                  }}
                                >
                                  <Copy className="h-3.5 w-3.5" />
                                </Button>
                              )}
                            </div>
                            {t.secret_key && (
                              <div className="flex items-center gap-1.5 px-2 py-1 bg-yellow-50/50 dark:bg-yellow-900/10 rounded border border-yellow-100 dark:border-yellow-900/20">
                                <Key className="h-3 w-3 text-yellow-600" />
                                <span className="text-[10px] font-mono text-yellow-700">Signed with Bizo-Key</span>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}

                      {(!wf.triggers || wf.triggers.length === 0) && (
                        <div className="col-span-full py-10 flex flex-col items-center justify-center border-2 border-dashed border-gray-100 dark:border-gray-800 rounded-2xl bg-gray-50/20">
                          <div className="h-12 w-12 rounded-full bg-white dark:bg-gray-900 flex items-center justify-center shadow-sm mb-3">
                            <Shield className="h-6 w-6 text-gray-200" />
                          </div>
                          <p className="text-sm font-medium text-gray-400 mb-4">No autonomous triggers active.</p>
                          <Button
                            variant="outline"
                            size="sm"
                            className="font-bold text-indigo-600 border-indigo-100 hover:bg-indigo-50"
                            onClick={() => {
                              setEditingWorkflow(wf);
                              setTriggerModalOpen(true);
                            }}
                          >
                            Set Initial Trigger
                          </Button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="overview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Activity className="w-5 h-5 mr-2" />
                All Workflows Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {workflows.map(workflow => (
                  <div key={workflow.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                    <div className="flex items-center space-x-4">
                      {getTypeIcon(workflow.type)}
                      <div>
                        <h3 className="font-medium">{workflow.name}</h3>
                        <div className="flex items-center space-x-2 text-sm text-gray-500">
                          {getStatusIcon(workflow.status)}
                          <span>Last run: {workflow.lastRun}</span>
                          <span>•</span>
                          <span>Next: {workflow.nextRun}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <p className="text-sm font-medium">{workflow.successRate}% success</p>
                        <p className="text-xs text-gray-500">{workflow.tenantCount} tenants</p>
                      </div>
                      <div className="flex space-x-1">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleWorkflowAction(workflow.id, 'start')}
                          disabled={workflow.status === 'running'}
                        >
                          <Play className="w-3 h-3" />
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleWorkflowAction(workflow.id, 'pause')}
                          disabled={workflow.status === 'paused'}
                        >
                          <Pause className="w-3 h-3" />
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleWorkflowAction(workflow.id, 'stop')}
                          disabled={workflow.status === 'stopped'}
                        >
                          <Square className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="ai-agents" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Zap className="w-5 h-5 mr-2" />
                AI Agent Workflows
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {workflows
                  .filter(wf => wf.type === 'ai-agent')
                  .map(workflow => (
                    <Card key={workflow.id} className="hover:shadow-md transition-shadow">
                      <CardHeader className="pb-3">
                        <div className="flex items-center justify-between">
                          <CardTitle className="text-sm">{workflow.name}</CardTitle>
                          {getStatusIcon(workflow.status)}
                        </div>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span>Success Rate:</span>
                            <span className="font-medium">{workflow.successRate}%</span>
                          </div>
                          <div className="flex justify-between text-sm">
                            <span>Executions:</span>
                            <span className="font-medium">{workflow.executionCount}</span>
                          </div>
                          <div className="flex justify-between text-sm">
                            <span>Tenants:</span>
                            <span className="font-medium">{workflow.tenantCount}</span>
                          </div>
                          <div className="flex justify-between text-sm">
                            <span>Next Run:</span>
                            <span className="font-medium">{workflow.nextRun}</span>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="integrations" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Globe className="w-5 h-5 mr-2" />
                Integration Workflows
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {workflows
                  .filter(wf => wf.type === 'integration')
                  .map(workflow => (
                    <div key={workflow.id} className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-medium">{workflow.name}</h3>
                          <p className="text-sm text-gray-500">
                            Serving {workflow.tenantCount} tenants • {workflow.executionCount} total executions
                          </p>
                        </div>
                        <Badge variant={workflow.status === 'running' ? 'default' : 'secondary'}>
                          {workflow.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Performance Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>Average Execution Time</span>
                    <span className="font-medium">{metrics?.avgExecutionTime}s</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Successful Runs (24h)</span>
                    <span className="font-medium text-green-600">{metrics?.successfulRuns}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Failed Runs (24h)</span>
                    <span className="font-medium text-red-600">{metrics?.failedRuns}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Active Users</span>
                    <span className="font-medium">{metrics?.activeUsers}</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>System Health</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Shield className="w-4 h-4 text-green-500" />
                      <span>Security Status</span>
                    </div>
                    <Badge variant="default">Secure</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Database className="w-4 h-4 text-blue-500" />
                      <span>Database Health</span>
                    </div>
                    <Badge variant="default">Healthy</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Globe className="w-4 h-4 text-purple-500" />
                      <span>API Gateway</span>
                    </div>
                    <Badge variant="default">Operational</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <DollarSign className="w-4 h-4 text-green-500" />
                      <span>Billing System</span>
                    </div>
                    <Badge variant="default">Active</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      {/* Trigger Configuration Dialog */}
      <Dialog open={triggerModalOpen} onOpenChange={setTriggerModalOpen}>
        <DialogContent className="sm:max-w-[425px] border-none shadow-2xl bg-white dark:bg-gray-950 p-0 overflow-hidden rounded-3xl">
          <div className="bg-indigo-600 p-8 text-white relative">
            <div className="absolute top-0 right-0 p-6 opacity-20">
              <Zap className="h-24 w-24 rotate-12" />
            </div>
            <DialogHeader className="space-y-1 relative z-10">
              <DialogTitle className="text-3xl font-black tracking-tight">Activate Workflow</DialogTitle>
              <DialogDescription className="text-indigo-100 text-base opacity-90">
                Setup a signal to drive <span className="font-bold underline decoration-indigo-300 decoration-2 underline-offset-4">{editingWorkflow?.name}</span>.
              </DialogDescription>
            </DialogHeader>
          </div>

          <div className="p-8 space-y-8 bg-white dark:bg-gray-950">
            <div className="grid gap-6">
              <div className="grid gap-3">
                <Label htmlFor="type" className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">Trigger Strategy</Label>
                <Select
                  value={newTrigger.type}
                  onValueChange={(v: any) => setNewTrigger({ ...newTrigger, type: v })}
                >
                  <SelectTrigger id="type" className="h-12 bg-gray-50 dark:bg-black/20 border-gray-100 dark:border-gray-800 rounded-xl focus:ring-indigo-500">
                    <SelectValue placeholder="Selection strategy" />
                  </SelectTrigger>
                  <SelectContent className="rounded-xl border-gray-100 dark:border-gray-800 shadow-xl">
                    <SelectItem value="webhook" className="py-3 px-4 focus:bg-indigo-50">🌐 Universal Webhook Hook</SelectItem>
                    <SelectItem value="schedule" className="py-3 px-4 focus:bg-indigo-50">⏰ Cron Schedule</SelectItem>
                    <SelectItem value="event" className="py-3 px-4 focus:bg-indigo-50">⚡ Platform Internal Event</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {newTrigger.type === 'webhook' && (
                <div className="space-y-6 animate-in fade-in slide-in-from-top-2">
                  <div className="grid gap-3">
                    <Label htmlFor="path" className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">Listener Path</Label>
                    <div className="flex flex-col gap-2">
                      <div className="flex items-center gap-2 bg-gray-50 dark:bg-black/20 border border-gray-100 dark:border-gray-800 rounded-xl px-4 py-3 group focus-within:ring-2 focus-within:ring-indigo-500 transition-all">
                        <span className="text-xs font-mono text-gray-400">/webhook</span>
                        <Input
                          id="path"
                          placeholder="/custom-endpoint"
                          className="flex-1 h-6 border-none bg-transparent p-0 text-sm font-mono focus-visible:ring-0 placeholder:text-gray-300"
                          value={newTrigger.path || ''}
                          onChange={(e) => setNewTrigger({ ...newTrigger, path: e.target.value })}
                        />
                      </div>
                      <p className="text-[10px] text-gray-400">Full URL: api.bizoholic.net/api/triggers/webhook{newTrigger.path || '...'}</p>
                    </div>
                  </div>
                  <div className="grid gap-3">
                    <Label htmlFor="secret" className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">Discovery Key (Optional)</Label>
                    <div className="relative">
                      <Key className="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-300" />
                      <Input
                        id="secret"
                        placeholder="X-Bizo-Key"
                        className="h-12 pl-11 bg-gray-50 dark:bg-black/20 border-gray-100 dark:border-gray-800 rounded-xl focus:ring-indigo-500"
                        value={newTrigger.secret_key || ''}
                        onChange={(e) => setNewTrigger({ ...newTrigger, secret_key: e.target.value })}
                      />
                    </div>
                  </div>
                </div>
              )}

              {newTrigger.type === 'schedule' && (
                <div className="grid gap-3 animate-in fade-in slide-in-from-top-2">
                  <Label htmlFor="cron" className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">Cron Configuration</Label>
                  <Input
                    id="cron"
                    placeholder="* * * * *"
                    className="h-12 bg-gray-50 dark:bg-black/20 border-gray-100 dark:border-gray-800 rounded-xl font-mono text-lg tracking-wider focus:ring-indigo-500"
                    value={newTrigger.cron || ''}
                    onChange={(e) => setNewTrigger({ ...newTrigger, cron: e.target.value })}
                  />
                  <div className="p-3 bg-indigo-50/50 dark:bg-indigo-900/10 rounded-lg flex items-start gap-3">
                    <Clock className="h-4 w-4 text-indigo-600 mt-0.5" />
                    <p className="text-xs text-indigo-700 leading-relaxed">Runs autonomously based on server time (UTC). Ensure the expression follows standard 5-part cron syntax.</p>
                  </div>
                </div>
              )}

              {newTrigger.type === 'event' && (
                <div className="grid gap-3 animate-in fade-in slide-in-from-top-2">
                  <Label htmlFor="event" className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">Event Topic</Label>
                  <Select
                    value={newTrigger.event_name}
                    onValueChange={(v) => setNewTrigger({ ...newTrigger, event_name: v })}
                  >
                    <SelectTrigger className="h-12 bg-gray-50 dark:bg-black/20 border-gray-100 dark:border-gray-800 rounded-xl">
                      <SelectValue placeholder="Select platform event" />
                    </SelectTrigger>
                    <SelectContent className="rounded-xl border-gray-100 dark:border-gray-800">
                      <SelectItem value="tenant.created">🏢 Tenant Onboarded</SelectItem>
                      <SelectItem value="payment.succeeded">💰 Payment Success</SelectItem>
                      <SelectItem value="agent.propose_workflow">🤖 AI Step Proposal</SelectItem>
                      <SelectItem value="system.anomaly_detected">⚠️ System Health Alert</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              )}
            </div>

            <DialogFooter className="flex-col sm:flex-row gap-3 pt-4">
              <Button
                variant="ghost"
                onClick={() => setTriggerModalOpen(false)}
                className="flex-1 h-12 rounded-xl font-bold text-gray-500 hover:bg-gray-50"
              >
                Dismiss
              </Button>
              <Button
                className="flex-[2] h-12 bg-indigo-600 hover:bg-indigo-700 text-white font-black rounded-xl shadow-xl shadow-indigo-200 dark:shadow-none transition-all transform hover:translate-y-[-2px] active:translate-y-[0px]"
                onClick={handleSaveTriggers}
              >
                Integrate Trigger
              </Button>
            </DialogFooter>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}