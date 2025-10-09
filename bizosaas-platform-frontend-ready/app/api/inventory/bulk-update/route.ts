import { NextRequest, NextResponse } from 'next/server'
import { inventorySync } from '@/lib/inventory-sync'
import { BulkInventoryUpdate } from '@/lib/amazon-sp-api'

// POST /api/inventory/bulk-update - Bulk update inventory
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { updates, dryRun = false } = body

    // Validate updates
    if (!Array.isArray(updates) || updates.length === 0) {
      return NextResponse.json(
        { error: 'Updates array is required' },
        { status: 400 }
      )
    }

    // Validate each update
    const validUpdates: BulkInventoryUpdate[] = []
    const validationErrors: string[] = []

    for (let i = 0; i < updates.length; i++) {
      const update = updates[i]
      
      if (!update.asin) {
        validationErrors.push(`Update ${i}: ASIN is required`)
        continue
      }

      if (update.quantity !== undefined && (typeof update.quantity !== 'number' || update.quantity < 0)) {
        validationErrors.push(`Update ${i}: Quantity must be a non-negative number`)
        continue
      }

      if (update.price !== undefined && (typeof update.price !== 'number' || update.price <= 0)) {
        validationErrors.push(`Update ${i}: Price must be a positive number`)
        continue
      }

      if (update.status && !['active', 'inactive'].includes(update.status)) {
        validationErrors.push(`Update ${i}: Status must be 'active' or 'inactive'`)
        continue
      }

      if (update.fulfillmentChannel && !['FBM', 'FBA'].includes(update.fulfillmentChannel)) {
        validationErrors.push(`Update ${i}: FulfillmentChannel must be 'FBM' or 'FBA'`)
        continue
      }

      validUpdates.push(update)
    }

    if (validationErrors.length > 0) {
      return NextResponse.json(
        { 
          error: 'Validation errors',
          validationErrors,
          validUpdates: validUpdates.length,
          totalUpdates: updates.length
        },
        { status: 400 }
      )
    }

    // If dry run, return what would be updated
    if (dryRun) {
      return NextResponse.json({
        success: true,
        dryRun: true,
        validUpdates: validUpdates.length,
        updates: validUpdates.map(update => ({
          asin: update.asin,
          changes: {
            ...(update.quantity !== undefined && { quantity: update.quantity }),
            ...(update.price !== undefined && { price: update.price }),
            ...(update.status && { status: update.status }),
            ...(update.fulfillmentChannel && { fulfillmentChannel: update.fulfillmentChannel })
          }
        }))
      })
    }

    // Perform bulk update
    const result = await inventorySync.bulkUpdateInventory(validUpdates)

    return NextResponse.json({
      success: result.failed === 0,
      result: {
        totalUpdates: validUpdates.length,
        successful: result.success,
        failed: result.failed,
        errors: result.errors
      },
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('Bulk update API error:', error)
    return NextResponse.json(
      { 
        error: 'Failed to perform bulk update',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}