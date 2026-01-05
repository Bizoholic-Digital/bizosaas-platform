'use client'

import { useState, useEffect } from 'react'
import { Activity, Brain, CheckCircle, XCircle, Clock, AlertTriangle, Zap, Target, Users, BarChart3, Settings } from 'lucide-react'
import { AgentManagementControls } from '../../components/agent-management/AgentManagementControls'

interface AgentStatus {
  id: string
  name: string
  type: 'marketing' | 'analytics' | 'content' | 'lead-scoring' | 'automation'
  status: 'active' | 'idle' | 'error' | 'processing'
  lastExecution: string
  successRate: number
  tasksCompleted: number
  averageTime: number
  description: string
}

interface AgentMetrics {
  totalAgents: number
  activeAgents: number
  totalExecutions: number
  successRate: number
  avgResponseTime: number
  errors: number
}

export default function AIAgentsPage() {
  const [agents, setAgents] = useState<AgentStatus[]>([])
  const [metrics, setMetrics] = useState<AgentMetrics | null>(null)
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null)
  const [managingAgentId, setManagingAgentId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate fetching AI agent data
    const fetchAgentData = () => {
      const mockAgents: AgentStatus[] = [
        {
          id: 'agent-1',
          name: 'Lead Scoring Agent',
          type: 'lead-scoring',
          status: 'active',
          lastExecution: '2 minutes ago',
          successRate: 98.5,
          tasksCompleted: 1247,
          averageTime: 1.2,
          description: 'Analyzes and scores incoming leads based on behavioral patterns'
        },
        {
          id: 'agent-2',
          name: 'Content Generation Agent',
          type: 'content',
          status: 'processing',
          lastExecution: '5 minutes ago',
          successRate: 94.2,
          tasksCompleted: 892,
          averageTime: 3.8,
          description: 'Generates personalized marketing content and email campaigns'
        },
        {
          id: 'agent-3',
          name: 'Marketing Analytics Agent',
          type: 'analytics',
          status: 'idle',
          lastExecution: '15 minutes ago',
          successRate: 99.1,
          tasksCompleted: 634,
          averageTime: 2.1,
          description: 'Analyzes campaign performance and provides optimization recommendations'
        },
        {
          id: 'agent-4',
          name: 'Customer Segmentation Agent',
          type: 'marketing',
          status: 'active',
          lastExecution: '1 minute ago',
          successRate: 96.7,
          tasksCompleted: 456,
          averageTime: 1.8,
          description: 'Segments customers based on behavior, demographics, and purchase history'
        },
        {
          id: 'agent-5',
          name: 'Workflow Automation Agent',
          type: 'automation',
          status: 'error',
          lastExecution: '30 minutes ago',
          successRate: 87.3,
          tasksCompleted: 223,
          averageTime: 4.2,
          description: 'Automates complex multi-step marketing workflows and follow-ups'
        }
      ]

      const mockMetrics: AgentMetrics = {
        totalAgents: 5,
        activeAgents: 2,
        totalExecutions: 3452,
        successRate: 95.2,
        avgResponseTime: 2.4,
        errors: 12
      }

      setAgents(mockAgents)
      setMetrics(mockMetrics)
      setIsLoading(false)
    }

    fetchAgentData()
    const interval = setInterval(fetchAgentData, 30000) // Refresh every 30 seconds

    return () => clearInterval(interval)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100'
      case 'processing': return 'text-blue-600 bg-blue-100'
      case 'idle': return 'text-gray-600 bg-gray-100'
      case 'error': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle className="h-4 w-4" />
      case 'processing': return <Clock className="h-4 w-4" />
      case 'idle': return <Activity className="h-4 w-4" />
      case 'error': return <XCircle className="h-4 w-4" />
      default: return <Activity className="h-4 w-4" />
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'marketing': return <Target className="h-5 w-5" />
      case 'analytics': return <BarChart3 className="h-5 w-5" />
      case 'content': return <Brain className="h-5 w-5" />
      case 'lead-scoring': return <Users className="h-5 w-5" />
      case 'automation': return <Zap className="h-5 w-5" />
      default: return <Brain className="h-5 w-5" />
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading AI agents...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      {managingAgentId && (
        <AgentManagementControls
          agentId={managingAgentId}
          onClose={() => setManagingAgentId(null)}
        />
      )}

      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">AI Agent Status Monitor</h1>
          <p className="text-gray-600">Real-time monitoring of AI agent execution and performance</p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-600">Live monitoring</span>
          </div>
        </div>
      </div>

      {/* Metrics Overview */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Brain className="h-8 w-8 text-blue-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Total Agents</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.totalAgents}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <CheckCircle className="h-8 w-8 text-green-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Active Agents</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.activeAgents}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Activity className="h-8 w-8 text-purple-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Total Executions</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.totalExecutions.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Target className="h-8 w-8 text-green-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Success Rate</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.successRate}%</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Clock className="h-8 w-8 text-blue-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Avg Response</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.avgResponseTime}s</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <AlertTriangle className="h-8 w-8 text-red-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Errors</p>
                <p className="text-2xl font-bold text-gray-900">{metrics.errors}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Agents List */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">AI Agents</h3>
          <p className="text-sm text-gray-500">Monitor individual agent performance and status</p>
        </div>
        <div className="divide-y divide-gray-200">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className={`p-6 hover:bg-gray-50 transition-colors cursor-pointer ${selectedAgent === agent.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''
                }`}
              onClick={() => setSelectedAgent(selectedAgent === agent.id ? null : agent.id)}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="flex-shrink-0">
                    {getTypeIcon(agent.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-3">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {agent.name}
                      </p>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(agent.status)}`}>
                        {getStatusIcon(agent.status)}
                        <span className="ml-1 capitalize">{agent.status}</span>
                      </span>
                    </div>
                    <p className="text-sm text-gray-500">{agent.description}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-6 text-sm text-gray-500">
                  <div className="text-center">
                    <p className="font-medium text-gray-900">{agent.successRate}%</p>
                    <p>Success Rate</p>
                  </div>
                  <div className="text-center">
                    <p className="font-medium text-gray-900">{agent.tasksCompleted}</p>
                    <p>Tasks</p>
                  </div>
                  <div className="text-center">
                    <p className="font-medium text-gray-900">{agent.averageTime}s</p>
                    <p>Avg Time</p>
                  </div>
                  <div className="text-center">
                    <p className="font-medium text-gray-900">{agent.lastExecution}</p>
                    <p>Last Run</p>
                  </div>
                </div>
              </div>

              {/* Expanded details */}
              {selectedAgent === agent.id && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="space-y-2">
                      <h4 className="text-sm font-medium text-gray-900">Performance Metrics</h4>
                      <div className="space-y-1">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">Success Rate:</span>
                          <span className="font-medium">{agent.successRate}%</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">Tasks Completed:</span>
                          <span className="font-medium">{agent.tasksCompleted}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">Average Response Time:</span>
                          <span className="font-medium">{agent.averageTime}s</span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <h4 className="text-sm font-medium text-gray-900">Recent Activity</h4>
                      <div className="space-y-1">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">Last Execution:</span>
                          <span className="font-medium">{agent.lastExecution}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">Status:</span>
                          <span className={`font-medium capitalize ${agent.status === 'active' ? 'text-green-600' :
                              agent.status === 'error' ? 'text-red-600' :
                                agent.status === 'processing' ? 'text-blue-600' : 'text-gray-600'
                            }`}>
                            {agent.status}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <h4 className="text-sm font-medium text-gray-900">Actions</h4>
                      <div className="space-y-2">
                        <button
                          className="w-full text-left px-3 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors flex items-center justify-center font-medium shadow-sm"
                          onClick={(e) => {
                            e.stopPropagation();
                            setManagingAgentId(agent.id);
                          }}
                        >
                          <Settings className="w-4 h-4 mr-2" />
                          Manage Agent Configuration
                        </button>
                        <button className="w-full text-left px-3 py-2 text-sm bg-blue-50 text-blue-700 rounded hover:bg-blue-100 transition-colors">
                          View Execution Log
                        </button>
                        <button className="w-full text-left px-3 py-2 text-sm bg-gray-50 text-gray-700 rounded hover:bg-gray-100 transition-colors">
                          Download Report
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}