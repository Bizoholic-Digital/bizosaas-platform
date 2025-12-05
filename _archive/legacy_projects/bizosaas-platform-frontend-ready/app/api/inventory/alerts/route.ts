import { NextRequest, NextResponse } from 'next/server'
import { inventorySync } from '@/lib/inventory-sync'

// GET /api/inventory/alerts - Get inventory alerts
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const type = searchParams.get('type') || undefined
    const priority = searchParams.get('priority') || undefined
    const resolved = searchParams.get('resolved') ? searchParams.get('resolved') === 'true' : undefined
    const page = parseInt(searchParams.get('page') || '1')
    const limit = parseInt(searchParams.get('limit') || '20')

    // Get alerts with filters
    const allAlerts = inventorySync.getAlerts({ type, priority, resolved })

    // Paginate results
    const startIndex = (page - 1) * limit
    const endIndex = startIndex + limit
    const paginatedAlerts = allAlerts.slice(startIndex, endIndex)

    // Calculate summary
    const summary = {
      total: allAlerts.length,
      unresolved: allAlerts.filter(alert => !alert.isResolved).length,
      byType: {
        low_stock: allAlerts.filter(alert => alert.type === 'low_stock').length,
        out_of_stock: allAlerts.filter(alert => alert.type === 'out_of_stock').length,
        sync_conflict: allAlerts.filter(alert => alert.type === 'sync_conflict').length,
        price_variance: allAlerts.filter(alert => alert.type === 'price_variance').length,
        sync_error: allAlerts.filter(alert => alert.type === 'sync_error').length
      },
      byPriority: {
        critical: allAlerts.filter(alert => alert.priority === 'critical').length,
        high: allAlerts.filter(alert => alert.priority === 'high').length,
        medium: allAlerts.filter(alert => alert.priority === 'medium').length,
        low: allAlerts.filter(alert => alert.priority === 'low').length
      }
    }

    return NextResponse.json({
      success: true,
      data: {
        alerts: paginatedAlerts,
        pagination: {
          page,
          limit,
          total: allAlerts.length,
          pages: Math.ceil(allAlerts.length / limit),
          hasNext: endIndex < allAlerts.length,
          hasPrev: page > 1
        },
        summary
      }
    })

  } catch (error) {
    console.error('Alerts API error:', error)
    return NextResponse.json(
      { error: 'Failed to get alerts' },
      { status: 500 }
    )
  }
}

// PATCH /api/inventory/alerts - Resolve alert
export async function PATCH(request: NextRequest) {
  try {
    const body = await request.json()
    const { alertId, action = 'resolve' } = body

    if (!alertId) {
      return NextResponse.json(
        { error: 'Alert ID is required' },
        { status: 400 }
      )
    }

    let success = false

    switch (action) {
      case 'resolve':
        success = inventorySync.resolveAlert(alertId)
        break
      default:
        return NextResponse.json(
          { error: 'Invalid action' },
          { status: 400 }
        )
    }

    if (!success) {
      return NextResponse.json(
        { error: 'Alert not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      success: true,
      message: `Alert ${action}d successfully`
    })

  } catch (error) {
    console.error('Alert action API error:', error)
    return NextResponse.json(
      { error: 'Failed to process alert action' },
      { status: 500 }
    )
  }
}