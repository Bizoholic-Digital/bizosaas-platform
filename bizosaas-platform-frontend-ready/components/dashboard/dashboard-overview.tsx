'use client'

import { useState, useEffect } from 'react'
import { TrendingUp, TrendingDown, DollarSign, Users, Target, Zap, ArrowUpRight, ArrowDownRight } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'

interface MetricData {
  title: string
  value: string
  change: number
  changeType: 'increase' | 'decrease'
  icon: React.ElementType
  description: string
}

export function DashboardOverview() {
  const [metrics, setMetrics] = useState<MetricData[]>([])
  const [loading, setLoading] = useState(true)

  // Simulate real-time data updates
  useEffect(() => {
    const fetchMetrics = async () => {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const mockMetrics: MetricData[] = [
        {
          title: 'Total Revenue',
          value: '$45,231',
          change: 12.5,
          changeType: 'increase',
          icon: DollarSign,
          description: 'Revenue generated this month'
        },
        {
          title: 'Active Campaigns',
          value: '24',
          change: 8.2,
          changeType: 'increase',
          icon: Target,
          description: 'Campaigns currently running'
        },
        {
          title: 'Total Leads',
          value: '1,247',
          change: -3.1,
          changeType: 'decrease',
          icon: Users,
          description: 'Leads generated this month'
        },
        {
          title: 'AI Automations',
          value: '156',
          change: 23.7,
          changeType: 'increase',
          icon: Zap,
          description: 'Automated tasks completed today'
        }
      ]
      
      setMetrics(mockMetrics)
      setLoading(false)
    }

    fetchMetrics()
    
    // Update metrics every 30 seconds for real-time feel
    const interval = setInterval(() => {
      setMetrics(prev => prev.map(metric => ({
        ...metric,
        change: metric.change + (Math.random() - 0.5) * 2 // Small random fluctuation
      })))
    }, 30000)

    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Card key={i}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <Skeleton className="h-4 w-[100px]" />
              <Skeleton className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-6 w-[120px]" />
              <Skeleton className="h-3 w-[80px] mt-2" />
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {metrics.map((metric, index) => {
        const Icon = metric.icon
        const TrendIcon = metric.changeType === 'increase' ? ArrowUpRight : ArrowDownRight
        const trendColor = metric.changeType === 'increase' ? 'text-green-600' : 'text-red-600'
        const bgColor = metric.changeType === 'increase' ? 'bg-green-50' : 'bg-red-50'
        
        return (
          <Card key={index} className="relative overflow-hidden hover:shadow-md transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {metric.title}
              </CardTitle>
              <div className={`p-2 rounded-lg ${bgColor}`}>
                <Icon className={`h-4 w-4 ${trendColor}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex items-baseline space-x-3">
                <div className="text-2xl font-bold">{metric.value}</div>
                <div className={`flex items-center text-xs ${trendColor}`}>
                  <TrendIcon className="h-3 w-3 mr-1" />
                  {Math.abs(metric.change).toFixed(1)}%
                </div>
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                {metric.description}
              </p>
              
              {/* Real-time indicator */}
              <div className="absolute top-2 right-2">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                  <Badge variant="secondary" className="text-xs px-1.5 py-0.5">
                    Live
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}