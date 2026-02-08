import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// GET /api/brain/saleor/cart - Get or create cart
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const cartToken = searchParams.get('token')
    
    let url = `${BRAIN_API_URL}/api/brain/saleor/cart`
    if (cartToken) {
      url += `?token=${cartToken}`
    }

    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
      },
      cache: 'no-store',
    })

    if (!response.ok) {
      throw new Error(`Brain API responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching cart from Brain API:', error)
    
    // Return fallback empty cart
    const fallbackData = {
      cart: {
        id: 'fallback-cart',
        token: 'fallback-token',
        lines: [],
        totalPrice: {
          gross: {
            amount: 0,
            currency: 'USD'
          }
        },
        itemsCount: 0,
        isShippingRequired: false,
        shippingPrice: {
          gross: {
            amount: 0,
            currency: 'USD'
          }
        }
      },
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 200 })
  }
}

// POST /api/brain/saleor/cart - Create new cart
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/cart`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`Brain API responded with status: ${response.status}, ${JSON.stringify(errorData)}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error creating cart via Brain API:', error)
    return NextResponse.json(
      { error: 'Failed to create cart', details: error.message },
      { status: 500 }
    )
  }
}

// PUT /api/brain/saleor/cart - Update cart (e.g., apply discount)
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/cart`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`Brain API responded with status: ${response.status}, ${JSON.stringify(errorData)}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error updating cart via Brain API:', error)
    return NextResponse.json(
      { error: 'Failed to update cart', details: error.message },
      { status: 500 }
    )
  }
}