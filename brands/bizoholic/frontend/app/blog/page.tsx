'use client'

import { useEffect } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { useState } from 'react'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'

interface BlogPost {
  id: string
  title: string
  excerpt: string
  content: string
  category: string
  author: {
    name: string
    avatar: string
    role: string
  }
  publishedAt: string
  readTime: string
  featured: boolean
  tags: string[]
  image: string
}

export default function BlogPage() {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [blogPosts, setBlogPosts] = useState<BlogPost[]>([])
  const [loading, setLoading] = useState(true)

  const categories = [
    'all',
    'AI Marketing',
    'SEO Strategy',
    'Content Marketing',
    'Social Media',
    'Email Marketing',
    'Data Analytics',
    'Industry Trends'
  ]

  // Fallback blog posts
  const fallbackPosts: BlogPost[] = [
    {
      id: '1',
      title: 'The AI Revolution in Digital Marketing: What You Need to Know in 2024',
      excerpt: 'Discover how artificial intelligence is transforming marketing strategies and what businesses need to do to stay competitive.',
      content: 'Full article content here...',
      category: 'AI Marketing',
      author: {
        name: 'Sarah Johnson',
        avatar: 'https://placehold.co/100x100/2563eb/ffffff?text=SJ',
        role: 'CEO & Founder'
      },
      publishedAt: '2024-01-15',
      readTime: '8 min read',
      featured: true,
      tags: ['AI', 'Marketing Automation', 'Strategy'],
      image: 'https://placehold.co/800x450/2563eb/ffffff?text=AI+Marketing+2024'
    },
    {
      id: '2',
      title: 'Advanced SEO Strategies That Actually Drive Results',
      excerpt: 'Beyond basic optimization: learn the advanced SEO techniques that separate winning brands from the competition.',
      content: 'Full article content here...',
      category: 'SEO Strategy',
      author: {
        name: 'Michael Chen',
        avatar: 'https://placehold.co/100x100/2563eb/ffffff?text=MC',
        role: 'Head of Strategy'
      },
      publishedAt: '2024-01-12',
      readTime: '12 min read',
      featured: true,
      tags: ['SEO', 'Search Strategy', 'Technical SEO'],
      image: 'https://placehold.co/800x450/2563eb/ffffff?text=Advanced+SEO'
    },
    {
      id: '3',
      title: 'Content That Converts: Psychology-Driven Marketing Strategies',
      excerpt: 'Understand the psychological triggers that make content irresistible and drive real business results.',
      content: 'Full article content here...',
      category: 'Content Marketing',
      author: {
        name: 'Emily Rodriguez',
        avatar: 'https://placehold.co/100x100/2563eb/ffffff?text=ER',
        role: 'Creative Director'
      },
      publishedAt: '2024-01-10',
      readTime: '10 min read',
      featured: false,
      tags: ['Content Strategy', 'Psychology', 'Conversion'],
      image: 'https://placehold.co/800x450/2563eb/ffffff?text=Content+Psychology'
    },
    {
      id: '4',
      title: 'Social Media ROI: Measuring What Actually Matters',
      excerpt: 'Move beyond vanity metrics and discover the KPIs that truly indicate social media success.',
      content: 'Full article content here...',
      category: 'Social Media',
      author: {
        name: 'David Kim',
        avatar: 'https://placehold.co/100x100/2563eb/ffffff?text=DK',
        role: 'Tech Lead'
      },
      publishedAt: '2024-01-08',
      readTime: '7 min read',
      featured: false,
      tags: ['Social Media', 'Analytics', 'ROI'],
      image: 'https://placehold.co/800x450/2563eb/ffffff?text=Social+Media+ROI'
    },
    {
      id: '5',
      title: 'Email Marketing in 2024: Personalization at Scale',
      excerpt: 'Learn how to create highly personalized email campaigns that feel human while serving thousands of customers.',
      content: 'Full article content here...',
      category: 'Email Marketing',
      author: {
        name: 'Sarah Johnson',
        avatar: 'https://placehold.co/100x100/2563eb/ffffff?text=SJ',
        role: 'CEO & Founder'
      },
      publishedAt: '2024-01-05',
      readTime: '9 min read',
      featured: false,
      tags: ['Email Marketing', 'Personalization', 'Automation'],
      image: 'https://placehold.co/800x450/2563eb/ffffff?text=Email+Marketing'
    },
    {
      id: '6',
      title: 'Data-Driven Marketing: Making Decisions That Drive Growth',
      excerpt: 'Transform your marketing from guesswork to science with these data analysis frameworks and tools.',
      content: 'Full article content here...',
      category: 'Data Analytics',
      author: {
        name: 'Michael Chen',
        avatar: 'https://placehold.co/100x100/2563eb/ffffff?text=MC',
        role: 'Head of Strategy'
      },
      publishedAt: '2024-01-03',
      readTime: '11 min read',
      featured: false,
      tags: ['Data Analytics', 'Growth Marketing', 'KPIs'],
      image: 'https://placehold.co/800x450/2563eb/ffffff?text=Data+Driven'
    }
  ]

  useEffect(() => {
    const fetchBlogPosts = async () => {
      try {
        const response = await fetch('/api/brain/wagtail/blog')
        if (response.ok) {
          const data = await response.json()
          if (data.posts && data.posts.length > 0) {
            setBlogPosts(data.posts)
          } else {
            setBlogPosts(fallbackPosts)
          }
        } else {
          setBlogPosts(fallbackPosts)
        }
      } catch (error) {
        console.error('Error fetching blog posts:', error)
        setBlogPosts(fallbackPosts)
      } finally {
        setLoading(false)
      }
    }

    fetchBlogPosts()
  }, [])

  const featuredPosts = blogPosts.filter(post => post.featured)
  const regularPosts = blogPosts.filter(post => !post.featured)

  const filteredPosts = blogPosts.filter(post => {
    const matchesCategory = selectedCategory === 'all' || post.category === selectedCategory
    const matchesSearch = post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      post.excerpt.toLowerCase().includes(searchQuery.toLowerCase()) ||
      post.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
    return matchesCategory && matchesSearch
  })

  const handleNewsletterSignup = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const email = formData.get('email') as string

    try {
      const response = await fetch('/api/brain/wagtail/newsletter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          source: 'blog_signup',
          interests: ['marketing_insights', 'industry_trends']
        }),
      })

      if (response.ok) {
        alert('Successfully subscribed to our newsletter!')
        e.currentTarget.reset()
      } else {
        throw new Error('Signup failed')
      }
    } catch (error) {
      console.error('Newsletter signup error:', error)
      alert('There was an error signing up. Please try again.')
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      {/* Hero Section */}
      <section className="py-20 bg-muted/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-foreground mb-6">
              Marketing <span className="text-primary">Insights</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Expert strategies, industry trends, and actionable insights to help your business dominate the digital landscape.
            </p>
          </div>

          {/* Search and Filter */}
          <div className="max-w-4xl mx-auto mb-12">
            <div className="flex flex-col md:flex-row gap-4 mb-8">
              <div className="flex-1">
                <input
                  type="text"
                  placeholder="Search articles..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-4 py-3 border border-input bg-background rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-4 py-3 border border-input bg-background rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                {categories.map(category => (
                  <option key={category} value={category}>
                    {category === 'all' ? 'All Categories' : category}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Articles */}
      {selectedCategory === 'all' && searchQuery === '' && (
        <section className="py-16 bg-background">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-foreground mb-12 text-center">Featured Articles</h2>
            <div className="grid md:grid-cols-2 gap-8">
              {featuredPosts.map(post => (
                <article key={post.id} className="bg-card rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow border border-border">
                  <div className="aspect-video bg-gray-200 relative">
                    <Image
                      src={post.image}
                      alt={post.title}
                      fill
                      className="object-cover"
                    />
                    <div className="absolute top-4 left-4">
                      <span className="bg-primary text-primary-foreground px-3 py-1 rounded-full text-sm font-medium">
                        Featured
                      </span>
                    </div>
                  </div>
                  <div className="p-6">
                    <div className="flex items-center mb-4">
                      <Image
                        src={post.author.avatar}
                        alt={post.author.name}
                        width={40}
                        height={40}
                        className="rounded-full mr-3"
                      />
                      <div>
                        <p className="text-sm font-medium text-foreground">{post.author.name}</p>
                        <p className="text-xs text-muted-foreground">{post.author.role}</p>
                      </div>
                      <div className="ml-auto text-right">
                        <p className="text-xs text-muted-foreground">{new Date(post.publishedAt).toLocaleDateString()}</p>
                        <p className="text-xs text-muted-foreground">{post.readTime}</p>
                      </div>
                    </div>
                    <h3 className="text-xl font-bold text-foreground mb-3">{post.title}</h3>
                    <p className="text-muted-foreground mb-4">{post.excerpt}</p>
                    <div className="flex flex-wrap gap-2 mb-4">
                      {post.tags.map(tag => (
                        <span key={tag} className="bg-secondary text-secondary-foreground px-2 py-1 rounded text-xs">
                          {tag}
                        </span>
                      ))}
                    </div>
                    <Link
                      href={`/blog/${post.id}`}
                      className="inline-flex items-center text-primary hover:text-primary/80 font-medium"
                    >
                      Read Full Article
                      <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </Link>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* All Articles */}
      <section className="py-16 bg-muted/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-foreground mb-12 text-center">
            {selectedCategory === 'all' ? 'Latest Articles' : `${selectedCategory} Articles`}
          </h2>

          {filteredPosts.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground text-lg">No articles found matching your criteria.</p>
              <button
                onClick={() => {
                  setSelectedCategory('all')
                  setSearchQuery('')
                }}
                className="mt-4 text-primary hover:text-primary/80 font-medium"
              >
                Clear filters
              </button>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredPosts.map(post => (
                <article key={post.id} className="bg-card rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow border border-border">
                  <div className="aspect-video bg-gray-200 relative">
                    <Image
                      src={post.image}
                      alt={post.title}
                      fill
                      className="object-cover"
                    />
                    <div className="absolute top-4 left-4">
                      <span className="bg-foreground text-background px-3 py-1 rounded-full text-sm">
                        {post.category}
                      </span>
                    </div>
                  </div>
                  <div className="p-6">
                    <div className="flex items-center mb-4">
                      <Image
                        src={post.author.avatar}
                        alt={post.author.name}
                        width={32}
                        height={32}
                        className="rounded-full mr-3"
                      />
                      <div className="flex-1">
                        <p className="text-sm font-medium text-foreground">{post.author.name}</p>
                        <div className="flex items-center text-xs text-muted-foreground">
                          <span>{new Date(post.publishedAt).toLocaleDateString()}</span>
                          <span className="mx-1">•</span>
                          <span>{post.readTime}</span>
                        </div>
                      </div>
                    </div>
                    <h3 className="text-lg font-bold text-foreground mb-3 line-clamp-2">{post.title}</h3>
                    <p className="text-muted-foreground mb-4 line-clamp-3">{post.excerpt}</p>
                    <div className="flex flex-wrap gap-2 mb-4">
                      {post.tags.slice(0, 2).map(tag => (
                        <span key={tag} className="bg-secondary text-secondary-foreground px-2 py-1 rounded text-xs">
                          {tag}
                        </span>
                      ))}
                      {post.tags.length > 2 && (
                        <span className="text-muted-foreground text-xs">+{post.tags.length - 2} more</span>
                      )}
                    </div>
                    <Link
                      href={`/blog/${post.id}`}
                      className="inline-flex items-center text-primary hover:text-primary/80 font-medium"
                    >
                      Read Article
                      <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </Link>
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Newsletter Signup */}
      <section className="py-16 bg-primary">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-primary-foreground mb-4">
            Stay Ahead of the Curve
          </h2>
          <p className="text-xl text-primary-foreground/90 mb-8">
            Get weekly marketing insights and exclusive strategies delivered to your inbox
          </p>
          <form onSubmit={handleNewsletterSignup} className="max-w-md mx-auto">
            <div className="flex flex-col sm:flex-row gap-4">
              <input
                type="email"
                name="email"
                placeholder="Enter your email"
                required
                className="flex-1 px-4 py-3 rounded-lg border-0 focus:ring-2 focus:ring-ring bg-background text-foreground"
              />
              <button
                type="submit"
                className="bg-background text-primary px-6 py-3 rounded-lg font-semibold hover:bg-background/90 transition-colors"
              >
                Subscribe
              </button>
            </div>
          </form>
          <p className="text-sm text-primary-foreground/80 mt-4">
            No spam, unsubscribe anytime. We respect your privacy.
          </p>
        </div>
      </section>

      <Footer />
    </div>
  )
}