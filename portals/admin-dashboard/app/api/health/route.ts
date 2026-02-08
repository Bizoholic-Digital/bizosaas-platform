import { NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || "http://brain-gateway:8000";

export async function GET() {
  try {
    // Check Brain Hub connectivity
    const brainHealthUrl = `${BRAIN_API_URL}/health`;
    let brainStatus = "unknown";

    try {
      const response = await fetch(brainHealthUrl, {
        signal: AbortSignal.timeout(3000)
      });
      brainStatus = response.ok ? "healthy" : `degraded (${response.status})`;
    } catch (e) {
      brainStatus = "unreachable";
    }

    const healthData = {
      status: brainStatus === "healthy" ? 'healthy' : 'degraded',
      service: 'bizosaas-admin',
      timestamp: new Date().toISOString(),
      dependencies: {
        brain_gateway: brainStatus
      },
      uptime: process.uptime(),
      memory: process.memoryUsage(),
    };

    return NextResponse.json(healthData, {
      status: brainStatus === "healthy" ? 200 : 503
    });
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