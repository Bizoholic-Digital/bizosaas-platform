import { NextRequest, NextResponse } from "next/server";

const BRAIN_HUB_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://bizosaas-brain-unified:8001";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const queryString = searchParams.toString();
    const url = `${BRAIN_HUB_URL}/api/brain/saleor/products${queryString ? `?${queryString}` : ""}`;

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
    console.error("Saleor Products API Error:", error);
    
    // Return fallback data for development
    const fallbackData = {
      success: true,
      products: [
        {
          id: "prod_001",
          name: "Demo Product",
          slug: "demo-product",
          price: { amount: 99.0, currency: "USD" }
        }
      ],
      pagination: { total: 1, page: 1, pages: 1, per_page: 10 },
      message: "Using fallback data - Brain Hub connection failed"
    };
    
    return NextResponse.json(fallbackData);
  }
}
