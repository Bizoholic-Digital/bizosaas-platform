'use client'

/**
 * Individual Blog Post Page - Dynamic Route
 * Content managed via Wagtail CMS backend
 */

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { notFound } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { 
  ArrowLeft,
  ArrowRight,
  Calendar,
  Clock,
  User,
  Share2,
  BookOpen,
  Tag
} from 'lucide-react'

interface BlogPost {
  id: number
  title: string
  slug: string
  content: string
  excerpt: string
  featured_image?: string
  published_date: string
  updated_date?: string
  author: string
  author_bio?: string
  author_image?: string
  category: string
  tags: string[]
  read_time: number
  featured: boolean
  seo_title?: string
  seo_description?: string
}

interface RelatedPost {
  id: number
  title: string
  slug: string
  excerpt: string
  author: string
  published_date: string
  category: string
  read_time: number
}

interface BlogPostPageProps {
  params: {
    slug: string
  }
}

export default function BlogPostPage({ params }: BlogPostPageProps) {
  const [blogPost, setBlogPost] = useState<BlogPost | null>(null)
  const [relatedPosts, setRelatedPosts] = useState<RelatedPost[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchBlogPost()
  }, [params.slug])

  const fetchBlogPost = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Fetch individual blog post from Brain API
      const response = await fetch(`/api/brain/wagtail/blog/${params.slug}`)
      
      if (response.ok) {
        const data = await response.json()
        setBlogPost(data.post)
        setRelatedPosts(data.related_posts || [])
      } else if (response.status === 404) {
        // Use fallback content for demo
        const fallbackPost = getFallbackPost(params.slug)
        if (fallbackPost) {
          setBlogPost(fallbackPost)
          setRelatedPosts(getFallbackRelatedPosts())
        } else {
          setError('Post not found')
        }
      } else {
        setError('Failed to load blog post')
      }
    } catch (error) {
      console.error('Error fetching blog post:', error)
      // Try fallback content
      const fallbackPost = getFallbackPost(params.slug)
      if (fallbackPost) {
        setBlogPost(fallbackPost)
        setRelatedPosts(getFallbackRelatedPosts())
      } else {
        setError('Failed to load blog post')
      }
    } finally {
      setLoading(false)
    }
  }

  const getFallbackPost = (slug: string): BlogPost | null => {
    const fallbackPosts: Record<string, BlogPost> = {
      'ai-powered-campaign-optimization-guide-2024': {
        id: 1,
        title: "The Ultimate Guide to AI-Powered Campaign Optimization in 2024",
        slug: "ai-powered-campaign-optimization-guide-2024",
        content: `
          <h2>Introduction to AI Campaign Optimization</h2>
          <p>Artificial intelligence is revolutionizing the way we approach digital marketing campaigns. Gone are the days of manual bid adjustments, guesswork-based targeting, and reactive campaign management. Today's AI-powered systems can analyze thousands of data points in real-time, make intelligent decisions, and optimize campaigns for maximum performance.</p>
          
          <h2>How AI Agents Transform Marketing</h2>
          <p>Our BizoSaaS platform employs 28+ specialized AI agents, each designed for specific marketing tasks:</p>
          <ul>
            <li><strong>Campaign Strategy Agent:</strong> Analyzes market conditions and creates comprehensive campaign strategies</li>
            <li><strong>Bid Management Agent:</strong> Optimizes bids in real-time based on performance data</li>
            <li><strong>Audience Targeting Agent:</strong> Identifies and segments high-value audiences</li>
            <li><strong>Creative Optimization Agent:</strong> Tests and optimizes ad creatives automatically</li>
            <li><strong>Budget Allocation Agent:</strong> Distributes budget across campaigns for maximum ROI</li>
          </ul>
          
          <h2>Real-World Results</h2>
          <p>Our clients have seen remarkable improvements in their campaign performance:</p>
          <blockquote>"We achieved a 300% increase in qualified leads and reduced our cost-per-acquisition by 60% within the first quarter of using BizoSaaS." - TechStartup Inc, CMO</blockquote>
          
          <h2>The Future of Marketing Automation</h2>
          <p>As AI technology continues to evolve, we can expect even more sophisticated automation capabilities. Machine learning algorithms will become better at predicting customer behavior, understanding market trends, and making strategic decisions that drive business growth.</p>
          
          <h2>Getting Started</h2>
          <p>Ready to transform your marketing with AI? Our platform makes it easy to get started with autonomous campaign management. From setup to optimization, our AI agents handle the complexity while you focus on growing your business.</p>
        `,
        excerpt: "Discover how artificial intelligence is revolutionizing digital marketing campaigns with autonomous optimization, predictive analytics, and real-time performance improvements.",
        featured_image: "/blog/ai-campaign-optimization.jpg",
        published_date: "2024-01-15",
        updated_date: "2024-01-16",
        author: "Sarah Chen",
        author_bio: "Sarah is our Chief Marketing Officer with over 10 years of experience in digital marketing and AI automation. She leads our marketing strategy and oversees the development of our AI agents.",
        author_image: "/team/sarah-chen.jpg",
        category: "AI Marketing",
        tags: ["AI", "Campaign Optimization", "Digital Marketing", "Automation", "ROI"],
        read_time: 8,
        featured: true,
        seo_title: "AI Campaign Optimization Guide 2024 | BizoSaaS",
        seo_description: "Complete guide to AI-powered campaign optimization. Learn how 28+ AI agents can transform your marketing results with autonomous optimization."
      },
      'ai-content-generation-workflow': {
        id: 2,
        title: "How to Generate High-Converting Content with AI: A Complete Workflow",
        slug: "ai-content-generation-workflow",
        content: `
          <h2>The Content Generation Challenge</h2>
          <p>Creating compelling, high-converting content consistently is one of the biggest challenges marketers face today. Traditional content creation processes are time-consuming, resource-intensive, and often struggle to maintain quality at scale.</p>
          
          <h2>Our AI-Powered Content Workflow</h2>
          <p>Our content generation system uses multiple AI agents working in harmony:</p>
          
          <h3>1. Research & Strategy Agent</h3>
          <p>This agent analyzes your target audience, competitors, and market trends to develop content strategies that resonate with your customers.</p>
          
          <h3>2. Content Creation Agent</h3>
          <p>Using advanced language models, this agent generates original, engaging content tailored to your brand voice and marketing objectives.</p>
          
          <h3>3. SEO Optimization Agent</h3>
          <p>Ensures all content is optimized for search engines while maintaining readability and user engagement.</p>
          
          <h3>4. Performance Analysis Agent</h3>
          <p>Continuously monitors content performance and provides insights for improvement.</p>
          
          <h2>Best Practices for AI Content</h2>
          <ul>
            <li>Always review and edit AI-generated content</li>
            <li>Maintain your brand voice and tone</li>
            <li>Focus on providing value to your audience</li>
            <li>Use data to inform content strategy</li>
            <li>Test different content formats and styles</li>
          </ul>
          
          <h2>Measuring Success</h2>
          <p>Track these key metrics to measure your content's effectiveness:</p>
          <ul>
            <li>Engagement rates (likes, shares, comments)</li>
            <li>Conversion rates from content to leads/sales</li>
            <li>Time spent on page</li>
            <li>Bounce rates</li>
            <li>SEO rankings and organic traffic</li>
          </ul>
        `,
        excerpt: "Learn the complete process of using AI tools to create compelling content that converts, from ideation to optimization and performance tracking.",
        featured_image: "/blog/ai-content-generation.jpg",
        published_date: "2024-01-10",
        author: "Michael Rodriguez",
        author_bio: "Michael is our Head of Content Strategy, specializing in AI-powered content creation and optimization. He has helped hundreds of businesses scale their content marketing efforts.",
        author_image: "/team/michael-rodriguez.jpg",
        category: "Content Strategy",
        tags: ["Content Marketing", "AI Tools", "Copywriting", "Conversion", "SEO"],
        read_time: 6,
        featured: true
      }
    }
    
    return fallbackPosts[slug] || null
  }

  const getFallbackRelatedPosts = (): RelatedPost[] => [
    {
      id: 3,
      title: "5 AI Marketing Trends That Will Dominate 2024",
      slug: "ai-marketing-trends-2024",
      excerpt: "Explore the cutting-edge AI marketing trends that forward-thinking businesses are using to gain competitive advantages.",
      author: "Emily Johnson",
      published_date: "2024-01-08",
      category: "Industry Insights",
      read_time: 5
    },
    {
      id: 4,
      title: "Case Study: 300% Lead Increase with AI Campaigns",
      slug: "techstartup-300-percent-lead-increase-case-study",
      excerpt: "Deep dive into how a B2B SaaS company leveraged AI campaign management to dramatically improve results.",
      author: "David Kim",
      published_date: "2024-01-05",
      category: "Case Studies",
      read_time: 10
    },
    {
      id: 5,
      title: "Complete SEO Automation Setup with AI Tools",
      slug: "complete-seo-automation-ai-tools",
      excerpt: "Step-by-step tutorial on setting up automated SEO workflows using AI tools for maximum visibility.",
      author: "Lisa Park",
      published_date: "2024-01-03",
      category: "SEO & Analytics",
      read_time: 12
    }
  ]

  if (loading) {
    return (
      <div className="flex flex-col min-h-screen">
        <Header />
        <div className="container py-20">
          <div className="max-w-4xl mx-auto">
            <div className="animate-pulse">
              <div className="h-8 bg-muted rounded w-1/4 mb-4" />
              <div className="h-12 bg-muted rounded w-3/4 mb-6" />
              <div className="h-64 bg-muted rounded mb-8" />
              <div className="space-y-4">
                <div className="h-4 bg-muted rounded w-full" />
                <div className="h-4 bg-muted rounded w-5/6" />
                <div className="h-4 bg-muted rounded w-4/6" />
              </div>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    )
  }

  if (error || !blogPost) {
    return (
      <div className="flex flex-col min-h-screen">
        <Header />
        <div className="container py-20">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-foreground mb-4">Blog Post Not Found</h1>
            <p className="text-muted-foreground mb-8">
              {error || 'The blog post you are looking for does not exist.'}
            </p>
            <Link href="/blog">
              <Button>
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to Blog
              </Button>
            </Link>
          </div>
        </div>
        <Footer />
      </div>
    )
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      {/* Breadcrumb */}
      <div className="border-b bg-muted/30">
        <div className="container py-4">
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-foreground transition-colors">Home</Link>
            <span>/</span>
            <Link href="/blog" className="hover:text-foreground transition-colors">Blog</Link>
            <span>/</span>
            <span className="text-foreground">{blogPost.title}</span>
          </div>
        </div>
      </div>

      {/* Article Header */}
      <article className="py-12">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <header className="mb-12">
              <div className="flex items-center gap-4 mb-6">
                <Badge variant="secondary">{blogPost.category}</Badge>
                {blogPost.featured && <Badge variant="outline">Featured</Badge>}
                <div className="flex flex-wrap gap-1">
                  {blogPost.tags.slice(0, 3).map((tag, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      <Tag className="mr-1 h-3 w-3" />
                      {tag}
                    </Badge>
                  ))}
                </div>
              </div>
              
              <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-foreground mb-6">
                {blogPost.title}
              </h1>
              
              <p className="text-xl text-muted-foreground mb-8">
                {blogPost.excerpt}
              </p>
              
              <div className="flex flex-col sm:flex-row sm:items-center gap-4 pb-8 border-b">
                <div className="flex items-center space-x-4">
                  {blogPost.author_image && (
                    <Image
                      src={blogPost.author_image}
                      alt={blogPost.author}
                      width={48}
                      height={48}
                      className="rounded-full"
                    />
                  )}
                  <div>
                    <div className="flex items-center space-x-1 text-sm font-medium">
                      <User className="h-4 w-4" />
                      <span>{blogPost.author}</span>
                    </div>
                    {blogPost.author_bio && (
                      <p className="text-xs text-muted-foreground mt-1">
                        {blogPost.author_bio.substring(0, 100)}...
                      </p>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-6 text-sm text-muted-foreground">
                  <div className="flex items-center space-x-1">
                    <Calendar className="h-4 w-4" />
                    <span>{new Date(blogPost.published_date).toLocaleDateString('en-US', { 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Clock className="h-4 w-4" />
                    <span>{blogPost.read_time} min read</span>
                  </div>
                  <Button variant="ghost" size="sm">
                    <Share2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </header>
            
            {/* Featured Image */}
            {blogPost.featured_image && (
              <div className="aspect-video relative overflow-hidden rounded-lg mb-12">
                <Image
                  src={blogPost.featured_image}
                  alt={blogPost.title}
                  fill
                  className="object-cover"
                />
              </div>
            )}
            
            {/* Article Content */}
            <div 
              className="prose prose-lg max-w-none"
              dangerouslySetInnerHTML={{ __html: blogPost.content }}
            />
            
            {/* Article Footer */}
            <footer className="mt-12 pt-8 border-t">
              <div className="flex items-center justify-between">
                <div className="flex flex-wrap gap-2">
                  {blogPost.tags.map((tag, index) => (
                    <Badge key={index} variant="secondary" className="text-xs">
                      {tag}
                    </Badge>
                  ))}
                </div>
                <div className="flex items-center space-x-4">
                  <span className="text-sm text-muted-foreground">
                    Last updated: {new Date(blogPost.updated_date || blogPost.published_date).toLocaleDateString()}
                  </span>
                  <Button variant="outline" size="sm">
                    <Share2 className="mr-2 h-4 w-4" />
                    Share Article
                  </Button>
                </div>
              </div>
            </footer>
          </div>
        </div>
      </article>
      
      {/* Related Posts */}
      {relatedPosts.length > 0 && (
        <section className="py-16 bg-muted/30">
          <div className="container">
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl mb-4">
                  Related Articles
                </h2>
                <p className="text-lg text-muted-foreground">
                  Continue exploring AI marketing insights
                </p>
              </div>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {relatedPosts.map((post) => (
                  <Link key={post.id} href={`/blog/${post.slug}`}>
                    <Card className="hover:shadow-lg transition-shadow cursor-pointer group h-full">
                      <CardHeader>
                        <Badge variant="outline" className="text-xs mb-2 w-fit">
                          {post.category}
                        </Badge>
                        <CardTitle className="group-hover:text-primary transition-colors text-lg line-clamp-2">
                          {post.title}
                        </CardTitle>
                        <div className="flex items-center space-x-4 text-xs text-muted-foreground">
                          <span>By {post.author}</span>
                          <span>{post.read_time} min read</span>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <p className="text-muted-foreground text-sm line-clamp-3 mb-4">
                          {post.excerpt}
                        </p>
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-muted-foreground">
                            {new Date(post.published_date).toLocaleDateString()}
                          </span>
                          <ArrowRight className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />
                        </div>
                      </CardContent>
                    </Card>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}
      
      {/* CTA Section */}
      <section className="py-16 bg-primary text-primary-foreground">
        <div className="container">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl mb-4">
              Ready to Implement These Strategies?
            </h2>
            <p className="text-lg opacity-90 mb-8">
              Take your marketing to the next level with our AI-powered automation platform
              and expert consulting services.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/bizosaas">
                <Button size="lg" variant="secondary" className="px-8">
                  Try BizoSaaS Platform
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/contact">
                <Button size="lg" variant="outline" className="px-8 border-white text-white hover:bg-white hover:text-primary">
                  Schedule Consultation
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
      
      {/* Back to Blog */}
      <div className="border-t bg-background">
        <div className="container py-8">
          <div className="max-w-4xl mx-auto">
            <Link href="/blog">
              <Button variant="ghost">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to All Articles
              </Button>
            </Link>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  )
}