/**
 * Bizoholic Blog/Insights Page
 * Marketing insights, industry trends, and expert commentary
 */

'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useState } from 'react'

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

  const blogPosts: BlogPost[] = [
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
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center space-x-2">
              <Image 
                src="/images/logo.png" 
                alt="Bizoholic" 
                width={40} 
                height={40}
                className="w-10 h-10"
              />
              <span className="text-2xl font-bold text-gray-900">Bizoholic</span>
            </Link>
            <nav className="hidden md:flex space-x-8">
              <Link href="/" className="text-gray-700 hover:text-blue-600 transition-colors">Home</Link>
              <Link href="/about" className="text-gray-700 hover:text-blue-600 transition-colors">About</Link>
              <Link href="/portfolio" className="text-gray-700 hover:text-blue-600 transition-colors">Portfolio</Link>
              <Link href="/pricing" className="text-gray-700 hover:text-blue-600 transition-colors">Pricing</Link>
              <Link href="/blog" className="text-blue-600 font-medium">Blog</Link>
              <Link href="/contact" className="text-gray-700 hover:text-blue-600 transition-colors">Contact</Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-purple-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              Marketing <span className="text-blue-600">Insights</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
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
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">Featured Articles</h2>
            <div className="grid md:grid-cols-2 gap-8">
              {featuredPosts.map(post => (
                <article key={post.id} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
                  <div className="aspect-video bg-gray-200 relative">
                    <Image
                      src={post.image}
                      alt={post.title}
                      fill
                      className="object-cover"
                    />
                    <div className="absolute top-4 left-4">
                      <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
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
                        <p className="text-sm font-medium text-gray-900">{post.author.name}</p>
                        <p className="text-xs text-gray-500">{post.author.role}</p>
                      </div>
                      <div className="ml-auto text-right">
                        <p className="text-xs text-gray-500">{new Date(post.publishedAt).toLocaleDateString()}</p>
                        <p className="text-xs text-gray-500">{post.readTime}</p>
                      </div>
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 mb-3">{post.title}</h3>
                    <p className="text-gray-600 mb-4">{post.excerpt}</p>
                    <div className="flex flex-wrap gap-2 mb-4">
                      {post.tags.map(tag => (
                        <span key={tag} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
                          {tag}
                        </span>
                      ))}
                    </div>
                    <Link
                      href={`/blog/${post.id}`}
                      className="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium"
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
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">
            {selectedCategory === 'all' ? 'Latest Articles' : `${selectedCategory} Articles`}
          </h2>
          
          {filteredPosts.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600 text-lg">No articles found matching your criteria.</p>
              <button
                onClick={() => {
                  setSelectedCategory('all')
                  setSearchQuery('')
                }}
                className="mt-4 text-blue-600 hover:text-blue-700 font-medium"
              >
                Clear filters
              </button>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredPosts.map(post => (
                <article key={post.id} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
                  <div className="aspect-video bg-gray-200 relative">
                    <Image
                      src={post.image}
                      alt={post.title}
                      fill
                      className="object-cover"
                    />
                    <div className="absolute top-4 left-4">
                      <span className="bg-gray-900 text-white px-3 py-1 rounded-full text-sm">
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
                        <p className="text-sm font-medium text-gray-900">{post.author.name}</p>
                        <div className="flex items-center text-xs text-gray-500">
                          <span>{new Date(post.publishedAt).toLocaleDateString()}</span>
                          <span className="mx-1">•</span>
                          <span>{post.readTime}</span>
                        </div>
                      </div>
                    </div>
                    <h3 className="text-lg font-bold text-gray-900 mb-3 line-clamp-2">{post.title}</h3>
                    <p className="text-gray-600 mb-4 line-clamp-3">{post.excerpt}</p>
                    <div className="flex flex-wrap gap-2 mb-4">
                      {post.tags.slice(0, 2).map(tag => (
                        <span key={tag} className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
                          {tag}
                        </span>
                      ))}
                      {post.tags.length > 2 && (
                        <span className="text-gray-500 text-xs">+{post.tags.length - 2} more</span>
                      )}
                    </div>
                    <Link
                      href={`/blog/${post.id}`}
                      className="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium"
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
      <section className="py-16 bg-blue-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Stay Ahead of the Curve
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Get weekly marketing insights and exclusive strategies delivered to your inbox
          </p>
          <form onSubmit={handleNewsletterSignup} className="max-w-md mx-auto">
            <div className="flex flex-col sm:flex-row gap-4">
              <input
                type="email"
                name="email"
                placeholder="Enter your email"
                required
                className="flex-1 px-4 py-3 rounded-lg border-0 focus:ring-2 focus:ring-blue-300"
              />
              <button
                type="submit"
                className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Subscribe
              </button>
            </div>
          </form>
          <p className="text-sm text-blue-100 mt-4">
            No spam, unsubscribe anytime. We respect your privacy.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Image 
                  src="/images/logo.png" 
                  alt="Bizoholic" 
                  width={32} 
                  height={32}
                  className="w-8 h-8"
                />
                <span className="text-xl font-bold">Bizoholic</span>
              </div>
              <p className="text-gray-400">
                Transforming businesses through intelligent digital marketing strategies.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Services</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/seo" className="hover:text-white transition-colors">SEO Optimization</Link></li>
                <li><Link href="/social-media-marketing" className="hover:text-white transition-colors">Social Media</Link></li>
                <li><Link href="/content-marketing" className="hover:text-white transition-colors">Content Marketing</Link></li>
                <li><Link href="/ai-campaign-management" className="hover:text-white transition-colors">AI Campaigns</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/about" className="hover:text-white transition-colors">About</Link></li>
                <li><Link href="/portfolio" className="hover:text-white transition-colors">Portfolio</Link></li>
                <li><Link href="/blog" className="hover:text-white transition-colors">Blog</Link></li>
                <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Contact</h3>
              <ul className="space-y-2 text-gray-400">
                <li>hello@bizoholic.com</li>
                <li>+1 (555) 123-4567</li>
                <li>San Francisco, CA</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Bizoholic. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}