import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import Link from 'next/link'
import { Search, Target, Share2, FileText, Mail, Code, TrendingUp, BarChart3, CheckCircle, ArrowRight, Award, Zap } from 'lucide-react'

export const metadata: Metadata = {
  title: 'Digital Marketing Services | Bizoholic',
  description: 'Comprehensive AI-powered digital marketing services for small businesses. SEO, PPC, social media, content marketing, and more.',
}

export default function ServicesPage() {
  const services = [
    {
      icon: <Search className="w-8 h-8" />,
      title: 'SEO Optimization',
      slug: 'seo-optimization',
      description: 'Dominate search results with AI-powered SEO strategies that drive organic traffic, leads, and revenue.',
      price: 'From $299/mo',
      features: ['Keyword research', 'Technical SEO', 'Local SEO', 'Content optimization'],
      badge: 'Most Popular'
    },
    {
      icon: <Target className="w-8 h-8" />,
      title: 'PPC Management',
      slug: 'ppc-management',
      description: 'Maximize ROI with expert Google Ads, Facebook Ads, and LinkedIn Ads management.',
      price: 'From $599/mo',
      features: ['Google Ads', 'Social media ads', 'Budget optimization', 'A/B testing'],
      badge: 'High ROI'
    },
    {
      icon: <Share2 className="w-8 h-8" />,
      title: 'Social Media Management',
      slug: 'social-media',
      description: 'Build engaged communities across Facebook, Instagram, LinkedIn, and Twitter.',
      price: 'From $399/mo',
      features: ['Content creation', 'Community management', 'Social advertising', 'Analytics'],
      badge: null
    },
    {
      icon: <FileText className="w-8 h-8" />,
      title: 'Content Marketing',
      slug: 'content-creation',
      description: 'Create compelling content that engages your audience and drives conversions.',
      price: 'From $499/mo',
      features: ['Blog posts', 'Landing pages', 'Email copy', 'Video scripts'],
      badge: null
    },
    {
      icon: <Mail className="w-8 h-8" />,
      title: 'Email Marketing',
      slug: 'email-marketing',
      description: 'Nurture leads and drive sales with AI-optimized email campaigns and automation.',
      price: 'From $299/mo',
      features: ['Email campaigns', 'Marketing automation', 'List segmentation', 'A/B testing'],
      badge: null
    },
    {
      icon: <Code className="w-8 h-8" />,
      title: 'Web Development',
      slug: 'web-development',
      description: 'Build fast, beautiful, conversion-focused websites that drive business results.',
      price: 'From $2,999',
      features: ['Custom design', 'Mobile responsive', 'SEO optimized', 'Fast loading'],
      badge: null
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: 'Conversion Optimization',
      slug: 'conversion-optimization',
      description: 'Increase revenue without more traffic through data-driven CRO strategies.',
      price: 'From $799/mo',
      features: ['A/B testing', 'Landing page optimization', 'Funnel analysis', 'UX improvements'],
      badge: null
    },
    {
      icon: <BarChart3 className="w-8 h-8" />,
      title: 'Analytics & Reporting',
      slug: 'analytics',
      description: 'Make data-driven decisions with comprehensive analytics and insights.',
      price: 'From $399/mo',
      features: ['Custom dashboards', 'Performance tracking', 'ROI analysis', 'Predictive analytics'],
      badge: null
    }
  ]

  const benefits = [
    'AI-Powered Strategies',
    'Transparent Pricing',
    'Dedicated Account Manager',
    'Monthly Reporting',
    'No Long-Term Contracts',
    'Results Guarantee'
  ]

  const industries = [
    'Legal & Professional Services',
    'Healthcare & Medical',
    'E-commerce & Retail',
    'Home Services',
    'B2B SaaS',
    'Real Estate',
    'Restaurants & Hospitality',
    'Financial Services'
  ]

  const faqs = [
    {
      question: 'Which services do I need for my business?',
      answer: 'It depends on your goals and current marketing efforts. Most businesses start with SEO and PPC for immediate traffic, then add content marketing and social media. We offer a free consultation to assess your needs and recommend the right mix of services.'
    },
    {
      question: 'Can I bundle multiple services?',
      answer: 'Yes! We offer bundled packages that combine multiple services at a discounted rate. For example, our Growth Package includes SEO, PPC, and content marketing for 20% less than purchasing separately.'
    },
    {
      question: 'How do you measure success?',
      answer: 'We track metrics that matter to your business: traffic, leads, conversions, and revenue. Every client gets a custom dashboard showing real-time performance. We focus on ROI, not vanity metrics.'
    },
    {
      question: 'What makes Bizoholic different?',
      answer: 'We combine AI-powered automation with human expertise. Our proprietary tools optimize campaigns 24/7 while our strategists ensure alignment with your business goals. Plus, we are transparent, affordable, and results-focused.'
    },
    {
      question: 'Do you work with my industry?',
      answer: 'Yes! We have experience across 50+ industries. Every strategy is customized for your specific market, competition, and audience. We will never use cookie-cutter approaches.'
    },
    {
      question: 'What is your pricing model?',
      answer: 'We offer transparent monthly pricing with no long-term contracts. Most services are month-to-month, so you can cancel anytime. We also offer performance-based pricing for qualified clients.'
    }
  ]

  return (
    <>
      <Navigation />
      <main className="min-h-screen bg-white">
        {/* Breadcrumb */}
        <section className="pt-8">
          <div className="container">
            <Breadcrumb items={[
              { label: 'Services' }
            ]} />
          </div>
        </section>

        {/* Hero Section */}
        <section className="bg-gray-50 py-20">
          <div className="container">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
                Comprehensive Digital Marketing Services
              </h1>
              <p className="text-xl text-gray-700 mb-8">
                AI-powered marketing automation designed for small businesses who want to dominate their market
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/contact" className="btn-primary px-8 py-4 text-lg">
                  Get Free Consultation
                </Link>
                <Link href="/pricing" className="btn-secondary px-8 py-4 text-lg">
                  View Pricing
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Services Grid */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Everything You Need to Grow
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                From SEO to PPC to social media, we offer a complete suite of digital marketing services
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {services.map((service, index) => (
                <Link key={index} href={`/services/${service.slug}`} className="group">
                  <div className="card-feature relative h-full">
                    {service.badge && (
                      <div className="absolute -top-3 -right-3">
                        <span className="badge-popular text-xs px-3 py-1">
                          {service.badge}
                        </span>
                      </div>
                    )}

                    <div className="icon-container mb-4 text-primary-600">
                      {service.icon}
                    </div>

                    <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors">
                      {service.title}
                    </h3>

                    <p className="text-gray-600 mb-4 text-sm leading-relaxed">
                      {service.description}
                    </p>

                    <div className="mb-4">
                      <p className="text-primary-600 font-bold">{service.price}</p>
                    </div>

                    <ul className="space-y-2 mb-4">
                      {service.features.map((feature, idx) => (
                        <li key={idx} className="flex items-start text-sm">
                          <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-600">{feature}</span>
                        </li>
                      ))}
                    </ul>

                    <div className="flex items-center text-primary-600 font-medium mt-auto">
                      Learn more
                      <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* Why Choose Us Section */}
        <section className="py-20 bg-gray-50">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Why Choose Bizoholic?
              </h2>
              <p className="text-xl text-gray-600">
                What sets us apart from other digital marketing agencies
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {benefits.map((benefit, index) => (
                <div key={index} className="flex items-center">
                  <Award className="w-6 h-6 text-primary-600 mr-3 flex-shrink-0" />
                  <span className="text-lg font-medium text-gray-900">{benefit}</span>
                </div>
              ))}
            </div>

            <div className="mt-16 max-w-4xl mx-auto">
              <div className="bg-white rounded-2xl p-8 shadow-lg">
                <div className="grid md:grid-cols-3 gap-8 text-center">
                  <div className="stat-card">
                    <div className="stat-value">93+</div>
                    <div className="stat-label">AI Agents Working 24/7</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">500+</div>
                    <div className="stat-label">Happy Clients</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">4.8x</div>
                    <div className="stat-label">Average ROI</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Industries Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Industries We Serve
              </h2>
              <p className="text-xl text-gray-600">
                Proven strategies across 50+ industries
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 max-w-6xl mx-auto">
              {industries.map((industry, index) => (
                <div key={index} className="bg-white border border-gray-200 rounded-lg p-4 text-center hover:border-primary-500 hover:shadow-md transition-all">
                  <p className="font-medium text-gray-900">{industry}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Service Comparison */}
        <section className="py-20 bg-gray-50">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Compare Our Services
              </h2>
              <p className="text-xl text-gray-600">
                Find the right service for your business goals
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full bg-white rounded-xl shadow-lg overflow-hidden">
                <thead className="bg-primary-600 text-white">
                  <tr>
                    <th className="px-6 py-4 text-left">Service</th>
                    <th className="px-6 py-4 text-left">Best For</th>
                    <th className="px-6 py-4 text-left">Timeline</th>
                    <th className="px-6 py-4 text-left">Starting Price</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr className="hover:bg-gray-50">
                    <td className="px-6 py-4 font-semibold">SEO Optimization</td>
                    <td className="px-6 py-4">Long-term traffic growth</td>
                    <td className="px-6 py-4">3-6 months</td>
                    <td className="px-6 py-4">$299/mo</td>
                  </tr>
                  <tr className="hover:bg-gray-50">
                    <td className="px-6 py-4 font-semibold">PPC Management</td>
                    <td className="px-6 py-4">Immediate traffic & leads</td>
                    <td className="px-6 py-4">2-4 weeks</td>
                    <td className="px-6 py-4">$599/mo</td>
                  </tr>
                  <tr className="hover:bg-gray-50">
                    <td className="px-6 py-4 font-semibold">Social Media</td>
                    <td className="px-6 py-4">Brand awareness & engagement</td>
                    <td className="px-6 py-4">1-3 months</td>
                    <td className="px-6 py-4">$399/mo</td>
                  </tr>
                  <tr className="hover:bg-gray-50">
                    <td className="px-6 py-4 font-semibold">Content Marketing</td>
                    <td className="px-6 py-4">Authority & lead nurturing</td>
                    <td className="px-6 py-4">2-4 months</td>
                    <td className="px-6 py-4">$499/mo</td>
                  </tr>
                  <tr className="hover:bg-gray-50">
                    <td className="px-6 py-4 font-semibold">Email Marketing</td>
                    <td className="px-6 py-4">Customer retention & sales</td>
                    <td className="px-6 py-4">1-2 months</td>
                    <td className="px-6 py-4">$299/mo</td>
                  </tr>
                  <tr className="hover:bg-gray-50">
                    <td className="px-6 py-4 font-semibold">Web Development</td>
                    <td className="px-6 py-4">New website or redesign</td>
                    <td className="px-6 py-4">4-8 weeks</td>
                    <td className="px-6 py-4">$2,999</td>
                  </tr>
                  <tr className="hover:bg-gray-50">
                    <td className="px-6 py-4 font-semibold">Conversion Optimization</td>
                    <td className="px-6 py-4">Improve existing traffic</td>
                    <td className="px-6 py-4">1-2 months</td>
                    <td className="px-6 py-4">$799/mo</td>
                  </tr>
                  <tr className="hover:bg-gray-50">
                    <td className="px-6 py-4 font-semibold">Analytics & Reporting</td>
                    <td className="px-6 py-4">Data-driven decisions</td>
                    <td className="px-6 py-4">Immediate</td>
                    <td className="px-6 py-4">$399/mo</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Frequently Asked Questions
              </h2>
              <p className="text-xl text-gray-600">
                Common questions about our services
              </p>
            </div>

            <div className="max-w-4xl mx-auto space-y-6">
              {faqs.map((faq, index) => (
                <div key={index} className="bg-white rounded-xl p-6 shadow-md border border-gray-200">
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">
                    {faq.question}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {faq.answer}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-gray-50">
          <div className="container">
            <div className="cta-section">
              <h2 className="text-4xl font-bold mb-4">
                Ready to Grow Your Business?
              </h2>
              <p className="text-xl mb-8 text-white/90">
                Get a free consultation and discover which services are right for you
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  href="/contact"
                  className="inline-block bg-white text-primary-600 font-semibold px-8 py-4 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  Get Free Consultation
                </Link>
                <Link
                  href="/pricing"
                  className="inline-block bg-transparent border-2 border-white text-white font-semibold px-8 py-4 rounded-lg hover:bg-white hover:text-primary-600 transition-colors"
                >
                  View All Pricing
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
