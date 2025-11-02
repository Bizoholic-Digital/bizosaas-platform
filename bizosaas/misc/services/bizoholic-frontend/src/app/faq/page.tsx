import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'

export const metadata: Metadata = {
  title: 'FAQ | Bizoholic',
  description: 'Frequently asked questions about Bizoholic AI-powered marketing services.',
}

export default function FAQPage() {
  const faqs = [
    {
      category: 'Getting Started',
      questions: [
        {
          q: 'How quickly can I get started with Bizoholic?',
          a: 'You can be up and running in as little as 15 minutes. Simply sign up for an account, connect your business accounts (like Google Analytics, Google Ads, etc.), and our AI agents will begin analyzing your data and creating personalized strategies immediately.'
        },
        {
          q: 'Do I need technical knowledge to use Bizoholic?',
          a: 'No technical knowledge is required. Our platform is designed for business owners and marketers of all skill levels. The AI handles the technical complexity while presenting you with clear, actionable recommendations through an intuitive dashboard.'
        },
        {
          q: 'What information do I need to provide during setup?',
          a: 'You\'ll need basic business information (name, industry, target audience) and access to your existing marketing accounts (Google Analytics, social media, email platform, etc.). The more data you connect, the better our AI can optimize your campaigns.'
        }
      ]
    },
    {
      category: 'Pricing & Plans',
      questions: [
        {
          q: 'How does the pricing work?',
          a: 'We offer tiered pricing based on your business needs. Each plan includes a set number of AI agent hours, automation workflows, and supported channels. You can start with our Basic plan at $299/month and scale up as your business grows. All plans include a 14-day free trial.'
        },
        {
          q: 'Is there a free trial?',
          a: 'Yes! We offer a 14-day free trial with full access to our platform. No credit card is required to start. You can explore all features and see real results before committing to a paid plan.'
        },
        {
          q: 'Can I change or cancel my plan?',
          a: 'Absolutely. You can upgrade, downgrade, or cancel your plan at any time. Changes take effect at the start of your next billing cycle. If you cancel, you\'ll retain access until the end of your current billing period.'
        },
        {
          q: 'Do you offer custom enterprise pricing?',
          a: 'Yes, we offer custom enterprise plans for businesses with specific needs, multiple brands, or high-volume requirements. Contact our sales team at sales@bizoholic.com for a personalized quote.'
        }
      ]
    },
    {
      category: 'AI & Technology',
      questions: [
        {
          q: 'How does the AI automation work?',
          a: 'Our platform uses 93+ specialized AI agents powered by advanced machine learning models. These agents continuously analyze your data, monitor market trends, optimize campaigns, create content, and make data-driven decisions 24/7. Each agent specializes in a specific marketing function like SEO, PPC, content creation, or social media management.'
        },
        {
          q: 'What is the claimed 75% cost reduction?',
          a: 'Traditional marketing agencies charge $5,000-$15,000/month for services that our AI agents can perform for a fraction of the cost. By automating repetitive tasks, optimizing in real-time, and eliminating human inefficiencies, we deliver the same (or better) results at 75% less cost than traditional agency models.'
        },
        {
          q: 'How accurate are the AI recommendations?',
          a: 'Our AI agents are trained on millions of successful campaigns and continuously learn from your specific data. They achieve 85-95% accuracy in predictions and recommendations, and improve over time as they learn your business. All recommendations include confidence scores and supporting data.'
        },
        {
          q: 'Can I override AI decisions?',
          a: 'Yes, you maintain full control. The AI makes recommendations and can execute automatically with your approval, but you can always review, modify, or override any decision. We also offer different automation levels from "full auto" to "suggestions only."'
        }
      ]
    },
    {
      category: 'Services & Features',
      questions: [
        {
          q: 'What marketing services does Bizoholic provide?',
          a: 'We offer a comprehensive suite of AI-powered marketing services including: SEO optimization, PPC advertising management, social media marketing, content creation, email marketing automation, conversion rate optimization, analytics and reporting, reputation management, and lead generation.'
        },
        {
          q: 'Can I use Bizoholic for specific channels only?',
          a: 'Yes, you can choose which marketing channels to activate. Start with one or two channels and expand as you see results. Our platform is modular, so you pay only for the services you use.'
        },
        {
          q: 'Do you provide content creation?',
          a: 'Yes! Our AI content agents can create blog posts, social media captions, email campaigns, ad copy, landing page content, and more. All content is optimized for SEO and your brand voice. You can review and edit before publishing.'
        },
        {
          q: 'How does the reporting work?',
          a: 'You get real-time dashboards with all key metrics, plus automated weekly and monthly reports. Reports are customizable and can be white-labeled. You can also schedule reports to be sent to clients or stakeholders automatically.'
        }
      ]
    },
    {
      category: 'Results & ROI',
      questions: [
        {
          q: 'When will I see results?',
          a: 'Most clients see measurable improvements within 7-14 days. Quick wins include optimized ad campaigns, better email open rates, and improved website conversions. Longer-term results like SEO rankings and brand awareness typically show significant improvement within 60-90 days.'
        },
        {
          q: 'What kind of ROI can I expect?',
          a: 'Most clients see 3-5x ROI within the first 90 days. The exact ROI depends on your industry, budget, and current marketing maturity. Our AI provides ROI projections and tracks actual performance against targets in real-time.'
        },
        {
          q: 'Do you guarantee results?',
          a: 'While we cannot guarantee specific outcomes (as they depend on many factors), we do guarantee our AI agents will work 24/7 to optimize your campaigns. If you\'re not satisfied in the first 30 days, we offer a full refund, no questions asked.'
        }
      ]
    },
    {
      category: 'Integration & Compatibility',
      questions: [
        {
          q: 'What platforms do you integrate with?',
          a: 'We integrate with 50+ major platforms including: Google Analytics, Google Ads, Facebook Ads, Instagram, LinkedIn, Twitter, HubSpot, Mailchimp, Shopify, WordPress, WooCommerce, Stripe, and many more. New integrations are added regularly.'
        },
        {
          q: 'Can I use Bizoholic with my existing tools?',
          a: 'Yes! Bizoholic is designed to work alongside your existing marketing stack. We enhance rather than replace your current tools. Our AI pulls data from your existing platforms and pushes optimized campaigns back to them.'
        },
        {
          q: 'Do you work with e-commerce platforms?',
          a: 'Absolutely. We have deep integrations with Shopify, WooCommerce, BigCommerce, and other major e-commerce platforms. Our AI can optimize product listings, create dynamic retargeting campaigns, and predict customer lifetime value.'
        }
      ]
    },
    {
      category: 'Support & Training',
      questions: [
        {
          q: 'What kind of support do you offer?',
          a: 'All plans include email support with 24-hour response time. Premium and Enterprise plans include live chat support, dedicated account managers, and priority phone support. We also offer extensive documentation, video tutorials, and webinars.'
        },
        {
          q: 'Do you provide training?',
          a: 'Yes! We offer comprehensive onboarding for all new users, including personalized training sessions. We also host weekly webinars covering advanced features and best practices. All training resources are available in our knowledge base.'
        },
        {
          q: 'Can you help migrate from another platform?',
          a: 'Yes, our team can assist with migration from other marketing platforms or agencies. We\'ll help transfer your campaigns, import historical data, and ensure a smooth transition with zero downtime.'
        }
      ]
    },
    {
      category: 'Security & Privacy',
      questions: [
        {
          q: 'Is my data secure?',
          a: 'Yes, security is our top priority. We use bank-level encryption (AES-256), secure data centers, regular security audits, and SOC 2 Type II compliance. Your data is never shared with third parties without your explicit consent.'
        },
        {
          q: 'Who has access to my data?',
          a: 'Only you and authorized users on your account can access your data. Our AI agents process your data securely, and our support team can only access your account with your explicit permission. We never sell or share your data.'
        },
        {
          q: 'Are you GDPR and CCPA compliant?',
          a: 'Yes, we are fully compliant with GDPR, CCPA, and other major data protection regulations. We have built-in tools for data export, deletion requests, and consent management. All data is processed in accordance with applicable privacy laws.'
        }
      ]
    },
    {
      category: 'Advanced Features',
      questions: [
        {
          q: 'Can I create custom AI workflows?',
          a: 'Yes! Premium and Enterprise plans include a visual workflow builder where you can create custom automation sequences. Combine multiple AI agents, set triggers, and define custom logic without coding.'
        },
        {
          q: 'Do you support multi-location or franchise businesses?',
          a: 'Yes, our Enterprise plan includes multi-location management with location-specific campaigns, unified reporting, and location performance comparison. Perfect for franchises, retail chains, and service businesses with multiple branches.'
        },
        {
          q: 'Can I white-label Bizoholic for my clients?',
          a: 'Yes! Agency and Enterprise plans support white-labeling. You can customize the platform with your branding, create client accounts, and resell our services under your brand. We provide partner support and training.'
        }
      ]
    }
  ]

  return (
    <>
      <Navigation />
      <main className="min-h-screen bg-white">
        <div className="container py-24">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-16">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">Frequently Asked Questions</h1>
              <p className="text-xl text-gray-600">
                Everything you need to know about Bizoholic AI-powered marketing
              </p>
            </div>

            {faqs.map((section, sectionIndex) => (
              <div key={sectionIndex} className="mb-12">
                <h2 className="text-2xl font-semibold text-gray-900 mb-6 pb-3 border-b-2 border-primary-500">
                  {section.category}
                </h2>
                <div className="space-y-6">
                  {section.questions.map((faq, faqIndex) => (
                    <div key={faqIndex} className="bg-gray-50 rounded-lg p-6 hover:bg-gray-100 transition-colors">
                      <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-start">
                        <span className="text-primary-600 mr-2 flex-shrink-0">Q:</span>
                        <span>{faq.q}</span>
                      </h3>
                      <div className="flex items-start">
                        <span className="text-gray-500 mr-2 flex-shrink-0 font-semibold">A:</span>
                        <p className="text-gray-700 leading-relaxed">{faq.a}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}

            <div className="mt-16 bg-primary-50 rounded-xl p-8 text-center">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Still Have Questions?</h2>
              <p className="text-gray-700 mb-6">
                Can&apos;t find the answer you&apos;re looking for? Our team is here to help.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <a
                  href="/contact"
                  className="btn-primary px-8 py-3 inline-block"
                >
                  Contact Support
                </a>
                <a
                  href="mailto:support@bizoholic.com"
                  className="btn-secondary px-8 py-3 inline-block"
                >
                  Email Us
                </a>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
