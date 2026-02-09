/**
 * Dynamic Platform Homepage
 * - Port 3000 (Bizoholic): Marketing website
 * - Port 3002 (BizOSaaS): Redirects to dashboard
 * - Port 3001 (Coreldove): E-commerce homepage
 */

'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { usePlatform } from '@/lib/platform-config'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
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

// Types for CMS data
interface HomepageContent {
  title: string
  hero_title: string
  hero_subtitle: string
  hero_cta_text: string
  hero_cta_url: string
  features_title: string
  features: Array<{
    icon: string
    title: string
    description: string
    link?: string
  }>
  stats?: Array<{
    number: string
    label: string
    description: string
  }>
  show_service_status: boolean
  tenant_id: string
}

interface ServicePage {
  id: number
  title: string
  slug: string
  icon: string
  badge: string
  category: string
  service_description: string
  featured: boolean
  order: number
  price_data: {
    starting_price: string
    currency: string
    billing_period: string
  }
}

interface BlogPost {
  id: number
  title: string
  slug: string
  excerpt: string
  featured_image?: string
  published_date: string
  author: string
  category: string
  tags: string[]
  read_time: number
  featured: boolean
}

import { gql, useQuery } from 'urql'

const GET_HOME_CONTENT = gql`
  query GetHomeContent($tenantId: String!) {
    cmsPages(tenantId: $tenantId) {
      id
      title
      slug
      status
    }
    cmsPosts(tenantId: $tenantId) {
      id
      title
      slug
      excerpt
      featuredImage
      publishedAt
      authorId
    }
  }
`;

export default function HomePage() {
  const router = useRouter()
  const { platform } = usePlatform()
  const [homepageContent, setHomepageContent] = useState<HomepageContent | null>(null)
  const [servicePages, setServicePages] = useState<ServicePage[]>([])
  const [blogPosts, setBlogPosts] = useState<BlogPost[]>([])

  const [result] = useQuery({
    query: GET_HOME_CONTENT,
    variables: { tenantId: 'bizoholic' },
    pause: platform === 'bizosaas',
  });

  const { data, fetching, error } = result;

  useEffect(() => {
    if (platform === 'bizosaas') {
      router.push('/dashboard')
      return
    }
  }, [platform, router])

  useEffect(() => {
    if (data?.cmsPosts) {
      const mappedPosts = data.cmsPosts.map((p: any) => ({
        id: parseInt(p.id) || 0,
        title: p.title,
        slug: p.slug,
        excerpt: p.excerpt,
        featured_image: p.featuredImage || '/blog/placeholder.jpg',
        published_date: p.publishedAt,
        author: p.authorId || 'Bizoholic Team',
        category: 'Blog',
        tags: [],
        read_time: 5,
        featured: true
      }));
      setBlogPosts(mappedPosts.slice(0, 3));
    }
  }, [data]);

  const loading = fetching;

  const fetchHomepageContent = async () => {
    // Keep it for manual refresh if needed, but urql handles it
  }

  // Fallback content if CMS is unavailable
  const fallbackContent: HomepageContent = {
    title: "Bizoholic - AI-Powered Marketing",
    hero_title: "Transform Your Business with AI Marketing",
    hero_subtitle: "Bizoholic Digital empowers businesses with autonomous AI agents that handle marketing campaigns, content creation, SEO optimization, and lead generation - all running 24/7 on autopilot.",
    hero_cta_text: "Start Free Trial",
    hero_cta_url: "https://app.bizoholic.net/signup",
    features_title: "Everything You Need to Dominate Digital Marketing",
    features: [
      {
        icon: "🤖",
        title: "AI Campaign Management",
        description: "Autonomous agents create, optimize, and manage your advertising campaigns across Google Ads, Meta, LinkedIn, and 40+ other platforms.",
        link: "/services/ai-campaign-management"
      },
      {
        icon: "🎯",
        title: "Content Generation",
        description: "AI-powered content creation for blogs, social media, email campaigns, and website copy that converts visitors into customers.",
        link: "/services/content-generation"
      },
      {
        icon: "📊",
        title: "Performance Analytics",
        description: "Real-time analytics and insights with automated reporting that helps you understand what's working and what needs optimization.",
        link: "/services/performance-analytics"
      },
      {
        icon: "🚀",
        title: "Marketing Automation",
        description: "End-to-end marketing automation workflows that nurture leads and convert prospects into customers automatically.",
        link: "/services/marketing-automation"
      },
      {
        icon: "💡",
        title: "Strategy Consulting",
        description: "Expert marketing strategy consultation to align your business goals with data-driven marketing approaches.",
        link: "/services/strategy-consulting"
      },
      {
        icon: "🎨",
        title: "Creative Design",
        description: "Professional design services for all your marketing materials, from social media graphics to landing pages.",
        link: "/services/creative-design"
      },
      {
        icon: "🔍",
        title: "SEO Optimization",
        description: "Advanced SEO strategies and on-page optimization to boost your search engine rankings and organic traffic.",
        link: "/services/seo-optimization"
      },
      {
        icon: "📧",
        title: "Email Marketing",
        description: "Strategic email campaigns with personalized content, automation, and advanced segmentation for maximum engagement.",
        link: "/services/email-marketing"
      },
      {
        icon: "📱",
        title: "Social Media Marketing",
        description: "Comprehensive social media management across all platforms with content creation, community management, and paid advertising.",
        link: "/services/social-media-marketing"
      }
    ],
    show_service_status: true,
    tenant_id: "demo"
  }

  // Use CMS content if available, otherwise use fallback
  // Show fallback immediately during loading to avoid empty state
  const content = homepageContent ? {
    ...homepageContent,
    hero_cta_url: "https://app.bizoholic.net/signup" // Force correct URL for Client Portal
  } : fallbackContent
  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      {/* Hero Section */}
      <section className="py-20 lg:py-28">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <Badge variant="outline" className="mb-6">
              <Bot className="mr-2 h-3 w-3" />
              AI-Powered Marketing Automation
            </Badge>

            <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-7xl">
              {content.hero_title.split(' ').slice(0, -2).join(' ')}{' '}
              <span className="text-primary">{content.hero_title.split(' ').slice(-2).join(' ')}</span>
            </h1>

            <p className="mt-6 text-lg leading-8 text-muted-foreground max-w-2xl mx-auto">
              {content.hero_subtitle}
            </p>

            <div className="mt-10 flex items-center justify-center gap-6">
              <Link href={content.hero_cta_url}>
                <Button size="lg" className="px-8">
                  {content.hero_cta_text}
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
              {content.features_title}
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Our AI agents work around the clock to optimize your marketing performance
            </p>
          </div>

          <div className="flex overflow-x-auto pb-6 -mx-4 px-4 snap-x snap-mandatory md:grid md:gap-8 md:grid-cols-2 lg:grid-cols-3 md:overflow-visible md:pb-0 md:mx-0 md:px-0 hide-scrollbar">
            {content.features.map((feature, index) => {
              const CardComponent = feature.link ? Link : 'div'
              return (
                <CardComponent key={index} href={feature.link || '#'} className={`${feature.link ? 'block' : ''} min-w-[280px] w-[85vw] md:w-auto md:min-w-0 snap-center md:snap-align-none`}>
                  <Card className="hover:shadow-lg transition-all duration-300 hover:scale-105 cursor-pointer group h-full flex flex-col">
                    <CardHeader className="flex-none">
                      <CardTitle className="group-hover:text-blue-600 transition-colors flex items-center gap-2">
                        <span className="text-2xl">{feature.icon}</span>
                        <span>{feature.title}</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="flex-grow flex flex-col justify-between">
                      <p className="text-muted-foreground mb-4 flex-grow">
                        {feature.description}
                      </p>
                      {feature.link && (
                        <div className="flex items-center text-blue-600 font-medium group-hover:text-blue-700 transition-colors mt-auto">
                          <span>Learn More</span>
                          <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </CardComponent>
              )
            })}
          </div>

          {/* Featured Blog Posts Section - Dynamic from CMS with Fallback */}
          {(
            <div className="mt-16">
              <div className="mx-auto max-w-2xl text-center mb-12">
                <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                  Latest Insights & Guides
                </h2>
                <p className="mt-4 text-lg text-muted-foreground">
                  Expert insights, industry trends, and actionable strategies for AI-powered marketing
                </p>
              </div>

              <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
                {(blogPosts.length > 0 ? blogPosts : [
                  {
                    id: 1,
                    title: "10 AI Marketing Strategies That Actually Work in 2024",
                    slug: "ai-marketing-strategies-2024",
                    excerpt: "Discover the latest AI marketing tactics that leading companies use to automate campaigns, personalize content, and boost ROI.",
                    featured_image: "/blog/ai-marketing-2024.jpg",
                    published_date: "2024-03-15",
                    author: "Sarah Chen",
                    category: "AI Marketing",
                    tags: ["AI", "Marketing", "Strategy"],
                    read_time: 8,
                    featured: true
                  },
                  {
                    id: 2,
                    title: "Complete Guide to Marketing Automation for Small Businesses",
                    slug: "marketing-automation-small-business",
                    excerpt: "Step-by-step guide to implementing marketing automation workflows that nurture leads and convert prospects automatically.",
                    featured_image: "/blog/automation-guide.jpg",
                    published_date: "2024-03-10",
                    author: "Michael Rodriguez",
                    category: "Automation",
                    tags: ["Automation", "Small Business", "Workflows"],
                    read_time: 12,
                    featured: true
                  },
                  {
                    id: 3,
                    title: "How to Measure ROI from AI-Powered Campaigns",
                    slug: "measure-roi-ai-campaigns",
                    excerpt: "Learn the key metrics and tools you need to track the performance and return on investment of your AI marketing campaigns.",
                    featured_image: "/blog/roi-measurement.jpg",
                    published_date: "2024-03-05",
                    author: "Emily Davis",
                    category: "Analytics",
                    tags: ["ROI", "Analytics", "AI Campaigns"],
                    read_time: 6,
                    featured: true
                  }
                ]).map((post) => (
                  <Link key={post.id} href={`/blog/${post.slug}`}>
                    <Card className="hover:shadow-lg transition-shadow cursor-pointer group h-full flex flex-col overflow-hidden">
                      {post.featured_image && (
                        <div className="aspect-video relative overflow-hidden">
                          <Image
                            src={post.featured_image}
                            alt={post.title}
                            fill
                            className="object-cover group-hover:scale-105 transition-transform duration-300"
                          />
                        </div>
                      )}
                      <CardHeader>
                        <div className="flex items-center justify-between mb-2">
                          <Badge variant="outline" className="text-xs">
                            {post.category}
                          </Badge>
                          <span className="text-xs text-muted-foreground">
                            {post.read_time} min read
                          </span>
                        </div>
                        <CardTitle className="group-hover:text-primary transition-colors text-lg line-clamp-2">
                          {post.title}
                        </CardTitle>
                        <p className="text-sm text-muted-foreground">
                          By {post.author} • {new Date(post.published_date).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                          })}
                        </p>
                      </CardHeader>
                      <CardContent className="flex-grow flex flex-col justify-between">
                        <p className="text-muted-foreground mb-4 line-clamp-3 flex-grow">
                          {post.excerpt}
                        </p>
                        <div className="flex items-center justify-between mt-auto">
                          <div className="flex flex-wrap gap-1">
                            {post.tags.slice(0, 2).map((tag, index) => (
                              <Badge key={index} variant="secondary" className="text-xs">
                                {tag}
                              </Badge>
                            ))}
                          </div>
                          <ArrowRight className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />
                        </div>
                      </CardContent>
                    </Card>
                  </Link>
                ))}
              </div>

              <div className="text-center mt-8">
                <Link href="/blog">
                  <Button variant="outline" size="lg">
                    View All Articles
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </div>
          )}

          {/* Stats Section - Dynamic from CMS */}
          {content.stats && content.stats.length > 0 && (
            <div className="mt-16">
              <div className="mx-auto max-w-2xl text-center mb-12">
                <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                  Proven Results
                </h2>
                <p className="mt-4 text-lg text-muted-foreground">
                  See what our AI-powered marketing automation can achieve
                </p>
              </div>

              <div className="flex overflow-x-auto pb-6 -mx-4 px-4 snap-x snap-mandatory md:grid md:gap-8 md:grid-cols-2 lg:grid-cols-4 md:overflow-visible md:pb-0 md:mx-0 md:px-0 hide-scrollbar">
                {content.stats.map((stat, index) => (
                  <div key={index} className="text-center min-w-[160px] snap-center">
                    <div className="text-4xl font-bold text-primary mb-2">{stat.number}</div>
                    <div className="text-lg font-semibold text-foreground mb-1">{stat.label}</div>
                    <div className="text-sm text-muted-foreground">{stat.description}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
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
                {[1, 2, 3, 4, 5].map((star) => (
                  <Star key={star} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                ))}
                <span className="ml-2 text-sm text-muted-foreground">4.9/5 from 1,000+ reviews</span>
              </div>
            </div>

            <div className="mt-8">
              <Link href="https://app.bizoholic.net/signup">
                <Button size="lg" className="px-12">
                  Start Your Free Trial Today
                  <ArrowRight className="ml-2 h-5 w-5" />
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