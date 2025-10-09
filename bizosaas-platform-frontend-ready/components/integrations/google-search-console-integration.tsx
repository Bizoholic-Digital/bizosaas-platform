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
  Gauge
} from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'

interface GoogleSearchConsoleProperty {
  property_url: string
  property_type: 'URL_PREFIX' | 'DOMAIN'
  permission_level: 'siteOwner' | 'siteFullUser' | 'siteRestrictedUser' | 'siteUnverifiedUser'
  verified: boolean
  verification_method?: string
  site_url: string
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

interface IndexCoverageIssue {
  category: 'error' | 'warning' | 'excluded' | 'valid'
  detail: string
  count: number
  examples: string[]
}

interface CoreWebVitalsData {
  url: string
  origin_fallback: boolean
  loading_experience: {
    id: string
    metrics: {
      CUMULATIVE_LAYOUT_SHIFT_SCORE: {
        percentile: number
        distributions: Array<{
          min: number
          max?: number
          proportion: number
        }>
        category: 'FAST' | 'AVERAGE' | 'SLOW'
      }
      FIRST_CONTENTFUL_PAINT_MS: {
        percentile: number
        distributions: Array<{
          min: number
          max?: number
          proportion: number
        }>
        category: 'FAST' | 'AVERAGE' | 'SLOW'
      }
      FIRST_INPUT_DELAY_MS: {
        percentile: number
        distributions: Array<{
          min: number
          max?: number
          proportion: number
        }>
        category: 'FAST' | 'AVERAGE' | 'SLOW'
      }
    }
  }
}

interface SitemapData {
  path: string
  lastSubmitted: string
  isPending: boolean
  isSitemapsIndex: boolean
  type: 'sitemap' | 'robotsTxt'
  warnings: number
  errors: number
  contents?: Array<{
    type: string
    submitted: number
    indexed: number
  }>
}

interface URLInspectionData {
  url: string
  index_status_result: {
    coverage_state: 'Submitted and indexed' | 'Duplicate without user-selected canonical' | 'Crawled - currently not indexed' | 'Discovered - currently not indexed' | 'Page with redirect' | 'Submitted URL not found (404)' | 'Submitted URL seems to be Soft 404' | 'Submitted URL returned 403' | 'Submitted URL returned 401' | 'Submitted URL blocked by robots.txt'
    page_fetch_state: 'Successful' | 'Soft 404' | 'Page not found (404)' | 'Access denied (401)' | 'Access forbidden (403)' | 'Server error (5xx)' | 'Redirect error' | 'Access blocked by robots.txt' | 'Internal error'
    google_canonical: string
    user_canonical?: string
    referring_urls: string[]
    crawl_date: string
    index_date?: string
  }
  mobile_usability_result?: {
    verdict: 'PASS' | 'PARTIAL' | 'FAIL' | 'NEUTRAL'
    issues: Array<{
      rule: string
      severity: 'ERROR' | 'WARNING'
    }>
  }
}

interface GoogleSearchConsoleIntegrationProps {
  tenantId?: string
  onUpdate?: (status: string) => void
}

export function GoogleSearchConsoleIntegration({ tenantId = "demo", onUpdate }: GoogleSearchConsoleIntegrationProps) {
  const [isConnected, setIsConnected] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [properties, setProperties] = useState<GoogleSearchConsoleProperty[]>([])
  const [selectedProperty, setSelectedProperty] = useState<string>("")
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected' | 'error'>('disconnected')
  const [authUrl, setAuthUrl] = useState<string>("")
  const [error, setError] = useState<string>("")
  
  // Data states
  const [searchPerformanceData, setSearchPerformanceData] = useState<SearchPerformanceData[]>([])
  const [indexCoverageData, setIndexCoverageData] = useState<IndexCoverageIssue[]>([])
  const [coreWebVitalsData, setCoreWebVitalsData] = useState<CoreWebVitalsData | null>(null)
  const [sitemapsData, setSitemapsData] = useState<SitemapData[]>([])
  const [urlInspectionData, setUrlInspectionData] = useState<URLInspectionData | null>(null)
  
  // UI states
  const [activeTab, setActiveTab] = useState('connection')
  const [dateRange, setDateRange] = useState('last_7_days')
  const [filterDimension, setFilterDimension] = useState('query')
  const [inspectionUrl, setInspectionUrl] = useState('')
  const [newSitemapUrl, setNewSitemapUrl] = useState('')
  const [showAddProperty, setShowAddProperty] = useState(false)
  const [showAddSitemap, setShowAddSitemap] = useState(false)
  const [showUrlInspection, setShowUrlInspection] = useState(false)

  // Check existing connection status
  useEffect(() => {
    checkConnectionStatus()
  }, [])

  const checkConnectionStatus = async () => {
    try {
      const response = await fetch(`/api/brain/integrations/google-search-console?tenant_id=${tenantId}`)
      if (response.ok) {
        const data = await response.json()
        setIsConnected(data.status === 'connected')
        setConnectionStatus(data.status === 'connected' ? 'connected' : 'disconnected')
        if (data.properties) {
          setProperties(data.properties)
          if (data.properties.length > 0 && !selectedProperty) {
            setSelectedProperty(data.properties[0].property_url)
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
      const response = await fetch('/api/brain/integrations/google-search-console/oauth/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          redirect_uri: `${window.location.origin}/integrations/google-search-console/callback`,
          scopes: ['https://www.googleapis.com/auth/webmasters.readonly']
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setAuthUrl(data.auth_url)
        
        const authWindow = window.open(
          data.auth_url,
          'google-search-console-auth',
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

  const checkOAuthCompletion = async () => {
    try {
      const response = await fetch(`/api/brain/integrations/google-search-console/oauth/status?tenant_id=${tenantId}`)
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'completed') {
          setIsConnected(true)
          setConnectionStatus('connected')
          setProperties(data.properties || [])
          if (data.properties?.length > 0) {
            setSelectedProperty(data.properties[0].property_url)
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
    if (!selectedProperty) return

    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/google-search-console/search-analytics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          site_url: selectedProperty,
          start_date: getDateRangeStart(dateRange),
          end_date: new Date().toISOString().split('T')[0],
          dimensions: ['query', 'page'],
          row_limit: 100
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setSearchPerformanceData(data.rows || [])
      } else {
        throw new Error('Failed to fetch search performance data')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to fetch search performance data')
    } finally {
      setIsLoading(false)
    }
  }

  const fetchIndexCoverage = async () => {
    if (!selectedProperty) return

    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/google-search-console/index-coverage', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          site_url: selectedProperty
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setIndexCoverageData(data.coverage_data || [])
      } else {
        throw new Error('Failed to fetch index coverage data')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to fetch index coverage data')
    } finally {
      setIsLoading(false)
    }
  }

  const fetchCoreWebVitals = async () => {
    if (!selectedProperty) return

    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/google-search-console/core-web-vitals', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          origin_url: selectedProperty
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setCoreWebVitalsData(data.vitals_data)
      } else {
        throw new Error('Failed to fetch Core Web Vitals data')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to fetch Core Web Vitals data')
    } finally {
      setIsLoading(false)
    }
  }

  const fetchSitemaps = async () => {
    if (!selectedProperty) return

    setIsLoading(true)
    try {
      const response = await fetch(`/api/brain/integrations/google-search-console/sitemaps?tenant_id=${tenantId}&site_url=${encodeURIComponent(selectedProperty)}`)
      
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

  const inspectURL = async () => {
    if (!selectedProperty || !inspectionUrl) return

    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/google-search-console/url-inspection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          site_url: selectedProperty,
          inspection_url: inspectionUrl
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setUrlInspectionData(data.inspection_result)
        setShowUrlInspection(false)
        setInspectionUrl('')
      } else {
        throw new Error('Failed to inspect URL')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to inspect URL')
    } finally {
      setIsLoading(false)
    }
  }

  const addSitemap = async () => {
    if (!selectedProperty || !newSitemapUrl) return

    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/google-search-console/sitemaps', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          site_url: selectedProperty,
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

  const deleteSitemap = async (sitemapPath: string) => {
    if (!selectedProperty) return

    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/google-search-console/sitemaps', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          site_url: selectedProperty,
          sitemap_path: sitemapPath
        }),
      })

      if (response.ok) {
        fetchSitemaps()
      } else {
        throw new Error('Failed to delete sitemap')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to delete sitemap')
    } finally {
      setIsLoading(false)
    }
  }

  const disconnectIntegration = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/brain/integrations/google-search-console/disconnect', {
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
        setSearchPerformanceData([])
        setIndexCoverageData([])
        setCoreWebVitalsData(null)
        setSitemapsData([])
        setUrlInspectionData(null)
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
      const response = await fetch('/api/brain/integrations/google-search-console/test', {
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

  const getCoverageStatusColor = (category: string) => {
    switch (category) {
      case 'valid': return 'text-green-600 bg-green-50'
      case 'error': return 'text-red-600 bg-red-50'
      case 'warning': return 'text-yellow-600 bg-yellow-50'
      case 'excluded': return 'text-gray-600 bg-gray-50'
      default: return 'text-blue-600 bg-blue-50'
    }
  }

  const getWebVitalCategory = (category: string) => {
    switch (category) {
      case 'FAST': return 'text-green-600 bg-green-50'
      case 'AVERAGE': return 'text-yellow-600 bg-yellow-50'
      case 'SLOW': return 'text-red-600 bg-red-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  // Effect to fetch data when property changes
  useEffect(() => {
    if (selectedProperty && isConnected) {
      if (activeTab === 'analytics') {
        fetchSearchPerformanceData()
      } else if (activeTab === 'seo-tools') {
        fetchIndexCoverage()
      } else if (activeTab === 'sitemaps') {
        fetchSitemaps()
      } else if (activeTab === 'web-vitals') {
        fetchCoreWebVitals()
      }
    }
  }, [selectedProperty, isConnected, activeTab, dateRange])

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                <Search className="w-6 h-6 text-white" />
              </div>
              <div>
                <CardTitle>Google Search Console</CardTitle>
                <CardDescription>Monitor search performance, SEO health, and site indexing status</CardDescription>
              </div>
            </div>
            <ConnectionStatusBadge />
          </div>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList>
              <TabsTrigger value="connection">Connection</TabsTrigger>
              <TabsTrigger value="properties" disabled={!isConnected}>Properties</TabsTrigger>
              <TabsTrigger value="analytics" disabled={!isConnected || !selectedProperty}>Analytics</TabsTrigger>
              <TabsTrigger value="seo-tools" disabled={!isConnected || !selectedProperty}>SEO Tools</TabsTrigger>
              <TabsTrigger value="sitemaps" disabled={!isConnected || !selectedProperty}>Sitemaps</TabsTrigger>
              <TabsTrigger value="web-vitals" disabled={!isConnected || !selectedProperty}>Web Vitals</TabsTrigger>
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
                    <Search className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
                    <h3 className="text-lg font-medium mb-2">Connect Google Search Console</h3>
                    <p className="text-muted-foreground mb-6">
                      Monitor your website's search performance and SEO health with comprehensive analytics
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
                        Search performance analytics and keyword insights
                      </li>
                      <li className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        Index coverage monitoring and SEO issue detection
                      </li>
                      <li className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        Core Web Vitals performance tracking
                      </li>
                      <li className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        Sitemap management and URL inspection tools
                      </li>
                    </ul>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="text-center py-4">
                    <CheckCircle2 className="w-16 h-16 mx-auto text-green-500 mb-4" />
                    <h3 className="text-lg font-medium mb-2">Google Search Console Connected!</h3>
                    <p className="text-muted-foreground mb-4">
                      Your Google Search Console is connected and ready to provide search insights.
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

            <TabsContent value="properties" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Search Console Properties</h3>
                <Button variant="outline" size="sm" onClick={() => setShowAddProperty(true)}>
                  <Plus className="w-4 h-4 mr-2" />
                  Add Property
                </Button>
              </div>
              
              <div className="grid gap-4">
                {properties.map((property) => (
                  <Card key={property.property_url} className={`cursor-pointer transition-colors ${
                    selectedProperty === property.property_url ? 'ring-2 ring-primary' : ''
                  }`} onClick={() => setSelectedProperty(property.property_url)}>
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className="p-2 bg-blue-50 rounded-lg">
                            {property.property_type === 'DOMAIN' ? <Globe className="w-5 h-5 text-blue-600" /> : <Link className="w-5 h-5 text-blue-600" />}
                          </div>
                          <div>
                            <h4 className="font-medium">{property.site_url}</h4>
                            <p className="text-sm text-muted-foreground">
                              {property.property_type} Property • {property.permission_level}
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <Badge variant={property.verified ? "default" : "secondary"} className="flex items-center gap-1">
                            {property.verified ? <CheckCircle className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
                            {property.verified ? "Verified" : "Unverified"}
                          </Badge>
                          {property.verification_method && (
                            <p className="text-xs text-muted-foreground mt-1">
                              Via {property.verification_method}
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
                    change="+12.5%"
                  />
                  <MetricsCard
                    title="Total Impressions"
                    value={formatNumber(searchPerformanceData.reduce((sum, row) => sum + row.impressions, 0))}
                    icon={Eye}
                    color="green"
                    change="+8.3%"
                  />
                  <MetricsCard
                    title="Average CTR"
                    value={`${(searchPerformanceData.reduce((sum, row) => sum + row.ctr, 0) / searchPerformanceData.length).toFixed(2)}%`}
                    icon={Target}
                    color="purple"
                    change="+2.1%"
                  />
                  <MetricsCard
                    title="Average Position"
                    value={(searchPerformanceData.reduce((sum, row) => sum + row.position, 0) / searchPerformanceData.length).toFixed(1)}
                    icon={TrendingUp}
                    color="orange"
                    change="-1.2"
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

            <TabsContent value="seo-tools" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">SEO Tools & Index Coverage</h3>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" onClick={() => setShowUrlInspection(true)}>
                    <Search className="w-4 h-4 mr-2" />
                    Inspect URL
                  </Button>
                  <Button variant="outline" size="sm" onClick={fetchIndexCoverage} disabled={isLoading}>
                    <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                    Refresh
                  </Button>
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Shield className="w-5 h-5" />
                      Index Coverage Status
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    {indexCoverageData.length > 0 ? (
                      <div className="space-y-3">
                        {indexCoverageData.map((issue, index) => (
                          <div key={index} className="flex items-center justify-between p-3 rounded-lg border">
                            <div>
                              <p className="font-medium capitalize">{issue.category}</p>
                              <p className="text-sm text-muted-foreground">{issue.detail}</p>
                            </div>
                            <div className="text-right">
                              <Badge className={getCoverageStatusColor(issue.category)}>
                                {formatNumber(issue.count)}
                              </Badge>
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="text-center py-8 text-muted-foreground">
                        <Shield className="w-12 h-12 mx-auto mb-2" />
                        <p>No coverage data available</p>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {urlInspectionData && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Search className="w-5 h-5" />
                        URL Inspection Results
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div>
                        <Label className="text-sm font-medium">Coverage State</Label>
                        <p className="text-sm">{urlInspectionData.index_status_result.coverage_state}</p>
                      </div>
                      <div>
                        <Label className="text-sm font-medium">Page Fetch State</Label>
                        <p className="text-sm">{urlInspectionData.index_status_result.page_fetch_state}</p>
                      </div>
                      <div>
                        <Label className="text-sm font-medium">Google Canonical</Label>
                        <p className="text-sm text-blue-600 break-all">{urlInspectionData.index_status_result.google_canonical}</p>
                      </div>
                      {urlInspectionData.index_status_result.crawl_date && (
                        <div>
                          <Label className="text-sm font-medium">Last Crawled</Label>
                          <p className="text-sm">{new Date(urlInspectionData.index_status_result.crawl_date).toLocaleString()}</p>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                )}
              </div>
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
                                Last submitted: {new Date(sitemap.lastSubmitted).toLocaleDateString()}
                              </p>
                              {sitemap.contents && sitemap.contents.length > 0 && (
                                <div className="mt-2 text-xs text-muted-foreground">
                                  {sitemap.contents.map((content, idx) => (
                                    <span key={idx} className="mr-4">
                                      {content.type}: {formatNumber(content.submitted)} submitted, {formatNumber(content.indexed)} indexed
                                    </span>
                                  ))}
                                </div>
                              )}
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
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
                            {sitemap.isPending && (
                              <Badge variant="outline" className="flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                Pending
                              </Badge>
                            )}
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => deleteSitemap(sitemap.path)}
                              className="text-red-600"
                            >
                              Remove
                            </Button>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))
                ) : (
                  <Card>
                    <CardContent className="py-8 text-center">
                      <FileText className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                      <p className="text-muted-foreground">No sitemaps found. Add your first sitemap to help Google crawl your site.</p>
                    </CardContent>
                  </Card>
                )}
              </div>
            </TabsContent>

            <TabsContent value="web-vitals" className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Core Web Vitals Performance</h3>
                <Button variant="outline" size="sm" onClick={fetchCoreWebVitals} disabled={isLoading}>
                  <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </div>

              {coreWebVitalsData ? (
                <div className="grid gap-4 md:grid-cols-3">
                  <Card>
                    <CardContent className="p-4">
                      <div className="text-center">
                        <div className="mb-2">
                          <Gauge className="w-8 h-8 mx-auto text-blue-600" />
                        </div>
                        <h4 className="font-medium mb-1">Cumulative Layout Shift</h4>
                        <p className="text-2xl font-bold mb-2">
                          {coreWebVitalsData.loading_experience.metrics.CUMULATIVE_LAYOUT_SHIFT_SCORE.percentile.toFixed(3)}
                        </p>
                        <Badge className={getWebVitalCategory(coreWebVitalsData.loading_experience.metrics.CUMULATIVE_LAYOUT_SHIFT_SCORE.category)}>
                          {coreWebVitalsData.loading_experience.metrics.CUMULATIVE_LAYOUT_SHIFT_SCORE.category}
                        </Badge>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardContent className="p-4">
                      <div className="text-center">
                        <div className="mb-2">
                          <Zap className="w-8 h-8 mx-auto text-green-600" />
                        </div>
                        <h4 className="font-medium mb-1">First Contentful Paint</h4>
                        <p className="text-2xl font-bold mb-2">
                          {Math.round(coreWebVitalsData.loading_experience.metrics.FIRST_CONTENTFUL_PAINT_MS.percentile / 1000 * 10) / 10}s
                        </p>
                        <Badge className={getWebVitalCategory(coreWebVitalsData.loading_experience.metrics.FIRST_CONTENTFUL_PAINT_MS.category)}>
                          {coreWebVitalsData.loading_experience.metrics.FIRST_CONTENTFUL_PAINT_MS.category}
                        </Badge>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardContent className="p-4">
                      <div className="text-center">
                        <div className="mb-2">
                          <MousePointer className="w-8 h-8 mx-auto text-purple-600" />
                        </div>
                        <h4 className="font-medium mb-1">First Input Delay</h4>
                        <p className="text-2xl font-bold mb-2">
                          {coreWebVitalsData.loading_experience.metrics.FIRST_INPUT_DELAY_MS.percentile}ms
                        </p>
                        <Badge className={getWebVitalCategory(coreWebVitalsData.loading_experience.metrics.FIRST_INPUT_DELAY_MS.category)}>
                          {coreWebVitalsData.loading_experience.metrics.FIRST_INPUT_DELAY_MS.category}
                        </Badge>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              ) : (
                <Card>
                  <CardContent className="py-8 text-center">
                    <Activity className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                    <p className="text-muted-foreground">Core Web Vitals data will appear here once available.</p>
                  </CardContent>
                </Card>
              )}
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Add Property Dialog */}
      <Dialog open={showAddProperty} onOpenChange={setShowAddProperty}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New Property</DialogTitle>
            <DialogDescription>
              Add a new property to your Google Search Console account
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="property-url">Property URL</Label>
              <Input
                id="property-url"
                placeholder="https://example.com/"
                disabled
              />
              <p className="text-xs text-muted-foreground">
                Properties must be added through Google Search Console first.
              </p>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowAddProperty(false)}>
              Cancel
            </Button>
            <Button variant="outline" asChild>
              <a href="https://search.google.com/search-console" target="_blank" rel="noopener noreferrer">
                <ExternalLink className="w-4 h-4 mr-2" />
                Open Search Console
              </a>
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
              Submit a sitemap for {selectedProperty}
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

      {/* URL Inspection Dialog */}
      <Dialog open={showUrlInspection} onOpenChange={setShowUrlInspection}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>URL Inspection Tool</DialogTitle>
            <DialogDescription>
              Inspect any URL on {selectedProperty} for indexing and mobile usability issues
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="inspection-url">URL to Inspect</Label>
              <Input
                id="inspection-url"
                value={inspectionUrl}
                onChange={(e) => setInspectionUrl(e.target.value)}
                placeholder="https://example.com/page-to-inspect"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowUrlInspection(false)}>
              Cancel
            </Button>
            <Button onClick={inspectURL} disabled={isLoading || !inspectionUrl}>
              {isLoading ? (
                <>
                  <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  Inspecting...
                </>
              ) : (
                <>
                  <Search className="w-4 h-4 mr-2" />
                  Inspect URL
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}