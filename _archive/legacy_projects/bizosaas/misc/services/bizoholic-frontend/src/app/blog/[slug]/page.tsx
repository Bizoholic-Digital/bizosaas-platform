'use client'

import { useParams } from 'next/navigation'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Link from 'next/link'
import { Calendar, Clock, ArrowLeft, Share2 } from 'lucide-react'

export default function BlogPostPage() {
  const params = useParams()
  const slug = params.slug as string
  // Mock data - will be replaced with Wagtail CMS data
  const post = {
    title: '10 Ways AI Marketing Automation Can Transform Your Business',
    excerpt: 'Discover how AI-powered marketing automation can save time, reduce costs, and increase ROI.',
    category: 'AI Marketing',
    author: 'John Smith',
    authorRole: 'Chief Marketing Officer',
    date: '2025-01-15',
    readTime: '8 min read',
    image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200',
    content: `
      <p>Marketing automation powered by artificial intelligence is revolutionizing how businesses connect with customers and drive growth. In this comprehensive guide, we'll explore 10 transformative ways AI can elevate your marketing efforts.</p>

      <h2>1. Predictive Lead Scoring</h2>
      <p>AI algorithms analyze historical data to predict which leads are most likely to convert, allowing your sales team to focus on high-value prospects.</p>

      <h2>2. Personalized Content Recommendations</h2>
      <p>Machine learning models understand user behavior and preferences, delivering personalized content that resonates with each visitor.</p>

      <h2>3. Automated Email Campaigns</h2>
      <p>AI determines the optimal send times, subject lines, and content for each recipient, significantly improving open and click-through rates.</p>

      <h2>4. Chatbot Customer Service</h2>
      <p>24/7 AI-powered chatbots handle common inquiries, qualify leads, and provide instant support, improving customer satisfaction.</p>

      <h2>5. Dynamic Pricing Optimization</h2>
      <p>AI analyzes market conditions, competitor pricing, and demand patterns to optimize your pricing strategy in real-time.</p>

      <h2>Conclusion</h2>
      <p>AI marketing automation isn't just a trend—it's a fundamental shift in how businesses operate. Companies that embrace these technologies now will have a significant competitive advantage in the years ahead.</p>
    `
  }

  return (
    <>
      <Navigation />
      <main className="min-h-screen bg-white">
        {/* Hero Section */}
        <section className="bg-gray-50 py-12">
          <div className="container">
            <Link
              href="/blog"
              className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-6"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Blog
            </Link>
            <div className="max-w-4xl">
              <div className="flex flex-wrap items-center gap-4 mb-4">
                <span className="px-3 py-1 bg-primary-600 text-white text-sm font-semibold rounded-full">
                  {post.category}
                </span>
                <div className="flex items-center text-gray-600">
                  <Calendar className="w-4 h-4 mr-2" />
                  {new Date(post.date).toLocaleDateString('en-US', {
                    month: 'long',
                    day: 'numeric',
                    year: 'numeric'
                  })}
                </div>
                <div className="flex items-center text-gray-600">
                  <Clock className="w-4 h-4 mr-2" />
                  {post.readTime}
                </div>
              </div>
              <h1 className="text-5xl font-bold text-gray-900 mb-6">
                {post.title}
              </h1>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-gray-300 rounded-full mr-4"></div>
                  <div>
                    <p className="font-semibold text-gray-900">{post.author}</p>
                    <p className="text-sm text-gray-600">{post.authorRole}</p>
                  </div>
                </div>
                <button className="flex items-center gap-2 btn-secondary px-4 py-2">
                  <Share2 className="w-4 h-4" />
                  Share
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Featured Image */}
        <section className="py-12">
          <div className="container">
            <div className="max-w-4xl mx-auto">
              <img
                src={post.image}
                alt={post.title}
                className="w-full aspect-video object-cover rounded-xl"
              />
            </div>
          </div>
        </section>

        {/* Article Content */}
        <section className="py-12">
          <div className="container">
            <div className="max-w-4xl mx-auto">
              <div
                className="prose prose-lg max-w-none"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-gray-50">
          <div className="container">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Ready to Transform Your Marketing?
              </h2>
              <p className="text-lg text-gray-600 mb-8">
                Get started with Bizoholic AI-powered marketing automation today
              </p>
              <Link href="/contact" className="btn-primary px-8 py-3">
                Get Started Free
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
