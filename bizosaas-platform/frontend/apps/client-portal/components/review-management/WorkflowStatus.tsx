"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import {
  Play,
  Pause,
  Square,
  RefreshCw,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle,
  Loader2,
  Eye
} from 'lucide-react';

interface WorkflowExecution {
  id: string;
  type: string;
  status: 'running' | 'completed' | 'failed' | 'cancelled' | 'paused';
  startedAt: string;
  completedAt?: string;
  progress: number;
  details: string;
  result?: any;
  error?: string;
}

export default function WorkflowStatus() {
  const [workflows, setWorkflows] = useState<WorkflowExecution[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchWorkflows();
    const interval = setInterval(fetchWorkflows, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchWorkflows = async () => {
    try {
      const response = await fetch('/api/brain/review-management/workflows');
      const data = await response.json();
      setWorkflows(data.workflows || []);
    } catch (error) {
      console.error('Failed to fetch workflows:', error);
    } finally {
      setLoading(false);
    }
  };

  const controlWorkflow = async (workflowId: string, action: 'pause' | 'resume' | 'cancel') => {
    try {
      await fetch(`/api/brain/review-management/workflows/${workflowId}/${action}`, {
        method: 'POST'
      });
      fetchWorkflows();
    } catch (error) {
      console.error(`Failed to ${action} workflow:`, error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'failed': return 'bg-red-100 text-red-800';
      case 'cancelled': return 'bg-gray-100 text-gray-800';
      case 'paused': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <Loader2 className="h-4 w-4 animate-spin" />;
      case 'completed': return <CheckCircle className="h-4 w-4" />;
      case 'failed': return <XCircle className="h-4 w-4" />;
      case 'cancelled': return <Square className="h-4 w-4" />;
      case 'paused': return <Pause className="h-4 w-4" />;
      default: return <Clock className="h-4 w-4" />;
    }
  };

  const getWorkflowTypeDisplay = (type: string) => {
    return type.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  const activeWorkflows = workflows.filter(w => w.status === 'running' || w.status === 'paused');
  const completedWorkflows = workflows.filter(w => w.status === 'completed');
  const failedWorkflows = workflows.filter(w => w.status === 'failed');

  if (loading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-8">
          <Loader2 className="h-6 w-6 animate-spin mr-2" />
          <span>Loading workflow status...</span>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center">
          <div>
            <CardTitle>Temporal Workflow Status</CardTitle>
            <CardDescription>
              Monitor active and recent workflow executions
            </CardDescription>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={fetchWorkflows}>
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {workflows.length === 0 ? (
          <div className="text-center py-8">
            <Clock className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">No Workflows</h3>
            <p className="text-muted-foreground">
              No workflow executions found. Start a review collection or response generation to see workflows here.
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Summary Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="text-center p-3 border rounded-lg">
                <div className="text-xl font-bold text-blue-600">{activeWorkflows.length}</div>
                <div className="text-sm text-muted-foreground">Active</div>
              </div>
              <div className="text-center p-3 border rounded-lg">
                <div className="text-xl font-bold text-green-600">{completedWorkflows.length}</div>
                <div className="text-sm text-muted-foreground">Completed</div>
              </div>
              <div className="text-center p-3 border rounded-lg">
                <div className="text-xl font-bold text-red-600">{failedWorkflows.length}</div>
                <div className="text-sm text-muted-foreground">Failed</div>
              </div>
              <div className="text-center p-3 border rounded-lg">
                <div className="text-xl font-bold text-gray-600">{workflows.length}</div>
                <div className="text-sm text-muted-foreground">Total</div>
              </div>
            </div>

            {/* Active Workflows */}
            {activeWorkflows.length > 0 && (
              <div className="space-y-4">
                <h4 className="text-sm font-medium">Active Workflows</h4>
                {activeWorkflows.map((workflow) => (
                  <div key={workflow.id} className="border rounded-lg p-4 space-y-3">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h5 className="font-medium">{getWorkflowTypeDisplay(workflow.type)}</h5>
                          <Badge className={getStatusColor(workflow.status)}>
                            {getStatusIcon(workflow.status)}
                            <span className="ml-1">{workflow.status}</span>
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground">{workflow.details}</p>
                        <div className="text-xs text-muted-foreground mt-1">
                          Started: {new Date(workflow.startedAt).toLocaleString()}
                        </div>
                      </div>
                      <div className="flex gap-2">
                        {workflow.status === 'running' && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => controlWorkflow(workflow.id, 'pause')}
                          >
                            <Pause className="h-4 w-4" />
                          </Button>
                        )}
                        {workflow.status === 'paused' && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => controlWorkflow(workflow.id, 'resume')}
                          >
                            <Play className="h-4 w-4" />
                          </Button>
                        )}
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => controlWorkflow(workflow.id, 'cancel')}
                        >
                          <Square className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                    
                    {workflow.progress > 0 && (
                      <div className="space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="text-xs font-medium">Progress</span>
                          <span className="text-xs text-muted-foreground">{workflow.progress}%</span>
                        </div>
                        <Progress value={workflow.progress} className="h-2" />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Recent Workflows */}
            {(completedWorkflows.length > 0 || failedWorkflows.length > 0) && (
              <div className="space-y-4">
                <h4 className="text-sm font-medium">Recent Workflows</h4>
                {[...completedWorkflows, ...failedWorkflows]
                  .sort((a, b) => new Date(b.startedAt).getTime() - new Date(a.startedAt).getTime())
                  .slice(0, 5)
                  .map((workflow) => (
                    <div key={workflow.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h5 className="font-medium">{getWorkflowTypeDisplay(workflow.type)}</h5>
                            <Badge className={getStatusColor(workflow.status)}>
                              {getStatusIcon(workflow.status)}
                              <span className="ml-1">{workflow.status}</span>
                            </Badge>
                          </div>
                          <p className="text-sm text-muted-foreground">{workflow.details}</p>
                          <div className="text-xs text-muted-foreground mt-1">
                            Started: {new Date(workflow.startedAt).toLocaleString()}
                            {workflow.completedAt && (
                              <span> • Completed: {new Date(workflow.completedAt).toLocaleString()}</span>
                            )}
                          </div>
                          {workflow.error && (
                            <div className="text-xs text-red-600 mt-1 p-2 bg-red-50 rounded">
                              Error: {workflow.error}
                            </div>
                          )}
                        </div>
                        {workflow.result && (
                          <Button size="sm" variant="outline">
                            <Eye className="h-4 w-4 mr-1" />
                            View Result
                          </Button>
                        )}
                      </div>
                    </div>
                  ))}
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}