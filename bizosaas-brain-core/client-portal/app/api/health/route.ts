import { NextRequest, NextResponse } from "next/server";

const BRAIN_HUB_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://bizosaas-brain-unified:8001";

export async function GET(request: NextRequest) {
  try {
    const url = `${BRAIN_HUB_URL}/health`;

    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      // Add timeout for health checks
      signal: AbortSignal.timeout(5000)
    });

    if (!response.ok) {
      throw new Error(`Brain Hub responded with status: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error("Health Check API Error:", error);
    
    // Return unhealthy status when Brain Hub is not reachable
    const fallbackData = {
      status: "unhealthy",
      timestamp: new Date().toISOString(),
      service: "bizosaas-client-portal",
      components: {
        brain_api: "unavailable"
      },
      message: "Brain Hub connection failed"
    };
    
    return NextResponse.json(fallbackData, { status: 503 });
  }
}
