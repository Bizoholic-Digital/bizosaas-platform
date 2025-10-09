import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://host.docker.internal:8001'

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const slug = searchParams.get('slug')
  
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
    
    // Filter by slug if provided
    if (slug && data.services) {
      const service = data.services.find((s: any) => s.slug === slug)
      if (service) {
        return NextResponse.json({ services: [service], count: 1, source: data.source })
      }
    }
    
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching services from Brain API:', error)
    
    // Return fallback data if Brain API is unavailable
    const fallbackData = {
      services: [
        {
          id: "ai-campaign-management",
          title: "AI Campaign Management",
          slug: "ai-campaign-management",
          icon: "🤖",
          badge: "AI-First",
          category: "Digital Marketing",
          description: "Autonomous AI agents that create, optimize, and manage your marketing campaigns across all platforms 24/7.",
          featured: true,
          order: 1,
          price_data: { starting_price: "₹29,999", currency: "INR", billing_period: "month" },
          features: [
            "24/7 Autonomous Campaign Creation",
            "Real-time Multi-platform Optimization",
            "AI-powered Audience Targeting",
            "Automated Budget Management",
            "Cross-platform Analytics Integration",
            "Intelligent Ad Creative Testing",
            "Dynamic Bid Optimization",
            "Performance Anomaly Detection"
          ],
          benefits: [
            "Reduce campaign management time by 90%",
            "Increase ROAS by average 45%", 
            "24/7 optimization without human intervention",
            "Consistent performance across all platforms",
            "Data-driven creative optimization",
            "Automated budget reallocation"
          ],
          case_studies: [
            {
              client_name: "TechStartup Inc",
              industry: "Technology",
              results: "300% increase in qualified leads within 60 days",
              metrics: "45% lower CPA, 4.2x ROAS improvement"
            },
            {
              client_name: "RetailPro",
              industry: "E-commerce",
              results: "500% growth in online sales through AI optimization",
              metrics: "60% cost reduction, 800% conversion rate boost"
            }
          ],
          testimonials: [
            {
              quote: "The AI campaign management has completely transformed our marketing results. We're seeing unprecedented ROI.",
              author: "Sarah Chen",
              position: "Marketing Director",
              company: "TechStartup Inc",
              rating: 5
            }
          ]
        },
        {
          id: "content-generation",
          title: "Content Generation",
          slug: "content-generation",
          icon: "✍️",
          badge: "AI-Powered",
          category: "Content Marketing",
          description: "Create unlimited high-quality content across all formats - blogs, social posts, ads, videos, and more - using advanced AI technology.",
          featured: true,
          order: 2,
          price_data: { starting_price: "₹19,999", currency: "INR", billing_period: "month" },
          features: [
            "Unlimited Blog Posts & Articles",
            "Social Media Content Calendar",
            "Ad Copy & Creative Generation", 
            "Video Scripts & Storyboards",
            "Email Marketing Sequences",
            "SEO-Optimized Content",
            "Multi-language Content Support",
            "Brand Voice Consistency",
            "Content Performance Analytics",
            "Automated Publishing Workflows"
          ],
          benefits: [
            "Generate 10x more content in half the time",
            "Maintain consistent brand voice across all platforms",
            "SEO-optimized content that ranks higher",
            "Multi-format content from single brief",
            "Real-time performance optimization",
            "Significant cost reduction vs hiring writers"
          ],
          case_studies: [
            {
              client_name: "DigitalCorp",
              industry: "Technology",
              results: "500% increase in organic traffic through AI-generated content",
              metrics: "50+ articles/month, 400% engagement boost"
            }
          ],
          testimonials: [
            {
              quote: "Content generation AI has revolutionized our content strategy. Quality and quantity both improved dramatically.",
              author: "Mike Johnson",
              position: "Content Manager",
              company: "DigitalCorp",
              rating: 5
            }
          ]
        },
        {
          id: "seo-optimization",
          title: "SEO Optimization",
          slug: "seo-optimization",
          icon: "🔍",
          badge: "Most Popular",
          category: "Search Marketing",
          description: "Advanced SEO strategies and on-page optimization to boost your search engine rankings and organic traffic.",
          featured: true,
          order: 3,
          price_data: { starting_price: "₹15,999", currency: "INR", billing_period: "month" },
          features: [
            "Comprehensive SEO Audits",
            "Keyword Research & Strategy",
            "On-Page Optimization",
            "Technical SEO Improvements",
            "Content Optimization",
            "Link Building Campaigns",
            "Local SEO Management",
            "Performance Tracking & Reporting"
          ],
          benefits: [
            "Improve search rankings within 3 months",
            "Increase organic traffic by 200%+",
            "Better user experience and site performance",
            "Higher conversion rates from organic traffic",
            "Long-term sustainable growth",
            "Comprehensive competitive analysis"
          ],
          case_studies: [
            {
              client_name: "LocalBiz",
              industry: "Local Services",
              results: "Ranked #1 for 15 target keywords within 4 months",
              metrics: "300% organic traffic increase, 180% lead growth"
            }
          ],
          testimonials: [
            {
              quote: "SEO optimization delivered exactly what was promised. We're now dominating our local market.",
              author: "David Park",
              position: "Business Owner",
              company: "LocalBiz",
              rating: 5
            }
          ]
        }
      ],
      count: 3,
      source: "fallback"
    }
    
    // Filter by slug if provided for fallback data too
    if (slug) {
      const service = fallbackData.services.find(s => s.slug === slug)
      if (service) {
        return NextResponse.json({ services: [service], count: 1, source: "fallback" })
      } else {
        return NextResponse.json({ services: [], count: 0, source: "fallback" })
      }
    }
    
    return NextResponse.json(fallbackData)
  }
}