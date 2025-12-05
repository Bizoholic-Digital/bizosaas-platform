import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    // Forward the request to the Brain API
    const response = await fetch(`${BRAIN_API_URL}/api/brain/wagtail/services`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000', // Set proper host for tenant resolution
      },
      cache: 'no-store', // Disable caching for dynamic content
    })

    if (!response.ok) {
      throw new Error(`Brain API responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching services from Brain API:', error)
    
    // Return fallback data if Brain API is unavailable
    const fallbackData = {
      services: [
        {
          id: 1,
          title: "SEO Optimization & Local SEO",
          slug: "seo-optimization-local-seo",
          icon: "🔍",
          badge: "Most Popular",
          category: "Search Marketing",
          service_description: "Boost your search rankings with AI-powered SEO optimization. Our advanced algorithms analyze your website, competitors, and search trends to deliver 200% better organic traffic within 90 days.",
          featured: true,
          order: 1,
          price_data: { starting_price: "$299", currency: "USD", billing_period: "month" }
        },
        {
          id: 2,
          title: "Paid Advertising (PPC) Management", 
          slug: "paid-advertising-ppc-management",
          icon: "💰",
          badge: "High ROI",
          category: "Paid Media",
          service_description: "Maximize your ad spend with AI-driven PPC campaigns. Our intelligent bidding algorithms reduce cost-per-click by 45% while increasing conversions by 180%.",
          featured: true,
          order: 2,
          price_data: { starting_price: "$599", currency: "USD", billing_period: "month" }
        },
        {
          id: 3,
          title: "Social Media Marketing & Management",
          slug: "social-media-marketing-management", 
          icon: "📱",
          badge: "Trending",
          category: "Social Media",
          service_description: "Grow your social presence with AI-powered content creation and scheduling. Generate viral-worthy posts, optimize posting times, and engage with your audience automatically.",
          featured: true,
          order: 3,
          price_data: { starting_price: "$399", currency: "USD", billing_period: "month" }
        }
      ],
      count: 3,
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData)
  }
}