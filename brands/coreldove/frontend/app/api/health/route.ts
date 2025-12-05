import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Basic health check for CoreLDove E-commerce Frontend
    const healthData = {
      status: 'healthy',
      service: 'coreldove-frontend',
      timestamp: new Date().toISOString(),
      platform: 'coreldove-ecommerce',
      version: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
      environment: process.env.NODE_ENV || 'development',
      port: process.env.PORT || 3007,
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      tenant: 'coreldove',
      features: {
        ecommerce: true,
        payments: process.env.NEXT_PUBLIC_ENABLE_PAYMENTS === 'true',
        inventory: process.env.NEXT_PUBLIC_ENABLE_INVENTORY_TRACKING === 'true',
      },
    };

    return NextResponse.json(healthData, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        service: 'coreldove-frontend',
        timestamp: new Date().toISOString(),
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}