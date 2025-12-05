import { NextRequest, NextResponse } from 'next/server'

const API_GATEWAY_URL = process.env.API_GATEWAY_URL || 'http://localhost:8082'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const domain = searchParams.get('domain') || request.headers.get('host') || 'localhost:3000'
    
    // For now, create mock tenant data based on domain
    // In production, this would call the backend tenant_context_service
    let tenantData = getMockTenantData(domain)
    
    // Try to call backend first, fall back to mock on error
    try {
      const response = await fetch(`${API_GATEWAY_URL}/api/tenant-context?domain=${domain}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          // Forward authorization if present
          ...(request.headers.get('authorization') && {
            'Authorization': request.headers.get('authorization')!
          })
        },
        signal: AbortSignal.timeout(5000) // 5 second timeout
      })
      
      if (response.ok) {
        const backendData = await response.json()
        // Transform backend data to frontend format
        tenantData = transformBackendTenantData(backendData, domain)
      }
    } catch (error) {
      // Backend not available, use mock data
      console.log('Backend not available, using mock tenant data:', error)
    }
    
    return NextResponse.json(tenantData)
    
  } catch (error) {
    console.error('Tenant context API error:', error)
    
    // Return default tenant on error
    return NextResponse.json({
      tenant_id: 'default',
      bizosaas_tenant_id: 'default',
      domain: 'localhost:3000',
      name: 'BizOSaaS Platform',
      subscription_tier: 'enterprise',
      features: ['*'],
      branding: {
        brand_name: 'BizOSaaS',
        primary_color: '#3B82F6',
        secondary_color: '#1E40AF'
      },
      is_active: true,
      error: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}

function getMockTenantData(domain: string) {
  // Mock tenant data based on domain
  const tenantMap = {
    'bizoholic.com': {
      tenant_id: 'bizoholic',
      bizosaas_tenant_id: 'bizoholic',
      domain: 'bizoholic.com',
      name: 'Bizoholic Digital',
      subscription_tier: 'enterprise',
      features: ['ai-marketing', 'campaign-management', 'analytics', 'crm'],
      branding: {
        logo_url: '/logos/bizoholic-logo.svg',
        primary_color: '#3B82F6',
        secondary_color: '#1E40AF',
        brand_name: 'Bizoholic'
      },
      is_active: true
    },
    'coreldove.com': {
      tenant_id: 'coreldove',
      bizosaas_tenant_id: 'coreldove',
      domain: 'coreldove.com',
      name: 'CoreLDove',
      subscription_tier: 'enterprise',
      features: ['ai-sourcing', 'ecommerce', 'supplier-network', 'analytics'],
      branding: {
        logo_url: '/logos/coreldove-logo.svg',
        primary_color: '#10B981',
        secondary_color: '#059669',
        brand_name: 'CoreLDove'
      },
      is_active: true
    },
    'thrillring.com': {
      tenant_id: 'thrillring',
      bizosaas_tenant_id: 'thrillring',
      domain: 'thrillring.com',
      name: 'ThrillRing',
      subscription_tier: 'professional',
      features: ['ai-matching', 'social-network', 'dating', 'events'],
      branding: {
        logo_url: '/logos/thrillring-logo.svg',
        primary_color: '#EF4444',
        secondary_color: '#DC2626',
        brand_name: 'ThrillRing'
      },
      is_active: true
    },
    'quanttrade.com': {
      tenant_id: 'quanttrade',
      bizosaas_tenant_id: 'quanttrade', 
      domain: 'quanttrade.com',
      name: 'QuantTrade',
      subscription_tier: 'enterprise',
      features: ['ai-trading', 'portfolio-management', 'risk-analysis', 'backtesting'],
      branding: {
        logo_url: '/logos/quanttrade-logo.svg',
        primary_color: '#7C3AED',
        secondary_color: '#6D28D9',
        brand_name: 'QuantTrade'
      },
      is_active: true
    }
  }
  
  // Return specific tenant or default
  return tenantMap[domain as keyof typeof tenantMap] || {
    tenant_id: 'default',
    bizosaas_tenant_id: 'default',
    domain: domain,
    name: 'BizOSaaS Platform',
    subscription_tier: 'enterprise',
    features: ['*'],
    branding: {
      logo_url: '/logos/bizosaas-logo.svg',
      brand_name: 'BizOSaaS',
      primary_color: '#3B82F6',
      secondary_color: '#1E40AF'
    },
    is_active: true
  }
}

function transformBackendTenantData(backendData: any, domain: string) {
  // Transform backend tenant context to frontend format
  return {
    tenant_id: backendData.tenant_id || backendData.bizosaas_tenant_id,
    bizosaas_tenant_id: backendData.bizosaas_tenant_id,
    domain: backendData.full_domain || domain,
    name: backendData.name || 'Platform',
    subscription_tier: backendData.subscription_tier || 'free',
    features: backendData.features || [],
    branding: {
      logo_url: backendData.branding?.logo_url,
      primary_color: backendData.branding?.primary_color || '#3B82F6',
      secondary_color: backendData.branding?.secondary_color || '#1E40AF',
      brand_name: backendData.name || 'Platform'
    },
    is_active: backendData.is_active !== false,
    // Include service-specific contexts for debugging
    wagtail_context: backendData.wagtail_context,
    saleor_context: backendData.saleor_context,
    crm_context: backendData.crm_context
  }
}