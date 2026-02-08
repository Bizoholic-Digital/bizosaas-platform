'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Label } from "@/components/ui/label";
import {
  Calendar,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle,
  Play,
  Pause,
  Square,
  MoreVertical,
  Plus,
  Filter,
  Search,
  Bot,
  Target,
  Users,
  Activity,
  Zap,
  ArrowRight,
  Edit,
  Trash2,
  RefreshCw,
  Eye,
  BarChart3,
  Timer,
  FileText,
  Tag,
  Flag,
  MessageSquare,
  History
} from 'lucide-react';

// Task interface definitions
interface TaskTemplate {
  id: string;
  name: string;
  description: string;
  category: 'lead_processing' | 'content_generation' | 'analysis' | 'monitoring' | 'optimization';
  estimatedDuration: number; // minutes
  complexity: 'low' | 'medium' | 'high';
  requiredCapabilities: string[];
  priority: 'low' | 'medium' | 'high' | 'urgent';
}

interface AgentTask {
  id: string;
  templateId?: string;
  title: string;
  description: string;
  assignedAgentId: string;
  assignedAgentName: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  category: string;

  // Timing
  createdAt: Date;
  startedAt?: Date;
  completedAt?: Date;
  dueDate?: Date;
  estimatedDuration: number; // minutes
  actualDuration?: number; // minutes

  // Progress tracking
  progress: number; // 0-100
  steps: TaskStep[];

  // Results and metadata
  result?: any;
  errorMessage?: string;
  notes?: string;
  tags: string[];

  // Dependencies
  dependencies: string[]; // Task IDs
  dependents: string[]; // Task IDs

  // Context data
  inputData?: any;
  outputData?: any;

  // Retry information
  retryCount: number;
  maxRetries: number;
}

interface TaskStep {
  id: string;
  name: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  startedAt?: Date;
  completedAt?: Date;
  duration?: number;
  result?: any;
  errorMessage?: string;
}

interface AgentWorkload {
  agentId: string;
  agentName: string;
  currentTasks: number;
  maxConcurrentTasks: number;
  completedToday: number;
  averageTaskDuration: number;
  successRate: number;
  status: 'available' | 'busy' | 'overloaded' | 'offline';
}

// Mock data
const mockTaskTemplates: TaskTemplate[] = [
  {
    id: 'template-1',
    name: 'Lead Scoring Analysis',
    description: 'Analyze and score incoming leads based on behavioral and demographic data',
    category: 'lead_processing',
    estimatedDuration: 5,
    complexity: 'medium',
    requiredCapabilities: ['lead_qualification', 'behavioral_analysis'],
    priority: 'high'
  },
  {
    id: 'template-2',
    name: 'Content SEO Optimization',
    description: 'Optimize existing content for search engines and keyword targeting',
    category: 'content_generation',
    estimatedDuration: 15,
    complexity: 'high',
    requiredCapabilities: ['seo_optimization', 'content_analysis'],
    priority: 'medium'
  },
  {
    id: 'template-3',
    name: 'Performance Monitoring Check',
    description: 'Monitor system performance and generate alerts for anomalies',
    category: 'monitoring',
    estimatedDuration: 2,
    complexity: 'low',
    requiredCapabilities: ['performance_monitoring', 'anomaly_detection'],
    priority: 'high'
  }
];

const mockAgentWorkloads: AgentWorkload[] = [
  {
    agentId: 'lead-scoring-agent',
    agentName: 'Lead Scoring Agent',
    currentTasks: 3,
    maxConcurrentTasks: 5,
    completedToday: 24,
    averageTaskDuration: 4.2,
    successRate: 96.8,
    status: 'busy'
  },
  {
    agentId: 'content-creation-agent',
    agentName: 'Content Creation Agent',
    currentTasks: 1,
    maxConcurrentTasks: 3,
    completedToday: 8,
    averageTaskDuration: 12.5,
    successRate: 93.4,
    status: 'available'
  },
  {
    agentId: 'seo-optimization-agent',
    agentName: 'SEO Optimization Agent',
    currentTasks: 2,
    maxConcurrentTasks: 4,
    completedToday: 15,
    averageTaskDuration: 8.7,
    successRate: 89.7,
    status: 'busy'
  }
];

const generateMockTasks = (): AgentTask[] => {
  const tasks: AgentTask[] = [];
  const statuses: AgentTask['status'][] = ['pending', 'in_progress', 'completed', 'failed'];
  const priorities: AgentTask['priority'][] = ['low', 'medium', 'high', 'urgent'];

  for (let i = 1; i <= 15; i++) {
    const template = mockTaskTemplates[Math.floor(Math.random() * mockTaskTemplates.length)];
    const agent = mockAgentWorkloads[Math.floor(Math.random() * mockAgentWorkloads.length)];
    const status = statuses[Math.floor(Math.random() * statuses.length)];
    const createdAt = new Date(Date.now() - Math.random() * 24 * 60 * 60 * 1000);

    tasks.push({
      id: `task-${i}`,
      templateId: template.id,
      title: `${template.name} #${i}`,
      description: template.description,
      assignedAgentId: agent.agentId,
      assignedAgentName: agent.agentName,
      status,
      priority: priorities[Math.floor(Math.random() * priorities.length)],
      category: template.category,
      createdAt,
      startedAt: status !== 'pending' ? new Date(createdAt.getTime() + Math.random() * 3600000) : undefined,
      completedAt: status === 'completed' || status === 'failed' ? new Date(Date.now() - Math.random() * 3600000) : undefined,
      dueDate: new Date(Date.now() + Math.random() * 24 * 60 * 60 * 1000),
      estimatedDuration: template.estimatedDuration,
      actualDuration: status === 'completed' ? template.estimatedDuration + (Math.random() - 0.5) * 5 : undefined,
      progress: status === 'completed' ? 100 : status === 'failed' ? 0 : Math.floor(Math.random() * 100),
      steps: [
        {
          id: 'step-1',
          name: 'Initialize',
          status: 'completed',
          startedAt: createdAt,
          completedAt: new Date(createdAt.getTime() + 30000),
          duration: 0.5
        },
        {
          id: 'step-2',
          name: 'Process Data',
          status: status === 'pending' ? 'pending' : Math.random() > 0.5 ? 'completed' : 'in_progress',
          startedAt: status !== 'pending' ? new Date(createdAt.getTime() + 30000) : undefined
        },
        {
          id: 'step-3',
          name: 'Generate Output',
          status: status === 'completed' ? 'completed' : 'pending'
        }
      ],
      result: status === 'completed' ? { success: true, data: 'Task completed successfully' } : undefined,
      errorMessage: status === 'failed' ? 'Processing failed due to invalid input data' : undefined,
      notes: Math.random() > 0.7 ? 'Additional context or requirements' : undefined,
      tags: ['automated', template.category],
      dependencies: [],
      dependents: [],
      inputData: { leadId: 12345, source: 'website' },
      outputData: status === 'completed' ? { score: Math.floor(Math.random() * 100), confidence: 0.95 } : undefined,
      retryCount: status === 'failed' ? Math.floor(Math.random() * 3) : 0,
      maxRetries: 3
    });
  }

  return tasks;
};

// Task status badge component
const TaskStatusBadge: React.FC<{ status: AgentTask['status'] }> = ({ status }) => {
  const statusConfig = {
    pending: { color: 'bg-gray-500', text: 'Pending', icon: Clock },
    in_progress: { color: 'bg-blue-500', text: 'In Progress', icon: Play },
    completed: { color: 'bg-green-500', text: 'Completed', icon: CheckCircle },
    failed: { color: 'bg-red-500', text: 'Failed', icon: XCircle },
    cancelled: { color: 'bg-orange-500', text: 'Cancelled', icon: Square }
  };

  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <Badge variant="outline" className={`${config.color} text-white border-0`}>
      <Icon className="w-3 h-3 mr-1" />
      {config.text}
    </Badge>
  );
};

// Priority badge component
const PriorityBadge: React.FC<{ priority: AgentTask['priority'] }> = ({ priority }) => {
  const priorityConfig = {
    low: { color: 'bg-gray-100 text-gray-800', text: 'Low' },
    medium: { color: 'bg-yellow-100 text-yellow-800', text: 'Medium' },
    high: { color: 'bg-orange-100 text-orange-800', text: 'High' },
    urgent: { color: 'bg-red-100 text-red-800', text: 'Urgent' }
  };

  return (
    <Badge variant="outline" className={priorityConfig[priority].color}>
      <Flag className="w-3 h-3 mr-1" />
      {priorityConfig[priority].text}
    </Badge>
  );
};

// Task card component
const TaskCard: React.FC<{
  task: AgentTask;
  onEdit: (task: AgentTask) => void;
  onView: (task: AgentTask) => void;
  onDelete: (taskId: string) => void;
}> = ({ task, onEdit, onView, onDelete }) => {
  const getTimeRemaining = () => {
    if (!task.dueDate) return null;
    const now = new Date();
    const diff = task.dueDate.getTime() - now.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

    if (diff < 0) return 'Overdue';
    if (hours < 24) return `${hours}h ${minutes}m`;
    return `${Math.floor(hours / 24)}d ${hours % 24}h`;
  };

  const isOverdue = task.dueDate && new Date() > task.dueDate && task.status !== 'completed';

  return (
    <Card className={`hover:shadow-lg transition-shadow ${isOverdue ? 'border-red-200' : ''}`}>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bot className="w-4 h-4 text-blue-600" />
            <CardTitle className="text-sm font-medium">{task.title}</CardTitle>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={() => onView(task)}>
                <Eye className="w-4 h-4 mr-2" />
                View Details
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onEdit(task)}>
                <Edit className="w-4 h-4 mr-2" />
                Edit Task
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onDelete(task.id)} className="text-red-600">
                <Trash2 className="w-4 h-4 mr-2" />
                Delete Task
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        <CardDescription className="text-xs">{task.description}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex items-center justify-between">
          <TaskStatusBadge status={task.status} />
          <PriorityBadge priority={task.priority} />
        </div>

        <div className="space-y-2">
          <div className="flex justify-between text-xs">
            <span>Progress</span>
            <span>{task.progress}%</span>
          </div>
          <Progress value={task.progress} className="h-2" />
        </div>

        <div className="grid grid-cols-2 gap-2 text-xs">
          <div>
            <p className="text-gray-500">Assigned to</p>
            <p className="font-medium truncate">{task.assignedAgentName}</p>
          </div>
          <div>
            <p className="text-gray-500">Duration</p>
            <p className="font-medium">
              {task.actualDuration ? `${task.actualDuration.toFixed(1)}m` : `~${task.estimatedDuration}m`}
            </p>
          </div>
        </div>

        {task.dueDate && (
          <div className="flex items-center justify-between text-xs">
            <span className="text-gray-500">Due in:</span>
            <span className={`font-medium ${isOverdue ? 'text-red-600' : 'text-gray-700'}`}>
              {getTimeRemaining()}
            </span>
          </div>
        )}

        <div className="flex flex-wrap gap-1">
          {task.tags.slice(0, 3).map((tag, index) => (
            <Badge key={index} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
          {task.tags.length > 3 && (
            <Badge variant="secondary" className="text-xs">
              +{task.tags.length - 3}
            </Badge>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

// Agent workload component
const AgentWorkloadCard: React.FC<{ workload: AgentWorkload }> = ({ workload }) => {
  const utilizationPercentage = (workload.currentTasks / workload.maxConcurrentTasks) * 100;

  const getStatusColor = () => {
    switch (workload.status) {
      case 'available': return 'text-green-600';
      case 'busy': return 'text-yellow-600';
      case 'overloaded': return 'text-red-600';
      case 'offline': return 'text-gray-400';
      default: return 'text-gray-600';
    }
  };

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm">{workload.agentName}</CardTitle>
          <Badge variant="outline" className={getStatusColor()}>
            {workload.status}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="space-y-2">
          <div className="flex justify-between text-xs">
            <span>Task Load</span>
            <span>{workload.currentTasks}/{workload.maxConcurrentTasks}</span>
          </div>
          <Progress value={utilizationPercentage} className="h-2" />
        </div>

        <div className="grid grid-cols-2 gap-2 text-xs">
          <div>
            <p className="text-gray-500">Completed Today</p>
            <p className="font-medium">{workload.completedToday}</p>
          </div>
          <div>
            <p className="text-gray-500">Success Rate</p>
            <p className="font-medium">{workload.successRate}%</p>
          </div>
        </div>

        <div className="text-xs">
          <p className="text-gray-500">Avg Duration</p>
          <p className="font-medium">{workload.averageTaskDuration.toFixed(1)}m</p>
        </div>
      </CardContent>
    </Card>
  );
};

// Task creation dialog
const TaskCreationDialog: React.FC<{
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onCreateTask: (task: Partial<AgentTask>) => void;
  templates: TaskTemplate[];
  agents: AgentWorkload[];
}> = ({ open, onOpenChange, onCreateTask, templates, agents }) => {
  const [selectedTemplate, setSelectedTemplate] = useState<string>('');
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    assignedAgentId: '',
    priority: 'medium' as AgentTask['priority'],
    dueDate: '',
    notes: '',
    tags: ''
  });

  const handleTemplateSelect = (templateId: string) => {
    const template = templates.find(t => t.id === templateId);
    if (template) {
      setFormData(prev => ({
        ...prev,
        title: template.name,
        description: template.description
      }));
    }
    setSelectedTemplate(templateId);
  };

  const handleSubmit = () => {
    const newTask: Partial<AgentTask> = {
      ...formData,
      templateId: selectedTemplate || undefined,
      category: selectedTemplate ? templates.find(t => t.id === selectedTemplate)?.category : 'analysis',
      status: 'pending',
      progress: 0,
      estimatedDuration: selectedTemplate ? templates.find(t => t.id === selectedTemplate)?.estimatedDuration : 10,
      tags: formData.tags.split(',').map(tag => tag.trim()).filter(Boolean),
      dueDate: formData.dueDate ? new Date(formData.dueDate) : undefined,
      createdAt: new Date(),
      steps: [],
      dependencies: [],
      dependents: [],
      retryCount: 0,
      maxRetries: 3
    };

    onCreateTask(newTask);
    onOpenChange(false);

    // Reset form
    setFormData({
      title: '',
      description: '',
      assignedAgentId: '',
      priority: 'medium',
      dueDate: '',
      notes: '',
      tags: ''
    });
    setSelectedTemplate('');
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Create New Task</DialogTitle>
          <DialogDescription>
            Create a new task and assign it to an agent
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          {/* Template Selection */}
          <div className="space-y-2">
            <Label>Task Template (Optional)</Label>
            <Select value={selectedTemplate} onValueChange={handleTemplateSelect}>
              <SelectTrigger>
                <SelectValue placeholder="Select a template or create custom task" />
              </SelectTrigger>
              <SelectContent>
                {templates.map((template) => (
                  <SelectItem key={template.id} value={template.id}>
                    {template.name} ({template.estimatedDuration}m)
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Basic Information */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="title">Task Title</Label>
              <Input
                id="title"
                value={formData.title}
                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                placeholder="Enter task title"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="assigned-agent">Assign to Agent</Label>
              <Select
                value={formData.assignedAgentId}
                onValueChange={(value) => setFormData(prev => ({ ...prev, assignedAgentId: value }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select an agent" />
                </SelectTrigger>
                <SelectContent>
                  {agents.map((agent) => (
                    <SelectItem key={agent.agentId} value={agent.agentId}>
                      {agent.agentName} ({agent.currentTasks}/{agent.maxConcurrentTasks} tasks)
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              placeholder="Describe the task requirements and expected output"
              rows={3}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="priority">Priority</Label>
              <Select
                value={formData.priority}
                onValueChange={(value) => setFormData(prev => ({ ...prev, priority: value as AgentTask['priority'] }))}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="urgent">Urgent</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="due-date">Due Date</Label>
              <Input
                id="due-date"
                type="datetime-local"
                value={formData.dueDate}
                onChange={(e) => setFormData(prev => ({ ...prev, dueDate: e.target.value }))}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="tags">Tags (comma-separated)</Label>
            <Input
              id="tags"
              value={formData.tags}
              onChange={(e) => setFormData(prev => ({ ...prev, tags: e.target.value }))}
              placeholder="urgent, customer-facing, analysis"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Additional Notes</Label>
            <Textarea
              id="notes"
              value={formData.notes}
              onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
              placeholder="Any additional context or requirements"
              rows={2}
            />
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={!formData.title || !formData.assignedAgentId}>
            Create Task
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

// Main task management interface
export default function TaskManagementInterface() {
  const [tasks, setTasks] = useState<AgentTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [agentWorkloads, setAgentWorkloads] = useState<AgentWorkload[]>(mockAgentWorkloads);
  const [selectedTask, setSelectedTask] = useState<AgentTask | null>(null);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<AgentTask['status'] | 'all'>('all');
  const [priorityFilter, setPriorityFilter] = useState<AgentTask['priority'] | 'all'>('all');
  const [assigneeFilter, setAssigneeFilter] = useState<string>('all');

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/brain/plane?type=issues');
      if (!response.ok) throw new Error('Failed to fetch tasks');
      const data = await response.json();

      // Map Plane issues to AgentTask interface
      const planeTasks: AgentTask[] = (data.results || []).map((issue: any) => ({
        id: issue.id,
        title: issue.name,
        description: issue.description_strip || issue.description_html || '',
        assignedAgentId: issue.assignees?.[0] || 'unassigned',
        assignedAgentName: issue.assignees_detail?.[0]?.display_name || 'Unassigned',
        status: mapPlaneStatus(issue.state_detail?.name || 'Backlog'),
        priority: (issue.priority || 'medium') as AgentTask['priority'],
        category: 'general',
        createdAt: new Date(issue.created_at),
        dueDate: issue.target_date ? new Date(issue.target_date) : undefined,
        estimatedDuration: issue.estimate || 0,
        progress: issue.state_detail?.group === 'completed' ? 100 : 0,
        steps: [],
        tags: issue.labels || [],
        retryCount: 0,
        maxRetries: 3,
        dependencies: [],
        dependents: []
      }));

      setTasks(planeTasks);
    } catch (err: any) {
      console.error('Error fetching tasks:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const mapPlaneStatus = (state: string): AgentTask['status'] => {
    const s = state.toLowerCase();
    if (s.includes('backlog') || s.includes('todo')) return 'pending';
    if (s.includes('progress')) return 'in_progress';
    if (s.includes('done') || s.includes('completed')) return 'completed';
    if (s.includes('fail') || s.includes('error')) return 'failed';
    if (s.includes('cancel')) return 'cancelled';
    return 'pending';
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  // Filter tasks
  const filteredTasks = tasks.filter(task => {
    if (searchTerm && !task.title.toLowerCase().includes(searchTerm.toLowerCase()) &&
      !task.description.toLowerCase().includes(searchTerm.toLowerCase())) return false;
    if (statusFilter !== 'all' && task.status !== statusFilter) return false;
    if (priorityFilter !== 'all' && task.priority !== priorityFilter) return false;
    if (assigneeFilter !== 'all' && task.assignedAgentId !== assigneeFilter) return false;
    return true;
  });

  // Group tasks by status
  const tasksByStatus = {
    pending: filteredTasks.filter(t => t.status === 'pending'),
    in_progress: filteredTasks.filter(t => t.status === 'in_progress'),
    completed: filteredTasks.filter(t => t.status === 'completed'),
    failed: filteredTasks.filter(t => t.status === 'failed')
  };

  const handleCreateTask = async (taskData: Partial<AgentTask>) => {
    try {
      const response = await fetch('/api/brain/plane', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          data: {
            name: taskData.title,
            description_html: `<p>${taskData.description}</p>`,
            priority: taskData.priority,
            assignees: taskData.assignedAgentId !== 'unassigned' ? [taskData.assignedAgentId] : []
          }
        })
      });

      if (!response.ok) throw new Error('Failed to create task');

      // Refresh list
      fetchTasks();
    } catch (err: any) {
      console.error('Error creating task:', err);
      alert('Failed to create task: ' + err.message);
    }
  };

  const handleDeleteTask = (taskId: string) => {
    setTasks(prev => prev.filter(t => t.id !== taskId));
  };

  const handleEditTask = (task: AgentTask) => {
    // This would open an edit dialog - simplified for demo
    console.log('Edit task:', task);
  };

  const handleViewTask = (task: AgentTask) => {
    setSelectedTask(task);
  };

  // Calculate statistics
  const stats = {
    total: tasks.length,
    pending: tasks.filter(t => t.status === 'pending').length,
    inProgress: tasks.filter(t => t.status === 'in_progress').length,
    completed: tasks.filter(t => t.status === 'completed').length,
    failed: tasks.filter(t => t.status === 'failed').length,
    overdue: tasks.filter(t => t.dueDate && new Date() > t.dueDate && t.status !== 'completed').length
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center">
            <Target className="w-6 h-6 mr-2" />
            Task Management Center
          </h2>
          <p className="text-gray-600">Assign, monitor, and manage AI agent tasks</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={fetchTasks} disabled={loading}>
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Create Task
          </Button>
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-xs text-gray-500">Total Tasks</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-600">{stats.pending}</p>
              <p className="text-xs text-gray-500">Pending</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{stats.inProgress}</p>
              <p className="text-xs text-gray-500">In Progress</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">{stats.completed}</p>
              <p className="text-xs text-gray-500">Completed</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-red-600">{stats.failed}</p>
              <p className="text-xs text-gray-500">Failed</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-orange-600">{stats.overdue}</p>
              <p className="text-xs text-gray-500">Overdue</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <div className="md:col-span-2">
              <Input
                placeholder="Search tasks..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <Select value={statusFilter} onValueChange={(value) => setStatusFilter(value as any)}>
              <SelectTrigger>
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="pending">Pending</SelectItem>
                <SelectItem value="in_progress">In Progress</SelectItem>
                <SelectItem value="completed">Completed</SelectItem>
                <SelectItem value="failed">Failed</SelectItem>
              </SelectContent>
            </Select>
            <Select value={priorityFilter} onValueChange={(value) => setPriorityFilter(value as any)}>
              <SelectTrigger>
                <SelectValue placeholder="Priority" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Priority</SelectItem>
                <SelectItem value="urgent">Urgent</SelectItem>
                <SelectItem value="high">High</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="low">Low</SelectItem>
              </SelectContent>
            </Select>
            <Select value={assigneeFilter} onValueChange={setAssigneeFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Assignee" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Agents</SelectItem>
                {agentWorkloads.map((agent) => (
                  <SelectItem key={agent.agentId} value={agent.agentId}>
                    {agent.agentName}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Tasks Board */}
        <div className="lg:col-span-3">
          <Tabs defaultValue="board" className="space-y-4">
            <TabsList>
              <TabsTrigger value="board">Board View</TabsTrigger>
              <TabsTrigger value="list">List View</TabsTrigger>
              <TabsTrigger value="timeline">Timeline</TabsTrigger>
            </TabsList>

            <TabsContent value="board" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {Object.entries(tasksByStatus).map(([status, statusTasks]) => (
                  <div key={status} className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h3 className="font-medium capitalize">{status.replace('_', ' ')}</h3>
                      <Badge variant="secondary">{statusTasks.length}</Badge>
                    </div>
                    <div className="space-y-3 max-h-96 overflow-y-auto">
                      {statusTasks.map((task) => (
                        <TaskCard
                          key={task.id}
                          task={task}
                          onEdit={handleEditTask}
                          onView={handleViewTask}
                          onDelete={handleDeleteTask}
                        />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="list" className="space-y-4">
              <div className="space-y-2">
                {filteredTasks.map((task) => (
                  <Card key={task.id} className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <TaskStatusBadge status={task.status} />
                        <div>
                          <h4 className="font-medium">{task.title}</h4>
                          <p className="text-sm text-gray-500">{task.assignedAgentName}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <PriorityBadge priority={task.priority} />
                        <Progress value={task.progress} className="w-20 h-2" />
                        <span className="text-sm text-gray-500">{task.progress}%</span>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="timeline">
              <div className="space-y-4">
                <p className="text-gray-500">Timeline view coming soon...</p>
              </div>
            </TabsContent>
          </Tabs>
        </div>

        {/* Agent Workloads Sidebar */}
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center">
                <Users className="w-5 h-5 mr-2" />
                Agent Workloads
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {agentWorkloads.map((workload) => (
                <AgentWorkloadCard key={workload.agentId} workload={workload} />
              ))}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Create Task Dialog */}
      <TaskCreationDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
        onCreateTask={handleCreateTask}
        templates={mockTaskTemplates}
        agents={agentWorkloads}
      />
    </div>
  );
}