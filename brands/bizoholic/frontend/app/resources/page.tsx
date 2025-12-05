'use client'

import Link from 'next/link'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, FileText, Video, Download, BookOpen } from 'lucide-react'

const resources = [
  {
    title: 'The Future of AI Marketing',
    type: 'Whitepaper',
    description: 'A comprehensive guide to how artificial intelligence is reshaping the digital marketing landscape in 2024.',
    icon: FileText,
    category: 'AI Trends'
  },
  {
    title: 'SEO Best Practices Guide',
    type: 'E-Book',
    description: 'Master the art of search engine optimization with our step-by-step guide to ranking higher on Google.',
    icon: BookOpen,
    category: 'SEO'
  },
  {
    title: 'Social Media Masterclass',
    type: 'Webinar',
    description: 'Watch our recorded webinar on how to build a loyal community and drive engagement on social platforms.',
    icon: Video,
    category: 'Social Media'
  },
  {
    title: 'Marketing ROI Calculator',
    type: 'Tool',
    description: 'Download our free spreadsheet tool to calculate and forecast your marketing return on investment.',
    icon: Download,
    category: 'Analytics'
  },
  {
    title: 'Content Strategy Template',
    type: 'Template',
    description: 'A ready-to-use template for planning your content calendar and strategy for the entire year.',
    icon: FileText,
    category: 'Content'
  },
  {
    title: 'Email Marketing Checklist',
    type: 'Checklist',
    description: 'Ensure your email campaigns are perfect before hitting send with this comprehensive checklist.',
    icon: FileText,
    category: 'Email'
  }
]

export default function ResourcesPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      {/* Hero Section */}
      <section className="py-20 bg-muted/30">
        <div className="container text-center">
          <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl mb-6">
            Marketing Resources
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
            Expert insights, guides, and tools to help you grow your business and master digital marketing.
          </p>
        </div>
      </section>

      {/* Resources Grid */}
      <section className="py-20">
        <div className="container">
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {resources.map((resource, index) => (
              <Card key={index} className="h-full hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 rounded-lg bg-primary/10 text-primary">
                      <resource.icon className="h-6 w-6" />
                    </div>
                    <Badge variant="outline">{resource.type}</Badge>
                  </div>
                  <div className="mb-2">
                    <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      {resource.category}
                    </span>
                  </div>
                  <CardTitle className="text-xl">
                    {resource.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base mb-6">
                    {resource.description}
                  </CardDescription>
                  <Button variant="outline" className="w-full group">
                    Access Resource
                    <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="py-20 bg-primary text-primary-foreground">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-6">Stay Updated</h2>
          <p className="text-xl opacity-90 mb-10 max-w-2xl mx-auto">
            Subscribe to our newsletter to get the latest marketing insights and resources delivered to your inbox.
          </p>
          <div className="max-w-md mx-auto flex gap-4">
            <input 
              type="email" 
              placeholder="Enter your email" 
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 text-foreground"
            />
            <Button variant="secondary">Subscribe</Button>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}
