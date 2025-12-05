import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Basic health check for Bizoholic Marketing Frontend
    const healthData = {
      status: 'healthy',
      service: 'bizoholic-frontend',
      timestamp: new Date().toISOString(),
      platform: 'bizoholic-marketing',
      version: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
      environment: process.env.NODE_ENV || 'development',
      port: process.env.PORT || 3008,
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      tenant: 'bizoholic',
      features: {
        marketing: true,
        leadCapture: process.env.NEXT_PUBLIC_ENABLE_LEAD_CAPTURE === 'true',
        blog: process.env.NEXT_PUBLIC_ENABLE_BLOG === 'true',
        caseStudies: process.env.NEXT_PUBLIC_ENABLE_CASE_STUDIES === 'true',
        seo: process.env.NEXT_PUBLIC_ENABLE_SEO_OPTIMIZATION === 'true',
      },
    };

    return NextResponse.json(healthData, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        service: 'bizoholic-frontend',
        timestamp: new Date().toISOString(),
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}