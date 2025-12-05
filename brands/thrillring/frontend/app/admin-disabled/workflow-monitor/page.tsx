'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Progress } from '@/components/ui/progress'
import { 
  Brain,
  Activity, 
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  Clock,
  TrendingUp,
  Target,
  Zap,
  RefreshCw,
  Play,
  Pause,
  Settings,
  BarChart3,
  Users,
  Shield,
  Wrench,
  Lightbulb,
  Database,
  Monitor,
  FileText,
  Plus,
  Filter,
  Calendar
} from 'lucide-react'

interface ImprovementTask {
  id: string
  title: string
  description: string
  category: 'performance' | 'security' | 'user_experience' | 'infrastructure' | 'features' | 'optimization' | 'monitoring' | 'documentation'
  priority: 'critical' | 'high' | 'medium' | 'low'
  estimated_effort: string
  impact_score: number
  confidence: number
  data_source: string
  metrics: Record<string, any>
  suggested_solution: string
  dependencies: string[]
  tenant_specific?: string
  created_at: string
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled' | 'on_hold'
}

interface TaskSummary {
  total_tasks: number
  by_priority: Record<string, number>
  by_category: Record<string, number>
  by_status: Record<string, number>
}

const categoryIcons = {
  performance: TrendingUp,
  security: Shield,
  user_experience: Users,
  infrastructure: Database,
  features: Lightbulb,
  optimization: Zap,
  monitoring: Monitor,
  documentation: FileText
}

const categoryColors = {
  performance: 'bg-blue-100 text-blue-800',
  security: 'bg-red-100 text-red-800',
  user_experience: 'bg-green-100 text-green-800',
  infrastructure: 'bg-purple-100 text-purple-800',
  features: 'bg-yellow-100 text-yellow-800',
  optimization: 'bg-orange-100 text-orange-800',
  monitoring: 'bg-indigo-100 text-indigo-800',
  documentation: 'bg-gray-100 text-gray-800'
}

const priorityColors = {
  critical: 'bg-red-500 text-white',
  high: 'bg-orange-500 text-white', 
  medium: 'bg-yellow-500 text-white',
  low: 'bg-green-500 text-white'
}

export default function WorkflowMonitorPage() {
  const [tasks, setTasks] = useState<ImprovementTask[]>([])
  const [taskSummary, setTaskSummary] = useState<TaskSummary | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isRunningCycle, setIsRunningCycle] = useState(false)
  const [selectedFilters, setSelectedFilters] = useState({
    priority: 'all',
    category: 'all',
    status: 'pending'
  })
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [alerts, setAlerts] = useState<{ type: 'success' | 'error' | 'info', message: string }[]>([])
  const [dashboardData, setDashboardData] = useState<any>(null)

  useEffect(() => {
    fetchDashboardData()
    fetchTasks()
    fetchTaskSummary()
  }, [selectedFilters])

  const addAlert = (type: 'success' | 'error' | 'info', message: string) => {
    const alert = { type, message }
    setAlerts(prev => [...prev, alert])
    setTimeout(() => {
      setAlerts(prev => prev.filter(a => a !== alert))
    }, 5000)
  }

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('/api/brain/workflow-monitor/dashboard')
      if (response.ok) {
        const data = await response.json()
        setDashboardData(data.dashboard)
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    }
  }

  const fetchTasks = async () => {
    try {
      const params = new URLSearchParams({
        limit: '50',
        ...(selectedFilters.priority !== 'all' && { priority: selectedFilters.priority }),
        ...(selectedFilters.category !== 'all' && { category: selectedFilters.category }),
        status: selectedFilters.status
      })
      
      const response = await fetch(`/api/brain/workflow-monitor/tasks?${params}`)
      if (response.ok) {
        const data = await response.json()
        setTasks(data.tasks)
      } else {
        addAlert('error', 'Failed to fetch improvement tasks')
      }
    } catch (error) {
      addAlert('error', 'Network error while fetching tasks')
    } finally {
      setIsLoading(false)
    }
  }

  const fetchTaskSummary = async () => {
    try {
      const response = await fetch('/api/brain/workflow-monitor/summary')
      if (response.ok) {
        const data = await response.json()
        setTaskSummary(data.summary)
      }
    } catch (error) {
      console.error('Error fetching task summary:', error)
    }
  }

  const runMonitoringCycle = async () => {
    setIsRunningCycle(true)
    try {
      const response = await fetch('/api/brain/workflow-monitor/run-cycle', { method: 'POST' })
      if (response.ok) {
        const data = await response.json()
        addAlert('success', `Monitoring cycle completed. Generated ${data.tasks_generated} new tasks.`)
        fetchTasks()
        fetchTaskSummary()
        fetchDashboardData()
      } else {
        addAlert('error', 'Failed to run monitoring cycle')
      }
    } catch (error) {
      addAlert('error', 'Network error while running monitoring cycle')
    } finally {
      setIsRunningCycle(false)
    }
  }

  const updateTaskStatus = async (taskId: string, newStatus: string) => {
    try {
      const response = await fetch(`/api/brain/workflow-monitor/tasks/${taskId}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      })
      
      if (response.ok) {
        setTasks(prev => prev.map(task => 
          task.id === taskId ? { ...task, status: newStatus as any } : task
        ))
        addAlert('success', 'Task status updated successfully')
        fetchTaskSummary()
      } else {
        addAlert('error', 'Failed to update task status')
      }
    } catch (error) {
      addAlert('error', 'Network error while updating task')
    }
  }

  const TaskCard = ({ task }: { task: ImprovementTask }) => {
    const IconComponent = categoryIcons[task.category]
    const categoryColorClass = categoryColors[task.category]
    const priorityColorClass = priorityColors[task.priority]

    return (
      <Card className="hover:shadow-lg transition-shadow">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex items-center space-x-3">
              <div className={`p-2 rounded-lg ${categoryColorClass}`}>
                <IconComponent className="w-4 h-4" />
              </div>
              <div className="flex-1">
                <CardTitle className="text-lg">{task.title}</CardTitle>
                <CardDescription className="text-sm mt-1">{task.description}</CardDescription>
              </div>
            </div>
            <Badge className={priorityColorClass}>
              {task.priority}
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex flex-wrap gap-2">
              <Badge variant="outline" className={categoryColorClass}>
                {task.category.replace('_', ' ')}
              </Badge>
              <Badge variant="secondary">
                {task.estimated_effort}
              </Badge>
              <Badge variant="outline">
                Impact: {task.impact_score}/10
              </Badge>
            </div>

            {task.suggested_solution && (
              <div className="text-sm">
                <Label className="text-xs font-medium text-muted-foreground">Suggested Solution:</Label>
                <p className="mt-1">{task.suggested_solution}</p>
              </div>
            )}

            {task.dependencies.length > 0 && (
              <div className="text-sm">
                <Label className="text-xs font-medium text-muted-foreground">Dependencies:</Label>
                <div className="mt-1 flex flex-wrap gap-1">
                  {task.dependencies.map((dep, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {dep}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            <div className="flex items-center justify-between">
              <div className="text-xs text-muted-foreground">
                Confidence: {(task.confidence * 100).toFixed(0)}% • Source: {task.data_source}
              </div>
              
              <Select
                value={task.status}
                onValueChange={(value) => updateTaskStatus(task.id, value)}
              >
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="pending">Pending</SelectItem>
                  <SelectItem value="in_progress">In Progress</SelectItem>
                  <SelectItem value="completed">Completed</SelectItem>
                  <SelectItem value="on_hold">On Hold</SelectItem>
                  <SelectItem value="cancelled">Cancelled</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  const CreateTaskModal = () => {
    const [formData, setFormData] = useState({
      title: '',
      description: '',
      category: 'features',
      priority: 'medium',
      estimated_effort: '1-2 days',
      impact_score: 5,
      suggested_solution: '',
      dependencies: '',
      tenant_specific: ''
    })

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault()
      
      try {
        const taskData = {
          ...formData,
          dependencies: formData.dependencies.split(',').map(d => d.trim()).filter(d => d),
          tenant_specific: formData.tenant_specific || undefined
        }
        
        const response = await fetch('/api/brain/workflow-monitor/tasks/manual', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(taskData)
        })
        
        if (response.ok) {
          addAlert('success', 'Manual task created successfully')
          setShowCreateModal(false)
          fetchTasks()
          fetchTaskSummary()
          setFormData({
            title: '',
            description: '',
            category: 'features',
            priority: 'medium',
            estimated_effort: '1-2 days',
            impact_score: 5,
            suggested_solution: '',
            dependencies: '',
            tenant_specific: ''
          })
        } else {
          addAlert('error', 'Failed to create manual task')
        }
      } catch (error) {
        addAlert('error', 'Network error while creating task')
      }
    }

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
          <CardHeader>
            <CardTitle>Create Manual Improvement Task</CardTitle>
            <CardDescription>Add a custom improvement task to the workflow monitor</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2">
                  <Label htmlFor="title">Task Title</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                    required
                  />
                </div>
                
                <div className="col-span-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    value={formData.description}
                    onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                    required
                  />
                </div>
                
                <div>
                  <Label>Category</Label>
                  <Select
                    value={formData.category}
                    onValueChange={(value) => setFormData(prev => ({ ...prev, category: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="performance">Performance</SelectItem>
                      <SelectItem value="security">Security</SelectItem>
                      <SelectItem value="user_experience">User Experience</SelectItem>
                      <SelectItem value="infrastructure">Infrastructure</SelectItem>
                      <SelectItem value="features">Features</SelectItem>
                      <SelectItem value="optimization">Optimization</SelectItem>
                      <SelectItem value="monitoring">Monitoring</SelectItem>
                      <SelectItem value="documentation">Documentation</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <Label>Priority</Label>
                  <Select
                    value={formData.priority}
                    onValueChange={(value) => setFormData(prev => ({ ...prev, priority: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="critical">Critical</SelectItem>
                      <SelectItem value="high">High</SelectItem>
                      <SelectItem value="medium">Medium</SelectItem>
                      <SelectItem value="low">Low</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <Label htmlFor="estimated_effort">Estimated Effort</Label>
                  <Input
                    id="estimated_effort"
                    value={formData.estimated_effort}
                    onChange={(e) => setFormData(prev => ({ ...prev, estimated_effort: e.target.value }))}
                    placeholder="e.g., 1-2 days"
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="impact_score">Impact Score (1-10)</Label>
                  <Input
                    id="impact_score"
                    type="number"
                    min="1"
                    max="10"
                    value={formData.impact_score}
                    onChange={(e) => setFormData(prev => ({ ...prev, impact_score: parseInt(e.target.value) }))}
                    required
                  />
                </div>
                
                <div className="col-span-2">
                  <Label htmlFor="suggested_solution">Suggested Solution</Label>
                  <Textarea
                    id="suggested_solution"
                    value={formData.suggested_solution}
                    onChange={(e) => setFormData(prev => ({ ...prev, suggested_solution: e.target.value }))}
                  />
                </div>
                
                <div>
                  <Label htmlFor="dependencies">Dependencies (comma-separated)</Label>
                  <Input
                    id="dependencies"
                    value={formData.dependencies}
                    onChange={(e) => setFormData(prev => ({ ...prev, dependencies: e.target.value }))}
                    placeholder="task1, task2, task3"
                  />
                </div>
                
                <div>
                  <Label htmlFor="tenant_specific">Tenant Specific</Label>
                  <Input
                    id="tenant_specific"
                    value={formData.tenant_specific}
                    onChange={(e) => setFormData(prev => ({ ...prev, tenant_specific: e.target.value }))}
                    placeholder="tenant_id (optional)"
                  />
                </div>
              </div>
              
              <div className="flex justify-end space-x-2">
                <Button type="button" variant="outline" onClick={() => setShowCreateModal(false)}>
                  Cancel
                </Button>
                <Button type="submit">
                  Create Task
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Alerts */}
      {alerts.map((alert, index) => (
        <Alert key={index} className={
          alert.type === 'error' ? 'border-red-200 bg-red-50' : 
          alert.type === 'info' ? 'border-blue-200 bg-blue-50' :
          'border-green-200 bg-green-50'
        }>
          <AlertDescription>{alert.message}</AlertDescription>
        </Alert>
      ))}

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center">
            <Brain className="w-8 h-8 mr-3 text-purple-600" />
            AI Workflow Monitor
          </h1>
          <p className="text-muted-foreground">Autonomous monitoring and continuous improvement system</p>
        </div>
        <div className="flex space-x-2">
          <Button
            onClick={runMonitoringCycle}
            disabled={isRunningCycle}
            className="bg-purple-600 hover:bg-purple-700"
          >
            {isRunningCycle ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Play className="w-4 h-4 mr-2" />
            )}
            Run Monitoring Cycle
          </Button>
          <Button
            variant="outline"
            onClick={() => setShowCreateModal(true)}
          >
            <Plus className="w-4 h-4 mr-2" />
            Create Task
          </Button>
        </div>
      </div>

      {/* Dashboard Overview */}
      {taskSummary && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Tasks</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{taskSummary.total_tasks}</div>
              <p className="text-xs text-muted-foreground">
                {taskSummary.by_status.pending || 0} pending
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Critical Tasks</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">
                {taskSummary.by_priority.critical || 0}
              </div>
              <p className="text-xs text-muted-foreground">
                Requires immediate attention
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Completed</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">
                {taskSummary.by_status.completed || 0}
              </div>
              <p className="text-xs text-muted-foreground">
                Successfully resolved
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">In Progress</CardTitle>
              <Clock className="h-4 w-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">
                {taskSummary.by_status.in_progress || 0}
              </div>
              <p className="text-xs text-muted-foreground">
                Currently being worked on
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-wrap gap-4">
            <div>
              <Label>Priority Filter</Label>
              <Select
                value={selectedFilters.priority}
                onValueChange={(value) => setSelectedFilters(prev => ({ ...prev, priority: value }))}
              >
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Priorities</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="low">Low</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div>
              <Label>Category Filter</Label>
              <Select
                value={selectedFilters.category}
                onValueChange={(value) => setSelectedFilters(prev => ({ ...prev, category: value }))}
              >
                <SelectTrigger className="w-40">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  <SelectItem value="performance">Performance</SelectItem>
                  <SelectItem value="security">Security</SelectItem>
                  <SelectItem value="user_experience">User Experience</SelectItem>
                  <SelectItem value="infrastructure">Infrastructure</SelectItem>
                  <SelectItem value="features">Features</SelectItem>
                  <SelectItem value="optimization">Optimization</SelectItem>
                  <SelectItem value="monitoring">Monitoring</SelectItem>
                  <SelectItem value="documentation">Documentation</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div>
              <Label>Status Filter</Label>
              <Select
                value={selectedFilters.status}
                onValueChange={(value) => setSelectedFilters(prev => ({ ...prev, status: value }))}
              >
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="pending">Pending</SelectItem>
                  <SelectItem value="in_progress">In Progress</SelectItem>
                  <SelectItem value="completed">Completed</SelectItem>
                  <SelectItem value="on_hold">On Hold</SelectItem>
                  <SelectItem value="cancelled">Cancelled</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tasks List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold">Improvement Tasks ({tasks.length})</h2>
          <Button variant="outline" onClick={() => { fetchTasks(); fetchTaskSummary(); }}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        </div>
        
        {tasks.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
              <p className="text-lg font-semibold text-muted-foreground">No tasks found</p>
              <p className="text-sm text-muted-foreground mt-2">
                All improvement tasks are completed or no issues detected with current filters
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {tasks.map((task) => (
              <TaskCard key={task.id} task={task} />
            ))}
          </div>
        )}
      </div>

      {/* Create Task Modal */}
      {showCreateModal && <CreateTaskModal />}
    </div>
  )
}