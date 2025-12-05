'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  AlertCircle, 
  TrendingUp, 
  Clock, 
  CheckCircle, 
  XCircle, 
  Pause,
  Zap,
  BarChart3,
  Settings,
  Target,
  DollarSign,
  Users,
  Shield,
  Cpu,
  Workflow,
  Bot,
  Play,
  RefreshCw,
  Filter,
  ArrowUp,
  ArrowDown,
  Star,
  MessageCircle,
  FileText,
  Calendar,
  Activity
} from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import { useToast } from '@/components/ui/use-toast'

// Types and interfaces
interface OptimizationSuggestion {
  id: string
  title: string
  description: string
  optimization_type: 'performance' | 'user_experience' | 'automation' | 'cost_reduction' | 'security' | 'scalability' | 'integration' | 'workflow_efficiency'
  priority: 'critical' | 'high' | 'medium' | 'low'
  estimated_impact: number
  estimated_effort: string
  implementation_complexity: string
  affected_systems: string[]
  prerequisites: string[]
  success_metrics: Record<string, any>
  ai_confidence: number
  data_sources: string[]
  recommendation_reason: string
  implementation_steps: string[]
  risks: string[]
  benefits: string[]
  status: 'suggested' | 'approved' | 'in_progress' | 'completed' | 'rejected' | 'on_hold'
  created_at: string
  tenant_id: string
  roi_estimate: Record<string, any>
}

interface OptimizationMetrics {
  tenant_id: string
  optimization_summary: {
    total_suggestions: number
    implemented: number
    in_progress: number
    pending_approval: number
  }
  performance_improvements: {
    api_response_time_reduction: string
    database_query_optimization: string
    user_engagement_increase: string
    error_rate_reduction: string
  }
  cost_savings: {
    monthly_infrastructure_savings: string
    annual_projected_savings: string
    roi_percentage: string
  }
  automation_achievements: {
    processes_automated: number
    time_saved_per_week: string
    manual_error_reduction: string
  }
  user_satisfaction: {
    nps_improvement: string
    support_ticket_reduction: string
    feature_adoption_increase: string
  }
}

interface OptimizationTrends {
  tenant_id: string
  period: string
  trends: {
    suggestions_generated: {
      this_period: number
      previous_period: number
      change_percentage: string
    }
    implementation_rate: {
      this_period: number
      previous_period: number
      change_percentage: string
    }
    average_impact_score: {
      this_period: number
      previous_period: number
      change_percentage: string
    }
    time_to_implementation: {
      this_period: string
      previous_period: string
      change_percentage: string
    }
  }
  category_breakdown: Record<string, number>
  success_patterns: string[]
}

const OPTIMIZATION_TYPE_ICONS = {
  performance: Cpu,
  user_experience: Users,
  automation: Bot,
  cost_reduction: DollarSign,
  security: Shield,
  scalability: TrendingUp,
  integration: Workflow,
  workflow_efficiency: Activity
}

const OPTIMIZATION_TYPE_COLORS = {
  performance: 'bg-blue-500',
  user_experience: 'bg-green-500',
  automation: 'bg-purple-500',
  cost_reduction: 'bg-yellow-500',
  security: 'bg-red-500',
  scalability: 'bg-indigo-500',
  integration: 'bg-pink-500',
  workflow_efficiency: 'bg-orange-500'
}

const PRIORITY_COLORS = {
  critical: 'bg-red-100 text-red-800 border-red-200',
  high: 'bg-orange-100 text-orange-800 border-orange-200',
  medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  low: 'bg-blue-100 text-blue-800 border-blue-200'
}

const STATUS_COLORS = {
  suggested: 'bg-gray-100 text-gray-800',
  approved: 'bg-blue-100 text-blue-800',
  in_progress: 'bg-yellow-100 text-yellow-800',
  completed: 'bg-green-100 text-green-800',
  rejected: 'bg-red-100 text-red-800',
  on_hold: 'bg-purple-100 text-purple-800'
}

export default function WorkflowOptimizerPage() {
  // State management
  const [suggestions, setSuggestions] = useState<OptimizationSuggestion[]>([])
  const [metrics, setMetrics] = useState<OptimizationMetrics | null>(null)
  const [trends, setTrends] = useState<OptimizationTrends | null>(null)
  const [loading, setLoading] = useState(false)
  const [generateLoading, setGenerateLoading] = useState(false)
  const [selectedSuggestion, setSelectedSuggestion] = useState<OptimizationSuggestion | null>(null)
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [filterType, setFilterType] = useState<string>('all')
  const [sortBy, setSortBy] = useState<string>('priority')
  const [activeTab, setActiveTab] = useState('suggestions')
  const [feedbackDialog, setFeedbackDialog] = useState(false)
  const [implementDialog, setImplementDialog] = useState(false)
  
  // Form states
  const [feedback, setFeedback] = useState({
    type: '',
    text: '',
    rating: 5
  })
  const [implementationPlan, setImplementationPlan] = useState('')
  const [assignedTeam, setAssignedTeam] = useState('')

  const { toast } = useToast()

  // API calls
  const fetchSuggestions = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/brain/workflow-optimizer/suggestions/demo${filterStatus !== 'all' ? `?status=${filterStatus}` : ''}`)
      if (response.ok) {
        const data = await response.json()
        setSuggestions(data.suggestions || [])
      }
    } catch (error) {
      console.error('Error fetching suggestions:', error)
      toast({
        title: "Error",
        description: "Failed to fetch optimization suggestions",
        variant: "destructive"
      })
    } finally {
      setLoading(false)
    }
  }

  const fetchMetrics = async () => {
    try {
      const response = await fetch('/api/brain/workflow-optimizer/metrics/optimization-impact?tenant_id=demo')
      if (response.ok) {
        const data = await response.json()
        setMetrics(data.metrics)
      }
    } catch (error) {
      console.error('Error fetching metrics:', error)
    }
  }

  const fetchTrends = async () => {
    try {
      const response = await fetch('/api/brain/workflow-optimizer/analytics/trends?tenant_id=demo&period=30d')
      if (response.ok) {
        const data = await response.json()
        setTrends(data.analytics)
      }
    } catch (error) {
      console.error('Error fetching trends:', error)
    }
  }

  const generateOptimizations = async () => {
    try {
      setGenerateLoading(true)
      const response = await fetch('/api/brain/workflow-optimizer/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tenant_id: 'demo' })
      })
      
      if (response.ok) {
        const data = await response.json()
        toast({
          title: "Success",
          description: `Generated ${data.suggestions_generated} new optimization suggestions`,
        })
        fetchSuggestions()
        fetchMetrics()
      }
    } catch (error) {
      console.error('Error generating optimizations:', error)
      toast({
        title: "Error",
        description: "Failed to generate optimization suggestions",
        variant: "destructive"
      })
    } finally {
      setGenerateLoading(false)
    }
  }

  const updateSuggestionStatus = async (suggestionId: string, newStatus: string) => {
    try {
      const response = await fetch(`/api/brain/workflow-optimizer/suggestions/${suggestionId}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      })
      
      if (response.ok) {
        toast({
          title: "Success",
          description: `Suggestion status updated to ${newStatus}`,
        })
        fetchSuggestions()
        fetchMetrics()
      }
    } catch (error) {
      console.error('Error updating status:', error)
      toast({
        title: "Error",
        description: "Failed to update suggestion status",
        variant: "destructive"
      })
    }
  }

  const submitFeedback = async () => {
    if (!selectedSuggestion || !feedback.type) return

    try {
      const response = await fetch('/api/brain/workflow-optimizer/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          suggestion_id: selectedSuggestion.id,
          type: feedback.type,
          feedback: feedback.text,
          rating: feedback.rating
        })
      })
      
      if (response.ok) {
        toast({
          title: "Success",
          description: "Feedback submitted successfully",
        })
        setFeedbackDialog(false)
        setFeedback({ type: '', text: '', rating: 5 })
      }
    } catch (error) {
      console.error('Error submitting feedback:', error)
      toast({
        title: "Error",
        description: "Failed to submit feedback",
        variant: "destructive"
      })
    }
  }

  const implementSuggestion = async () => {
    if (!selectedSuggestion) return

    try {
      const response = await fetch(`/api/brain/workflow-optimizer/suggestions/${selectedSuggestion.id}/implement`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          implementation_plan: implementationPlan,
          assigned_team: assignedTeam
        })
      })
      
      if (response.ok) {
        toast({
          title: "Success",
          description: "Implementation started successfully",
        })
        setImplementDialog(false)
        setImplementationPlan('')
        setAssignedTeam('')
        fetchSuggestions()
        fetchMetrics()
      }
    } catch (error) {
      console.error('Error implementing suggestion:', error)
      toast({
        title: "Error",
        description: "Failed to start implementation",
        variant: "destructive"
      })
    }
  }

  // Filter and sort suggestions
  const filteredAndSortedSuggestions = suggestions
    .filter(s => filterType === 'all' || s.optimization_type === filterType)
    .sort((a, b) => {
      switch (sortBy) {
        case 'priority':
          const priorityOrder = { critical: 4, high: 3, medium: 2, low: 1 }
          return priorityOrder[b.priority] - priorityOrder[a.priority]
        case 'impact':
          return b.estimated_impact - a.estimated_impact
        case 'confidence':
          return b.ai_confidence - a.ai_confidence
        case 'created':
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        default:
          return 0
      }
    })

  useEffect(() => {
    fetchSuggestions()
    fetchMetrics()
    fetchTrends()
  }, [filterStatus])

  const renderMetricsCards = () => {
    if (!metrics) return null

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Suggestions</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.optimization_summary.total_suggestions}</div>
            <div className="text-xs text-muted-foreground">
              {metrics.optimization_summary.implemented} implemented
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Performance Gains</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.performance_improvements.api_response_time_reduction}</div>
            <div className="text-xs text-muted-foreground">
              API response time reduction
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Cost Savings</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.cost_savings.monthly_infrastructure_savings}</div>
            <div className="text-xs text-muted-foreground">
              Monthly infrastructure savings
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Time Saved</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.automation_achievements.time_saved_per_week}</div>
            <div className="text-xs text-muted-foreground">
              Weekly time savings
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const renderSuggestionCard = (suggestion: OptimizationSuggestion) => {
    const TypeIcon = OPTIMIZATION_TYPE_ICONS[suggestion.optimization_type]
    
    return (
      <Card key={suggestion.id} className="hover:shadow-md transition-shadow">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-lg ${OPTIMIZATION_TYPE_COLORS[suggestion.optimization_type]} text-white`}>
                <TypeIcon className="h-4 w-4" />
              </div>
              <div>
                <CardTitle className="text-lg">{suggestion.title}</CardTitle>
                <p className="text-sm text-muted-foreground">{suggestion.optimization_type.replace('_', ' ')}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge className={PRIORITY_COLORS[suggestion.priority]}>
                {suggestion.priority}
              </Badge>
              <Badge className={STATUS_COLORS[suggestion.status]}>
                {suggestion.status.replace('_', ' ')}
              </Badge>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-sm mb-4">{suggestion.description}</p>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div>
              <p className="text-xs font-medium text-muted-foreground">Impact</p>
              <div className="flex items-center gap-2">
                <Progress value={suggestion.estimated_impact} className="h-2" />
                <span className="text-sm font-medium">{suggestion.estimated_impact}%</span>
              </div>
            </div>
            <div>
              <p className="text-xs font-medium text-muted-foreground">AI Confidence</p>
              <div className="flex items-center gap-2">
                <Progress value={suggestion.ai_confidence * 100} className="h-2" />
                <span className="text-sm font-medium">{Math.round(suggestion.ai_confidence * 100)}%</span>
              </div>
            </div>
            <div>
              <p className="text-xs font-medium text-muted-foreground">Effort</p>
              <p className="text-sm">{suggestion.estimated_effort}</p>
            </div>
            <div>
              <p className="text-xs font-medium text-muted-foreground">Complexity</p>
              <p className="text-sm capitalize">{suggestion.implementation_complexity}</p>
            </div>
          </div>

          <div className="mb-4">
            <p className="text-xs font-medium text-muted-foreground mb-2">Affected Systems</p>
            <div className="flex flex-wrap gap-1">
              {suggestion.affected_systems.map((system, index) => (
                <Badge key={index} variant="outline" className="text-xs">{system}</Badge>
              ))}
            </div>
          </div>

          <div className="mb-4">
            <p className="text-xs font-medium text-muted-foreground mb-2">Benefits</p>
            <ul className="list-disc list-inside text-sm space-y-1">
              {suggestion.benefits.slice(0, 3).map((benefit, index) => (
                <li key={index}>{benefit}</li>
              ))}
            </ul>
          </div>

          <div className="flex gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={() => {
                setSelectedSuggestion(suggestion)
                setFeedbackDialog(true)
              }}
            >
              <MessageCircle className="h-4 w-4 mr-1" />
              Feedback
            </Button>
            
            {suggestion.status === 'suggested' && (
              <>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => updateSuggestionStatus(suggestion.id, 'approved')}
                >
                  <CheckCircle className="h-4 w-4 mr-1" />
                  Approve
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => {
                    setSelectedSuggestion(suggestion)
                    setImplementDialog(true)
                  }}
                >
                  <Play className="h-4 w-4 mr-1" />
                  Implement
                </Button>
              </>
            )}
            
            {suggestion.status === 'approved' && (
              <Button
                size="sm"
                variant="outline"
                onClick={() => {
                  setSelectedSuggestion(suggestion)
                  setImplementDialog(true)
                }}
              >
                <Play className="h-4 w-4 mr-1" />
                Start Implementation
              </Button>
            )}
            
            {suggestion.status === 'in_progress' && (
              <Button
                size="sm"
                variant="outline"
                onClick={() => updateSuggestionStatus(suggestion.id, 'completed')}
              >
                <CheckCircle className="h-4 w-4 mr-1" />
                Mark Complete
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    )
  }

  const renderTrendsChart = () => {
    if (!trends) return null

    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Optimization Trends</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(trends.trends).map(([key, data]) => (
                <div key={key} className="flex items-center justify-between">
                  <div>
                    <p className="font-medium capitalize">{key.replace('_', ' ')}</p>
                    <p className="text-sm text-muted-foreground">
                      {typeof data.this_period === 'number' ? data.this_period : data.this_period}
                    </p>
                  </div>
                  <div className={`flex items-center gap-1 ${
                    data.change_percentage.startsWith('+') ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {data.change_percentage.startsWith('+') ? 
                      <ArrowUp className="h-4 w-4" /> : 
                      <ArrowDown className="h-4 w-4" />
                    }
                    <span className="font-medium">{data.change_percentage}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Category Breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {Object.entries(trends.category_breakdown).map(([category, count]) => (
                <div key={category} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className={`w-3 h-3 rounded ${OPTIMIZATION_TYPE_COLORS[category as keyof typeof OPTIMIZATION_TYPE_COLORS]}`} />
                    <span className="capitalize">{category.replace('_', ' ')}</span>
                  </div>
                  <Badge variant="outline">{count}</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold">Workflow Optimizer</h1>
          <p className="text-muted-foreground">AI-powered optimization suggestions and continuous improvement</p>
        </div>
        <Button onClick={generateOptimizations} disabled={generateLoading}>
          {generateLoading ? (
            <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
          ) : (
            <Zap className="h-4 w-4 mr-2" />
          )}
          Generate Optimizations
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="suggestions">Suggestions</TabsTrigger>
          <TabsTrigger value="metrics">Impact Metrics</TabsTrigger>
          <TabsTrigger value="trends">Trends & Analytics</TabsTrigger>
          <TabsTrigger value="health">System Health</TabsTrigger>
        </TabsList>

        <TabsContent value="suggestions" className="space-y-6">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4" />
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="w-40">
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="suggested">Suggested</SelectItem>
                  <SelectItem value="approved">Approved</SelectItem>
                  <SelectItem value="in_progress">In Progress</SelectItem>
                  <SelectItem value="completed">Completed</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <Select value={filterType} onValueChange={setFilterType}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Filter by type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="performance">Performance</SelectItem>
                <SelectItem value="user_experience">User Experience</SelectItem>
                <SelectItem value="automation">Automation</SelectItem>
                <SelectItem value="cost_reduction">Cost Reduction</SelectItem>
                <SelectItem value="security">Security</SelectItem>
                <SelectItem value="scalability">Scalability</SelectItem>
              </SelectContent>
            </Select>
            
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="priority">Priority</SelectItem>
                <SelectItem value="impact">Impact Score</SelectItem>
                <SelectItem value="confidence">AI Confidence</SelectItem>
                <SelectItem value="created">Date Created</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {loading ? (
              <div className="col-span-2 text-center py-8">
                <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-2" />
                <p>Loading optimization suggestions...</p>
              </div>
            ) : filteredAndSortedSuggestions.length === 0 ? (
              <div className="col-span-2 text-center py-8">
                <Bot className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-lg font-medium mb-2">No optimization suggestions found</p>
                <p className="text-muted-foreground mb-4">Generate new suggestions to get AI-powered recommendations</p>
                <Button onClick={generateOptimizations}>
                  <Zap className="h-4 w-4 mr-2" />
                  Generate First Suggestions
                </Button>
              </div>
            ) : (
              filteredAndSortedSuggestions.map(renderSuggestionCard)
            )}
          </div>
        </TabsContent>

        <TabsContent value="metrics" className="space-y-6">
          {renderMetricsCards()}
          
          {metrics && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Performance Improvements</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {Object.entries(metrics.performance_improvements).map(([key, value]) => (
                      <div key={key} className="flex items-center justify-between">
                        <span className="capitalize">{key.replace('_', ' ')}</span>
                        <Badge variant="outline" className="text-green-600">
                          {value}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>ROI & Cost Savings</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {Object.entries(metrics.cost_savings).map(([key, value]) => (
                      <div key={key} className="flex items-center justify-between">
                        <span className="capitalize">{key.replace('_', ' ')}</span>
                        <Badge variant="outline" className="text-green-600">
                          {value}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>

        <TabsContent value="trends" className="space-y-6">
          {renderTrendsChart()}
          
          {trends && (
            <Card>
              <CardHeader>
                <CardTitle>Success Patterns</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {trends.success_patterns.map((pattern, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <Star className="h-4 w-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">{pattern}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="health" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>System Health Status</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span>Optimization Engine</span>
                    <Badge className="bg-green-100 text-green-800">Active</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>ML Model Accuracy</span>
                    <Badge variant="outline">94.2%</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Prediction Confidence</span>
                    <Badge variant="outline">High</Badge>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span>Suggestion Relevance</span>
                    <Badge variant="outline">89%</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Implementation Success Rate</span>
                    <Badge variant="outline">76%</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>User Satisfaction Score</span>
                    <Badge variant="outline">4.3/5</Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Feedback Dialog */}
      <Dialog open={feedbackDialog} onOpenChange={setFeedbackDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Submit Feedback</DialogTitle>
            <DialogDescription>
              Help us improve optimization suggestions by providing your feedback
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="feedback-type">Feedback Type</Label>
              <Select value={feedback.type} onValueChange={(value) => setFeedback(prev => ({ ...prev, type: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Select feedback type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="helpful">Helpful</SelectItem>
                  <SelectItem value="not_helpful">Not Helpful</SelectItem>
                  <SelectItem value="implemented">Implemented Successfully</SelectItem>
                  <SelectItem value="needs_revision">Needs Revision</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="feedback-rating">Rating (1-5)</Label>
              <Input
                id="feedback-rating"
                type="number"
                min="1"
                max="5"
                value={feedback.rating}
                onChange={(e) => setFeedback(prev => ({ ...prev, rating: parseInt(e.target.value) }))}
              />
            </div>
            <div>
              <Label htmlFor="feedback-text">Additional Comments</Label>
              <Textarea
                id="feedback-text"
                value={feedback.text}
                onChange={(e) => setFeedback(prev => ({ ...prev, text: e.target.value }))}
                placeholder="Provide additional feedback..."
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setFeedbackDialog(false)}>
              Cancel
            </Button>
            <Button onClick={submitFeedback} disabled={!feedback.type}>
              Submit Feedback
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Implementation Dialog */}
      <Dialog open={implementDialog} onOpenChange={setImplementDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Start Implementation</DialogTitle>
            <DialogDescription>
              Configure implementation details for this optimization suggestion
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="assigned-team">Assigned Team</Label>
              <Input
                id="assigned-team"
                value={assignedTeam}
                onChange={(e) => setAssignedTeam(e.target.value)}
                placeholder="Enter team name..."
              />
            </div>
            <div>
              <Label htmlFor="implementation-plan">Implementation Plan</Label>
              <Textarea
                id="implementation-plan"
                value={implementationPlan}
                onChange={(e) => setImplementationPlan(e.target.value)}
                placeholder="Describe the implementation approach..."
                rows={4}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setImplementDialog(false)}>
              Cancel
            </Button>
            <Button onClick={implementSuggestion}>
              Start Implementation
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}