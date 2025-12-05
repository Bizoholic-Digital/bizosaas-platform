import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    // Forward the request to the Brain API
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/categories`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000', // Set proper host for tenant resolution
      },
      cache: 'no-store', // Disable caching for dynamic content
    })

    if (!response.ok) {
      throw new Error(`Brain API responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching categories from Brain API:', error)
    
    // Return fallback data if Brain API is unavailable
    const fallbackData = {
      categories: [
        {
          id: "fallback-1",
          name: "Electronics",
          slug: "electronics",
          description: "Latest gadgets and tech accessories",
          products: { totalCount: 45 }
        },
        {
          id: "fallback-2",
          name: "Fashion",
          slug: "fashion",
          description: "Trendy clothing and accessories",
          products: { totalCount: 89 }
        },
        {
          id: "fallback-3",
          name: "Home & Garden",
          slug: "home-garden",
          description: "Everything for your home and garden",
          products: { totalCount: 67 }
        }
      ],
      count: 3,
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData)
  }
}