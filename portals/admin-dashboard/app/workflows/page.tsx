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
  DollarSign
} from 'lucide-react';

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

  useEffect(() => {
    loadWorkflowData();
    const interval = setInterval(loadWorkflowData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadWorkflowData = async () => {
    try {
      setLoading(true);
      const res = await adminApi.getWorkflows();

      if (res.data) {
        // Transform API data to UI model if needed, or use directly if matching
        // Assuming API returns comparable structure. We might need to map 'type'
        const mapped: WorkflowStatus[] = res.data.map((w: any) => ({
          id: w.id,
          name: w.name,
          type: (w.type?.toLowerCase() || 'system') as any, // fallback
          status: w.status,
          lastRun: w.lastRun ? new Date(w.lastRun).toLocaleString() : 'Never',
          nextRun: 'Scheduled', // API might not return next_run yet
          successRate: w.successRate || 0,
          executionCount: w.runsToday || 0,
          tenantCount: 1 // Default for now
        }));
        setWorkflows(mapped);

        // Calculate metrics
        setMetrics({
          totalWorkflows: mapped.length,
          activeWorkflows: mapped.filter(w => w.status === 'running').length,
          successfulRuns: mapped.reduce((acc, w) => acc + (w.executionCount || 0), 0), // Mock calc
          failedRuns: 0,
          avgExecutionTime: 0,
          totalTenants: 1,
          activeUsers: 0,
          apiRequests: 0
        });
      }
    } catch (error) {
      console.error('Error loading workflow data:', error);
      toast.error('Failed to load workflows');
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
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="ai-agents">AI Agents</TabsTrigger>
          <TabsTrigger value="integrations">Integrations</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

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
    </div>
  );
}