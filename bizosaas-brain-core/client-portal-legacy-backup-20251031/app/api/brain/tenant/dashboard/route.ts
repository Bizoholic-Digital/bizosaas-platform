import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const tenantId = searchParams.get('tenant') || 'demo'

    // Forward the request to the Brain API with tenant context
    const response = await fetch(`${BRAIN_API_URL}/api/brain/tenant/dashboard`, {
      headers: {
        'Content-Type': 'application/json',
        'X-Tenant-ID': tenantId,
        'Host': 'localhost:3001',
      },
      cache: 'no-store',
    })

    if (!response.ok) {
      throw new Error(`Brain API responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching tenant dashboard from Brain API:', error)

    // Return fallback data based on tenant
    const tenantId = new URL(request.url).searchParams.get('tenant') || 'demo'
    const fallbackData = getTenantFallbackData(tenantId)

    return NextResponse.json({
      ...fallbackData,
      source: 'fallback'
    })
  }
}

function getTenantFallbackData(tenantId: string) {
  const baseMetrics = {
    timestamp: new Date().toISOString(),
    tenant_id: tenantId
  }

  switch (tenantId) {
    case 'coreldove':
      return {
        ...baseMetrics,
        tenant_name: 'CorelDove E-commerce',
        industry: 'E-commerce',
        metrics: {
          total_leads: 156,
          revenue: 28450,
          orders: 234,
          growth: 18.5,
          conversion_rate: 3.2,
          avg_order_value: 121.58
        },
        features: ['products', 'orders', 'inventory', 'analytics'],
        recent_activity: [
          { type: 'order', message: 'New order #1234 received', time: '2 minutes ago' },
          { type: 'product', message: 'Product "Wireless Headphones" updated', time: '15 minutes ago' },
          { type: 'campaign', message: 'Email campaign "Summer Sale" sent', time: '1 hour ago' }
        ],
        ai_insights: [
          'Product performance is 23% above average this month',
          'Inventory levels for electronics category need attention',
          'Recommended: Launch retargeting campaign for abandoned carts'
        ]
      }

    case 'business_directory':
      return {
        ...baseMetrics,
        tenant_name: 'Business Directory Platform',
        industry: 'Local Business',
        metrics: {
          total_leads: 89,
          revenue: 15200,
          orders: 67,
          growth: 12.3,
          business_listings: 1240,
          verified_businesses: 892
        },
        features: ['businesses', 'leads', 'local_seo', 'analytics'],
        recent_activity: [
          { type: 'business', message: 'New business "Downtown Cafe" added', time: '5 minutes ago' },
          { type: 'lead', message: 'Lead qualification completed for ABC Corp', time: '20 minutes ago' },
          { type: 'seo', message: 'Local SEO optimization completed', time: '2 hours ago' }
        ],
        ai_insights: [
          'Local search traffic increased by 35% this week',
          'Restaurant category showing highest engagement',
          'Recommended: Focus on healthcare and automotive categories'
        ]
      }

    case 'thrillring':
      return {
        ...baseMetrics,
        tenant_name: 'ThrillRing Gaming',
        industry: 'Gaming & E-sports',
        metrics: {
          total_leads: 312,
          revenue: 18900,
          orders: 145,
          growth: 28.7,
          active_players: 2840,
          tournaments: 12
        },
        features: ['tournaments', 'players', 'gaming_analytics', 'community'],
        recent_activity: [
          { type: 'tournament', message: 'Weekly CS:GO tournament started', time: '1 minute ago' },
          { type: 'player', message: 'New player "ProGamer123" registered', time: '8 minutes ago' },
          { type: 'achievement', message: 'Player unlocked "Victory Streak" achievement', time: '25 minutes ago' }
        ],
        ai_insights: [
          'E-sports tournament engagement up 45% this month',
          'FPS games showing highest participation rates',
          'Recommended: Launch mobile gaming tournaments'
        ]
      }

    default:
      return {
        ...baseMetrics,
        tenant_name: 'Demo Client',
        industry: 'General',
        metrics: {
          total_leads: 1234,
          revenue: 45231,
          orders: 892,
          growth: 12.0,
          conversion_rate: 2.8,
          customer_satisfaction: 4.7
        },
        features: ['crm', 'cms', 'analytics', 'marketing'],
        recent_activity: [
          { type: 'lead', message: 'New lead from contact form', time: '3 minutes ago' },
          { type: 'campaign', message: 'Marketing campaign launched', time: '30 minutes ago' },
          { type: 'content', message: 'Blog post published', time: '1 hour ago' }
        ],
        ai_insights: [
          'Website traffic increased by 15% this week',
          'Email open rates are above industry average',
          'Recommended: A/B test your landing page headlines'
        ]
      }
  }
}