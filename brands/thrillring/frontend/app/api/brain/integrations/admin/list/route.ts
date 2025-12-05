import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://host.docker.internal:8001'

export async function GET(request: NextRequest) {
  try {
    const response = await fetch(`${BRAIN_API_URL}/api/integrations/admin/list`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // Add authentication headers if needed
      },
      cache: 'no-store'
    })

    if (!response.ok) {
      throw new Error(`Brain API responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error('Error fetching integrations from Brain API:', error)
    
    // Return mock data for development
    return NextResponse.json({
      integrations: [
        {
          id: 'google-analytics-4',
          name: 'Google Analytics 4',
          category: 'analytics',
          description: 'Advanced web analytics and insights platform',
          status: 'enabled',
          global_enabled: true,
          tenant_count: 45,
          usage_stats: {
            active_tenants: 42,
            total_requests: 125430,
            success_rate: 98.5,
            avg_response_time: 245
          },
          permissions: {
            super_admin_only: false,
            require_approval: false,
            auto_provision: true,
            rate_limit: 1000
          },
          health: {
            status: 'healthy',
            last_check: '2025-09-13T16:20:00Z',
            uptime: 99.9,
            error_count: 2
          },
          features: ['Enhanced E-commerce', 'Custom Dimensions', 'Real-time Reporting'],
          dependencies: ['Google Tag Manager'],
          created_at: '2025-01-01T00:00:00Z',
          updated_at: '2025-09-13T16:00:00Z'
        },
        {
          id: 'meta-ads-advanced',
          name: 'Meta Ads (Advanced)',
          category: 'advertising',
          description: 'Facebook and Instagram advertising platform with advanced targeting',
          status: 'enabled',
          global_enabled: true,
          tenant_count: 38,
          usage_stats: {
            active_tenants: 35,
            total_requests: 89234,
            success_rate: 97.2,
            avg_response_time: 187
          },
          permissions: {
            super_admin_only: false,
            require_approval: true,
            auto_provision: false,
            rate_limit: 500
          },
          health: {
            status: 'healthy',
            last_check: '2025-09-13T16:15:00Z',
            uptime: 99.7,
            error_count: 5
          },
          features: ['Advanced Targeting', 'Custom Audiences', 'Lookalike Audiences', 'Campaign Automation'],
          dependencies: ['Meta Business Manager', 'Facebook Pixel'],
          created_at: '2025-01-01T00:00:00Z',
          updated_at: '2025-09-13T15:30:00Z'
        },
        {
          id: 'hubspot-enterprise',
          name: 'HubSpot Enterprise',
          category: 'crm',
          description: 'Enterprise CRM and marketing automation platform',
          status: 'enabled',
          global_enabled: false,
          tenant_count: 12,
          usage_stats: {
            active_tenants: 12,
            total_requests: 45678,
            success_rate: 99.1,
            avg_response_time: 156
          },
          permissions: {
            super_admin_only: true,
            require_approval: true,
            auto_provision: false,
            rate_limit: 2000
          },
          health: {
            status: 'healthy',
            last_check: '2025-09-13T16:10:00Z',
            uptime: 99.95,
            error_count: 1
          },
          features: ['Contact Management', 'Deal Tracking', 'Email Automation', 'Custom Properties'],
          dependencies: ['HubSpot API Key', 'OAuth 2.0'],
          created_at: '2025-02-01T00:00:00Z',
          updated_at: '2025-09-13T14:00:00Z'
        },
        {
          id: 'stripe-payments',
          name: 'Stripe Payments',
          category: 'payment',
          description: 'Advanced payment processing and subscription management',
          status: 'maintenance',
          global_enabled: true,
          tenant_count: 67,
          usage_stats: {
            active_tenants: 63,
            total_requests: 234567,
            success_rate: 99.8,
            avg_response_time: 98
          },
          permissions: {
            super_admin_only: true,
            require_approval: true,
            auto_provision: false,
            rate_limit: 5000
          },
          health: {
            status: 'warning',
            last_check: '2025-09-13T16:25:00Z',
            uptime: 99.2,
            error_count: 12
          },
          features: ['Payment Processing', 'Subscription Management', 'Invoice Generation', 'Webhooks'],
          dependencies: ['Stripe API Keys', 'Webhook Endpoints'],
          created_at: '2025-01-01T00:00:00Z',
          updated_at: '2025-09-13T16:25:00Z'
        }
      ]
    })
  }
}