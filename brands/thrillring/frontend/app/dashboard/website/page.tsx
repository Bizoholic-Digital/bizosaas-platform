"use client"

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
  Globe,
  Edit,
  Plus,
  Search,
  Settings,
  Eye,
  ExternalLink,
  FileText,
  Image,
  RefreshCw,
  BarChart3,
  Users,
  Target,
  Clock,
  CheckCircle,
  AlertTriangle,
  Save,
  Undo2,
  History,
  GitBranch
} from 'lucide-react'
import { wagtailCMS, useWagtailPage, useWagtailContentPages } from '@/lib/brain-cms'
import { FeatureGate } from '@/components/tenant/feature-gate'

interface WebsiteStats {
  totalPages: number
  publishedPages: number
  draftPages: number
  lastUpdate: string
  seoScore: number
  pageViews: number
  conversionRate: number
}

interface PageRevision {
  id: string
  title: string
  author: string
  created: string
  status: 'draft' | 'published' | 'scheduled'
  changes: string[]
}

export default function WebsiteManagement() {
  const [activeTab, setActiveTab] = useState('overview')
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [wagtailConnected, setWagtailConnected] = useState(false)
  const [websiteStats, setWebsiteStats] = useState<WebsiteStats>({
    totalPages: 0,
    publishedPages: 0,
    draftPages: 0,
    lastUpdate: '',
    seoScore: 0,
    pageViews: 0,
    conversionRate: 0
  })

  // Get content pages from Wagtail
  const { pages: contentPages, loading: pagesLoading } = useWagtailContentPages(20)
  const { page: homePage, loading: homeLoading } = useWagtailPage('home')

  useEffect(() => {
    const initializeCMS = async () => {
      try {
        setIsLoading(true)
        // Test Wagtail connection
        const testPage = await wagtailCMS.getPage('home')
        setWagtailConnected(!!testPage)

        // Load website statistics
        setWebsiteStats({
          totalPages: 12,
          publishedPages: 10,
          draftPages: 2,
          lastUpdate: '2024-09-10T14:30:00Z',
          seoScore: 85,
          pageViews: 15420,
          conversionRate: 3.2
        })
      } catch (error) {
        console.error('CMS initialization error:', error)
        setWagtailConnected(false)
      } finally {
        setIsLoading(false)
      }
    }

    initializeCMS()
  }, [])

  const handleCreatePage = () => {
    // Open Wagtail admin in new tab for page creation
    window.open('http://localhost:8006/admin/pages/add/', '_blank')
  }

  const handleEditPage = (pageId: string) => {
    // Open specific page editor in Wagtail
    window.open(`http://localhost:8006/admin/pages/${pageId}/edit/`, '_blank')
  }

  const mockRevisions: PageRevision[] = [
    {
      id: '1',
      title: 'Homepage - Hero Section Update',
      author: 'Super Admin',
      created: '2024-09-10T14:30:00Z',
      status: 'published',
      changes: ['Updated hero text', 'Added new CTA button', 'Optimized mobile layout']
    },
    {
      id: '2',
      title: 'Services Page - AI Features',
      author: 'Content Admin',
      created: '2024-09-10T10:15:00Z',
      status: 'draft',
      changes: ['Added AI automation section', 'Updated pricing', 'New testimonials']
    },
    {
      id: '3',
      title: 'About Page - Team Updates',
      author: 'Content Admin',
      created: '2024-09-09T16:45:00Z',
      status: 'published',
      changes: ['Added new team members', 'Updated company mission', 'New office photos']
    }
  ]

  if (isLoading) {
    return (
      <div className="flex-1 p-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4 text-primary" />
            <p className="text-muted-foreground">Loading website management...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 p-8 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight flex items-center">
            <Globe className="h-8 w-8 text-blue-600 mr-3" />
            Website Management
          </h2>
          <p className="text-muted-foreground">
            Manage Bizoholic website content, pages, and SEO settings
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={() => window.open('http://localhost:3000', '_blank')}>
            <Eye className="h-4 w-4 mr-2" />
            Preview Site
          </Button>
          <Button onClick={handleCreatePage}>
            <Plus className="h-4 w-4 mr-2" />
            New Page
          </Button>
        </div>
      </div>

      {/* CMS Connection Status */}
      <Alert>
        <div className="flex items-center">
          {wagtailConnected ? (
            <>
              <CheckCircle className="h-4 w-4 text-green-600" />
              <AlertDescription className="ml-2">
                Wagtail CMS is connected and active. Content management is fully operational.
                <Button variant="link" className="p-0 ml-2 h-auto" asChild>
                  <a href="http://localhost:8006/admin/" target="_blank" rel="noopener noreferrer">
                    <ExternalLink className="h-3 w-3 mr-1" />
                    Open Full CMS Admin
                  </a>
                </Button>
              </AlertDescription>
            </>
          ) : (
            <>
              <AlertTriangle className="h-4 w-4 text-yellow-600" />
              <AlertDescription className="ml-2">
                Wagtail CMS connection unavailable. Using static content mode.
              </AlertDescription>
            </>
          )}
        </div>
      </Alert>

      {/* Website Statistics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Pages</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{websiteStats.totalPages}</div>
            <p className="text-xs text-muted-foreground">
              {websiteStats.publishedPages} published, {websiteStats.draftPages} drafts
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">SEO Score</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{websiteStats.seoScore}/100</div>
            <p className="text-xs text-green-600">
              Excellent optimization
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Page Views</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{websiteStats.pageViews.toLocaleString()}</div>
            <p className="text-xs text-green-600">
              +12.5% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{websiteStats.conversionRate}%</div>
            <p className="text-xs text-green-600">
              +0.3% from last week
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Content Management Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="pages">Pages</TabsTrigger>
          <TabsTrigger value="content">Content</TabsTrigger>
          <TabsTrigger value="revisions">Revisions</TabsTrigger>
          <TabsTrigger value="seo">SEO</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-6 md:grid-cols-2">
            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
                <CardDescription>Common website management tasks</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="outline" className="w-full justify-start" onClick={handleCreatePage}>
                  <Plus className="h-4 w-4 mr-2" />
                  Create New Page
                </Button>
                <Button variant="outline" className="w-full justify-start" onClick={() => handleEditPage('1')}>
                  <Edit className="h-4 w-4 mr-2" />
                  Edit Homepage
                </Button>
                <Button variant="outline" className="w-full justify-start" asChild>
                  <a href="http://localhost:8006/admin/images/" target="_blank" rel="noopener noreferrer">
                    <Image className="h-4 w-4 mr-2" />
                    Manage Images
                  </a>
                </Button>
                <Button variant="outline" className="w-full justify-start" asChild>
                  <a href="http://localhost:8006/admin/settings/" target="_blank" rel="noopener noreferrer">
                    <Settings className="h-4 w-4 mr-2" />
                    Site Settings
                  </a>
                </Button>
              </CardContent>
            </Card>

            {/* Recent Activity */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>Latest content changes</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {mockRevisions.slice(0, 3).map((revision) => (
                    <div key={revision.id} className="flex items-start space-x-3">
                      <div className="flex-shrink-0">
                        {revision.status === 'published' ? (
                          <CheckCircle className="h-4 w-4 text-green-600 mt-0.5" />
                        ) : (
                          <Clock className="h-4 w-4 text-yellow-600 mt-0.5" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium">{revision.title}</p>
                        <p className="text-xs text-muted-foreground">
                          by {revision.author} • {new Date(revision.created).toLocaleDateString()}
                        </p>
                      </div>
                      <Badge variant={revision.status === 'published' ? 'default' : 'secondary'}>
                        {revision.status}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="pages" className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Search className="h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search pages..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="max-w-sm"
              />
            </div>
            <Button onClick={handleCreatePage}>
              <Plus className="h-4 w-4 mr-2" />
              New Page
            </Button>
          </div>

          {wagtailConnected && contentPages.length > 0 ? (
            <div className="grid gap-4">
              {contentPages.map((page) => (
                <Card key={page.id}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-semibold">{page.title}</h3>
                        <p className="text-sm text-muted-foreground">{page.url_path}</p>
                        <p className="text-xs text-muted-foreground mt-1">
                          Last updated: {new Date(page.last_published_at).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button variant="outline" size="sm" onClick={() => window.open(`http://localhost:3000${page.url_path}`, '_blank')}>
                          <Eye className="h-3 w-3 mr-1" />
                          Preview
                        </Button>
                        <Button size="sm" onClick={() => handleEditPage(page.id.toString())}>
                          <Edit className="h-3 w-3 mr-1" />
                          Edit
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="p-8 text-center">
                <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="font-semibold mb-2">No Pages Found</h3>
                <p className="text-muted-foreground mb-4">
                  {wagtailConnected ? 'Start creating pages to manage your website content.' : 'CMS connection required to manage pages.'}
                </p>
                {wagtailConnected && (
                  <Button onClick={handleCreatePage}>
                    <Plus className="h-4 w-4 mr-2" />
                    Create First Page
                  </Button>
                )}
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="revisions" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <History className="h-5 w-5 mr-2" />
                Content Revisions & Version Control
              </CardTitle>
              <CardDescription>
                Track all changes made to your website content with ability to revert
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mockRevisions.map((revision) => (
                  <div key={revision.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-3">
                        <GitBranch className="h-4 w-4 text-primary mt-1" />
                        <div>
                          <h4 className="font-medium">{revision.title}</h4>
                          <p className="text-sm text-muted-foreground">
                            {revision.author} • {new Date(revision.created).toLocaleString()}
                          </p>
                          <div className="mt-2">
                            <p className="text-sm font-medium mb-1">Changes:</p>
                            <ul className="text-sm text-muted-foreground space-y-1">
                              {revision.changes.map((change, index) => (
                                <li key={index} className="flex items-center">
                                  <span className="w-1 h-1 bg-primary rounded-full mr-2" />
                                  {change}
                                </li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant={revision.status === 'published' ? 'default' : 'secondary'}>
                          {revision.status}
                        </Badge>
                        <FeatureGate feature="version_control" tier="professional">
                          <Button variant="outline" size="sm">
                            <Undo2 className="h-3 w-3 mr-1" />
                            Revert
                          </Button>
                        </FeatureGate>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="seo" className="space-y-4">
          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>SEO Overview</CardTitle>
                <CardDescription>Website search engine optimization status</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Overall SEO Score</span>
                    <Badge variant="default" className="bg-green-600">{websiteStats.seoScore}/100</Badge>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Meta Descriptions</span>
                      <span className="text-green-600">✓ Complete</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Image Alt Tags</span>
                      <span className="text-green-600">✓ Optimized</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Page Load Speed</span>
                      <span className="text-yellow-600">△ Needs Work</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Mobile Optimization</span>
                      <span className="text-green-600">✓ Excellent</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>SEO Actions</CardTitle>
                <CardDescription>Recommended improvements</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <Button variant="outline" className="w-full justify-start" asChild>
                    <a href="http://localhost:8006/admin/settings/seo/" target="_blank" rel="noopener noreferrer">
                      <Settings className="h-4 w-4 mr-2" />
                      Global SEO Settings
                    </a>
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <BarChart3 className="h-4 w-4 mr-2" />
                    Generate SEO Report
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Audit All Pages
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}