import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

const fallbackHomepage = {
  title: "Bizoholic - AI-Powered Marketing",
  hero_title: "Transform Your Business with AI Marketing",
  hero_subtitle: "Bizoholic Digital empowers businesses with autonomous AI agents that handle marketing campaigns, content creation, SEO optimization, and lead generation - all running 24/7 on autopilot.",
  hero_cta_text: "Start Free Trial",
  hero_cta_url: "http://localhost:3003/register",
  features_title: "Everything You Need to Dominate Digital Marketing",
  features: [
    {
      icon: "🤖",
      title: "AI Campaign Management",
      description: "Autonomous agents create, optimize, and manage your advertising campaigns across Google Ads, Meta, LinkedIn, and 40+ other platforms.",
      link: "/services/ai-campaign-management"
    },
    {
      icon: "🎯",
      title: "Content Generation",
      description: "AI-powered content creation for blogs, social media, email campaigns, and website copy that converts visitors into customers.",
      link: "/services/content-generation"
    },
    {
      icon: "📊",
      title: "Performance Analytics",
      description: "Real-time analytics and insights with automated reporting that helps you understand what's working and what needs optimization.",
      link: "/services/performance-analytics"
    },
    {
      icon: "🚀",
      title: "Marketing Automation",
      description: "End-to-end marketing automation workflows that nurture leads and convert prospects into customers automatically.",
      link: "/services/marketing-automation"
    },
    {
      icon: "💡",
      title: "Strategy Consulting",
      description: "Expert marketing strategy consultation to align your business goals with data-driven marketing approaches.",
      link: "/services/strategy-consulting"
    },
    {
      icon: "🎨",
      title: "Creative Design",
      description: "Professional design services for all your marketing materials, from social media graphics to landing pages.",
      link: "/services/creative-design"
    },
    {
      icon: "🔍",
      title: "SEO Optimization",
      description: "Advanced SEO strategies and on-page optimization to boost your search engine rankings and organic traffic.",
      link: "/services/seo-optimization"
    },
    {
      icon: "📧",
      title: "Email Marketing",
      description: "Strategic email campaigns with personalized content, automation, and advanced segmentation for maximum engagement.",
      link: "/services/email-marketing"
    },
    {
      icon: "📱",
      title: "Social Media Marketing",
      description: "Comprehensive social media management across all platforms with content creation, community management, and paid advertising.",
      link: "/services/social-media-marketing"
    }
  ],
  stats: [
    { "number": "75%", "label": "Cost Reduction", "description": "Average marketing cost savings" },
    { "number": "300%", "label": "ROI Increase", "description": "Average return on investment boost" },
    { "number": "7 Days", "label": "Quick Results", "description": "Time to see measurable results" },
    { "number": "15 Min", "label": "Fast Setup", "description": "Time to get started" }
  ],
  show_service_status: true,
  tenant_id: "demo"
}

export async function GET(request: NextRequest) {
  try {
    // Call Brain API Gateway
    const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://localhost:8000'
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 10000) // 10s timeout

    console.log(`Fetching homepage from Brain API: ${BRAIN_API_URL}/api/v1/cms/homepage/`)

    const response = await fetch(`${BRAIN_API_URL}/api/v1/cms/homepage/`, {
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
        homepage: fallbackHomepage,
        source: 'fallback'
      })
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error('Error fetching homepage from Wagtail:', error)

    // Return fallback data on error
    return NextResponse.json({
      homepage: fallbackHomepage,
      source: 'fallback'
    })
  }
}