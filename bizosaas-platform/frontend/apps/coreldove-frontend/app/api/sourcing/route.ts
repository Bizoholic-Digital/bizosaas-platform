import { NextRequest, NextResponse } from 'next/server'

// Direct connection to Amazon sourcing service for now
const AMAZON_SOURCING_URL = 'http://amazon-sourcing-8085:8080'

export async function GET(request: NextRequest) {
  try {
    // Extract query parameters
    const searchParams = request.nextUrl.searchParams
    const query = searchParams.get('query') || 'fitness equipment'
    const category = searchParams.get('category')
    const minPrice = searchParams.get('min_price')
    const maxPrice = searchParams.get('max_price')
    const limit = searchParams.get('limit') || '10'
    
    console.log('🔍 Amazon sourcing request:', { query, category, minPrice, maxPrice, limit })
    
    // Forward the request to the Amazon sourcing service
    const response = await fetch(`${AMAZON_SOURCING_URL}/sourcing/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        category,
        min_price: minPrice ? parseFloat(minPrice) : undefined,
        max_price: maxPrice ? parseFloat(maxPrice) : undefined,
        limit: parseInt(limit),
        marketplace: 'amazon.in'
      }),
      cache: 'no-store', // Disable caching for dynamic content
    })

    if (!response.ok) {
      throw new Error(`Amazon sourcing service responded with status: ${response.status}`)
    }

    const sourcedProducts = await response.json()
    
    // Transform Amazon sourced products to match Saleor product format for compatibility
    const transformedProducts = sourcedProducts.map((product: any, index: number) => ({
      id: product.asin,
      name: product.title,
      description: product.features.join('. ') || `High-quality ${product.title}`,
      pricing: {
        priceRange: {
          start: {
            gross: {
              amount: parseFloat(product.price || '0'),
              currency: product.currency || 'INR'
            }
          }
        }
      },
      thumbnail: {
        url: product.image_url || `/placeholder-product-${index + 1}.jpg`
      },
      category: {
        name: product.category || 'Sourced Products'
      },
      rating: product.rating || 4.0,
      reviews: product.review_count || 50,
      brand: product.brand,
      brand_url: product.brand_url,  // Added brand store URL
      availability: product.availability,
      amazonUrl: product.product_url,
      seller_name: product.seller_name,
      seller_url: product.seller_url,  // Added seller profile URL
      seller_rating: product.seller_rating,
      seller_review_count: product.seller_review_count,
      source: 'amazon_sourcing'
    }))
    
    const responseData = {
      products: transformedProducts,
      count: transformedProducts.length,
      totalCount: transformedProducts.length,
      hasNextPage: false,
      source: 'amazon_sourcing',
      currency: 'INR',
      marketplace: 'amazon.in'
    }
    
    console.log('✅ Amazon sourcing response:', responseData.count, 'products sourced')
    return NextResponse.json(responseData)
    
  } catch (error) {
    console.error('❌ Error fetching products from Amazon sourcing service:', error)
    
    // Return fallback INR products if Amazon sourcing is unavailable
    const fallbackData = {
      products: [
        {
          id: "fallback-indian-1",
          name: "Premium Yoga Mat Anti-Slip 6mm",
          description: "High-quality yoga mat with anti-slip surface, perfect for fitness enthusiasts.",
          pricing: {
            priceRange: {
              start: {
                gross: {
                  amount: 899,
                  currency: "INR"
                }
              }
            }
          },
          thumbnail: {
            url: "/placeholder-yoga-mat.jpg"
          },
          category: {
            name: "Fitness"
          },
          rating: 4.3,
          reviews: 127,
          source: "fallback_indian"
        },
        {
          id: "fallback-indian-2",
          name: "Resistance Bands Set with Door Anchor",
          description: "Complete resistance bands set with 5 resistance levels and exercise guide.",
          pricing: {
            priceRange: {
              start: {
                gross: {
                  amount: 599,
                  currency: "INR"
                }
              }
            }
          },
          thumbnail: {
            url: "/placeholder-resistance-bands.jpg"
          },
          category: {
            name: "Fitness"
          },
          rating: 4.5,
          reviews: 89,
          source: "fallback_indian"
        },
        {
          id: "fallback-indian-3",
          name: "Adjustable Dumbbell Set 10-40kg",
          description: "Space-saving adjustable dumbbells with steel construction and rubber grip.",
          pricing: {
            priceRange: {
              start: {
                gross: {
                  amount: 4999,
                  currency: "INR"
                }
              }
            }
          },
          thumbnail: {
            url: "/placeholder-dumbbells.jpg"
          },
          category: {
            name: "Fitness"
          },
          rating: 4.7,
          reviews: 156,
          source: "fallback_indian"
        }
      ],
      count: 3,
      totalCount: 50,
      hasNextPage: true,
      source: "fallback_indian",
      currency: "INR",
      marketplace: "amazon.in"
    }
    
    return NextResponse.json(fallbackData)
  }
}

export async function POST(request: NextRequest) {
  // Handle POST requests for advanced sourcing
  try {
    const body = await request.json()
    console.log('🔍 Amazon sourcing POST request:', body)
    
    const response = await fetch(`${AMAZON_SOURCING_URL}/sourcing/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...body,
        marketplace: 'amazon.in'
      }),
    })

    if (!response.ok) {
      throw new Error(`Amazon sourcing service responded with status: ${response.status}`)
    }

    const sourcedProducts = await response.json()
    
    // Transform products to match expected format
    const transformedProducts = sourcedProducts.map((product: any, index: number) => ({
      id: product.asin,
      name: product.title,
      description: product.features.join('. ') || `High-quality ${product.title}`,
      pricing: {
        priceRange: {
          start: {
            gross: {
              amount: parseFloat(product.price || '0'),
              currency: product.currency || 'INR'
            }
          }
        }
      },
      thumbnail: {
        url: product.image_url || `/placeholder-product-${index + 1}.jpg`
      },
      category: {
        name: product.category || 'Sourced Products'
      },
      rating: product.rating || 4.0,
      reviews: product.review_count || 50,
      brand: product.brand,
      brand_url: product.brand_url,  // Added brand store URL
      availability: product.availability,
      amazonUrl: product.product_url,
      seller_name: product.seller_name,
      seller_url: product.seller_url,  // Added seller profile URL
      seller_rating: product.seller_rating,
      seller_review_count: product.seller_review_count,
      source: 'amazon_sourcing'
    }))
    
    return NextResponse.json({
      products: transformedProducts,
      count: transformedProducts.length,
      source: 'amazon_sourcing',
      currency: 'INR',
      marketplace: 'amazon.in'
    })
    
  } catch (error) {
    console.error('❌ Error in Amazon sourcing POST:', error)
    return NextResponse.json({ error: 'Amazon sourcing service unavailable' }, { status: 500 })
  }
}