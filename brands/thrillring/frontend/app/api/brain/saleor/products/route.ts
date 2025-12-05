import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://host.docker.internal:8001'

export async function GET(request: NextRequest) {
  try {
    // Extract query parameters
    const searchParams = request.nextUrl.searchParams
    const category = searchParams.get('category')
    const search = searchParams.get('search')
    const limit = searchParams.get('limit') || '12'
    
    // Build query string for Brain API
    const queryParams = new URLSearchParams()
    if (category) queryParams.set('category', category)
    if (search) queryParams.set('search', search)
    queryParams.set('limit', limit)
    
    // Forward the request to the Brain API
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/products?${queryParams.toString()}`, {
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
    console.error('Error fetching products from Brain API:', error)
    
    // Return fallback data if Brain API is unavailable
    const fallbackData = {
      products: [
        {
          id: "fallback-1",
          name: "Premium Wireless Headphones",
          description: "High-quality wireless headphones with noise cancellation and premium sound quality.",
          pricing: {
            priceRange: {
              start: {
                gross: {
                  amount: 149.99,
                  currency: "USD"
                }
              }
            }
          },
          thumbnail: {
            url: "/placeholder-product.jpg"
          },
          category: {
            name: "Electronics"
          },
          rating: 4.5,
          reviews: 128
        },
        {
          id: "fallback-2",
          name: "Organic Cotton T-Shirt",
          description: "Comfortable and sustainable organic cotton t-shirt in various colors and sizes.",
          pricing: {
            priceRange: {
              start: {
                gross: {
                  amount: 29.99,
                  currency: "USD"
                }
              }
            }
          },
          thumbnail: {
            url: "/placeholder-product.jpg"
          },
          category: {
            name: "Fashion"
          },
          rating: 4.2,
          reviews: 64
        },
        {
          id: "fallback-3",
          name: "Smart Plant Pot",
          description: "Self-watering smart plant pot with built-in sensors and smartphone connectivity.",
          pricing: {
            priceRange: {
              start: {
                gross: {
                  amount: 79.99,
                  currency: "USD"
                }
              }
            }
          },
          thumbnail: {
            url: "/placeholder-product.jpg"
          },
          category: {
            name: "Home & Garden"
          },
          rating: 4.7,
          reviews: 92
        },
        {
          id: "fallback-4",
          name: "Bluetooth Speaker",
          description: "Portable wireless speaker with deep bass and 12-hour battery life.",
          pricing: {
            priceRange: {
              start: {
                gross: {
                  amount: 89.99,
                  currency: "USD"
                }
              }
            }
          },
          thumbnail: {
            url: "/placeholder-product.jpg"
          },
          category: {
            name: "Electronics"
          },
          rating: 4.3,
          reviews: 156
        },
        {
          id: "fallback-5",
          name: "Designer Handbag",
          description: "Elegant leather handbag with premium craftsmanship and timeless design.",
          pricing: {
            priceRange: {
              start: {
                gross: {
                  amount: 199.99,
                  currency: "USD"
                }
              }
            }
          },
          thumbnail: {
            url: "/placeholder-product.jpg"
          },
          category: {
            name: "Fashion"
          },
          rating: 4.8,
          reviews: 73
        },
        {
          id: "fallback-6",
          name: "Garden Tool Set",
          description: "Complete set of premium gardening tools with ergonomic handles and storage case.",
          pricing: {
            priceRange: {
              start: {
                gross: {
                  amount: 124.99,
                  currency: "USD"
                }
              }
            }
          },
          thumbnail: {
            url: "/placeholder-product.jpg"
          },
          category: {
            name: "Home & Garden"
          },
          rating: 4.6,
          reviews: 89
        }
      ],
      count: 6,
      totalCount: 156,
      hasNextPage: true,
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData)
  }
}