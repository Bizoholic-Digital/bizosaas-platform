"use client"

import Link from 'next/link'
import { ArrowRight, Calendar, Clock, User, Bot } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'

const featuredPost = {
  id: 1,
  title: 'The Future of AI-Driven Marketing: 28 Agents Working in Harmony',
  excerpt: 'Discover how our revolutionary BizoSaaS platform uses specialized AI agents to transform marketing campaigns and deliver unprecedented results.',
  content: 'A deep dive into how autonomous marketing works...',
  author: 'Bizoholic AI Team',
  date: '2025-01-15',
  readTime: '8 min read',
  category: 'AI Marketing',
  featured: true,
  image: '/api/placeholder/800/400'
}

const blogPosts = [
  {
    id: 2,
    title: 'How AI Agents Optimize Google Ads Campaigns in Real-Time',
    excerpt: 'Learn how our specialized advertising agents continuously monitor and optimize your Google Ads campaigns for maximum ROI.',
    author: 'Marketing Strategy Team',
    date: '2025-01-12',
    readTime: '6 min read',
    category: 'Google Ads',
    featured: false
  },
  {
    id: 3,
    title: 'Customer Success: 300% ROI Increase with Autonomous Marketing',
    excerpt: 'Real case study showing how a mid-size business achieved unprecedented growth using our AI-powered marketing automation.',
    author: 'Success Team',
    date: '2025-01-10',
    readTime: '5 min read',
    category: 'Case Studies',
    featured: false
  },
  {
    id: 4,
    title: 'Multi-Platform Campaign Management: Meta, LinkedIn & Beyond',
    excerpt: 'Explore how our AI agents manage campaigns across multiple advertising platforms simultaneously for optimal results.',
    author: 'Platform Integration Team',
    date: '2025-01-08',
    readTime: '7 min read',
    category: 'Multi-Platform',
    featured: false
  },
  {
    id: 5,
    title: 'The Science Behind Predictive Analytics in Marketing',
    excerpt: 'Understanding how machine learning algorithms predict customer behavior and optimize marketing strategies in real-time.',
    author: 'AI Research Team',
    date: '2025-01-05',
    readTime: '9 min read',
    category: 'Analytics',
    featured: false
  },
  {
    id: 6,
    title: 'Building Enterprise-Grade Marketing Automation',
    excerpt: 'Insights into the technical architecture that powers our scalable, secure, and SOC 2 compliant marketing platform.',
    author: 'Engineering Team',
    date: '2025-01-03',
    readTime: '6 min read',
    category: 'Technology',
    featured: false
  },
  {
    id: 7,
    title: '2025 Digital Marketing Trends: AI Takes Center Stage',
    excerpt: 'Our predictions for the marketing industry this year, focusing on autonomous systems and intelligent automation.',
    author: 'Strategy Team',
    date: '2025-01-01',
    readTime: '8 min read',
    category: 'Trends',
    featured: false
  }
]

const categories = [
  'All Posts',
  'AI Marketing',
  'Google Ads',
  'Case Studies',
  'Multi-Platform',
  'Analytics',
  'Technology',
  'Trends'
]

export default function BlogPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      {/* Hero Section */}
      <section className="relative py-20 md:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5" />
        <div className="container relative">
          <div className="mx-auto max-w-3xl text-center">
            <Badge variant="outline" className="mb-6">
              Latest Insights & Updates
            </Badge>
            
            <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
              AI Marketing
              <span className="text-primary"> Insights</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-muted-foreground mb-8">
              Stay ahead of the curve with expert insights, industry analysis, 
              and the latest developments in AI-powered marketing automation.
            </p>
            
            <Badge variant="secondary" className="text-sm">
              Updated Weekly • Expert Analysis • Industry Trends
            </Badge>
          </div>
        </div>
      </section>

      {/* Featured Post */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              <span className="text-primary">Featured</span> Article
            </h2>
            <p className="text-lg text-muted-foreground">
              Our latest deep dive into the future of autonomous marketing.
            </p>
          </div>
          
          <Card className="hover:shadow-lg transition-shadow max-w-4xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-8">
              <div className="lg:order-2 p-8">
                <div className="flex items-center gap-4 mb-4">
                  <Badge variant="secondary" className="text-xs">
                    {featuredPost.category}
                  </Badge>
                  <Badge variant="outline" className="text-xs">
                    Featured
                  </Badge>
                </div>
                <CardTitle className="text-2xl mb-4">{featuredPost.title}</CardTitle>
                <CardDescription className="text-base mb-6">
                  {featuredPost.excerpt}
                </CardDescription>
                <div className="flex items-center gap-4 text-sm text-muted-foreground mb-6">
                  <div className="flex items-center gap-1">
                    <User className="h-4 w-4" />
                    {featuredPost.author}
                  </div>
                  <div className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    {new Date(featuredPost.date).toLocaleDateString('en-US', { 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    {featuredPost.readTime}
                  </div>
                </div>
                <Button>
                  Read Full Article
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
              <div className="lg:order-1 bg-gradient-to-br from-primary/10 to-accent/10 rounded-lg flex items-center justify-center p-8">
                <Bot className="h-32 w-32 text-primary" />
              </div>
            </div>
          </Card>
        </div>
      </section>

      {/* Category Filter */}
      <section className="py-8 border-b">
        <div className="container">
          <div className="flex flex-wrap gap-2 justify-center">
            {categories.map((category, index) => (
              <Badge 
                key={index} 
                variant={index === 0 ? "default" : "outline"} 
                className="cursor-pointer hover:bg-primary hover:text-primary-foreground transition-colors"
              >
                {category}
              </Badge>
            ))}
          </div>
        </div>
      </section>

      {/* Blog Posts Grid */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Latest <span className="text-primary">Articles</span>
            </h2>
            <p className="text-lg text-muted-foreground">
              Expert insights and analysis from our AI marketing specialists.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {blogPosts.map((post, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between mb-4">
                    <Badge variant="secondary" className="text-xs">
                      {post.category}
                    </Badge>
                  </div>
                  <CardTitle className="text-xl mb-2">{post.title}</CardTitle>
                  <CardDescription className="text-base">
                    {post.excerpt}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground mb-4">
                    <div className="flex items-center gap-1">
                      <User className="h-4 w-4" />
                      {post.author}
                    </div>
                    <div className="flex items-center gap-1">
                      <Clock className="h-4 w-4" />
                      {post.readTime}
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="text-sm text-muted-foreground">
                      {new Date(post.date).toLocaleDateString('en-US', { 
                        year: 'numeric', 
                        month: 'short', 
                        day: 'numeric' 
                      })}
                    </div>
                    <Button variant="ghost" size="sm">
                      Read More
                      <ArrowRight className="ml-2 h-3 w-3" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Stay <span className="text-primary">Updated</span>
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Get the latest AI marketing insights, platform updates, and industry 
              analysis delivered directly to your inbox.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-md mx-auto mb-8">
              <input 
                type="email" 
                placeholder="Enter your email address"
                className="flex-1 px-4 py-2 rounded-md border border-input bg-background text-sm"
              />
              <Button>
                Subscribe
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
            
            <p className="text-sm text-muted-foreground">
              Join 5,000+ marketing professionals • No spam • Unsubscribe anytime
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to experience AI marketing?
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Don't just read about the future of marketing - experience it firsthand 
              with our BizoSaaS platform and expert consulting services.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/bizosaas">
                <Button size="lg" className="btn-gradient">
                  Try BizoSaaS Platform
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/contact">
                <Button variant="outline" size="lg">
                  Schedule Consultation
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
      
      <Footer />
    </div>
  )
}