'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { 
  Facebook, 
  RefreshCw, 
  ExternalLink, 
  CheckCircle2,
  AlertCircle,
  Plus,
  Target,
  TrendingUp,
  Users,
  MousePointer,
  Heart,
  Settings,
  Play,
  Pause,
  DollarSign,
  Eye,
  Share,
  MessageSquare,
  ChevronRight,
  BarChart3
} from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

interface FacebookAdsCampaign {
  id: string
  name: string
  status: 'active' | 'paused' | 'ended' | 'draft'
  objective: string
  budget_remaining: number
  daily_budget: number
  lifetime_budget?: number
  spend: number
  impressions: number
  clicks: number
  ctr: number
  cpc: number
  cpm: number
  reach: number
  frequency: number
  video_views?: number
  engagements: number
  conversions: number
  cost_per_conversion: number
  roas: number
  created_time: string
  updated_time: string
  start_time: string
  end_time?: string
}

interface FacebookAdsAccount {
  id: string
  name: string
  account_id: string
  currency: string
  timezone_name: string
  account_status: number
  balance: number
  spend_cap?: number
  business_name?: string
  business_id?: string
}

interface FacebookAdsAudience {
  id: string
  name: string
  description: string
  subtype: string
  approximate_count: number
  status: string
  retention_days: number
}

interface FacebookAdsCreative {
  id: string
  name: string
  title?: string
  body?: string
  image_url?: string
  video_id?: string
  call_to_action_type?: string
  status: string
  created_time: string
}

interface FacebookAdsIntegrationProps {
  tenantId?: string
  onUpdate?: (status: string) => void
}

export function FacebookAdsIntegration({ tenantId = "demo", onUpdate }: FacebookAdsIntegrationProps) {
  const [isConnected, setIsConnected] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [accounts, setAccounts] = useState<FacebookAdsAccount[]>([])
  const [selectedAccount, setSelectedAccount] = useState<FacebookAdsAccount | null>(null)
  const [campaigns, setCampaigns] = useState<FacebookAdsCampaign[]>([])
  const [audiences, setAudiences] = useState<FacebookAdsAudience[]>([])
  const [creatives, setCreatives] = useState<FacebookAdsCreative[]>([])
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected' | 'error'>('disconnected')
  const [error, setError] = useState<string>("")
  const [setupStep, setSetupStep] = useState<'auth' | 'account' | 'complete'>('auth')
  const [businessAccounts, setBusinessAccounts] = useState<any[]>([])
  const [isOAuthFlow, setIsOAuthFlow] = useState(false)

  // Check existing connection status
  useEffect(() => {
    checkConnectionStatus()
  }, [])

  const checkConnectionStatus = async () => {
    try {
      const response = await fetch(`/api/brain/integrations/facebook-ads?tenant_id=${tenantId}`)
      if (response.ok) {
        const data = await response.json()
        setIsConnected(data.status === 'connected')
        setConnectionStatus(data.status === 'connected' ? 'connected' : 'disconnected')
        if (data.accounts) {
          setAccounts(data.accounts)
          setSelectedAccount(data.selected_account || data.accounts[0])
        }
        if (data.campaigns) {
          setCampaigns(data.campaigns)
        }
        if (data.audiences) {
          setAudiences(data.audiences)
        }
        if (data.creatives) {
          setCreatives(data.creatives)
        }
      }
    } catch (error) {
      console.error('Error checking connection status:', error)
    }
  }

  const handleOAuthConnect = async () => {
    setIsLoading(true)
    setConnectionStatus('connecting')
    setError("")
    setIsOAuthFlow(true)

    try {
      const response = await fetch('/api/brain/integrations/facebook-ads/oauth/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          scopes: ['ads_management', 'ads_read', 'business_management', 'pages_read_engagement']
        }),
      })

      if (response.ok) {
        const data = await response.json()
        if (data.auth_url) {
          // Open OAuth flow in popup
          const popup = window.open(
            data.auth_url,
            'facebook-oauth',
            'width=600,height=600,scrollbars=yes,resizable=yes'
          )
          
          // Poll for OAuth completion
          const pollOAuth = setInterval(async () => {
            try {
              const statusResponse = await fetch(`/api/brain/integrations/facebook-ads/oauth/status?tenant_id=${tenantId}`)
              const statusData = await statusResponse.json()
              
              if (statusData.status === 'completed') {
                clearInterval(pollOAuth)
                if (popup && !popup.closed) {
                  popup.close()
                }
                await handleOAuthSuccess(statusData)
              } else if (statusData.status === 'error') {
                clearInterval(pollOAuth)
                if (popup && !popup.closed) {
                  popup.close()
                }
                throw new Error(statusData.error || 'OAuth flow failed')
              }
            } catch (error) {
              clearInterval(pollOAuth)
              if (popup && !popup.closed) {
                popup.close()
              }
              throw error
            }
          }, 2000)

          // Handle popup closed manually
          const checkClosed = setInterval(() => {
            if (popup?.closed) {
              clearInterval(checkClosed)
              clearInterval(pollOAuth)
              setIsLoading(false)
              setConnectionStatus('error')
              setError('OAuth flow was cancelled')
            }
          }, 1000)
        }
      } else {
        throw new Error('Failed to start OAuth flow')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to connect')
      setConnectionStatus('error')
      setIsLoading(false)
      setIsOAuthFlow(false)
    }
  }

  const handleOAuthSuccess = async (oauthData: any) => {
    try {
      // Fetch available ad accounts
      const accountsResponse = await fetch('/api/brain/integrations/facebook-ads/accounts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          access_token: oauthData.access_token
        }),
      })

      if (accountsResponse.ok) {
        const accountsData = await accountsResponse.json()
        setAccounts(accountsData.accounts || [])
        setBusinessAccounts(accountsData.business_accounts || [])
        setSetupStep('account')
        setIsLoading(false)
        setIsOAuthFlow(false)
      } else {
        throw new Error('Failed to fetch ad accounts')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to complete setup')
      setConnectionStatus('error')
      setIsLoading(false)
      setIsOAuthFlow(false)
    }
  }

  const selectAdAccount = async (account: FacebookAdsAccount) => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/facebook-ads/connect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          account_id: account.id,
          account_data: account
        }),
      })

      if (response.ok) {
        setSelectedAccount(account)
        setIsConnected(true)
        setConnectionStatus('connected')
        setSetupStep('complete')
        onUpdate?.('connected')
        
        // Sync initial data
        await syncAllData()
      } else {
        throw new Error('Failed to connect ad account')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to connect account')
      setConnectionStatus('error')
    } finally {
      setIsLoading(false)
    }
  }

  const syncAllData = async () => {
    setIsLoading(true)
    try {
      await Promise.all([
        syncCampaigns(),
        syncAudiences(),
        syncCreatives()
      ])
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to sync data')
    } finally {
      setIsLoading(false)
    }
  }

  const syncCampaigns = async () => {
    try {
      const response = await fetch('/api/brain/integrations/facebook-ads/campaigns/sync', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          account_id: selectedAccount?.id
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setCampaigns(data.campaigns || [])
      }
    } catch (error) {
      console.error('Error syncing campaigns:', error)
    }
  }

  const syncAudiences = async () => {
    try {
      const response = await fetch('/api/brain/integrations/facebook-ads/audiences/sync', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          account_id: selectedAccount?.id
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setAudiences(data.audiences || [])
      }
    } catch (error) {
      console.error('Error syncing audiences:', error)
    }
  }

  const syncCreatives = async () => {
    try {
      const response = await fetch('/api/brain/integrations/facebook-ads/creatives/sync', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          account_id: selectedAccount?.id
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setCreatives(data.creatives || [])
      }
    } catch (error) {
      console.error('Error syncing creatives:', error)
    }
  }

  const toggleCampaign = async (campaignId: string, action: 'pause' | 'resume') => {
    try {
      const response = await fetch(`/api/brain/integrations/facebook-ads/campaigns/${campaignId}/${action}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          tenant_id: tenantId,
          account_id: selectedAccount?.id 
        }),
      })

      if (response.ok) {
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
      const response = await fetch('/api/brain/integrations/facebook-ads/disconnect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tenant_id: tenantId }),
      })

      if (response.ok) {
        setIsConnected(false)
        setConnectionStatus('disconnected')
        setSelectedAccount(null)
        setAccounts([])
        setCampaigns([])
        setAudiences([])
        setCreatives([])
        setSetupStep('auth')
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

  const CampaignCard = ({ campaign }: { campaign: FacebookAdsCampaign }) => (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h4 className="font-medium">{campaign.name}</h4>
            <p className="text-sm text-muted-foreground">{campaign.objective}</p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant={
              campaign.status === 'active' ? 'default' : 
              campaign.status === 'paused' ? 'secondary' : 
              campaign.status === 'ended' ? 'destructive' : 'outline'
            }>
              {campaign.status}
            </Badge>
            <Button
              size="sm"
              variant="outline"
              onClick={() => toggleCampaign(campaign.id, campaign.status === 'active' ? 'pause' : 'resume')}
              disabled={campaign.status === 'ended' || campaign.status === 'draft'}
            >
              {campaign.status === 'active' ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm mb-3">
          <div>
            <p className="text-muted-foreground">Daily Budget</p>
            <p className="font-medium">${campaign.daily_budget.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Spent</p>
            <p className="font-medium">${campaign.spend.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Impressions</p>
            <p className="font-medium">{campaign.impressions.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Reach</p>
            <p className="font-medium">{campaign.reach.toLocaleString()}</p>
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
          <div>
            <p className="text-muted-foreground">CPM</p>
            <p className="font-medium">${campaign.cpm.toFixed(2)}</p>
          </div>
        </div>

        {campaign.conversions > 0 && (
          <div className="pt-3 border-t">
            <div className="grid grid-cols-3 gap-4 text-sm">
              <div>
                <p className="text-muted-foreground">Conversions</p>
                <p className="font-medium text-green-600">{campaign.conversions}</p>
              </div>
              <div>
                <p className="text-muted-foreground">Cost/Conv</p>
                <p className="font-medium">${campaign.cost_per_conversion.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-muted-foreground">ROAS</p>
                <p className="font-medium">{campaign.roas.toFixed(2)}x</p>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )

  const AudienceCard = ({ audience }: { audience: FacebookAdsAudience }) => (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-2">
          <h4 className="font-medium">{audience.name}</h4>
          <Badge variant={audience.status === 'READY' ? 'default' : 'secondary'}>
            {audience.status}
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground mb-3">{audience.description}</p>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-muted-foreground">Size</p>
            <p className="font-medium">{audience.approximate_count.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Type</p>
            <p className="font-medium">{audience.subtype}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  )

  const CreativeCard = ({ creative }: { creative: FacebookAdsCreative }) => (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-2">
          <h4 className="font-medium">{creative.name}</h4>
          <Badge variant={creative.status === 'ACTIVE' ? 'default' : 'secondary'}>
            {creative.status}
          </Badge>
        </div>
        {creative.title && (
          <p className="text-sm font-medium mb-1">{creative.title}</p>
        )}
        {creative.body && (
          <p className="text-sm text-muted-foreground mb-3 line-clamp-2">{creative.body}</p>
        )}
        <div className="flex items-center justify-between">
          {creative.image_url && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Eye className="w-4 h-4" />
              Image
            </div>
          )}
          {creative.call_to_action_type && (
            <Badge variant="outline" className="text-xs">
              {creative.call_to_action_type}
            </Badge>
          )}
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
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
                <Facebook className="w-6 h-6 text-white" />
              </div>
              <div>
                <CardTitle>Facebook Ads</CardTitle>
                <CardDescription>Advanced Facebook & Instagram advertising management</CardDescription>
              </div>
            </div>
            <ConnectionStatusBadge />
          </div>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="setup" className="w-full">
            <TabsList className="grid grid-cols-6 w-full">
              <TabsTrigger value="setup">Setup</TabsTrigger>
              <TabsTrigger value="campaigns" disabled={!isConnected}>Campaigns</TabsTrigger>
              <TabsTrigger value="audiences" disabled={!isConnected}>Audiences</TabsTrigger>
              <TabsTrigger value="creatives" disabled={!isConnected}>Creatives</TabsTrigger>
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
                <div className="space-y-6">
                  {/* Step 1: OAuth Authentication */}
                  {setupStep === 'auth' && (
                    <div className="text-center py-8">
                      <Facebook className="w-16 h-16 mx-auto text-blue-600 mb-4" />
                      <h3 className="text-lg font-medium mb-2">Connect to Facebook Business Manager</h3>
                      <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                        Connect your Facebook Business Manager account to access ad accounts, create campaigns, and manage your advertising.
                      </p>
                      
                      <Button 
                        onClick={handleOAuthConnect} 
                        disabled={isLoading || isOAuthFlow}
                        size="lg"
                        className="bg-blue-600 hover:bg-blue-700 text-white"
                      >
                        {isLoading || isOAuthFlow ? (
                          <>
                            <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                            {isOAuthFlow ? 'Waiting for authorization...' : 'Connecting...'}
                          </>
                        ) : (
                          <>
                            <Facebook className="w-4 h-4 mr-2" />
                            Connect Facebook Account
                          </>
                        )}
                      </Button>

                      <div className="border-t pt-6 mt-8">
                        <h4 className="font-medium mb-3">What you'll get:</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-left">
                          <div className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-green-500" />
                            Full campaign management across Facebook & Instagram
                          </div>
                          <div className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-green-500" />
                            Advanced audience targeting and lookalikes
                          </div>
                          <div className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-green-500" />
                            Creative testing and optimization
                          </div>
                          <div className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-green-500" />
                            Real-time performance analytics
                          </div>
                          <div className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-green-500" />
                            Automated bid optimization
                          </div>
                          <div className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-green-500" />
                            Cross-platform conversion tracking
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Step 2: Ad Account Selection */}
                  {setupStep === 'account' && accounts.length > 0 && (
                    <div className="space-y-4">
                      <div className="text-center py-4">
                        <h3 className="text-lg font-medium mb-2">Select Ad Account</h3>
                        <p className="text-muted-foreground mb-6">
                          Choose the ad account you want to connect for campaign management.
                        </p>
                      </div>

                      <div className="grid gap-3">
                        {accounts.map((account) => (
                          <Card key={account.id} className="cursor-pointer hover:shadow-md transition-shadow">
                            <CardContent className="p-4">
                              <div className="flex items-center justify-between">
                                <div className="flex-1">
                                  <div className="flex items-center gap-2 mb-1">
                                    <h4 className="font-medium">{account.name}</h4>
                                    <Badge variant="outline">{account.currency}</Badge>
                                  </div>
                                  <p className="text-sm text-muted-foreground">
                                    Account ID: {account.account_id}
                                  </p>
                                  {account.business_name && (
                                    <p className="text-sm text-muted-foreground">
                                      Business: {account.business_name}
                                    </p>
                                  )}
                                  <div className="flex items-center gap-4 mt-2 text-sm">
                                    <span className="text-muted-foreground">
                                      Balance: ${(account.balance / 100).toLocaleString()}
                                    </span>
                                    <span className={`${account.account_status === 1 ? 'text-green-600' : 'text-red-600'}`}>
                                      {account.account_status === 1 ? 'Active' : 'Inactive'}
                                    </span>
                                  </div>
                                </div>
                                <Button 
                                  onClick={() => selectAdAccount(account)}
                                  disabled={isLoading || account.account_status !== 1}
                                >
                                  {isLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : 'Select'}
                                </Button>
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="text-center py-4">
                    <CheckCircle2 className="w-16 h-16 mx-auto text-green-500 mb-4" />
                    <h3 className="text-lg font-medium mb-2">Facebook Ads Connected!</h3>
                    <p className="text-muted-foreground mb-4">
                      Your Facebook ad account is connected and ready for campaign management.
                    </p>
                    {selectedAccount && (
                      <div className="text-sm text-muted-foreground space-y-1">
                        <p>Account: {selectedAccount.name}</p>
                        <p>Account ID: {selectedAccount.account_id}</p>
                        <p>Currency: {selectedAccount.currency}</p>
                        <p>Balance: ${(selectedAccount.balance / 100).toLocaleString()}</p>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex gap-2 justify-center">
                    <Button variant="outline" onClick={syncAllData} disabled={isLoading}>
                      <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                      Sync All Data
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
                <h3 className="font-medium">Campaigns</h3>
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
                    Create your first Facebook advertising campaign
                  </p>
                  <Button>
                    <Plus className="w-4 h-4 mr-2" />
                    Create Campaign
                  </Button>
                </div>
              )}
            </TabsContent>

            <TabsContent value="audiences" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Custom Audiences</h3>
                <div className="flex gap-2">
                  <Button size="sm" onClick={syncAudiences} disabled={isLoading}>
                    <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
                  </Button>
                  <Button size="sm">
                    <Plus className="w-4 h-4 mr-2" />
                    Create Audience
                  </Button>
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                {audiences.map((audience) => (
                  <AudienceCard key={audience.id} audience={audience} />
                ))}
              </div>

              {audiences.length === 0 && (
                <div className="text-center py-8">
                  <Users className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
                  <h4 className="font-medium mb-2">No Audiences Found</h4>
                  <p className="text-muted-foreground mb-4">
                    Create custom audiences for better targeting
                  </p>
                  <Button>
                    <Plus className="w-4 h-4 mr-2" />
                    Create Audience
                  </Button>
                </div>
              )}
            </TabsContent>

            <TabsContent value="creatives" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Ad Creatives</h3>
                <div className="flex gap-2">
                  <Button size="sm" onClick={syncCreatives} disabled={isLoading}>
                    <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
                  </Button>
                  <Button size="sm">
                    <Plus className="w-4 h-4 mr-2" />
                    Create Creative
                  </Button>
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {creatives.map((creative) => (
                  <CreativeCard key={creative.id} creative={creative} />
                ))}
              </div>

              {creatives.length === 0 && (
                <div className="text-center py-8">
                  <Heart className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
                  <h4 className="font-medium mb-2">No Creatives Found</h4>
                  <p className="text-muted-foreground mb-4">
                    Upload and manage your ad creatives
                  </p>
                  <Button>
                    <Plus className="w-4 h-4 mr-2" />
                    Create Creative
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
                    value={`$${campaigns.reduce((sum, c) => sum + c.spend, 0).toLocaleString()}`}
                    icon={DollarSign}
                    change="+12.5%"
                  />
                  <MetricsCard
                    title="Impressions"
                    value={campaigns.reduce((sum, c) => sum + c.impressions, 0).toLocaleString()}
                    icon={Eye}
                    change="+8.3%"
                  />
                  <MetricsCard
                    title="Reach"
                    value={campaigns.reduce((sum, c) => sum + c.reach, 0).toLocaleString()}
                    icon={Users}
                    change="+15.2%"
                  />
                  <MetricsCard
                    title="Clicks"
                    value={campaigns.reduce((sum, c) => sum + c.clicks, 0).toLocaleString()}
                    icon={MousePointer}
                    change="+22.1%"
                  />
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <MetricsCard
                  title="Avg. CTR"
                  value={`${(campaigns.reduce((sum, c) => sum + c.ctr, 0) / campaigns.length || 0).toFixed(2)}%`}
                  icon={Target}
                  change="+5.7%"
                />
                <MetricsCard
                  title="Avg. CPC"
                  value={`$${(campaigns.reduce((sum, c) => sum + c.cpc, 0) / campaigns.length || 0).toFixed(2)}`}
                  icon={DollarSign}
                  change="-3.2%"
                />
                <MetricsCard
                  title="Total Conversions"
                  value={campaigns.reduce((sum, c) => sum + c.conversions, 0).toLocaleString()}
                  icon={Target}
                  change="+18.9%"
                />
                <MetricsCard
                  title="Avg. ROAS"
                  value={`${(campaigns.reduce((sum, c) => sum + c.roas, 0) / campaigns.length || 0).toFixed(2)}x`}
                  icon={BarChart3}
                  change="+11.4%"
                />
              </div>
            </TabsContent>

            <TabsContent value="settings" className="space-y-4">
              <div className="space-y-4">
                <h3 className="font-medium">Facebook Ads Settings</h3>
                
                <div className="space-y-4">
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
                    <Label>Automatic Placements</Label>
                    <div className="flex items-center gap-2">
                      <input type="checkbox" defaultChecked />
                      <span className="text-sm">Allow Facebook to optimize ad placements</span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>Performance Reports</Label>
                    <Select defaultValue="weekly">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="daily">Daily</SelectItem>
                        <SelectItem value="weekly">Weekly</SelectItem>
                        <SelectItem value="monthly">Monthly</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Attribution Window</Label>
                    <Select defaultValue="7d_click_1d_view">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1d_click">1-day click</SelectItem>
                        <SelectItem value="7d_click_1d_view">7-day click, 1-day view</SelectItem>
                        <SelectItem value="28d_click_1d_view">28-day click, 1-day view</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <Button className="w-full">Save Settings</Button>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}