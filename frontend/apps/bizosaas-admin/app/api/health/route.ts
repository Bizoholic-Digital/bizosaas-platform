import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Basic health check for BizOSaaS Admin Dashboard
    const healthData = {
      status: 'healthy',
      service: 'bizosaas-admin',
      timestamp: new Date().toISOString(),
      platform: 'bizosaas-admin',
      version: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
      environment: process.env.NODE_ENV || 'development',
      port: process.env.PORT || 3009,
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      tenant: 'bizosaas',
      features: {
        userManagement: process.env.NEXT_PUBLIC_ENABLE_USER_MANAGEMENT === 'true',
        tenantManagement: process.env.NEXT_PUBLIC_ENABLE_TENANT_MANAGEMENT === 'true',
        systemMonitoring: process.env.NEXT_PUBLIC_ENABLE_SYSTEM_MONITORING === 'true',
        analytics: process.env.NEXT_PUBLIC_ENABLE_ADVANCED_ANALYTICS === 'true',
        security: process.env.NEXT_PUBLIC_ENABLE_SECURITY_CONTROLS === 'true',
      },
    };

    return NextResponse.json(healthData, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        service: 'bizosaas-admin',
        timestamp: new Date().toISOString(),
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}