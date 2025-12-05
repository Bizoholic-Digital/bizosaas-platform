import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// POST /api/brain/saleor/checkout/payment - Process checkout payment
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/checkout/payment`, {
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
    console.error('Error processing payment via Brain API:', error)
    return NextResponse.json(
      { error: 'Failed to process payment', details: error.message },
      { status: 500 }
    )
  }
}

// GET /api/brain/saleor/checkout/payment - Get payment methods
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

    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/checkout/payment?token=${checkoutToken}`, {
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
    console.error('Error fetching payment methods from Brain API:', error)
    
    // Return fallback payment methods
    const fallbackData = {
      paymentMethods: [
        {
          id: 'stripe',
          name: 'Credit Card',
          description: 'Pay securely with your credit or debit card',
          isActive: true,
          config: []
        },
        {
          id: 'paypal',
          name: 'PayPal',
          description: 'Pay with your PayPal account',
          isActive: true,
          config: []
        }
      ],
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 200 })
  }
}