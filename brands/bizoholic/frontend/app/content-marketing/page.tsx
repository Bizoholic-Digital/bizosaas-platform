"use client"

import Link from 'next/link'
import { ArrowLeft, Lightbulb, CheckCircle, Star } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/button'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'

export default function ContentMarketingPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      {/* Breadcrumb */}
      <div className="bg-muted/30 py-4">
        <div className="container">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-primary">Home</Link>
            <span>/</span>
            <Link href="/#services" className="hover:text-primary">Services</Link>
            <span>/</span>
            <span className="text-foreground">Content Marketing</span>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <section className="py-20 md:py-32">
        <div className="container">
          <div className="text-center max-w-4xl mx-auto">
            <Link href="/#services" className="inline-flex items-center gap-2 text-muted-foreground hover:text-primary mb-6">
              <ArrowLeft className="h-4 w-4" />
              Back to Services
            </Link>
            
            <Badge variant="outline" className="mb-4">
              <Lightbulb className="h-4 w-4 mr-2" />
              AI + Expert Based Solution
            </Badge>
            
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              Content Marketing
            </h1>
            
            <p className="text-xl text-muted-foreground mb-8">
              AI-generated content ideas, automated blog writing, and content optimization 
              guided by expert content strategists for maximum engagement and conversions.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
              <Button size="lg" className="btn-gradient">
                Get Free Content Audit
              </Button>
              <Button variant="outline" size="lg">
                View Content Samples
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Coming Soon Notice */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <Card className="max-w-2xl mx-auto text-center">
            <CardHeader>
              <CardTitle className="text-2xl">Coming Soon</CardTitle>
              <CardDescription>
                We're putting the finishing touches on this service page. 
                Contact us for more information about our Content Marketing services.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button>Contact Us for Details</Button>
            </CardContent>
          </Card>
        </div>
      </section>
      
      <Footer />
    </div>
  )
}