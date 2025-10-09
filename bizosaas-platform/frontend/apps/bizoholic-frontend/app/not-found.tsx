import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { MainHeader } from '@/components/layout/main-header'
import { Home, Search, ArrowLeft, Bot, MessageCircle } from 'lucide-react'

export default function NotFound() {
  return (
    <div className="min-h-screen bg-background">
      <MainHeader showNavigation={false} />
      
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto text-center">
          {/* 404 Header */}
          <div className="mb-8">
            <h1 className="text-9xl font-bold text-primary/20 mb-4">404</h1>
            <h2 className="text-3xl font-bold text-foreground mb-4">Page Not Found</h2>
            <p className="text-lg text-muted-foreground mb-8">
              The page you're looking for doesn't exist or has been moved.
            </p>
          </div>

          {/* Quick Actions */}
          <div className="grid gap-4 md:grid-cols-2 mb-8">
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg flex items-center justify-center">
                  <Home className="h-5 w-5 mr-2" />
                  Go Home
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">
                  Return to our homepage and explore our AI marketing platform
                </p>
                <Button asChild className="w-full">
                  <Link href="/">
                    <Home className="h-4 w-4 mr-2" />
                    Homepage
                  </Link>
                </Button>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg flex items-center justify-center">
                  <Search className="h-5 w-5 mr-2" />
                  Explore Services
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">
                  Discover our comprehensive AI marketing services and solutions
                </p>
                <Button asChild variant="outline" className="w-full">
                  <Link href="/services">
                    <Search className="h-4 w-4 mr-2" />
                    View Services
                  </Link>
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Popular Pages */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Popular Pages</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-2 md:grid-cols-2 lg:grid-cols-3">
                <Button asChild variant="ghost" className="justify-start">
                  <Link href="/onboarding">
                    <Bot className="h-4 w-4 mr-2" />
                    Get Started
                  </Link>
                </Button>
                <Button asChild variant="ghost" className="justify-start">
                  <Link href="/directory">
                    <Search className="h-4 w-4 mr-2" />
                    Business Directory
                  </Link>
                </Button>
                <Button asChild variant="ghost" className="justify-start">
                  <Link href="/about">
                    <MessageCircle className="h-4 w-4 mr-2" />
                    About Us
                  </Link>
                </Button>
                <Button asChild variant="ghost" className="justify-start">
                  <Link href="/contact">
                    <MessageCircle className="h-4 w-4 mr-2" />
                    Contact Support
                  </Link>
                </Button>
                <Button asChild variant="ghost" className="justify-start">
                  <Link href="/auth/login">
                    <ArrowLeft className="h-4 w-4 mr-2" />
                    Sign In
                  </Link>
                </Button>
                <Button asChild variant="ghost" className="justify-start">
                  <Link href="/blog">
                    <MessageCircle className="h-4 w-4 mr-2" />
                    Blog
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Help Section */}
          <Card>
            <CardHeader>
              <CardTitle>Need Help?</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-4">
                If you believe this is an error or need assistance, our support team is here to help.
              </p>
              <div className="flex flex-col sm:flex-row gap-2 justify-center">
                <Button asChild>
                  <Link href="/contact">
                    <MessageCircle className="h-4 w-4 mr-2" />
                    Contact Support
                  </Link>
                </Button>
                <Button asChild variant="outline">
                  <Link href="/onboarding">
                    <Bot className="h-4 w-4 mr-2" />
                    Start Free Trial
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}