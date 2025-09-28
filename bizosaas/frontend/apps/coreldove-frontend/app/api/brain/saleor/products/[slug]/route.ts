import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://bizosaas-brain-unified:8001'

export async function GET(
  request: NextRequest,
  { params }: { params: { slug: string } }
) {
  try {
    const productSlug = params.slug
    
    // Forward the request to the Brain API
    const brainApiUrl = `${BRAIN_API_URL}/api/brain/saleor/products/${productSlug}`
    console.log('🔍 Calling Brain API for product:', brainApiUrl)
    
    const response = await fetch(brainApiUrl, {
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3002',
      },
      cache: 'no-store',
    })

    if (!response.ok) {
      throw new Error(`Brain API responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching product from Brain API:', error)
    
    // Return fallback product data
    const productSlug = params.slug
    const fallbackProduct = {
      product: {
        id: `fallback-${productSlug}`,
        name: productSlug.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        slug: productSlug,
        description: `This is a premium ${productSlug.replace(/-/g, ' ')} product with excellent features and quality construction.`,
        seoTitle: `${productSlug.replace(/-/g, ' ')} | Premium Quality`,
        seoDescription: `Buy high-quality ${productSlug.replace(/-/g, ' ')} online. Fast shipping and great customer service.`,
        images: [
          {
            id: '1',
            url: '/placeholder-product.jpg',
            alt: `${productSlug.replace(/-/g, ' ')} main image`
          }
        ],
        variants: [
          {
            id: 'variant-1',
            name: 'Standard',
            sku: `${productSlug.toUpperCase()}-STD`,
            pricing: {
              price: {
                gross: {
                  amount: 2999,
                  currency: 'INR'
                }
              }
            },
            quantityAvailable: 10
          }
        ],
        category: {
          id: 'electronics',
          name: 'Electronics',
          slug: 'electronics'
        },
        collections: [],
        attributes: [
          {
            attribute: {
              name: 'Brand',
              slug: 'brand'
            },
            values: [
              {
                name: 'Premium Brand',
                slug: 'premium-brand'
              }
            ]
          },
          {
            attribute: {
              name: 'Warranty',
              slug: 'warranty'
            },
            values: [
              {
                name: '1 Year',
                slug: '1-year'
              }
            ]
          }
        ],
        rating: 4.5,
        reviews: 128,
        isAvailable: true,
        isPublished: true,
        availableForPurchase: true
      },
      source: 'fallback'
    }
    
    return NextResponse.json(fallbackProduct)
  }
}