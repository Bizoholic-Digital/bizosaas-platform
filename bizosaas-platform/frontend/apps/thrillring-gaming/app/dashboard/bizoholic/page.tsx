'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Globe, FileText, Image, Users, BarChart3, Settings, ExternalLink } from 'lucide-react'
import { useAuthStore } from '@/lib/auth-store'

interface WagtailPage {
  id: number
  title: string
  slug: string
  status: string
  content_type: string
  last_published_at: string
  url_path: string
}

interface WagtailStats {
  total_pages: number
  published_pages: number
  draft_pages: number
  total_images: number
  recent_activity: Array<{
    action: string
    page_title: string
    timestamp: string
    user: string
  }>
}

export default function BizoholicAdminDashboard() {
  const { user } = useAuthStore()
  const [pages, setPages] = useState<WagtailPage[]>([])
  const [stats, setStats] = useState<WagtailStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchWagtailData()
  }, [])

  const fetchWagtailData = async () => {
    try {
      setLoading(true)
      
      // Mock data for demo - in real implementation, connect to Wagtail API
      const mockStats: WagtailStats = {
        total_pages: 24,
        published_pages: 20,
        draft_pages: 4,
        total_images: 156,
        recent_activity: [
          { action: 'Published', page_title: 'AI Marketing Solutions', timestamp: '2 hours ago', user: 'Admin' },
          { action: 'Updated', page_title: 'About Us', timestamp: '1 day ago', user: 'Content Manager' },
          { action: 'Created', page_title: 'New Service Page', timestamp: '2 days ago', user: 'Admin' },
          { action: 'Published', page_title: 'Blog Post - AI Trends', timestamp: '3 days ago', user: 'Content Manager' }
        ]
      }

      const mockPages: WagtailPage[] = [
        { id: 1, title: 'Homepage', slug: 'home', status: 'published', content_type: 'HomePage', last_published_at: '2024-01-15T10:30:00Z', url_path: '/' },
        { id: 2, title: 'About Us', slug: 'about', status: 'published', content_type: 'ContentPage', last_published_at: '2024-01-14T15:20:00Z', url_path: '/about/' },
        { id: 3, title: 'AI Marketing Solutions', slug: 'ai-solutions', status: 'published', content_type: 'ServicePage', last_published_at: '2024-01-16T09:15:00Z', url_path: '/services/ai-solutions/' },
        { id: 4, title: 'Contact', slug: 'contact', status: 'published', content_type: 'ContactPage', last_published_at: '2024-01-13T14:45:00Z', url_path: '/contact/' },
        { id: 5, title: 'New Service Page', slug: 'new-service', status: 'draft', content_type: 'ServicePage', last_published_at: '', url_path: '/services/new-service/' }
      ]

      setStats(mockStats)
      setPages(mockPages)
    } catch (error) {
      console.error('Error fetching Wagtail data:', error)
    } finally {
      setLoading(false)
    }
  }

  const openWagtailAdmin = () => {
    window.open('http://localhost:8006/admin/', '_blank')
  }

  const openWebsite = () => {
    window.open('http://localhost:3001', '_blank')
  }

  if (!user?.permissions?.includes('bizoholic')) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="w-96">
          <CardHeader>
            <CardTitle className="text-red-600">Access Denied</CardTitle>
            <CardDescription>
              You don't have permission to access Bizoholic administration.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Bizoholic Administration</h1>
          <p className="text-muted-foreground">
            Manage Bizoholic website content, pages, and marketing materials
          </p>
        </div>
        <div className="flex space-x-2">
          <Button onClick={openWebsite} variant="outline">
            <Globe className="mr-2 h-4 w-4" />
            View Website
          </Button>
          <Button onClick={openWagtailAdmin}>
            <ExternalLink className="mr-2 h-4 w-4" />
            Wagtail Admin
          </Button>
        </div>
      </div>

      {/* Quick Stats */}
      {stats && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Pages</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total_pages}</div>
              <p className="text-xs text-muted-foreground">
                {stats.published_pages} published, {stats.draft_pages} drafts
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Published Pages</CardTitle>
              <Globe className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{stats.published_pages}</div>
              <p className="text-xs text-muted-foreground">
                Live on website
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Draft Pages</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">{stats.draft_pages}</div>
              <p className="text-xs text-muted-foreground">
                Awaiting publication
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Media Files</CardTitle>
              <Image className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total_images}</div>
              <p className="text-xs text-muted-foreground">
                Images and documents
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Main Content */}
      <Tabs defaultValue="pages" className="space-y-4">
        <TabsList>
          <TabsTrigger value="pages">Pages</TabsTrigger>
          <TabsTrigger value="content">Content Management</TabsTrigger>
          <TabsTrigger value="activity">Recent Activity</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="pages" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Website Pages</CardTitle>
              <CardDescription>
                Manage all pages on the Bizoholic website
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center justify-center py-8">
                  <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
                </div>
              ) : (
                <div className="space-y-3">
                  {pages.map((page) => (
                    <div key={page.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <FileText className="h-5 w-5 text-muted-foreground" />
                        <div>
                          <h3 className="font-medium">{page.title}</h3>
                          <p className="text-sm text-muted-foreground">{page.url_path}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Badge variant={page.status === 'published' ? 'default' : 'secondary'}>
                          {page.status}
                        </Badge>
                        <Button size="sm" variant="outline" onClick={openWagtailAdmin}>
                          Edit
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="content" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
                <CardDescription>Common content management tasks</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button className="w-full justify-start" variant="outline" onClick={openWagtailAdmin}>
                  <FileText className="mr-2 h-4 w-4" />
                  Create New Page
                </Button>
                <Button className="w-full justify-start" variant="outline" onClick={openWagtailAdmin}>
                  <Image className="mr-2 h-4 w-4" />
                  Upload Media
                </Button>
                <Button className="w-full justify-start" variant="outline" onClick={openWagtailAdmin}>
                  <Users className="mr-2 h-4 w-4" />
                  Manage Users
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Content Types</CardTitle>
                <CardDescription>Available page templates</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="text-sm">
                  <div className="font-medium">HomePage</div>
                  <div className="text-muted-foreground">Main landing page template</div>
                </div>
                <div className="text-sm">
                  <div className="font-medium">ServicePage</div>
                  <div className="text-muted-foreground">AI marketing service pages</div>
                </div>
                <div className="text-sm">
                  <div className="font-medium">ContentPage</div>
                  <div className="text-muted-foreground">General content pages</div>
                </div>
                <div className="text-sm">
                  <div className="font-medium">ContactPage</div>
                  <div className="text-muted-foreground">Contact and form pages</div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="activity" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>
                Recent changes to the Bizoholic website
              </CardDescription>
            </CardHeader>
            <CardContent>
              {stats?.recent_activity && (
                <div className="space-y-4">
                  {stats.recent_activity.map((activity, index) => (
                    <div key={index} className="flex items-center space-x-4 p-3 border rounded-lg">
                      <div className="h-2 w-2 bg-primary rounded-full"></div>
                      <div className="flex-1">
                        <p className="text-sm">
                          <span className="font-medium">{activity.action}</span> "{activity.page_title}"
                        </p>
                        <p className="text-xs text-muted-foreground">
                          by {activity.user} • {activity.timestamp}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Bizoholic Settings</CardTitle>
              <CardDescription>
                Configuration and management options
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <Button variant="outline" className="justify-start h-auto p-4" onClick={openWagtailAdmin}>
                  <div className="text-left">
                    <div className="font-medium">Site Settings</div>
                    <div className="text-sm text-muted-foreground">Configure site-wide settings</div>
                  </div>
                </Button>
                <Button variant="outline" className="justify-start h-auto p-4" onClick={openWagtailAdmin}>
                  <div className="text-left">
                    <div className="font-medium">SEO Configuration</div>
                    <div className="text-sm text-muted-foreground">Manage meta tags and SEO</div>
                  </div>
                </Button>
                <Button variant="outline" className="justify-start h-auto p-4" onClick={openWagtailAdmin}>
                  <div className="text-left">
                    <div className="font-medium">Menu Management</div>
                    <div className="text-sm text-muted-foreground">Configure navigation menus</div>
                  </div>
                </Button>
                <Button variant="outline" className="justify-start h-auto p-4" onClick={openWagtailAdmin}>
                  <div className="text-left">
                    <div className="font-medium">User Permissions</div>
                    <div className="text-sm text-muted-foreground">Manage content editor access</div>
                  </div>
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}