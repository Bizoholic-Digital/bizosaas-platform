'use client'

import React, { useEffect, useRef, useState, useCallback, useMemo } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Separator } from '@/components/ui/separator'
import { 
  Play, 
  Pause, 
  Square, 
  RefreshCw, 
  Zap, 
  Clock, 
  CheckCircle, 
  XCircle, 
  AlertCircle,
  Activity,
  BarChart3,
  Maximize,
  Minimize,
  ArrowRight
} from 'lucide-react'

// Types
interface WorkflowNode {
  id: string
  name: string
  type: 'agent' | 'task' | 'decision'
  status: 'idle' | 'working' | 'waiting' | 'completed' | 'failed'
  start_time?: string
  end_time?: string
  duration?: number
  metrics?: Record<string, number>
  error?: string
}

interface WorkflowEdge {
  from_node: string
  to_node: string
  condition?: string
  data_flow?: Record<string, any>
}

interface WorkflowState {
  workflow_id: string
  company_id: string
  workflow_type: string
  status: 'pending' | 'running' | 'paused' | 'completed' | 'failed' | 'cancelled'
  nodes: Record<string, WorkflowNode>
  edges: WorkflowEdge[]
  start_time: string
  end_time?: string
  progress_percentage: number
  current_node?: string
  estimated_completion?: string
  performance_metrics?: Record<string, number>
}

interface WorkflowVisualizationProps {
  workflowId?: string
  platform?: 'bizoholic' | 'coreldove' | 'thrillring'
  workflowType?: string
  autoStart?: boolean
  height?: string
  showControls?: boolean
  showMetrics?: boolean
  className?: string
}

const WorkflowVisualization: React.FC<WorkflowVisualizationProps> = ({
  workflowId,
  platform = 'bizoholic',
  workflowType = 'marketing_campaign',
  autoStart = false,
  height = '400px',
  showControls = true,
  showMetrics = true,
  className = ''
}) => {
  // Refs
  const diagramRef = useRef<HTMLDivElement>(null)
  const websocketRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>()
  
  // State
  const [workflowState, setWorkflowState] = useState<WorkflowState | null>(null)
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('disconnected')
  const [error, setError] = useState<string>('')
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [performanceMetrics, setPerformanceMetrics] = useState<Record<string, number>>({})
  const [reconnectAttempts, setReconnectAttempts] = useState(0)
  const maxReconnectAttempts = 5

  // Mock auth store for now
  const token = 'demo-token'
  const user = { companyId: 'demo-company' }

  // Mock workflow data for demo
  const mockWorkflowState: WorkflowState = useMemo(() => ({
    workflow_id: 'demo-workflow-001',
    company_id: 'demo-company',
    workflow_type: 'marketing_campaign',
    status: 'running',
    nodes: {
      'start': {
        id: 'start',
        name: 'Start Campaign',
        type: 'task',
        status: 'completed',
        start_time: '2025-01-15T10:00:00Z',
        end_time: '2025-01-15T10:01:00Z',
        duration: 60
      },
      'analyze': {
        id: 'analyze',
        name: 'Analyze Target Audience',
        type: 'agent',
        status: 'completed',
        start_time: '2025-01-15T10:01:00Z',
        end_time: '2025-01-15T10:05:00Z',
        duration: 240
      },
      'create': {
        id: 'create',
        name: 'Create Content',
        type: 'agent',
        status: 'working',
        start_time: '2025-01-15T10:05:00Z',
        duration: 120
      },
      'review': {
        id: 'review',
        name: 'Review & Approve',
        type: 'decision',
        status: 'waiting',
      },
      'deploy': {
        id: 'deploy',
        name: 'Deploy Campaign',
        type: 'task',
        status: 'idle',
      }
    },
    edges: [
      { from_node: 'start', to_node: 'analyze' },
      { from_node: 'analyze', to_node: 'create' },
      { from_node: 'create', to_node: 'review' },
      { from_node: 'review', to_node: 'deploy' }
    ],
    start_time: '2025-01-15T10:00:00Z',
    progress_percentage: 65,
    current_node: 'create',
    estimated_completion: '2025-01-15T10:15:00Z'
  }), [])

  // Initialize with mock data
  useEffect(() => {
    setWorkflowState(mockWorkflowState)
    setPerformanceMetrics({
      'avg_response_time': 2.3,
      'success_rate': 96.8,
      'active_agents': 12,
      'completed_tasks': 847
    })
  }, [mockWorkflowState])

  // WebSocket connection
  const connectWebSocket = useCallback(() => {
    if (!token || !user) {
      setError('Authentication required for real-time updates')
      return
    }

    if (websocketRef.current?.readyState === WebSocket.OPEN) {
      return // Already connected
    }

    setConnectionStatus('connecting')
    setError('')

    const wsUrl = process.env.NEXT_PUBLIC_API_URL?.replace('http', 'ws') || 'ws://localhost:8000'
    const wsEndpoint = `${wsUrl}/api/v1/workflows/visualization/ws?token=${token}&platforms=${platform}`

    try {
      const ws = new WebSocket(wsEndpoint)
      
      ws.onopen = () => {
        setConnectionStatus('connected')
        setReconnectAttempts(0)
        console.log('Workflow visualization WebSocket connected')
        
        // Subscribe to specific workflow if provided
        if (workflowId) {
          ws.send(JSON.stringify({
            type: 'subscribe_workflow',
            workflow_id: workflowId
          }))
        }
      }

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          handleWebSocketMessage(message)
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err)
        }
      }

      ws.onclose = () => {
        setConnectionStatus('disconnected')
        console.log('Workflow visualization WebSocket disconnected')
        
        // Attempt to reconnect
        if (reconnectAttempts < maxReconnectAttempts) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000)
          reconnectTimeoutRef.current = setTimeout(() => {
            setReconnectAttempts(prev => prev + 1)
            connectWebSocket()
          }, delay)
        }
      }

      ws.onerror = (error) => {
        console.error('Workflow visualization WebSocket error:', error)
        setError('WebSocket connection error')
      }

      websocketRef.current = ws
    } catch (err) {
      setError('Failed to create WebSocket connection')
      setConnectionStatus('disconnected')
    }
  }, [token, user, platform, workflowId, reconnectAttempts])

  // Handle WebSocket messages
  const handleWebSocketMessage = useCallback((message: any) => {
    switch (message.type) {
      case 'workflow_update':
        if (!workflowId || message.workflow_id === workflowId) {
          setWorkflowState(message.workflow_state)
        }
        break
        
      case 'initial_workflows':
        if (workflowId && message.workflows[workflowId]) {
          setWorkflowState(message.workflows[workflowId])
        }
        break
        
      case 'workflow_subscribed':
        if (message.workflow_id === workflowId) {
          setWorkflowState(message.workflow_state)
        }
        break
        
      case 'performance_update':
        if (message.company_id === user?.companyId) {
          setPerformanceMetrics(message.metrics)
        }
        break
        
      case 'pong':
        // Heartbeat response
        break
        
      default:
        console.log('Unhandled message type:', message.type)
    }
  }, [workflowId, user?.companyId])

  // Connect on mount and when dependencies change
  useEffect(() => {
    if (token && user) {
      connectWebSocket()
    }

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
      if (websocketRef.current) {
        websocketRef.current.close()
      }
    }
  }, [connectWebSocket])

  // Auto-start workflow
  useEffect(() => {
    if (autoStart && !workflowId && token) {
      startNewWorkflow()
    }
  }, [autoStart, workflowId, token])

  // React-based diagram component
  const WorkflowDiagram = () => {
    if (!workflowState) return null

    const nodePositions = {
      start: { x: 120, y: 80 },
      analyze: { x: 280, y: 80 },
      create: { x: 440, y: 80 },
      review: { x: 600, y: 80 },
      deploy: { x: 760, y: 80 }
    }

    return (
      <div className="relative w-full h-full min-h-[300px] min-w-[900px] bg-white rounded-lg border overflow-x-auto">
        {/* SVG for connections */}
        <svg className="absolute inset-0 w-full h-full">
          {workflowState.edges.map((edge, index) => {
            const fromPos = nodePositions[edge.from_node as keyof typeof nodePositions]
            const toPos = nodePositions[edge.to_node as keyof typeof nodePositions]
            if (!fromPos || !toPos) return null
            
            return (
              <line
                key={index}
                x1={fromPos.x + 70}
                y1={fromPos.y}
                x2={toPos.x - 70}
                y2={toPos.y}
                stroke="#64748b"
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
              refX="9"
              refY="3.5"
              orient="auto"
            >
              <polygon
                points="0 0, 10 3.5, 0 7"
                fill="#64748b"
              />
            </marker>
          </defs>
        </svg>
        
        {/* Nodes */}
        {Object.entries(workflowState.nodes).map(([nodeId, node]) => {
          const position = nodePositions[nodeId as keyof typeof nodePositions]
          if (!position) return null
          
          return (
            <div
              key={nodeId}
              className={`absolute cursor-pointer transition-all duration-200 hover:scale-105`}
              style={{
                left: position.x,
                top: position.y,
                transform: 'translate(-50%, -50%)'
              }}
              onClick={() => handleNodeClick(nodeId, node)}
            >
              <div className={`
                px-3 py-2 rounded-lg border-2 bg-white shadow-md w-[140px] text-center
                ${
                  node.status === 'completed' ? 'border-green-500 bg-green-50' :
                  node.status === 'working' ? 'border-blue-500 bg-blue-50 animate-pulse' :
                  node.status === 'failed' ? 'border-red-500 bg-red-50' :
                  node.status === 'waiting' ? 'border-yellow-500 bg-yellow-50' :
                  'border-gray-300'
                }
              `}>
                <div className="flex items-center justify-center mb-1">
                  {getStatusIcon(node.status)}
                </div>
                <h4 className="font-medium text-sm">{node.name}</h4>
                <p className="text-xs text-gray-600 capitalize">{node.type}</p>
              </div>
            </div>
          )
        })}
      </div>
    )
  }

  const handleNodeClick = (nodeId: string, node: WorkflowNode) => {
    console.log('Node clicked:', nodeId, node)
    // Could show detailed node information in a modal
  }

  // API calls
  const startNewWorkflow = async () => {
    if (!token || !workflowType) return

    try {
      const response = await fetch('/api/v1/workflows/visualization/start', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          workflow_id: `${platform}_${workflowType}_${Date.now()}`,
          workflow_type: workflowType,
          platform
        })
      })

      if (!response.ok) {
        throw new Error('Failed to start workflow')
      }

      const result = await response.json()
      console.log('Workflow started:', result)
    } catch (err) {
      setError('Failed to start workflow')
      console.error(err)
    }
  }

  const pauseWorkflow = async () => {
    if (!workflowId || !token) return

    try {
      const response = await fetch(`/api/v1/workflows/${workflowId}/pause`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('Failed to pause workflow')
      }
    } catch (err) {
      setError('Failed to pause workflow')
      console.error(err)
    }
  }

  const resumeWorkflow = async () => {
    if (!workflowId || !token) return

    try {
      const response = await fetch(`/api/v1/workflows/${workflowId}/resume`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('Failed to resume workflow')
      }
    } catch (err) {
      setError('Failed to resume workflow')
      console.error(err)
    }
  }

  const stopWorkflow = async () => {
    if (!workflowId || !token) return

    try {
      const response = await fetch(`/api/v1/workflows/${workflowId}/stop`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('Failed to stop workflow')
      }
    } catch (err) {
      setError('Failed to stop workflow')
      console.error(err)
    }
  }

  // Helper functions
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-4 h-4 text-green-500" />
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

  const formatDuration = (seconds?: number) => {
    if (!seconds) return 'N/A'
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const sendHeartbeat = () => {
    if (websocketRef.current?.readyState === WebSocket.OPEN) {
      websocketRef.current.send(JSON.stringify({ type: 'ping' }))
    }
  }

  // Heartbeat interval
  useEffect(() => {
    const interval = setInterval(sendHeartbeat, 30000) // 30 seconds
    return () => clearInterval(interval)
  }, [])

  // Render
  return (
    <div className={`workflow-visualization ${className} ${isFullscreen ? 'fixed inset-0 z-50 bg-white' : ''}`}>
      <Card>
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <CardTitle className="text-lg font-semibold">
                Workflow Visualization
              </CardTitle>
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${
                  connectionStatus === 'connected' ? 'bg-green-500' :
                  connectionStatus === 'connecting' ? 'bg-yellow-500' :
                  'bg-red-500'
                }`} />
                <span className="text-sm text-gray-600 capitalize">
                  {connectionStatus}
                </span>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              {workflowState && (
                <Badge className={getStatusColor(workflowState.status)}>
                  {getStatusIcon(workflowState.status)}
                  <span className="ml-1 capitalize">{workflowState.status}</span>
                </Badge>
              )}

              {showControls && (
                <div className="flex items-center space-x-1">
                  {!workflowId && (
                    <Button size="sm" onClick={startNewWorkflow} disabled={!token}>
                      <Play className="w-4 h-4" />
                    </Button>
                  )}
                  {workflowState?.status === 'running' && (
                    <Button size="sm" variant="outline" onClick={pauseWorkflow}>
                      <Pause className="w-4 h-4" />
                    </Button>
                  )}
                  {workflowState?.status === 'paused' && (
                    <Button size="sm" variant="outline" onClick={resumeWorkflow}>
                      <RefreshCw className="w-4 h-4" />
                    </Button>
                  )}
                  {workflowState && ['running', 'paused'].includes(workflowState.status) && (
                    <Button size="sm" variant="outline" onClick={stopWorkflow}>
                      <Square className="w-4 h-4" />
                    </Button>
                  )}
                  <Button 
                    size="sm" 
                    variant="outline" 
                    onClick={() => setIsFullscreen(!isFullscreen)}
                  >
                    {isFullscreen ? <Minimize className="w-4 h-4" /> : <Maximize className="w-4 h-4" />}
                  </Button>
                </div>
              )}
            </div>
          </div>

          {workflowState && (
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <span>{workflowState.workflow_type.replace('_', ' ')} • {platform}</span>
              <Progress value={workflowState.progress_percentage} className="flex-1 max-w-xs" />
              <span>{workflowState.progress_percentage.toFixed(1)}%</span>
            </div>
          )}
        </CardHeader>

        <CardContent>
          {error && (
            <Alert className="mb-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <Tabs defaultValue="diagram" className="space-y-4">
            <TabsList>
              <TabsTrigger value="diagram">Workflow Diagram</TabsTrigger>
              {showMetrics && (
                <TabsTrigger value="metrics">Performance</TabsTrigger>
              )}
              <TabsTrigger value="nodes">Node Details</TabsTrigger>
            </TabsList>

            <TabsContent value="diagram" className="space-y-4">
              <div 
                ref={diagramRef}
                className="workflow-diagram border rounded-lg p-4 bg-gray-50 overflow-x-auto overflow-y-hidden"
                style={{ height, minHeight: '300px' }}
              >
                <WorkflowDiagram />
              </div>
              {!workflowState && !error && (
                <div className="flex items-center justify-center h-64 text-gray-500">
                  <div className="text-center">
                    <Activity className="w-8 h-8 mx-auto mb-2 animate-pulse" />
                    <p>Waiting for workflow data...</p>
                  </div>
                </div>
              )}
            </TabsContent>

            {showMetrics && (
              <TabsContent value="metrics" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {Object.entries(performanceMetrics).map(([key, value]) => (
                    <Card key={key}>
                      <CardContent className="p-4">
                        <div className="flex items-center space-x-2">
                          <BarChart3 className="w-4 h-4 text-blue-500" />
                          <span className="font-medium text-sm">{key.replace('_', ' ')}</span>
                        </div>
                        <p className="text-2xl font-bold mt-2">{
                          typeof value === 'number' ? value.toFixed(2) : value
                        }</p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>
            )}

            <TabsContent value="nodes" className="space-y-4">
              {workflowState ? (
                <div className="space-y-2">
                  {Object.entries(workflowState.nodes).map(([nodeId, node]) => (
                    <Card key={nodeId} className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          {getStatusIcon(node.status)}
                          <div>
                            <h4 className="font-medium">{node.name}</h4>
                            <p className="text-sm text-gray-600 capitalize">{node.type}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-4 text-sm text-gray-600">
                          <span>Duration: {formatDuration(node.duration)}</span>
                          <Badge className={getStatusColor(node.status)}>
                            {node.status}
                          </Badge>
                        </div>
                      </div>
                      {node.error && (
                        <Alert className="mt-2">
                          <XCircle className="h-4 w-4" />
                          <AlertDescription>{node.error}</AlertDescription>
                        </Alert>
                      )}
                    </Card>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">No workflow data available</p>
              )}
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}

export default WorkflowVisualization