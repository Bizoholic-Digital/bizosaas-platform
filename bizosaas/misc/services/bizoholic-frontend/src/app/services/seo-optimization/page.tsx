import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import Link from 'next/link'
import { Search, TrendingUp, Target, Zap, CheckCircle, ArrowRight, Award, Quote } from 'lucide-react'

export const metadata: Metadata = {
  title: 'SEO Optimization & Local SEO Services | Bizoholic',
  description: 'Boost your search rankings with AI-powered SEO optimization. Get more organic traffic, leads, and revenue with data-driven strategies.',
}

export default function SEOOptimizationPage() {
  const features = [
    {
      icon: <Search className="w-6 h-6" />,
      title: 'Keyword Research & Strategy',
      description: 'AI-powered keyword analysis to identify high-value opportunities and search intent'
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: 'Technical SEO Optimization',
      description: 'Site speed, mobile optimization, schema markup, and crawlability improvements'
    },
    {
      icon: <Target className="w-6 h-6" />,
      title: 'Local SEO & Google Business',
      description: 'Dominate local search with optimized GMB profiles and local citations'
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: 'Content Optimization',
      description: 'AI-optimized content that ranks while engaging your target audience'
    }
  ]

  const benefits = [
    'Increase organic traffic by 200-500%',
    'Rank on page 1 for target keywords within 90 days',
    'Improve domain authority and backlink profile',
    'Higher conversion rates from targeted traffic',
    '24/7 AI monitoring and optimization',
    'Comprehensive monthly reporting and insights'
  ]

  const process = [
    {
      step: 1,
      title: 'SEO Audit & Analysis',
      description: 'Comprehensive site audit identifying opportunities and technical issues'
    },
    {
      step: 2,
      title: 'Strategy Development',
      description: 'Custom SEO roadmap based on your goals, industry, and competition'
    },
    {
      step: 3,
      title: 'Implementation',
      description: 'Technical optimizations, content creation, and link building execution'
    },
    {
      step: 4,
      title: 'Monitor & Optimize',
      description: 'Continuous AI-powered optimization and performance tracking'
    }
  ]

  const pricing = [
    {
      name: 'Local SEO',
      price: '$299',
      period: '/month',
      description: 'Perfect for local businesses',
      features: [
        'Google Business Profile optimization',
        'Local keyword targeting (up to 20)',
        'Local citations and directory listings',
        'Monthly local ranking reports',
        'Review management support'
      ],
      popular: false
    },
    {
      name: 'Growth SEO',
      price: '$599',
      period: '/month',
      description: 'For growing businesses',
      features: [
        'Everything in Local SEO',
        'National keyword targeting (up to 50)',
        'Content optimization (4 pages/month)',
        'Technical SEO fixes',
        'Backlink building (5 quality links/month)',
        'Competitor analysis'
      ],
      popular: true
    },
    {
      name: 'Enterprise SEO',
      price: '$1,299',
      period: '/month',
      description: 'For established brands',
      features: [
        'Everything in Growth SEO',
        'Unlimited keyword targeting',
        'Content creation (8 articles/month)',
        'Advanced technical SEO',
        'Premium backlink building (15+ links/month)',
        'Dedicated SEO strategist',
        'Custom reporting dashboard'
      ],
      popular: false
    }
  ]

  const caseStudies = [
    {
      industry: 'Local Law Firm',
      challenge: 'Zero online visibility, relying 100% on referrals',
      solution: 'Local SEO package with Google Business optimization and content strategy',
      results: [
        '450% increase in organic traffic in 6 months',
        'Ranking #1 for 15 target keywords',
        '12 new cases per month from organic search',
        'ROI of 800% on SEO investment'
      ]
    },
    {
      industry: 'E-commerce Store',
      challenge: 'High bounce rate, poor product page rankings',
      solution: 'Technical SEO overhaul, product page optimization, backlink building',
      results: [
        '320% increase in organic revenue',
        'Reduced bounce rate from 68% to 32%',
        'Page 1 rankings for 200+ product keywords',
        'Average order value increased 45%'
      ]
    }
  ]

  const testimonials = [
    {
      name: 'Sarah Johnson',
      company: 'Johnson & Associates Law Firm',
      role: 'Managing Partner',
      quote: 'Before Bizoholic, we had zero online presence. Now we rank #1 for all our target keywords and get 12+ qualified leads every month from Google. The ROI has been incredible.',
      rating: 5
    },
    {
      name: 'Mike Chen',
      company: 'Urban Boutique',
      role: 'Owner',
      quote: 'Our organic traffic tripled in just 4 months. The team really knows their stuff - they found technical issues we had no idea existed and fixed them all. Sales are up 200%.',
      rating: 5
    }
  ]

  const faqs = [
    {
      question: 'How long does it take to see SEO results?',
      answer: 'Most clients start seeing improvements in rankings and traffic within 30-60 days. Significant results typically appear within 90 days. SEO is a long-term strategy, with compounding benefits over 6-12 months.'
    },
    {
      question: 'Do you guarantee first page rankings?',
      answer: 'While we cannot guarantee specific rankings (no ethical SEO company can), we do guarantee measurable improvements in traffic, rankings, and conversions. Our track record shows 95% of clients achieve page 1 rankings for their target keywords within 6 months.'
    },
    {
      question: 'What makes your SEO different from competitors?',
      answer: 'We combine AI-powered analysis with human expertise. Our proprietary algorithms identify opportunities competitors miss, while our experienced strategists ensure quality and authenticity. Plus, we focus on ROI, not just rankings.'
    },
    {
      question: 'Can I cancel anytime?',
      answer: 'Yes, all our plans are month-to-month with no long-term contracts. However, we recommend at least 6 months to see the full benefits of SEO. Most clients stay with us for years because of the consistent results.'
    },
    {
      question: 'Do you work with my industry?',
      answer: 'Yes! We have successfully helped businesses across 50+ industries including legal, healthcare, e-commerce, professional services, home services, and more. Every strategy is customized for your specific industry and competition.'
    },
    {
      question: 'What is included in the free SEO audit?',
      answer: 'Our comprehensive audit includes technical SEO analysis, on-page optimization review, backlink profile assessment, competitor analysis, keyword gap analysis, and a detailed action plan. You will receive a 20+ page report with specific recommendations.'
    },
    {
      question: 'Do you do the work or just provide recommendations?',
      answer: 'We do everything. Our team implements all technical fixes, creates and optimizes content, builds backlinks, monitors performance, and provides monthly reports. You get a fully managed SEO service.'
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
              { label: 'Services', href: '/services' },
              { label: 'SEO Optimization' }
            ]} />
          </div>
        </section>

        {/* Hero Section */}
        <section className="bg-gray-50 py-20">
          <div className="container">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl font-bold text-gray-900 mb-6">
                SEO Optimization & Local SEO
              </h1>
              <p className="text-xl text-gray-700 mb-8">
                Dominate search results with AI-powered SEO strategies that drive organic traffic, leads, and revenue for your business
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/contact" className="btn-primary px-8 py-4 text-lg">
                  Get Free SEO Audit
                </Link>
                <Link href="/pricing" className="btn-secondary px-8 py-4 text-lg">
                  View Pricing
                </Link>
              </div>
              <p className="text-sm text-gray-600 mt-6">
                No credit card required • 14-day free trial • ROI within 7 days
              </p>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Comprehensive SEO Services
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Everything you need to rank higher and attract qualified organic traffic
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <div key={index} className="bg-white p-6 rounded-xl border border-gray-200 hover:border-primary-500 hover:shadow-lg transition-all">
                  <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center text-primary-600 mb-4">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="py-20 bg-gray-50">
          <div className="container">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-4xl font-bold text-gray-900 mb-12 text-center">
                What You&apos;ll Achieve
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0 mt-1" />
                    <span className="text-lg text-gray-700">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Process Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Our SEO Process
              </h2>
              <p className="text-xl text-gray-600">
                A proven 4-step approach to SEO success
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {process.map((item, index) => (
                <div key={index} className="relative">
                  <div className="bg-white p-6 rounded-xl border-2 border-primary-200 hover:border-primary-500 transition-all">
                    <div className="w-12 h-12 bg-primary-600 rounded-full flex items-center justify-center text-white text-xl font-bold mb-4">
                      {item.step}
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {item.title}
                    </h3>
                    <p className="text-gray-600">
                      {item.description}
                    </p>
                  </div>
                  {index < process.length - 1 && (
                    <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                      <ArrowRight className="w-8 h-8 text-primary-300" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Pricing Section */}
        <section className="py-20 bg-gray-50">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                SEO Pricing Plans
              </h2>
              <p className="text-xl text-gray-600">
                Choose the plan that fits your business goals
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {pricing.map((plan, index) => (
                <div key={index} className={`bg-white rounded-2xl shadow-lg p-8 relative ${plan.popular ? 'border-2 border-primary-500 transform scale-105' : 'border border-gray-200'}`}>
                  {plan.popular && (
                    <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                      <span className="bg-primary-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                        Most Popular
                      </span>
                    </div>
                  )}
                  <div className="text-center mb-6">
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">
                      {plan.name}
                    </h3>
                    <p className="text-gray-600 mb-4">{plan.description}</p>
                    <div className="flex items-baseline justify-center">
                      <span className="text-5xl font-bold text-gray-900">{plan.price}</span>
                      <span className="text-gray-600 ml-2">{plan.period}</span>
                    </div>
                  </div>
                  <ul className="space-y-3 mb-8">
                    {plan.features.map((feature, idx) => (
                      <li key={idx} className="flex items-start space-x-3">
                        <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                        <span className="text-gray-700">{feature}</span>
                      </li>
                    ))}
                  </ul>
                  <Link
                    href="/contact"
                    className={`block w-full text-center py-3 px-6 rounded-lg font-semibold transition-colors ${plan.popular ? 'bg-primary-600 hover:bg-primary-700 text-white' : 'bg-gray-100 hover:bg-gray-200 text-gray-900'}`}
                  >
                    Get Started
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Case Studies Section */}
        <section className="py-20 bg-white">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Real Results from Real Clients
              </h2>
              <p className="text-xl text-gray-600">
                See how we have helped businesses like yours dominate search rankings
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
              {caseStudies.map((study, index) => (
                <div key={index} className="card">
                  <div className="flex items-center mb-4">
                    <Award className="w-8 h-8 text-primary-600 mr-3" />
                    <h3 className="text-2xl font-bold text-gray-900">{study.industry}</h3>
                  </div>

                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-900 mb-2">The Challenge:</h4>
                    <p className="text-gray-600">{study.challenge}</p>
                  </div>

                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-900 mb-2">Our Solution:</h4>
                    <p className="text-gray-600">{study.solution}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">The Results:</h4>
                    <ul className="space-y-2">
                      {study.results.map((result, idx) => (
                        <li key={idx} className="flex items-start">
                          <CheckCircle className="w-5 h-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-700">{result}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Testimonials Section */}
        <section className="py-20 bg-gray-50">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                What Our Clients Say
              </h2>
              <p className="text-xl text-gray-600">
                Do not just take our word for it
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
              {testimonials.map((testimonial, index) => (
                <div key={index} className="bg-white rounded-2xl p-8 shadow-lg relative">
                  <Quote className="w-12 h-12 text-primary-200 absolute top-6 right-6" />
                  <div className="flex mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <svg key={i} className="w-5 h-5 text-yellow-400 fill-current" viewBox="0 0 20 20">
                        <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                      </svg>
                    ))}
                  </div>
                  <p className="text-gray-700 text-lg mb-6 italic">&quot;{testimonial.quote}&quot;</p>
                  <div>
                    <p className="font-semibold text-gray-900">{testimonial.name}</p>
                    <p className="text-gray-600">{testimonial.role}, {testimonial.company}</p>
                  </div>
                </div>
              ))}
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
                Everything you need to know about our SEO services
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
                Ready to Dominate Search Results?
              </h2>
              <p className="text-xl mb-8 text-white/90">
                Get a free SEO audit and discover how we can boost your rankings
              </p>
              <Link
                href="/contact"
                className="inline-block bg-white text-primary-600 font-semibold px-8 py-4 rounded-lg hover:bg-gray-100 transition-colors"
              >
                Get Free SEO Audit
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
