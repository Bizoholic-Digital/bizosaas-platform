"use client"

import { useState, useEffect } from 'react'
import { useLeads, useCRMStats, useLeadSources, useTeamMembers } from '@/hooks/use-crm-data'
import { leadStatusColors, leadStatusLabels, getLeadScoreColor, formatLeadValue, Lead } from '@/lib/api/crm-api'
import { formatDate, formatCurrency } from '@/lib/date-utils'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Users, 
  Plus, 
  Search,
  MoreVertical,
  Mail,
  Phone,
  Calendar,
  Target,
  TrendingUp,
  UserPlus,
  MessageSquare,
  FileText
} from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'


export default function CRMPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [activeTab, setActiveTab] = useState('leads')
  
  // Live CRM data hooks
  const { leads, loading: leadsLoading, error: leadsError, refreshLeads } = useLeads({
    search: searchTerm || undefined,
    status: statusFilter === 'all' ? undefined : statusFilter,
    autoRefresh: true,
    refreshInterval: 30000 // Refresh every 30 seconds
  })
  
  const { stats, loading: statsLoading, error: statsError } = useCRMStats()
  const { sources } = useLeadSources()
  const { teamMembers } = useTeamMembers()

  // Leads are already filtered by the API based on search and status
  const filteredLeads = leads

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'new': return 'bg-blue-500'
      case 'qualified': return 'bg-green-500'
      case 'contacted': return 'bg-yellow-500'
      case 'opportunity': return 'bg-purple-500'
      case 'converted': return 'bg-emerald-500'
      case 'lost': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  // Date and currency formatting moved to date-utils to prevent hydration issues

  // Use live stats when available, fallback to calculated values
  const totalLeads = stats?.totalLeads || leads.length
  const newLeads = stats?.newLeads || leads.filter(lead => lead.status === 'new').length
  const qualifiedLeads = stats?.qualifiedLeads || leads.filter(lead => lead.status === 'qualified').length
  const totalValue = stats?.totalValue || leads.reduce((sum, lead) => sum + (lead.value || 0), 0)

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">CRM & Leads</h1>
          <p className="text-muted-foreground">
            Manage leads and customer relationships
          </p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Add Lead
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Leads</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {statsLoading ? '...' : totalLeads}
            </div>
            <p className="text-xs text-muted-foreground">
              {stats?.monthlyGrowth ? `+${stats.monthlyGrowth}% from last month` : '+3 from yesterday'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">New Leads</CardTitle>
            <UserPlus className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {statsLoading ? '...' : newLeads}
            </div>
            <p className="text-xs text-muted-foreground">Awaiting qualification</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Qualified Leads</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {statsLoading ? '...' : qualifiedLeads}
            </div>
            <p className="text-xs text-muted-foreground">
              {stats?.conversionRate ? `${stats.conversionRate}% conversion rate` : 'Ready for follow-up'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pipeline Value</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {statsLoading ? '...' : formatCurrency(totalValue)}
            </div>
            <p className="text-xs text-muted-foreground">
              {stats?.avgLeadScore ? `Avg score: ${stats.avgLeadScore}%` : 'Potential revenue'}
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="leads">Leads</TabsTrigger>
          <TabsTrigger value="pipeline">Pipeline</TabsTrigger>
          <TabsTrigger value="activities">Activities</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
        </TabsList>

        <TabsContent value="leads">
          <Card>
            <CardHeader>
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search leads..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
                
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-40">
                    <SelectValue placeholder="Status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="new">New</SelectItem>
                    <SelectItem value="qualified">Qualified</SelectItem>
                    <SelectItem value="contacted">Contacted</SelectItem>
                    <SelectItem value="opportunity">Opportunity</SelectItem>
                    <SelectItem value="converted">Converted</SelectItem>
                    <SelectItem value="lost">Lost</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardHeader>

            <CardContent>
              {leadsError && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-red-600 text-sm">Error loading leads: {leadsError}</p>
                  <Button onClick={refreshLeads} size="sm" className="mt-2">
                    Retry
                  </Button>
                </div>
              )}
              
              {leadsLoading ? (
                <div className="space-y-4">
                  {[...Array(3)].map((_, i) => (
                    <div key={i} className="animate-pulse">
                      <div className="h-24 bg-gray-200 rounded-md"></div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="space-y-4">
                  {filteredLeads.map((lead) => (
                    <Card key={lead.id} className="hover:shadow-md transition-shadow">
                      <CardContent className="p-6">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <h3 className="text-lg font-semibold">{lead.name}</h3>
                            <Badge className={`${getStatusColor(lead.status)} text-white`}>
                              {lead.status}
                            </Badge>
                            <div className="px-2 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-600">
                              {lead.score}% score
                            </div>
                          </div>
                          
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-4">
                            <div>
                              <p className="text-muted-foreground">Email</p>
                              <p className="font-medium">{lead.email}</p>
                            </div>
                            {lead.company && (
                              <div>
                                <p className="text-muted-foreground">Company</p>
                                <p className="font-medium">{lead.company}</p>
                              </div>
                            )}
                            <div>
                              <p className="text-muted-foreground">Source</p>
                              <p className="font-medium">{lead.source}</p>
                            </div>
                            {lead.value && (
                              <div>
                                <p className="text-muted-foreground">Value</p>
                                <p className="font-medium">{formatCurrency(lead.value)}</p>
                              </div>
                            )}
                          </div>

                          <div className="text-xs text-muted-foreground">
                            Created: {formatDate(lead.createdAt)}
                          </div>
                        </div>
                        
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="icon">
                              <MoreVertical className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem>
                              <Mail className="mr-2 h-4 w-4" />
                              Send Email
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Phone className="mr-2 h-4 w-4" />
                              Make Call
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Calendar className="mr-2 h-4 w-4" />
                              Schedule Meeting
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                    </CardContent>
                    </Card>
                  ))}
                  
                  {filteredLeads.length === 0 && !leadsLoading && (
                    <div className="text-center py-12 text-muted-foreground">
                      <Users className="h-16 w-16 mx-auto mb-4" />
                      <p>No leads found</p>
                      {searchTerm || statusFilter !== 'all' ? (
                        <p className="text-sm mt-2">Try adjusting your search or filters</p>
                      ) : (
                        <p className="text-sm mt-2">Start by adding your first lead</p>
                      )}
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="pipeline">
          <Card>
            <CardHeader>
              <CardTitle>Sales Pipeline</CardTitle>
              <CardDescription>Visual representation of your sales pipeline</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-muted-foreground">
                <TrendingUp className="h-16 w-16 mx-auto mb-4" />
                <p>Pipeline visualization coming soon</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="activities">
          <Card>
            <CardHeader>
              <CardTitle>Recent Activities</CardTitle>
              <CardDescription>Track all interactions and activities</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-muted-foreground">
                <MessageSquare className="h-16 w-16 mx-auto mb-4" />
                <p>Activity timeline coming soon</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="reports">
          <Card>
            <CardHeader>
              <CardTitle>CRM Reports</CardTitle>
              <CardDescription>Analytics and performance reports</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-muted-foreground">
                <FileText className="h-16 w-16 mx-auto mb-4" />
                <p>CRM reports coming soon</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}