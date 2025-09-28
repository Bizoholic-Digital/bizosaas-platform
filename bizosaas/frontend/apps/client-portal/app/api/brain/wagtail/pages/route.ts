import { NextRequest, NextResponse } from "next/server";

const BRAIN_HUB_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://bizosaas-brain-unified:8001";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const queryString = searchParams.toString();
    const url = `${BRAIN_HUB_URL}/api/brain/wagtail/pages${queryString ? `?${queryString}` : ""}`;

    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": request.headers.get("authorization") || "",
      },
    });

    if (!response.ok) {
      throw new Error(`Brain Hub responded with status: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error("Wagtail Pages API Error:", error);
    
    // Return fallback data for development
    const fallbackData = {
      success: true,
      pages: [
        {
          id: "page_001",
          title: "Demo Page",
          slug: "demo-page",
          url_path: "/demo-page/",
          page_type: "StandardPage"
        }
      ],
      message: "Using fallback data - Brain Hub connection failed"
    };
    
    return NextResponse.json(fallbackData);
  }
}
