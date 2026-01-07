'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Progress } from '@/components/ui/progress'
import { 
  Users, Database, TrendingUp, UserPlus, Phone, Mail, 
  MessageSquare, Calendar, Target, BarChart3, Filter,
  RefreshCw, CheckCircle, Clock, AlertTriangle, Star,
  ArrowUpRight, ArrowDownRight, Plus, Search, Settings,
  Activity, Award, Zap
} from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

interface Lead {
  id: string
  first_name: string
  last_name: string
  email: string
  phone: string
  company: string
  job_title: string
  status: string
  priority: string
  score: number
  score_factors: Record<string, number>
  source: string
  assigned_to: string | null
  budget: number | null
  timeline: string
  decision_maker: boolean
  pain_points: string
  requirements: string
  created_at: string
  last_contact_date: string | null
  next_follow_up: string | null
}

interface CrmStats {
  leads: {
    total: number
    new_this_month: number
    qualified_this_month: number
    converted_this_month: number
    conversion_rate: number
    average_score: number
  }
  pipeline: {
    total_value: number
    average_deal_size: number
    pipeline_velocity: number
    win_rate: number
  }
  activities: {
    calls_this_week: number
    emails_sent: number
    meetings_scheduled: number
    follow_ups_due: number
  }
  performance: {
    top_sources: Array<{
      name: string
      leads: number
      conversion_rate: number
    }>
    team_performance: Array<{
      name: string
      leads: number
      conversion_rate: number
    }>
  }
  integration_insights: {
    google_ads_performance: {
      leads_generated: number
      total_spend: number
      cost_per_lead: number
      roi: number
    }
    google_analytics_insights: {
      website_conversions: number
      top_converting_pages: Array<{
        page: string
        conversions: number
      }>
    }
  }
}

export function DjangoCrmIntegration() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [leads, setLeads] = useState<Lead[]>([])
  const [stats, setStats] = useState<CrmStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    status: '',
    assigned_to: '',
    search: ''
  })

  useEffect(() => {
    loadCrmData()
  }, [])

  const loadCrmData = async () => {
    try {
      setLoading(true)
      
      // Load dashboard stats
      const statsResponse = await fetch('/api/brain/crm/dashboard/stats?tenant_id=demo')
      const statsData = await statsResponse.json()
      
      if (statsData.success) {
        setStats(statsData.stats)
      }
      
      // Load leads
      const leadsResponse = await fetch('/api/brain/crm/leads?tenant_id=demo&limit=20')
      const leadsData = await leadsResponse.json()
      
      if (leadsData.success) {
        setLeads(leadsData.leads)
      }
      
    } catch (error) {
      console.error('Error loading CRM data:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredLeads = leads.filter(lead => {
    const matchesStatus = !filters.status || lead.status === filters.status
    const matchesAssignee = !filters.assigned_to || lead.assigned_to === filters.assigned_to
    const matchesSearch = !filters.search || 
      lead.first_name.toLowerCase().includes(filters.search.toLowerCase()) ||
      lead.last_name.toLowerCase().includes(filters.search.toLowerCase()) ||
      lead.company.toLowerCase().includes(filters.search.toLowerCase()) ||
      lead.email.toLowerCase().includes(filters.search.toLowerCase())
    
    return matchesStatus && matchesAssignee && matchesSearch
  })

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50'
    if (score >= 60) return 'text-blue-600 bg-blue-50'
    if (score >= 40) return 'text-yellow-600 bg-yellow-50'
    return 'text-red-600 bg-red-50'
  }

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      'new': { variant: 'secondary' as const, icon: Plus },
      'contacted': { variant: 'default' as const, icon: Phone },
      'qualified': { variant: 'default' as const, icon: CheckCircle },
      'proposal': { variant: 'default' as const, icon: Target },
      'negotiation': { variant: 'default' as const, icon: MessageSquare },
      'converted': { variant: 'default' as const, icon: Award },
      'lost': { variant: 'destructive' as const, icon: ArrowDownRight },
      'unresponsive': { variant: 'secondary' as const, icon: Clock }
    }
    
    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.new
    const Icon = config.icon
    
    return (
      <Badge variant={config.variant} className="capitalize">
        <Icon className="w-3 h-3 mr-1" />
        {status}
      </Badge>
    )
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      notation: 'compact',
      maximumFractionDigits: 1
    }).format(amount)
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-3">
          <Database className="h-6 w-6 text-blue-600" />
          <div>
            <h3 className="font-semibold text-lg">Django CRM Integration</h3>
            <p className="text-sm text-muted-foreground">Loading CRM data...</p>
          </div>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <Card key={i}>
              <CardHeader className="animate-pulse">
                <div className="h-4 bg-gray-200 rounded"></div>
                <div className="h-8 bg-gray-200 rounded"></div>
              </CardHeader>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-start gap-3">
        <Database className="h-6 w-6 text-blue-600 mt-1" />
        <div className="flex-1">
          <h3 className="font-semibold text-lg">Django CRM Integration</h3>
          <p className="text-sm text-muted-foreground">
            AI-powered lead management with multi-tenant architecture
          </p>
          <div className="flex items-center gap-2 mt-2">
            <Badge variant="default" className="bg-green-100 text-green-700">
              <CheckCircle className="w-3 h-3 mr-1" />
              Connected
            </Badge>
            <Badge variant="secondary">
              Multi-tenant
            </Badge>
            <Badge variant="secondary">
              AI Scoring
            </Badge>
          </div>
        </div>
        <Button variant="outline" size="sm">
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="dashboard">
            <BarChart3 className="w-4 h-4 mr-2" />
            Dashboard
          </TabsTrigger>
          <TabsTrigger value="leads">
            <Users className="w-4 h-4 mr-2" />
            Leads ({leads.length})
          </TabsTrigger>
          <TabsTrigger value="insights">
            <TrendingUp className="w-4 h-4 mr-2" />
            Insights
          </TabsTrigger>
          <TabsTrigger value="settings">
            <Settings className="w-4 h-4 mr-2" />
            Settings
          </TabsTrigger>
        </TabsList>

        <TabsContent value="dashboard" className="space-y-6">
          {stats && (
            <>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Total Leads</CardTitle>
                    <Users className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{stats.leads.total.toLocaleString()}</div>
                    <p className="text-xs text-muted-foreground">
                      +{stats.leads.new_this_month} this month
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Pipeline Value</CardTitle>
                    <Target className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{formatCurrency(stats.pipeline.total_value)}</div>
                    <p className="text-xs text-muted-foreground">
                      Avg: {formatCurrency(stats.pipeline.average_deal_size)}
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
                    <TrendingUp className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{stats.leads.conversion_rate}%</div>
                    <p className="text-xs text-muted-foreground">
                      {stats.leads.converted_this_month} conversions this month
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Average Score</CardTitle>
                    <Star className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{stats.leads.average_score}</div>
                    <p className="text-xs text-muted-foreground">
                      AI-powered scoring
                    </p>
                  </CardContent>
                </Card>
              </div>

              <div className="grid gap-6 md:grid-cols-2">
                <Card>
                  <CardHeader>
                    <CardTitle>Top Lead Sources</CardTitle>
                    <CardDescription>Performance by acquisition channel</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {stats.performance.top_sources.map((source, index) => (
                        <div key={index} className="flex items-center justify-between">
                          <div className="space-y-1">
                            <p className="text-sm font-medium">{source.name}</p>
                            <p className="text-xs text-muted-foreground">
                              {source.leads} leads • {source.conversion_rate}% conversion
                            </p>
                          </div>
                          <Badge variant="secondary">
                            {source.conversion_rate}%
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Team Performance</CardTitle>
                    <CardDescription>Individual conversion rates</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {stats.performance.team_performance.map((member, index) => (
                        <div key={index} className="flex items-center justify-between">
                          <div className="space-y-1">
                            <p className="text-sm font-medium">{member.name}</p>
                            <p className="text-xs text-muted-foreground">
                              {member.leads} leads managed
                            </p>
                          </div>
                          <div className="flex items-center gap-2">
                            <Progress 
                              value={member.conversion_rate} 
                              className="w-16 h-2"
                            />
                            <span className="text-sm font-medium">
                              {member.conversion_rate}%
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </>
          )}
        </TabsContent>

        <TabsContent value="leads" className="space-y-4">
          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <Input
                placeholder="Search leads..."
                value={filters.search}
                onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
              />
            </div>
            <Select
              value={filters.status}
              onValueChange={(value) => setFilters(prev => ({ ...prev, status: value }))}
            >
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Statuses</SelectItem>
                <SelectItem value="new">New</SelectItem>
                <SelectItem value="contacted">Contacted</SelectItem>
                <SelectItem value="qualified">Qualified</SelectItem>
                <SelectItem value="proposal">Proposal</SelectItem>
                <SelectItem value="converted">Converted</SelectItem>
                <SelectItem value="lost">Lost</SelectItem>
              </SelectContent>
            </Select>
            <Button>
              <UserPlus className="w-4 h-4 mr-2" />
              Add Lead
            </Button>
          </div>

          {/* Leads List */}
          <div className="space-y-4">
            {filteredLeads.map((lead) => (
              <Card key={lead.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="space-y-2">
                      <div className="flex items-center gap-3">
                        <div>
                          <h4 className="font-semibold">
                            {lead.first_name} {lead.last_name}
                          </h4>
                          <p className="text-sm text-muted-foreground">
                            {lead.job_title} at {lead.company}
                          </p>
                        </div>
                        {getStatusBadge(lead.status)}
                      </div>
                      
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Mail className="w-3 h-3" />
                          {lead.email}
                        </div>
                        {lead.phone && (
                          <div className="flex items-center gap-1">
                            <Phone className="w-3 h-3" />
                            {lead.phone}
                          </div>
                        )}
                        <div className="flex items-center gap-1">
                          <Activity className="w-3 h-3" />
                          {lead.source}
                        </div>
                      </div>

                      {lead.pain_points && (
                        <p className="text-sm text-muted-foreground max-w-2xl">
                          {lead.pain_points}
                        </p>
                      )}
                      
                      <div className="flex items-center gap-4 text-xs text-muted-foreground">
                        <span>Created: {new Date(lead.created_at).toLocaleDateString()}</span>
                        {lead.assigned_to && <span>Assigned to: {lead.assigned_to}</span>}
                        {lead.budget && <span>Budget: {formatCurrency(lead.budget)}</span>}
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      <div className="text-center">
                        <div className={`text-2xl font-bold px-3 py-1 rounded-full ${getScoreColor(lead.score)}`}>
                          {lead.score}
                        </div>
                        <p className="text-xs text-muted-foreground mt-1">AI Score</p>
                      </div>
                      
                      <div className="flex flex-col gap-2">
                        <Button size="sm" variant="outline">
                          <MessageSquare className="w-3 h-3 mr-1" />
                          Contact
                        </Button>
                        <Button size="sm" variant="ghost">
                          <Settings className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}

            {filteredLeads.length === 0 && (
              <Card>
                <CardContent className="py-12 text-center">
                  <Search className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-lg font-medium mb-2">No leads found</h3>
                  <p className="text-muted-foreground">
                    Try adjusting your filters or add a new lead
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </TabsContent>

        <TabsContent value="insights" className="space-y-6">
          {stats && (
            <>
              <Alert>
                <Zap className="h-4 w-4" />
                <AlertDescription>
                  <strong>Integration Insights:</strong> Your connected Google Ads campaigns 
                  have generated {stats.integration_insights.google_ads_performance.leads_generated} leads 
                  with a {stats.integration_insights.google_ads_performance.roi}x ROI.
                </AlertDescription>
              </Alert>

              <div className="grid gap-6 md:grid-cols-2">
                <Card>
                  <CardHeader>
                    <CardTitle>Google Ads Performance</CardTitle>
                    <CardDescription>CRM integration with advertising data</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-sm text-muted-foreground">Leads Generated</span>
                        <span className="font-medium">
                          {stats.integration_insights.google_ads_performance.leads_generated}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-muted-foreground">Total Spend</span>
                        <span className="font-medium">
                          {formatCurrency(stats.integration_insights.google_ads_performance.total_spend)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-muted-foreground">Cost per Lead</span>
                        <span className="font-medium">
                          {formatCurrency(stats.integration_insights.google_ads_performance.cost_per_lead)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-muted-foreground">ROI</span>
                        <span className="font-medium text-green-600">
                          {stats.integration_insights.google_ads_performance.roi}x
                        </span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Website Conversions</CardTitle>
                    <CardDescription>Top converting pages from Google Analytics</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {stats.integration_insights.google_analytics_insights.top_converting_pages.map((page, index) => (
                        <div key={index} className="flex justify-between">
                          <span className="text-sm">{page.page}</span>
                          <Badge variant="secondary">
                            {page.conversions} conversions
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </>
          )}
        </TabsContent>

        <TabsContent value="settings" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>CRM Configuration</CardTitle>
              <CardDescription>
                Configure Django CRM integration settings and AI scoring parameters
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Alert>
                  <CheckCircle className="h-4 w-4" />
                  <AlertDescription>
                    Django CRM is fully integrated with multi-tenant support and AI scoring.
                    All lead data is automatically synchronized across integrations.
                  </AlertDescription>
                </Alert>

                <div className="grid gap-4">
                  <div>
                    <h4 className="font-medium mb-2">AI Scoring Factors</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>Company Size</span>
                        <span className="text-muted-foreground">Up to 60 points</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Budget Range</span>
                        <span className="text-muted-foreground">Up to 30 points</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Decision Maker Status</span>
                        <span className="text-muted-foreground">15 points</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Contact Completeness</span>
                        <span className="text-muted-foreground">Up to 15 points</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Engagement Status</span>
                        <span className="text-muted-foreground">Up to 40 points</span>
                      </div>
                    </div>
                  </div>

                  <Button variant="outline">
                    <Settings className="w-4 h-4 mr-2" />
                    Configure Scoring Rules
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}