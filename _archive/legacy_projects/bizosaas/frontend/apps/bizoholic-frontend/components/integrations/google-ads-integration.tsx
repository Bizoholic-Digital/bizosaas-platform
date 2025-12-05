'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { 
  Search, 
  RefreshCw, 
  ExternalLink, 
  CheckCircle2,
  AlertCircle,
  Plus,
  Target,
  TrendingUp,
  Users,
  MousePointer,
  Globe,
  Settings,
  Play,
  Pause,
  DollarSign
} from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

interface GoogleAdsCampaign {
  id: string
  name: string
  status: 'active' | 'paused' | 'ended'
  budget: number
  spent: number
  impressions: number
  clicks: number
  conversions: number
  ctr: number
  cpc: number
  createdAt: string
  lastUpdated: string
}

interface GoogleAdsAccount {
  customerId: string
  accountName: string
  currency: string
  timeZone: string
  status: string
  balance: number
}

interface GoogleAdsIntegrationProps {
  tenantId?: string
  onUpdate?: (status: string) => void
}

export function GoogleAdsIntegration({ tenantId = "demo", onUpdate }: GoogleAdsIntegrationProps) {
  const [isConnected, setIsConnected] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [account, setAccount] = useState<GoogleAdsAccount | null>(null)
  const [campaigns, setCampaigns] = useState<GoogleAdsCampaign[]>([])
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected' | 'error'>('disconnected')
  const [error, setError] = useState<string>("")
  const [setupMethod, setSetupMethod] = useState<'guided' | 'existing'>('guided')

  // Check existing connection status
  useEffect(() => {
    checkConnectionStatus()
  }, [])

  const checkConnectionStatus = async () => {
    try {
      const response = await fetch(`/api/brain/integrations/google-ads?tenant_id=${tenantId}`)
      if (response.ok) {
        const data = await response.json()
        setIsConnected(data.status === 'connected')
        setConnectionStatus(data.status === 'connected' ? 'connected' : 'disconnected')
        if (data.account) {
          setAccount(data.account)
        }
        if (data.campaigns) {
          setCampaigns(data.campaigns)
        }
      }
    } catch (error) {
      console.error('Error checking connection status:', error)
    }
  }

  const handleConnect = async (credentials?: any) => {
    setIsLoading(true)
    setConnectionStatus('connecting')
    setError("")

    try {
      const response = await fetch('/api/brain/integrations/google-ads/connect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          setup_method: setupMethod,
          credentials: credentials
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setIsConnected(true)
        setConnectionStatus('connected')
        setAccount(data.account)
        onUpdate?.('connected')
      } else {
        throw new Error('Failed to connect Google Ads account')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to connect')
      setConnectionStatus('error')
    } finally {
      setIsLoading(false)
    }
  }

  const syncCampaigns = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/google-ads/campaigns/sync', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setCampaigns(data.campaigns || [])
      } else {
        throw new Error('Failed to sync campaigns')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to sync campaigns')
    } finally {
      setIsLoading(false)
    }
  }

  const toggleCampaign = async (campaignId: string, action: 'pause' | 'resume') => {
    try {
      const response = await fetch(`/api/brain/integrations/google-ads/campaigns/${campaignId}/${action}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tenant_id: tenantId }),
      })

      if (response.ok) {
        // Update campaign status locally
        setCampaigns(prev => prev.map(campaign => 
          campaign.id === campaignId 
            ? { ...campaign, status: action === 'pause' ? 'paused' : 'active' }
            : campaign
        ))
      } else {
        throw new Error(`Failed to ${action} campaign`)
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : `Failed to ${action} campaign`)
    }
  }

  const disconnectAccount = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/google-ads/disconnect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tenant_id: tenantId }),
      })

      if (response.ok) {
        setIsConnected(false)
        setConnectionStatus('disconnected')
        setAccount(null)
        setCampaigns([])
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

  const CampaignCard = ({ campaign }: { campaign: GoogleAdsCampaign }) => (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h4 className="font-medium">{campaign.name}</h4>
            <p className="text-sm text-muted-foreground">ID: {campaign.id}</p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant={campaign.status === 'active' ? 'default' : campaign.status === 'paused' ? 'secondary' : 'destructive'}>
              {campaign.status}
            </Badge>
            <Button
              size="sm"
              variant="outline"
              onClick={() => toggleCampaign(campaign.id, campaign.status === 'active' ? 'pause' : 'resume')}
              disabled={campaign.status === 'ended'}
            >
              {campaign.status === 'active' ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-muted-foreground">Budget</p>
            <p className="font-medium">${campaign.budget.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Spent</p>
            <p className="font-medium">${campaign.spent.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Impressions</p>
            <p className="font-medium">{campaign.impressions.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Clicks</p>
            <p className="font-medium">{campaign.clicks.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-muted-foreground">CTR</p>
            <p className="font-medium">{campaign.ctr.toFixed(2)}%</p>
          </div>
          <div>
            <p className="text-muted-foreground">CPC</p>
            <p className="font-medium">${campaign.cpc.toFixed(2)}</p>
          </div>
        </div>

        {campaign.conversions > 0 && (
          <div className="mt-3 pt-3 border-t">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Conversions</span>
              <span className="font-medium text-green-600">{campaign.conversions}</span>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-green-500 rounded-lg flex items-center justify-center">
                <Search className="w-6 h-6 text-white" />
              </div>
              <div>
                <CardTitle>Google Ads</CardTitle>
                <CardDescription>Automated Google Ads campaign management and optimization</CardDescription>
              </div>
            </div>
            <ConnectionStatusBadge />
          </div>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="setup" className="w-full">
            <TabsList>
              <TabsTrigger value="setup">Setup</TabsTrigger>
              <TabsTrigger value="campaigns" disabled={!isConnected}>Campaigns</TabsTrigger>
              <TabsTrigger value="performance" disabled={!isConnected}>Performance</TabsTrigger>
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
                  <Tabs value={setupMethod} onValueChange={(value) => setSetupMethod(value as 'guided' | 'existing')}>
                    <TabsList className="grid w-full grid-cols-2">
                      <TabsTrigger value="guided">Guided Setup</TabsTrigger>
                      <TabsTrigger value="existing">Existing Account</TabsTrigger>
                    </TabsList>

                    <TabsContent value="guided" className="space-y-4">
                      <div className="text-center py-8">
                        <Search className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
                        <h3 className="text-lg font-medium mb-2">Set Up Google Ads</h3>
                        <p className="text-muted-foreground mb-6">
                          We'll guide you through creating and configuring your Google Ads account
                        </p>
                        <Button 
                          onClick={() => handleConnect()} 
                          disabled={isLoading}
                          className="flex items-center gap-2"
                        >
                          {isLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
                          Start Guided Setup
                        </Button>
                      </div>

                      <div className="border-t pt-4">
                        <h4 className="font-medium mb-2">What's included:</h4>
                        <ul className="space-y-1 text-sm text-muted-foreground">
                          <li className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-green-500" />
                            Account creation and verification
                          </li>
                          <li className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-green-500" />
                            Automated campaign setup with AI optimization
                          </li>
                          <li className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-green-500" />
                            Smart bidding and budget management
                          </li>
                          <li className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-green-500" />
                            Conversion tracking and analytics
                          </li>
                        </ul>
                      </div>
                    </TabsContent>

                    <TabsContent value="existing" className="space-y-4">
                      <div className="space-y-4">
                        <div>
                          <Label htmlFor="customer-id">Google Ads Customer ID</Label>
                          <Input
                            id="customer-id"
                            placeholder="123-456-7890"
                            className="font-mono"
                          />
                          <p className="text-xs text-muted-foreground mt-1">
                            Find this in your Google Ads account under Settings → Account Settings
                          </p>
                        </div>

                        <div className="flex gap-3">
                          <Button
                            onClick={() => handleConnect({ customerId: "123-456-7890" })}
                            disabled={isLoading}
                          >
                            {isLoading ? <RefreshCw className="w-4 h-4 animate-spin mr-2" /> : null}
                            Connect Account
                          </Button>
                          
                          <Button 
                            variant="outline"
                            onClick={() => window.open('https://ads.google.com', '_blank')}
                          >
                            Open Google Ads
                            <ExternalLink className="ml-2 h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </TabsContent>
                  </Tabs>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="text-center py-4">
                    <CheckCircle2 className="w-16 h-16 mx-auto text-green-500 mb-4" />
                    <h3 className="text-lg font-medium mb-2">Google Ads Connected!</h3>
                    <p className="text-muted-foreground mb-4">
                      Your Google Ads account is connected and ready for campaign management.
                    </p>
                    {account && (
                      <div className="text-sm text-muted-foreground">
                        <p>Account: {account.accountName}</p>
                        <p>Customer ID: {account.customerId}</p>
                        <p>Currency: {account.currency}</p>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex gap-2">
                    <Button variant="outline" onClick={syncCampaigns} disabled={isLoading}>
                      <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                      Sync Campaigns
                    </Button>
                    <Button variant="destructive" onClick={disconnectAccount} disabled={isLoading}>
                      Disconnect
                    </Button>
                  </div>
                </div>
              )}
            </TabsContent>

            <TabsContent value="campaigns" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Active Campaigns</h3>
                <div className="flex gap-2">
                  <Button size="sm" onClick={syncCampaigns} disabled={isLoading}>
                    <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
                  </Button>
                  <Button size="sm">
                    <Plus className="w-4 h-4 mr-2" />
                    New Campaign
                  </Button>
                </div>
              </div>

              <div className="grid gap-4">
                {campaigns.map((campaign) => (
                  <CampaignCard key={campaign.id} campaign={campaign} />
                ))}
              </div>

              {campaigns.length === 0 && (
                <div className="text-center py-8">
                  <Target className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
                  <h4 className="font-medium mb-2">No Campaigns Found</h4>
                  <p className="text-muted-foreground mb-4">
                    Create your first campaign to start advertising
                  </p>
                  <Button>
                    <Plus className="w-4 h-4 mr-2" />
                    Create Campaign
                  </Button>
                </div>
              )}
            </TabsContent>

            <TabsContent value="performance" className="space-y-4">
              <div>
                <h3 className="font-medium mb-4">Performance Overview</h3>
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                  <MetricsCard
                    title="Total Spent"
                    value={`$${campaigns.reduce((sum, c) => sum + c.spent, 0).toLocaleString()}`}
                    icon={DollarSign}
                    change="+12.5%"
                  />
                  <MetricsCard
                    title="Impressions"
                    value={campaigns.reduce((sum, c) => sum + c.impressions, 0).toLocaleString()}
                    icon={Users}
                    change="+8.3%"
                  />
                  <MetricsCard
                    title="Clicks"
                    value={campaigns.reduce((sum, c) => sum + c.clicks, 0).toLocaleString()}
                    icon={MousePointer}
                    change="+15.2%"
                  />
                  <MetricsCard
                    title="Conversions"
                    value={campaigns.reduce((sum, c) => sum + c.conversions, 0).toLocaleString()}
                    icon={Target}
                    change="+22.1%"
                  />
                </div>
              </div>
            </TabsContent>

            <TabsContent value="settings" className="space-y-4">
              <div className="space-y-4">
                <h3 className="font-medium">Account Settings</h3>
                
                <div className="space-y-2">
                  <Label>Auto-optimization</Label>
                  <div className="flex items-center gap-2">
                    <input type="checkbox" defaultChecked />
                    <span className="text-sm">Enable AI-powered campaign optimization</span>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Budget Alerts</Label>
                  <div className="flex items-center gap-2">
                    <input type="checkbox" defaultChecked />
                    <span className="text-sm">Send alerts when campaigns reach 80% of budget</span>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Performance Reports</Label>
                  <select className="w-full p-2 border rounded-md">
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                  </select>
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