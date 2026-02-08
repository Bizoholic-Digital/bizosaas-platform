import { NextRequest, NextResponse } from 'next/server'
import { inventorySync } from '@/lib/inventory-sync'
import { headers } from 'next/headers'

// POST /api/inventory/sync - Start inventory sync
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { 
      type = 'full',
      filters = {},
      platforms = [],
      asins = []
    } = body

    // Validate request
    if (type === 'single_product' && !asins.length) {
      return NextResponse.json(
        { error: 'ASIN required for single product sync' },
        { status: 400 }
      )
    }

    // Start sync job
    const job = await inventorySync.syncAllProducts({
      asins: asins.length > 0 ? asins : undefined,
      platforms: platforms.length > 0 ? platforms : undefined,
      categories: filters.categories
    })

    return NextResponse.json({
      success: true,
      job: {
        id: job.id,
        type: job.type,
        status: job.status,
        progress: job.progress,
        startedAt: job.startedAt
      }
    })

  } catch (error) {
    console.error('Sync API error:', error)
    return NextResponse.json(
      { error: 'Failed to start sync' },
      { status: 500 }
    )
  }
}

// GET /api/inventory/sync - Get sync jobs
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const jobId = searchParams.get('jobId')

    if (jobId) {
      // Get specific job
      const job = inventorySync.getSyncJob(jobId)
      if (!job) {
        return NextResponse.json(
          { error: 'Job not found' },
          { status: 404 }
        )
      }

      return NextResponse.json({ job })
    } else {
      // Get all jobs
      const jobs = inventorySync.getAllSyncJobs()
      return NextResponse.json({ jobs })
    }

  } catch (error) {
    console.error('Sync status API error:', error)
    return NextResponse.json(
      { error: 'Failed to get sync status' },
      { status: 500 }
    )
  }
}