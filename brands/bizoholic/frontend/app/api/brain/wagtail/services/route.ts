import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://localhost:8000'

const fallbackServices = [
  {
    id: 1,
    title: "AI Campaign Management",
    slug: "ai-campaign-management",
    icon: "🤖",
    badge: "Most Popular",
    category: "Paid Media",
    service_description: "Autonomous agents create, optimize, and manage your advertising campaigns across Google Ads, Meta, LinkedIn, and 40+ other platforms.",
    featured: true,
    order: 1,
    price_data: { starting_price: "$997", currency: "USD", billing_period: "month" }
  },
  {
    id: 2,
    title: "Content Generation",
    slug: "content-generation",
    icon: "🎯",
    badge: "New",
    category: "Content",
    service_description: "AI-powered content creation for blogs, social media, email campaigns, and website copy that converts visitors into customers.",
    featured: true,
    order: 2,
    price_data: { starting_price: "$697", currency: "USD", billing_period: "month" }
  },
  {
    id: 3,
    title: "Performance Analytics",
    slug: "performance-analytics",
    icon: "📊",
    badge: "Essential",
    category: "Analytics",
    service_description: "Real-time analytics and insights with automated reporting that helps you understand what's working and what needs optimization.",
    featured: true,
    order: 3,
    price_data: { starting_price: "$497", currency: "USD", billing_period: "month" }
  },
  {
    id: 4,
    title: "Marketing Automation",
    slug: "marketing-automation",
    icon: "🚀",
    badge: "Trending",
    category: "Automation",
    service_description: "End-to-end marketing automation workflows that nurture leads and convert prospects into customers automatically.",
    featured: true,
    order: 4,
    price_data: { starting_price: "$797", currency: "USD", billing_period: "month" }
  },
  {
    id: 5,
    title: "Strategy Consulting",
    slug: "strategy-consulting",
    icon: "💡",
    badge: "Expert",
    category: "Strategy",
    service_description: "Expert marketing strategy consultation to align your business goals with data-driven marketing approaches.",
    featured: true,
    order: 5,
    price_data: { starting_price: "$4,997", currency: "USD", billing_period: "one-time" }
  },
  {
    id: 6,
    title: "Creative Design",
    slug: "creative-design",
    icon: "🎨",
    badge: "Visuals",
    category: "Design",
    service_description: "Professional design services for all your marketing materials, from social media graphics to landing pages.",
    featured: true,
    order: 6,
    price_data: { starting_price: "$997", currency: "USD", billing_period: "month" }
  },
  {
    id: 7,
    title: "SEO Optimization",
    slug: "seo-optimization",
    icon: "🔍",
    badge: "Traffic",
    category: "Search",
    service_description: "Advanced SEO strategies and on-page optimization to boost your search engine rankings and organic traffic.",
    featured: true,
    order: 7,
    price_data: { starting_price: "$1,497", currency: "USD", billing_period: "month" }
  },
  {
    id: 8,
    title: "Email Marketing",
    slug: "email-marketing",
    icon: "📧",
    badge: "Retention",
    category: "Email",
    service_description: "Strategic email campaigns with personalized content, automation, and advanced segmentation for maximum engagement.",
    featured: true,
    order: 8,
    price_data: { starting_price: "$599", currency: "USD", billing_period: "month" }
  },
  {
    id: 9,
    title: "Social Media Marketing",
    slug: "social-media-marketing",
    icon: "📱",
    badge: "Engagement",
    category: "Social",
    service_description: "Comprehensive social media management across all platforms with content creation, community management, and paid advertising.",
    featured: true,
    order: 9,
    price_data: { starting_price: "$899", currency: "USD", billing_period: "month" }
  }
]

export async function GET(request: NextRequest) {
  try {
    // Call Brain API Gateway
    const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://localhost:8000'
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 10000) // 10s timeout

    console.log(`Fetching services from Brain API: ${BRAIN_API_URL}/api/v1/cms/services/`)

    const response = await fetch(`${BRAIN_API_URL}/api/v1/cms/services/`, {
      headers: {
        'Content-Type': 'application/json',
      },
      signal: controller.signal,
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      console.error(`Wagtail API error: ${response.status}`)
      // Return fallback data
      return NextResponse.json({
        services: fallbackServices,
        count: fallbackServices.length,
        source: 'fallback'
      })
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error('Error fetching services from Wagtail:', error)

    // Return fallback data on error
    return NextResponse.json({
      services: fallbackServices,
      count: fallbackServices.length,
      source: 'fallback'
    })
  }
}