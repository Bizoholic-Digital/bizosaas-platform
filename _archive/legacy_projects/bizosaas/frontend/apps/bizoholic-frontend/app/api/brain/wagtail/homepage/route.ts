import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    // Forward the request to the Brain API
    const response = await fetch(`${BRAIN_API_URL}/api/brain/wagtail/homepage`, {
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
    console.error('Error fetching homepage from Brain API:', error)
    
    // Return fallback data if Brain API is unavailable
    const fallbackData = {
      homepage: {
        title: "Bizoholic - AI-Powered Marketing",
        hero_title: "Transform Your Business with AI Marketing", 
        hero_subtitle: "Bizoholic Digital empowers businesses with autonomous AI agents that handle marketing campaigns, content creation, SEO optimization, and lead generation - all running 24/7 on autopilot.",
        hero_cta_text: "Start Free Trial",
        hero_cta_url: "/auth/login",
        features_title: "Everything You Need to Dominate Digital Marketing",
        features: [
          {
            icon: "🤖",
            title: "AI Campaign Management",
            description: "Autonomous agents create, optimize, and manage your advertising campaigns across Google Ads, Meta, LinkedIn, and 40+ other platforms."
          },
          {
            icon: "🎯", 
            title: "Content Generation",
            description: "AI-powered content creation for blogs, social media, email campaigns, and website copy that converts visitors into customers."
          },
          {
            icon: "📊",
            title: "Performance Analytics", 
            description: "Real-time analytics and insights with automated reporting that helps you understand what's working and what needs optimization."
          }
        ],
        stats: [
          {"number": "75%", "label": "Cost Reduction", "description": "Average marketing cost savings"},
          {"number": "300%", "label": "ROI Increase", "description": "Average return on investment boost"},
          {"number": "7 Days", "label": "Quick Results", "description": "Time to see measurable results"},
          {"number": "15 Min", "label": "Fast Setup", "description": "Time to get started"}
        ],
        show_service_status: true,
        tenant_id: "demo"
      },
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData)
  }
}