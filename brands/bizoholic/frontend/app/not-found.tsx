'use client'

/**
 * Enhanced 404 Not Found Page
 * With dark mode support and helpful navigation
 */

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import {
  Home,
  ArrowLeft,
  Search,
  FileQuestion,
  Bot,
  BarChart3,
  Mail,
  BookOpen
} from 'lucide-react'

export default function NotFound() {
  const popularPages = [
    {
      title: "Home",
      description: "Return to our homepage",
      href: "/",
      icon: Home
    },
    {
      title: "Services",
      description: "Explore our AI marketing services",
      href: "/services",
      icon: Bot
    },
    {
      title: "Blog",
      description: "Read marketing insights",
      href: "/blog",
      icon: BookOpen
    },
    {
      title: "About Us",
      description: "Learn about Bizoholic",
      href: "/about",
      icon: BarChart3
    },
    {
      title: "Contact",
      description: "Get in touch with us",
      href: "/contact",
      icon: Mail
    }
  ]

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-1 flex items-center justify-center py-20">
        <div className="container">
          <div className="mx-auto max-w-4xl">
            {/* 404 Icon and Message */}
            <div className="text-center mb-12">
              <div className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-muted mb-6">
                <FileQuestion className="h-12 w-12 text-muted-foreground" />
              </div>

              <h1 className="text-6xl font-bold text-foreground mb-4">404</h1>
              <h2 className="text-3xl font-bold text-foreground mb-4">
                Page Not Found
              </h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Sorry, we couldn't find the page you're looking for. The page may have been moved, deleted, or never existed.
              </p>
            </div>

            {/* Quick Actions */}
            <div className="flex items-center justify-center gap-4 mb-16">
              <Link href="/">
                <Button size="lg" className="px-8">
                  <Home className="mr-2 h-5 w-5" />
                  Go Home
                </Button>
              </Link>
              <Link href="/services">
                <Button variant="outline" size="lg">
                  <Search className="mr-2 h-5 w-5" />
                  Browse Services
                </Button>
              </Link>
            </div>

            {/* Popular Pages */}
            <div className="mb-12">
              <h3 className="text-2xl font-bold text-foreground text-center mb-8">
                Popular Pages
              </h3>

              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {popularPages.map((page, index) => {
                  const Icon = page.icon
                  return (
                    <Link key={index} href={page.href}>
                      <Card className="hover:shadow-lg transition-all duration-300 hover:scale-105 cursor-pointer group h-full">
                        <CardContent className="pt-6">
                          <div className="flex items-start space-x-4">
                            <div className="flex-shrink-0">
                              <div className="flex items-center justify-center w-12 h-12 rounded-lg bg-primary/10 group-hover:bg-primary/20 transition-colors">
                                <Icon className="h-6 w-6 text-primary" />
                              </div>
                            </div>
                            <div className="flex-1 min-w-0">
                              <h4 className="text-lg font-semibold text-foreground group-hover:text-primary transition-colors mb-1">
                                {page.title}
                              </h4>
                              <p className="text-sm text-muted-foreground">
                                {page.description}
                              </p>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    </Link>
                  )
                })}
              </div>
            </div>

            {/* Help Section */}
            <div className="bg-muted/30 rounded-lg border p-8 text-center">
              <h3 className="text-xl font-bold text-foreground mb-3">
                Still can't find what you're looking for?
              </h3>
              <p className="text-muted-foreground mb-6">
                Our team is here to help. Contact us and we'll get you to the right place.
              </p>
              <div className="flex items-center justify-center gap-4">
                <Link href="/contact">
                  <Button variant="outline">
                    <Mail className="mr-2 h-4 w-4" />
                    Contact Support
                  </Button>
                </Link>
                <Link href="/blog">
                  <Button variant="outline">
                    <BookOpen className="mr-2 h-4 w-4" />
                    Read Our Blog
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}