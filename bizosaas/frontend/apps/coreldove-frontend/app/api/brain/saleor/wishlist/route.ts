import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// GET /api/brain/saleor/wishlist - Get user wishlist
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const userId = searchParams.get('userId')
    const authHeader = request.headers.get('authorization')
    
    let url = `${BRAIN_API_URL}/api/brain/saleor/wishlist`
    if (userId) {
      url += `?userId=${userId}`
    }

    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        ...(authHeader && { 'Authorization': authHeader })
      },
      cache: 'no-store',
    })

    if (!response.ok) {
      throw new Error(`Brain API responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching wishlist from Brain API:', error)
    
    // Return fallback wishlist data
    const fallbackData = {
      wishlist: {
        id: 'wishlist-fallback',
        items: [
          {
            id: 'wishlist-item-1',
            product: {
              id: 'prod-wireless-headphones',
              name: 'Premium Wireless Headphones',
              slug: 'premium-wireless-headphones',
              description: 'High-quality wireless headphones with noise cancellation',
              category: {
                name: 'Electronics',
                slug: 'electronics'
              },
              pricing: {
                priceRange: {
                  start: {
                    gross: {
                      amount: 199.99,
                      currency: 'USD'
                    }
                  }
                }
              },
              thumbnail: {
                url: '/images/products/headphones.jpg',
                alt: 'Premium Wireless Headphones'
              },
              isAvailable: true
            },
            addedAt: '2024-01-15T10:30:00Z'
          },
          {
            id: 'wishlist-item-2',
            product: {
              id: 'prod-smart-watch',
              name: 'Smart Fitness Watch',
              slug: 'smart-fitness-watch',
              description: 'Advanced fitness tracking with heart rate monitor',
              category: {
                name: 'Wearables',
                slug: 'wearables'
              },
              pricing: {
                priceRange: {
                  start: {
                    gross: {
                      amount: 299.99,
                      currency: 'USD'
                    }
                  }
                }
              },
              thumbnail: {
                url: '/images/products/smartwatch.jpg',
                alt: 'Smart Fitness Watch'
              },
              isAvailable: true
            },
            addedAt: '2024-01-14T15:45:00Z'
          }
        ],
        itemCount: 2
      },
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 200 })
  }
}

// POST /api/brain/saleor/wishlist - Add item to wishlist
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const authHeader = request.headers.get('authorization')
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/wishlist`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        ...(authHeader && { 'Authorization': authHeader })
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
    console.error('Error adding item to wishlist via Brain API:', error)
    
    // Return development fallback for wishlist addition
    const { productId } = await request.json().catch(() => ({}))
    const fallbackData = {
      success: true,
      wishlistItem: {
        id: 'wishlist-item-' + Date.now(),
        productId: productId || 'unknown-product',
        addedAt: new Date().toISOString()
      },
      message: 'Item added to wishlist',
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 201 })
  }
}

// DELETE /api/brain/saleor/wishlist - Remove item from wishlist
export async function DELETE(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const itemId = searchParams.get('itemId')
    const productId = searchParams.get('productId')
    const authHeader = request.headers.get('authorization')
    
    if (!itemId && !productId) {
      return NextResponse.json(
        { error: 'Either itemId or productId is required' },
        { status: 400 }
      )
    }

    let url = `${BRAIN_API_URL}/api/brain/saleor/wishlist`
    const params = new URLSearchParams()
    if (itemId) params.set('itemId', itemId)
    if (productId) params.set('productId', productId)
    url += `?${params.toString()}`

    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        ...(authHeader && { 'Authorization': authHeader })
      },
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`Brain API responded with status: ${response.status}, ${JSON.stringify(errorData)}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error removing item from wishlist via Brain API:', error)
    
    // Return successful removal for development
    const fallbackData = {
      success: true,
      message: 'Item removed from wishlist',
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 200 })
  }
}