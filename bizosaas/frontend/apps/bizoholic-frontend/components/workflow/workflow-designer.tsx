'use client'

import React, { useState, useCallback, useRef, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { Textarea } from '@/components/ui/textarea'
import { 
  Play, 
  Pause, 
  Save, 
  Plus, 
  Trash2, 
  Settings, 
  User, 
  Bot, 
  ArrowRight,
  ArrowDown,
  GitBranch,
  Clock,
  CheckCircle,
  AlertCircle,
  Zap,
  Users,
  Database,
  Globe,
  MessageSquare,
  FileText,
  BarChart3,
  Target,
  Mail,
  Phone,
  Calendar,
  DollarSign,
  ShoppingCart,
  TrendingUp,
  Workflow as WorkflowIcon,
  Network,
  Brain
} from 'lucide-react'

// Types for workflow nodes and connections
interface WorkflowNode {
  id: string
  type: 'trigger' | 'action' | 'condition' | 'approval' | 'agent' | 'integration'
  name: string
  description: string
  position: { x: number; y: number }
  config: Record<string, any>
  requiresHuman?: boolean
  agentPattern?: '4-agent' | '3-agent' | '2-agent' | 'single-agent'
  status?: 'pending' | 'running' | 'completed' | 'failed' | 'waiting-approval'
}

interface WorkflowConnection {
  id: string
  sourceId: string
  targetId: string
  condition?: string
}

interface WorkflowTemplate {
  id: string
  name: string
  description: string
  category: 'marketing' | 'sales' | 'support' | 'operations' | 'analytics'
  isHITL: boolean
  nodes: WorkflowNode[]
  connections: WorkflowConnection[]
  estimatedDuration: string
  complexity: 'simple' | 'medium' | 'complex'
}

// Predefined workflow templates
const WORKFLOW_TEMPLATES: WorkflowTemplate[] = [
  {
    id: 'hitl-campaign-approval',
    name: 'Campaign Creation with Human Approval',
    description: 'AI creates campaign content, human reviews and approves before launch',
    category: 'marketing',
    isHITL: true,
    estimatedDuration: '2-4 hours',
    complexity: 'medium',
    nodes: [
      {
        id: 'trigger-1',
        type: 'trigger',
        name: 'Campaign Request',
        description: 'New campaign request received',
        position: { x: 100, y: 100 },
        config: { eventType: 'campaign_request' }
      },
      {
        id: 'agent-1',
        type: 'agent',
        name: 'Content Creator Agent',
        description: 'AI creates campaign content and strategy',
        position: { x: 300, y: 100 },
        config: { agentType: 'content_creator' },
        agentPattern: '4-agent'
      },
      {
        id: 'approval-1',
        type: 'approval',
        name: 'Human Review',
        description: 'Marketing manager reviews AI-generated content',
        position: { x: 500, y: 100 },
        config: { approverRole: 'marketing_manager', timeoutHours: 24 },
        requiresHuman: true
      },
      {
        id: 'action-1',
        type: 'action',
        name: 'Launch Campaign',
        description: 'Deploy approved campaign across platforms',
        position: { x: 700, y: 100 },
        config: { platforms: ['google_ads', 'meta_ads', 'linkedin'] }
      }
    ],
    connections: [
      { id: 'conn-1', sourceId: 'trigger-1', targetId: 'agent-1' },
      { id: 'conn-2', sourceId: 'agent-1', targetId: 'approval-1' },
      { id: 'conn-3', sourceId: 'approval-1', targetId: 'action-1', condition: 'approved' }
    ]
  },
  {
    id: 'autonomous-lead-nurture',
    name: 'Autonomous Lead Nurturing',
    description: 'Fully automated lead nurturing with AI decision making',
    category: 'sales',
    isHITL: false,
    estimatedDuration: '24/7 continuous',
    complexity: 'complex',
    nodes: [
      {
        id: 'trigger-2',
        type: 'trigger',
        name: 'New Lead',
        description: 'Lead captured from form or CRM',
        position: { x: 100, y: 100 },
        config: { eventType: 'lead_captured' }
      },
      {
        id: 'agent-2',
        type: 'agent',
        name: 'Lead Scoring Agent',
        description: 'AI scores and categorizes lead',
        position: { x: 300, y: 100 },
        config: { agentType: 'lead_scorer' },
        agentPattern: '3-agent'
      },
      {
        id: 'condition-1',
        type: 'condition',
        name: 'Lead Quality Check',
        description: 'Route based on lead score',
        position: { x: 500, y: 100 },
        config: { conditions: [{ if: 'score > 80', then: 'high-priority' }] }
      },
      {
        id: 'agent-3',
        type: 'agent',
        name: 'Personalization Agent',
        description: 'Creates personalized outreach sequence',
        position: { x: 700, y: 50 },
        config: { agentType: 'personalizer' },
        agentPattern: '2-agent'
      },
      {
        id: 'agent-4',
        type: 'agent',
        name: 'Nurture Agent',
        description: 'Standard nurture sequence',
        position: { x: 700, y: 150 },
        config: { agentType: 'nurturer' },
        agentPattern: 'single-agent'
      }
    ],
    connections: [
      { id: 'conn-4', sourceId: 'trigger-2', targetId: 'agent-2' },
      { id: 'conn-5', sourceId: 'agent-2', targetId: 'condition-1' },
      { id: 'conn-6', sourceId: 'condition-1', targetId: 'agent-3', condition: 'high-priority' },
      { id: 'conn-7', sourceId: 'condition-1', targetId: 'agent-4', condition: 'standard' }
    ]
  }
]

// Available AI agents by category and pattern
const AI_AGENTS = {
  'marketing': {
    '4-agent': ['Content Strategy Team', 'Campaign Optimization Squad', 'SEO Enhancement Crew'],
    '3-agent': ['Social Media Trio', 'Ad Creative Team', 'Email Marketing Unit'],
    '2-agent': ['Competitor Analysis Pair', 'Keyword Research Duo'],
    'single-agent': ['Blog Writer', 'Ad Copy Creator', 'Social Scheduler', 'SEO Auditor']
  },
  'sales': {
    '4-agent': ['Lead Qualification Team', 'Sales Pipeline Crew'],
    '3-agent': ['Outreach Optimization Trio', 'Deal Closing Squad'],
    '2-agent': ['Proposal Generation Pair', 'Follow-up Duo'],
    'single-agent': ['Lead Scorer', 'Email Sequencer', 'CRM Updater', 'Meeting Scheduler']
  },
  'support': {
    '4-agent': ['Customer Success Team', 'Issue Resolution Crew'],
    '3-agent': ['Ticket Triage Trio', 'Knowledge Base Squad'],
    '2-agent': ['Response Automation Pair', 'Escalation Duo'],
    'single-agent': ['FAQ Bot', 'Satisfaction Tracker', 'Feedback Analyzer']
  },
  'operations': {
    '4-agent': ['Data Processing Team', 'Workflow Optimization Crew'],
    '3-agent': ['Report Generation Trio', 'System Monitor Squad'],
    '2-agent': ['Backup Validation Pair', 'Performance Tracking Duo'],
    'single-agent': ['Log Analyzer', 'Health Checker', 'Alert Manager']
  },
  'analytics': {
    '4-agent': ['Business Intelligence Team', 'Predictive Analytics Crew'],
    '3-agent': ['Dashboard Builder Trio', 'Data Visualization Squad'],
    '2-agent': ['Trend Analysis Pair', 'Reporting Duo'],
    'single-agent': ['Metric Tracker', 'Goal Monitor', 'KPI Calculator']
  }
}

// Node type configurations
const NODE_TYPES = {
  trigger: { icon: Zap, color: 'bg-green-500', label: 'Trigger' },
  action: { icon: Play, color: 'bg-blue-500', label: 'Action' },
  condition: { icon: GitBranch, color: 'bg-yellow-500', label: 'Condition' },
  approval: { icon: User, color: 'bg-purple-500', label: 'Human Approval' },
  agent: { icon: Bot, color: 'bg-orange-500', label: 'AI Agent' },
  integration: { icon: Globe, color: 'bg-pink-500', label: 'Integration' }
}

export default function WorkflowDesigner() {
  const [selectedTemplate, setSelectedTemplate] = useState<WorkflowTemplate | null>(null)
  const [currentWorkflow, setCurrentWorkflow] = useState<WorkflowTemplate | null>(null)
  const [isHITLMode, setIsHITLMode] = useState(true)
  const [selectedNode, setSelectedNode] = useState<WorkflowNode | null>(null)
  const [workflowName, setWorkflowName] = useState('')
  const [isPlaying, setIsPlaying] = useState(false)
  const [executionLogs, setExecutionLogs] = useState<string[]>([])
  const [currentNamespace, setCurrentNamespace] = useState('marketing-campaigns-001')
  
  const canvasRef = useRef<HTMLDivElement>(null)

  // Handle template selection
  const handleTemplateSelect = (template: WorkflowTemplate) => {
    setSelectedTemplate(template)
    setCurrentWorkflow({ ...template })
    setIsHITLMode(template.isHITL)
    setWorkflowName(template.name)
    setSelectedNode(null)
  }

  // Create new workflow
  const handleCreateNew = (type: 'hitl' | 'autonomous') => {
    const newWorkflow: WorkflowTemplate = {
      id: `workflow-${Date.now()}`,
      name: `New ${type === 'hitl' ? 'HITL' : 'Autonomous'} Workflow`,
      description: 'Drag components to build your workflow',
      category: 'marketing',
      isHITL: type === 'hitl',
      estimatedDuration: '1 hour',
      complexity: 'simple',
      nodes: [],
      connections: []
    }
    
    setCurrentWorkflow(newWorkflow)
    setIsHITLMode(type === 'hitl')
    setWorkflowName(newWorkflow.name)
    setSelectedNode(null)
  }

  // Add node to workflow
  const handleAddNode = (nodeType: keyof typeof NODE_TYPES) => {
    if (!currentWorkflow) return

    const newNode: WorkflowNode = {
      id: `node-${Date.now()}`,
      type: nodeType,
      name: `New ${NODE_TYPES[nodeType].label}`,
      description: `Configure this ${NODE_TYPES[nodeType].label.toLowerCase()}`,
      position: { 
        x: 200 + (currentWorkflow.nodes.length * 150), 
        y: 200 + (Math.random() * 100) 
      },
      config: {},
      requiresHuman: nodeType === 'approval',
      agentPattern: nodeType === 'agent' ? 'single-agent' : undefined
    }

    setCurrentWorkflow({
      ...currentWorkflow,
      nodes: [...currentWorkflow.nodes, newNode]
    })
    setSelectedNode(newNode)
  }

  // Start workflow execution simulation
  const handlePlay = () => {
    if (!currentWorkflow) return
    
    setIsPlaying(true)
    setExecutionLogs([])
    
    // Simulate workflow execution
    const executeNode = (nodeIndex: number) => {
      if (nodeIndex >= currentWorkflow.nodes.length) {
        setIsPlaying(false)
        setExecutionLogs(prev => [...prev, '✅ Workflow completed successfully'])
        return
      }

      const node = currentWorkflow.nodes[nodeIndex]
      setExecutionLogs(prev => [...prev, `🔄 Executing: ${node.name}`])
      
      setTimeout(() => {
        if (node.requiresHuman && isHITLMode) {
          setExecutionLogs(prev => [...prev, `⏳ Waiting for human approval: ${node.name}`])
          // In real implementation, this would wait for actual approval
          setTimeout(() => {
            setExecutionLogs(prev => [...prev, `✅ Approved: ${node.name}`])
            executeNode(nodeIndex + 1)
          }, 2000)
        } else {
          setExecutionLogs(prev => [...prev, `✅ Completed: ${node.name}`])
          executeNode(nodeIndex + 1)
        }
      }, 1000)
    }

    executeNode(0)
  }

  // Stop workflow execution
  const handleStop = () => {
    setIsPlaying(false)
    setExecutionLogs(prev => [...prev, '⏹️ Workflow execution stopped'])
  }

  // Node component for canvas
  const WorkflowNode = ({ node }: { node: WorkflowNode }) => {
    const NodeIcon = NODE_TYPES[node.type].icon
    const isSelected = selectedNode?.id === node.id
    
    return (
      <div
        className={`absolute p-4 bg-white border-2 rounded-lg shadow-lg cursor-pointer transition-all min-w-40 ${
          isSelected ? 'border-blue-500 shadow-xl' : 'border-gray-200 hover:border-gray-300'
        }`}
        style={{ left: node.position.x, top: node.position.y }}
        onClick={() => setSelectedNode(node)}
      >
        <div className="flex items-center space-x-2 mb-2">
          <div className={`p-1 rounded ${NODE_TYPES[node.type].color}`}>
            <NodeIcon className="w-4 h-4 text-white" />
          </div>
          <Badge variant="outline" className="text-xs">
            {NODE_TYPES[node.type].label}
          </Badge>
          {node.requiresHuman && (
            <Badge variant="secondary" className="text-xs">
              HITL
            </Badge>
          )}
        </div>
        <div className="font-medium text-sm mb-1">{node.name}</div>
        <div className="text-xs text-gray-500">{node.description}</div>
        {node.agentPattern && (
          <Badge variant="outline" className="text-xs mt-2">
            {node.agentPattern}
          </Badge>
        )}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Temporal Workflow Designer</h2>
          <p className="text-muted-foreground">
            Design and deploy HITL and autonomous workflows for your AI agents
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <Select value={currentNamespace} onValueChange={setCurrentNamespace}>
            <SelectTrigger className="w-64">
              <SelectValue placeholder="Select namespace" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="marketing-campaigns-001">marketing-campaigns-001</SelectItem>
              <SelectItem value="sales-automation-002">sales-automation-002</SelectItem>
              <SelectItem value="customer-support-003">customer-support-003</SelectItem>
              <SelectItem value="analytics-reports-004">analytics-reports-004</SelectItem>
              <SelectItem value="operations-mgmt-005">operations-mgmt-005</SelectItem>
            </SelectContent>
          </Select>
          <Badge variant={isHITLMode ? "default" : "secondary"}>
            {isHITLMode ? 'HITL Mode' : 'Autonomous Mode'}
          </Badge>
        </div>
      </div>

      <Tabs defaultValue="templates" className="space-y-6">
        <TabsList>
          <TabsTrigger value="templates">Templates</TabsTrigger>
          <TabsTrigger value="designer">Visual Designer</TabsTrigger>
          <TabsTrigger value="execution">Execution Monitor</TabsTrigger>
          <TabsTrigger value="namespaces">Namespace Manager</TabsTrigger>
        </TabsList>

        {/* Templates Tab */}
        <TabsContent value="templates" className="space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Label htmlFor="hitl-mode">HITL Mode</Label>
                <Switch
                  id="hitl-mode"
                  checked={isHITLMode}
                  onCheckedChange={setIsHITLMode}
                />
              </div>
              <div className="text-sm text-muted-foreground">
                {isHITLMode ? 'Human-in-the-Loop workflows require approval steps' : 'Fully autonomous workflows'}
              </div>
            </div>
            <div className="flex space-x-2">
              <Button onClick={() => handleCreateNew('hitl')} variant="outline">
                <User className="w-4 h-4 mr-2" />
                New HITL Workflow
              </Button>
              <Button onClick={() => handleCreateNew('autonomous')} variant="outline">
                <Bot className="w-4 h-4 mr-2" />
                New Autonomous Workflow
              </Button>
            </div>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {WORKFLOW_TEMPLATES
              .filter(template => isHITLMode ? template.isHITL : !template.isHITL)
              .map((template) => (
                <Card key={template.id} className="cursor-pointer hover:shadow-lg transition-shadow"
                      onClick={() => handleTemplateSelect(template)}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg">{template.name}</CardTitle>
                      <div className="flex space-x-1">
                        <Badge variant={template.isHITL ? "default" : "secondary"}>
                          {template.isHITL ? 'HITL' : 'Auto'}
                        </Badge>
                        <Badge variant="outline">
                          {template.category}
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground mb-4">
                      {template.description}
                    </p>
                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span>{template.nodes.length} steps</span>
                      <span>{template.estimatedDuration}</span>
                      <Badge variant="outline" className="text-xs">
                        {template.complexity}
                      </Badge>
                    </div>
                  </CardContent>
                </Card>
              ))}
          </div>
        </TabsContent>

        {/* Visual Designer Tab */}
        <TabsContent value="designer" className="space-y-6">
          {currentWorkflow ? (
            <div className="grid grid-cols-4 gap-6 h-[800px]">
              {/* Component Palette */}
              <div className="space-y-4">
                <h3 className="font-semibold">Components</h3>
                
                {Object.entries(NODE_TYPES).map(([type, config]) => {
                  const Icon = config.icon
                  return (
                    <Button
                      key={type}
                      variant="outline"
                      className="w-full justify-start"
                      onClick={() => handleAddNode(type as keyof typeof NODE_TYPES)}
                    >
                      <Icon className="w-4 h-4 mr-2" />
                      {config.label}
                    </Button>
                  )
                })}

                <div className="pt-4 border-t">
                  <h4 className="font-medium mb-2">AI Agents</h4>
                  <div className="space-y-2">
                    {Object.entries(AI_AGENTS.marketing).map(([pattern, agents]) => (
                      <div key={pattern} className="text-sm">
                        <div className="font-medium text-xs text-muted-foreground uppercase">
                          {pattern}
                        </div>
                        {agents.slice(0, 2).map((agent) => (
                          <Button
                            key={agent}
                            variant="ghost"
                            size="sm"
                            className="w-full justify-start text-xs"
                            onClick={() => {
                              const newNode: WorkflowNode = {
                                id: `agent-${Date.now()}`,
                                type: 'agent',
                                name: agent,
                                description: `${agent} with ${pattern} pattern`,
                                position: { x: 200, y: 200 },
                                config: { agentType: agent.toLowerCase().replace(' ', '_') },
                                agentPattern: pattern as any
                              }
                              if (currentWorkflow) {
                                setCurrentWorkflow({
                                  ...currentWorkflow,
                                  nodes: [...currentWorkflow.nodes, newNode]
                                })
                              }
                            }}
                          >
                            <Brain className="w-3 h-3 mr-1" />
                            {agent}
                          </Button>
                        ))}
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Canvas */}
              <div className="col-span-2 border rounded-lg relative bg-gray-50 overflow-hidden">
                <div className="absolute top-4 left-4 z-10 flex space-x-2">
                  <Input
                    value={workflowName}
                    onChange={(e) => setWorkflowName(e.target.value)}
                    className="w-64"
                    placeholder="Workflow name"
                  />
                  <Button onClick={handlePlay} disabled={isPlaying} size="sm">
                    <Play className="w-4 h-4" />
                  </Button>
                  <Button onClick={handleStop} disabled={!isPlaying} size="sm" variant="outline">
                    <Pause className="w-4 h-4" />
                  </Button>
                  <Button size="sm" variant="outline">
                    <Save className="w-4 h-4" />
                  </Button>
                </div>

                <div ref={canvasRef} className="relative w-full h-full">
                  {currentWorkflow.nodes.map((node) => (
                    <WorkflowNode key={node.id} node={node} />
                  ))}
                  
                  {/* Connection lines would be rendered here */}
                  <svg className="absolute inset-0 pointer-events-none">
                    {currentWorkflow.connections.map((connection) => {
                      const sourceNode = currentWorkflow.nodes.find(n => n.id === connection.sourceId)
                      const targetNode = currentWorkflow.nodes.find(n => n.id === connection.targetId)
                      
                      if (!sourceNode || !targetNode) return null
                      
                      const x1 = sourceNode.position.x + 80
                      const y1 = sourceNode.position.y + 40
                      const x2 = targetNode.position.x
                      const y2 = targetNode.position.y + 40
                      
                      return (
                        <line
                          key={connection.id}
                          x1={x1}
                          y1={y1}
                          x2={x2}
                          y2={y2}
                          stroke="#3b82f6"
                          strokeWidth="2"
                          markerEnd="url(#arrowhead)"
                        />
                      )
                    })}
                    
                    <defs>
                      <marker
                        id="arrowhead"
                        markerWidth="10"
                        markerHeight="7"
                        refX="10"
                        refY="3.5"
                        orient="auto"
                      >
                        <polygon
                          points="0 0, 10 3.5, 0 7"
                          fill="#3b82f6"
                        />
                      </marker>
                    </defs>
                  </svg>
                </div>
              </div>

              {/* Properties Panel */}
              <div className="space-y-4">
                <h3 className="font-semibold">Properties</h3>
                
                {selectedNode ? (
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="node-name">Name</Label>
                      <Input
                        id="node-name"
                        value={selectedNode.name}
                        onChange={(e) => {
                          const updatedNode = { ...selectedNode, name: e.target.value }
                          setSelectedNode(updatedNode)
                          setCurrentWorkflow(prev => prev ? {
                            ...prev,
                            nodes: prev.nodes.map(n => n.id === selectedNode.id ? updatedNode : n)
                          } : null)
                        }}
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="node-description">Description</Label>
                      <Textarea
                        id="node-description"
                        value={selectedNode.description}
                        onChange={(e) => {
                          const updatedNode = { ...selectedNode, description: e.target.value }
                          setSelectedNode(updatedNode)
                          setCurrentWorkflow(prev => prev ? {
                            ...prev,
                            nodes: prev.nodes.map(n => n.id === selectedNode.id ? updatedNode : n)
                          } : null)
                        }}
                      />
                    </div>

                    {selectedNode.type === 'agent' && (
                      <div>
                        <Label htmlFor="agent-pattern">Agent Pattern</Label>
                        <Select 
                          value={selectedNode.agentPattern} 
                          onValueChange={(value) => {
                            const updatedNode = { ...selectedNode, agentPattern: value as any }
                            setSelectedNode(updatedNode)
                            setCurrentWorkflow(prev => prev ? {
                              ...prev,
                              nodes: prev.nodes.map(n => n.id === selectedNode.id ? updatedNode : n)
                            } : null)
                          }}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select pattern" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="4-agent">4-Agent Team</SelectItem>
                            <SelectItem value="3-agent">3-Agent Squad</SelectItem>
                            <SelectItem value="2-agent">2-Agent Pair</SelectItem>
                            <SelectItem value="single-agent">Single Agent</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    )}

                    {selectedNode.type === 'approval' && (
                      <div className="space-y-2">
                        <div className="flex items-center space-x-2">
                          <Switch
                            checked={selectedNode.requiresHuman}
                            onCheckedChange={(checked) => {
                              const updatedNode = { ...selectedNode, requiresHuman: checked }
                              setSelectedNode(updatedNode)
                            }}
                          />
                          <Label>Requires Human Approval</Label>
                        </div>
                        <div>
                          <Label>Approver Role</Label>
                          <Select>
                            <SelectTrigger>
                              <SelectValue placeholder="Select role" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="marketing_manager">Marketing Manager</SelectItem>
                              <SelectItem value="campaign_manager">Campaign Manager</SelectItem>
                              <SelectItem value="admin">Admin</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                    )}
                    
                    <Button
                      variant="destructive"
                      size="sm"
                      onClick={() => {
                        if (currentWorkflow) {
                          setCurrentWorkflow({
                            ...currentWorkflow,
                            nodes: currentWorkflow.nodes.filter(n => n.id !== selectedNode.id)
                          })
                          setSelectedNode(null)
                        }
                      }}
                    >
                      <Trash2 className="w-4 h-4 mr-2" />
                      Delete Node
                    </Button>
                  </div>
                ) : (
                  <div className="text-sm text-muted-foreground">
                    Select a node to edit its properties
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <WorkflowIcon className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No Workflow Selected</h3>
              <p className="text-muted-foreground mb-4">
                Choose a template or create a new workflow to start designing
              </p>
              <div className="flex justify-center space-x-2">
                <Button onClick={() => handleCreateNew('hitl')}>
                  <User className="w-4 h-4 mr-2" />
                  New HITL Workflow
                </Button>
                <Button onClick={() => handleCreateNew('autonomous')} variant="outline">
                  <Bot className="w-4 h-4 mr-2" />
                  New Autonomous Workflow
                </Button>
              </div>
            </div>
          )}
        </TabsContent>

        {/* Execution Monitor Tab */}
        <TabsContent value="execution" className="space-y-6">
          <div className="grid grid-cols-3 gap-6">
            <Card className="col-span-2">
              <CardHeader>
                <CardTitle>Execution Logs</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-black text-green-400 p-4 rounded-lg font-mono text-sm h-96 overflow-y-auto">
                  {executionLogs.length === 0 ? (
                    <div className="text-gray-500">No execution logs yet. Start a workflow to see logs.</div>
                  ) : (
                    executionLogs.map((log, index) => (
                      <div key={index} className="mb-1">
                        [{new Date().toLocaleTimeString()}] {log}
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>

            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Active Workflows</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between p-2 border rounded">
                      <div className="text-sm">
                        <div className="font-medium">Lead Nurture Campaign</div>
                        <div className="text-xs text-muted-foreground">Running for 2h 34m</div>
                      </div>
                      <Badge className="bg-green-500">Running</Badge>
                    </div>
                    <div className="flex items-center justify-between p-2 border rounded">
                      <div className="text-sm">
                        <div className="font-medium">Content Approval</div>
                        <div className="text-xs text-muted-foreground">Waiting for approval</div>
                      </div>
                      <Badge variant="secondary">Pending</Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Performance Metrics</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-sm">Success Rate</span>
                      <span className="font-medium">94.2%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Avg. Duration</span>
                      <span className="font-medium">1.2h</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Total Executions</span>
                      <span className="font-medium">1,247</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        {/* Namespace Manager Tab */}
        <TabsContent value="namespaces" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {[
              { name: 'marketing-campaigns-001', workflows: 23, active: 8, capacity: '87%' },
              { name: 'sales-automation-002', workflows: 15, active: 12, capacity: '64%' },
              { name: 'customer-support-003', workflows: 31, active: 6, capacity: '45%' },
              { name: 'analytics-reports-004', workflows: 18, active: 15, capacity: '92%' },
              { name: 'operations-mgmt-005', workflows: 7, active: 3, capacity: '23%' }
            ].map((namespace) => (
              <Card key={namespace.name}>
                <CardHeader>
                  <CardTitle className="text-sm">{namespace.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Total Workflows</span>
                      <span className="font-medium">{namespace.workflows}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Active</span>
                      <span className="font-medium">{namespace.active}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Capacity</span>
                      <Badge variant={parseInt(namespace.capacity) > 80 ? "destructive" : "default"}>
                        {namespace.capacity}
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}