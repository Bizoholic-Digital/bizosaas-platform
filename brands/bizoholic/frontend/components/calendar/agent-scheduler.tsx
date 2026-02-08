'use client'

import { useState, useEffect } from 'react'
import { DayPicker } from 'react-day-picker'
import { format, addMinutes, addHours, isBefore, isAfter } from 'date-fns'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Textarea } from '@/components/ui/textarea'
import { Switch } from '@/components/ui/switch'
import { Bot, Clock, Play, Pause, Settings, Timer, Zap, AlertCircle } from 'lucide-react'
import { useAIAgentsData } from '@/hooks/use-ai-agents-live'

// Types for AI agent scheduling
interface AgentTask {
  id: string
  agent_id: string
  agent_name: string
  agent_type: string
  task_name: string
  description: string
  scheduled_time: Date
  estimated_duration: number // in minutes
  priority: 'low' | 'medium' | 'high' | 'critical'
  status: 'scheduled' | 'running' | 'completed' | 'failed' | 'cancelled'
  tenant_id: string
  recurring: boolean
  recurrence_pattern?: string
  dependencies: string[] // other task IDs this depends on
  parameters: Record<string, any>
  max_retries: number
  retry_count: number
  last_execution?: Date
  next_execution?: Date
}

interface AgentSchedulerProps {
  tenantId?: string
  agentId?: string
  className?: string
}

export function AgentScheduler({ tenantId, agentId, className }: AgentSchedulerProps) {
  const [selected, setSelected] = useState<Date | undefined>(new Date())
  const [tasks, setTasks] = useState<AgentTask[]>([])
  const [isScheduling, setIsScheduling] = useState(false)
  const [selectedTask, setSelectedTask] = useState<AgentTask | null>(null)
  const [newTask, setNewTask] = useState<Partial<AgentTask>>({
    task_name: '',
    description: '',
    estimated_duration: 30,
    priority: 'medium',
    recurring: false,
    max_retries: 3
  })

  const { data: agentsData, isLoading } = useAIAgentsData()

  // Mock data for AI agent tasks
  useEffect(() => {
    const mockTasks: AgentTask[] = [
      {
        id: '1',
        agent_id: 'marketing-strategist',
        agent_name: 'Marketing Strategist',
        agent_type: 'marketing',
        task_name: 'Campaign Analysis',
        description: 'Analyze current campaign performance and provide optimization recommendations',
        scheduled_time: addHours(new Date(), 2),
        estimated_duration: 45,
        priority: 'high',
        status: 'scheduled',
        tenant_id: 'tenant_1',
        recurring: true,
        recurrence_pattern: 'daily',
        dependencies: [],
        parameters: {
          campaign_ids: ['camp_1', 'camp_2'],
          analysis_depth: 'comprehensive'
        },
        max_retries: 3,
        retry_count: 0
      },
      {
        id: '2',
        agent_id: 'seo-optimizer',
        agent_name: 'SEO Optimizer',
        agent_type: 'seo',
        task_name: 'Keyword Research',
        description: 'Research new keyword opportunities for client websites',
        scheduled_time: addHours(new Date(), 24),
        estimated_duration: 60,
        priority: 'medium',
        status: 'scheduled',
        tenant_id: 'tenant_2',
        recurring: false,
        dependencies: [],
        parameters: {
          target_domains: ['client1.com', 'client2.com'],
          keyword_count: 100
        },
        max_retries: 2,
        retry_count: 0
      },
      {
        id: '3',
        agent_id: 'content-creator',
        agent_name: 'Content Creator',
        agent_type: 'content',
        task_name: 'Blog Post Generation',
        description: 'Generate weekly blog posts for client websites',
        scheduled_time: addHours(new Date(), 48),
        estimated_duration: 90,
        priority: 'medium',
        status: 'scheduled',
        tenant_id: 'tenant_3',
        recurring: true,
        recurrence_pattern: 'weekly',
        dependencies: ['2'], // depends on SEO research
        parameters: {
          post_count: 3,
          topics: ['technology', 'business', 'marketing']
        },
        max_retries: 3,
        retry_count: 0
      }
    ]
    setTasks(mockTasks)
  }, [])

  // Filter tasks by tenant and agent if specified
  const filteredTasks = tasks.filter(task => {
    if (tenantId && task.tenant_id !== tenantId) return false
    if (agentId && task.agent_id !== agentId) return false
    return true
  })

  // Get tasks for selected date
  const selectedDateTasks = filteredTasks.filter(task => 
    selected && format(task.scheduled_time, 'yyyy-MM-dd') === format(selected, 'yyyy-MM-dd')
  )

  // Get available agents
  const availableAgents = agentsData?.agents || []

  const handleScheduleTask = () => {
    if (!newTask.task_name || !newTask.agent_id || !selected) return

    // Calculate scheduled time (using current time of selected date + time input)
    const scheduledTime = new Date(selected)
    scheduledTime.setHours(9, 0, 0, 0) // Default to 9 AM

    const task: AgentTask = {
      id: Math.random().toString(36).substr(2, 9),
      agent_id: newTask.agent_id!,
      agent_name: availableAgents.find(a => a.id === newTask.agent_id)?.name || 'Unknown Agent',
      agent_type: availableAgents.find(a => a.id === newTask.agent_id)?.type || 'unknown',
      task_name: newTask.task_name!,
      description: newTask.description || '',
      scheduled_time: scheduledTime,
      estimated_duration: newTask.estimated_duration || 30,
      priority: newTask.priority || 'medium',
      status: 'scheduled',
      tenant_id: tenantId || 'default',
      recurring: newTask.recurring || false,
      recurrence_pattern: newTask.recurrence_pattern,
      dependencies: [],
      parameters: {},
      max_retries: newTask.max_retries || 3,
      retry_count: 0
    }

    setTasks([...tasks, task])
    setNewTask({
      task_name: '',
      description: '',
      estimated_duration: 30,
      priority: 'medium',
      recurring: false,
      max_retries: 3
    })
    setIsScheduling(false)
  }

  const getStatusColor = (status: string) => {
    const colors = {
      scheduled: 'bg-blue-500',
      running: 'bg-yellow-500',
      completed: 'bg-green-500',
      failed: 'bg-red-500',
      cancelled: 'bg-gray-500'
    }
    return colors[status as keyof typeof colors] || 'bg-gray-500'
  }

  const getPriorityColor = (priority: string) => {
    const colors = {
      low: 'border-l-green-500',
      medium: 'border-l-yellow-500',
      high: 'border-l-orange-500',
      critical: 'border-l-red-500'
    }
    return colors[priority as keyof typeof colors] || 'border-l-gray-500'
  }

  const getAgentTypeIcon = (type: string) => {
    const icons = {
      marketing: '📈',
      seo: '🔍',
      content: '✍️',
      analytics: '📊',
      support: '🎧',
      ecommerce: '🛒'
    }
    return icons[type as keyof typeof icons] || '🤖'
  }

  // Get days with tasks for calendar highlighting
  const taskDays = filteredTasks.map(task => task.scheduled_time)

  return (
    <div className={`space-y-6 ${className}`}>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-5 w-5" />
            AI Agent Scheduler
          </CardTitle>
          <CardDescription>
            Schedule and manage AI agent tasks, workflows, and automation
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Calendar */}
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold">
                  {format(selected || new Date(), 'MMMM yyyy')}
                </h3>
                <Dialog open={isScheduling} onOpenChange={setIsScheduling}>
                  <DialogTrigger asChild>
                    <Button size="sm" className="gap-2" disabled={isLoading}>
                      <Timer className="h-4 w-4" />
                      Schedule Task
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-2xl">
                    <DialogHeader>
                      <DialogTitle>Schedule AI Agent Task</DialogTitle>
                      <DialogDescription>
                        Create a new automated task for {selected && format(selected, 'PPP')}
                      </DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4 max-h-[60vh] overflow-y-auto">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="grid gap-2">
                          <Label htmlFor="agent">AI Agent</Label>
                          <Select
                            value={newTask.agent_id}
                            onValueChange={(value) => setNewTask({ ...newTask, agent_id: value })}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Select agent..." />
                            </SelectTrigger>
                            <SelectContent>
                              {availableAgents.map((agent) => (
                                <SelectItem key={agent.id} value={agent.id}>
                                  <div className="flex items-center gap-2">
                                    <span>{getAgentTypeIcon(agent.type)}</span>
                                    <span>{agent.name}</span>
                                    <Badge variant="secondary" className="ml-auto">
                                      {agent.type}
                                    </Badge>
                                  </div>
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="grid gap-2">
                          <Label htmlFor="priority">Priority</Label>
                          <Select
                            value={newTask.priority}
                            onValueChange={(value) => setNewTask({ ...newTask, priority: value as any })}
                          >
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="low">Low</SelectItem>
                              <SelectItem value="medium">Medium</SelectItem>
                              <SelectItem value="high">High</SelectItem>
                              <SelectItem value="critical">Critical</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                      
                      <div className="grid gap-2">
                        <Label htmlFor="task_name">Task Name</Label>
                        <Input
                          id="task_name"
                          value={newTask.task_name}
                          onChange={(e) => setNewTask({ ...newTask, task_name: e.target.value })}
                          placeholder="Enter task name..."
                        />
                      </div>
                      
                      <div className="grid gap-2">
                        <Label htmlFor="description">Description</Label>
                        <Textarea
                          id="description"
                          value={newTask.description}
                          onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                          placeholder="Describe what this agent should do..."
                          rows={3}
                        />
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4">
                        <div className="grid gap-2">
                          <Label htmlFor="duration">Duration (minutes)</Label>
                          <Input
                            id="duration"
                            type="number"
                            value={newTask.estimated_duration}
                            onChange={(e) => setNewTask({ ...newTask, estimated_duration: parseInt(e.target.value) })}
                            min="5"
                            max="480"
                          />
                        </div>
                        <div className="grid gap-2">
                          <Label htmlFor="retries">Max Retries</Label>
                          <Input
                            id="retries"
                            type="number"
                            value={newTask.max_retries}
                            onChange={(e) => setNewTask({ ...newTask, max_retries: parseInt(e.target.value) })}
                            min="0"
                            max="10"
                          />
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <Switch
                          id="recurring"
                          checked={newTask.recurring}
                          onCheckedChange={(checked) => setNewTask({ ...newTask, recurring: checked })}
                        />
                        <Label htmlFor="recurring">Recurring Task</Label>
                      </div>
                      
                      {newTask.recurring && (
                        <div className="grid gap-2">
                          <Label>Recurrence Pattern</Label>
                          <Select
                            value={newTask.recurrence_pattern}
                            onValueChange={(value) => setNewTask({ ...newTask, recurrence_pattern: value })}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Select pattern..." />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="hourly">Every Hour</SelectItem>
                              <SelectItem value="daily">Daily</SelectItem>
                              <SelectItem value="weekly">Weekly</SelectItem>
                              <SelectItem value="monthly">Monthly</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      )}
                    </div>
                    <DialogFooter>
                      <Button type="submit" onClick={handleScheduleTask}>
                        Schedule Task
                      </Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              </div>
              
              <DayPicker
                mode="single"
                selected={selected}
                onSelect={setSelected}
                className="rounded-md border"
                modifiers={{
                  hasTask: taskDays,
                  today: new Date()
                }}
                modifiersClassNames={{
                  hasTask: 'bg-primary/20 font-bold',
                  today: 'bg-accent'
                }}
              />
            </div>

            {/* Tasks for Selected Date */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">
                Tasks for {selected ? format(selected, 'PPP') : 'Select a date'}
              </h3>
              
              {selectedDateTasks.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <Bot className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>No AI agent tasks scheduled for this date</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {selectedDateTasks
                    .sort((a, b) => a.scheduled_time.getTime() - b.scheduled_time.getTime())
                    .map((task) => (
                      <Card
                        key={task.id}
                        className={`cursor-pointer hover:shadow-md transition-shadow border-l-4 ${getPriorityColor(task.priority)}`}
                        onClick={() => setSelectedTask(task)}
                      >
                        <CardContent className="p-4">
                          <div className="flex justify-between items-start mb-2">
                            <div className="flex items-center gap-2">
                              <span className="text-lg">{getAgentTypeIcon(task.agent_type)}</span>
                              <Badge className={`${getStatusColor(task.status)} text-white`}>
                                {task.status}
                              </Badge>
                              <Badge variant="outline">
                                {task.priority.toUpperCase()}
                              </Badge>
                              {task.recurring && (
                                <Badge variant="secondary">
                                  🔄 {task.recurrence_pattern}
                                </Badge>
                              )}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              {format(task.scheduled_time, 'HH:mm')}
                            </div>
                          </div>
                          
                          <h4 className="font-semibold text-sm">{task.task_name}</h4>
                          <p className="text-xs text-muted-foreground mb-2">{task.agent_name}</p>
                          
                          {task.description && (
                            <p className="text-xs text-muted-foreground mb-2">
                              {task.description}
                            </p>
                          )}
                          
                          <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                            <div className="flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              {task.estimated_duration}m
                            </div>
                            {task.dependencies.length > 0 && (
                              <div className="flex items-center gap-1">
                                <AlertCircle className="h-3 w-3" />
                                {task.dependencies.length} deps
                              </div>
                            )}
                            {task.retry_count > 0 && (
                              <div className="flex items-center gap-1 text-orange-600">
                                <Zap className="h-3 w-3" />
                                Retry {task.retry_count}/{task.max_retries}
                              </div>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                </div>
              )}
            </div>
          </div>

          {/* Summary Stats */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mt-6 pt-6 border-t">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{filteredTasks.length}</div>
              <div className="text-xs text-muted-foreground">Total Tasks</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {filteredTasks.filter(t => t.status === 'scheduled').length}
              </div>
              <div className="text-xs text-muted-foreground">Scheduled</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">
                {filteredTasks.filter(t => t.status === 'running').length}
              </div>
              <div className="text-xs text-muted-foreground">Running</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {filteredTasks.filter(t => t.status === 'completed').length}
              </div>
              <div className="text-xs text-muted-foreground">Completed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {filteredTasks.filter(t => t.recurring).length}
              </div>
              <div className="text-xs text-muted-foreground">Recurring</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Task Details Dialog */}
      {selectedTask && (
        <Dialog open={!!selectedTask} onOpenChange={() => setSelectedTask(null)}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                <span>{getAgentTypeIcon(selectedTask.agent_type)}</span>
                {selectedTask.task_name}
              </DialogTitle>
              <DialogDescription>
                {selectedTask.agent_name} • {format(selectedTask.scheduled_time, 'PPP p')}
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium mb-1">Status</h4>
                  <Badge className={`${getStatusColor(selectedTask.status)} text-white`}>
                    {selectedTask.status}
                  </Badge>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Priority</h4>
                  <Badge variant="outline">{selectedTask.priority.toUpperCase()}</Badge>
                </div>
              </div>
              
              {selectedTask.description && (
                <div>
                  <h4 className="font-medium mb-1">Description</h4>
                  <p className="text-sm text-muted-foreground">{selectedTask.description}</p>
                </div>
              )}
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium mb-1">Duration</h4>
                  <p className="text-sm">{selectedTask.estimated_duration} minutes</p>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Retries</h4>
                  <p className="text-sm">{selectedTask.retry_count}/{selectedTask.max_retries}</p>
                </div>
              </div>
              
              {selectedTask.recurring && (
                <div>
                  <h4 className="font-medium mb-1">Recurrence</h4>
                  <Badge variant="secondary">
                    🔄 {selectedTask.recurrence_pattern}
                  </Badge>
                </div>
              )}
              
              {selectedTask.dependencies.length > 0 && (
                <div>
                  <h4 className="font-medium mb-1">Dependencies</h4>
                  <div className="flex flex-wrap gap-1">
                    {selectedTask.dependencies.map((depId) => (
                      <Badge key={depId} variant="outline" className="text-xs">
                        Task {depId}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setSelectedTask(null)}>
                Close
              </Button>
              <Button>
                <Settings className="h-4 w-4 mr-2" />
                Edit Task
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      )}
    </div>
  )
}