/**
 * Client Portal - Page Editor
 * Allows clients to edit CMS page content through Wagtail backend
 */

'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { ArrowLeft, Save, Eye, AlertCircle, CheckCircle, Edit } from 'lucide-react'

interface PageContent {
  id: number
  title: string
  slug: string
  content: string
  meta: {
    seo_title?: string
    search_description?: string
  }
  last_published_at?: string
}

interface PageEditorProps {
  params: Promise<{ slug: string }>
}

export default function PageEditor({ params }: PageEditorProps) {
  const router = useRouter()
  const [slug, setSlug] = useState<string>('')
  
  const [pageData, setPageData] = useState<PageContent | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  
  // Resolve params in useEffect
  useEffect(() => {
    params.then(resolvedParams => {
      setSlug(resolvedParams.slug)
    })
  }, [params])
  const [saveStatus, setSaveStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [error, setError] = useState<string | null>(null)
  
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    seo_title: '',
    search_description: ''
  })

  // Load page data on mount
  useEffect(() => {
    const loadPageData = async () => {
      try {
        const response = await fetch(`/api/brain/wagtail/pages?slug=${slug}`)
        const data = await response.json()
        
        if (data.items && data.items.length > 0) {
          const page = data.items[0]
          setPageData(page)
          setFormData({
            title: page.title,
            content: page.content,
            seo_title: page.meta?.seo_title || '',
            search_description: page.meta?.search_description || ''
          })
        } else {
          setError('Page not found')
        }
      } catch (err) {
        console.error('Error loading page:', err)
        setError('Failed to load page content')
      } finally {
        setIsLoading(false)
      }
    }

    if (slug) {
      loadPageData()
    }
  }, [slug])

  const handleSave = async () => {
    setIsSaving(true)
    setSaveStatus('idle')
    
    try {
      const response = await fetch(`/api/brain/wagtail/pages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id: pageData?.id,
          slug: slug,
          title: formData.title,
          content: formData.content,
          meta: {
            seo_title: formData.seo_title,
            search_description: formData.search_description
          }
        }),
      })

      if (response.ok) {
        setSaveStatus('success')
        // Update pageData with saved content
        if (pageData) {
          setPageData({
            ...pageData,
            title: formData.title,
            content: formData.content,
            meta: {
              seo_title: formData.seo_title,
              search_description: formData.search_description
            },
            last_published_at: new Date().toISOString()
          })
        }
      } else {
        setSaveStatus('error')
      }
    } catch (error) {
      console.error('Error saving page:', error)
      setSaveStatus('error')
    } finally {
      setIsSaving(false)
    }
  }

  const handlePreview = () => {
    // Open the live page in a new tab
    window.open(`http://localhost:3012/${slug}`, '_blank')
  }

  if (isLoading) {
    return (
      <div className="container max-w-4xl py-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading page editor...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container max-w-4xl py-8">
        <Card className="border-red-200">
          <CardContent className="pt-6 text-center">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2">Error Loading Page</h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <Button onClick={() => router.back()} variant="outline">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Go Back
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container max-w-6xl py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-4">
          <Button onClick={() => router.back()} variant="outline" size="sm">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Button>
          <div>
            <h1 className="text-2xl font-bold">Edit Page</h1>
            <p className="text-gray-600">/{slug}</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          {saveStatus === 'success' && (
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              <CheckCircle className="w-3 h-3 mr-1" />
              Saved
            </Badge>
          )}
          {saveStatus === 'error' && (
            <Badge variant="destructive">
              <AlertCircle className="w-3 h-3 mr-1" />
              Error
            </Badge>
          )}
          
          <Button onClick={handlePreview} variant="outline" size="sm">
            <Eye className="mr-2 h-4 w-4" />
            Preview
          </Button>
          
          <Button onClick={handleSave} disabled={isSaving} size="sm">
            {isSaving ? (
              <>
                <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                Saving...
              </>
            ) : (
              <>
                <Save className="mr-2 h-4 w-4" />
                Save Changes
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Content Editor */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Main Editor */}
        <div className="lg:col-span-2 space-y-6">
          {/* Page Content */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Edit className="mr-2 h-5 w-5" />
                Page Content
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Page Title</label>
                <Input
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  placeholder="Enter page title"
                />
              </div>
              
              <div>
                <label className="text-sm font-medium mb-2 block">Content (HTML)</label>
                <textarea
                  className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
                  rows={20}
                  value={formData.content}
                  onChange={(e) => setFormData({...formData, content: e.target.value})}
                  placeholder="Enter HTML content..."
                />
                <p className="text-xs text-gray-500 mt-1">
                  You can use HTML tags like &lt;h1&gt;, &lt;p&gt;, &lt;ul&gt;, &lt;li&gt;, &lt;strong&gt;, etc.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* SEO Settings */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">SEO Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">SEO Title</label>
                <Input
                  value={formData.seo_title}
                  onChange={(e) => setFormData({...formData, seo_title: e.target.value})}
                  placeholder="SEO-optimized title"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Recommended: 50-60 characters
                </p>
              </div>
              
              <div>
                <label className="text-sm font-medium mb-2 block">Meta Description</label>
                <textarea
                  className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                  rows={3}
                  value={formData.search_description}
                  onChange={(e) => setFormData({...formData, search_description: e.target.value})}
                  placeholder="Brief description for search engines"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Recommended: 150-160 characters
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Page Info */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Page Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Slug:</span>
                <span className="font-mono">/{slug}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Status:</span>
                <Badge variant="secondary">Published</Badge>
              </div>
              {pageData?.last_published_at && (
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Last Updated:</span>
                  <span>{new Date(pageData.last_published_at).toLocaleDateString()}</span>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Help */}
          <Card className="bg-blue-50">
            <CardHeader>
              <CardTitle className="text-lg text-blue-900">Help & Tips</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-blue-800 space-y-2">
              <p><strong>HTML Formatting:</strong> Use standard HTML tags to format your content.</p>
              <p><strong>SEO:</strong> Keep titles under 60 characters and descriptions under 160 characters.</p>
              <p><strong>Preview:</strong> Use the Preview button to see how your page looks live.</p>
              <p><strong>Auto-save:</strong> Changes are saved when you click "Save Changes".</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}