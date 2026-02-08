import { NextRequest, NextResponse } from 'next/server'

export async function GET() {
  const platformsData = {
    'client-portal': {
      name: 'Client Portal',
      status: 'healthy',
      uptime: 99.9,
      users: 1205
    },
    'business-directory': {
      name: 'Business Directory',
      status: 'healthy',
      uptime: 99.7,
      businesses: 15487
    },
    'thrillring': {
      name: 'ThrillRing Gaming',
      status: 'healthy',
      uptime: 99.8,
      players: 2048000
    },
    'bizoholic': {
      name: 'Bizoholic Marketing',
      status: 'healthy',
      uptime: 99.6,
      campaigns: 156
    },
    'coreldove': {
      name: 'CorelDove E-commerce',
      status: 'healthy',
      uptime: 99.5,
      orders: 892
    }
  }

  return NextResponse.json({
    success: true,
    source: 'enhanced_fallback',
    data: platformsData,
    meta: {
      totalPlatforms: Object.keys(platformsData).length,
      lastUpdated: new Date().toISOString()
    }
  })
}
