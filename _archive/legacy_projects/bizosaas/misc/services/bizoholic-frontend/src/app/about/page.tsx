import { Metadata } from 'next'
import Link from 'next/link'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import {
  Target,
  Eye,
  Heart,
  TrendingUp,
  Users,
  Zap,
  Shield,
  Award,
  Cpu,
  Cloud,
  Lock,
  Sparkles,
  CheckCircle2,
  ArrowRight
} from 'lucide-react'

export default function AboutPage() {
  return (
    <>
      <Navigation />
      <main className="pt-20">
        {/* Breadcrumb */}
        <div className="container py-8">
          <Breadcrumb items={[{ label: 'About Us' }]} />
        </div>

        {/* Hero Section */}
        <section className="py-16 md:py-24 bg-gray-50">
          <div className="container px-4">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="heading-1 mb-6">
                Transforming Small Business Marketing with AI
              </h1>
              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                We believe every small business deserves access to enterprise-level marketing automation.
                That's why we've built the most affordable, powerful, and easy-to-use AI marketing platform
                on the market.
              </p>
              <div className="flex flex-wrap gap-4 justify-center">
                <Link href="/contact" className="btn-primary">
                  Get Started Today
                </Link>
                <Link href="/services" className="btn-secondary">
                  Explore Our Services
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Mission & Vision */}
        <section className="py-16 md:py-24">
          <div className="container px-4">
            <div className="grid md:grid-cols-2 gap-12">
              {/* Mission */}
              <div className="card-premium p-8">
                <div className="w-16 h-16 bg-primary-100 rounded-2xl flex items-center justify-center mb-6">
                  <Target className="h-8 w-8 text-primary-600" />
                </div>
                <h2 className="heading-2 mb-4">Our Mission</h2>
                <p className="text-gray-600 leading-relaxed">
                  To democratize marketing automation by making enterprise-level AI technology accessible
                  and affordable for small businesses worldwide. We're committed to delivering 75% cost
                  savings while maintaining premium quality and exceptional results.
                </p>
              </div>

              {/* Vision */}
              <div className="card-premium p-8">
                <div className="w-16 h-16 bg-secondary-100 rounded-2xl flex items-center justify-center mb-6">
                  <Eye className="h-8 w-8 text-secondary-600" />
                </div>
                <h2 className="heading-2 mb-4">Our Vision</h2>
                <p className="text-gray-600 leading-relaxed">
                  To become the world's most trusted AI marketing partner for small businesses, empowering
                  millions of entrepreneurs to compete with enterprise brands through intelligent automation,
                  data-driven insights, and continuous innovation.
                </p>
              </div>
            </div>

            {/* Values */}
            <div className="mt-12 text-center">
              <h3 className="heading-3 mb-8">Our Core Values</h3>
              <div className="grid md:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Heart className="h-6 w-6 text-blue-600" />
                  </div>
                  <h4 className="font-semibold text-gray-900 mb-2">Customer First</h4>
                  <p className="text-sm text-gray-600">Your success is our success</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Sparkles className="h-6 w-6 text-green-600" />
                  </div>
                  <h4 className="font-semibold text-gray-900 mb-2">Innovation</h4>
                  <p className="text-sm text-gray-600">Always pushing boundaries</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Shield className="h-6 w-6 text-purple-600" />
                  </div>
                  <h4 className="font-semibold text-gray-900 mb-2">Integrity</h4>
                  <p className="text-sm text-gray-600">Transparent and honest</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Award className="h-6 w-6 text-orange-600" />
                  </div>
                  <h4 className="font-semibold text-gray-900 mb-2">Excellence</h4>
                  <p className="text-sm text-gray-600">Premium quality always</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Our Story */}
        <section className="py-16 md:py-24 bg-gray-50">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto">
              <h2 className="heading-2 text-center mb-12">Our Story</h2>

              <div className="space-y-8">
                <div className="card-premium p-8">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <Sparkles className="h-6 w-6 text-primary-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-2">The Beginning</h3>
                      <p className="text-gray-600 leading-relaxed">
                        Bizoholic was founded on a simple observation: small businesses were being left behind
                        in the digital marketing revolution. Enterprise companies had access to sophisticated
                        marketing automation, but the cost was prohibitive for smaller players. We knew there
                        had to be a better way.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="card-premium p-8">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-secondary-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <Cpu className="h-6 w-6 text-secondary-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-2">The Innovation</h3>
                      <p className="text-gray-600 leading-relaxed">
                        We assembled a team of AI engineers, marketing experts, and business strategists to
                        build something revolutionary. By leveraging modern microservices architecture, advanced
                        AI models, and intelligent automation, we created a platform that delivers enterprise
                        results at a fraction of the cost.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="card-premium p-8">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <TrendingUp className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-2">The Impact</h3>
                      <p className="text-gray-600 leading-relaxed">
                        Today, we're proud to serve over 500 small businesses worldwide, helping them achieve
                        marketing results that were previously out of reach. Our clients see an average 4.8x ROI
                        within their first month, and we're just getting started.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Statistics */}
        <section className="py-16 md:py-24">
          <div className="container px-4">
            <div className="text-center mb-12">
              <h2 className="heading-2 mb-4">By the Numbers</h2>
              <p className="text-xl text-gray-600">Real results from real businesses</p>
            </div>

            <div className="grid md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="stat-card">
                  <div className="stat-number text-primary-600">500+</div>
                  <div className="stat-label">Clients Served</div>
                  <p className="text-sm text-gray-600 mt-2">Small businesses worldwide</p>
                </div>
              </div>

              <div className="text-center">
                <div className="stat-card">
                  <div className="stat-number text-secondary-600">4.8x</div>
                  <div className="stat-label">Average ROI</div>
                  <p className="text-sm text-gray-600 mt-2">Within first month</p>
                </div>
              </div>

              <div className="text-center">
                <div className="stat-card">
                  <div className="stat-number text-blue-600">93+</div>
                  <div className="stat-label">AI Agents</div>
                  <p className="text-sm text-gray-600 mt-2">Autonomous marketing experts</p>
                </div>
              </div>

              <div className="text-center">
                <div className="stat-card">
                  <div className="stat-number text-green-600">75%</div>
                  <div className="stat-label">Cost Reduction</div>
                  <p className="text-sm text-gray-600 mt-2">vs. traditional agencies</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Technology Showcase */}
        <section className="py-16 md:py-24 bg-gray-900 text-white">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto text-center mb-12">
              <h2 className="text-4xl font-bold mb-4">Built for the Future</h2>
              <p className="text-xl text-gray-300">
                Enterprise-grade technology that scales with your business
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-primary-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <Cpu className="h-8 w-8 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Advanced AI Technology</h3>
                <p className="text-gray-300 leading-relaxed">
                  Powered by 93+ specialized AI agents that autonomously manage campaigns, analyze data,
                  and optimize performance 24/7.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-secondary-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <Cloud className="h-8 w-8 text-secondary-600" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Microservices Architecture</h3>
                <p className="text-gray-300 leading-relaxed">
                  Modern, scalable infrastructure built with Next.js 15, FastAPI, and Domain-Driven Design
                  principles for maximum reliability.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <Lock className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Security & Reliability</h3>
                <p className="text-gray-300 leading-relaxed">
                  Enterprise-grade security with multi-tenant isolation, encrypted data storage, and
                  99.9% uptime SLA.
                </p>
              </div>
            </div>

            <div className="mt-12 text-center">
              <div className="inline-flex items-center gap-6 bg-gray-800 border border-gray-700 rounded-2xl px-8 py-6">
                <div className="text-left">
                  <div className="text-sm text-gray-400 mb-1">Tech Stack</div>
                  <div className="font-semibold">Next.js 15 • React 18 • TypeScript • FastAPI • PostgreSQL</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Team Section */}
        <section className="py-16 md:py-24">
          <div className="container px-4">
            <div className="text-center mb-12">
              <h2 className="heading-2 mb-4">Meet Our Leadership</h2>
              <p className="text-xl text-gray-600">Experts in AI, marketing, and business growth</p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {/* Team Member 1 */}
              <div className="card-premium p-6 text-center">
                <div className="w-24 h-24 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users className="h-12 w-12 text-primary-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">Leadership Team</h3>
                <p className="text-sm text-primary-600 mb-3">Founders & Executives</p>
                <p className="text-sm text-gray-600">
                  20+ years combined experience in AI, digital marketing, and SaaS platforms
                </p>
              </div>

              {/* Team Member 2 */}
              <div className="card-premium p-6 text-center">
                <div className="w-24 h-24 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Cpu className="h-12 w-12 text-secondary-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">AI Engineering</h3>
                <p className="text-sm text-secondary-600 mb-3">Technical Experts</p>
                <p className="text-sm text-gray-600">
                  Specialists in machine learning, NLP, and autonomous agent systems
                </p>
              </div>

              {/* Team Member 3 */}
              <div className="card-premium p-6 text-center">
                <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <TrendingUp className="h-12 w-12 text-blue-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">Marketing Strategy</h3>
                <p className="text-sm text-blue-600 mb-3">Growth Advisors</p>
                <p className="text-sm text-gray-600">
                  Proven track record of scaling businesses and driving measurable ROI
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Why Choose Us */}
        <section className="py-16 md:py-24 bg-gray-50">
          <div className="container px-4">
            <div className="text-center mb-12">
              <h2 className="heading-2 mb-4">Why Choose Bizoholic?</h2>
              <p className="text-xl text-gray-600">What makes us different from everyone else</p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              <div className="card-premium p-6">
                <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center mb-4">
                  <Zap className="h-6 w-6 text-primary-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Lightning-Fast Setup</h3>
                <p className="text-gray-600">
                  Get started in just 15 minutes. No complex onboarding, no lengthy contracts, no headaches.
                </p>
              </div>

              <div className="card-premium p-6">
                <div className="w-12 h-12 bg-secondary-100 rounded-xl flex items-center justify-center mb-4">
                  <TrendingUp className="h-6 w-6 text-secondary-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Proven ROI</h3>
                <p className="text-gray-600">
                  See measurable results within 7 days. Our clients average 4.8x ROI in their first month.
                </p>
              </div>

              <div className="card-premium p-6">
                <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-4">
                  <Cpu className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">93+ AI Agents</h3>
                <p className="text-gray-600">
                  Autonomous agents handle everything from SEO to social media, working 24/7 for your business.
                </p>
              </div>

              <div className="card-premium p-6">
                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mb-4">
                  <CheckCircle2 className="h-6 w-6 text-green-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">75% Cost Savings</h3>
                <p className="text-gray-600">
                  Get enterprise-level marketing at a fraction of the cost of traditional agencies.
                </p>
              </div>

              <div className="card-premium p-6">
                <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mb-4">
                  <Shield className="h-6 w-6 text-purple-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Enterprise Security</h3>
                <p className="text-gray-600">
                  Bank-level encryption, multi-tenant isolation, and 99.9% uptime guarantee.
                </p>
              </div>

              <div className="card-premium p-6">
                <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center mb-4">
                  <Users className="h-6 w-6 text-orange-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Dedicated Support</h3>
                <p className="text-gray-600">
                  Real humans, real help. Our support team is available whenever you need us.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="py-20 md:py-28 bg-primary-600 text-white">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-4xl font-bold mb-6">
                Ready to Transform Your Marketing?
              </h2>
              <p className="text-xl text-primary-100 mb-8">
                Join 500+ small businesses already using AI to compete with the big players.
                Setup takes 15 minutes, ROI comes in 7 days.
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

export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn about Bizoholic Digital - the AI-powered marketing platform transforming small business marketing with 93+ autonomous agents, 75% cost savings, and proven ROI.',
  openGraph: {
    title: 'About Bizoholic Digital - AI Marketing Automation',
    description: 'Enterprise-level marketing automation made accessible for small businesses. 500+ clients, 4.8x average ROI, 93+ AI agents working 24/7.',
  },
}
