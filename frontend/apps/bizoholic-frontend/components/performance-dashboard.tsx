'use client'

import React, { useEffect, useState, useRef } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Progress } from '@/components/ui/progress'
import { 
  BarChart3,
  Activity,
  Clock,
  Zap,
  TrendingUp,
  TrendingDown,
  Minus,
  RefreshCw,
  Download,
  Filter
} from 'lucide-react'
import { usePerformanceMetrics, useWorkflowUpdates } from '@/lib/websocket'
import { useAuthStore } from '@/lib/auth-store'
import mermaid from 'mermaid'

interface PerformanceMetric {
  name: string
  value: number
  unit: string
  change?: number
  trend?: 'up' | 'down' | 'neutral'
  target?: number
}

interface WorkflowPerformance {
  workflowId: string
  workflowType: string
  platform: string
  status: string
  duration: number
  completionRate: number
  agentEfficiency: number
  errorRate: number
  startTime: string
  endTime?: string
}

interface PerformanceDashboardProps {
  className?: string
  companyId?: string
  timeRange?: '1h' | '24h' | '7d' | '30d'
  platforms?: string[]
  autoRefresh?: boolean
  refreshInterval?: number
}

const PerformanceDashboard: React.FC<PerformanceDashboardProps> = ({
  className = '',
  companyId,
  timeRange = '24h',
  platforms = ['bizoholic', 'coreldove', 'thrillring'],
  autoRefresh = true,
  refreshInterval = 30000
}) => {
  // State
  const [metrics, setMetrics] = useState<Record<string, PerformanceMetric>>({})
  const [workflowPerformance, setWorkflowPerformance] = useState<WorkflowPerformance[]>([])
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date())
  const [selectedTimeRange, setSelectedTimeRange] = useState(timeRange)
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(platforms)
  
  // Refs
  const chartRef = useRef<HTMLDivElement>(null)
  const refreshTimeoutRef = useRef<NodeJS.Timeout>()
  
  // Auth
  const { user, token } = useAuthStore()

  // WebSocket subscriptions
  usePerformanceMetrics((data) => {
    console.log('Performance metrics received:', data)
    updateMetrics(data)
  })

  useWorkflowUpdates((data) => {
    console.log('Workflow update received:', data)
    updateWorkflowPerformance(data)
  })

  // Initialize component
  useEffect(() => {
    if (token) {
      fetchInitialData()
    }
  }, [token, selectedTimeRange, selectedPlatforms])

  // Auto-refresh setup
  useEffect(() => {
    if (autoRefresh) {
      refreshTimeoutRef.current = setInterval(() => {
        fetchPerformanceData()
      }, refreshInterval)

      return () => {
        if (refreshTimeoutRef.current) {
          clearInterval(refreshTimeoutRef.current)
        }
      }
    }
  }, [autoRefresh, refreshInterval])

  // Mermaid chart rendering
  useEffect(() => {
    if (Object.keys(metrics).length > 0) {
      renderPerformanceChart()
    }
  }, [metrics])

  const fetchInitialData = async () => {
    setLoading(true)
    try {
      await Promise.all([
        fetchPerformanceData(),
        fetchWorkflowHistory()
      ])
    } catch (error) {
      console.error('Failed to fetch initial data:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchPerformanceData = async () => {
    if (!token) return

    try {
      const response = await fetch('/api/v1/workflows/performance/metrics', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          time_range: selectedTimeRange,
          platforms: selectedPlatforms,
          metrics_types: [
            'avg_execution_time',
            'completion_rate',
            'error_rate',
            'agent_efficiency',
            'throughput',
            'memory_usage',
            'cpu_usage'
          ]
        })
      })

      if (response.ok) {
        const data = await response.json()
        updateMetrics(data.metrics)
      }
    } catch (error) {
      console.error('Failed to fetch performance data:', error)
    }
  }

  const fetchWorkflowHistory = async () => {
    if (!token || !user?.companyId) return

    try {
      const response = await fetch(`/api/v1/workflows/visualization/company/${user.companyId}/active`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        const workflows = Object.values(data.active_workflows) as any[]
        setWorkflowPerformance(workflows.map(wf => ({
          workflowId: wf.workflow_id,
          workflowType: wf.workflow_type,
          platform: wf.platform || 'bizoholic',
          status: wf.status,
          duration: wf.duration || 0,
          completionRate: wf.progress_percentage || 0,
          agentEfficiency: Math.random() * 100, // Mock data
          errorRate: Math.random() * 10, // Mock data
          startTime: wf.start_time,
          endTime: wf.end_time
        })))
      }
    } catch (error) {
      console.error('Failed to fetch workflow history:', error)
    }
  }

  const updateMetrics = (newMetrics: Record<string, any>) => {
    const formattedMetrics: Record<string, PerformanceMetric> = {}
    
    for (const [key, value] of Object.entries(newMetrics)) {
      if (typeof value === 'number') {
        formattedMetrics[key] = {
          name: formatMetricName(key),
          value: value,
          unit: getMetricUnit(key),
          change: Math.random() * 20 - 10, // Mock change data
          trend: Math.random() > 0.5 ? 'up' : 'down',
          target: getMetricTarget(key)
        }
      }
    }
    
    setMetrics(prevMetrics => ({ ...prevMetrics, ...formattedMetrics }))
    setLastUpdated(new Date())
  }

  const updateWorkflowPerformance = (workflowData: any) => {
    if (workflowData.workflow_state) {
      const wf = workflowData.workflow_state
      const newPerformance: WorkflowPerformance = {
        workflowId: wf.workflow_id,
        workflowType: wf.workflow_type,
        platform: workflowData.platform || 'bizoholic',
        status: wf.status,
        duration: calculateDuration(wf.start_time, wf.end_time),
        completionRate: wf.progress_percentage || 0,
        agentEfficiency: calculateAgentEfficiency(wf.nodes),
        errorRate: calculateErrorRate(wf.nodes),
        startTime: wf.start_time,
        endTime: wf.end_time
      }

      setWorkflowPerformance(prev => {
        const index = prev.findIndex(p => p.workflowId === newPerformance.workflowId)
        if (index !== -1) {
          const updated = [...prev]
          updated[index] = newPerformance
          return updated
        } else {
          return [newPerformance, ...prev.slice(0, 9)] // Keep last 10
        }
      })
    }
  }

  const renderPerformanceChart = async () => {
    if (!chartRef.current || Object.keys(metrics).length === 0) return

    try {
      const chartData = Object.entries(metrics)
        .filter(([_, metric]) => typeof metric.value === 'number')
        .slice(0, 8) // Limit to 8 metrics for readability

      const mermaidChart = `
        graph TD
          subgraph "Performance Metrics"
            ${chartData.map(([key, metric], index) => 
              `M${index}["${metric.name}: ${metric.value.toFixed(2)}${metric.unit}"]`
            ).join('\n            ')}
          end
          
          ${chartData.map((_, index) => 
            index < chartData.length - 1 ? `M${index} --> M${index + 1}` : ''
          ).join('\n          ')}
          
          classDef high fill:#22c55e,stroke:#16a34a,color:#ffffff
          classDef medium fill:#eab308,stroke:#ca8a04,color:#ffffff  
          classDef low fill:#ef4444,stroke:#dc2626,color:#ffffff
          
          ${chartData.map(([_, metric], index) => {
            if (metric.target && metric.value >= metric.target * 0.9) return `class M${index} high`
            if (metric.target && metric.value >= metric.target * 0.7) return `class M${index} medium`
            return `class M${index} low`
          }).join('\n          ')}
      `

      const diagramId = `performance-chart-${Date.now()}`
      const { svg } = await mermaid.render(diagramId, mermaidChart)
      
      chartRef.current.innerHTML = svg
    } catch (error) {
      console.error('Failed to render performance chart:', error)
    }
  }

  // Helper functions
  const formatMetricName = (key: string): string => {
    return key.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ')
  }

  const getMetricUnit = (key: string): string => {
    if (key.includes('time')) return 's'
    if (key.includes('rate') || key.includes('percentage')) return '%'
    if (key.includes('memory')) return 'MB'
    if (key.includes('cpu')) return '%'
    if (key.includes('throughput')) return '/min'
    return ''
  }

  const getMetricTarget = (key: string): number => {
    const targets: Record<string, number> = {
      'avg_execution_time': 60,
      'completion_rate': 95,
      'error_rate': 5,
      'agent_efficiency': 90,
      'throughput': 10,
      'memory_usage': 512,
      'cpu_usage': 80
    }
    return targets[key] || 100
  }

  const calculateDuration = (startTime: string, endTime?: string): number => {
    if (!endTime) return 0
    return (new Date(endTime).getTime() - new Date(startTime).getTime()) / 1000
  }

  const calculateAgentEfficiency = (nodes: Record<string, any>): number => {
    const nodeValues = Object.values(nodes)
    const completedNodes = nodeValues.filter((node: any) => node.status === 'completed')
    return nodeValues.length > 0 ? (completedNodes.length / nodeValues.length) * 100 : 0
  }

  const calculateErrorRate = (nodes: Record<string, any>): number => {
    const nodeValues = Object.values(nodes)
    const failedNodes = nodeValues.filter((node: any) => node.status === 'failed')
    return nodeValues.length > 0 ? (failedNodes.length / nodeValues.length) * 100 : 0
  }

  const getTrendIcon = (trend?: string) => {
    switch (trend) {
      case 'up': return <TrendingUp className="w-4 h-4 text-green-600" />
      case 'down': return <TrendingDown className="w-4 h-4 text-red-600" />
      default: return <Minus className="w-4 h-4 text-gray-400" />
    }
  }

  const formatTimeAgo = (date: Date): string => {
    const seconds = Math.floor((Date.now() - date.getTime()) / 1000)
    if (seconds < 60) return `${seconds}s ago`
    const minutes = Math.floor(seconds / 60)
    if (minutes < 60) return `${minutes}m ago`
    const hours = Math.floor(minutes / 60)
    return `${hours}h ago`
  }

  if (loading) {
    return (
      <Card className={className}>
        <CardContent className="flex items-center justify-center h-64">
          <div className="text-center">
            <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-2 text-blue-600" />
            <p className="text-gray-600">Loading performance data...</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className={`performance-dashboard space-y-6 ${className}`}>
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="w-5 h-5 text-blue-600" />
              <span>Performance Dashboard</span>
            </CardTitle>
            <div className="flex items-center space-x-2">
              <Badge variant="outline" className="text-xs">
                <Activity className="w-3 h-3 mr-1" />
                Live Updates
              </Badge>
              <span className="text-xs text-gray-500">
                Updated {formatTimeAgo(lastUpdated)}
              </span>
              <Button size="sm" variant="outline" onClick={fetchPerformanceData}>
                <RefreshCw className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="metrics">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="metrics">Key Metrics</TabsTrigger>
              <TabsTrigger value="workflows">Workflow Performance</TabsTrigger>
              <TabsTrigger value="charts">Visual Analytics</TabsTrigger>
            </TabsList>

            <TabsContent value="metrics" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {Object.entries(metrics).slice(0, 8).map(([key, metric]) => (
                  <Card key={key} className="hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-600">
                          {metric.name}
                        </span>
                        {getTrendIcon(metric.trend)}
                      </div>
                      <div className="text-2xl font-bold">
                        {metric.value.toFixed(2)}{metric.unit}
                      </div>
                      {metric.target && (
                        <Progress 
                          value={(metric.value / metric.target) * 100} 
                          className="mt-2 h-2"
                        />
                      )}
                      {metric.change !== undefined && (
                        <div className={`text-xs mt-1 ${
                          metric.change > 0 ? 'text-green-600' : 
                          metric.change < 0 ? 'text-red-600' : 'text-gray-600'
                        }`}>
                          {metric.change > 0 ? '+' : ''}{metric.change.toFixed(1)}% from last period
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="workflows" className="space-y-4">
              <div className="space-y-2">
                {workflowPerformance.length > 0 ? (
                  workflowPerformance.slice(0, 10).map((workflow) => (
                    <Card key={workflow.workflowId} className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <Badge variant="outline" className="text-xs">
                            {workflow.platform}
                          </Badge>
                          <div>
                            <h4 className="font-medium">
                              {workflow.workflowType.replace('_', ' ')}
                            </h4>
                            <p className="text-sm text-gray-600">
                              ID: {workflow.workflowId.slice(0, 8)}...
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-4 text-sm">
                          <div className="text-center">
                            <div className="font-medium">Duration</div>
                            <div className="text-gray-600">
                              {Math.floor(workflow.duration / 60)}:{(workflow.duration % 60).toFixed(0).padStart(2, '0')}
                            </div>
                          </div>
                          <div className="text-center">
                            <div className="font-medium">Completion</div>
                            <div className="text-gray-600">{workflow.completionRate.toFixed(1)}%</div>
                          </div>
                          <div className="text-center">
                            <div className="font-medium">Efficiency</div>
                            <div className="text-gray-600">{workflow.agentEfficiency.toFixed(1)}%</div>
                          </div>
                          <Badge 
                            variant={workflow.status === 'completed' ? 'default' : 
                                    workflow.status === 'failed' ? 'destructive' : 'secondary'}
                            className="capitalize"
                          >
                            {workflow.status}
                          </Badge>
                        </div>
                      </div>
                    </Card>
                  ))
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <Activity className="w-8 h-8 mx-auto mb-2" />
                    <p>No workflow performance data available</p>
                  </div>
                )}
              </div>
            </TabsContent>

            <TabsContent value="charts" className="space-y-4">
              <div 
                ref={chartRef}
                className="performance-chart border rounded-lg p-4 bg-gray-50 min-h-[400px]"
              />
              {Object.keys(metrics).length === 0 && (
                <div className="flex items-center justify-center h-64 text-gray-500">
                  <div className="text-center">
                    <BarChart3 className="w-8 h-8 mx-auto mb-2" />
                    <p>No performance data available for visualization</p>
                  </div>
                </div>
              )}
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}

export default PerformanceDashboard