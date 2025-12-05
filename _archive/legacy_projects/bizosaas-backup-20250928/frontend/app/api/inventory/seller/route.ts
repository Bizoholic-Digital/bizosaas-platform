import { NextRequest, NextResponse } from 'next/server'
import { inventorySync } from '@/lib/inventory-sync'
import { amazonSPAPI } from '@/lib/amazon-sp-api'

// GET /api/inventory/seller - Get seller inventory from Amazon
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const nextToken = searchParams.get('nextToken') || undefined
    const page = parseInt(searchParams.get('page') || '1')
    const limit = parseInt(searchParams.get('limit') || '20')
    const category = searchParams.get('category') || undefined
    const status = searchParams.get('status') || undefined
    const search = searchParams.get('search') || undefined

    // Get inventory from Amazon
    const result = await inventorySync.getSellerInventory(nextToken)

    let filteredItems = result.items

    // Apply filters
    if (category && category !== 'all') {
      filteredItems = filteredItems.filter(item => 
        item.category.toLowerCase().includes(category.toLowerCase())
      )
    }

    if (status && status !== 'all') {
      filteredItems = filteredItems.filter(item => item.status === status)
    }

    if (search) {
      const searchLower = search.toLowerCase()
      filteredItems = filteredItems.filter(item =>
        item.title.toLowerCase().includes(searchLower) ||
        item.asin.toLowerCase().includes(searchLower) ||
        item.sellerSku.toLowerCase().includes(searchLower) ||
        (item.brand && item.brand.toLowerCase().includes(searchLower))
      )
    }

    // Paginate results
    const startIndex = (page - 1) * limit
    const endIndex = startIndex + limit
    const paginatedItems = filteredItems.slice(startIndex, endIndex)

    // Calculate summary statistics
    const summary = {
      totalProducts: filteredItems.length,
      totalValue: filteredItems.reduce((sum, item) => sum + (item.price * item.quantity), 0),
      totalQuantity: filteredItems.reduce((sum, item) => sum + item.quantity, 0),
      averagePrice: filteredItems.length > 0 ? 
        filteredItems.reduce((sum, item) => sum + item.price, 0) / filteredItems.length : 0,
      byStatus: {
        active: filteredItems.filter(item => item.status === 'active').length,
        inactive: filteredItems.filter(item => item.status === 'inactive').length,
        incomplete: filteredItems.filter(item => item.status === 'incomplete').length
      },
      byFulfillment: {
        FBA: filteredItems.filter(item => item.fulfillmentChannel === 'FBA').length,
        FBM: filteredItems.filter(item => item.fulfillmentChannel === 'FBM').length
      },
      lowStock: filteredItems.filter(item => item.quantity <= 10 && item.quantity > 0).length,
      outOfStock: filteredItems.filter(item => item.quantity === 0).length
    }

    return NextResponse.json({
      success: true,
      data: {
        items: paginatedItems,
        pagination: {
          page,
          limit,
          total: filteredItems.length,
          pages: Math.ceil(filteredItems.length / limit),
          hasNext: endIndex < filteredItems.length,
          hasPrev: page > 1
        },
        summary,
        nextToken: result.nextToken
      }
    })

  } catch (error) {
    console.error('Seller inventory API error:', error)
    return NextResponse.json(
      { 
        error: 'Failed to get seller inventory',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}