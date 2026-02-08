'use client'

/**
 * Wagtail CMS Management Interface - TailAdmin v2 Style
 * Manages Bizoholic website content via FastAPI AI Central Hub
 */

import { useState, useEffect } from 'react'
import { Card } from '../../components/ui/card'
import { Button } from '../../components/ui/button'
import { Badge } from '../../components/ui/badge'
import { Input } from '../../components/ui/input'
import { Textarea } from '../../components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs'
import {
  FileText,
  Globe,
  Image,
  Settings,
  Users,
  Search,
  Plus,
  Edit3,
  Trash2,
  Eye,
  Save,
  RefreshCw,
  Calendar,
  Tag,
  TrendingUp
} from 'lucide-react'

import { useAuth } from '@/shared/components/AuthProvider'
import { gql, useQuery } from 'urql'

const GET_CMS_DATA = gql`
  query GetCMSData($tenantId: String!) {
    cmsPages(tenantId: $tenantId) {
      id
      title
      slug
      status
      contentType
      lastModified
      author
      views
      seoScore
    }
    cmsStats(tenantId: $tenantId) {
      posts
      pages
    }
  }
`;

// Types for the CMS Management Interface
interface Page {
  id: string;
  title: string;
  slug: string;
  status: string;
  content_type: string;
  last_modified: string;
  author: string;
  views: number;
  seo_score: number;
}

interface Media {
  id: string;
  title: string;
  file_url: string;
  file_type: string;
  file_size: number;
  upload_date: string;
  usage_count: number;
}

interface FormSubmission {
  id: string;
  form_name: string;
  email: string;
  message: string;
  submitted_at: string;
  status: string;
  source_page: string;
}

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://localhost:8000';

export default function CMSManagementPage() {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState('pages')
  const [pages, setPages] = useState<Page[]>([])
  const [media, setMedia] = useState<Media[]>([])
  const [submissions, setSubmissions] = useState<FormSubmission[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedPage, setSelectedPage] = useState<Page | null>(null)
  const [isEditing, setIsEditing] = useState(false)

  const [result, reexecuteCMSData] = useQuery({
    query: GET_CMS_DATA,
    variables: { tenantId: user?.tenant || 'default' },
    pause: !user,
  });

  const { data, fetching, error } = result;

  useEffect(() => {
    if (data?.cmsPages) {
      const mappedPages = data.cmsPages.map((p: any) => ({
        ...p,
        content_type: p.contentType,
        last_modified: p.lastModified,
        seo_score: p.seoScore
      }));
      setPages(mappedPages);
    } else if (!fetching && !error) {
      setPages(fallbackPages);
    }

    // Media and Submissions still use fallbacks for now
    setMedia(fallbackMedia);
    setSubmissions(fallbackSubmissions);
  }, [data, fetching, error]);

  const fetchCMSData = async () => {
    reexecuteCMSData({ requestPolicy: 'network-only' });
  }

  const handlePublishPage = async (pageId: string) => {
    // This should also be migrated to a GraphQL mutation soon
    try {
      const response = await fetch(`${BRAIN_API_URL}/api/brain/wagtail/pages/${pageId}/publish`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })

      if (response.ok) {
        await fetchCMSData()
      }
    } catch (error) {
      console.error('Error publishing page:', error)
    }
  }

  const handleDeletePage = async (pageId: string) => {
    if (!confirm('Are you sure you want to delete this page?')) return

    try {
      const response = await fetch(`${BRAIN_API_URL}/api/brain/wagtail/pages/${pageId}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' }
      })

      if (response.ok) {
        await fetchCMSData()
      }
    } catch (error) {
      console.error('Error deleting page:', error)
    }
  }

  const filteredPages = pages.filter(page =>
    page.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    page.slug.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published': return 'bg-green-100 text-green-800'
      case 'draft': return 'bg-yellow-100 text-yellow-800'
      case 'archived': return 'bg-gray-100 text-gray-800'
      default: return 'bg-blue-100 text-blue-800'
    }
  }

  if (fetching && !data) {
    return (
      <div className="flex items-center justify-center h-96">
        <RefreshCw className="w-8 h-8 animate-spin text-blue-600" />
        <span className="ml-2 text-lg">Loading CMS data...</span>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Wagtail CMS Management
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mt-1">
            Manage Bizoholic website content, pages, and media
          </p>
        </div>
        <div className="flex space-x-3">
          <Button onClick={fetchCMSData} variant="outline">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
          <Button className="bg-blue-600 hover:bg-blue-700">
            <Plus className="w-4 h-4 mr-2" />
            New Page
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Total Pages</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{data?.cmsStats?.pages ?? pages.length}</p>
            </div>
            <FileText className="w-8 h-8 text-blue-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Blog Posts</p>
              <p className="text-2xl font-bold text-green-600">
                {data?.cmsStats?.posts ?? 0}
              </p>
            </div>
            <Globe className="w-8 h-8 text-green-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Media Files</p>
              <p className="text-2xl font-bold text-purple-600">{media.length}</p>
            </div>
            <Image className="w-8 h-8 text-purple-600" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Form Submissions</p>
              <p className="text-2xl font-bold text-orange-600">{submissions.length}</p>
            </div>
            <Users className="w-8 h-8 text-orange-600" />
          </div>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="pages">Pages</TabsTrigger>
          <TabsTrigger value="media">Media</TabsTrigger>
          <TabsTrigger value="forms">Form Submissions</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        {/* Pages Tab */}
        <TabsContent value="pages" className="space-y-4">
          <div className="flex justify-between items-center">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                placeholder="Search pages..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 w-80"
              />
            </div>
            <Select defaultValue="all">
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="published">Published</SelectItem>
                <SelectItem value="draft">Draft</SelectItem>
                <SelectItem value="archived">Archived</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Card>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Page
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Last Modified
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Views
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      SEO Score
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                  {filteredPages.map((page) => (
                    <tr key={page.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                      <td className="px-6 py-4">
                        <div>
                          <div className="text-sm font-medium text-gray-900 dark:text-white">
                            {page.title}
                          </div>
                          <div className="text-sm text-gray-500">/{page.slug}</div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <Badge className={getStatusColor(page.status)}>
                          {page.status}
                        </Badge>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                        {new Date(page.last_modified).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                        {page.views.toLocaleString()}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center">
                          <div className="text-sm text-gray-900 dark:text-white mr-2">
                            {page.seo_score}%
                          </div>
                          <div className="w-16 bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-green-600 h-2 rounded-full"
                              style={{ width: `${page.seo_score}%` }}
                            ></div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm font-medium space-x-2">
                        <Button variant="ghost" size="sm">
                          <Eye className="w-4 h-4" />
                        </Button>
                        <Button variant="ghost" size="sm">
                          <Edit3 className="w-4 h-4" />
                        </Button>
                        {page.status === 'draft' && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handlePublishPage(page.id)}
                          >
                            <Globe className="w-4 h-4" />
                          </Button>
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDeletePage(page.id)}
                        >
                          <Trash2 className="w-4 h-4 text-red-500" />
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </TabsContent>

        {/* Media Tab */}
        <TabsContent value="media" className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Media Library</h3>
            <Button className="bg-purple-600 hover:bg-purple-700">
              <Plus className="w-4 h-4 mr-2" />
              Upload Media
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {media.map((file) => (
              <Card key={file.id} className="p-4">
                <div className="aspect-square bg-gray-100 dark:bg-gray-800 rounded-lg mb-3 flex items-center justify-center">
                  {file.file_type.startsWith('image/') ? (
                    <img
                      src={file.file_url}
                      alt={file.title}
                      className="w-full h-full object-cover rounded-lg"
                    />
                  ) : (
                    <FileText className="w-12 h-12 text-gray-400" />
                  )}
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                    {file.title}
                  </p>
                  <p className="text-xs text-gray-500">
                    {(file.file_size / 1024).toFixed(1)} KB
                  </p>
                  <p className="text-xs text-gray-500">
                    Used {file.usage_count} times
                  </p>
                </div>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Form Submissions Tab */}
        <TabsContent value="forms" className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Form Submissions</h3>
            <Badge variant="secondary">
              {submissions.filter(s => s.status === 'new').length} new
            </Badge>
          </div>

          <Card>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Form
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Email
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Message
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Submitted
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                  {submissions.map((submission) => (
                    <tr key={submission.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                      <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white">
                        {submission.form_name}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                        {submission.email}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 dark:text-white max-w-xs truncate">
                        {submission.message}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                        {new Date(submission.submitted_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4">
                        <Badge className={
                          submission.status === 'new' ? 'bg-blue-100 text-blue-800' :
                            submission.status === 'read' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-green-100 text-green-800'
                        }>
                          {submission.status}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </TabsContent>

        {/* Settings Tab */}
        <TabsContent value="settings" className="space-y-4">
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">CMS Settings</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Site Title
                </label>
                <Input defaultValue="Bizoholic Digital Marketing Agency" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Site Description
                </label>
                <Textarea defaultValue="AI-powered digital marketing solutions for modern businesses" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Default Page Status
                </label>
                <Select defaultValue="draft">
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="draft">Draft</SelectItem>
                    <SelectItem value="published">Published</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button className="bg-blue-600 hover:bg-blue-700">
                <Save className="w-4 h-4 mr-2" />
                Save Settings
              </Button>
            </div>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

// Fallback data for development/testing
const fallbackPages: Page[] = [
  {
    id: 'page-1',
    title: 'Homepage',
    slug: 'home',
    status: 'published',
    content_type: 'HomePage',
    last_modified: '2024-01-15T10:30:00Z',
    author: 'Admin',
    views: 15234,
    seo_score: 95
  },
  {
    id: 'page-2',
    title: 'About Us',
    slug: 'about',
    status: 'published',
    content_type: 'StandardPage',
    last_modified: '2024-01-14T15:45:00Z',
    author: 'Content Manager',
    views: 8756,
    seo_score: 88
  },
  {
    id: 'page-3',
    title: 'AI Marketing Strategy Guide',
    slug: 'ai-marketing-guide',
    status: 'draft',
    content_type: 'BlogPage',
    last_modified: '2024-01-16T09:15:00Z',
    author: 'Marketing Team',
    views: 0,
    seo_score: 72
  }
]

const fallbackMedia: Media[] = [
  {
    id: 'media-1',
    title: 'Hero Image - AI Marketing',
    file_url: '/images/ai-marketing-hero.jpg',
    file_type: 'image/jpeg',
    file_size: 245760,
    upload_date: '2024-01-10T14:20:00Z',
    usage_count: 5
  },
  {
    id: 'media-2',
    title: 'Team Photo',
    file_url: '/images/team-photo.jpg',
    file_type: 'image/jpeg',
    file_size: 183542,
    upload_date: '2024-01-08T11:30:00Z',
    usage_count: 3
  }
]

const fallbackSubmissions: FormSubmission[] = [
  {
    id: 'sub-1',
    form_name: 'Contact Form',
    email: 'john.doe@example.com',
    message: 'Interested in AI marketing automation services...',
    submitted_at: '2024-01-16T10:30:00Z',
    status: 'new',
    source_page: '/contact'
  },
  {
    id: 'sub-2',
    form_name: 'Newsletter Signup',
    email: 'jane.smith@company.com',
    message: 'Subscribe to marketing insights',
    submitted_at: '2024-01-15T16:45:00Z',
    status: 'read',
    source_page: '/blog'
  }
]