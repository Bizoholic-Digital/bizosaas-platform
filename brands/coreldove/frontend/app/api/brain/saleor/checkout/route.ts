import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// POST /api/brain/saleor/checkout - Create checkout from cart
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/checkout`, {
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
    console.error('Error creating checkout via Brain API:', error)
    return NextResponse.json(
      { error: 'Failed to create checkout', details: error.message },
      { status: 500 }
    )
  }
}

// GET /api/brain/saleor/checkout - Get checkout by token
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const checkoutToken = searchParams.get('token')
    
    if (!checkoutToken) {
      return NextResponse.json(
        { error: 'Checkout token is required' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/checkout?token=${checkoutToken}`, {
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
    console.error('Error fetching checkout from Brain API:', error)
    
    // Return fallback checkout data
    const fallbackData = {
      checkout: {
        id: 'fallback-checkout',
        token: 'fallback-checkout-token',
        lines: [],
        totalPrice: {
          gross: {
            amount: 0,
            currency: 'USD'
          }
        },
        subtotalPrice: {
          gross: {
            amount: 0,
            currency: 'USD'
          }
        },
        shippingPrice: {
          gross: {
            amount: 0,
            currency: 'USD'
          }
        },
        isShippingRequired: false,
        availableShippingMethods: [],
        email: '',
        shippingAddress: null,
        billingAddress: null,
        discount: null,
        voucherCode: null
      },
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 200 })
  }
}

// PUT /api/brain/saleor/checkout - Update checkout
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/checkout`, {
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
    console.error('Error updating checkout via Brain API:', error)
    return NextResponse.json(
      { error: 'Failed to update checkout', details: error.message },
      { status: 500 }
    )
  }
}