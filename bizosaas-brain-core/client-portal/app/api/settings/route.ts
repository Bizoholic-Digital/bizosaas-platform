/**
 * Settings API Route for Client Portal
 * Manages user and tenant settings
 */

import { NextRequest, NextResponse } from 'next/server'

// Mock settings data for demo
const mockSettingsData = {
  user_settings: {
    id: "user_demo_001",
    email: "demo@bizosaas.com",
    name: "Demo User",
    avatar: "/api/placeholder/150/150",
    timezone: "America/Los_Angeles",
    language: "en",
    notification_preferences: {
      email_notifications: true,
      push_notifications: false,
      marketing_emails: true,
      security_alerts: true
    },
    dashboard_preferences: {
      default_view: "overview",
      cards_per_row: 3,
      theme: "light",
      sidebar_collapsed: false
    }
  },
  tenant_settings: {
    tenant_id: "tenant_demo",
    company_name: "BizOSaaS Demo",
    company_logo: "/api/placeholder/200/80",
    domain: "demo.bizosaas.com",
    industry: "technology",
    company_size: "1-10",
    billing: {
      plan: "professional",
      billing_cycle: "monthly",
      next_billing_date: "2024-10-25T00:00:00Z",
      payment_method: "card",
      card_last_four: "4242"
    },
    features: {
      crm_enabled: true,
      analytics_enabled: true,
      integrations_enabled: true,
      ai_agents_enabled: true,
      custom_domains: false,
      white_labeling: false
    },
    limits: {
      max_users: 5,
      current_users: 1,
      max_campaigns: 10,
      current_campaigns: 3,
      max_integrations: 15,
      current_integrations: 7
    }
  },
  integrations: {
    google_ads: {
      enabled: true,
      status: "connected",
      last_sync: "2024-09-25T10:30:00Z",
      account_id: "123-456-7890"
    },
    facebook_ads: {
      enabled: true,
      status: "connected", 
      last_sync: "2024-09-25T09:15:00Z",
      account_id: "987654321"
    },
    google_analytics: {
      enabled: true,
      status: "connected",
      last_sync: "2024-09-25T08:45:00Z",
      account_id: "GA4-ABCD123"
    },
    stripe: {
      enabled: false,
      status: "disconnected",
      last_sync: null,
      account_id: null
    },
    hubspot: {
      enabled: false,
      status: "disconnected",
      last_sync: null,
      account_id: null
    }
  },
  security: {
    two_factor_enabled: false,
    last_password_change: "2024-08-15T14:20:00Z",
    active_sessions: 2,
    login_history: [
      {
        timestamp: "2024-09-25T14:30:00Z",
        ip_address: "192.168.1.100",
        device: "Chrome on macOS",
        location: "San Francisco, CA"
      },
      {
        timestamp: "2024-09-24T16:45:00Z",
        ip_address: "192.168.1.100",
        device: "Chrome on macOS", 
        location: "San Francisco, CA"
      }
    ]
  },
  api_keys: [
    {
      id: "key_001",
      name: "Production API Key",
      key: "bzo_live_********************************",
      created_at: "2024-09-01T10:00:00Z",
      last_used: "2024-09-25T12:30:00Z",
      permissions: ["read", "write"]
    },
    {
      id: "key_002", 
      name: "Development API Key",
      key: "bzo_test_********************************",
      created_at: "2024-09-10T14:15:00Z",
      last_used: "2024-09-23T09:20:00Z",
      permissions: ["read"]
    }
  ]
}

// GET /api/settings - Fetch all settings
export async function GET(request: NextRequest) {
  try {
    console.log('[CLIENT-PORTAL] GET settings data')
    
    // Simulate slight delay for realism
    await new Promise(resolve => setTimeout(resolve, 100))
    
    return NextResponse.json({
      success: true,
      data: mockSettingsData,
      last_updated: new Date().toISOString(),
      source: "fallback"
    })
  } catch (error) {
    console.error('Error fetching settings:', error)
    return NextResponse.json(
      { error: 'Failed to fetch settings', details: error.message },
      { status: 500 }
    )
  }
}

// PUT /api/settings - Update settings
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    const { section, data } = body
    
    console.log(`[CLIENT-PORTAL] PUT settings section: ${section}`)
    
    // Validate section
    const validSections = ['user_settings', 'tenant_settings', 'integrations', 'security', 'api_keys']
    if (!validSections.includes(section)) {
      return NextResponse.json(
        { error: 'Invalid settings section' },
        { status: 400 }
      )
    }
    
    // Simulate update
    await new Promise(resolve => setTimeout(resolve, 200))
    
    return NextResponse.json({
      success: true,
      message: `${section} updated successfully`,
      updated_at: new Date().toISOString(),
      source: "fallback"
    })
  } catch (error) {
    console.error('Error updating settings:', error)
    return NextResponse.json(
      { error: 'Failed to update settings', details: error.message },
      { status: 500 }
    )
  }
}

// POST /api/settings - Create new setting (like API key)
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { action, data } = body
    
    console.log(`[CLIENT-PORTAL] POST settings action: ${action}`)
    
    if (action === 'create_api_key') {
      const newKey = {
        id: 'key_' + Date.now(),
        name: data.name || 'New API Key',
        key: 'bzo_' + (data.environment || 'live') + '_' + Math.random().toString(36).substring(2, 34),
        created_at: new Date().toISOString(),
        last_used: null,
        permissions: data.permissions || ['read']
      }
      
      return NextResponse.json({
        success: true,
        message: 'API key created successfully',
        api_key: newKey,
        source: "fallback"
      })
    }
    
    return NextResponse.json({
      success: true,
      message: 'Setting created successfully',
      created_at: new Date().toISOString(),
      source: "fallback"
    })
  } catch (error) {
    console.error('Error creating setting:', error)
    return NextResponse.json(
      { error: 'Failed to create setting', details: error.message },
      { status: 500 }
    )
  }
}

// DELETE /api/settings - Delete setting
export async function DELETE(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const section = searchParams.get('section')
    const id = searchParams.get('id')
    
    console.log(`[CLIENT-PORTAL] DELETE settings section: ${section}, id: ${id}`)
    
    if (!section || !id) {
      return NextResponse.json(
        { error: 'Section and ID are required' },
        { status: 400 }
      )
    }
    
    // Simulate deletion
    await new Promise(resolve => setTimeout(resolve, 150))
    
    return NextResponse.json({
      success: true,
      message: `Setting deleted successfully`,
      deleted_at: new Date().toISOString(),
      source: "fallback"
    })
  } catch (error) {
    console.error('Error deleting setting:', error)
    return NextResponse.json(
      { error: 'Failed to delete setting', details: error.message },
      { status: 500 }
    )
  }
}