import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// GET /api/brain/saleor/shipping - Get available shipping methods
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const checkoutToken = searchParams.get('token')
    const countryCode = searchParams.get('country')
    
    let url = `${BRAIN_API_URL}/api/brain/saleor/shipping`
    const params = new URLSearchParams()
    
    if (checkoutToken) params.set('token', checkoutToken)
    if (countryCode) params.set('country', countryCode)
    
    if (params.toString()) {
      url += `?${params.toString()}`
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
    console.error('Error fetching shipping methods from Brain API:', error)
    
    // Return fallback shipping methods
    const fallbackData = {
      shippingMethods: [
        {
          id: 'standard-shipping',
          name: 'Standard Shipping',
          description: 'Delivery in 5-7 business days',
          price: {
            amount: 9.99,
            currency: 'USD'
          },
          minimumOrderWeight: null,
          maximumOrderWeight: null,
          isActive: true
        },
        {
          id: 'express-shipping', 
          name: 'Express Shipping',
          description: 'Delivery in 2-3 business days',
          price: {
            amount: 19.99,
            currency: 'USD'
          },
          minimumOrderWeight: null,
          maximumOrderWeight: null,
          isActive: true
        },
        {
          id: 'free-shipping',
          name: 'Free Shipping',
          description: 'Free delivery on orders over $75',
          price: {
            amount: 0,
            currency: 'USD'
          },
          minimumOrderWeight: null,
          maximumOrderWeight: null,
          isActive: true,
          minimumOrderPrice: {
            amount: 75,
            currency: 'USD'
          }
        }
      ],
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 200 })
  }
}

// POST /api/brain/saleor/shipping - Apply shipping method to checkout
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/shipping`, {
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
    console.error('Error applying shipping method via Brain API:', error)
    return NextResponse.json(
      { error: 'Failed to apply shipping method', details: error.message },
      { status: 500 }
    )
  }
}