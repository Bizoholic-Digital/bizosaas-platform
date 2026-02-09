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
  Search, 
  RefreshCw, 
  ExternalLink, 
  CheckCircle2,
  AlertCircle,
  Plus,
  BarChart3,
  TrendingUp,
  Eye,
  Globe,
  Smartphone,
  Link,
  FileText,
  Activity,
  Settings,
  Filter,
  Calendar,
  Download,
  Upload,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Clock,
  MousePointer,
  Users,
  Target,
  Zap,
  MapPin,
  Shield,
  Gauge,
  Key,
  Database,
  TrendingDown,
  Bug,
  Ban
} from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'

interface BingWebmasterSite {
  url: string
  is_verified: boolean
  verification_method?: string
  site_status: 'Active' | 'Inactive' | 'Pending'
  crawl_stats?: {
    pages_crawled: number
    pages_in_index: number
    crawl_errors: number
  }
}

interface SearchPerformanceData {
  query: string
  page: string
  country: string
  device: string
  clicks: number
  impressions: number
  ctr: number
  position: number
  date: string
}

interface KeywordResearchData {
  keyword: string
  search_volume: number
  competition: 'Low' | 'Medium' | 'High'
  cpc: number
  difficulty: number
  trends: Array<{
    month: string
    volume: number
  }>
}

interface CrawlStatsData {
  site_url: string
  last_crawl_date: string
  pages_crawled: number
  pages_discovered: number
  pages_in_index: number
  crawl_errors: number
  blocked_urls: number
  crawl_issues: Array<{
    issue_type: string
    count: number
    severity: 'High' | 'Medium' | 'Low'
    pages: string[]
  }>
}

interface SitemapData {
  path: string
  last_submitted: string
  status: 'Submitted' | 'Processed' | 'Error' | 'Warning'
  urls_submitted: number
  urls_indexed: number
  errors: number
  warnings: number
}

interface URLSubmissionData {
  url: string
  submission_date: string
  status: 'Submitted' | 'Processing' | 'Indexed' | 'Error'
  quota_remaining: number
  daily_quota: number
}

interface BingWebmasterIntegrationProps {
  tenantId?: string
  onUpdate?: (status: string) => void
}

export function BingWebmasterIntegration({ tenantId = "demo", onUpdate }: BingWebmasterIntegrationProps) {
  const [isConnected, setIsConnected] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [sites, setSites] = useState<BingWebmasterSite[]>([])
  const [selectedSite, setSelectedSite] = useState<string>("")
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected' | 'error'>('disconnected')
  const [authUrl, setAuthUrl] = useState<string>("")
  const [error, setError] = useState<string>("")
  const [apiKey, setApiKey] = useState<string>("")
  const [showApiKeyInput, setShowApiKeyInput] = useState(false)
  
  // Data states
  const [searchPerformanceData, setSearchPerformanceData] = useState<SearchPerformanceData[]>([])
  const [keywordData, setKeywordData] = useState<KeywordResearchData[]>([])
  const [crawlStatsData, setCrawlStatsData] = useState<CrawlStatsData | null>(null)
  const [sitemapsData, setSitemapsData] = useState<SitemapData[]>([])
  const [urlSubmissionData, setUrlSubmissionData] = useState<URLSubmissionData[]>([])
  const [blockedUrls, setBlockedUrls] = useState<string[]>([])
  
  // UI states
  const [activeTab, setActiveTab] = useState('connection')
  const [dateRange, setDateRange] = useState('last_7_days')
  const [urlsToSubmit, setUrlsToSubmit] = useState('')
  const [keywordQuery, setKeywordQuery] = useState('')
  const [newSitemapUrl, setNewSitemapUrl] = useState('')
  const [urlsToBlock, setUrlsToBlock] = useState('')
  const [showAddSitemap, setShowAddSitemap] = useState(false)
  const [showUrlSubmission, setShowUrlSubmission] = useState(false)
  const [showKeywordResearch, setShowKeywordResearch] = useState(false)
  const [showBlockUrls, setShowBlockUrls] = useState(false)

  // Check existing connection status
  useEffect(() => {
    checkConnectionStatus()
  }, [])

  const checkConnectionStatus = async () => {
    try {
      const response = await fetch(`/api/brain/integrations/bing-webmaster?tenant_id=${tenantId}`)
      if (response.ok) {
        const data = await response.json()
        setIsConnected(data.status === 'connected')
        setConnectionStatus(data.status === 'connected' ? 'connected' : 'disconnected')
        if (data.sites) {
          setSites(data.sites)
          if (data.sites.length > 0 && !selectedSite) {
            setSelectedSite(data.sites[0].url)
          }
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
      const response = await fetch('/api/brain/integrations/bing-webmaster/oauth/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          redirect_uri: `${window.location.origin}/integrations/bing-webmaster/callback`,
          scopes: ['wt.read']
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setAuthUrl(data.auth_url)
        
        const authWindow = window.open(
          data.auth_url,
          'bing-webmaster-auth',
          'width=600,height=600,scrollbars=yes,resizable=yes'
        )

        const pollTimer = setInterval(() => {
          try {
            if (authWindow?.closed) {
              clearInterval(pollTimer)
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

  const connectWithApiKey = async () => {
    if (!apiKey.trim()) {
      setError('Please enter your Bing Webmaster API key')
      return
    }

    setIsLoading(true)
    setConnectionStatus('connecting')
    setError("")
    
    try {
      const response = await fetch('/api/brain/integrations/bing-webmaster/api-key', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          api_key: apiKey
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setIsConnected(true)
        setConnectionStatus('connected')
        setSites(data.sites || [])
        if (data.sites?.length > 0) {
          setSelectedSite(data.sites[0].url)
        }
        setShowApiKeyInput(false)
        setApiKey('')
        onUpdate?.('connected')
      } else {
        const data = await response.json()
        throw new Error(data.error || 'Invalid API key')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to connect with API key')
      setConnectionStatus('error')
    } finally {
      setIsLoading(false)
    }
  }

  const checkOAuthCompletion = async () => {
    try {
      const response = await fetch(`/api/brain/integrations/bing-webmaster/oauth/status?tenant_id=${tenantId}`)
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'completed') {
          setIsConnected(true)
          setConnectionStatus('connected')
          setSites(data.sites || [])
          if (data.sites?.length > 0) {
            setSelectedSite(data.sites[0].url)
          }
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

  const fetchSearchPerformanceData = async () => {
    if (!selectedSite) return

    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/bing-webmaster/search-analytics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          site_url: selectedSite,
          start_date: getDateRangeStart(dateRange),
          end_date: new Date().toISOString().split('T')[0],
          dimensions: ['query', 'page'],
          max_results: 100
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setSearchPerformanceData(data.search_data || [])
      } else {
        throw new Error('Failed to fetch search performance data')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to fetch search performance data')
    } finally {
      setIsLoading(false)
    }
  }

  const fetchKeywordResearch = async () => {
    if (!keywordQuery.trim()) {
      setError('Please enter a keyword to research')
      return
    }

    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/bing-webmaster/keyword-research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          keywords: [keywordQuery],
          location: 'US',
          language: 'en'
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setKeywordData(data.keyword_data || [])
        setShowKeywordResearch(false)
      } else {
        throw new Error('Failed to fetch keyword research data')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to fetch keyword research data')
    } finally {
      setIsLoading(false)
    }
  }

  const fetchCrawlStats = async () => {
    if (!selectedSite) return

    setIsLoading(true)
    try {
      const response = await fetch(`/api/brain/integrations/bing-webmaster/crawl-stats?tenant_id=${tenantId}&site_url=${encodeURIComponent(selectedSite)}`)
      
      if (response.ok) {
        const data = await response.json()
        setCrawlStatsData(data.crawl_stats)
      } else {
        throw new Error('Failed to fetch crawl statistics')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to fetch crawl statistics')
    } finally {
      setIsLoading(false)
    }
  }

  const fetchSitemaps = async () => {
    if (!selectedSite) return

    setIsLoading(true)
    try {
      const response = await fetch(`/api/brain/integrations/bing-webmaster/sitemaps?tenant_id=${tenantId}&site_url=${encodeURIComponent(selectedSite)}`)
      
      if (response.ok) {
        const data = await response.json()
        setSitemapsData(data.sitemaps || [])
      } else {
        throw new Error('Failed to fetch sitemaps data')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to fetch sitemaps data')
    } finally {
      setIsLoading(false)
    }
  }

  const submitUrls = async () => {
    if (!selectedSite || !urlsToSubmit.trim()) return

    const urls = urlsToSubmit.split('\n').filter(url => url.trim())
    if (urls.length === 0) {
      setError('Please enter at least one URL to submit')
      return
    }

    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/bing-webmaster/url-submission', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          site_url: selectedSite,
          urls: urls
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setUrlSubmissionData(prev => [...prev, ...data.submissions])
        setShowUrlSubmission(false)
        setUrlsToSubmit('')
      } else {
        throw new Error('Failed to submit URLs')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to submit URLs')
    } finally {
      setIsLoading(false)
    }
  }

  const addSitemap = async () => {
    if (!selectedSite || !newSitemapUrl) return

    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/bing-webmaster/sitemaps', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          site_url: selectedSite,
          sitemap_url: newSitemapUrl
        }),
      })

      if (response.ok) {
        fetchSitemaps()
        setShowAddSitemap(false)
        setNewSitemapUrl('')
      } else {
        throw new Error('Failed to add sitemap')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to add sitemap')
    } finally {
      setIsLoading(false)
    }
  }

  const blockUrls = async () => {
    if (!selectedSite || !urlsToBlock.trim()) return

    const urls = urlsToBlock.split('\n').filter(url => url.trim())
    if (urls.length === 0) {
      setError('Please enter at least one URL to block')
      return
    }

    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/bing-webmaster/block-urls', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          site_url: selectedSite,
          urls: urls
        }),
      })

      if (response.ok) {
        setBlockedUrls(prev => [...prev, ...urls])
        setShowBlockUrls(false)
        setUrlsToBlock('')
      } else {
        throw new Error('Failed to block URLs')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to block URLs')
    } finally {
      setIsLoading(false)
    }
  }

  const disconnectIntegration = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/bing-webmaster/disconnect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tenant_id: tenantId }),
      })

      if (response.ok) {
        setIsConnected(false)
        setConnectionStatus('disconnected')
        setSites([])
        setSelectedSite("")
        setSearchPerformanceData([])
        setKeywordData([])
        setCrawlStatsData(null)
        setSitemapsData([])
        setUrlSubmissionData([])
        setBlockedUrls([])
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
      const response = await fetch('/api/brain/integrations/bing-webmaster/test', {
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
          setSites(data.sites || sites)
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

  const getDateRangeStart = (range: string) => {
    const now = new Date()
    const daysAgo = {
      'last_7_days': 7,
      'last_28_days': 28,
      'last_3_months': 90,
      'last_12_months': 365
    }[range] || 7

    const startDate = new Date(now.getTime() - (daysAgo * 24 * 60 * 60 * 1000))
    return startDate.toISOString().split('T')[0]
  }

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat().format(num)
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

  const MetricsCard = ({ title, value, icon: Icon, change, color = "blue" }: { 
    title: string, 
    value: string | number, 
    icon: any, 
    change?: string,
    color?: string
  }) => (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-muted-foreground">{title}</p>
            <p className="text-2xl font-bold">{value}</p>
            {change && (
              <p className={`text-xs flex items-center gap-1 ${change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                <TrendingUp className="w-3 h-3" />
                {change}
              </p>
            )}
          </div>
          <Icon className={`w-8 h-8 text-${color}-500`} />
        </div>
      </CardContent>
    </Card>
  )

  const getCrawlIssueColor = (severity: string) => {
    switch (severity) {
      case 'High': return 'text-red-600 bg-red-50'
      case 'Medium': return 'text-yellow-600 bg-yellow-50'
      case 'Low': return 'text-blue-600 bg-blue-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  const getSitemapStatusColor = (status: string) => {
    switch (status) {
      case 'Processed': return 'text-green-600 bg-green-50'
      case 'Error': return 'text-red-600 bg-red-50'
      case 'Warning': return 'text-yellow-600 bg-yellow-50'
      case 'Submitted': return 'text-blue-600 bg-blue-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  const getSubmissionStatusColor = (status: string) => {
    switch (status) {
      case 'Indexed': return 'text-green-600 bg-green-50'
      case 'Error': return 'text-red-600 bg-red-50'
      case 'Processing': return 'text-yellow-600 bg-yellow-50'
      case 'Submitted': return 'text-blue-600 bg-blue-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  // Effect to fetch data when site changes
  useEffect(() => {
    if (selectedSite && isConnected) {
      if (activeTab === 'analytics') {
        fetchSearchPerformanceData()
      } else if (activeTab === 'crawl-stats') {
        fetchCrawlStats()
      } else if (activeTab === 'sitemaps') {
        fetchSitemaps()
      }
    }
  }, [selectedSite, isConnected, activeTab, dateRange])

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
                <Search className="w-6 h-6 text-white" />
              </div>
              <div>
                <CardTitle>Bing Webmaster Tools</CardTitle>
                <CardDescription>Monitor search performance, crawl stats, and manage your site on Bing</CardDescription>
              </div>
            </div>
            <ConnectionStatusBadge />
          </div>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList>
              <TabsTrigger value="connection">Connection</TabsTrigger>
              <TabsTrigger value="sites" disabled={!isConnected}>Sites</TabsTrigger>
              <TabsTrigger value="analytics" disabled={!isConnected || !selectedSite}>Analytics</TabsTrigger>
              <TabsTrigger value="url-tools" disabled={!isConnected || !selectedSite}>URL Tools</TabsTrigger>
              <TabsTrigger value="keywords" disabled={!isConnected}>Keywords</TabsTrigger>
              <TabsTrigger value="crawl-stats" disabled={!isConnected || !selectedSite}>Crawl Stats</TabsTrigger>
              <TabsTrigger value="sitemaps" disabled={!isConnected || !selectedSite}>Sitemaps</TabsTrigger>
              <TabsTrigger value="block-urls" disabled={!isConnected || !selectedSite}>Block URLs</TabsTrigger>
            </TabsList>

            <TabsContent value="connection" className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {!isConnected ? (
                <div className="space-y-4">
                  <div className="text-center py-8">
                    <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
                      <Search className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-lg font-medium mb-2">Connect Bing Webmaster Tools</h3>
                    <p className="text-muted-foreground mb-6">
                      Monitor your website's performance on Bing and manage search optimization
                    </p>
                    
                    <div className="flex flex-col gap-3 max-w-sm mx-auto">
                      <Button 
                        onClick={initiateOAuthFlow} 
                        disabled={isLoading}
                        className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700"
                      >
                        {isLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
                        Connect with Microsoft
                      </Button>
                      
                      <div className="text-center">
                        <span className="text-sm text-muted-foreground">or</span>
                      </div>
                      
                      {!showApiKeyInput ? (
                        <Button 
                          variant="outline"
                          onClick={() => setShowApiKeyInput(true)}
                          className="flex items-center gap-2"
                        >
                          <Key className="w-4 h-4" />
                          Use API Key
                        </Button>
                      ) : (
                        <div className="space-y-3">
                          <div>
                            <Label htmlFor="api-key">Bing Webmaster API Key</Label>
                            <Input
                              id="api-key"
                              type="password"
                              value={apiKey}
                              onChange={(e) => setApiKey(e.target.value)}
                              placeholder="Enter your API key"
                            />
                            <p className="text-xs text-muted-foreground mt-1">
                              Get your API key from Bing Webmaster Tools dashboard
                            </p>
                          </div>
                          <div className="flex gap-2">
                            <Button 
                              onClick={connectWithApiKey}
                              disabled={isLoading || !apiKey.trim()}
                              className="flex-1"
                            >
                              {isLoading ? <RefreshCw className="w-4 h-4 animate-spin mr-2" /> : null}
                              Connect
                            </Button>
                            <Button 
                              variant="outline"
                              onClick={() => {
                                setShowApiKeyInput(false)
                                setApiKey('')
                              }}
                            >
                              Cancel
                            </Button>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h4 className="font-medium mb-2">What you'll get:</h4>
                    <ul className="space-y-1 text-sm text-muted-foreground">
                      <li className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        Search performance analytics and keyword insights
                      </li>
                      <li className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        URL submission with 10,000 daily quota
                      </li>
                      <li className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        Keyword research with search volume data
                      </li>
                      <li className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        Crawl statistics and error monitoring
                      </li>
                      <li className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        Sitemap management and URL blocking tools
                      </li>
                    </ul>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="text-center py-4">
                    <CheckCircle2 className="w-16 h-16 mx-auto text-green-500 mb-4" />
                    <h3 className="text-lg font-medium mb-2">Bing Webmaster Tools Connected!</h3>
                    <p className="text-muted-foreground mb-4">
                      Your Bing Webmaster Tools is connected and ready to provide search insights.
                    </p>
                  </div>
                  
                  <div className="flex gap-2">
                    <Button variant="outline" onClick={testConnection} disabled={isLoading}>
                      <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                      Test Connection
                    </Button>
                    <Button variant="outline" onClick={checkConnectionStatus} disabled={isLoading}>
                      <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                      Refresh Data
                    </Button>
                    <Button variant="destructive" onClick={disconnectIntegration} disabled={isLoading}>
                      Disconnect
                    </Button>
                  </div>
                </div>
              )}
            </TabsContent>

            <TabsContent value="sites" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Bing Webmaster Sites</h3>
                <Button variant="outline" asChild>
                  <a href="https://www.bing.com/webmasters" target="_blank" rel="noopener noreferrer">
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Bing Webmaster Tools
                  </a>
                </Button>
              </div>
              
              <div className="grid gap-4">
                {sites.map((site) => (
                  <Card key={site.url} className={`cursor-pointer transition-colors ${
                    selectedSite === site.url ? 'ring-2 ring-blue-500' : ''
                  }`} onClick={() => setSelectedSite(site.url)}>
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className="p-2 bg-blue-50 rounded-lg">
                            <Globe className="w-5 h-5 text-blue-600" />
                          </div>
                          <div>
                            <h4 className="font-medium">{site.url}</h4>
                            <p className="text-sm text-muted-foreground">
                              Status: {site.site_status}
                            </p>
                            {site.crawl_stats && (
                              <p className="text-xs text-muted-foreground mt-1">
                                {formatNumber(site.crawl_stats.pages_in_index)} pages indexed, {site.crawl_stats.crawl_errors} errors
                              </p>
                            )}
                          </div>
                        </div>
                        <div className="text-right">
                          <Badge variant={site.is_verified ? "default" : "secondary"} className="flex items-center gap-1 mb-2">
                            {site.is_verified ? <CheckCircle className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
                            {site.is_verified ? "Verified" : "Unverified"}
                          </Badge>
                          {site.verification_method && (
                            <p className="text-xs text-muted-foreground">
                              Via {site.verification_method}
                            </p>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="analytics" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Search Performance Analytics</h3>
                <div className="flex items-center gap-2">
                  <Select value={dateRange} onValueChange={setDateRange}>
                    <SelectTrigger className="w-40">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="last_7_days">Last 7 days</SelectItem>
                      <SelectItem value="last_28_days">Last 28 days</SelectItem>
                      <SelectItem value="last_3_months">Last 3 months</SelectItem>
                      <SelectItem value="last_12_months">Last 12 months</SelectItem>
                    </SelectContent>
                  </Select>
                  <Button variant="outline" size="sm" onClick={fetchSearchPerformanceData} disabled={isLoading}>
                    <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                    Refresh
                  </Button>
                </div>
              </div>

              {searchPerformanceData.length > 0 && (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                  <MetricsCard
                    title="Total Clicks"
                    value={formatNumber(searchPerformanceData.reduce((sum, row) => sum + row.clicks, 0))}
                    icon={MousePointer}
                    color="blue"
                    change="+8.7%"
                  />
                  <MetricsCard
                    title="Total Impressions"
                    value={formatNumber(searchPerformanceData.reduce((sum, row) => sum + row.impressions, 0))}
                    icon={Eye}
                    color="green"
                    change="+15.3%"
                  />
                  <MetricsCard
                    title="Average CTR"
                    value={`${(searchPerformanceData.reduce((sum, row) => sum + row.ctr, 0) / searchPerformanceData.length).toFixed(2)}%`}
                    icon={Target}
                    color="purple"
                    change="+1.8%"
                  />
                  <MetricsCard
                    title="Average Position"
                    value={(searchPerformanceData.reduce((sum, row) => sum + row.position, 0) / searchPerformanceData.length).toFixed(1)}
                    icon={TrendingUp}
                    color="orange"
                    change="-0.9"
                  />
                </div>
              )}

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="w-5 h-5" />
                    Top Performing Queries
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {searchPerformanceData.length > 0 ? (
                    <div className="overflow-x-auto">
                      <table className="w-full">
                        <thead>
                          <tr className="border-b">
                            <th className="text-left p-2">Query</th>
                            <th className="text-right p-2">Clicks</th>
                            <th className="text-right p-2">Impressions</th>
                            <th className="text-right p-2">CTR</th>
                            <th className="text-right p-2">Position</th>
                          </tr>
                        </thead>
                        <tbody>
                          {searchPerformanceData.slice(0, 10).map((row, index) => (
                            <tr key={index} className="border-b">
                              <td className="p-2 font-medium">{row.query}</td>
                              <td className="p-2 text-right">{formatNumber(row.clicks)}</td>
                              <td className="p-2 text-right">{formatNumber(row.impressions)}</td>
                              <td className="p-2 text-right">{row.ctr.toFixed(2)}%</td>
                              <td className="p-2 text-right">{row.position.toFixed(1)}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      <BarChart3 className="w-12 h-12 mx-auto mb-2" />
                      <p>No search performance data available</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="url-tools" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">URL Submission Tools</h3>
                <Button variant="outline" size="sm" onClick={() => setShowUrlSubmission(true)}>
                  <Plus className="w-4 h-4 mr-2" />
                  Submit URLs
                </Button>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Upload className="w-5 h-5" />
                      URL Submission Quota
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center py-4">
                      <div className="text-3xl font-bold text-blue-600 mb-2">
                        {urlSubmissionData.length > 0 ? urlSubmissionData[0].quota_remaining : 10000}
                      </div>
                      <p className="text-sm text-muted-foreground mb-4">
                        URLs remaining today (out of {urlSubmissionData.length > 0 ? urlSubmissionData[0].daily_quota : 10000})
                      </p>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full"
                          style={{
                            width: `${urlSubmissionData.length > 0 
                              ? (urlSubmissionData[0].quota_remaining / urlSubmissionData[0].daily_quota) * 100
                              : 100}%`
                          }}
                        ></div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Clock className="w-5 h-5" />
                      Recent Submissions
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    {urlSubmissionData.length > 0 ? (
                      <div className="space-y-2">
                        {urlSubmissionData.slice(0, 5).map((submission, index) => (
                          <div key={index} className="flex items-center justify-between p-2 rounded border">
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium truncate">{submission.url}</p>
                              <p className="text-xs text-muted-foreground">
                                {new Date(submission.submission_date).toLocaleDateString()}
                              </p>
                            </div>
                            <Badge className={getSubmissionStatusColor(submission.status)}>
                              {submission.status}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="text-center py-4 text-muted-foreground">
                        <Clock className="w-8 h-8 mx-auto mb-2" />
                        <p className="text-sm">No URL submissions yet</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="keywords" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Keyword Research</h3>
                <Button variant="outline" size="sm" onClick={() => setShowKeywordResearch(true)}>
                  <Search className="w-4 h-4 mr-2" />
                  Research Keywords
                </Button>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Database className="w-5 h-5" />
                    Keyword Analysis Results
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {keywordData.length > 0 ? (
                    <div className="overflow-x-auto">
                      <table className="w-full">
                        <thead>
                          <tr className="border-b">
                            <th className="text-left p-2">Keyword</th>
                            <th className="text-right p-2">Search Volume</th>
                            <th className="text-center p-2">Competition</th>
                            <th className="text-right p-2">CPC</th>
                            <th className="text-right p-2">Difficulty</th>
                          </tr>
                        </thead>
                        <tbody>
                          {keywordData.map((keyword, index) => (
                            <tr key={index} className="border-b">
                              <td className="p-2 font-medium">{keyword.keyword}</td>
                              <td className="p-2 text-right">{formatNumber(keyword.search_volume)}</td>
                              <td className="p-2 text-center">
                                <Badge variant={keyword.competition === 'High' ? 'destructive' : keyword.competition === 'Medium' ? 'default' : 'secondary'}>
                                  {keyword.competition}
                                </Badge>
                              </td>
                              <td className="p-2 text-right">${keyword.cpc.toFixed(2)}</td>
                              <td className="p-2 text-right">{keyword.difficulty}/100</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      <Database className="w-12 h-12 mx-auto mb-2" />
                      <p>Use the research tool to analyze keywords</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="crawl-stats" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Crawl Statistics</h3>
                <Button variant="outline" size="sm" onClick={fetchCrawlStats} disabled={isLoading}>
                  <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </div>

              {crawlStatsData ? (
                <div className="grid gap-4">
                  <div className="grid gap-4 md:grid-cols-3">
                    <MetricsCard
                      title="Pages Crawled"
                      value={formatNumber(crawlStatsData.pages_crawled)}
                      icon={Activity}
                      color="blue"
                    />
                    <MetricsCard
                      title="Pages in Index"
                      value={formatNumber(crawlStatsData.pages_in_index)}
                      icon={Database}
                      color="green"
                    />
                    <MetricsCard
                      title="Crawl Errors"
                      value={formatNumber(crawlStatsData.crawl_errors)}
                      icon={Bug}
                      color="red"
                    />
                  </div>

                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Bug className="w-5 h-5" />
                        Crawl Issues
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      {crawlStatsData.crawl_issues && crawlStatsData.crawl_issues.length > 0 ? (
                        <div className="space-y-3">
                          {crawlStatsData.crawl_issues.map((issue, index) => (
                            <div key={index} className="flex items-center justify-between p-3 rounded-lg border">
                              <div>
                                <p className="font-medium">{issue.issue_type}</p>
                                <p className="text-sm text-muted-foreground">
                                  {issue.count} affected pages
                                </p>
                              </div>
                              <div className="text-right">
                                <Badge className={getCrawlIssueColor(issue.severity)}>
                                  {issue.severity}
                                </Badge>
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-center py-8 text-muted-foreground">
                          <CheckCircle className="w-12 h-12 mx-auto mb-2 text-green-500" />
                          <p>No crawl issues found</p>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </div>
              ) : (
                <Card>
                  <CardContent className="py-8 text-center">
                    <Activity className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                    <p className="text-muted-foreground">Click refresh to load crawl statistics</p>
                  </CardContent>
                </Card>
              )}
            </TabsContent>

            <TabsContent value="sitemaps" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Sitemap Management</h3>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" onClick={() => setShowAddSitemap(true)}>
                    <Plus className="w-4 h-4 mr-2" />
                    Add Sitemap
                  </Button>
                  <Button variant="outline" size="sm" onClick={fetchSitemaps} disabled={isLoading}>
                    <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                    Refresh
                  </Button>
                </div>
              </div>

              <div className="grid gap-4">
                {sitemapsData.length > 0 ? (
                  sitemapsData.map((sitemap, index) => (
                    <Card key={index}>
                      <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <div className="p-2 bg-green-50 rounded-lg">
                              <FileText className="w-5 h-5 text-green-600" />
                            </div>
                            <div>
                              <h4 className="font-medium">{sitemap.path}</h4>
                              <p className="text-sm text-muted-foreground">
                                Last submitted: {new Date(sitemap.last_submitted).toLocaleDateString()}
                              </p>
                              <p className="text-xs text-muted-foreground mt-1">
                                {formatNumber(sitemap.urls_indexed)} / {formatNumber(sitemap.urls_submitted)} URLs indexed
                              </p>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <Badge className={getSitemapStatusColor(sitemap.status)}>
                              {sitemap.status}
                            </Badge>
                            {sitemap.errors > 0 && (
                              <Badge variant="destructive" className="flex items-center gap-1">
                                <XCircle className="w-3 h-3" />
                                {sitemap.errors} errors
                              </Badge>
                            )}
                            {sitemap.warnings > 0 && (
                              <Badge variant="outline" className="flex items-center gap-1">
                                <AlertTriangle className="w-3 h-3" />
                                {sitemap.warnings} warnings
                              </Badge>
                            )}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))
                ) : (
                  <Card>
                    <CardContent className="py-8 text-center">
                      <FileText className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                      <p className="text-muted-foreground">No sitemaps found. Add your first sitemap to help Bing crawl your site.</p>
                    </CardContent>
                  </Card>
                )}
              </div>
            </TabsContent>

            <TabsContent value="block-urls" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Block URLs from Search</h3>
                <Button variant="outline" size="sm" onClick={() => setShowBlockUrls(true)}>
                  <Ban className="w-4 h-4 mr-2" />
                  Block URLs
                </Button>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Ban className="w-5 h-5" />
                    Blocked URLs
                  </CardTitle>
                  <CardDescription>
                    URLs blocked from appearing in Bing search results
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {blockedUrls.length > 0 ? (
                    <div className="space-y-2">
                      {blockedUrls.map((url, index) => (
                        <div key={index} className="flex items-center justify-between p-3 rounded-lg border">
                          <div className="flex-1 min-w-0">
                            <p className="font-medium truncate">{url}</p>
                            <p className="text-sm text-muted-foreground">
                              Blocked from search results
                            </p>
                          </div>
                          <Badge variant="destructive" className="flex items-center gap-1">
                            <Ban className="w-3 h-3" />
                            Blocked
                          </Badge>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      <Ban className="w-12 h-12 mx-auto mb-2" />
                      <p>No URLs are currently blocked</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* URL Submission Dialog */}
      <Dialog open={showUrlSubmission} onOpenChange={setShowUrlSubmission}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Submit URLs to Bing</DialogTitle>
            <DialogDescription>
              Submit URLs for crawling and indexing on Bing (Daily limit: 10,000 URLs)
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="urls-to-submit">URLs to Submit</Label>
              <Textarea
                id="urls-to-submit"
                value={urlsToSubmit}
                onChange={(e) => setUrlsToSubmit(e.target.value)}
                placeholder="Enter URLs, one per line&#10;https://example.com/page1&#10;https://example.com/page2"
                className="min-h-[200px]"
              />
              <p className="text-xs text-muted-foreground">
                Enter one URL per line. Maximum 100 URLs per submission.
              </p>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowUrlSubmission(false)}>
              Cancel
            </Button>
            <Button onClick={submitUrls} disabled={isLoading || !urlsToSubmit.trim()}>
              {isLoading ? (
                <>
                  <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  Submitting...
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4 mr-2" />
                  Submit URLs
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Keyword Research Dialog */}
      <Dialog open={showKeywordResearch} onOpenChange={setShowKeywordResearch}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Keyword Research</DialogTitle>
            <DialogDescription>
              Research keywords to find search volume, competition, and cost data
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="keyword-query">Keyword to Research</Label>
              <Input
                id="keyword-query"
                value={keywordQuery}
                onChange={(e) => setKeywordQuery(e.target.value)}
                placeholder="e.g., digital marketing"
              />
              <p className="text-xs text-muted-foreground">
                Enter a keyword phrase to get detailed research data
              </p>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowKeywordResearch(false)}>
              Cancel
            </Button>
            <Button onClick={fetchKeywordResearch} disabled={isLoading || !keywordQuery.trim()}>
              {isLoading ? (
                <>
                  <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  Researching...
                </>
              ) : (
                <>
                  <Search className="w-4 h-4 mr-2" />
                  Research Keyword
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Add Sitemap Dialog */}
      <Dialog open={showAddSitemap} onOpenChange={setShowAddSitemap}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Sitemap</DialogTitle>
            <DialogDescription>
              Submit a sitemap for {selectedSite}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="sitemap-url">Sitemap URL</Label>
              <Input
                id="sitemap-url"
                value={newSitemapUrl}
                onChange={(e) => setNewSitemapUrl(e.target.value)}
                placeholder="sitemap.xml"
              />
              <p className="text-xs text-muted-foreground">
                Enter the path relative to your domain (e.g., "sitemap.xml" or "sitemaps/products.xml")
              </p>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowAddSitemap(false)}>
              Cancel
            </Button>
            <Button onClick={addSitemap} disabled={isLoading || !newSitemapUrl}>
              {isLoading ? (
                <>
                  <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  Adding...
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4 mr-2" />
                  Add Sitemap
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Block URLs Dialog */}
      <Dialog open={showBlockUrls} onOpenChange={setShowBlockUrls}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Block URLs from Search</DialogTitle>
            <DialogDescription>
              Block specific URLs from appearing in Bing search results
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="urls-to-block">URLs to Block</Label>
              <Textarea
                id="urls-to-block"
                value={urlsToBlock}
                onChange={(e) => setUrlsToBlock(e.target.value)}
                placeholder="Enter URLs to block, one per line&#10;https://example.com/private-page&#10;https://example.com/test-page"
                className="min-h-[150px]"
              />
              <p className="text-xs text-muted-foreground">
                Enter one URL per line. These URLs will be removed from Bing search results.
              </p>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowBlockUrls(false)}>
              Cancel
            </Button>
            <Button onClick={blockUrls} disabled={isLoading || !urlsToBlock.trim()} variant="destructive">
              {isLoading ? (
                <>
                  <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  Blocking...
                </>
              ) : (
                <>
                  <Ban className="w-4 h-4 mr-2" />
                  Block URLs
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}