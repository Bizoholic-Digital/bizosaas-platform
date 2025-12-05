import { NextRequest, NextResponse } from 'next/server'
import { inventorySync } from '@/lib/inventory-sync'

// GET /api/inventory/export - Export inventory data
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const format = (searchParams.get('format') as 'csv' | 'json') || 'csv'

    // Export inventory data
    const data = await inventorySync.exportInventoryData(format)

    // Set appropriate content type and headers
    const contentType = format === 'json' ? 'application/json' : 'text/csv'
    const filename = `inventory_export_${new Date().toISOString().split('T')[0]}.${format}`

    return new NextResponse(data, {
      headers: {
        'Content-Type': contentType,
        'Content-Disposition': `attachment; filename="${filename}"`,
        'Cache-Control': 'no-cache'
      }
    })

  } catch (error) {
    console.error('Export API error:', error)
    return NextResponse.json(
      { error: 'Failed to export inventory data' },
      { status: 500 }
    )
  }
}