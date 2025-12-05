"use client"

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Palette, 
  Plus, 
  Search,
  MoreVertical,
  Download,
  Share,
  Edit,
  Copy,
  FileText,
  Image,
  Video,
  Headphones,
  Sparkles,
  Filter
} from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

interface ContentAsset {
  id: string
  name: string
  type: 'text' | 'image' | 'video' | 'audio' | 'template'
  status: 'draft' | 'review' | 'approved' | 'published'
  aiGenerated: boolean
  createdAt: string
  updatedAt: string
  createdBy: string
  tags: string[]
  description: string
  thumbnail?: string
  fileSize?: string
  dimensions?: string
  duration?: string
}

const mockAssets: ContentAsset[] = [
  {
    id: '1',
    name: 'Q1 Campaign Blog Post',
    type: 'text',
    status: 'approved',
    aiGenerated: true,
    createdAt: '2024-01-26T10:30:00Z',
    updatedAt: '2024-01-26T14:20:00Z',
    createdBy: 'AI Content Generator',
    tags: ['marketing', 'blog', 'Q1', 'campaign'],
    description: 'Comprehensive blog post about Q1 marketing strategies and industry insights'
  },
  {
    id: '2',
    name: 'Social Media Graphics Set',
    type: 'image',
    status: 'published',
    aiGenerated: true,
    createdAt: '2024-01-25T09:15:00Z',
    updatedAt: '2024-01-25T16:30:00Z',
    createdBy: 'AI Design Studio',
    tags: ['social-media', 'graphics', 'branding'],
    description: 'Set of 5 social media graphics for various platforms',
    dimensions: '1080x1080',
    fileSize: '2.3 MB'
  },
  {
    id: '3',
    name: 'Product Demo Video',
    type: 'video',
    status: 'review',
    aiGenerated: true,
    createdAt: '2024-01-24T16:45:00Z',
    updatedAt: '2024-01-26T11:30:00Z',
    createdBy: 'AI Video Creator',
    tags: ['product', 'demo', 'video', 'marketing'],
    description: 'Engaging product demonstration video highlighting key features',
    duration: '2:34',
    fileSize: '45.7 MB'
  },
  {
    id: '4',
    name: 'Email Template - Welcome Series',
    type: 'template',
    status: 'draft',
    aiGenerated: false,
    createdAt: '2024-01-23T13:20:00Z',
    updatedAt: '2024-01-25T15:45:00Z',
    createdBy: 'Sarah Johnson',
    tags: ['email', 'template', 'welcome', 'onboarding'],
    description: 'Welcome email series template for new subscribers'
  }
]

export default function ContentHubPage() {
  const [assets] = useState<ContentAsset[]>(mockAssets)
  const [searchTerm, setSearchTerm] = useState('')
  const [typeFilter, setTypeFilter] = useState<string>('all')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [activeTab, setActiveTab] = useState('all')

  const filteredAssets = assets.filter(asset => {
    const matchesSearch = asset.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         asset.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         asset.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
    
    const matchesType = typeFilter === 'all' || asset.type === typeFilter
    const matchesStatus = statusFilter === 'all' || asset.status === statusFilter
    
    return matchesSearch && matchesType && matchesStatus
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'bg-gray-500'
      case 'review': return 'bg-yellow-500'
      case 'approved': return 'bg-green-500'
      case 'published': return 'bg-blue-500'
      default: return 'bg-gray-500'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'text': return <FileText className="h-5 w-5" />
      case 'image': return <Image className="h-5 w-5" />
      case 'video': return <Video className="h-5 w-5" />
      case 'audio': return <Headphones className="h-5 w-5" />
      case 'template': return <Copy className="h-5 w-5" />
      default: return <FileText className="h-5 w-5" />
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const totalAssets = assets.length
  const aiGeneratedAssets = assets.filter(asset => asset.aiGenerated).length
  const publishedAssets = assets.filter(asset => asset.status === 'published').length
  const draftAssets = assets.filter(asset => asset.status === 'draft').length

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Content Hub</h1>
          <p className="text-muted-foreground">
            AI-generated content and creative assets
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Sparkles className="mr-2 h-4 w-4" />
            Generate Content
          </Button>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Upload Asset
          </Button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Assets</CardTitle>
            <Palette className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalAssets}</div>
            <p className="text-xs text-muted-foreground">Across all types</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">AI Generated</CardTitle>
            <Sparkles className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{aiGeneratedAssets}</div>
            <p className="text-xs text-muted-foreground">Created by AI</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Published</CardTitle>
            <Share className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{publishedAssets}</div>
            <p className="text-xs text-muted-foreground">Live content</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">In Draft</CardTitle>
            <Edit className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{draftAssets}</div>
            <p className="text-xs text-muted-foreground">Work in progress</p>
          </CardContent>
        </Card>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="all">All Assets</TabsTrigger>
          <TabsTrigger value="recent">Recent</TabsTrigger>
          <TabsTrigger value="ai-generated">AI Generated</TabsTrigger>
          <TabsTrigger value="templates">Templates</TabsTrigger>
        </TabsList>

        <TabsContent value="all">
          <Card>
            <CardHeader>
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search content..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
                
                <Select value={typeFilter} onValueChange={setTypeFilter}>
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="Type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="text">Text</SelectItem>
                    <SelectItem value="image">Image</SelectItem>
                    <SelectItem value="video">Video</SelectItem>
                    <SelectItem value="template">Template</SelectItem>
                  </SelectContent>
                </Select>

                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="Status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="draft">Draft</SelectItem>
                    <SelectItem value="review">Review</SelectItem>
                    <SelectItem value="approved">Approved</SelectItem>
                    <SelectItem value="published">Published</SelectItem>
                  </SelectContent>
                </Select>

                <Button variant="outline" size="icon">
                  <Filter className="h-4 w-4" />
                </Button>
              </div>
            </CardHeader>

            <CardContent>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {filteredAssets.map((asset) => (
                  <Card key={asset.id} className="hover:shadow-md transition-shadow">
                    <CardContent className="p-6">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center gap-3">
                          {getTypeIcon(asset.type)}
                          <div>
                            <h3 className="font-semibold line-clamp-1">{asset.name}</h3>
                            <p className="text-sm text-muted-foreground capitalize">{asset.type}</p>
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
                              <Edit className="mr-2 h-4 w-4" />
                              Edit
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Download className="mr-2 h-4 w-4" />
                              Download
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Share className="mr-2 h-4 w-4" />
                              Share
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Copy className="mr-2 h-4 w-4" />
                              Duplicate
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>

                      <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
                        {asset.description}
                      </p>

                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-2">
                          <Badge className={`${getStatusColor(asset.status)} text-white text-xs`}>
                            {asset.status}
                          </Badge>
                          {asset.aiGenerated && (
                            <Badge variant="secondary" className="text-xs">
                              <Sparkles className="mr-1 h-3 w-3" />
                              AI
                            </Badge>
                          )}
                        </div>
                        
                        {(asset.fileSize || asset.duration) && (
                          <div className="text-xs text-muted-foreground">
                            {asset.fileSize && <span>{asset.fileSize}</span>}
                            {asset.duration && <span>{asset.duration}</span>}
                            {asset.dimensions && <span>{asset.dimensions}</span>}
                          </div>
                        )}
                      </div>

                      <div className="flex flex-wrap gap-1 mb-4">
                        {asset.tags.slice(0, 3).map((tag) => (
                          <Badge key={tag} variant="outline" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                        {asset.tags.length > 3 && (
                          <Badge variant="outline" className="text-xs">
                            +{asset.tags.length - 3}
                          </Badge>
                        )}
                      </div>

                      <div className="text-xs text-muted-foreground">
                        <p>Created: {formatDate(asset.createdAt)}</p>
                        <p>By: {asset.createdBy}</p>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="recent">
          <Card>
            <CardHeader>
              <CardTitle>Recent Assets</CardTitle>
              <CardDescription>Recently created or modified content</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-muted-foreground">
                <FileText className="h-16 w-16 mx-auto mb-4" />
                <p>Recent assets view coming soon</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="ai-generated">
          <Card>
            <CardHeader>
              <CardTitle>AI Generated Content</CardTitle>
              <CardDescription>Content created by AI agents</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-muted-foreground">
                <Sparkles className="h-16 w-16 mx-auto mb-4" />
                <p>AI content gallery coming soon</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="templates">
          <Card>
            <CardHeader>
              <CardTitle>Content Templates</CardTitle>
              <CardDescription>Reusable templates and layouts</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-muted-foreground">
                <Copy className="h-16 w-16 mx-auto mb-4" />
                <p>Template library coming soon</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}