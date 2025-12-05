import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// GET /api/brain/saleor/orders - Get user orders
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const userId = searchParams.get('userId')
    const orderId = searchParams.get('orderId')
    
    let url = `${BRAIN_API_URL}/api/brain/saleor/orders`
    const params = new URLSearchParams()
    
    if (userId) params.set('userId', userId)
    if (orderId) params.set('orderId', orderId)
    
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
    console.error('Error fetching orders from Brain API:', error)
    
    // Return fallback orders data
    const fallbackData = {
      orders: [
        {
          id: 'fallback-order-1',
          number: 'CD-001',
          token: 'fallback-order-token-1',
          status: 'FULFILLED',
          paymentStatus: 'FULLY_CHARGED',
          created: new Date().toISOString(),
          total: {
            gross: {
              amount: 199.99,
              currency: 'USD'
            }
          },
          lines: [
            {
              id: 'line-1',
              productName: 'Premium Wireless Headphones',
              quantity: 1,
              unitPrice: {
                gross: {
                  amount: 199.99,
                  currency: 'USD'
                }
              },
              totalPrice: {
                gross: {
                  amount: 199.99,
                  currency: 'USD'
                }
              }
            }
          ],
          shippingAddress: {
            firstName: 'John',
            lastName: 'Doe',
            streetAddress1: '123 Main St',
            city: 'New York',
            postalCode: '10001',
            country: {
              code: 'US',
              country: 'United States'
            }
          },
          billingAddress: {
            firstName: 'John',
            lastName: 'Doe',
            streetAddress1: '123 Main St',
            city: 'New York',
            postalCode: '10001',
            country: {
              code: 'US',
              country: 'United States'
            }
          }
        }
      ],
      totalCount: 1,
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 200 })
  }
}

// POST /api/brain/saleor/orders - Create order from checkout
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/orders`, {
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
    console.error('Error creating order via Brain API:', error)
    return NextResponse.json(
      { error: 'Failed to create order', details: error.message },
      { status: 500 }
    )
  }
}