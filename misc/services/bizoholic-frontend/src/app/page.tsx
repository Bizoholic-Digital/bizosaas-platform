import { Metadata } from 'next'
import Hero from '@/components/sections/Hero'
import Services from '@/components/sections/Services'
import Features from '@/components/sections/Features'
import SocialProof from '@/components/sections/SocialProof'
import CTA from '@/components/sections/CTA'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'

// This will fetch data from Wagtail headless CMS
async function getPageData() {
  try {
    // Fetch from Wagtail API when backend is ready
    // const response = await fetch(`${process.env.WAGTAIL_API_BASE_URL}/pages/`, {
    //   next: { revalidate: 300 } // Revalidate every 5 minutes
    // })
    // const data = await response.json()
    // return data
    
    // Mock data for now - will be replaced with Wagtail CMS content
    return {
      hero: {
        title: "Transform Your Marketing with AI Automation",
        subtitle: "Get 75% cost savings, ROI within 7 days, and setup in 15 minutes. The smartest marketing platform for small businesses.",
        cta_primary: "Get Started Free",
        cta_secondary: "View Demo"
      },
      features: {
        title: "Why Choose Bizoholic AI?",
        items: [
          {
            icon: "🚀",
            title: "75% Cost Reduction",
            description: "Our AI agents replace expensive marketing teams while delivering better results"
          },
          {
            icon: "⚡",
            title: "7-Day ROI",
            description: "See measurable returns within the first week of implementation"
          },
          {
            icon: "🎯",
            title: "15-Min Setup",
            description: "Get up and running in minutes, not months"
          }
        ]
      },
      services: {
        title: "Complete Marketing Automation Suite",
        items: [
          {
            title: "SEO Optimization & Local SEO",
            description: "Boost your search rankings with AI-powered SEO optimization",
            price: "$299/month",
            badge: "Most Popular"
          },
          {
            title: "Paid Advertising (PPC) Management",
            description: "Maximize your ad spend with AI-driven PPC campaigns",
            price: "$599/month",
            badge: "High ROI"
          }
        ]
      }
    }
  } catch (error) {
    console.error('Error fetching page data:', error)
    return null
  }
}

export default async function HomePage() {
  const pageData = await getPageData()

  return (
    <>
      <Navigation />
      <main>
        <Hero data={pageData?.hero} />
        <Features data={pageData?.features} />
        <Services data={pageData?.services} />
        <SocialProof />
        <CTA />
      </main>
      <Footer />
    </>
  )
}

export const metadata: Metadata = {
  title: 'Bizoholic - AI-Powered Marketing Automation',
  description: 'Transform your marketing with AI automation. Get 75% cost savings, ROI within 7 days, and setup in 15 minutes.',
}