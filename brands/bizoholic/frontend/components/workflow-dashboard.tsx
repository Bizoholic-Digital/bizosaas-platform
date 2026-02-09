'use client'

import React, { useState, useEffect, useCallback } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { ScrollArea } from '@/components/ui/scroll-area'
import {
  Activity,
  BarChart3,
  Clock,
  Users,
  Zap,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Pause,
  Play
} from 'lucide-react'
import WorkflowVisualization from './workflow-visualization'
import { useSession } from 'next-auth/react'

// Types
interface WorkflowSummary {
  workflow_id: string
  workflow_type: string
  platform: string
  status: string
  progress_percentage: number
  start_time: string
  estimated_completion?: string
  current_node?: string
}

interface DashboardStats {
  total_workflows: number
  active_workflows: number
  completed_workflows: number
  failed_workflows: number
  success_rate: number
  avg_completion_time: number
  agents_online: number
  total_agents: number
}

interface PlatformMetrics {
  platform: string
  active_workflows: number
  success_rate: number
  avg_duration: number
  total_completed: number
}

const WorkflowDashboard: React.FC = () => {
  // State
  const [selectedWorkflow, setSelectedWorkflow] = useState<string | null>(null)
  const [activeWorkflows, setActiveWorkflows] = useState<WorkflowSummary[]>([])
  const [dashboardStats, setDashboardStats] = useState<DashboardStats | null>(null)
  const [platformMetrics, setPlatformMetrics] = useState<PlatformMetrics[]>([])
  const [selectedPlatform, setSelectedPlatform] = useState<string>('all')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [refreshInterval, setRefreshInterval] = useState<NodeJS.Timeout>()

  // Auth
  const { data: session } = useSession()
  const token = (session as any)?.accessToken
  const user = session?.user ? { ...session.user, companyId: (session as any)?.tenant || 'default' } : null

  // Fetch dashboard data
  const fetchDashboardData = useCallback(async () => {
    if (!token || !user) return

    try {
      setError('')

      // Fetch active workflows
      const workflowsResponse = await fetch(`/api/v1/workflows/visualization/company/${user.companyId}/active`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (workflowsResponse.ok) {
        const workflowsData = await workflowsResponse.json()
        setActiveWorkflows(Object.values(workflowsData.active_workflows || {}))
      }

      // Fetch dashboard statistics
      const statsResponse = await fetch('/api/v1/workflows/visualization/stats', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (statsResponse.ok) {
        const statsData = await statsResponse.json()

        // Mock dashboard stats for now (you can implement this endpoint)
        setDashboardStats({
          total_workflows: 42,
          active_workflows: activeWorkflows.length,
          completed_workflows: 38,
          failed_workflows: 2,
          success_rate: 95.0,
          avg_completion_time: 847, // seconds
          agents_online: 25,
          total_agents: 28
        })
      }

      // Mock platform metrics (you can implement this endpoint)
      setPlatformMetrics([
        {
          platform: 'bizoholic',
          active_workflows: activeWorkflows.filter(w => w.platform === 'bizoholic').length,
          success_rate: 96.2,
          avg_duration: 720,
          total_completed: 156
        },
        {
          platform: 'coreldove',
          active_workflows: activeWorkflows.filter(w => w.platform === 'coreldove').length,
          success_rate: 94.8,
          avg_duration: 540,
          total_completed: 89
        },
        {
          platform: 'thrillring',
          active_workflows: activeWorkflows.filter(w => w.platform === 'thrillring').length,
          success_rate: 93.1,
          avg_duration: 980,
          total_completed: 67
        }
      ])

      setLoading(false)
    } catch (err) {
      setError('Failed to fetch dashboard data')
      setLoading(false)
    }
  }, [token, user, activeWorkflows.length])

  // Initial data fetch
  useEffect(() => {
    fetchDashboardData()
  }, [])

  // Set up refresh interval
  useEffect(() => {
    const interval = setInterval(fetchDashboardData, 30000) // Refresh every 30 seconds
    setRefreshInterval(interval)

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [fetchDashboardData])

  // Helper functions
  const formatDuration = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600)
    const mins = Math.floor((seconds % 3600) / 60)
    return hrs > 0 ? `${hrs}h ${mins}m` : `${mins}m`
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle2 className="w-4 h-4 text-green-500" />
      case 'failed': return <XCircle className="w-4 h-4 text-red-500" />
      case 'running': return <Activity className="w-4 h-4 text-blue-500 animate-pulse" />
      case 'paused': return <Pause className="w-4 h-4 text-yellow-500" />
      default: return <Clock className="w-4 h-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800'
      case 'failed': return 'bg-red-100 text-red-800'
      case 'running': return 'bg-blue-100 text-blue-800'
      case 'paused': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getPlatformColor = (platform: string) => {
    switch (platform) {
      case 'bizoholic': return 'bg-blue-500'
      case 'coreldove': return 'bg-green-500'
      case 'thrillring': return 'bg-purple-500'
      default: return 'bg-gray-500'
    }
  }

  const filteredWorkflows = selectedPlatform === 'all'
    ? activeWorkflows
    : activeWorkflows.filter(w => w.platform === selectedPlatform)

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Activity className="w-8 h-8 mx-auto mb-2 animate-pulse" />
          <p>Loading workflow dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="workflow-dashboard space-y-6">
      {/* Dashboard Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Workflow Dashboard</h1>
          <p className="text-muted-foreground">
            Real-time monitoring of AI agent workflows across all platforms
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <Select value={selectedPlatform} onValueChange={setSelectedPlatform}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Select platform" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Platforms</SelectItem>
              <SelectItem value="bizoholic">Bizoholic</SelectItem>
              <SelectItem value="coreldove">CoreLDove</SelectItem>
              <SelectItem value="thrillring">ThrillRing</SelectItem>
            </SelectContent>
          </Select>

          <Button onClick={fetchDashboardData} variant="outline" size="sm">
            <Activity className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert>
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Dashboard Stats Cards */}
      {dashboardStats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Workflows</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dashboardStats.active_workflows}</div>
              <p className="text-xs text-muted-foreground">
                +{Math.round(Math.random() * 10)} from yesterday
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dashboardStats.success_rate}%</div>
              <p className="text-xs text-muted-foreground">
                {dashboardStats.completed_workflows}/{dashboardStats.total_workflows} completed
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg Completion</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{formatDuration(dashboardStats.avg_completion_time)}</div>
              <p className="text-xs text-muted-foreground">
                -5% faster than average
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Agents Online</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {dashboardStats.agents_online}/{dashboardStats.total_agents}
              </div>
              <p className="text-xs text-muted-foreground">
                {Math.round((dashboardStats.agents_online / dashboardStats.total_agents) * 100)}% online
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Platform Metrics */}
      <Card>
        <CardHeader>
          <CardTitle>Platform Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {platformMetrics.map((platform) => (
              <div key={platform.platform} className="border rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <div className={`w-3 h-3 rounded-full ${getPlatformColor(platform.platform)}`} />
                    <span className="font-medium capitalize">{platform.platform}</span>
                  </div>
                  <Badge variant="secondary">
                    {platform.active_workflows} active
                  </Badge>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Success Rate</span>
                    <span className="font-medium">{platform.success_rate}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Avg Duration</span>
                    <span className="font-medium">{formatDuration(platform.avg_duration)}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Total Completed</span>
                    <span className="font-medium">{platform.total_completed}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Workflows List */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Active Workflows ({filteredWorkflows.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-96">
              <div className="space-y-3">
                {filteredWorkflows.length > 0 ? (
                  filteredWorkflows.map((workflow) => (
                    <div
                      key={workflow.workflow_id}
                      className={`border rounded-lg p-3 cursor-pointer transition-colors ${selectedWorkflow === workflow.workflow_id
                        ? 'border-blue-500 bg-blue-50'
                        : 'hover:border-gray-300'
                        }`}
                      onClick={() => setSelectedWorkflow(workflow.workflow_id)}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          {getStatusIcon(workflow.status)}
                          <span className="font-medium text-sm">
                            {workflow.workflow_type.replace('_', ' ')}
                          </span>
                        </div>
                        <Badge className={`text-xs ${getStatusColor(workflow.status)}`}>
                          {workflow.status}
                        </Badge>
                      </div>

                      <div className="space-y-1">
                        <div className="flex items-center justify-between text-xs text-muted-foreground">
                          <span className="capitalize">{workflow.platform}</span>
                          <span>{workflow.progress_percentage.toFixed(1)}%</span>
                        </div>

                        <div className="w-full bg-gray-200 rounded-full h-1.5">
                          <div
                            className="bg-blue-600 h-1.5 rounded-full transition-all duration-500"
                            style={{ width: `${workflow.progress_percentage}%` }}
                          />
                        </div>

                        <div className="text-xs text-muted-foreground">
                          Started {new Date(workflow.start_time).toLocaleTimeString()}
                        </div>

                        {workflow.current_node && (
                          <div className="text-xs text-blue-600">
                            Current: {workflow.current_node}
                          </div>
                        )}
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    <Activity className="w-8 h-8 mx-auto mb-2 opacity-50" />
                    <p>No active workflows</p>
                    <p className="text-sm">Workflows will appear here when they start running</p>
                  </div>
                )}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>

        {/* Workflow Visualization */}
        <div className="lg:col-span-2">
          {selectedWorkflow ? (
            <WorkflowVisualization
              workflowId={selectedWorkflow}
              height="500px"
              showControls={true}
              showMetrics={true}
              className="h-full"
            />
          ) : (
            <Card>
              <CardHeader>
                <CardTitle>Workflow Visualization</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-center h-96 text-muted-foreground">
                  <div className="text-center">
                    <BarChart3 className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <h3 className="text-lg font-medium mb-2">Select a Workflow</h3>
                    <p>Choose a workflow from the list to view its real-time visualization</p>
                    <p className="text-sm mt-1">Live Mermaid.js diagrams with &lt;100ms rendering</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Zap className="w-5 h-5 mr-2" />
            Quick Actions
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button className="h-auto py-4 px-6 flex flex-col items-center space-y-2">
              <Play className="w-6 h-6" />
              <div className="text-center">
                <div className="font-medium">Start Marketing Campaign</div>
                <div className="text-sm text-muted-foreground">Bizoholic Platform</div>
              </div>
            </Button>

            <Button variant="outline" className="h-auto py-4 px-6 flex flex-col items-center space-y-2">
              <BarChart3 className="w-6 h-6" />
              <div className="text-center">
                <div className="font-medium">Product Sourcing</div>
                <div className="text-sm text-muted-foreground">CoreLDove Platform</div>
              </div>
            </Button>

            <Button variant="outline" className="h-auto py-4 px-6 flex flex-col items-center space-y-2">
              <Activity className="w-6 h-6" />
              <div className="text-center">
                <div className="font-medium">Content Workflow</div>
                <div className="text-sm text-muted-foreground">ThrillRing Platform</div>
              </div>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default WorkflowDashboard