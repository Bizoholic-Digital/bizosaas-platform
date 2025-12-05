import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import Link from 'next/link'
import { Share2, MessageCircle, TrendingUp, Users, CheckCircle, ArrowRight, Award, Quote } from 'lucide-react'

export const metadata: Metadata = {
  title: 'Social Media Management & Marketing Services | Bizoholic',
  description: 'Build engaged communities and drive conversions with AI-powered social media strategies. Multi-platform management, content creation, and advertising.',
}

export default function SocialMediaPage() {
  const features = [
    {
      icon: <Share2 className="w-6 h-6" />,
      title: 'AI-Powered Content Generation',
      description: 'Create engaging social posts across all platforms with AI-assisted writing and design'
    },
    {
      icon: <MessageCircle className="w-6 h-6" />,
      title: 'Multi-Platform Scheduling',
      description: 'Manage all your social accounts from one dashboard with optimal posting times'
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: 'Engagement Tracking & Response',
      description: 'Monitor mentions, comments, and messages with automated response suggestions'
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: 'Influencer Identification',
      description: 'Find and connect with relevant influencers to amplify your brand reach'
    }
  ]

  const benefits = [
    'Increase brand awareness by 300-500%',
    'Build engaged communities that drive sales',
    'Generate qualified leads from social platforms',
    'Improve customer engagement and loyalty',
    '24/7 social monitoring and response',
    'Data-driven content strategy and optimization'
  ]

  const process = [
    {
      step: 1,
      title: 'Social Audit & Strategy',
      description: 'Analyze current presence, audience insights, and competitive landscape'
    },
    {
      step: 2,
      title: 'Content Calendar Development',
      description: 'Create strategic content plan aligned with business goals and audience interests'
    },
    {
      step: 3,
      title: 'Content Creation & Scheduling',
      description: 'Design engaging posts, graphics, and videos optimized for each platform'
    },
    {
      step: 4,
      title: 'Engage & Optimize',
      description: 'Monitor performance, respond to audience, and refine strategy continuously'
    }
  ]

  const pricing = [
    {
      name: 'Starter Social',
      price: '$299',
      period: '/month',
      description: 'Perfect for small businesses',
      features: [
        '3 social platforms (Facebook, Instagram, Twitter)',
        '15 posts per month (5 per platform)',
        'Basic engagement monitoring',
        'Monthly performance report',
        'Community management support'
      ],
      popular: false
    },
    {
      name: 'Growth Social',
      price: '$599',
      period: '/month',
      description: 'For growing brands',
      features: [
        'Everything in Starter Social',
        '5 social platforms (add LinkedIn, TikTok)',
        '30 posts per month (6 per platform)',
        'Social advertising management ($500 ad spend)',
        'Daily engagement monitoring',
        'Influencer outreach (5 contacts/month)',
        'Bi-weekly strategy calls'
      ],
      popular: true
    },
    {
      name: 'Enterprise Social',
      price: '$1,299',
      period: '/month',
      description: 'For established brands',
      features: [
        'Everything in Growth Social',
        'Unlimited platforms and posts',
        'Daily content posting',
        'Advanced social advertising ($2,000+ ad spend)',
        'Influencer partnership management',
        'Crisis management support',
        'Dedicated social media strategist',
        'Custom reporting dashboard'
      ],
      popular: false
    }
  ]

  const caseStudies = [
    {
      industry: 'Fashion Brand',
      challenge: 'Low engagement, minimal follower growth, poor brand awareness',
      solution: 'Comprehensive social strategy with influencer partnerships and targeted ads',
      results: [
        '450% follower growth in 6 months (5K to 27K followers)',
        '85% increase in website traffic from social',
        '12.5% average engagement rate (3x industry average)',
        '$125,000 in revenue directly attributed to social campaigns'
      ]
    },
    {
      industry: 'Restaurant Chain',
      challenge: 'Difficulty driving foot traffic, lack of local engagement',
      solution: 'Instagram-focused content strategy with location-based targeting and user-generated content',
      results: [
        '85% increase in foot traffic from Instagram',
        '2,500+ user-generated posts in 4 months',
        '35% growth in online ordering through social',
        'ROI of 650% on social advertising spend'
      ]
    }
  ]

  const testimonials = [
    {
      name: 'Emma Rodriguez',
      company: 'Luxe Fashion Boutique',
      role: 'Founder & CEO',
      quote: 'Bizoholic transformed our social media from crickets to conversations. Our follower count exploded, but more importantly, we are seeing real customers and sales. The influencer partnerships alone paid for the service 3x over.',
      rating: 5
    },
    {
      name: 'David Kim',
      company: 'Urban Eats Restaurant Group',
      role: 'Marketing Director',
      quote: 'We went from posting randomly to having a strategic, data-driven social presence. Our Instagram following grew 300% in 4 months, and we can track exactly how many customers are coming from social. The ROI is incredible.',
      rating: 5
    }
  ]

  const faqs = [
    {
      question: 'How many platforms should I be on?',
      answer: 'It depends on your target audience and business goals. Most businesses see the best results focusing on 2-3 platforms where their audience is most active. We help identify the right platforms during our initial strategy phase. Quality over quantity is key - it is better to dominate 2 platforms than be mediocre on 6.'
    },
    {
      question: 'Do you create all the content or do we need to provide it?',
      answer: 'We handle everything - content creation, graphics, captions, hashtags, and scheduling. You simply approve the content calendar each month. If you have specific photos, products, or content you want featured, we can incorporate those too. It is a collaborative process.'
    },
    {
      question: 'How quickly will we see results?',
      answer: 'You will see engagement improvements within the first 30 days. Follower growth and traffic increases typically appear within 60-90 days. Social media is a long-term strategy, but our clients consistently see measurable results within the first quarter.'
    },
    {
      question: 'What makes your social media management different?',
      answer: 'We combine AI-powered content optimization with human creativity and strategy. Our data-driven approach ensures every post is optimized for engagement, while our creative team ensures authenticity and brand alignment. Plus, we focus on business results - not just vanity metrics.'
    },
    {
      question: 'Do you respond to comments and messages?',
      answer: 'Yes! All plans include community management. We monitor comments, mentions, and messages during business hours (9am-6pm EST) and respond on your behalf following approved brand guidelines. For Enterprise clients, we offer 24/7 monitoring and response.'
    },
    {
      question: 'Can you help with social media advertising?',
      answer: 'Absolutely. Our Growth and Enterprise plans include social advertising management across Facebook, Instagram, LinkedIn, and TikTok. We handle everything from ad creative to targeting, optimization, and reporting. Minimum ad spend starts at $500/month.'
    },
    {
      question: 'What if we want to cancel?',
      answer: 'All plans are month-to-month with no long-term contracts. However, we recommend at least 6 months to build momentum and see full results. Most clients stay with us for years because social media is an ongoing strategy that compounds over time.'
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
              { label: 'Social Media Management' }
            ]} />
          </div>
        </section>

        {/* Hero Section */}
        <section className="bg-gray-50 py-20">
          <div className="container">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl font-bold text-gray-900 mb-6">
                Social Media Management & Marketing
              </h1>
              <p className="text-xl text-gray-700 mb-8">
                Build engaged communities and drive real business results with AI-powered social media strategies across all major platforms
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/contact" className="btn-primary px-8 py-4 text-lg">
                  Get Free Social Audit
                </Link>
                <Link href="/pricing" className="btn-secondary px-8 py-4 text-lg">
                  View Pricing
                </Link>
              </div>
              <p className="text-sm text-gray-600 mt-6">
                No credit card required • Free strategy session • Results in 30 days
              </p>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Complete Social Media Solutions
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Everything you need to build, engage, and convert your social audience
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
                Our Social Media Process
              </h2>
              <p className="text-xl text-gray-600">
                A proven 4-step approach to social media success
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
                Social Media Pricing Plans
              </h2>
              <p className="text-xl text-gray-600">
                Choose the plan that fits your social media goals
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
                See how we have helped businesses build engaged social communities
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
                Everything you need to know about our social media services
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
                Ready to Build Your Social Community?
              </h2>
              <p className="text-xl mb-8 text-white/90">
                Get a free social media audit and discover how to grow your following
              </p>
              <Link
                href="/contact"
                className="inline-block bg-white text-primary-600 font-semibold px-8 py-4 rounded-lg hover:bg-gray-100 transition-colors"
              >
                Get Free Social Audit
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
