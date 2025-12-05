'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { 
  Bot, 
  Target, 
  Users, 
  BarChart3, 
  FileText, 
  CheckCircle,
  AlertCircle,
  Clock,
  TrendingUp,
  Zap
} from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'

interface Activity {
  id: string
  type: 'campaign' | 'lead' | 'report' | 'ai' | 'system'
  title: string
  description: string
  timestamp: Date
  status: 'success' | 'warning' | 'info' | 'error'
  user?: {
    name: string
    avatar?: string
  }
  metadata?: {
    campaign?: string
    value?: number
    client?: string
  }
}

const mockActivities: Activity[] = [
  {
    id: '1',
    type: 'ai',
    title: 'Campaign optimization completed',
    description: 'AI agent improved CTR by 23% for Google Ads campaign',
    timestamp: new Date(Date.now() - 2 * 60 * 1000),
    status: 'success',
    metadata: { campaign: 'Q4 Holiday Sale', value: 23 }
  },
  {
    id: '2', 
    type: 'lead',
    title: 'New qualified lead',
    description: 'High-value lead captured from LinkedIn campaign',
    timestamp: new Date(Date.now() - 5 * 60 * 1000),
    status: 'success',
    user: { name: 'Sarah Johnson', avatar: '/avatars/sarah.png' },
    metadata: { client: 'TechCorp', value: 2500 }
  },
  {
    id: '3',
    type: 'campaign',
    title: 'Campaign launched',
    description: 'Meta Ads campaign for winter collection went live',
    timestamp: new Date(Date.now() - 15 * 60 * 1000),
    status: 'info',
    user: { name: 'Mike Chen', avatar: '/avatars/mike.png' },
    metadata: { campaign: 'Winter Collection 2024' }
  },
  {
    id: '4',
    type: 'report',
    title: 'Weekly report generated',
    description: 'Automated performance report for all active campaigns',
    timestamp: new Date(Date.now() - 30 * 60 * 1000),
    status: 'info',
    metadata: { value: 12 }
  },
  {
    id: '5',
    type: 'system',
    title: 'Integration connected',
    description: 'HubSpot CRM successfully linked to BizoSaaS',
    timestamp: new Date(Date.now() - 45 * 60 * 1000),
    status: 'success',
    user: { name: 'Alex Rivera', avatar: '/avatars/alex.png' }
  },
  {
    id: '6',
    type: 'ai',
    title: 'Content generation ready',
    description: '5 blog posts generated and ready for review',
    timestamp: new Date(Date.now() - 60 * 60 * 1000),
    status: 'info',
    metadata: { value: 5 }
  },
  {
    id: '7',
    type: 'campaign',
    title: 'Budget alert',
    description: 'Google Ads campaign approaching 80% budget usage',
    timestamp: new Date(Date.now() - 90 * 60 * 1000),
    status: 'warning',
    metadata: { campaign: 'Black Friday Sale', value: 80 }
  }
]

const getActivityIcon = (type: Activity['type']) => {
  switch (type) {
    case 'campaign': return Target
    case 'lead': return Users
    case 'report': return BarChart3
    case 'ai': return Bot
    case 'system': return Zap
    default: return FileText
  }
}

const getStatusColor = (status: Activity['status']) => {
  switch (status) {
    case 'success': return 'text-green-600 bg-green-50'
    case 'warning': return 'text-yellow-600 bg-yellow-50'
    case 'error': return 'text-red-600 bg-red-50'
    default: return 'text-blue-600 bg-blue-50'
  }
}

const getStatusIcon = (status: Activity['status']) => {
  switch (status) {
    case 'success': return CheckCircle
    case 'warning': return AlertCircle
    case 'error': return AlertCircle
    default: return Clock
  }
}

export function RecentActivity() {
  const [activities, setActivities] = useState<Activity[]>(mockActivities)
  const [showAll, setShowAll] = useState(false)

  // Simulate real-time activity updates
  useEffect(() => {
    const interval = setInterval(() => {
      // Randomly add new activity
      if (Math.random() > 0.7) {
        const newActivity: Activity = {
          id: Date.now().toString(),
          type: ['ai', 'lead', 'campaign'][Math.floor(Math.random() * 3)] as Activity['type'],
          title: 'New AI optimization completed',
          description: 'Campaign performance improved automatically',
          timestamp: new Date(),
          status: 'success'
        }
        
        setActivities(prev => [newActivity, ...prev.slice(0, 19)]) // Keep only 20 activities
      }
    }, 30000) // Check every 30 seconds

    return () => clearInterval(interval)
  }, [])

  const displayedActivities = showAll ? activities : activities.slice(0, 6)

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Clock className="h-5 w-5 text-muted-foreground" />
            <span>Recent Activity</span>
          </CardTitle>
          <Badge variant="outline">
            Live
            <div className="w-2 h-2 bg-green-500 rounded-full ml-2 animate-pulse" />
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-4">
          {displayedActivities.map((activity) => {
            const ActivityIcon = getActivityIcon(activity.type)
            const StatusIcon = getStatusIcon(activity.status)
            const statusColor = getStatusColor(activity.status)
            
            return (
              <div key={activity.id} className="flex items-start space-x-3 p-3 rounded-lg hover:bg-accent/50 transition-colors">
                <div className={`p-2 rounded-lg ${statusColor}`}>
                  <ActivityIcon className="h-4 w-4" />
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <p className="font-medium text-sm truncate">{activity.title}</p>
                    <div className="flex items-center space-x-1">
                      <StatusIcon className="h-3 w-3" />
                      <span className="text-xs text-muted-foreground">
                        {formatDistanceToNow(activity.timestamp, { addSuffix: true })}
                      </span>
                    </div>
                  </div>
                  
                  <p className="text-sm text-muted-foreground mb-2">{activity.description}</p>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      {activity.user && (
                        <>
                          <Avatar className="h-5 w-5">
                            <AvatarImage src={activity.user.avatar} />
                            <AvatarFallback className="text-xs">
                              {activity.user.name.split(' ').map(n => n[0]).join('')}
                            </AvatarFallback>
                          </Avatar>
                          <span className="text-xs text-muted-foreground">{activity.user.name}</span>
                        </>
                      )}
                      
                      {activity.metadata?.campaign && (
                        <Badge variant="secondary" className="text-xs">
                          {activity.metadata.campaign}
                        </Badge>
                      )}
                      
                      {activity.metadata?.client && (
                        <Badge variant="outline" className="text-xs">
                          {activity.metadata.client}
                        </Badge>
                      )}
                    </div>
                    
                    {activity.metadata?.value && (
                      <div className="flex items-center space-x-1">
                        {activity.type === 'lead' && (
                          <span className="text-xs font-medium text-green-600">
                            +${activity.metadata.value.toLocaleString()}
                          </span>
                        )}
                        {activity.type === 'ai' && activity.title.includes('optimization') && (
                          <span className="text-xs font-medium text-blue-600">
                            +{activity.metadata.value}%
                          </span>
                        )}
                        {activity.type === 'campaign' && activity.title.includes('budget') && (
                          <span className="text-xs font-medium text-yellow-600">
                            {activity.metadata.value}%
                          </span>
                        )}
                        {activity.type === 'report' && (
                          <span className="text-xs font-medium text-purple-600">
                            {activity.metadata.value} reports
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
        
        {activities.length > 6 && (
          <div className="mt-4 text-center">
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={() => setShowAll(!showAll)}
            >
              {showAll ? 'Show Less' : `View All (${activities.length})`}
            </Button>
          </div>
        )}
        
        {activities.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">
            <Clock className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>No recent activity</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}