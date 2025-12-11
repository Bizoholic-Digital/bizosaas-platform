'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Badge } from '../ui/badge'
import { Button } from '../ui/button'
import { Agent } from '../../lib/stores/agent-store'
import {
  BarChart3,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertTriangle,
  Zap,
  Target,
  Activity,
  Calendar,
  Download,
  RefreshCw
} from 'lucide-react'

interface AgentMetricsProps {
  agents: Agent[]
  selectedAgent: string | null
}

interface MetricData {
  label: string
  value: number
  change: number
  unit: string
  trend: 'up' | 'down' | 'stable'
}

export function AgentMetrics({ agents, selectedAgent }: AgentMetricsProps) {
  const [timeRange, setTimeRange] = useState('24h')
  const [selectedMetric, setSelectedMetric] = useState('performance')
  const [isLoading, setIsLoading] = useState(false)

  // Mock performance data for demonstration
  const performanceData = [
    { time: '00:00', value: 94 },
    { time: '04:00', value: 96 },
    { time: '08:00', value: 92 },
    { time: '12:00', value: 98 },
    { time: '16:00', value: 95 },
    { time: '20:00', value: 97 },
    { time: '24:00', value: 96 }
  ]

  const taskCompletionData = [
    { hour: '00', completed: 45, failed: 2 },
    { hour: '04', completed: 52, failed: 1 },
    { hour: '08', completed: 78, failed: 3 },
    { hour: '12', completed: 89, failed: 2 },
    { hour: '16', completed: 67, failed: 4 },
    { hour: '20', completed: 56, failed: 1 },
    { hour: '24', completed: 34, failed: 0 }
  ]

  const getOverallMetrics = (): MetricData[] => {
    const activeAgents = agents.filter(a => a.status === 'active')
    const totalTasks = agents.reduce((sum, a) => sum + a.tasksCompleted, 0)
    const avgPerformance = agents.reduce((sum, a) => sum + a.performance, 0) / agents.length
    const avgResponseTime = agents.reduce((sum, a) => sum + (a.avgResponseTime || 150), 0) / agents.length
    const avgSuccessRate = agents.reduce((sum, a) => sum + a.successRate, 0) / agents.length

    return [
      {
        label: 'Average Performance',
        value: Math.round(avgPerformance),
        change: 5.2,
        unit: '%',
        trend: 'up'
      },
      {
        label: 'Total Tasks Completed',
        value: totalTasks,
        change: 12.8,
        unit: '',
        trend: 'up'
      },
      {
        label: 'Average Response Time',
        value: Math.round(avgResponseTime),
        change: -8.4,
        unit: 'ms',
        trend: 'up'
      },
      {
        label: 'Success Rate',
        value: Math.round(avgSuccessRate),
        change: 2.1,
        unit: '%',
        trend: 'up'
      },
      {
        label: 'Active Agents',
        value: activeAgents.length,
        change: 0,
        unit: '',
        trend: 'stable'
      },
      {
        label: 'System Uptime',
        value: 99.8,
        change: 0.1,
        unit: '%',
        trend: 'up'
      }
    ]
  }

  const getDomainMetrics = () => {
    const domains = ['CRM', 'E-commerce', 'Analytics', 'Billing', 'CMS', 'Integration']
    return domains.map(domain => {
      const domainAgents = agents.filter(a => a.domain.includes(domain))
      const avgPerformance = domainAgents.reduce((sum, a) => sum + a.performance, 0) / (domainAgents.length || 1)
      const totalTasks = domainAgents.reduce((sum, a) => sum + a.tasksCompleted, 0)
      const activeCount = domainAgents.filter(a => a.status === 'active').length
      
      return {
        domain,
        performance: Math.round(avgPerformance),
        tasks: totalTasks,
        active: activeCount,
        total: domainAgents.length,
        status: activeCount === domainAgents.length ? 'optimal' : 
                activeCount > domainAgents.length * 0.7 ? 'good' : 'warning'
      }
    })
  }

  const getSelectedAgentMetrics = () => {
    if (!selectedAgent) return null
    
    const agent = agents.find(a => a.id === selectedAgent)
    if (!agent) return null

    return {
      performance: agent.performance,
      tasksCompleted: agent.tasksCompleted,
      successRate: agent.successRate,
      responseTime: agent.avgResponseTime || 145,
      errorRate: agent.errorRate || 2.1,
      uptime: agent.uptime || 99.5,
      recentTasks: [
        { id: 1, task: 'Lead qualification for TechCorp', status: 'completed', duration: '2.3s', timestamp: '2 min ago' },
        { id: 2, task: 'Email campaign automation', status: 'completed', duration: '1.8s', timestamp: '5 min ago' },
        { id: 3, task: 'Customer segmentation analysis', status: 'completed', duration: '4.2s', timestamp: '8 min ago' },
        { id: 4, task: 'Pipeline opportunity update', status: 'failed', duration: '0.9s', timestamp: '12 min ago' },
        { id: 5, task: 'Data synchronization', status: 'completed', duration: '3.1s', timestamp: '15 min ago' }
      ]
    }
  }

  const refreshMetrics = async () => {
    setIsLoading(true)
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    setIsLoading(false)
  }

  const exportMetrics = () => {
    // Simulate export functionality
    console.log('Exporting metrics for time range:', timeRange)
  }

  const overallMetrics = getOverallMetrics()
  const domainMetrics = getDomainMetrics()
  const selectedAgentMetrics = getSelectedAgentMetrics()

  return (
    <div className="space-y-6">
      {/* Header with Controls */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-6 w-6 text-blue-600" />
                Agent Performance Metrics
              </CardTitle>
              <p className="text-gray-600 mt-1">
                Real-time performance analytics and operational insights
              </p>
            </div>
            <div className="flex items-center gap-3">
              <select
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="1h">Last Hour</option>
                <option value="24h">Last 24 Hours</option>
                <option value="7d">Last 7 Days</option>
                <option value="30d">Last 30 Days</option>
              </select>
              <Button 
                variant="outline" 
                onClick={refreshMetrics}
                disabled={isLoading}
                className="flex items-center gap-2"
              >
                <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
              <Button 
                variant="outline"
                onClick={exportMetrics}
                className="flex items-center gap-2"
              >
                <Download className="h-4 w-4" />
                Export
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Overall System Metrics */}
      <div>
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Activity className="h-5 w-5 text-green-600" />
          System Overview
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {overallMetrics.map((metric, index) => (
            <Card key={index}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">{metric.label}</p>
                    <p className="text-2xl font-bold">
                      {metric.value.toLocaleString()}{metric.unit}
                    </p>
                    {metric.change !== 0 && (
                      <div className={`flex items-center gap-1 text-sm ${
                        metric.trend === 'up' ? 'text-green-600' : 
                        metric.trend === 'down' ? 'text-red-600' : 'text-gray-600'
                      }`}>
                        <TrendingUp className={`h-3 w-3 ${metric.trend === 'down' ? 'rotate-180' : ''}`} />
                        {Math.abs(metric.change)}% vs last period
                      </div>
                    )}
                  </div>
                  <div className={`p-3 rounded-full ${
                    metric.trend === 'up' ? 'bg-green-100' : 
                    metric.trend === 'down' ? 'bg-red-100' : 'bg-gray-100'
                  }`}>
                    {metric.label.includes('Performance') && <Zap className="h-5 w-5 text-yellow-600" />}
                    {metric.label.includes('Tasks') && <CheckCircle className="h-5 w-5 text-green-600" />}
                    {metric.label.includes('Response') && <Clock className="h-5 w-5 text-blue-600" />}
                    {metric.label.includes('Success') && <Target className="h-5 w-5 text-purple-600" />}
                    {metric.label.includes('Active') && <Activity className="h-5 w-5 text-orange-600" />}
                    {metric.label.includes('Uptime') && <CheckCircle className="h-5 w-5 text-green-600" />}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Domain Performance Breakdown */}
      <div>
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Target className="h-5 w-5 text-purple-600" />
          Domain Performance Breakdown
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {domainMetrics.map((domain, index) => (
            <Card key={index}>
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">{domain.domain}</CardTitle>
                  <Badge className={
                    domain.status === 'optimal' ? 'bg-green-100 text-green-800' :
                    domain.status === 'good' ? 'bg-blue-100 text-blue-800' :
                    'bg-yellow-100 text-yellow-800'
                  }>
                    {domain.status}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Performance</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${domain.performance}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium">{domain.performance}%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Tasks Completed</span>
                    <span className="text-sm font-medium">{domain.tasks.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Active Agents</span>
                    <span className="text-sm font-medium">{domain.active}/{domain.total}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Completion Rate</span>
                    <span className="text-sm font-medium">
                      {domain.total > 0 ? Math.round((domain.active / domain.total) * 100) : 0}%
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Selected Agent Deep Dive */}
      {selectedAgentMetrics && (
        <div>
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Activity className="h-5 w-5 text-blue-600" />
            Agent Deep Dive - {agents.find(a => a.id === selectedAgent)?.name}
          </h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Agent Performance Metrics */}
            <Card>
              <CardHeader>
                <CardTitle>Performance Metrics</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">{selectedAgentMetrics.performance}%</div>
                    <div className="text-sm text-gray-600">Performance Score</div>
                  </div>
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-2xl font-bold text-green-600">{selectedAgentMetrics.successRate}%</div>
                    <div className="text-sm text-gray-600">Success Rate</div>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <div className="text-2xl font-bold text-purple-600">{selectedAgentMetrics.responseTime}ms</div>
                    <div className="text-sm text-gray-600">Avg Response</div>
                  </div>
                  <div className="text-center p-4 bg-orange-50 rounded-lg">
                    <div className="text-2xl font-bold text-orange-600">{selectedAgentMetrics.uptime}%</div>
                    <div className="text-sm text-gray-600">Uptime</div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Tasks Completed</span>
                    <span className="font-medium">{selectedAgentMetrics.tasksCompleted.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Error Rate</span>
                    <span className="font-medium text-red-600">{selectedAgentMetrics.errorRate}%</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Recent Activity */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {selectedAgentMetrics.recentTasks.map((task) => (
                    <div key={task.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex-1">
                        <div className="font-medium text-sm">{task.task}</div>
                        <div className="text-xs text-gray-500">{task.timestamp}</div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge className={
                          task.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }>
                          {task.status}
                        </Badge>
                        <span className="text-xs text-gray-500">{task.duration}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Performance Chart Placeholder */}
      <Card>
        <CardHeader>
          <CardTitle>Performance Trends</CardTitle>
          <p className="text-gray-600">Agent performance over time</p>
        </CardHeader>
        <CardContent>
          <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
            <div className="text-center">
              <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-2" />
              <p className="text-gray-500">Performance chart would be rendered here</p>
              <p className="text-sm text-gray-400">Integration with Chart.js or Recharts recommended</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}