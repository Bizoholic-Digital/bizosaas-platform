/**
 * Multi-Tenant CMS Dashboard
 * Integrates with existing Wagtail CMS multi-tenant system
 */

'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { 
  FileText, 
  Globe, 
  Zap, 
  Users, 
  MessageSquare, 
  HelpCircle,
  Plus,
  ExternalLink,
  RefreshCw,
  Search,
  Filter,
  BarChart3
} from 'lucide-react'
import { useAuthStore } from '@/lib/auth-store'
import { apiClient } from '@/lib/api-client'

interface CMSTenant {
  id: string
  name: string
  domain: string
  subdomain?: string
  created_at: string
}

interface CMSPage {
  id: number
  title: string
  slug: string
  url: string
  content_type: string
  first_published_at?: string
  last_published_at?: string
}

interface ContentSummary {
  pages: {
    landing_pages: number
    campaign_pages: number
    content_pages: number
    service_pages: number
    faq_pages: number
    total_pages: number
  }
  snippets: {
    team_members: number
    testimonials: number
    ai_templates: number
  }
}

export default function CMSPage() {
  const { user, organization } = useAuthStore()
  const [tenants, setTenants] = useState<CMSTenant[]>([])
  const [selectedTenant, setSelectedTenant] = useState<string>('')
  const [pages, setPages] = useState<CMSPage[]>([])
  const [contentSummary, setContentSummary] = useState<ContentSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    loadCMSData()
  }, [])

  useEffect(() => {
    if (selectedTenant) {
      loadTenantData(selectedTenant)
    }
  }, [selectedTenant])

  const loadCMSData = async () => {
    try {
      setLoading(true)
      const tenantsData = await apiClient.getCMSTenants()
      setTenants(tenantsData)
      
      // Auto-select current organization's tenant if available
      if (organization && tenantsData.length > 0) {
        const currentTenant = tenantsData.find(t => t.id === organization.bizosaas_tenant_id) || tenantsData[0]
        setSelectedTenant(currentTenant.id)
      }
    } catch (error) {
      console.error('Failed to load CMS data:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadTenantData = async (tenantId: string) => {
    try {
      setLoading(true)
      const [pagesData, summaryData] = await Promise.all([
        apiClient.getCMSPages(tenantId),
        fetch(`http://localhost:8006/api/tenants/${tenantId}/content-summary/`).then(r => r.json())
      ])
      
      setPages(pagesData)
      setContentSummary(summaryData.content_summary)
    } catch (error) {
      console.error('Failed to load tenant data:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredPages = pages.filter(page =>
    page.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    page.content_type.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const getContentTypeIcon = (contentType: string) => {
    switch (contentType) {
      case 'landingpage':
        return <Zap className="h-4 w-4" />
      case 'campaignpage':
        return <BarChart3 className="h-4 w-4" />
      case 'contentpage':
        return <FileText className="h-4 w-4" />
      case 'servicepage':
        return <Globe className="h-4 w-4" />
      case 'faqpage':
        return <HelpCircle className="h-4 w-4" />
      default:
        return <FileText className="h-4 w-4" />
    }
  }

  const getContentTypeBadgeColor = (contentType: string) => {
    switch (contentType) {
      case 'landingpage':
        return 'bg-green-100 text-green-800'
      case 'campaignpage':
        return 'bg-purple-100 text-purple-800'
      case 'contentpage':
        return 'bg-blue-100 text-blue-800'
      case 'servicepage':
        return 'bg-orange-100 text-orange-800'
      case 'faqpage':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading && tenants.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4 text-gray-400" />
          <p className="text-gray-600">Loading CMS data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Content Management</h1>
          <p className="text-muted-foreground mt-2">
            Multi-tenant Wagtail CMS integration with site-based isolation
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => loadCMSData()}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            New Content
          </Button>
        </div>
      </div>

      {/* Tenant Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="h-5 w-5" />
            Content Sites
          </CardTitle>
          <CardDescription>
            Select a tenant site to manage content
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {tenants.map((tenant) => (
              <Card
                key={tenant.id}
                className={`cursor-pointer transition-colors ${
                  selectedTenant === tenant.id 
                    ? 'ring-2 ring-primary bg-primary/5' 
                    : 'hover:bg-muted/50'
                }`}
                onClick={() => setSelectedTenant(tenant.id)}
              >
                <CardContent className="p-4">
                  <div className="space-y-2">
                    <h3 className="font-semibold">{tenant.name}</h3>
                    <p className="text-sm text-muted-foreground">
                      {tenant.subdomain ? `${tenant.subdomain}.${tenant.domain}` : tenant.domain}
                    </p>
                    <Badge variant="secondary" className="text-xs">
                      {tenant.id}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {selectedTenant && (
        <div className="space-y-6">
          {/* Content Summary */}
          {contentSummary && (
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Zap className="h-4 w-4 text-green-600" />
                    <span className="text-sm font-medium">Landing Pages</span>
                  </div>
                  <div className="text-2xl font-bold">{contentSummary.pages.landing_pages}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <BarChart3 className="h-4 w-4 text-purple-600" />
                    <span className="text-sm font-medium">Campaigns</span>
                  </div>
                  <div className="text-2xl font-bold">{contentSummary.pages.campaign_pages}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <FileText className="h-4 w-4 text-blue-600" />
                    <span className="text-sm font-medium">Content</span>
                  </div>
                  <div className="text-2xl font-bold">{contentSummary.pages.content_pages}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Globe className="h-4 w-4 text-orange-600" />
                    <span className="text-sm font-medium">Services</span>
                  </div>
                  <div className="text-2xl font-bold">{contentSummary.pages.service_pages}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <HelpCircle className="h-4 w-4 text-gray-600" />
                    <span className="text-sm font-medium">FAQs</span>
                  </div>
                  <div className="text-2xl font-bold">{contentSummary.pages.faq_pages}</div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Content Management Tabs */}
          <Tabs defaultValue="pages" className="space-y-4">
            <TabsList>
              <TabsTrigger value="pages">All Pages</TabsTrigger>
              <TabsTrigger value="snippets">Snippets</TabsTrigger>
              <TabsTrigger value="templates">AI Templates</TabsTrigger>
              <TabsTrigger value="navigation">Navigation</TabsTrigger>
            </TabsList>

            <TabsContent value="pages" className="space-y-4">
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle>Content Pages</CardTitle>
                      <CardDescription>
                        Manage all content for the selected tenant
                      </CardDescription>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="relative">
                        <Search className="h-4 w-4 absolute left-3 top-3 text-muted-foreground" />
                        <Input
                          placeholder="Search pages..."
                          value={searchTerm}
                          onChange={(e) => setSearchTerm(e.target.value)}
                          className="pl-10 w-[300px]"
                        />
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {filteredPages.length === 0 ? (
                      <div className="text-center py-8 text-muted-foreground">
                        {searchTerm ? 'No pages found matching your search.' : 'No pages found for this tenant.'}
                      </div>
                    ) : (
                      filteredPages.map((page) => (
                        <div
                          key={page.id}
                          className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50"
                        >
                          <div className="flex items-center gap-3">
                            {getContentTypeIcon(page.content_type)}
                            <div>
                              <h3 className="font-medium">{page.title}</h3>
                              <div className="flex items-center gap-2 mt-1">
                                <Badge
                                  variant="secondary"
                                  className={`text-xs ${getContentTypeBadgeColor(page.content_type)}`}
                                >
                                  {page.content_type.replace('page', '').toUpperCase()}
                                </Badge>
                                <span className="text-xs text-muted-foreground">
                                  /{page.slug}
                                </span>
                                {page.first_published_at && (
                                  <span className="text-xs text-muted-foreground">
                                    Published {new Date(page.first_published_at).toLocaleDateString()}
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <Button variant="outline" size="sm">
                              Edit
                            </Button>
                            <Button variant="outline" size="sm">
                              <ExternalLink className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="snippets">
              <Card>
                <CardHeader>
                  <CardTitle>Content Snippets</CardTitle>
                  <CardDescription>
                    Reusable content components
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Card>
                      <CardContent className="p-4 text-center">
                        <Users className="h-8 w-8 mx-auto mb-2 text-blue-600" />
                        <h3 className="font-medium">Team Members</h3>
                        <p className="text-2xl font-bold mt-1">
                          {contentSummary?.snippets.team_members || 0}
                        </p>
                        <Button variant="outline" size="sm" className="mt-2">
                          Manage
                        </Button>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardContent className="p-4 text-center">
                        <MessageSquare className="h-8 w-8 mx-auto mb-2 text-green-600" />
                        <h3 className="font-medium">Testimonials</h3>
                        <p className="text-2xl font-bold mt-1">
                          {contentSummary?.snippets.testimonials || 0}
                        </p>
                        <Button variant="outline" size="sm" className="mt-2">
                          Manage
                        </Button>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardContent className="p-4 text-center">
                        <Zap className="h-8 w-8 mx-auto mb-2 text-purple-600" />
                        <h3 className="font-medium">AI Templates</h3>
                        <p className="text-2xl font-bold mt-1">
                          {contentSummary?.snippets.ai_templates || 0}
                        </p>
                        <Button variant="outline" size="sm" className="mt-2">
                          Manage
                        </Button>
                      </CardContent>
                    </Card>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="templates">
              <Card>
                <CardHeader>
                  <CardTitle>AI Content Templates</CardTitle>
                  <CardDescription>
                    Templates for AI-powered content generation
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8 text-muted-foreground">
                    AI Templates management coming soon...
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="navigation">
              <Card>
                <CardHeader>
                  <CardTitle>Site Navigation</CardTitle>
                  <CardDescription>
                    Configure site menu and navigation structure
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8 text-muted-foreground">
                    Navigation management coming soon...
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      )}

      {/* Direct Wagtail Admin Link */}
      <Card className="border-dashed border-2">
        <CardContent className="p-6 text-center">
          <Globe className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
          <h3 className="font-medium mb-2">Full CMS Access</h3>
          <p className="text-sm text-muted-foreground mb-4">
            Access the full Wagtail admin interface for advanced content management
          </p>
          <Button variant="outline" asChild>
            <a href="http://localhost:8006/admin" target="_blank" rel="noopener noreferrer">
              <ExternalLink className="h-4 w-4 mr-2" />
              Open Wagtail Admin
            </a>
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}