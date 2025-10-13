'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { 
  Bot, 
  Target, 
  FileText, 
  BarChart3, 
  Users, 
  Megaphone,
  Search,
  Mail,
  Palette,
  Globe,
  TrendingUp,
  Shield,
  Play,
  Pause,
  Settings,
  AlertCircle
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface AIAgentStatusProps {
  onAgentClick?: (agentId: string) => void
}

interface AIAgent {
  id: string
  name: string
  status: 'active' | 'idle' | 'error' | 'processing'
  icon: React.ElementType
  description: string
  progress: number
  lastActive: string
  tasksCompleted: number
  efficiency: number
  category: 'strategy' | 'content' | 'analytics' | 'automation'
}

const mockAgents: AIAgent[] = [
  {
    id: '1',
    name: 'Campaign Strategy',
    status: 'active',
    icon: Target,
    description: 'Optimizing ad targeting for Q4 campaigns',
    progress: 78,
    lastActive: '2 min ago',
    tasksCompleted: 23,
    efficiency: 94,
    category: 'strategy'
  },
  {
    id: '2',
    name: 'Content Studio',
    status: 'processing',
    icon: FileText,
    description: 'Generating blog content for client portfolio',
    progress: 45,
    lastActive: 'Now',
    tasksCompleted: 12,
    efficiency: 89,
    category: 'content'
  },
  {
    id: '3',
    name: 'SEO Optimizer',
    status: 'active',
    icon: Search,
    description: 'Analyzing competitor keywords',
    progress: 92,
    lastActive: '1 min ago',
    tasksCompleted: 34,
    efficiency: 96,
    category: 'strategy'
  },
  {
    id: '4',
    name: 'Analytics Engine',
    status: 'idle',
    icon: BarChart3,
    description: 'Waiting for new data batch',
    progress: 0,
    lastActive: '15 min ago',
    tasksCompleted: 8,
    efficiency: 91,
    category: 'analytics'
  },
  {
    id: '5',
    name: 'Social Media',
    status: 'error',
    icon: Megaphone,
    description: 'API connection issue - reconnecting',
    progress: 0,
    lastActive: '5 min ago',
    tasksCompleted: 0,
    efficiency: 0,
    category: 'automation'
  },
  {
    id: '6',
    name: 'Lead Scoring',
    status: 'active',
    icon: Users,
    description: 'Processing new lead batch (247 leads)',
    progress: 67,
    lastActive: 'Now',
    tasksCompleted: 15,
    efficiency: 93,
    category: 'analytics'
  }
]

const getStatusColor = (status: AIAgent['status']) => {
  switch (status) {
    case 'active': return 'text-green-600 bg-green-50'
    case 'processing': return 'text-blue-600 bg-blue-50'
    case 'idle': return 'text-yellow-600 bg-yellow-50'
    case 'error': return 'text-red-600 bg-red-50'
    default: return 'text-gray-600 bg-gray-50'
  }
}

const getStatusIcon = (status: AIAgent['status']) => {
  switch (status) {
    case 'active': return <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
    case 'processing': return <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
    case 'idle': return <div className="w-2 h-2 bg-yellow-500 rounded-full" />
    case 'error': return <AlertCircle className="w-3 h-3 text-red-500" />
    default: return <div className="w-2 h-2 bg-gray-500 rounded-full" />
  }
}

export function AIAgentStatus({ onAgentClick }: AIAgentStatusProps = {}) {
  const [agents, setAgents] = useState<AIAgent[]>(mockAgents)
  const [selectedCategory, setSelectedCategory] = useState<string>('all')

  useEffect(() => {
    // Simulate real-time updates
    const interval = setInterval(() => {
      setAgents(prev => prev.map(agent => {
        // Simulate progress updates for active/processing agents
        if (agent.status === 'active' || agent.status === 'processing') {
          const newProgress = Math.min(100, agent.progress + Math.random() * 5)
          return {
            ...agent,
            progress: newProgress,
            tasksCompleted: newProgress === 100 ? agent.tasksCompleted + 1 : agent.tasksCompleted
          }
        }
        return agent
      }))
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  const filteredAgents = selectedCategory === 'all' 
    ? agents 
    : agents.filter(agent => agent.category === selectedCategory)

  const activeAgents = agents.filter(agent => agent.status === 'active').length
  const totalTasks = agents.reduce((sum, agent) => sum + agent.tasksCompleted, 0)
  const avgEfficiency = Math.round(agents.reduce((sum, agent) => sum + agent.efficiency, 0) / agents.length)

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center space-x-2">
              <Bot className="h-5 w-5 text-primary" />
              <span>AI Agents</span>
            </CardTitle>
            <div className="flex items-center space-x-4 mt-2 text-sm text-muted-foreground">
              <span>{activeAgents}/12 Active</span>
              <span>{totalTasks} Tasks Today</span>
              <span>{avgEfficiency}% Efficiency</span>
            </div>
          </div>
          <Button variant="ghost" size="icon">
            <Settings className="h-4 w-4" />
          </Button>
        </div>
        
        {/* Category Filter */}
        <div className="flex items-center space-x-2 mt-4">
          {['all', 'strategy', 'content', 'analytics', 'automation'].map((category) => (
            <Button
              key={category}
              variant={selectedCategory === category ? 'secondary' : 'ghost'}
              size="sm"
              onClick={() => setSelectedCategory(category)}
              className="capitalize"
            >
              {category}
            </Button>
          ))}
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-4 max-h-[400px] overflow-y-auto">
          {filteredAgents.map((agent) => {
            const Icon = agent.icon
            
            return (
              <div 
                key={agent.id} 
                className="flex items-center justify-between p-3 rounded-lg border bg-card hover:bg-accent/50 transition-colors cursor-pointer"
                onClick={() => onAgentClick?.(agent.id)}
              >
                <div className="flex items-center space-x-3 flex-1">
                  <div className={cn('p-2 rounded-lg', getStatusColor(agent.status))}>
                    <Icon className="h-4 w-4" />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center space-x-2">
                        <h4 className="font-medium text-sm truncate">{agent.name}</h4>
                        {getStatusIcon(agent.status)}
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge variant="outline" className="text-xs">
                          {agent.status}
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {agent.efficiency}%
                        </span>
                      </div>
                    </div>
                    
                    <p className="text-xs text-muted-foreground truncate mb-2">
                      {agent.description}
                    </p>
                    
                    {(agent.status === 'active' || agent.status === 'processing') && (
                      <div className="flex items-center space-x-2">
                        <Progress value={agent.progress} className="flex-1 h-1.5" />
                        <span className="text-xs text-muted-foreground min-w-[30px]">
                          {Math.round(agent.progress)}%
                        </span>
                      </div>
                    )}
                    
                    <div className="flex items-center justify-between mt-1">
                      <span className="text-xs text-muted-foreground">
                        {agent.tasksCompleted} tasks completed
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {agent.lastActive}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-1 ml-2">
                  {agent.status === 'error' ? (
                    <Button variant="ghost" size="icon" className="h-6 w-6">
                      <Play className="h-3 w-3" />
                    </Button>
                  ) : agent.status === 'active' ? (
                    <Button variant="ghost" size="icon" className="h-6 w-6">
                      <Pause className="h-3 w-3" />
                    </Button>
                  ) : (
                    <Button variant="ghost" size="icon" className="h-6 w-6">
                      <Play className="h-3 w-3" />
                    </Button>
                  )}
                </div>
              </div>
            )
          })}
        </div>
        
        {filteredAgents.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">
            <Bot className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>No agents found in this category</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}