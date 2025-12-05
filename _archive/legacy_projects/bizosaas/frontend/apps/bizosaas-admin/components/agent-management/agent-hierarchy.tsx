'use client'

import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Badge } from '../ui/badge'
import { Agent } from '../../types/agent'
import {
  ChevronDown,
  ChevronRight,
  Crown,
  Users,
  Bot,
  CheckCircle,
  AlertTriangle,
  Pause,
  Settings,
  Play,
  Brain,
  Network,
  Zap
} from 'lucide-react'

interface AgentHierarchyProps {
  agents?: Agent[]
  selectedAgent: string | null
  onSelectAgent: (agentId: string) => void
}

const hierarchyData = {
  master: {
    id: 'master-supervisor',
    name: 'Master Business Supervisor',
    type: 'master' as const,
    domain: 'Platform Orchestration',
    status: 'active' as const,
    description: 'AI-powered master orchestrator managing all business operations across platforms',
    performance: 96,
    tasksCompleted: 1247,
    successRate: 98.5,
    lastActive: '2 min ago',
    children: [
      {
        id: 'strategic-coordinator',
        name: 'Strategic Decision Coordinator',
        type: 'supervisor' as const,
        domain: 'Strategic Planning',
        status: 'active' as const,
        description: 'High-level strategic decision making and planning',
        performance: 94,
        tasksCompleted: 342,
        successRate: 96.8,
        lastActive: '5 min ago'
      },
      {
        id: 'resource-manager',
        name: 'Resource Allocation Manager',
        type: 'supervisor' as const,
        domain: 'Resource Management',
        status: 'active' as const,
        description: 'Intelligent resource allocation and optimization',
        performance: 92,
        tasksCompleted: 567,
        successRate: 94.2,
        lastActive: '3 min ago'
      },
      {
        id: 'platform-orchestrator',
        name: 'Cross-Platform Orchestrator',
        type: 'supervisor' as const,
        domain: 'Platform Integration',
        status: 'active' as const,
        description: 'Coordination across all platform ecosystems',
        performance: 89,
        tasksCompleted: 438,
        successRate: 91.7,
        lastActive: '7 min ago'
      }
    ]
  },
  supervisors: [
    {
      id: 'crm-supervisor',
      name: 'CRM Domain Supervisor',
      type: 'supervisor' as const,
      domain: 'Customer Relationship Management',
      status: 'active' as const,
      description: 'Supervising all customer relationship and sales operations',
      performance: 95,
      tasksCompleted: 892,
      successRate: 97.3,
      lastActive: '1 min ago',
      children: [
        {
          id: 'lead-scoring',
          name: 'Lead Scoring Agent',
          type: 'specialist' as const,
          domain: 'CRM',
          status: 'active' as const,
          description: 'AI-powered lead qualification and scoring',
          performance: 97,
          tasksCompleted: 234,
          successRate: 98.1,
          lastActive: '1 min ago'
        },
        {
          id: 'lead-assignment',
          name: 'Lead Assignment Agent',
          type: 'specialist' as const,
          domain: 'CRM',
          status: 'active' as const,
          description: 'Intelligent lead distribution based on skills and territory',
          performance: 94,
          tasksCompleted: 187,
          successRate: 96.5,
          lastActive: '3 min ago'
        },
        {
          id: 'nurturing-campaign',
          name: 'Nurturing Campaign Agent',
          type: 'specialist' as const,
          domain: 'CRM',
          status: 'active' as const,
          description: 'Automated email sequences and content delivery',
          performance: 91,
          tasksCompleted: 156,
          successRate: 93.8,
          lastActive: '2 min ago'
        },
        {
          id: 'sales-pipeline',
          name: 'Sales Pipeline Agent',
          type: 'specialist' as const,
          domain: 'CRM',
          status: 'active' as const,
          description: 'Opportunity management and stage progression',
          performance: 96,
          tasksCompleted: 198,
          successRate: 97.7,
          lastActive: '4 min ago'
        },
        {
          id: 'customer-segmentation',
          name: 'Customer Segmentation Agent',
          type: 'specialist' as const,
          domain: 'CRM',
          status: 'active' as const,
          description: 'Behavioral analysis and customer grouping',
          performance: 93,
          tasksCompleted: 143,
          successRate: 95.2,
          lastActive: '6 min ago'
        },
        {
          id: 'relationship-scoring',
          name: 'Relationship Scoring Agent',
          type: 'specialist' as const,
          domain: 'CRM',
          status: 'active' as const,
          description: 'Customer health and engagement tracking',
          performance: 89,
          tasksCompleted: 167,
          successRate: 92.4,
          lastActive: '5 min ago'
        }
      ]
    },
    {
      id: 'ecommerce-supervisor',
      name: 'E-commerce Domain Supervisor',
      type: 'supervisor' as const,
      domain: 'E-commerce Operations',
      status: 'active' as const,
      description: 'Overseeing product management and order processing',
      performance: 87,
      tasksCompleted: 567,
      successRate: 89.4,
      lastActive: '8 min ago',
      children: [
        {
          id: 'product-recommendation',
          name: 'Product Recommendation Agent',
          type: 'specialist' as const,
          domain: 'E-commerce',
          status: 'active' as const,
          description: 'AI-powered product suggestions and recommendations',
          performance: 92,
          tasksCompleted: 298,
          successRate: 94.6,
          lastActive: '2 min ago'
        },
        {
          id: 'inventory-optimization',
          name: 'Inventory Optimization Agent',
          type: 'specialist' as const,
          domain: 'E-commerce',
          status: 'starting' as const,
          description: 'Stock level prediction and management',
          performance: 85,
          tasksCompleted: 134,
          successRate: 87.2,
          lastActive: '15 min ago'
        },
        {
          id: 'price-optimization',
          name: 'Price Optimization Agent',
          type: 'specialist' as const,
          domain: 'E-commerce',
          status: 'starting' as const,
          description: 'Dynamic pricing based on market conditions',
          performance: 78,
          tasksCompleted: 89,
          successRate: 82.1,
          lastActive: '25 min ago'
        },
        {
          id: 'order-fulfillment',
          name: 'Order Fulfillment Agent',
          type: 'specialist' as const,
          domain: 'E-commerce',
          status: 'starting' as const,
          description: 'Automated order processing and shipping',
          performance: 83,
          tasksCompleted: 167,
          successRate: 85.7,
          lastActive: '18 min ago'
        },
        {
          id: 'customer-service',
          name: 'Customer Service Agent',
          type: 'specialist' as const,
          domain: 'E-commerce',
          status: 'inactive' as const,
          description: 'Automated support and issue resolution',
          performance: 0,
          tasksCompleted: 0,
          successRate: 0,
          lastActive: '2 hours ago'
        },
        {
          id: 'fraud-detection',
          name: 'Fraud Detection Agent',
          type: 'specialist' as const,
          domain: 'E-commerce',
          status: 'inactive' as const,
          description: 'Transaction security and risk assessment',
          performance: 0,
          tasksCompleted: 0,
          successRate: 0,
          lastActive: '3 hours ago'
        }
      ]
    },
    {
      id: 'analytics-supervisor',
      name: 'Analytics Domain Supervisor',
      type: 'supervisor' as const,
      domain: 'Data Analytics',
      status: 'active' as const,
      description: 'Managing data processing and insights generation',
      performance: 93,
      tasksCompleted: 743,
      successRate: 95.8,
      lastActive: '3 min ago',
      children: [
        {
          id: 'data-collection',
          name: 'Data Collection Agent',
          type: 'specialist' as const,
          domain: 'Analytics',
          status: 'active' as const,
          description: 'Automated data gathering from multiple sources',
          performance: 96,
          tasksCompleted: 345,
          successRate: 97.8,
          lastActive: '1 min ago'
        },
        {
          id: 'report-generation',
          name: 'Report Generation Agent',
          type: 'specialist' as const,
          domain: 'Analytics',
          status: 'active' as const,
          description: 'Dynamic report creation and scheduling',
          performance: 94,
          tasksCompleted: 267,
          successRate: 96.3,
          lastActive: '2 min ago'
        },
        {
          id: 'insight-discovery',
          name: 'Insight Discovery Agent',
          type: 'specialist' as const,
          domain: 'Analytics',
          status: 'inactive' as const,
          description: 'Pattern recognition and trend analysis',
          performance: 0,
          tasksCompleted: 0,
          successRate: 0,
          lastActive: '1 hour ago'
        },
        {
          id: 'performance-monitoring',
          name: 'Performance Monitoring Agent',
          type: 'specialist' as const,
          domain: 'Analytics',
          status: 'active' as const,
          description: 'Real-time metrics and alerting',
          performance: 91,
          tasksCompleted: 423,
          successRate: 93.7,
          lastActive: '30 sec ago'
        },
        {
          id: 'predictive-analytics',
          name: 'Predictive Analytics Agent',
          type: 'specialist' as const,
          domain: 'Analytics',
          status: 'inactive' as const,
          description: 'Forecasting and trend prediction',
          performance: 0,
          tasksCompleted: 0,
          successRate: 0,
          lastActive: '2 hours ago'
        },
        {
          id: 'dashboard-creation',
          name: 'Dashboard Creation Agent',
          type: 'specialist' as const,
          domain: 'Analytics',
          status: 'active' as const,
          description: 'Automated visualization and chart generation',
          performance: 88,
          tasksCompleted: 156,
          successRate: 91.4,
          lastActive: '8 min ago'
        }
      ]
    }
  ]
}

export function AgentHierarchy({ agents, selectedAgent, onSelectAgent }: AgentHierarchyProps) {
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set(['master-supervisor']))

  const toggleExpand = (nodeId: string) => {
    const newExpanded = new Set(expandedNodes)
    if (newExpanded.has(nodeId)) {
      newExpanded.delete(nodeId)
    } else {
      newExpanded.add(nodeId)
    }
    setExpandedNodes(newExpanded)
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'inactive':
        return <Pause className="h-4 w-4 text-gray-500" />
      case 'error':
        return <AlertTriangle className="h-4 w-4 text-red-500" />
      case 'starting':
        return <Zap className="h-4 w-4 text-yellow-500" />
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

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'master':
        return <Crown className="h-5 w-5 text-purple-600" />
      case 'supervisor':
        return <Users className="h-5 w-5 text-blue-600" />
      case 'specialist':
        return <Brain className="h-4 w-4 text-green-600" />
      default:
        return <Bot className="h-4 w-4 text-gray-600" />
    }
  }

  const renderAgent = (agent: any, level: number = 0) => {
    const isExpanded = expandedNodes.has(agent.id)
    const hasChildren = agent.children && agent.children.length > 0
    const isSelected = selectedAgent === agent.id

    return (
      <div key={agent.id} className="w-full">
        <Card 
          className={`mb-2 cursor-pointer transition-all duration-200 hover:shadow-md ${
            isSelected ? 'ring-2 ring-blue-500 bg-blue-50' : ''
          } ${level > 0 ? 'ml-6' : ''}`}
          onClick={() => onSelectAgent(agent.id)}
        >
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {hasChildren && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      toggleExpand(agent.id)
                    }}
                    className="p-1 hover:bg-gray-100 rounded"
                  >
                    {isExpanded ? (
                      <ChevronDown className="h-4 w-4" />
                    ) : (
                      <ChevronRight className="h-4 w-4" />
                    )}
                  </button>
                )}
                {!hasChildren && level > 0 && (
                  <div className="w-6 h-4 flex items-center justify-center">
                    <div className="w-3 h-px bg-gray-300" />
                  </div>
                )}
                {getTypeIcon(agent.type)}
                <div>
                  <CardTitle className="text-lg flex items-center gap-2">
                    {agent.name}
                    <Badge className={getStatusColor(agent.status)}>
                      {agent.status}
                    </Badge>
                  </CardTitle>
                  <p className="text-sm text-gray-600 mt-1">{agent.description}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                {getStatusIcon(agent.status)}
                <div className="text-right">
                  <div className="text-sm font-medium">{agent.performance}%</div>
                  <div className="text-xs text-gray-500">Performance</div>
                </div>
              </div>
            </div>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Domain:</span>
                <div className="font-medium">{agent.domain}</div>
              </div>
              <div>
                <span className="text-gray-600">Tasks Completed:</span>
                <div className="font-medium">{agent.tasksCompleted.toLocaleString()}</div>
              </div>
              <div>
                <span className="text-gray-600">Success Rate:</span>
                <div className="font-medium">{agent.successRate}%</div>
              </div>
              <div>
                <span className="text-gray-600">Last Active:</span>
                <div className="font-medium">{agent.lastActive}</div>
              </div>
            </div>
            <div className="flex gap-2 mt-4">
              <Button 
                size="sm" 
                variant={agent.status === 'active' ? 'outline' : 'default'}
                onClick={(e) => e.stopPropagation()}
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
              <Button 
                size="sm" 
                variant="outline"
                onClick={(e) => e.stopPropagation()}
              >
                <Settings className="h-3 w-3 mr-1" />
                Configure
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Render children if expanded */}
        {hasChildren && isExpanded && (
          <div className="ml-4 border-l-2 border-gray-200 pl-4">
            {agent.children!.map((child: any) => renderAgent(child, level + 1))}
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Network className="h-6 w-6 text-blue-600" />
            AI Agent Hierarchy
          </CardTitle>
          <p className="text-gray-600">
            Hierarchical view of all AI agents with master orchestration, domain supervisors, and specialist agents
          </p>
        </CardHeader>
      </Card>

      <div className="space-y-4">
        {/* Master Orchestration Layer */}
        <div>
          <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
            <Crown className="h-5 w-5 text-purple-600" />
            Master Orchestration Layer
          </h3>
          {renderAgent(hierarchyData.master)}
        </div>

        {/* Domain Supervisors */}
        <div>
          <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
            <Users className="h-5 w-5 text-blue-600" />
            Domain Supervisors (70% Complete)
          </h3>
          <div className="space-y-4">
            {hierarchyData.supervisors.map((supervisor) => renderAgent(supervisor))}
          </div>
        </div>
      </div>
    </div>
  )
}