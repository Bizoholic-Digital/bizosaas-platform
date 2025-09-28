/**
 * Dynamic CMS Page Client Component
 * Handles interactive parts of the CMS page
 */

'use client'

import { useEffect } from 'react'
import Link from 'next/link'
import { Button } from '../../components/ui/button'
import { Badge } from '../../components/ui/badge'
import Header from '../../components/navigation/header'
import Footer from '../../components/navigation/footer'
import { ArrowRight, ArrowLeft, Clock, Edit, Eye } from 'lucide-react'

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

interface DynamicPageClientProps {
  slug: string
  initialPage: PageContent | null
  initialError: string | null
}

export default function DynamicPageClient({ slug, initialPage, initialError }: DynamicPageClientProps) {
  // Update document title when page loads
  useEffect(() => {
    if (initialPage?.meta?.seo_title) {
      document.title = initialPage.meta.seo_title
    } else if (initialPage?.title) {
      document.title = `${initialPage.title} - CorelDove`
    }
  }, [initialPage])

  if (initialError || !initialPage) {
    return (
      <div className="flex flex-col min-h-screen">
        <Header currentPath={`/${slug}`} />
        
        <main className="flex-1 py-16">
          <div className="container max-w-4xl text-center">
            <h1 className="text-4xl font-bold mb-4">Page Not Found</h1>
            <p className="text-muted-foreground mb-8">
              The page you're looking for doesn't exist or has been moved.
            </p>
            <div className="flex gap-4 justify-center">
              <Button asChild>
                <Link href="/">
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back to Home
                </Link>
              </Button>
              <Button variant="outline" asChild>
                <Link href="/contact">Contact Support</Link>
              </Button>
            </div>
          </div>
        </main>

        <Footer />
      </div>
    )
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Header currentPath={`/${slug}`} />
      
      {/* Breadcrumb */}
      <div className="border-b bg-muted/30 py-4">
        <div className="container max-w-4xl">
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-foreground">Home</Link>
            <ArrowRight className="h-4 w-4" />
            <span className="text-foreground">{initialPage.title}</span>
          </div>
        </div>
      </div>

      <main className="flex-1 py-8">
        <article className="container max-w-4xl">
          {/* Page Header */}
          <header className="mb-8">
            <h1 className="text-3xl font-bold mb-2">{initialPage.title}</h1>
            {initialPage.meta?.search_description && (
              <p className="text-muted-foreground">
                {initialPage.meta.search_description}
              </p>
            )}
          </header>

          {/* Page Content */}
          <div 
            className="prose prose-lg max-w-none prose-headings:text-foreground prose-p:text-foreground prose-li:text-foreground prose-strong:text-foreground"
            dangerouslySetInnerHTML={{ __html: initialPage.content }}
          />

          {/* Page Actions */}
          <footer className="mt-12 pt-8 border-t">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <Button variant="outline" asChild>
                  <Link href="/">
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Back to Home
                  </Link>
                </Button>
                
                <Button variant="outline" asChild>
                  <Link href="/contact">
                    Need Help? Contact Us
                  </Link>
                </Button>
              </div>

              {/* Edit link for client portal users (hidden from public) */}
              <div className="hidden">{/*
                Admin-only edit link - will be shown when user authentication is implemented
                <Button variant="ghost" size="sm" className="text-muted-foreground" asChild>
                  <Link href={`/client-portal/pages/${slug}/edit`}>
                    <Edit className="mr-2 h-4 w-4" />
                    Edit in Client Portal
                  </Link>
                </Button>
              */}</div>
            </div>
          </footer>
        </article>
      </main>

      <Footer />
    </div>
  )
}