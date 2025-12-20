import { NextRequest, NextResponse } from "next/server";

const BRAIN_HUB_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://bizosaas-brain-unified:8001";

export async function GET(request: NextRequest) {
  let brainStatus = "unknown";

  try {
    const url = `${BRAIN_HUB_URL}/health`;

    // Attempt to check backend health but don't fail if it's down
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      signal: AbortSignal.timeout(2000)
    });

    if (response.ok) {
      brainStatus = "healthy";
    } else {
      brainStatus = "unhealthy_response";
    }
  } catch (error) {
    console.warn("Backend health check failed:", error);
    brainStatus = "unreachable";
  }

  // Always return healthy for the frontend itself
  return NextResponse.json({
    status: "healthy",
    timestamp: new Date().toISOString(),
    service: "bizosaas-client-portal",
    components: {
      brain_api: brainStatus
    }
  }, { status: 200 });
}
