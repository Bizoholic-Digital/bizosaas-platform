'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Badge } from '../ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs'
import { 
  Activity, 
  Bot, 
  Play, 
  Pause, 
  Settings, 
  BarChart3, 
  AlertTriangle,
  CheckCircle,
  Clock,
  Zap,
  Brain,
  Network,
  Eye,
  Filter,
  Search,
  RefreshCw
} from 'lucide-react'
import { AgentHierarchy } from './agent-hierarchy'
import { AgentMetrics } from './agent-metrics'
import { AgentLogs } from './agent-logs'
import { AgentControls } from './agent-controls'
import { useAgentStore } from '../../lib/stores/agent-store'

interface AgentStats {
  total: number
  active: number
  inactive: number
  error: number
  performance: number
}

export function AgentDashboard() {
  const { agents, isLoading, fetchAgents, getAgentStats } = useAgentStore()
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState('overview')
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState<string>('all')

  const stats: AgentStats = getAgentStats()

  useEffect(() => {
    fetchAgents()
    // Set up real-time updates every 30 seconds
    const interval = setInterval(fetchAgents, 30000)
    return () => clearInterval(interval)
  }, [fetchAgents])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'inactive':
        return <Pause className="h-4 w-4 text-gray-500" />
      case 'error':
        return <AlertTriangle className="h-4 w-4 text-red-500" />
      case 'starting':
        return <Clock className="h-4 w-4 text-yellow-500" />
      default:
        return <Bot className="h-4 w-4 text-blue-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'inactive':
        return 'bg-gray-100 text-gray-800'
      case 'error':
        return 'bg-red-100 text-red-800'
      case 'starting':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-blue-100 text-blue-800'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
              <Bot className="h-8 w-8 text-blue-600" />
              Agent Management System
            </h1>
            <p className="text-gray-600 mt-2">
              Monitor and control your AI agent ecosystem across all platforms
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Button 
              variant="outline" 
              onClick={fetchAgents}
              disabled={isLoading}
              className="flex items-center gap-2"
            >
              <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
            <Button className="flex items-center gap-2">
              <Settings className="h-4 w-4" />
              System Settings
            </Button>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Agents</CardTitle>
              <Network className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total}</div>
              <p className="text-xs text-gray-600">32 specialist agents</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{stats.active}</div>
              <p className="text-xs text-gray-600">Running smoothly</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Inactive</CardTitle>
              <Pause className="h-4 w-4 text-gray-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-600">{stats.inactive}</div>
              <p className="text-xs text-gray-600">Standby mode</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Errors</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">{stats.error}</div>
              <p className="text-xs text-gray-600">Need attention</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Performance</CardTitle>
              <Zap className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.performance}%</div>
              <p className="text-xs text-gray-600">Avg efficiency</p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview" className="flex items-center gap-2">
              <Eye className="h-4 w-4" />
              Overview
            </TabsTrigger>
            <TabsTrigger value="hierarchy" className="flex items-center gap-2">
              <Network className="h-4 w-4" />
              Hierarchy
            </TabsTrigger>
            <TabsTrigger value="metrics" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              Metrics
            </TabsTrigger>
            <TabsTrigger value="logs" className="flex items-center gap-2">
              <Activity className="h-4 w-4" />
              Logs
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {/* Search and Filter Controls */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Search className="h-5 w-5" />
                  Agent Search & Filter
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="flex-1">
                    <input
                      type="text"
                      placeholder="Search agents by name, domain, or function..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div className="flex gap-2">
                    <select
                      value={filterStatus}
                      onChange={(e) => setFilterStatus(e.target.value)}
                      className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="all">All Status</option>
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                      <option value="error">Error</option>
                    </select>
                    <Button variant="outline" className="flex items-center gap-2">
                      <Filter className="h-4 w-4" />
                      Filters
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Agent Grid Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {agents
                .filter(agent => 
                  (filterStatus === 'all' || agent.status === filterStatus) &&
                  agent.name.toLowerCase().includes(searchTerm.toLowerCase())
                )
                .map((agent) => (
                  <Card 
                    key={agent.id}
                    className={`cursor-pointer transition-all duration-200 hover:shadow-lg ${
                      selectedAgent === agent.id ? 'ring-2 ring-blue-500' : ''
                    }`}
                    onClick={() => setSelectedAgent(agent.id)}
                  >
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Brain className="h-5 w-5 text-blue-600" />
                          <CardTitle className="text-lg">{agent.name}</CardTitle>
                        </div>
                        <div className="flex items-center gap-2">
                          {getStatusIcon(agent.status)}
                          <Badge className={getStatusColor(agent.status)}>
                            {agent.status}
                          </Badge>
                        </div>
                      </div>
                      <CardDescription className="text-sm">
                        {agent.description}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Domain:</span>
                          <Badge variant="outline">{agent.domain}</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Type:</span>
                          <Badge variant="outline">{agent.type}</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Performance:</span>
                          <div className="flex items-center gap-1">
                            <div className="w-16 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                                style={{ width: `${agent.performance}%` }}
                              />
                            </div>
                            <span className="text-sm font-medium">{agent.performance}%</span>
                          </div>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Last Active:</span>
                          <span className="text-sm">{agent.lastActive}</span>
                        </div>
                        <div className="flex gap-2 mt-4">
                          <Button 
                            size="sm" 
                            variant={agent.status === 'active' ? 'outline' : 'default'}
                            className="flex-1"
                          >
                            {agent.status === 'active' ? (
                              <>
                                <Pause className="h-3 w-3 mr-1" />
                                Pause
                              </>
                            ) : (
                              <>
                                <Play className="h-3 w-3 mr-1" />
                                Start
                              </>
                            )}
                          </Button>
                          <Button size="sm" variant="outline">
                            <Settings className="h-3 w-3" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
            </div>
          </TabsContent>

          <TabsContent value="hierarchy" className="space-y-6">
            <AgentHierarchy 
              agents={agents}
              selectedAgent={selectedAgent}
              onSelectAgent={setSelectedAgent}
            />
          </TabsContent>

          <TabsContent value="metrics" className="space-y-6">
            <AgentMetrics 
              agents={agents}
              selectedAgent={selectedAgent}
            />
          </TabsContent>

          <TabsContent value="logs" className="space-y-6">
            <AgentLogs 
              selectedAgent={selectedAgent}
            />
          </TabsContent>
        </Tabs>

        {/* Agent Controls Panel */}
        {selectedAgent && (
          <AgentControls 
            agentId={selectedAgent}
            onClose={() => setSelectedAgent(null)}
          />
        )}
      </div>
    </div>
  )
}