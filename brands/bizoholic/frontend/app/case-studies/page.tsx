'use client'
import { useState, useEffect } from 'react'

import Link from 'next/link'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, TrendingUp, Users, BarChart3, Globe } from 'lucide-react'

const caseStudies = [
  {
    client: 'TechStartup Inc',
    industry: 'SaaS',
    title: 'How TechStartup Inc Scaled to $1M ARR in 6 Months',
    description: 'Using our AI campaign management, TechStartup Inc achieved 300% growth in qualified leads while reducing CAC by 40%.',
    metrics: [
      { label: 'Revenue Growth', value: '+300%' },
      { label: 'CAC Reduction', value: '-40%' },
      { label: 'Lead Quality', value: 'High' }
    ],
    image: '/case-studies/tech-startup.jpg',
    category: 'Growth'
  },
  {
    client: 'EcoStore',
    industry: 'E-commerce',
    title: 'EcoStore\'s Journey to 10x ROI with AI Marketing',
    description: 'A sustainable fashion brand leveraged our predictive analytics to optimize inventory and ad spend, resulting in record profits.',
    metrics: [
      { label: 'ROI', value: '10x' },
      { label: 'Sales', value: '+250%' },
      { label: 'Ad Spend', value: '-20%' }
    ],
    image: '/case-studies/eco-store.jpg',
    category: 'E-commerce'
  }
]


export default function CaseStudiesPage() {
  const [studies, setStudies] = useState<any[]>(caseStudies)

  useEffect(() => {
    const fetchCaseStudies = async () => {
      try {
        const res = await fetch('/api/brain/wordpress/case-studies')
        if (res.ok) {
          const data = await res.json()
          if (Array.isArray(data) && data.length > 0) {
            const mappedStudies = data.map((item: any) => ({
              client: item.title?.rendered || 'Client',
              industry: item.acf?.industry || 'General',
              title: item.title?.rendered,
              description: item.acf?.description || item.excerpt?.rendered?.replace(/<[^>]*>?/gm, ''),
              metrics: item.acf?.metrics || [],
              image: item.acf?.image || '/case-studies/placeholder.jpg',
              category: item.acf?.category || 'Growth'
            }))
            setStudies(mappedStudies)
          }
        }
      } catch (e) {
        console.error("Failed to fetch case studies", e)
      }
    }
    fetchCaseStudies()
  }, [])

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      {/* Hero Section */}
      <section className="py-20 bg-muted/30">
        <div className="container text-center">
          <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl mb-6">
            Client Success Stories
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
            See how businesses across industries are transforming their growth with our AI-powered platform.
          </p>
        </div>
      </section>

      {/* Case Studies Grid */}
      <section className="py-20">
        <div className="container">
          <div className="grid gap-8 md:grid-cols-2">
            {studies.map((study, index) => (
              <Card key={index} className="overflow-hidden hover:shadow-lg transition-shadow">
                <div className="h-48 bg-muted relative">
                  {/* Placeholder for image */}
                  <div className="absolute inset-0 flex items-center justify-center text-muted-foreground bg-secondary/20">
                    <BarChart3 className="h-12 w-12 opacity-50" />
                  </div>
                  <div className="absolute top-4 left-4">
                    <Badge variant="secondary" className="bg-background/80 backdrop-blur-sm">
                      {study.industry}
                    </Badge>
                  </div>
                </div>
                <CardHeader>
                  <div className="text-sm font-medium text-primary mb-2">{study.client}</div>
                  <CardTitle className="text-2xl mb-2">
                    {study.title}
                  </CardTitle>
                  <CardDescription className="text-base">
                    {study.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-3 gap-4 mb-6 py-4 border-y">
                    {study.metrics.map((metric, i) => (
                      <div key={i} className="text-center">
                        <div className="text-lg font-bold text-foreground">{metric.value}</div>
                        <div className="text-xs text-muted-foreground uppercase">{metric.label}</div>
                      </div>
                    ))}
                  </div>
                  <Button variant="outline" className="w-full group">
                    Read Full Story
                    <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary text-primary-foreground">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Write Your Success Story?</h2>
          <p className="text-xl opacity-90 mb-10 max-w-2xl mx-auto">
            Join these successful companies and start scaling your business with AI today.
          </p>
          <div className="flex justify-center gap-4">
            <Link href="https://app.bizoholic.net/register">
              <Button size="lg" variant="secondary" className="px-8">
                Start Free Trial
              </Button>
            </Link>
            <Link href="/contact">
              <Button size="lg" variant="outline" className="text-white border-white hover:bg-white hover:text-primary">
                Schedule Demo
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}
