import { NextRequest, NextResponse } from 'next/server'

const SALEOR_API_URL = process.env.NEXT_PUBLIC_SALEOR_API_URL || 'http://localhost:8024/graphql/'

const PRODUCT_QUERY = `
  query Product($id: ID!) {
    product(id: $id) {
      id
      name
      slug
      description
      seoTitle
      seoDescription
      thumbnail {
        url
        alt
      }
      media {
        url
        alt
      }
      category {
        id
        name
        slug
      }
      variants {
        id
        name
        sku
        pricing {
          priceRange {
            start {
              gross {
                amount
                currency
              }
            }
          }
        }
        quantityAvailable
      }
      pricing {
        priceRange {
          start {
            gross {
              amount
              currency
            }
          }
        }
      }
      isAvailable
      availableForPurchase
    }
  }
`

async function fetchFromSaleor(query: string, variables?: any) {
  try {
    const response = await fetch(SALEOR_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        variables,
      }),
    })

    if (!response.ok) {
      throw new Error(`Saleor API error: ${response.status}`)
    }

    const data = await response.json()
    
    if (data.errors) {
      throw new Error(`GraphQL errors: ${JSON.stringify(data.errors)}`)
    }

    return data.data
  } catch (error) {
    console.error('Error fetching from Saleor:', error)
    throw error
  }
}

function transformSaleorProduct(saleorProduct: any) {
  const product = saleorProduct
  // Generate realistic ratings and reviews for demo
  const rating = 4.0 + Math.random() * 1.0 // 4.0-5.0
  const reviews = Math.floor(Math.random() * 500) + 50 // 50-550 reviews
  const price = product.pricing?.priceRange?.start?.gross?.amount || 0
  // Generate original price for sale effect (20-40% higher)
  const originalPrice = Math.random() > 0.6 ? price * (1.2 + Math.random() * 0.2) : undefined
  const isNew = Math.random() > 0.7
  const isSale = originalPrice !== undefined
  const isFeatured = Math.random() > 0.5

  return {
    id: product.id,
    name: product.name,
    slug: product.slug,
    description: product.description || product.seoDescription || '',
    price: parseFloat(price.toString()),
    originalPrice: originalPrice ? parseFloat(originalPrice.toString()) : undefined,
    image: product.thumbnail?.url || product.media?.[0]?.url || '/placeholder-product.jpg',
    images: product.media?.map((m: any) => ({ url: m.url, alt: m.alt || product.name })) || [],
    category: product.category?.name?.toLowerCase() || 'general',
    categorySlug: product.category?.slug || 'general',
    rating: parseFloat(rating.toFixed(1)),
    reviews: reviews,
    inStock: product.variants?.some((v: any) => v.quantityAvailable > 0) || product.isAvailable,
    totalStock: product.variants?.reduce((sum: number, v: any) => sum + (v.quantityAvailable || 0), 0) || 0,
    isNew,
    isSale,
    isFeatured,
    currency: product.pricing?.priceRange?.start?.gross?.currency || 'USD',
    variants: product.variants?.map((v: any) => ({
      id: v.id,
      name: v.name,
      sku: v.sku,
      price: parseFloat(v.pricing?.priceRange?.start?.gross?.amount?.toString() || '0'),
      quantityAvailable: v.quantityAvailable || 0
    })) || [],
    seoTitle: product.seoTitle,
    seoDescription: product.seoDescription,
    availableForPurchase: product.availableForPurchase
  }
}

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    // Fetch product from Saleor
    const saleorData = await fetchFromSaleor(PRODUCT_QUERY, {
      id: params.id
    })

    if (!saleorData.product) {
      return NextResponse.json(
        { error: 'Product not found' }, 
        { status: 404 }
      )
    }

    // Transform Saleor product
    const product = transformSaleorProduct(saleorData.product)

    return NextResponse.json(product)

  } catch (error) {
    console.error('Error in product API:', error)
    
    return NextResponse.json(
      { error: 'Failed to fetch product' }, 
      { status: 500 }
    )
  }
}