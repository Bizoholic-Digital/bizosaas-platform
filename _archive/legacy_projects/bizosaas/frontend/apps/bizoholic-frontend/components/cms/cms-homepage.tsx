/**
 * CMS-Powered Homepage Component
 * Uses Wagtail CMS content with fallback to static content
 */

"use client"

import { useEffect, useState } from 'react'
import { wagtailCMS, WagtailPage } from '@/lib/wagtail-cms'
import { CMSPage } from '@/components/cms/content-blocks'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { Skeleton } from '@/components/ui/skeleton'

// Import the static homepage component as fallback
import StaticHomePage from '@/components/static-homepage'

export default function CMSHomePage() {
  const [cmsPage, setCMSPage] = useState<WagtailPage | null>(null)
  const [loading, setLoading] = useState(true)
  const [useCMS, setUseCMS] = useState(false)

  useEffect(() => {
    const fetchHomePage = async () => {
      try {
        setLoading(true)
        
        // Try to fetch the homepage from Wagtail CMS
        const page = await wagtailCMS.getPage('home')
        
        if (page && page.content_blocks && page.content_blocks.length > 0) {
          setCMSPage(page)
          setUseCMS(true)
          console.log('✅ Using CMS content for homepage')
        } else {
          console.log('⚠️ No CMS content found, using static homepage')
          setUseCMS(false)
        }
      } catch (error) {
        console.warn('CMS integration error:', error)
        setUseCMS(false)
      } finally {
        setLoading(false)
      }
    }

    fetchHomePage()
  }, [])

  // Show loading skeleton while fetching CMS content
  if (loading) {
    return (
      <div className="flex flex-col min-h-screen">
        <Header />
        <div className="container py-20">
          <div className="max-w-4xl mx-auto space-y-8">
            <div className="text-center space-y-4">
              <Skeleton className="h-12 w-3/4 mx-auto" />
              <Skeleton className="h-6 w-1/2 mx-auto" />
              <div className="flex gap-4 justify-center">
                <Skeleton className="h-10 w-32" />
                <Skeleton className="h-10 w-32" />
              </div>
            </div>
            <div className="grid md:grid-cols-3 gap-6">
              {Array.from({ length: 6 }).map((_, i) => (
                <Skeleton key={i} className="h-48" />
              ))}
            </div>
          </div>
        </div>
        <Footer />
      </div>
    )
  }

  // Use CMS content if available
  if (useCMS && cmsPage) {
    return (
      <div className="flex flex-col min-h-screen">
        <Header />
        <CMSPage page={cmsPage} className="flex-1" />
        <Footer />
      </div>
    )
  }

  // Fallback to static homepage
  return <StaticHomePage />
}

// Component for managing CMS integration status
export function CMSIntegrationStatus() {
  const [status, setStatus] = useState<'checking' | 'connected' | 'fallback'>('checking')
  const [pageCount, setPageCount] = useState(0)

  useEffect(() => {
    const checkCMSStatus = async () => {
      try {
        // Test CMS connection
        const page = await wagtailCMS.getPage('home')
        const contentPages = await wagtailCMS.getContentPages(5)
        
        if (page || contentPages.length > 0) {
          setStatus('connected')
          setPageCount(contentPages.length)
        } else {
          setStatus('fallback')
        }
      } catch (error) {
        setStatus('fallback')
      }
    }

    checkCMSStatus()
  }, [])

  const statusConfig = {
    checking: {
      color: 'bg-yellow-500',
      text: 'Checking CMS connection...',
      description: 'Verifying Wagtail CMS integration'
    },
    connected: {
      color: 'bg-green-500',
      text: 'CMS Connected',
      description: `Wagtail CMS is active with ${pageCount} content pages`
    },
    fallback: {
      color: 'bg-blue-500',
      text: 'Using Static Content',
      description: 'CMS not available, using fallback content'
    }
  }

  const config = statusConfig[status]

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <div className="bg-background border rounded-lg p-3 shadow-lg max-w-sm">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${config.color}`} />
          <span className="font-medium text-sm">{config.text}</span>
        </div>
        <p className="text-xs text-muted-foreground mt-1">
          {config.description}
        </p>
      </div>
    </div>
  )
}

// Hook for CMS-aware routing
export function useCMSRouting() {
  const [cmsEnabled, setCMSEnabled] = useState(false)
  
  useEffect(() => {
    const checkCMS = async () => {
      try {
        const page = await wagtailCMS.getPage('home')
        setCMSEnabled(!!page)
      } catch {
        setCMSEnabled(false)
      }
    }
    
    checkCMS()
  }, [])
  
  return { cmsEnabled }
}