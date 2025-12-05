'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import { getBlogPosts, getBlogCategories, subscribeNewsletter, type BlogPost } from '@/lib/wagtail-client'
import {
  Search,
  Calendar,
  Clock,
  User,
  Tag,
  ArrowRight,
  Mail,
  CheckCircle2
} from 'lucide-react'

export default function BlogPage() {
  const [posts, setPosts] = useState<BlogPost[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string>('')
  const [searchQuery, setSearchQuery] = useState('')
  const [newsletterEmail, setNewsletterEmail] = useState('')
  const [newsletterStatus, setNewsletterStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    async function loadBlogData() {
      setIsLoading(true)
      const [postsData, categoriesData] = await Promise.all([
        getBlogPosts({ category: selectedCategory || undefined }),
        getBlogCategories()
      ])
      setPosts(postsData.results)
      setCategories(categoriesData)
      setIsLoading(false)
    }

    loadBlogData()
  }, [selectedCategory])

  const handleNewsletterSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const success = await subscribeNewsletter(newsletterEmail)
    setNewsletterStatus(success ? 'success' : 'error')
    if (success) setNewsletterEmail('')
  }

  const filteredPosts = posts.filter(post =>
    searchQuery === '' ||
    post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    post.excerpt.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <>
      <Navigation />
      <main className="pt-20">
        {/* Breadcrumb */}
        <div className="container py-8">
          <Breadcrumb items={[{ label: 'Blog' }]} />
        </div>

        {/* Hero Section */}
        <section className="py-16 md:py-24 bg-gray-50">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h1 className="heading-1 mb-6">Latest Insights from Bizoholic</h1>
              <p className="text-xl text-gray-600 mb-8">
                Expert tips, strategies, and case studies on AI-powered marketing,
                SEO, social media, and growing your business.
              </p>

              {/* Search Bar */}
              <div className="max-w-2xl mx-auto">
                <div className="relative">
                  <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search articles..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-12 pr-4 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Main Content */}
        <section className="py-16 md:py-24">
          <div className="container px-4">
            <div className="grid lg:grid-cols-4 gap-12">
              {/* Sidebar - Categories Filter */}
              <aside className="lg:col-span-1">
                <div className="card-premium p-6 sticky top-24">
                  <h3 className="font-semibold text-gray-900 mb-4">Categories</h3>
                  <div className="space-y-2">
                    <button
                      onClick={() => setSelectedCategory('')}
                      className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                        selectedCategory === ''
                          ? 'bg-primary-100 text-primary-700 font-medium'
                          : 'text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      All Articles
                    </button>
                    {categories.map((category) => (
                      <button
                        key={category}
                        onClick={() => setSelectedCategory(category)}
                        className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                          selectedCategory === category
                            ? 'bg-primary-100 text-primary-700 font-medium'
                            : 'text-gray-600 hover:bg-gray-100'
                        }`}
                      >
                        {category}
                      </button>
                    ))}
                  </div>

                  {/* Newsletter Signup */}
                  <div className="mt-8 pt-8 border-t border-gray-200">
                    <h3 className="font-semibold text-gray-900 mb-2">Stay Updated</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Get the latest insights delivered to your inbox weekly.
                    </p>

                    {newsletterStatus === 'success' ? (
                      <div className="flex items-center gap-2 text-sm text-green-600">
                        <CheckCircle2 className="h-5 w-5" />
                        <span>Subscribed!</span>
                      </div>
                    ) : (
                      <form onSubmit={handleNewsletterSubmit} className="space-y-3">
                        <input
                          type="email"
                          placeholder="Your email"
                          value={newsletterEmail}
                          onChange={(e) => setNewsletterEmail(e.target.value)}
                          required
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        />
                        <button type="submit" className="btn-primary w-full py-2 text-sm">
                          Subscribe
                          <Mail className="ml-2 h-4 w-4" />
                        </button>
                      </form>
                    )}

                    {newsletterStatus === 'error' && (
                      <p className="text-sm text-red-600 mt-2">Failed to subscribe. Please try again.</p>
                    )}
                  </div>
                </div>
              </aside>

              {/* Blog Posts Grid */}
              <div className="lg:col-span-3">
                {isLoading ? (
                  <div className="text-center py-12">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                    <p className="mt-4 text-gray-600">Loading articles...</p>
                  </div>
                ) : filteredPosts.length === 0 ? (
                  <div className="text-center py-12">
                    <p className="text-gray-600">No articles found matching your search.</p>
                  </div>
                ) : (
                  <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-8">
                    {filteredPosts.map((post) => (
                      <article key={post.id} className="card-premium overflow-hidden group hover:shadow-xl transition-all duration-300">
                        {/* Featured Image */}
                        <div className="relative h-48 bg-primary-100 overflow-hidden">
                          <div className="absolute inset-0 flex items-center justify-center">
                            <Tag className="h-16 w-16 text-primary-300" />
                          </div>
                          <div className="absolute top-4 left-4">
                            <span className="inline-block px-3 py-1 bg-primary-600 text-white text-xs font-medium rounded-full">
                              {post.category}
                            </span>
                          </div>
                        </div>

                        {/* Content */}
                        <div className="p-6">
                          <h2 className="text-xl font-semibold text-gray-900 mb-3 group-hover:text-primary-600 transition-colors line-clamp-2">
                            <Link href={`/blog/${post.slug}`}>
                              {post.title}
                            </Link>
                          </h2>

                          <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                            {post.excerpt}
                          </p>

                          {/* Meta Info */}
                          <div className="flex flex-wrap gap-4 text-xs text-gray-500 mb-4">
                            <div className="flex items-center gap-1">
                              <User className="h-4 w-4" />
                              <span>{post.author}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Calendar className="h-4 w-4" />
                              <span>{new Date(post.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Clock className="h-4 w-4" />
                              <span>{post.read_time}</span>
                            </div>
                          </div>

                          {/* Read More Link */}
                          <Link
                            href={`/blog/${post.slug}`}
                            className="inline-flex items-center text-primary-600 hover:text-primary-700 font-medium text-sm group"
                          >
                            Read More
                            <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                          </Link>
                        </div>
                      </article>
                    ))}
                  </div>
                )}

                {/* Pagination */}
                {!isLoading && filteredPosts.length > 0 && (
                  <div className="mt-12 flex justify-center gap-2">
                    <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                      Previous
                    </button>
                    <button className="px-4 py-2 bg-primary-600 text-white rounded-lg">
                      1
                    </button>
                    <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                      2
                    </button>
                    <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                      3
                    </button>
                    <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                      Next
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 md:py-28 bg-primary-600 text-white">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-4xl font-bold mb-6">
                Ready to Transform Your Marketing?
              </h2>
              <p className="text-xl text-primary-100 mb-8">
                Stop reading and start doing. Our AI platform delivers the results you've been
                reading about.
              </p>
              <div className="flex flex-wrap gap-4 justify-center">
                <Link href="/contact" className="btn-white">
                  Get Started Free
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
                <Link href="/services" className="btn-white-outline">
                  View Our Services
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
