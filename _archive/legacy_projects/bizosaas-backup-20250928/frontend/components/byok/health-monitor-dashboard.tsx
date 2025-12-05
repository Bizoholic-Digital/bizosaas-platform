/*
BYOK Health Monitor Dashboard Component
Displays real-time health status, alerts, and monitoring for tenant API credentials
*/

import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  RefreshCw, 
  AlertTriangle, 
  CheckCircle, 
  XCircle, 
  Clock, 
  Zap,
  TrendingUp,
  TrendingDown,
  Bell,
  BellRing,
  Activity
} from 'lucide-react'
import { useBYOK } from '@/hooks/use-byok'

interface HealthStatus {
  platform: string
  tenant_id: string
  is_healthy: boolean
  last_check: string
  error_message?: string
  expires_at?: string
  api_quota_remaining?: number
  health_score: number
}

interface TenantHealthSummary {
  tenant_id: string
  overall_health_score: number
  healthy_platforms: number
  total_platforms: number
  critical_issues: string[]
  warnings: string[]
  last_check: string
}

interface Alert {
  tenant_id: string
  platform: string
  reasons: string[]
  health_score: number
  timestamp: string
  alert_type: string
}

export function HealthMonitorDashboard() {
  const router = useRouter()
  const { refresh, loading: isLoading, error } = useBYOK()
  
  const [healthSummary, setHealthSummary] = useState<TenantHealthSummary | null>(null)
  const [platformHealth, setPlatformHealth] = useState<Record<string, HealthStatus>>({})
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [autoRefresh, setAutoRefresh] = useState(true)

  // Fetch health data
  const fetchHealthData = async () => {
    try {
      setIsRefreshing(true)
      
      // Fetch tenant health summary
      const summaryResponse = await fetch('/api/byok/health', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
        }
      })
      
      if (summaryResponse.ok) {
        const summary = await summaryResponse.json()
        setHealthSummary(summary)
      }
      
      // Fetch platform-specific health data
      const platforms = ['google_ads', 'meta_ads', 'linkedin_ads']
      const healthData: Record<string, HealthStatus> = {}
      
      for (const platform of platforms) {
        try {
          const healthResponse = await fetch(`/api/byok/health/${platform}`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
            }
          })
          
          if (healthResponse.ok) {
            const health = await healthResponse.json()
            healthData[platform] = health
          }
        } catch (error) {
          console.warn(`Failed to fetch health for ${platform}:`, error)
        }
      }
      
      setPlatformHealth(healthData)
      
      // Fetch alerts
      const alertsResponse = await fetch('/api/byok/alerts', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
        }
      })
      
      if (alertsResponse.ok) {
        const alertsData = await alertsResponse.json()
        setAlerts(alertsData.alerts || [])
      }
      
    } catch (error) {
      console.error('Failed to fetch health data:', error)
    } finally {
      setIsRefreshing(false)
    }
  }

  // Auto-refresh every 30 seconds
  useEffect(() => {
    fetchHealthData()
    
    if (autoRefresh) {
      const interval = setInterval(fetchHealthData, 30000)
      return () => clearInterval(interval)
    }
  }, [autoRefresh])

  // Trigger manual health check
  const triggerHealthCheck = async (platform?: string) => {
    try {
      const response = await fetch('/api/byok/health/check', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ platform })
      })
      
      if (response.ok) {
        // Refresh data after a short delay
        setTimeout(fetchHealthData, 2000)
      }
    } catch (error) {
      console.error('Failed to trigger health check:', error)
    }
  }

  // Clear alerts
  const clearAlerts = async () => {
    try {
      const response = await fetch('/api/byok/alerts', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
        }
      })
      
      if (response.ok) {
        setAlerts([])
      }
    } catch (error) {
      console.error('Failed to clear alerts:', error)
    }
  }

  // Get health status color
  const getHealthColor = (score: number) => {
    if (score >= 0.9) return 'text-green-600'
    if (score >= 0.7) return 'text-yellow-600'
    if (score >= 0.4) return 'text-orange-600'
    return 'text-red-600'
  }

  // Get health badge variant
  const getHealthBadge = (isHealthy: boolean, score: number) => {
    if (!isHealthy) return { variant: 'destructive' as const, text: 'Unhealthy' }
    if (score >= 0.9) return { variant: 'default' as const, text: 'Excellent' }
    if (score >= 0.7) return { variant: 'secondary' as const, text: 'Good' }
    if (score >= 0.4) return { variant: 'outline' as const, text: 'Warning' }
    return { variant: 'destructive' as const, text: 'Critical' }
  }

  // Format time ago
  const timeAgo = (timestamp: string) => {
    const now = new Date()
    const time = new Date(timestamp)
    const diffMs = now.getTime() - time.getTime()
    const diffMins = Math.floor(diffMs / (1000 * 60))
    
    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`
    return `${Math.floor(diffMins / 1440)}d ago`
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">BYOK Health Monitor</h2>
          <p className="text-muted-foreground">
            Real-time monitoring of your API credentials and platform health
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setAutoRefresh(!autoRefresh)}
          >
            <Activity className="w-4 h-4 mr-2" />
            Auto-refresh {autoRefresh ? 'On' : 'Off'}
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => fetchHealthData()}
            disabled={isRefreshing}
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          
          <Button
            size="sm"
            onClick={() => triggerHealthCheck()}
            disabled={isRefreshing}
          >
            <Zap className="w-4 h-4 mr-2" />
            Run Check
          </Button>
        </div>
      </div>

      {/* Overall Health Summary */}
      {healthSummary && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="w-5 h-5" />
              Overall Health Status
            </CardTitle>
            <CardDescription>
              Last updated {timeAgo(healthSummary.last_check)}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Overall Score */}
              <div className="text-center">
                <div className={`text-3xl font-bold ${getHealthColor(healthSummary.overall_health_score)}`}>
                  {Math.round(healthSummary.overall_health_score * 100)}%
                </div>
                <div className="text-sm text-muted-foreground">Overall Score</div>
                <Progress 
                  value={healthSummary.overall_health_score * 100} 
                  className="mt-2"
                />
              </div>
              
              {/* Healthy Platforms */}
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">
                  {healthSummary.healthy_platforms}
                </div>
                <div className="text-sm text-muted-foreground">
                  of {healthSummary.total_platforms} Platforms Healthy
                </div>
              </div>
              
              {/* Critical Issues */}
              <div className="text-center">
                <div className={`text-3xl font-bold ${healthSummary.critical_issues.length > 0 ? 'text-red-600' : 'text-green-600'}`}>
                  {healthSummary.critical_issues.length}
                </div>
                <div className="text-sm text-muted-foreground">Critical Issues</div>
              </div>
              
              {/* Warnings */}
              <div className="text-center">
                <div className={`text-3xl font-bold ${healthSummary.warnings.length > 0 ? 'text-yellow-600' : 'text-green-600'}`}>
                  {healthSummary.warnings.length}
                </div>
                <div className="text-sm text-muted-foreground">Warnings</div>
              </div>
            </div>

            {/* Issues List */}
            {(healthSummary.critical_issues.length > 0 || healthSummary.warnings.length > 0) && (
              <div className="mt-6 space-y-2">
                {healthSummary.critical_issues.map((issue, index) => (
                  <Alert key={index} variant="destructive">
                    <AlertTriangle className="h-4 w-4" />
                    <AlertTitle>Critical Issue</AlertTitle>
                    <AlertDescription>{issue}</AlertDescription>
                  </Alert>
                ))}
                
                {healthSummary.warnings.map((warning, index) => (
                  <Alert key={index}>
                    <AlertTriangle className="h-4 w-4" />
                    <AlertTitle>Warning</AlertTitle>
                    <AlertDescription>{warning}</AlertDescription>
                  </Alert>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      <Tabs defaultValue="platforms" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="platforms">Platform Health</TabsTrigger>
          <TabsTrigger value="alerts">
            Alerts 
            {alerts.length > 0 && (
              <Badge variant="destructive" className="ml-2">
                {alerts.length}
              </Badge>
            )}
          </TabsTrigger>
          <TabsTrigger value="history">Health History</TabsTrigger>
        </TabsList>

        {/* Platform Health Tab */}
        <TabsContent value="platforms" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {Object.entries(platformHealth).map(([platform, health]) => {
              const badge = getHealthBadge(health.is_healthy, health.health_score)
              
              return (
                <Card key={platform}>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-lg flex items-center justify-between">
                      {platform.replace('_', ' ').toUpperCase()}
                      <Badge variant={badge.variant}>{badge.text}</Badge>
                    </CardTitle>
                    <CardDescription>
                      Last check: {timeAgo(health.last_check)}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {/* Health Score */}
                    <div>
                      <div className="flex items-center justify-between text-sm">
                        <span>Health Score</span>
                        <span className={getHealthColor(health.health_score)}>
                          {Math.round(health.health_score * 100)}%
                        </span>
                      </div>
                      <Progress value={health.health_score * 100} className="mt-1" />
                    </div>

                    {/* API Quota */}
                    {health.api_quota_remaining && (
                      <div>
                        <div className="flex items-center justify-between text-sm">
                          <span>API Quota</span>
                          <span className={health.api_quota_remaining < 1000 ? 'text-red-600' : 'text-green-600'}>
                            {health.api_quota_remaining.toLocaleString()}
                          </span>
                        </div>
                        <Progress 
                          value={Math.min((health.api_quota_remaining / 100000) * 100, 100)} 
                          className="mt-1" 
                        />
                      </div>
                    )}

                    {/* Expiry Warning */}
                    {health.expires_at && (
                      <div className="text-sm">
                        <span className="text-muted-foreground">Expires:</span>
                        <span className="ml-1">
                          {new Date(health.expires_at).toLocaleDateString()}
                        </span>
                      </div>
                    )}

                    {/* Error Message */}
                    {health.error_message && (
                      <Alert variant="destructive">
                        <XCircle className="h-4 w-4" />
                        <AlertDescription className="text-xs">
                          {health.error_message}
                        </AlertDescription>
                      </Alert>
                    )}

                    {/* Actions */}
                    <div className="flex gap-2 pt-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => triggerHealthCheck(platform)}
                        disabled={isRefreshing}
                      >
                        <RefreshCw className="w-3 h-3 mr-1" />
                        Test
                      </Button>
                      
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => router.push(`/dashboard/byok?tab=integrations&platform=${platform}`)}
                      >
                        Configure
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </TabsContent>

        {/* Alerts Tab */}
        <TabsContent value="alerts" className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Recent Alerts</h3>
            {alerts.length > 0 && (
              <Button variant="outline" size="sm" onClick={clearAlerts}>
                Clear All
              </Button>
            )}
          </div>

          {alerts.length === 0 ? (
            <Card>
              <CardContent className="text-center py-8">
                <CheckCircle className="w-12 h-12 text-green-600 mx-auto mb-4" />
                <p className="text-lg font-semibold">All systems healthy!</p>
                <p className="text-muted-foreground">No active alerts at this time.</p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-3">
              {alerts.map((alert, index) => (
                <Alert key={index} variant={alert.health_score === 0 ? "destructive" : "default"}>
                  <div className="flex items-start gap-3">
                    {alert.health_score === 0 ? (
                      <XCircle className="h-4 w-4 mt-0.5" />
                    ) : (
                      <AlertTriangle className="h-4 w-4 mt-0.5" />
                    )}
                    
                    <div className="flex-1">
                      <AlertTitle className="flex items-center justify-between">
                        <span>{alert.platform.replace('_', ' ').toUpperCase()}</span>
                        <span className="text-xs text-muted-foreground">
                          {timeAgo(alert.timestamp)}
                        </span>
                      </AlertTitle>
                      
                      <AlertDescription className="mt-1">
                        <ul className="list-disc list-inside space-y-1">
                          {alert.reasons.map((reason, reasonIndex) => (
                            <li key={reasonIndex}>{reason}</li>
                          ))}
                        </ul>
                        
                        <div className="mt-2 flex items-center gap-2">
                          <span className="text-xs">Health Score:</span>
                          <Badge variant={alert.health_score < 0.5 ? "destructive" : "outline"}>
                            {Math.round(alert.health_score * 100)}%
                          </Badge>
                        </div>
                      </AlertDescription>
                    </div>
                  </div>
                </Alert>
              ))}
            </div>
          )}
        </TabsContent>

        {/* Health History Tab */}
        <TabsContent value="history" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Health Trends</CardTitle>
              <CardDescription>
                Historical health data and performance trends
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <TrendingUp className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-lg font-semibold">Health History Coming Soon</p>
                <p className="text-muted-foreground">
                  Historical health trends and analytics will be available here.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}