'use client'

/**
 * Resources Page - Marketing Resources, Tools, Guides & Downloads
 * Comprehensive resource hub for marketing professionals and business owners
 */

import Link from 'next/link'
import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { 
  ArrowRight,
  Download,
  BookOpen,
  Video,
  Mic,
  Calculator,
  FileText,
  TrendingUp,
  Users,
  Target,
  Zap,
  Clock,
  Award,
  Search
} from 'lucide-react'

const resourceCategories = [
  'All Resources',
  'eBooks & Guides',
  'Templates',
  'Tools & Calculators',
  'Webinars',
  'Case Studies',
  'Podcasts',
  'Industry Reports'
]

const featuredResources = [
  {
    id: 1,
    title: "Complete Guide to AI Marketing Automation",
    description: "125-page comprehensive guide covering AI agents, campaign automation, and ROI optimization strategies.",
    category: "eBooks & Guides",
    type: "PDF Guide",
    pages: "125 pages",
    downloads: "15,000+",
    featured: true,
    icon: BookOpen,
    downloadLink: "#",
    preview: "Learn how 28+ AI agents work together to create, optimize, and scale marketing campaigns automatically."
  },
  {
    id: 2,
    title: "Marketing ROI Calculator & Dashboard Template",
    description: "Interactive spreadsheet template to calculate and track marketing ROI across all channels with AI optimization recommendations.",
    category: "Tools & Calculators",
    type: "Excel Template",
    pages: "Multi-sheet",
    downloads: "8,500+",
    featured: true,
    icon: Calculator,
    downloadLink: "#",
    preview: "Pre-built formulas for ROAS, LTV, CAC, and comprehensive reporting dashboards."
  }
]

const resources = [
  {
    id: 3,
    title: "30 AI Marketing Prompts for Campaign Creation",
    description: "Ready-to-use prompts for AI content generation, ad copy creation, and campaign strategy development.",
    category: "Templates",
    type: "Template Pack",
    downloads: "12,000+",
    icon: FileText,
    downloadLink: "#"
  },
  {
    id: 4,
    title: "B2B Lead Generation Playbook",
    description: "Step-by-step playbook for generating qualified B2B leads using AI-powered outreach and content strategies.",
    category: "eBooks & Guides",
    type: "PDF Guide",
    downloads: "6,800+",
    icon: BookOpen,
    downloadLink: "#"
  },
  {
    id: 5,
    title: "Social Media Automation Workshop",
    description: "60-minute masterclass on setting up AI agents for automated social media posting and engagement.",
    category: "Webinars",
    type: "Video",
    downloads: "4,200+",
    icon: Video,
    downloadLink: "#"
  },
  {
    id: 6,
    title: "E-commerce Marketing Checklist",
    description: "Complete checklist for optimizing e-commerce marketing with AI tools and automation workflows.",
    category: "Templates",
    type: "Checklist",
    downloads: "9,100+",
    icon: Target,
    downloadLink: "#"
  },
  {
    id: 7,
    title: "AI Marketing Trends Report 2025",
    description: "In-depth analysis of AI marketing trends, predictions, and opportunities for the coming year.",
    category: "Industry Reports",
    type: "Research Report",
    downloads: "7,500+",
    icon: TrendingUp,
    downloadLink: "#"
  },
  {
    id: 8,
    title: "Marketing Automation Podcast Series",
    description: "12-episode podcast series featuring AI marketing experts and successful automation case studies.",
    category: "Podcasts",
    type: "Audio Series",
    downloads: "3,600+",
    icon: Mic,
    downloadLink: "#"
  },
  {
    id: 9,
    title: "Campaign Performance Dashboard Template",
    description: "Real-time dashboard template for monitoring AI campaign performance across all marketing channels.",
    category: "Templates",
    type: "Dashboard",
    downloads: "5,400+",
    icon: Award,
    downloadLink: "#"
  }
]

const tools = [
  {
    name: "ROI Calculator",
    description: "Calculate marketing ROI and optimization potential",
    icon: Calculator
  },
  {
    name: "Campaign Planner",
    description: "AI-assisted campaign strategy and timeline planning",
    icon: Target
  },
  {
    name: "Content Generator",
    description: "AI-powered content ideas and copy generation",
    icon: Zap
  },
  {
    name: "Competitor Analyzer",
    description: "Analyze competitor marketing strategies and performance",
    icon: Search
  }
]

export default function ResourcesPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      {/* Hero Section */}
      <section className="py-16 lg:py-20">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <Badge variant="outline" className="mb-6">
              Marketing Resources Hub
            </Badge>
            
            <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl">
              Free Marketing Resources &
              <span className="text-primary"> AI Tools</span>
            </h1>
            
            <p className="mt-6 text-lg leading-8 text-muted-foreground max-w-2xl mx-auto">
              Access our comprehensive library of guides, templates, tools, and educational 
              content to accelerate your AI marketing journey.
            </p>
            
            <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="px-8 btn-gradient">
                Browse All Resources
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button variant="outline" size="lg">
                Newsletter Sign Up
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Access Tools */}
      <section className="py-16 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Free AI Marketing Tools
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Interactive tools to help you plan, calculate, and optimize your marketing
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {tools.map((tool, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <tool.icon className="h-12 w-12 text-primary mx-auto mb-4" />
                  <CardTitle className="text-lg">{tool.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-4">{tool.description}</p>
                  <Button size="sm" variant="outline">
                    Use Tool
                    <ArrowRight className="ml-1 h-3 w-3" />
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Category Filter */}
      <section className="py-8 border-b">
        <div className="container">
          <div className="flex flex-wrap gap-2 justify-center">
            {resourceCategories.map((category, index) => (
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

      {/* Featured Resources */}
      <section className="py-16">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Featured Resources
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Our most comprehensive and popular resources for AI marketing mastery
            </p>
          </div>
          
          <div className="grid lg:grid-cols-2 gap-8 mb-16">
            {featuredResources.map((resource) => (
              <Card key={resource.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center gap-4 mb-4">
                    <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                      <resource.icon className="h-6 w-6 text-primary" />
                    </div>
                    <div className="flex-1">
                      <Badge variant="secondary" className="text-xs mb-2">
                        {resource.category}
                      </Badge>
                      <Badge variant="outline" className="text-xs ml-2">
                        Featured
                      </Badge>
                    </div>
                  </div>
                  <CardTitle className="text-xl mb-2">{resource.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4">{resource.description}</p>
                  
                  <div className="bg-muted/50 rounded-lg p-3 mb-4">
                    <p className="text-sm text-foreground italic">"{resource.preview}"</p>
                  </div>
                  
                  <div className="flex items-center justify-between text-sm text-muted-foreground mb-4">
                    <div className="flex items-center space-x-4">
                      <span>{resource.type}</span>
                      {resource.pages && <span>{resource.pages}</span>}
                    </div>
                    <span>{resource.downloads} downloads</span>
                  </div>
                  
                  <Button className="w-full">
                    <Download className="mr-2 h-4 w-4" />
                    Download Free
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* All Resources Grid */}
      <section className="py-16 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Complete Resource Library
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Everything you need to master AI-powered marketing and automation
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {resources.map((resource) => (
              <Card key={resource.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                      <resource.icon className="h-5 w-5 text-primary" />
                    </div>
                    <Badge variant="outline" className="text-xs">
                      {resource.category}
                    </Badge>
                  </div>
                  <CardTitle className="text-lg mb-2">{resource.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-4">{resource.description}</p>
                  
                  <div className="flex items-center justify-between text-xs text-muted-foreground mb-4">
                    <span>{resource.type}</span>
                    <span>{resource.downloads} downloads</span>
                  </div>
                  
                  <Button size="sm" variant="outline" className="w-full">
                    <Download className="mr-2 h-3 w-3" />
                    Download
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
          
          <div className="text-center mt-12">
            <Button size="lg" variant="outline">
              Load More Resources
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="py-16">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Stay Updated with New Resources
            </h2>
            <p className="mt-4 text-lg text-muted-foreground mb-8">
              Get notified when we publish new guides, templates, and tools. 
              Plus receive exclusive AI marketing insights and tips.
            </p>
            
            <div className="bg-muted/30 rounded-lg p-8">
              <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-md mx-auto mb-6">
                <input 
                  type="email" 
                  placeholder="Enter your email address"
                  className="flex-1 px-4 py-2 rounded-md border border-input bg-background text-sm"
                />
                <Button className="btn-gradient">
                  Subscribe
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
              
              <p className="text-sm text-muted-foreground">
                Join 10,000+ marketers • Weekly resources • No spam • Unsubscribe anytime
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-primary text-primary-foreground">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Ready to Implement What You've Learned?
            </h2>
            <p className="mt-4 text-lg opacity-90">
              Take your marketing to the next level with our AI-powered automation platform 
              and expert consulting services.
            </p>
            
            <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/bizosaas">
                <Button size="lg" variant="secondary" className="px-8">
                  Try BizoSaaS Platform
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/contact">
                <Button size="lg" variant="outline" className="px-8 border-white text-white hover:bg-white hover:text-primary">
                  Get Expert Help
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