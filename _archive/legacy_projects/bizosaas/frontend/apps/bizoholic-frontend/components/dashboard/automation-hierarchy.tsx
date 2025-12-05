'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Settings,
  Zap,
  Brain,
  Workflow,
  AlertTriangle,
  CheckCircle,
  TrendingUp,
  Clock,
  DollarSign,
  Target,
  ArrowRight,
  Info
} from 'lucide-react'
import { cn } from '@/lib/utils'
import AutomationDecisionEngine, { 
  AutomationType, 
  TaskComplexity, 
  COMMON_AUTOMATION_TASKS,
  type AutomationTask,
  type AutomationRecommendation 
} from '@/lib/automation-hierarchy'

interface AutomationMetrics {
  logic_workflows: {
    active: number
    total: number
    success_rate: number
    avg_execution_time: number
  }
  ai_agents: {
    active: number
    total: number
    success_rate: number
    avg_execution_time: number
  }
  cost_efficiency: {
    logic_cost_per_task: number
    ai_cost_per_task: number
    savings_percentage: number
  }
  performance_comparison: {
    logic_accuracy: number
    ai_accuracy: number
    logic_speed: number
    ai_speed: number
  }
}

const mockMetrics: AutomationMetrics = {
  logic_workflows: {
    active: 47,
    total: 52,
    success_rate: 96.8,
    avg_execution_time: 2.3
  },
  ai_agents: {
    active: 8,
    total: 15,
    success_rate: 87.2,
    avg_execution_time: 8.7
  },
  cost_efficiency: {
    logic_cost_per_task: 0.02,
    ai_cost_per_task: 0.15,
    savings_percentage: 86.7
  },
  performance_comparison: {
    logic_accuracy: 94.5,
    ai_accuracy: 89.2,
    logic_speed: 92.1,
    ai_speed: 71.8
  }
}

export function AutomationHierarchy() {
  const [metrics, setMetrics] = useState<AutomationMetrics>(mockMetrics)
  const [selectedTask, setSelectedTask] = useState<string | null>(null)
  const [recommendations, setRecommendations] = useState<Record<string, AutomationRecommendation>>({})

  useEffect(() => {
    // Generate recommendations for all common tasks
    const recs: Record<string, AutomationRecommendation> = {}
    Object.entries(COMMON_AUTOMATION_TASKS).forEach(([key, task]) => {
      recs[key] = AutomationDecisionEngine.analyzeTask(task)
    })
    setRecommendations(recs)
  }, [])

  const getAutomationTypeColor = (type: AutomationType) => {
    switch (type) {
      case AutomationType.RULE_BASED:
      case AutomationType.WORKFLOW_LOGIC:
      case AutomationType.DATABASE_TRIGGERS:
      case AutomationType.API_INTEGRATIONS:
      case AutomationType.SCHEDULED_TASKS:
        return 'bg-green-100 text-green-800'
      case AutomationType.LOGIC_WITH_AI_VALIDATION:
      case AutomationType.AI_ENHANCED_WORKFLOWS:
        return 'bg-yellow-100 text-yellow-800'
      case AutomationType.AI_AGENT:
      case AutomationType.AI_DECISION_MAKING:
      case AutomationType.AI_CONTENT_GENERATION:
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getComplexityColor = (complexity: TaskComplexity) => {
    switch (complexity) {
      case TaskComplexity.SIMPLE: return 'bg-green-100 text-green-800'
      case TaskComplexity.MODERATE: return 'bg-yellow-100 text-yellow-800'
      case TaskComplexity.COMPLEX: return 'bg-orange-100 text-orange-800'
      case TaskComplexity.CREATIVE: return 'bg-purple-100 text-purple-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getAutomationIcon = (type: AutomationType) => {
    if ([AutomationType.RULE_BASED, AutomationType.WORKFLOW_LOGIC].includes(type)) {
      return <Workflow className="h-4 w-4" />
    }
    if ([AutomationType.AI_AGENT, AutomationType.AI_DECISION_MAKING].includes(type)) {
      return <Brain className="h-4 w-4" />
    }
    return <Zap className="h-4 w-4" />
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Logic-First Automation Hierarchy</h2>
        <p className="text-muted-foreground">
          Intelligent automation that prioritizes deterministic workflows over AI agents, 
          ensuring reliability, cost-efficiency, and predictable outcomes.
        </p>
      </div>

      {/* Performance Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Logic Workflows</p>
                <p className="text-2xl font-bold">{metrics.logic_workflows.active}</p>
                <p className="text-xs text-green-600">
                  {metrics.logic_workflows.success_rate}% success rate
                </p>
              </div>
              <Workflow className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">AI Agents</p>
                <p className="text-2xl font-bold">{metrics.ai_agents.active}</p>
                <p className="text-xs text-blue-600">
                  {metrics.ai_agents.success_rate}% success rate
                </p>
              </div>
              <Brain className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Cost Savings</p>
                <p className="text-2xl font-bold">{metrics.cost_efficiency.savings_percentage}%</p>
                <p className="text-xs text-green-600">
                  vs AI-first approach
                </p>
              </div>
              <DollarSign className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Avg Speed</p>
                <p className="text-2xl font-bold">{metrics.logic_workflows.avg_execution_time}s</p>
                <p className="text-xs text-green-600">
                  {((metrics.ai_agents.avg_execution_time - metrics.logic_workflows.avg_execution_time) / metrics.ai_agents.avg_execution_time * 100).toFixed(1)}% faster
                </p>
              </div>
              <Clock className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Analysis */}
      <Tabs defaultValue="hierarchy" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="hierarchy">Automation Hierarchy</TabsTrigger>
          <TabsTrigger value="tasks">Task Analysis</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
        </TabsList>

        <TabsContent value="hierarchy" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Automation Type Priority</CardTitle>
              <CardDescription>
                Tasks are automatically assigned to the most appropriate automation type based on complexity and requirements
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Logic-First Priority Levels */}
                <div className="border rounded-lg p-4 bg-green-50">
                  <div className="flex items-center space-x-2 mb-3">
                    <Workflow className="h-5 w-5 text-green-600" />
                    <h4 className="font-semibold text-green-900">Priority 1: Logic-Based Automation</h4>
                    <Badge className="bg-green-100 text-green-800">Highest Priority</Badge>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                    <div>
                      <p className="font-medium">Rule-Based Workflows</p>
                      <p className="text-muted-foreground">Simple conditional logic</p>
                    </div>
                    <div>
                      <p className="font-medium">Database Triggers</p>
                      <p className="text-muted-foreground">Event-driven processing</p>
                    </div>
                    <div>
                      <p className="font-medium">API Integrations</p>
                      <p className="text-muted-foreground">System synchronization</p>
                    </div>
                  </div>
                  <div className="mt-3 flex items-center space-x-4 text-xs text-green-700">
                    <span>✓ 99% Reliability</span>
                    <span>✓ Low Cost</span>
                    <span>✓ Fast Execution</span>
                    <span>✓ Predictable</span>
                  </div>
                </div>

                <div className="border rounded-lg p-4 bg-yellow-50">
                  <div className="flex items-center space-x-2 mb-3">
                    <Zap className="h-5 w-5 text-yellow-600" />
                    <h4 className="font-semibold text-yellow-900">Priority 2: Hybrid Automation</h4>
                    <Badge className="bg-yellow-100 text-yellow-800">Medium Priority</Badge>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                    <div>
                      <p className="font-medium">Logic with AI Validation</p>
                      <p className="text-muted-foreground">Rule-based with AI quality checks</p>
                    </div>
                    <div>
                      <p className="font-medium">AI-Enhanced Workflows</p>
                      <p className="text-muted-foreground">Structured processes with AI insights</p>
                    </div>
                  </div>
                  <div className="mt-3 flex items-center space-x-4 text-xs text-yellow-700">
                    <span>✓ 90% Reliability</span>
                    <span>✓ Moderate Cost</span>
                    <span>✓ Good Performance</span>
                    <span>✓ Balanced Approach</span>
                  </div>
                </div>

                <div className="border rounded-lg p-4 bg-blue-50">
                  <div className="flex items-center space-x-2 mb-3">
                    <Brain className="h-5 w-5 text-blue-600" />
                    <h4 className="font-semibold text-blue-900">Priority 3: AI-Based Automation</h4>
                    <Badge className="bg-blue-100 text-blue-800">Use When Necessary</Badge>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                    <div>
                      <p className="font-medium">AI Agents</p>
                      <p className="text-muted-foreground">Complex decision making</p>
                    </div>
                    <div>
                      <p className="font-medium">Content Generation</p>
                      <p className="text-muted-foreground">Creative and analytical tasks</p>
                    </div>
                    <div>
                      <p className="font-medium">Pattern Recognition</p>
                      <p className="text-muted-foreground">Unstructured data analysis</p>
                    </div>
                  </div>
                  <div className="mt-3 flex items-center space-x-4 text-xs text-blue-700">
                    <span>⚠ 85% Reliability</span>
                    <span>⚠ Higher Cost</span>
                    <span>⚠ Variable Speed</span>
                    <span>✓ Handles Complexity</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="tasks" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Common Task Analysis</CardTitle>
              <CardDescription>
                Analysis of common automation tasks and recommended approaches
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(COMMON_AUTOMATION_TASKS).map(([key, task]) => {
                  const recommendation = recommendations[key]
                  if (!recommendation) return null

                  return (
                    <div 
                      key={key} 
                      className="border rounded-lg p-4 cursor-pointer hover:bg-accent/50 transition-colors"
                      onClick={() => setSelectedTask(selectedTask === key ? null : key)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          {getAutomationIcon(recommendation.recommended_type)}
                          <div>
                            <h4 className="font-semibold">{task.name}</h4>
                            <p className="text-sm text-muted-foreground">{task.description}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge className={getComplexityColor(task.complexity)}>
                            {task.complexity}
                          </Badge>
                          <Badge className={getAutomationTypeColor(recommendation.recommended_type)}>
                            {recommendation.recommended_type.replace('_', ' ')}
                          </Badge>
                          <span className="text-sm text-muted-foreground">
                            {Math.round(recommendation.confidence * 100)}% confidence
                          </span>
                        </div>
                      </div>

                      {selectedTask === key && (
                        <div className="mt-4 pt-4 border-t space-y-3">
                          <div>
                            <p className="text-sm font-medium mb-1">Reasoning:</p>
                            <p className="text-sm text-muted-foreground">{recommendation.reasoning}</p>
                          </div>
                          
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                              <p className="text-sm font-medium mb-2">Primary Implementation:</p>
                              <div className="bg-green-50 border border-green-200 rounded p-3">
                                <div className="flex items-center justify-between mb-2">
                                  <span className="text-sm font-medium">{recommendation.implementation_options.primary.type.replace('_', ' ')}</span>
                                  <Badge variant="outline">Primary</Badge>
                                </div>
                                <div className="space-y-1 text-xs">
                                  <div className="flex justify-between">
                                    <span>Accuracy:</span>
                                    <span>{recommendation.implementation_options.primary.estimated_accuracy}%</span>
                                  </div>
                                  <div className="flex justify-between">
                                    <span>Speed:</span>
                                    <span>{recommendation.implementation_options.primary.estimated_speed}%</span>
                                  </div>
                                  <div className="flex justify-between">
                                    <span>Cost Efficiency:</span>
                                    <span>{recommendation.implementation_options.primary.cost_efficiency}%</span>
                                  </div>
                                </div>
                              </div>
                            </div>

                            {recommendation.implementation_options.fallback && (
                              <div>
                                <p className="text-sm font-medium mb-2">Fallback Option:</p>
                                <div className="bg-yellow-50 border border-yellow-200 rounded p-3">
                                  <div className="flex items-center justify-between mb-2">
                                    <span className="text-sm font-medium">{recommendation.implementation_options.fallback.type.replace('_', ' ')}</span>
                                    <Badge variant="outline">Fallback</Badge>
                                  </div>
                                  <div className="space-y-1 text-xs">
                                    <div className="flex justify-between">
                                      <span>Accuracy:</span>
                                      <span>{recommendation.implementation_options.fallback.estimated_accuracy}%</span>
                                    </div>
                                    <div className="flex justify-between">
                                      <span>Speed:</span>
                                      <span>{recommendation.implementation_options.fallback.estimated_speed}%</span>
                                    </div>
                                    <div className="flex justify-between">
                                      <span>Cost Efficiency:</span>
                                      <span>{recommendation.implementation_options.fallback.cost_efficiency}%</span>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            )}
                          </div>

                          <div className="flex space-x-4">
                            <div className="flex-1">
                              <p className="text-sm font-medium mb-1">Available Logic Workflows:</p>
                              <div className="flex flex-wrap gap-1">
                                {recommendation.logic_workflows.slice(0, 3).map((workflow, index) => (
                                  <Badge key={index} variant="secondary" className="text-xs">
                                    {workflow.replace('_', ' ')}
                                  </Badge>
                                ))}
                                {recommendation.logic_workflows.length > 3 && (
                                  <Badge variant="outline" className="text-xs">
                                    +{recommendation.logic_workflows.length - 3} more
                                  </Badge>
                                )}
                              </div>
                            </div>
                            
                            <div className="flex-1">
                              <p className="text-sm font-medium mb-1">AI Alternatives:</p>
                              <div className="flex flex-wrap gap-1">
                                {recommendation.ai_alternatives.slice(0, 2).map((agent, index) => (
                                  <Badge key={index} variant="outline" className="text-xs">
                                    {agent.replace('_', ' ')}
                                  </Badge>
                                ))}
                                {recommendation.ai_alternatives.length > 2 && (
                                  <Badge variant="outline" className="text-xs">
                                    +{recommendation.ai_alternatives.length - 2} more
                                  </Badge>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="performance" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Performance Comparison</CardTitle>
                <CardDescription>Logic workflows vs AI agents</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Logic Accuracy</span>
                    <span>{metrics.performance_comparison.logic_accuracy}%</span>
                  </div>
                  <Progress value={metrics.performance_comparison.logic_accuracy} className="h-2" />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>AI Accuracy</span>
                    <span>{metrics.performance_comparison.ai_accuracy}%</span>
                  </div>
                  <Progress value={metrics.performance_comparison.ai_accuracy} className="h-2" />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Logic Speed</span>
                    <span>{metrics.performance_comparison.logic_speed}%</span>
                  </div>
                  <Progress value={metrics.performance_comparison.logic_speed} className="h-2" />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>AI Speed</span>
                    <span>{metrics.performance_comparison.ai_speed}%</span>
                  </div>
                  <Progress value={metrics.performance_comparison.ai_speed} className="h-2" />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Cost Analysis</CardTitle>
                <CardDescription>Resource usage and cost efficiency</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm">Logic Cost per Task</span>
                  <span className="font-mono text-green-600">${metrics.cost_efficiency.logic_cost_per_task}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">AI Cost per Task</span>
                  <span className="font-mono text-blue-600">${metrics.cost_efficiency.ai_cost_per_task}</span>
                </div>
                <div className="border-t pt-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Total Savings</span>
                    <span className="font-mono text-lg font-bold text-green-600">
                      {metrics.cost_efficiency.savings_percentage}%
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">
                    By prioritizing logic-first automation
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="recommendations" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Optimization Recommendations</CardTitle>
              <CardDescription>
                Suggestions to improve your automation hierarchy
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-start space-x-3 p-4 bg-green-50 border border-green-200 rounded-lg">
                  <CheckCircle className="h-5 w-5 text-green-600 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-green-900">Excellent Logic Coverage</h4>
                    <p className="text-sm text-green-700">
                      90% of your automation tasks are using logic-first approaches. This is optimal for cost and reliability.
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-3 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-yellow-900">Opportunity: Content Tasks</h4>
                    <p className="text-sm text-yellow-700">
                      Consider using template-based logic for routine content generation before falling back to AI.
                    </p>
                    <Button variant="outline" size="sm" className="mt-2">
                      Implement Templates
                    </Button>
                  </div>
                </div>

                <div className="flex items-start space-x-3 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <Info className="h-5 w-5 text-blue-600 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-blue-900">Monitor AI Usage</h4>
                    <p className="text-sm text-blue-700">
                      8 AI agents are currently active. Review if any can be replaced with logic workflows.
                    </p>
                    <Button variant="outline" size="sm" className="mt-2">
                      Review AI Usage
                    </Button>
                  </div>
                </div>

                <div className="flex items-start space-x-3 p-4 bg-purple-50 border border-purple-200 rounded-lg">
                  <TrendingUp className="h-5 w-5 text-purple-600 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-purple-900">Performance Trend</h4>
                    <p className="text-sm text-purple-700">
                      Logic workflow success rate has improved 5% this month. Consider expanding logic coverage.
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}