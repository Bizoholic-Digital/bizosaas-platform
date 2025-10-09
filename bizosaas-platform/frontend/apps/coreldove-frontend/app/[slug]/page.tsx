/**
 * Dynamic CMS Page - Renders content from Wagtail CMS
 * Supports all footer pages and any custom pages created in the CMS
 */

import DynamicPageClient from './page-client'

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

interface PageResponse {
  meta: {
    total_count: number
  }
  items: PageContent[]
}

// Server component that fetches the page data
export default async function DynamicPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  let pageData: PageContent | null = null
  let error: string | null = null

  try {
    // Fetch page data on the server
    const response = await fetch(`${process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3012'}/api/brain/wagtail/pages?slug=${slug}`, {
      // Disable caching for development - in production you might want to enable it
      cache: 'no-store'
    })
    
    if (response.ok) {
      const data: PageResponse = await response.json()
      if (data.items && data.items.length > 0) {
        pageData = data.items[0]
      } else {
        error = 'Page not found'
      }
    } else {
      error = 'Failed to load page content'
    }
  } catch (err) {
    console.error('Error fetching page:', err)
    error = 'Failed to load page content'
  }

  // Pass the data to the client component
  return <DynamicPageClient slug={slug} initialPage={pageData} initialError={error} />
}

// Generate metadata for SEO
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3012'}/api/brain/wagtail/pages?slug=${slug}`)
    
    if (response.ok) {
      const data: PageResponse = await response.json()
      const page = data.items?.[0]
      
      if (page) {
        return {
          title: page.meta?.seo_title || `${page.title} - CorelDove`,
          description: page.meta?.search_description || `Learn more about ${page.title}`,
          openGraph: {
            title: page.meta?.seo_title || page.title,
            description: page.meta?.search_description,
            type: 'article'
          }
        }
      }
    }
  } catch (error) {
    console.error('Error generating metadata:', error)
  }

  return {
    title: 'Page - CorelDove',
    description: 'Page content from CorelDove'
  }
}