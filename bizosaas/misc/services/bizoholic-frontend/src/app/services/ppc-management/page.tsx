import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import Link from 'next/link'
import { Target, TrendingUp, DollarSign, BarChart3, CheckCircle, ArrowRight, Award, Quote, Zap, MousePointer } from 'lucide-react'

export const metadata: Metadata = {
  title: 'PPC Management & Paid Advertising | Bizoholic',
  description: 'Maximize your ad spend ROI with AI-powered PPC management. Expert Google Ads, Facebook Ads, LinkedIn Ads management that delivers results.',
}

export default function PPCManagementPage() {
  const features = [
    {
      icon: <Target className="w-6 h-6" />,
      title: 'Google Ads Management',
      description: 'Search, Display, Shopping, and YouTube campaigns optimized for maximum ROI'
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: 'Social Media Ads',
      description: 'Facebook, Instagram, LinkedIn, and Twitter campaigns that convert'
    },
    {
      icon: <DollarSign className="w-6 h-6" />,
      title: 'Budget Optimization',
      description: 'AI-powered bid management and budget allocation across all platforms'
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: 'Performance Tracking',
      description: 'Real-time analytics, conversion tracking, and comprehensive reporting'
    }
  ]

  const benefits = [
    'Reduce cost per acquisition by 40-60%',
    'Increase conversion rates by 2-3x',
    'Improve Quality Score and ad relevance',
    'Scale profitable campaigns automatically',
    '24/7 AI-powered bid optimization',
    'Comprehensive cross-platform reporting'
  ]

  const process = [
    {
      step: 1,
      title: 'PPC Audit & Analysis',
      description: 'Comprehensive audit of existing campaigns and competitive landscape analysis'
    },
    {
      step: 2,
      title: 'Strategy Development',
      description: 'Custom campaign strategy based on your goals, audience, and budget'
    },
    {
      step: 3,
      title: 'Campaign Launch',
      description: 'Setup and launch of optimized campaigns with conversion tracking'
    },
    {
      step: 4,
      title: 'Optimize & Scale',
      description: 'Continuous testing, optimization, and scaling of winning campaigns'
    }
  ]

  const pricing = [
    {
      name: 'Starter PPC',
      price: '$599',
      period: '/month',
      description: 'For small businesses',
      features: [
        'Google Ads or Facebook Ads (single platform)',
        'Up to $3,000 monthly ad spend',
        '2 campaign types',
        'Basic conversion tracking',
        'Monthly performance reports',
        'Email support'
      ],
      popular: false
    },
    {
      name: 'Growth PPC',
      price: '$1,299',
      period: '/month',
      description: 'For growing businesses',
      features: [
        'Multi-platform campaigns (Google + Social)',
        'Up to $10,000 monthly ad spend',
        'Advanced campaign types',
        'Full conversion tracking & analytics',
        'Bi-weekly optimization reports',
        'Dedicated account manager',
        'A/B testing & landing page optimization'
      ],
      popular: true
    },
    {
      name: 'Enterprise PPC',
      price: '$2,999',
      period: '/month',
      description: 'For established brands',
      features: [
        'All-platform campaign management',
        'Unlimited monthly ad spend',
        'Advanced remarketing strategies',
        'Custom conversion funnels',
        'Weekly strategy calls',
        'Dedicated PPC team',
        'Custom reporting dashboard',
        'Competitor intelligence'
      ],
      popular: false
    }
  ]

  const caseStudies = [
    {
      industry: 'SaaS Company',
      challenge: 'High cost per lead, poor campaign performance, wasted ad spend',
      solution: 'Complete account restructure, audience targeting refinement, AI bid optimization',
      results: [
        '58% reduction in cost per acquisition',
        '240% increase in qualified leads',
        'Quality Score improved from 4/10 to 8/10',
        'ROI increased from 150% to 420%'
      ]
    },
    {
      industry: 'E-commerce Retailer',
      challenge: 'Low ROAS, inefficient shopping campaigns, poor product feed',
      solution: 'Shopping campaign optimization, product feed restructure, smart bidding',
      results: [
        '385% increase in ROAS',
        'Cost per sale reduced by 52%',
        'Shopping campaign revenue up 310%',
        'Average order value increased 28%'
      ]
    }
  ]

  const testimonials = [
    {
      name: 'David Martinez',
      company: 'CloudFlow SaaS',
      role: 'VP of Marketing',
      quote: 'We were burning through our ad budget with little to show for it. Bizoholic completely transformed our PPC strategy. Our cost per lead dropped 58% while lead quality actually improved. Best investment we have made.',
      rating: 5
    },
    {
      name: 'Jennifer Lee',
      company: 'Urban Threads',
      role: 'E-commerce Director',
      quote: 'Our shopping campaigns were a mess before Bizoholic. Now they are our biggest revenue driver. ROAS went from 2.5x to 12x in just 3 months. The team really knows Google Ads inside and out.',
      rating: 5
    }
  ]

  const faqs = [
    {
      question: 'How much should I budget for PPC advertising?',
      answer: 'We recommend starting with at least $1,500-$3,000/month in ad spend for meaningful results. The management fee is separate. Your budget depends on your industry, competition, and goals. We will help determine the optimal budget during our initial consultation.'
    },
    {
      question: 'What platforms do you manage?',
      answer: 'We manage all major PPC platforms including Google Ads (Search, Display, Shopping, YouTube), Facebook/Instagram Ads, LinkedIn Ads, Twitter Ads, Pinterest Ads, and TikTok Ads. We recommend the best platforms based on your audience and goals.'
    },
    {
      question: 'How quickly will I see results?',
      answer: 'Initial results typically appear within 2-4 weeks as campaigns gather data. Significant optimization and improvement happens at 60-90 days once we have enough data to make informed decisions. PPC is faster than SEO but still requires optimization time.'
    },
    {
      question: 'Do you guarantee a specific ROAS?',
      answer: 'While we cannot guarantee specific results (they depend on many factors), we do guarantee continuous improvement and transparent reporting. Our average client sees 3-5x ROAS, with many achieving 8-12x once campaigns are fully optimized.'
    },
    {
      question: 'What makes your PPC management different?',
      answer: 'We combine AI-powered optimization with human strategic oversight. Our proprietary bidding algorithms continuously optimize in real-time, while our expert strategists ensure campaign alignment with your business goals. Plus, you get complete transparency with detailed reporting.'
    },
    {
      question: 'Can I cancel anytime?',
      answer: 'Yes, all plans are month-to-month with no long-term contracts. However, we recommend at least 90 days to see optimal results from testing and optimization. Account ownership always remains with you - we never hold your campaigns hostage.'
    },
    {
      question: 'What is included in the free PPC audit?',
      answer: 'Our comprehensive audit includes account structure analysis, campaign performance review, keyword analysis, ad copy assessment, landing page evaluation, conversion tracking audit, competitive analysis, and a detailed action plan with projected improvements.'
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
              { label: 'PPC Management' }
            ]} />
          </div>
        </section>

        {/* Hero Section */}
        <section className="bg-gray-50 py-20">
          <div className="container">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl font-bold text-gray-900 mb-6">
                PPC Management & Paid Advertising
              </h1>
              <p className="text-xl text-gray-700 mb-8">
                Maximize ROI with AI-optimized paid advertising campaigns across Google, Facebook, LinkedIn, and more
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/contact" className="btn-primary px-8 py-4 text-lg">
                  Get Free PPC Audit
                </Link>
                <Link href="/pricing" className="btn-secondary px-8 py-4 text-lg">
                  View Pricing
                </Link>
              </div>
              <p className="text-sm text-gray-600 mt-6">
                No credit card required • Free account audit • See improvement opportunities
              </p>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Comprehensive PPC Management
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Full-service paid advertising management across all major platforms
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <div key={index} className="card-feature">
                  <div className="icon-container mb-4">
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
                What You Will Achieve
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="feature-item">
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
                Our PPC Process
              </h2>
              <p className="text-xl text-gray-600">
                A proven 4-step approach to PPC success
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {process.map((item, index) => (
                <div key={index} className="relative">
                  <div className="step-card">
                    <div className="step-indicator mb-4">
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
                PPC Management Pricing
              </h2>
              <p className="text-xl text-gray-600">
                Transparent pricing based on your advertising needs
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {pricing.map((plan, index) => (
                <div key={index} className={plan.popular ? 'pricing-card-popular' : 'pricing-card'}>
                  {plan.popular && (
                    <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                      <span className="badge-popular">
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
                    <p className="text-sm text-gray-500 mt-2">+ ad spend budget</p>
                  </div>
                  <ul className="feature-list mb-8">
                    {plan.features.map((feature, idx) => (
                      <li key={idx} className="feature-item">
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
                Real Results from Real Campaigns
              </h2>
              <p className="text-xl text-gray-600">
                See how we have helped businesses maximize their PPC ROI
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
                Real feedback from real businesses
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
                Everything you need to know about PPC management
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
                Ready to Scale Your Paid Advertising?
              </h2>
              <p className="text-xl mb-8 text-white/90">
                Get a free PPC audit and discover optimization opportunities
              </p>
              <Link
                href="/contact"
                className="inline-block bg-white text-primary-600 font-semibold px-8 py-4 rounded-lg hover:bg-gray-100 transition-colors"
              >
                Get Free PPC Audit
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
