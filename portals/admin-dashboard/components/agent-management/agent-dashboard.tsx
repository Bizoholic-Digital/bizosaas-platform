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
  RefreshCw,
  Database
} from 'lucide-react'
import { AgentHierarchy } from './agent-hierarchy'
import { AgentMetrics } from './agent-metrics'
import { AgentLogs } from './agent-logs'
import { AgentManagementControls } from './AgentManagementControls'
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
  const [filterTeam, setFilterTeam] = useState<string>('all')

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
              <p className="text-xs text-gray-600">{stats.total} total agents in ecosystem</p>
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
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="overview" className="flex items-center gap-2">
              <Eye className="h-4 w-4" />
              Live Overview
            </TabsTrigger>
            <TabsTrigger value="catalog" className="flex items-center gap-2">
              <Bot className="h-4 w-4" />
              Agent Catalog
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
                      placeholder="Search 121+ agents by name, team, or function..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div className="flex gap-2">
                    <select
                      value={filterTeam}
                      onChange={(e) => setFilterTeam(e.target.value)}
                      className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="all">All Teams</option>
                      <option value="Marketing & Advertising">Marketing</option>
                      <option value="Content Creation">Content</option>
                      <option value="SEO Team">SEO</option>
                      <option value="E-commerce Team">E-commerce</option>
                      <option value="Analytics & Insights">Analytics</option>
                      <option value="CRM & Sales">CRM/Sales</option>
                      <option value="Operations & Compliance">Operations</option>
                      <option value="Gamification & Engagement">Gamification</option>
                      <option value="Platform Core">Platform Core</option>
                    </select>
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
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Agent Grid Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {agents
                .filter(agent =>
                  (filterStatus === 'all' || agent.status === filterStatus) &&
                  (filterTeam === 'all' || agent.team === filterTeam) &&
                  (agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                    agent.team.toLowerCase().includes(searchTerm.toLowerCase()))
                )
                .map((agent) => (
                  <Card
                    key={agent.id}
                    className={`cursor-pointer transition-all duration-200 hover:shadow-lg ${selectedAgent === agent.id ? 'ring-2 ring-blue-500' : ''
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
                          <span className="text-sm text-gray-600">Team:</span>
                          <Badge variant="secondary" className="bg-blue-50 text-blue-700 hover:bg-blue-100 border-none">{agent.team}</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Status:</span>
                          <Badge
                            variant="outline"
                            className={
                              agent.implementationStatus === 'implemented' ? 'text-green-600 border-green-200 bg-green-50' :
                                agent.implementationStatus === 'skeleton' ? 'text-yellow-600 border-yellow-200 bg-yellow-50' :
                                  'text-gray-400 border-gray-200 bg-gray-50'
                            }
                          >
                            {agent.implementationStatus}
                          </Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Type:</span>
                          <Badge variant="outline" className="text-gray-500 border-gray-200">{agent.type}</Badge>
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

          <TabsContent value="catalog" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Database className="h-5 w-5 text-blue-600" />
                  Full Agent Inventory (121+ Agents)
                </CardTitle>
                <CardDescription>
                  Explore every specialized AI agent in the BizOSaas ecosystem, organized by team.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-8">
                  {['Marketing & Advertising', 'Content Creation', 'SEO Team', 'E-commerce Team', 'Analytics & Insights', 'CRM & Sales', 'Operations & Compliance', 'Gamification & Engagement', 'Platform Core'].map(team => {
                    const teamAgents = agents.filter(a => a.team === team);
                    if (teamAgents.length === 0 && team !== 'Marketing & Advertising') return null;

                    return (
                      <div key={team} className="space-y-4">
                        <h3 className="text-lg font-semibold text-gray-900 border-b pb-2 flex items-center justify-between">
                          {team}
                          <Badge variant="outline">{teamAgents.length + (team === 'Marketing & Advertising' ? 100 : 0)} Agents</Badge>
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {teamAgents.slice(0, 6).map(agent => (
                            <div
                              key={agent.id}
                              className="p-4 border rounded-lg hover:border-blue-300 hover:shadow-sm cursor-pointer transition-all"
                              onClick={() => {
                                setSelectedAgent(agent.id);
                                setActiveTab('overview');
                              }}
                            >
                              <div className="flex justify-between items-start mb-2">
                                <h4 className="font-medium text-blue-700">{agent.name}</h4>
                                <Badge
                                  variant="outline"
                                  className="text-[10px] px-1.5 py-0"
                                >
                                  {agent.implementationStatus}
                                </Badge>
                              </div>
                              <p className="text-xs text-gray-500 line-clamp-2">{agent.description}</p>
                            </div>
                          ))}
                          {team === 'Marketing & Advertising' && (
                            <div className="p-4 border border-dashed rounded-lg bg-gray-50 flex items-center justify-center">
                              <p className="text-xs text-gray-400 font-medium">+ 100 Specialized Niche Agents</p>
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
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
          <AgentManagementControls
            agentId={selectedAgent}
            onClose={() => setSelectedAgent(null)}
          />
        )}
      </div>
    </div>
  )
}