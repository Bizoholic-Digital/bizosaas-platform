import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import Link from 'next/link'
import { Mail, Send, Users, TrendingUp, CheckCircle, ArrowRight, Award, Quote } from 'lucide-react'

export const metadata: Metadata = {
  title: 'Email Marketing Automation Services | Bizoholic',
  description: 'Drive revenue and retention with AI-powered email marketing automation. Personalized campaigns, behavioral triggers, and advanced segmentation.',
}

export default function EmailMarketingPage() {
  const features = [
    {
      icon: <Mail className="w-6 h-6" />,
      title: 'AI-Powered Subject Line Optimization',
      description: 'Maximize open rates with AI-tested subject lines and preview text'
    },
    {
      icon: <Send className="w-6 h-6" />,
      title: 'Behavioral Trigger Automation',
      description: 'Send the right message at the right time based on user actions and behavior'
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: 'Advanced Segmentation',
      description: 'Target specific audiences with personalized messaging based on demographics and behavior'
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: 'A/B Testing & Optimization',
      description: 'Continuously improve performance with systematic testing and data-driven insights'
    }
  ]

  const benefits = [
    'Increase email open rates by 40-60%',
    'Improve click-through rates by 50-100%',
    'Generate consistent revenue from automated sequences',
    'Retain customers with personalized nurture campaigns',
    'Reduce cart abandonment by 30-50%',
    'Build deeper relationships with your audience'
  ]

  const process = [
    {
      step: 1,
      title: 'List Audit & Strategy',
      description: 'Analyze email list health, segmentation opportunities, and campaign goals'
    },
    {
      step: 2,
      title: 'Automation Setup',
      description: 'Build automated workflows for welcome, nurture, abandoned cart, and re-engagement'
    },
    {
      step: 3,
      title: 'Campaign Creation',
      description: 'Design beautiful emails with compelling copy optimized for conversions'
    },
    {
      step: 4,
      title: 'Test & Optimize',
      description: 'Continuously test subject lines, content, and timing to maximize performance'
    }
  ]

  const pricing = [
    {
      name: 'Starter Email',
      price: '$299',
      period: '/month',
      description: 'Perfect for small lists',
      features: [
        'Up to 5,000 contacts',
        '4 email campaigns per month',
        'Basic automation (welcome series)',
        'Email template design',
        'Monthly performance report',
        'List management support'
      ],
      popular: false
    },
    {
      name: 'Growth Email',
      price: '$599',
      period: '/month',
      description: 'For growing businesses',
      features: [
        'Everything in Starter Email',
        'Up to 25,000 contacts',
        'Unlimited email campaigns',
        'Advanced automation (cart abandonment, nurture)',
        'A/B testing and optimization',
        'Advanced segmentation',
        'Bi-weekly strategy calls'
      ],
      popular: true
    },
    {
      name: 'Enterprise Email',
      price: '$1,299',
      period: '/month',
      description: 'For established brands',
      features: [
        'Everything in Growth Email',
        'Unlimited contacts',
        'Advanced behavioral triggers',
        'Predictive send time optimization',
        'Custom integrations (CRM, e-commerce)',
        'Dedicated email strategist',
        'Priority support',
        'Custom reporting dashboard'
      ],
      popular: false
    }
  ]

  const caseStudies = [
    {
      industry: 'E-commerce Store',
      challenge: 'Low open rates, minimal repeat purchases, high cart abandonment',
      solution: 'Comprehensive email automation with cart abandonment, product recommendations, and win-back campaigns',
      results: [
        '42% average open rate (2x industry average)',
        '8.5% click-through rate (3x industry average)',
        '$125,000 in recovered cart revenue in 6 months',
        '35% increase in repeat customer rate'
      ]
    },
    {
      industry: 'SaaS Company',
      challenge: 'Difficulty converting free trials, low engagement, high churn',
      solution: 'Automated drip campaign with educational content, feature highlights, and behavioral triggers',
      results: [
        '$85,000 in revenue from automated campaigns',
        '45% increase in trial-to-paid conversion',
        '25% reduction in customer churn',
        '55% open rate on onboarding sequence'
      ]
    }
  ]

  const testimonials = [
    {
      name: 'Jennifer Martinez',
      company: 'Urban Style Boutique',
      role: 'Owner',
      quote: 'Our email marketing was non-existent before Bizoholic. Now we have automated sequences that run 24/7, recovering thousands in abandoned carts and driving repeat purchases. Email is now our #1 revenue channel.',
      rating: 5
    },
    {
      name: 'Alex Thompson',
      company: 'ProjectFlow SaaS',
      role: 'Head of Growth',
      quote: 'The automated onboarding sequence they built has transformed our trial conversion rate. We went from 12% to 28% conversion in just 3 months. The ROI on email marketing has been phenomenal.',
      rating: 5
    }
  ]

  const faqs = [
    {
      question: 'What email platform do you work with?',
      answer: 'We work with all major email platforms including Mailchimp, Klaviyo, HubSpot, ActiveCampaign, ConvertKit, Brevo (Sendinblue), and custom SMTP solutions. We can also help you choose the right platform based on your needs and budget.'
    },
    {
      question: 'Do you provide the email lists or do we need our own?',
      answer: 'You need to have your own email list. We never provide purchased lists as they violate anti-spam laws and damage deliverability. We can help you grow your list organically through opt-in forms, lead magnets, and ethical list-building strategies.'
    },
    {
      question: 'How do you ensure emails do not go to spam?',
      answer: 'We follow email deliverability best practices including proper authentication (SPF, DKIM, DMARC), maintaining good sender reputation, following anti-spam laws, using clean lists, avoiding spam trigger words, and monitoring blacklists. Our clients consistently achieve 95%+ inbox placement rates.'
    },
    {
      question: 'What types of email campaigns do you create?',
      answer: 'We create all types of campaigns including welcome series, newsletter campaigns, promotional emails, abandoned cart recovery, product recommendations, win-back campaigns, event invitations, educational drip sequences, and more. Every campaign is customized to your business goals.'
    },
    {
      question: 'How quickly will we see results?',
      answer: 'You will see improvements in open and click rates within the first campaign (usually 1-2 weeks). Revenue from automated sequences typically appears within 30-60 days once automation is fully set up. Email marketing delivers consistent, measurable ROI from day one.'
    },
    {
      question: 'Can you integrate with our e-commerce or CRM system?',
      answer: 'Yes! Our Growth and Enterprise plans include integration with popular platforms like Shopify, WooCommerce, Salesforce, HubSpot, and more. These integrations enable advanced automation based on purchase history, browsing behavior, and customer lifecycle.'
    },
    {
      question: 'What if we want to cancel?',
      answer: 'All plans are month-to-month with no long-term contracts. You can cancel anytime. However, email marketing delivers the highest ROI of any marketing channel (average $42 for every $1 spent), so most clients continue for years and scale up as their list grows.'
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
              { label: 'Home', href: '/' },
              { label: 'Services', href: '/services' },
              { label: 'Email Marketing' }
            ]} />
          </div>
        </section>

        {/* Hero Section */}
        <section className="bg-gray-50 py-20">
          <div className="container">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl font-bold text-gray-900 mb-6">
                Email Marketing Automation
              </h1>
              <p className="text-xl text-gray-700 mb-8">
                Drive consistent revenue and customer loyalty with AI-optimized email campaigns that deliver $42 for every $1 spent
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/contact" className="btn-primary px-8 py-4 text-lg">
                  Get Free Email Audit
                </Link>
                <Link href="/pricing" className="btn-secondary px-8 py-4 text-lg">
                  View Pricing
                </Link>
              </div>
              <p className="text-sm text-gray-600 mt-6">
                No credit card required • Free strategy session • First campaign in 7 days
              </p>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Complete Email Marketing Solutions
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Everything you need to build, automate, and optimize high-performing email campaigns
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
                Our Email Marketing Process
              </h2>
              <p className="text-xl text-gray-600">
                A proven 4-step approach to email success
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
                Email Marketing Pricing Plans
              </h2>
              <p className="text-xl text-gray-600">
                Choose the plan that fits your list size and goals
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
                See how we have helped businesses drive revenue through email
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
                Everything you need to know about our email marketing services
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
                Ready to Turn Email Into Your Top Revenue Channel?
              </h2>
              <p className="text-xl mb-8 text-white/90">
                Get a free email audit and discover how to maximize your ROI
              </p>
              <Link
                href="/contact"
                className="inline-block bg-white text-primary-600 font-semibold px-8 py-4 rounded-lg hover:bg-gray-100 transition-colors"
              >
                Get Free Email Audit
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
