/**
 * Wagtail CMS API Client
 * Provides functions to interact with Wagtail CMS backend
 * Includes fallback data for development when backend is unavailable
 */

const WAGTAIL_API_URL = process.env.NEXT_PUBLIC_WAGTAIL_API_URL || 'http://localhost:4000/api'
const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// TypeScript Interfaces
export interface BlogPost {
  id: number
  title: string
  slug: string
  excerpt: string
  content?: string
  author: string
  author_bio?: string
  date: string
  read_time: string
  category: string
  image: string
  featured_image?: string
  tags?: string[]
}

export interface Resource {
  id: number
  title: string
  slug: string
  type: 'guide' | 'webinar' | 'ebook' | 'template' | 'calculator'
  description: string
  downloads?: number
  image?: string
  file_url?: string
  whats_included?: string[]
}

export interface ContactFormData {
  name: string
  email: string
  company?: string
  phone?: string
  service?: string
  message: string
}

// Blog Posts Functions

/**
 * Get all blog posts with optional filtering
 */
export async function getBlogPosts(params?: {
  category?: string
  limit?: number
  offset?: number
}): Promise<{ results: BlogPost[], count: number }> {
  try {
    const queryParams = new URLSearchParams()
    if (params?.category) queryParams.append('category', params.category)
    if (params?.limit) queryParams.append('limit', params.limit.toString())
    if (params?.offset) queryParams.append('offset', params.offset.toString())

    const url = `${WAGTAIL_API_URL}/blog/posts/?${queryParams.toString()}`
    const res = await fetch(url, {
      cache: 'no-store',
      headers: { 'Content-Type': 'application/json' }
    })

    if (!res.ok) throw new Error('Failed to fetch blog posts')
    return await res.json()
  } catch (error) {
    console.warn('Wagtail API unavailable, using fallback data:', error)
    return getFallbackBlogPosts(params)
  }
}

/**
 * Get a single blog post by slug
 */
export async function getBlogPost(slug: string): Promise<BlogPost | null> {
  try {
    const res = await fetch(`${WAGTAIL_API_URL}/blog/posts/${slug}/`, {
      cache: 'no-store',
      headers: { 'Content-Type': 'application/json' }
    })

    if (!res.ok) throw new Error('Failed to fetch blog post')
    return await res.json()
  } catch (error) {
    console.warn('Wagtail API unavailable, using fallback data:', error)
    return getFallbackBlogPost(slug)
  }
}

/**
 * Get blog categories
 */
export async function getBlogCategories(): Promise<string[]> {
  try {
    const res = await fetch(`${WAGTAIL_API_URL}/blog/categories/`, {
      cache: 'no-store',
      headers: { 'Content-Type': 'application/json' }
    })

    if (!res.ok) throw new Error('Failed to fetch categories')
    return await res.json()
  } catch (error) {
    console.warn('Wagtail API unavailable, using fallback categories')
    return ['AI Marketing', 'SEO', 'Social Media', 'Content Strategy', 'Analytics', 'Case Studies']
  }
}

// Resources Functions

/**
 * Get all resources with optional filtering
 */
export async function getResources(params?: {
  type?: string
  limit?: number
  offset?: number
}): Promise<{ results: Resource[], count: number }> {
  try {
    const queryParams = new URLSearchParams()
    if (params?.type) queryParams.append('type', params.type)
    if (params?.limit) queryParams.append('limit', params.limit.toString())
    if (params?.offset) queryParams.append('offset', params.offset.toString())

    const url = `${WAGTAIL_API_URL}/resources/?${queryParams.toString()}`
    const res = await fetch(url, {
      cache: 'no-store',
      headers: { 'Content-Type': 'application/json' }
    })

    if (!res.ok) throw new Error('Failed to fetch resources')
    return await res.json()
  } catch (error) {
    console.warn('Wagtail API unavailable, using fallback data:', error)
    return getFallbackResources(params)
  }
}

/**
 * Get a single resource by slug
 */
export async function getResource(slug: string): Promise<Resource | null> {
  try {
    const res = await fetch(`${WAGTAIL_API_URL}/resources/${slug}/`, {
      cache: 'no-store',
      headers: { 'Content-Type': 'application/json' }
    })

    if (!res.ok) throw new Error('Failed to fetch resource')
    return await res.json()
  } catch (error) {
    console.warn('Wagtail API unavailable, using fallback data:', error)
    return getFallbackResource(slug)
  }
}

// Form Submission Functions

/**
 * Submit contact form to Brain Hub
 */
export async function submitContactForm(data: ContactFormData): Promise<boolean> {
  try {
    const res = await fetch(`${BRAIN_API_URL}/api/brain/wagtail/contact`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })

    return res.ok
  } catch (error) {
    console.error('Failed to submit contact form:', error)
    return false
  }
}

/**
 * Subscribe to newsletter
 */
export async function subscribeNewsletter(email: string): Promise<boolean> {
  try {
    const res = await fetch(`${BRAIN_API_URL}/api/brain/wagtail/newsletter`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    })

    return res.ok
  } catch (error) {
    console.error('Failed to subscribe to newsletter:', error)
    return false
  }
}

/**
 * Download resource and track lead
 */
export async function downloadResource(slug: string, email: string, name?: string): Promise<{ success: boolean, download_url?: string }> {
  try {
    const res = await fetch(`${BRAIN_API_URL}/api/brain/wagtail/resources/download`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slug, email, name })
    })

    if (!res.ok) throw new Error('Failed to process download')
    return await res.json()
  } catch (error) {
    console.error('Failed to download resource:', error)
    return { success: false }
  }
}

// Fallback Data for Development

function getFallbackBlogPosts(params?: { category?: string, limit?: number, offset?: number }) {
  const allPosts: BlogPost[] = [
    {
      id: 1,
      title: "10 AI Marketing Strategies That Actually Work in 2025",
      slug: "ai-marketing-strategies-2025",
      excerpt: "Discover the top AI-powered marketing strategies that are driving real results for small businesses. From automated content generation to predictive analytics.",
      author: "Sarah Johnson",
      date: "2025-10-15",
      read_time: "8 min read",
      category: "AI Marketing",
      image: "/blog/ai-strategies.jpg",
      tags: ['AI', 'Strategy', 'Automation']
    },
    {
      id: 2,
      title: "SEO in the Age of AI: What's Changed and What Hasn't",
      slug: "seo-age-of-ai",
      excerpt: "AI is revolutionizing SEO, but some fundamentals remain the same. Learn how to balance AI automation with proven SEO best practices.",
      author: "Michael Chen",
      date: "2025-10-12",
      read_time: "6 min read",
      category: "SEO",
      image: "/blog/seo-ai.jpg",
      tags: ['SEO', 'AI', 'Search']
    },
    {
      id: 3,
      title: "How We Generated 10,000 Leads in 30 Days Using AI",
      slug: "10000-leads-30-days-ai",
      excerpt: "A detailed case study of how we used AI-powered lead generation to scale a client's business from 100 to 10,000 qualified leads per month.",
      author: "Emily Rodriguez",
      date: "2025-10-08",
      read_time: "10 min read",
      category: "Case Studies",
      image: "/blog/lead-generation.jpg",
      tags: ['Lead Generation', 'Case Study', 'AI']
    },
    {
      id: 4,
      title: "Social Media Automation: The Complete Guide",
      slug: "social-media-automation-guide",
      excerpt: "Learn how to automate your social media marketing without losing authenticity. Includes templates, tools, and proven workflows.",
      author: "David Kim",
      date: "2025-10-05",
      read_time: "12 min read",
      category: "Social Media",
      image: "/blog/social-automation.jpg",
      tags: ['Social Media', 'Automation', 'Tools']
    },
    {
      id: 5,
      title: "Content Marketing ROI: How to Track What Actually Matters",
      slug: "content-marketing-roi-tracking",
      excerpt: "Stop guessing and start measuring. A practical guide to tracking content marketing ROI with AI-powered analytics.",
      author: "Sarah Johnson",
      date: "2025-10-01",
      read_time: "7 min read",
      category: "Analytics",
      image: "/blog/content-roi.jpg",
      tags: ['Content', 'ROI', 'Analytics']
    },
    {
      id: 6,
      title: "The Future of Email Marketing: AI Personalization at Scale",
      slug: "email-marketing-ai-personalization",
      excerpt: "Discover how AI is enabling hyper-personalized email campaigns that convert 3x better than traditional approaches.",
      author: "Michael Chen",
      date: "2025-09-28",
      read_time: "9 min read",
      category: "Content Strategy",
      image: "/blog/email-ai.jpg",
      tags: ['Email', 'Personalization', 'AI']
    }
  ]

  let filteredPosts = allPosts
  if (params?.category) {
    filteredPosts = allPosts.filter(post => post.category === params.category)
  }

  const offset = params?.offset || 0
  const limit = params?.limit || filteredPosts.length
  const results = filteredPosts.slice(offset, offset + limit)

  return { results, count: filteredPosts.length }
}

function getFallbackBlogPost(slug: string): BlogPost | null {
  const posts = getFallbackBlogPosts().results
  const post = posts.find(p => p.slug === slug)

  if (post) {
    return {
      ...post,
      content: generateFallbackBlogContent(post.title),
      author_bio: "Marketing expert and AI enthusiast with 10+ years of experience helping small businesses grow through data-driven strategies."
    }
  }

  return null
}

function generateFallbackBlogContent(title: string): string {
  return `
# ${title}

This is fallback content for development. In production, this content will come from the Wagtail CMS.

## Introduction

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.

## Key Points

1. **First Important Point**: Detailed explanation of the first key concept
2. **Second Important Point**: Analysis and insights on this topic
3. **Third Important Point**: Practical applications and examples

## Implementation

Here's how you can implement these strategies in your business:

- Step one: Initial setup and configuration
- Step two: Optimization and testing
- Step three: Scaling and monitoring

## Conclusion

These strategies have been proven to work across hundreds of businesses. Start implementing them today to see real results.
  `.trim()
}

function getFallbackResources(params?: { type?: string, limit?: number, offset?: number }) {
  const allResources: Resource[] = [
    {
      id: 1,
      title: "Complete SEO Checklist for 2025",
      slug: "seo-checklist-2025",
      type: "guide",
      description: "A comprehensive 50-point checklist covering technical SEO, on-page optimization, content strategy, and link building. Perfect for businesses looking to improve their search rankings.",
      downloads: 1247,
      image: "/resources/seo-checklist.jpg",
      whats_included: ['50-point checklist', 'Technical SEO guide', 'Content templates', 'Link building strategies']
    },
    {
      id: 2,
      title: "AI Marketing ROI Calculator",
      slug: "roi-calculator",
      type: "calculator",
      description: "Calculate your potential ROI from AI marketing automation. Input your current marketing spend and see projected savings and revenue increase.",
      downloads: 823,
      image: "/resources/roi-calculator.jpg",
      whats_included: ['Excel template', 'ROI formulas', 'Benchmarking data', 'Case study examples']
    },
    {
      id: 3,
      title: "Social Media Content Calendar Template",
      slug: "social-media-calendar",
      type: "template",
      description: "A ready-to-use content calendar template for planning 90 days of social media posts across all major platforms.",
      downloads: 1534,
      image: "/resources/content-calendar.jpg",
      whats_included: ['90-day template', 'Post ideas', 'Best practices', 'Scheduling guide']
    },
    {
      id: 4,
      title: "The Ultimate Guide to Marketing Automation",
      slug: "marketing-automation-guide",
      type: "ebook",
      description: "Learn how to automate your marketing workflows and save 20+ hours per week. Covers email, social media, lead nurturing, and more.",
      downloads: 956,
      image: "/resources/automation-ebook.jpg",
      whats_included: ['78-page ebook', 'Workflow diagrams', 'Tool comparisons', 'Implementation checklist']
    },
    {
      id: 5,
      title: "AI Marketing Trends 2025 Webinar",
      slug: "ai-trends-webinar",
      type: "webinar",
      description: "Watch our recent webinar on emerging AI marketing trends and how to stay ahead of the competition in 2025.",
      downloads: 672,
      image: "/resources/webinar-ai-trends.jpg",
      whats_included: ['60-min recording', 'Slide deck PDF', 'Q&A transcript', 'Resource links']
    },
    {
      id: 6,
      title: "Email Marketing Template Pack",
      slug: "email-templates",
      type: "template",
      description: "20 professionally designed email templates for newsletters, promotions, onboarding, and re-engagement campaigns.",
      downloads: 1891,
      image: "/resources/email-templates.jpg",
      whats_included: ['20 email templates', 'HTML files', 'Design guidelines', 'Best practices']
    },
    {
      id: 7,
      title: "Content Marketing Strategy Workbook",
      slug: "content-strategy-workbook",
      type: "guide",
      description: "A step-by-step workbook to help you build a data-driven content marketing strategy that drives real business results.",
      downloads: 734,
      image: "/resources/content-workbook.jpg",
      whats_included: ['Interactive workbook', 'Strategy templates', 'Content audit sheet', 'KPI tracker']
    },
    {
      id: 8,
      title: "PPC Campaign Budget Calculator",
      slug: "ppc-budget-calculator",
      type: "calculator",
      description: "Optimize your PPC spending across Google Ads, Facebook, and LinkedIn. Calculate optimal bid strategies and expected returns.",
      downloads: 445,
      image: "/resources/ppc-calculator.jpg",
      whats_included: ['Excel calculator', 'Budget formulas', 'Platform comparisons', 'Optimization tips']
    }
  ]

  let filteredResources = allResources
  if (params?.type) {
    filteredResources = allResources.filter(resource => resource.type === params.type)
  }

  const offset = params?.offset || 0
  const limit = params?.limit || filteredResources.length
  const results = filteredResources.slice(offset, offset + limit)

  return { results, count: filteredResources.length }
}

function getFallbackResource(slug: string): Resource | null {
  const resources = getFallbackResources().results
  return resources.find(r => r.slug === slug) || null
}
