/**
 * Bizoholic Digital Marketing Website Homepage
 * Public marketing site for Bizoholic Digital services
 * (This should be served from Wagtail CMS on localhost:3000)
 */

import Link from 'next/link'
import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  ArrowRight, 
  Bot, 
  Users, 
  Zap, 
  Target, 
  BarChart3, 
  Globe,
  CheckCircle,
  Star
} from 'lucide-react'

export default function MarketingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center space-x-2">
            <Image
              src="/bizoholic-logo-hq.png"
              alt="Bizoholic Digital Logo"
              width={40}
              height={40}
              className="h-8 w-auto"
              priority
            />
            <span className="font-bold text-xl text-foreground">Bizoholic Digital</span>
          </Link>
          
          <nav className="hidden md:flex items-center space-x-6 text-sm font-medium">
            <Link href="#services" className="text-foreground/60 hover:text-foreground">Services</Link>
            <Link href="#about" className="text-foreground/60 hover:text-foreground">About</Link>
            <Link href="#contact" className="text-foreground/60 hover:text-foreground">Contact</Link>
          </nav>
          
          <div className="flex items-center space-x-4">
            <Link href="/auth/login">
              <Button variant="outline" size="sm">
                Sign In
              </Button>
            </Link>
            <Link href="/auth/login">
              <Button size="sm">
                Get Started
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 lg:py-28">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <Badge variant="outline" className="mb-6">
              <Bot className="mr-2 h-3 w-3" />
              AI-Powered Marketing Automation
            </Badge>
            
            <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-7xl">
              Transform Your Business with{' '}
              <span className="text-primary">AI Marketing</span>
            </h1>
            
            <p className="mt-6 text-lg leading-8 text-muted-foreground max-w-2xl mx-auto">
              Bizoholic Digital empowers businesses with autonomous AI agents that handle marketing campaigns, 
              content creation, SEO optimization, and lead generation - all running 24/7 on autopilot.
            </p>
            
            <div className="mt-10 flex items-center justify-center gap-6">
              <Link href="/auth/login">
                <Button size="lg" className="px-8">
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Button variant="outline" size="lg">
                Watch Demo
              </Button>
            </div>

            <div className="mt-10 flex items-center justify-center space-x-6 text-sm text-muted-foreground">
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <span>No Credit Card Required</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <span>14-Day Free Trial</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <span>Cancel Anytime</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="services" className="py-20 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Everything You Need to Dominate Digital Marketing
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Our AI agents work around the clock to optimize your marketing performance
            </p>
          </div>
          
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <Bot className="h-8 w-8 text-primary mb-2" />
                <CardTitle>AI Campaign Management</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Autonomous agents create, optimize, and manage your advertising campaigns across Google Ads, 
                  Meta, LinkedIn, and 40+ other platforms.
                </p>
              </CardContent>
            </Card>
            
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <Target className="h-8 w-8 text-primary mb-2" />
                <CardTitle>Content Generation</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  AI-powered content creation for blogs, social media, email campaigns, and website copy 
                  that converts visitors into customers.
                </p>
              </CardContent>
            </Card>
            
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <BarChart3 className="h-8 w-8 text-primary mb-2" />
                <CardTitle>Performance Analytics</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Real-time analytics and insights with automated reporting that helps you understand 
                  what's working and what needs optimization.
                </p>
              </CardContent>
            </Card>
            
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <Users className="h-8 w-8 text-primary mb-2" />
                <CardTitle>Lead Generation</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Automated lead discovery, qualification, and nurturing systems that convert prospects 
                  into paying customers while you sleep.
                </p>
              </CardContent>
            </Card>
            
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <Globe className="h-8 w-8 text-primary mb-2" />
                <CardTitle>SEO Optimization</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  AI agents continuously optimize your website for search engines, improving rankings 
                  and driving organic traffic growth.
                </p>
              </CardContent>
            </Card>
            
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <Zap className="h-8 w-8 text-primary mb-2" />
                <CardTitle>Marketing Automation</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Complete marketing workflow automation including email sequences, social media posting, 
                  and customer journey optimization.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Ready to Scale Your Business?
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Join thousands of businesses already using AI to transform their marketing results.
            </p>
            
            <div className="mt-8 flex items-center justify-center gap-4">
              <div className="flex items-center space-x-1">
                {[1,2,3,4,5].map((star) => (
                  <Star key={star} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                ))}
                <span className="ml-2 text-sm text-muted-foreground">4.9/5 from 1,000+ reviews</span>
              </div>
            </div>
            
            <div className="mt-8">
              <Link href="/auth/login">
                <Button size="lg" className="px-12">
                  Start Your Free Trial Today
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-muted/30">
        <div className="container py-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Image
                src="/bizoholic-logo-hq.png"
                alt="Bizoholic Digital Logo"
                width={32}
                height={32}
                className="h-6 w-auto"
              />
              <span className="font-semibold text-foreground">Bizoholic Digital</span>
            </div>
            
            <p className="text-sm text-muted-foreground">
              © 2024 Bizoholic Digital. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}