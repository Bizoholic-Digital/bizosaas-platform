"use client"

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Progress } from '@/components/ui/progress'
import { Separator } from '@/components/ui/separator'
import {
  BarChart3, TrendingUp, Clock, MessageCircle, CheckCircle, AlertTriangle,
  Users, Target, Activity, Zap, RefreshCw, Calendar, Filter
} from 'lucide-react'
import { ConversationInsights, ConversationAnalyticsManager } from '@/lib/conversation-analytics'

interface AnalyticsDashboardProps {
  analyticsManager: ConversationAnalyticsManager
  className?: string
}

export function AnalyticsDashboard({ analyticsManager, className = "" }: AnalyticsDashboardProps) {
  const [insights, setInsights] = useState<ConversationInsights | null>(null)
  const [timeframe, setTimeframe] = useState<'day' | 'week' | 'month' | 'all'>('week')
  const [isLoading, setIsLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<string | null>(null)

  // Load insights data
  const loadInsights = async () => {
    setIsLoading(true)
    try {
      const data = await analyticsManager.getConversationInsights(timeframe)
      setInsights(data)
      setLastUpdated(new Date().toLocaleTimeString())
    } catch (error) {
      console.error('Failed to load analytics insights:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadInsights()
  }, [timeframe])

  // Auto-refresh every 5 minutes
  useEffect(() => {
    const interval = setInterval(loadInsights, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [timeframe])

  const getPerformanceColor = (value: number, thresholds: { good: number; warning: number }) => {
    if (value >= thresholds.good) return 'text-green-600'
    if (value >= thresholds.warning) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getEngagementLevel = (retentionRate: number) => {
    if (retentionRate >= 80) return { level: 'Excellent', color: 'bg-green-500' }
    if (retentionRate >= 60) return { level: 'Good', color: 'bg-blue-500' }
    if (retentionRate >= 40) return { level: 'Average', color: 'bg-yellow-500' }
    return { level: 'Poor', color: 'bg-red-500' }
  }

  if (isLoading && !insights) {
    return (
      <div className={`space-y-6 ${className}`}>
        <div className="flex items-center justify-center py-12">
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 border-2 border-current border-t-transparent rounded-full animate-spin" />
            <span>Loading analytics...</span>
          </div>
        </div>
      </div>
    )
  }

  if (!insights) {
    return (
      <div className={`space-y-6 ${className}`}>
        <Card>
          <CardContent className="flex items-center justify-center py-12">
            <div className="text-center space-y-2">
              <AlertTriangle className="w-12 h-12 text-muted-foreground mx-auto" />
              <h3 className="font-semibold">No Data Available</h3>
              <p className="text-muted-foreground">Analytics data will appear after conversations are tracked.</p>
              <Button onClick={loadInsights} variant="outline">
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const engagement = getEngagementLevel(insights.userEngagement.retentionRate)

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Conversation Analytics</h2>
          <p className="text-muted-foreground">
            Performance insights and user engagement metrics
            {lastUpdated && <span className="ml-2">• Updated {lastUpdated}</span>}
          </p>
        </div>
        
        <div className="flex items-center space-x-2">
          <Select value={timeframe} onValueChange={(value: typeof timeframe) => setTimeframe(value)}>
            <SelectTrigger className="w-32">
              <Calendar className="w-4 h-4 mr-2" />
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="day">Today</SelectItem>
              <SelectItem value="week">This Week</SelectItem>
              <SelectItem value="month">This Month</SelectItem>
              <SelectItem value="all">All Time</SelectItem>
            </SelectContent>
          </Select>
          
          <Button onClick={loadInsights} variant="outline" size="sm" disabled={isLoading}>
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center space-x-2">
              <MessageCircle className="w-4 h-4" />
              <span>Total Conversations</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{insights.totalConversations.toLocaleString()}</div>
            <div className="text-xs text-muted-foreground">
              Avg {insights.averageMessageCount.toFixed(1)} messages per conversation
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center space-x-2">
              <Clock className="w-4 h-4" />
              <span>Avg Duration</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round(insights.averageDuration / 60000)}m
            </div>
            <div className="text-xs text-muted-foreground">
              Response time: {insights.performanceMetrics.averageResponseTime}ms
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center space-x-2">
              <Target className="w-4 h-4" />
              <span>Success Rate</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${getPerformanceColor(insights.performanceMetrics.completionRate, { good: 80, warning: 60 })}`}>
              {insights.performanceMetrics.completionRate.toFixed(1)}%
            </div>
            <div className="text-xs text-muted-foreground">
              Error rate: {insights.performanceMetrics.errorRate.toFixed(1)}%
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center space-x-2">
              <TrendingUp className="w-4 h-4" />
              <span>User Satisfaction</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${getPerformanceColor(insights.averageSatisfactionScore, { good: 4, warning: 3 })}`}>
              {insights.averageSatisfactionScore.toFixed(1)}/5
            </div>
            <div className="flex items-center space-x-1 text-xs">
              {[1, 2, 3, 4, 5].map((star) => (
                <div
                  key={star}
                  className={`w-2 h-2 rounded-full ${
                    star <= Math.round(insights.averageSatisfactionScore) ? 'bg-yellow-500' : 'bg-gray-300'
                  }`}
                />
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* User Engagement */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Users className="w-5 h-5" />
            <span>User Engagement</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Daily Active Users</span>
                <span className="text-lg font-semibold">{insights.userEngagement.dailyActiveUsers}</span>
              </div>
              <Progress value={(insights.userEngagement.dailyActiveUsers / insights.userEngagement.monthlyActiveUsers) * 100} className="h-2" />
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Weekly Active Users</span>
                <span className="text-lg font-semibold">{insights.userEngagement.weeklyActiveUsers}</span>
              </div>
              <Progress value={(insights.userEngagement.weeklyActiveUsers / insights.userEngagement.monthlyActiveUsers) * 100} className="h-2" />
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Monthly Active Users</span>
                <span className="text-lg font-semibold">{insights.userEngagement.monthlyActiveUsers}</span>
              </div>
              <Progress value={100} className="h-2" />
            </div>
          </div>
          
          <Separator />
          
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Retention Rate</span>
            <div className="flex items-center space-x-2">
              <Badge className={engagement.color}>
                {engagement.level}
              </Badge>
              <span className="font-semibold">{insights.userEngagement.retentionRate.toFixed(1)}%</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Performance Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Most Common Commands */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Zap className="w-5 h-5" />
              <span>Top Commands</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {insights.mostCommonCommands.slice(0, 5).map((command, index) => (
                <div key={command.command} className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium">
                      #{index + 1} {command.command}
                    </span>
                    <div className="flex items-center space-x-2">
                      <Badge variant="secondary" className="text-xs">
                        {command.count} uses
                      </Badge>
                      <span className={`text-xs ${getPerformanceColor(command.successRate, { good: 80, warning: 60 })}`}>
                        {command.successRate.toFixed(1)}%
                      </span>
                    </div>
                  </div>
                  <Progress value={command.successRate} className="h-1" />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Common Errors */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5" />
              <span>Common Issues</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {insights.mostCommonErrors.length > 0 ? (
                insights.mostCommonErrors.slice(0, 5).map((error, index) => (
                  <div key={error.error} className="flex items-center justify-between text-sm">
                    <span className="font-medium">
                      #{index + 1} {error.error}
                    </span>
                    <div className="flex items-center space-x-2">
                      <Badge variant="destructive" className="text-xs">
                        {error.count} times
                      </Badge>
                      <span className="text-xs text-muted-foreground">
                        {new Date(error.lastOccurred).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-4 text-muted-foreground">
                  <CheckCircle className="w-8 h-8 mx-auto mb-2" />
                  <p className="text-sm">No errors reported!</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Sentiment Trends */}
      {insights.sentimentTrends.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Activity className="w-5 h-5" />
              <span>Sentiment Trends</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {insights.sentimentTrends.slice(-7).map((trend, index) => (
                <div key={trend.date} className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium">{new Date(trend.date).toLocaleDateString()}</span>
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline" className="text-xs text-green-600">
                        {trend.positive}% positive
                      </Badge>
                      <Badge variant="outline" className="text-xs text-red-600">
                        {trend.negative}% negative
                      </Badge>
                    </div>
                  </div>
                  <div className="flex h-2 rounded-full overflow-hidden bg-gray-200">
                    <div className="bg-green-500" style={{ width: `${trend.positive}%` }} />
                    <div className="bg-gray-400" style={{ width: `${trend.neutral}%` }} />
                    <div className="bg-red-500" style={{ width: `${trend.negative}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}