'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { 
  Settings, 
  RefreshCw, 
  ExternalLink, 
  CheckCircle2,
  AlertCircle,
  Plus,
  BarChart3,
  TrendingUp,
  Users,
  MousePointer
} from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

interface GoogleAnalyticsProperty {
  id: string
  name: string
  websiteUrl: string
  timeZone: string
  currencyCode: string
  industryCategory: string
  connected: boolean
  lastSync?: string
  metrics?: {
    sessions: number
    users: number
    pageViews: number
    bounceRate: number
  }
}

interface GoogleAnalyticsIntegrationProps {
  tenantId?: string
  onUpdate?: (status: string) => void
}

export function GoogleAnalyticsIntegration({ tenantId = "demo", onUpdate }: GoogleAnalyticsIntegrationProps) {
  const [isConnected, setIsConnected] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [properties, setProperties] = useState<GoogleAnalyticsProperty[]>([])
  const [selectedProperty, setSelectedProperty] = useState<string>("")
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected' | 'error'>('disconnected')
  const [authUrl, setAuthUrl] = useState<string>("")
  const [error, setError] = useState<string>("")
  const [metrics, setMetrics] = useState<any>(null)

  // Check existing connection status
  useEffect(() => {
    checkConnectionStatus()
  }, [])

  const checkConnectionStatus = async () => {
    try {
      const response = await fetch(`/api/brain/integrations/google-analytics-4?tenant_id=${tenantId}`)
      if (response.ok) {
        const data = await response.json()
        setIsConnected(data.status === 'connected')
        setConnectionStatus(data.status === 'connected' ? 'connected' : 'disconnected')
        if (data.properties) {
          setProperties(data.properties)
        }
      }
    } catch (error) {
      console.error('Error checking connection status:', error)
    }
  }

  const initiateOAuthFlow = async () => {
    setIsLoading(true)
    setConnectionStatus('connecting')
    setError("")
    
    try {
      // Step 1: Get OAuth URL from Brain API
      const response = await fetch('/api/brain/integrations/google-analytics/oauth/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          redirect_uri: `${window.location.origin}/integrations/google-analytics/callback`,
          scopes: ['https://www.googleapis.com/auth/analytics.readonly']
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setAuthUrl(data.auth_url)
        
        // Open OAuth window
        const authWindow = window.open(
          data.auth_url,
          'google-analytics-auth',
          'width=600,height=600,scrollbars=yes,resizable=yes'
        )

        // Listen for OAuth completion
        const pollTimer = setInterval(() => {
          try {
            if (authWindow?.closed) {
              clearInterval(pollTimer)
              // Check if authentication was successful
              checkOAuthCompletion()
            }
          } catch (error) {
            // Cross-origin error is expected
          }
        }, 1000)

      } else {
        throw new Error('Failed to initiate OAuth flow')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to start authentication')
      setConnectionStatus('error')
    } finally {
      setIsLoading(false)
    }
  }

  const checkOAuthCompletion = async () => {
    try {
      const response = await fetch(`/api/brain/integrations/google-analytics/oauth/status?tenant_id=${tenantId}`)
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'completed') {
          setIsConnected(true)
          setConnectionStatus('connected')
          setProperties(data.properties || [])
          onUpdate?.('connected')
        } else if (data.status === 'error') {
          setError(data.error || 'Authentication failed')
          setConnectionStatus('error')
        }
      }
    } catch (error) {
      setError('Failed to complete authentication')
      setConnectionStatus('error')
    }
  }

  const syncData = async () => {
    if (!selectedProperty) {
      setError('Please select a Google Analytics property first')
      return
    }

    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/google-analytics-4/sync', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          property_id: selectedProperty
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setMetrics(data.metrics)
        // Update the selected property with new metrics
        setProperties(prev => prev.map(prop => 
          prop.id === selectedProperty 
            ? { ...prop, metrics: data.metrics, lastSync: new Date().toISOString() }
            : prop
        ))
      } else {
        throw new Error('Failed to sync data')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to sync data')
    } finally {
      setIsLoading(false)
    }
  }

  const disconnectIntegration = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/google-analytics-4/disconnect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tenant_id: tenantId }),
      })

      if (response.ok) {
        setIsConnected(false)
        setConnectionStatus('disconnected')
        setProperties([])
        setSelectedProperty("")
        setMetrics(null)
        onUpdate?.('disconnected')
      } else {
        throw new Error('Failed to disconnect')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to disconnect')
    } finally {
      setIsLoading(false)
    }
  }

  const testConnection = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/google-analytics-4/test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tenant_id: tenantId }),
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setError("")
          // Refresh properties list
          setProperties(data.properties || properties)
        } else {
          setError(data.error || 'Connection test failed')
        }
      } else {
        throw new Error('Connection test failed')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Connection test failed')
    } finally {
      setIsLoading(false)
    }
  }

  const ConnectionStatusBadge = () => {
    const statusConfig = {
      disconnected: { variant: "secondary" as const, icon: AlertCircle, text: "Not Connected" },
      connecting: { variant: "default" as const, icon: RefreshCw, text: "Connecting..." },
      connected: { variant: "default" as const, icon: CheckCircle2, text: "Connected" },
      error: { variant: "destructive" as const, icon: AlertCircle, text: "Error" }
    }

    const config = statusConfig[connectionStatus]
    const Icon = config.icon

    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <Icon className={`w-3 h-3 ${connectionStatus === 'connecting' ? 'animate-spin' : ''}`} />
        {config.text}
      </Badge>
    )
  }

  const MetricsCard = ({ title, value, icon: Icon, change }: { title: string, value: string | number, icon: any, change?: string }) => (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-muted-foreground">{title}</p>
            <p className="text-2xl font-bold">{value}</p>
            {change && (
              <p className="text-xs text-green-600 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" />
                {change}
              </p>
            )}
          </div>
          <Icon className="w-8 h-8 text-muted-foreground" />
        </div>
      </CardContent>
    </Card>
  )

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-600 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <div>
                <CardTitle>Google Analytics 4</CardTitle>
                <CardDescription>Advanced website analytics with AI-powered insights</CardDescription>
              </div>
            </div>
            <ConnectionStatusBadge />
          </div>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="setup" className="w-full">
            <TabsList>
              <TabsTrigger value="setup">Setup</TabsTrigger>
              <TabsTrigger value="properties" disabled={!isConnected}>Properties</TabsTrigger>
              <TabsTrigger value="metrics" disabled={!isConnected || !metrics}>Metrics</TabsTrigger>
              <TabsTrigger value="settings" disabled={!isConnected}>Settings</TabsTrigger>
            </TabsList>

            <TabsContent value="setup" className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {!isConnected ? (
                <div className="space-y-4">
                  <div className="text-center py-8">
                    <BarChart3 className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
                    <h3 className="text-lg font-medium mb-2">Connect Google Analytics 4</h3>
                    <p className="text-muted-foreground mb-6">
                      Get advanced website analytics with AI-powered insights and automated reporting
                    </p>
                    <Button 
                      onClick={initiateOAuthFlow} 
                      disabled={isLoading}
                      className="flex items-center gap-2"
                    >
                      {isLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
                      Connect with Google
                    </Button>
                  </div>

                  <div className="border-t pt-4">
                    <h4 className="font-medium mb-2">What you'll get:</h4>
                    <ul className="space-y-1 text-sm text-muted-foreground">
                      <li className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        Real-time website analytics and user behavior insights
                      </li>
                      <li className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        Automated report generation and anomaly detection
                      </li>
                      <li className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        AI-powered conversion optimization suggestions
                      </li>
                      <li className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        Custom dashboards and goal tracking
                      </li>
                    </ul>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="text-center py-4">
                    <CheckCircle2 className="w-16 h-16 mx-auto text-green-500 mb-4" />
                    <h3 className="text-lg font-medium mb-2">Google Analytics Connected!</h3>
                    <p className="text-muted-foreground mb-4">
                      Your Google Analytics is now connected and syncing data automatically.
                    </p>
                  </div>
                  
                  <div className="flex gap-2">
                    <Button variant="outline" onClick={testConnection} disabled={isLoading}>
                      <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                      Test Connection
                    </Button>
                    <Button variant="outline" onClick={syncData} disabled={isLoading}>
                      <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                      Sync Data
                    </Button>
                    <Button variant="destructive" onClick={disconnectIntegration} disabled={isLoading}>
                      Disconnect
                    </Button>
                  </div>
                </div>
              )}
            </TabsContent>

            <TabsContent value="properties" className="space-y-4">
              <div>
                <h3 className="font-medium mb-4">Google Analytics Properties</h3>
                <div className="grid gap-4">
                  {properties.map((property) => (
                    <Card key={property.id} className={`cursor-pointer transition-colors ${
                      selectedProperty === property.id ? 'ring-2 ring-primary' : ''
                    }`} onClick={() => setSelectedProperty(property.id)}>
                      <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                          <div>
                            <h4 className="font-medium">{property.name}</h4>
                            <p className="text-sm text-muted-foreground">{property.websiteUrl}</p>
                            <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                              <span>Timezone: {property.timeZone}</span>
                              <span>Currency: {property.currencyCode}</span>
                            </div>
                          </div>
                          <div className="text-right">
                            <Badge variant={property.connected ? "default" : "secondary"}>
                              {property.connected ? "Connected" : "Available"}
                            </Badge>
                            {property.lastSync && (
                              <p className="text-xs text-muted-foreground mt-1">
                                Last sync: {new Date(property.lastSync).toLocaleString()}
                              </p>
                            )}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            </TabsContent>

            <TabsContent value="metrics" className="space-y-4">
              {metrics && (
                <div>
                  <h3 className="font-medium mb-4">Analytics Overview</h3>
                  <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                    <MetricsCard
                      title="Total Users"
                      value={metrics.users?.toLocaleString() || '0'}
                      icon={Users}
                      change="+12.5%"
                    />
                    <MetricsCard
                      title="Sessions"
                      value={metrics.sessions?.toLocaleString() || '0'}
                      icon={MousePointer}
                      change="+8.3%"
                    />
                    <MetricsCard
                      title="Page Views"
                      value={metrics.pageViews?.toLocaleString() || '0'}
                      icon={BarChart3}
                      change="+15.2%"
                    />
                    <MetricsCard
                      title="Bounce Rate"
                      value={`${metrics.bounceRate || 0}%`}
                      icon={TrendingUp}
                    />
                  </div>
                </div>
              )}
            </TabsContent>

            <TabsContent value="settings" className="space-y-4">
              <div className="space-y-4">
                <h3 className="font-medium">Integration Settings</h3>
                
                <div className="space-y-2">
                  <Label htmlFor="sync-frequency">Data Sync Frequency</Label>
                  <select className="w-full p-2 border rounded-md">
                    <option value="hourly">Every Hour</option>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                  </select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="goals">Track Custom Goals</Label>
                  <Textarea 
                    id="goals"
                    placeholder="Enter goal IDs, one per line"
                    className="min-h-[100px]"
                  />
                </div>

                <div className="flex items-center gap-2">
                  <input type="checkbox" id="auto-reporting" defaultChecked />
                  <Label htmlFor="auto-reporting">Enable automated weekly reports</Label>
                </div>

                <div className="flex items-center gap-2">
                  <input type="checkbox" id="anomaly-detection" defaultChecked />
                  <Label htmlFor="anomaly-detection">Enable AI anomaly detection</Label>
                </div>

                <Button className="w-full">Save Settings</Button>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}