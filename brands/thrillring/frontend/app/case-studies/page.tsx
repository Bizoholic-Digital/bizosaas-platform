'use client'

/**
 * Case Studies Page - Client Success Stories
 * Comprehensive showcase of real client results and testimonials
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
  TrendingUp,
  Users,
  Target,
  DollarSign,
  BarChart3,
  Clock,
  Award,
  Star,
  Quote
} from 'lucide-react'

const caseStudies = [
  {
    id: 1,
    client: "TechStartup Inc",
    industry: "B2B SaaS Technology",
    challenge: "Struggling with lead generation and high customer acquisition costs",
    solution: "Implemented AI-powered campaign management across Google Ads, LinkedIn, and Meta with automated content generation",
    results: [
      { metric: "300%", label: "Increase in Qualified Leads" },
      { metric: "60%", label: "Reduction in CPA" },
      { metric: "4.2x", label: "Return on Ad Spend" },
      { metric: "90%", label: "Time Saved on Campaign Management" }
    ],
    quote: "The AI campaign management transformed our lead generation completely. We went from struggling to find prospects to having more qualified leads than we could handle.",
    author: "Sarah Chen, CMO",
    timeline: "6 months",
    investment: "₹50,000/month",
    featured: true,
    category: "B2B SaaS"
  },
  {
    id: 2,
    client: "E-commerce Fashion Brand",
    industry: "E-commerce & Retail",
    challenge: "Low conversion rates and poor ROAS across multiple advertising platforms",
    solution: "Deployed AI agents for dynamic product advertising, automated A/B testing, and personalized retargeting campaigns",
    results: [
      { metric: "180%", label: "Increase in Conversion Rate" },
      { metric: "45%", label: "Higher Average Order Value" },
      { metric: "5.8x", label: "Return on Ad Spend" },
      { metric: "250%", label: "Revenue Growth" }
    ],
    quote: "Our revenue increased by 250% within 8 months. The AI optimization of our product ads was a game-changer for our business.",
    author: "Priya Sharma, Founder",
    timeline: "8 months",
    investment: "₹75,000/month",
    featured: true,
    category: "E-commerce"
  },
  {
    id: 3,
    client: "Local Services Company",
    industry: "Home Services",
    challenge: "Limited local visibility and inconsistent lead flow from digital marketing efforts",
    solution: "Implemented local SEO optimization, Google My Business automation, and location-based AI campaign targeting",
    results: [
      { metric: "450%", label: "Increase in Local Leads" },
      { metric: "300%", label: "Improvement in Local Visibility" },
      { metric: "#1", label: "Ranking for 20+ Keywords" },
      { metric: "85%", label: "Increase in Phone Calls" }
    ],
    quote: "We became the #1 choice in our area. The local SEO and targeted campaigns brought us more business than we could handle.",
    author: "Raj Patel, Owner",
    timeline: "4 months",
    investment: "₹30,000/month",
    featured: false,
    category: "Local Services"
  },
  {
    id: 4,
    client: "Healthcare Clinic",
    industry: "Healthcare",
    challenge: "Difficulty reaching patients online and competing with larger healthcare providers",
    solution: "Created HIPAA-compliant AI marketing system with automated patient education content and local search optimization",
    results: [
      { metric: "200%", label: "Increase in New Patients" },
      { metric: "150%", label: "More Online Appointments" },
      { metric: "75%", label: "Improvement in Online Reviews" },
      { metric: "3.5x", label: "Website Traffic Growth" }
    ],
    quote: "Patient acquisition has never been easier. The AI handles our marketing while we focus on providing excellent healthcare.",
    author: "Dr. Amit Kumar, Director",
    timeline: "5 months",
    investment: "₹40,000/month",
    featured: false,
    category: "Healthcare"
  },
  {
    id: 5,
    client: "Manufacturing Company",
    industry: "B2B Manufacturing",
    challenge: "Long sales cycles and difficulty generating qualified B2B leads in a niche industry",
    solution: "Developed industry-specific content strategy with LinkedIn automation and technical SEO for manufacturing keywords",
    results: [
      { metric: "400%", label: "Increase in B2B Inquiries" },
      { metric: "50%", label: "Shorter Sales Cycle" },
      { metric: "8x", label: "LinkedIn Lead Generation" },
      { metric: "120%", label: "Qualified Demo Requests" }
    ],
    quote: "The B2B lead generation system brought us high-quality prospects we never could have reached before.",
    author: "Rohit Singh, Sales Director",
    timeline: "7 months",
    investment: "₹60,000/month",
    featured: false,
    category: "Manufacturing"
  },
  {
    id: 6,
    client: "Educational Institute",
    industry: "Education",
    challenge: "Declining enrollment and ineffective digital marketing to reach prospective students",
    solution: "Implemented AI-driven student journey mapping with personalized content and automated nurturing campaigns",
    results: [
      { metric: "220%", label: "Increase in Enrollments" },
      { metric: "65%", label: "Higher Application Rates" },
      { metric: "180%", label: "Social Media Engagement" },
      { metric: "90%", label: "Reduction in Cost per Lead" }
    ],
    quote: "Our enrollment numbers reached record highs. The personalized approach to prospective students was incredibly effective.",
    author: "Dr. Meera Gupta, Director",
    timeline: "6 months",
    investment: "₹35,000/month",
    featured: false,
    category: "Education"
  }
]

const industries = [
  'All Industries',
  'B2B SaaS',
  'E-commerce', 
  'Local Services',
  'Healthcare',
  'Manufacturing',
  'Education'
]

export default function CaseStudiesPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      {/* Hero Section */}
      <section className="py-16 lg:py-20">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <Badge variant="outline" className="mb-6">
              Client Success Stories
            </Badge>
            
            <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl">
              Real Results from
              <span className="text-primary"> AI-Powered Marketing</span>
            </h1>
            
            <p className="mt-6 text-lg leading-8 text-muted-foreground max-w-2xl mx-auto">
              Discover how businesses across industries have transformed their growth 
              with our autonomous marketing solutions and AI-first approach.
            </p>
            
            <div className="mt-8">
              <Link href="/contact">
                <Button size="lg" className="px-8 btn-gradient">
                  Get Your Success Story
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Success Metrics Overview */}
      <section className="py-16 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Proven Results Across Industries
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Combined success metrics from our client portfolio
            </p>
          </div>
          
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div className="bg-background rounded-lg p-6 shadow-sm">
              <div className="text-4xl font-bold text-primary mb-2">₹50Cr+</div>
              <div className="text-sm text-muted-foreground">Revenue Generated</div>
            </div>
            <div className="bg-background rounded-lg p-6 shadow-sm">
              <div className="text-4xl font-bold text-primary mb-2">300%</div>
              <div className="text-sm text-muted-foreground">Average ROI Increase</div>
            </div>
            <div className="bg-background rounded-lg p-6 shadow-sm">
              <div className="text-4xl font-bold text-primary mb-2">500+</div>
              <div className="text-sm text-muted-foreground">Campaigns Optimized</div>
            </div>
            <div className="bg-background rounded-lg p-6 shadow-sm">
              <div className="text-4xl font-bold text-primary mb-2">95%</div>
              <div className="text-sm text-muted-foreground">Client Retention Rate</div>
            </div>
          </div>
        </div>
      </section>

      {/* Industry Filter */}
      <section className="py-8 border-b">
        <div className="container">
          <div className="flex flex-wrap gap-2 justify-center">
            {industries.map((industry, index) => (
              <Badge 
                key={index} 
                variant={index === 0 ? "default" : "outline"} 
                className="cursor-pointer hover:bg-primary hover:text-primary-foreground transition-colors"
              >
                {industry}
              </Badge>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Case Studies */}
      <section className="py-16">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Featured Success Stories
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              In-depth analysis of our most impactful client transformations
            </p>
          </div>
          
          <div className="space-y-16">
            {caseStudies.filter(study => study.featured).map((study, index) => (
              <div key={study.id} className="bg-muted/30 rounded-lg p-8">
                <div className="grid lg:grid-cols-3 gap-8">
                  {/* Client Info */}
                  <div>
                    <div className="flex items-center gap-4 mb-4">
                      <Badge variant="secondary">{study.category}</Badge>
                      {study.featured && (
                        <Badge variant="default">Featured</Badge>
                      )}
                    </div>
                    <h3 className="text-2xl font-bold text-foreground mb-2">{study.client}</h3>
                    <p className="text-muted-foreground mb-4">{study.industry}</p>
                    
                    <div className="space-y-3 text-sm">
                      <div className="flex items-center gap-2">
                        <Clock className="h-4 w-4 text-primary" />
                        <span className="text-muted-foreground">Timeline: {study.timeline}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <DollarSign className="h-4 w-4 text-primary" />
                        <span className="text-muted-foreground">Investment: {study.investment}</span>
                      </div>
                    </div>
                  </div>
                  
                  {/* Challenge & Solution */}
                  <div>
                    <div className="mb-6">
                      <h4 className="font-semibold text-foreground mb-2">Challenge</h4>
                      <p className="text-sm text-muted-foreground">{study.challenge}</p>
                    </div>
                    
                    <div>
                      <h4 className="font-semibold text-foreground mb-2">Solution</h4>
                      <p className="text-sm text-muted-foreground">{study.solution}</p>
                    </div>
                  </div>
                  
                  {/* Results */}
                  <div>
                    <h4 className="font-semibold text-foreground mb-4">Key Results</h4>
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      {study.results.map((result, i) => (
                        <div key={i} className="text-center bg-background rounded-lg p-3">
                          <div className="text-2xl font-bold text-primary">{result.metric}</div>
                          <div className="text-xs text-muted-foreground">{result.label}</div>
                        </div>
                      ))}
                    </div>
                    
                    {/* Testimonial */}
                    <div className="bg-background rounded-lg p-4">
                      <Quote className="h-6 w-6 text-primary mb-2" />
                      <blockquote className="text-sm text-foreground mb-3">
                        "{study.quote}"
                      </blockquote>
                      <cite className="text-xs text-muted-foreground">
                        — {study.author}
                      </cite>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* All Case Studies Grid */}
      <section className="py-16 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              More Success Stories
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Additional client transformations across diverse industries
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {caseStudies.filter(study => !study.featured).map((study) => (
              <Card key={study.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between mb-2">
                    <Badge variant="outline">{study.category}</Badge>
                    <div className="flex items-center">
                      {[1,2,3,4,5].map((star) => (
                        <Star key={star} className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                      ))}
                    </div>
                  </div>
                  <CardTitle className="text-lg">{study.client}</CardTitle>
                  <p className="text-sm text-muted-foreground">{study.industry}</p>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <h4 className="text-sm font-semibold mb-1">Key Results</h4>
                      <div className="grid grid-cols-2 gap-2">
                        {study.results.slice(0, 2).map((result, i) => (
                          <div key={i} className="text-center bg-muted/50 rounded p-2">
                            <div className="text-lg font-bold text-primary">{result.metric}</div>
                            <div className="text-xs text-muted-foreground">{result.label}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div className="bg-muted/50 rounded p-3">
                      <blockquote className="text-sm text-foreground mb-2">
                        "{study.quote.substring(0, 100)}..."
                      </blockquote>
                      <cite className="text-xs text-muted-foreground">
                        — {study.author}
                      </cite>
                    </div>
                    
                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span>Timeline: {study.timeline}</span>
                      <Button variant="ghost" size="sm">
                        View Details
                        <ArrowRight className="ml-1 h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-primary text-primary-foreground">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Ready to Write Your Success Story?
            </h2>
            <p className="mt-4 text-lg opacity-90">
              Join hundreds of businesses achieving exceptional results with AI-powered marketing automation.
            </p>
            
            <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contact">
                <Button size="lg" variant="secondary" className="px-8">
                  Start Your Transformation
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/auth/register">
                <Button size="lg" variant="outline" className="px-8 border-white text-white hover:bg-white hover:text-primary">
                  Try Free Trial
                </Button>
              </Link>
            </div>
            
            <div className="mt-8 flex items-center justify-center gap-4">
              <div className="flex items-center space-x-1">
                {[1,2,3,4,5].map((star) => (
                  <Star key={star} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                ))}
                <span className="ml-2 text-sm opacity-75">4.9/5 from 500+ clients</span>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <Footer />
    </div>
  )
}