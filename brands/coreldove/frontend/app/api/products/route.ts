import { NextRequest, NextResponse } from 'next/server'

const SALEOR_API_URL = process.env.NEXT_PUBLIC_SALEOR_API_URL || 'http://localhost:4003/graphql/'
const AMAZON_SOURCING_URL = process.env.AMAZON_SOURCING_URL || 'http://localhost:8010'

interface SaleorProduct {
  id: string
  name: string
  description: string
  pricing: {
    priceRange: {
      start: {
        gross: {
          amount: number
          currency: string
        }
      }
    }
  }
  thumbnail: {
    url: string
  }
  category: {
    name: string
  }
  rating: number
  metadata: Array<{
    key: string
    value: string
  }>
  variants?: Array<{
    quantityAvailable: number
  }>
}

const PRODUCTS_QUERY = `
  query Products($first: Int, $filter: ProductFilterInput) {
    products(first: $first, filter: $filter) {
      edges {
        node {
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
      pageInfo {
        hasNextPage
        hasPreviousPage
        startCursor
        endCursor
      }
      totalCount
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

async function fetchFromAmazonSourcing(endpoint: string) {
  try {
    const response = await fetch(`${AMAZON_SOURCING_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`Amazon Sourcing API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Error fetching from Amazon Sourcing:', error)
    // Return fallback data if Amazon API is unavailable
    return { products: [] }
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

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  
  const category = searchParams.get('category') || undefined
  const search = searchParams.get('search') || undefined
  const sortBy = searchParams.get('sortBy') || 'RANK'
  const first = parseInt(searchParams.get('first') || '20')
  const minPrice = searchParams.get('minPrice')
  const maxPrice = searchParams.get('maxPrice')

  try {
    // Build filter object for Saleor
    const filter: any = {}
    
    if (category && category !== 'all') {
      filter.categories = [category]
    }
    
    if (search) {
      filter.search = search
    }

    if (minPrice && maxPrice) {
      filter.price = {
        gte: parseFloat(minPrice),
        lte: parseFloat(maxPrice)
      }
    }

    // Build sort object
    const sortByMap: Record<string, string> = {
      'featured': 'RANK',
      'price-low': 'PRICE',
      'price-high': '-PRICE',
      'newest': '-CREATED',
      'rating': 'RATING',
      'reviews': 'MINIMAL_PRICE'
    }

    const saleorSortBy = sortByMap[sortBy] || 'RANK'

    // Fetch products from Saleor
    const saleorData = await fetchFromSaleor(PRODUCTS_QUERY, {
      first,
      filter,
      sortBy: { field: saleorSortBy.replace('-', ''), direction: saleorSortBy.startsWith('-') ? 'DESC' : 'ASC' }
    })

    // Transform Saleor products
    const products = saleorData.products.edges.map((edge: any) => 
      transformSaleorProduct(edge.node)
    )

    // If no products from Saleor, try to get from Amazon sourcing service
    if (products.length === 0) {
      const amazonData = await fetchFromAmazonSourcing(`/products?category=${category || 'all'}&limit=${first}`)
      if (amazonData.products) {
        products.push(...amazonData.products.map((product: any) => ({
          id: product.asin || product.id,
          name: product.title || product.name,
          description: product.description || '',
          price: parseFloat(product.price || '0'),
          originalPrice: product.originalPrice ? parseFloat(product.originalPrice) : undefined,
          image: product.image || product.thumbnail || '/placeholder-product.jpg',
          category: product.category || 'general',
          rating: parseFloat(product.rating || '4.0'),
          reviews: parseInt(product.reviewCount || '0'),
          inStock: product.availability !== 'OutOfStock',
          isNew: product.isNew || false,
          isFeatured: product.isFeatured || false,
          currency: 'USD',
          source: 'amazon'
        })))
      }
    }

    return NextResponse.json({
      products,
      totalCount: saleorData.products.totalCount || products.length,
      hasNextPage: saleorData.products.edges.length === first
    })

  } catch (error) {
    console.error('Error in products API:', error)
    
    // Return fallback sample data
    const sampleProducts = [
      {
        id: 'sample-1',
        name: 'Premium Wireless Earbuds',
        description: 'High-quality sound with noise cancellation',
        price: 89.99,
        originalPrice: 129.99,
        image: '/products/earbuds.jpg',
        category: 'tech',
        rating: 4.8,
        reviews: 234,
        inStock: true,
        isNew: true,
        isFeatured: true,
        currency: 'USD'
      },
      {
        id: 'sample-2',
        name: 'Fitness Resistance Bands Set',
        description: 'Complete workout set with multiple resistance levels',
        price: 24.99,
        originalPrice: 34.99,
        image: '/products/resistance-bands.jpg',
        category: 'sports',
        rating: 4.6,
        reviews: 156,
        inStock: true,
        isFeatured: true,
        currency: 'USD'
      }
    ]

    return NextResponse.json({
      products: sampleProducts,
      totalCount: sampleProducts.length,
      hasNextPage: false,
      fallback: true
    })
  }
}