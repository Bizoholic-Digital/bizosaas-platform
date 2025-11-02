/**
 * Analytics Dashboards API Route for Client Portal
 * Manages analytics dashboards via FastAPI AI Central Hub
 */

import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// GET /api/brain/analytics/dashboards - Fetch dashboard data
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const dashboard_type = searchParams.get('dashboard_type') || 'overview'
  const period = searchParams.get('period') || '30d'
  
  try {
    const client_id = searchParams.get('client_id')
    const metrics = searchParams.get('metrics')
    
    let url = `${BRAIN_API_URL}/api/brain/analytics/dashboards`
    const params = new URLSearchParams()
    
    params.set('dashboard_type', dashboard_type)
    params.set('period', period)
    if (client_id) params.set('client_id', client_id)
    if (metrics) params.set('metrics', metrics)
    
    url += `?${params.toString()}`

    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      cache: 'no-store',
    })

    if (!response.ok) {
      throw new Error(`FastAPI AI Central Hub responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching analytics dashboards from Analytics API via Brain API:', error)
    
    // Return fallback dashboard data
    const fallbackData = {
      dashboard: {
        type: dashboard_type || 'overview',
        period: period || '30d',
        generated_at: new Date().toISOString(),
        widgets: [
          {
            id: 'widget-revenue',
            type: 'metric_card',
            title: 'Total Revenue',
            value: '$45,231',
            change: '+12.5%',
            change_type: 'positive',
            period_comparison: 'vs last 30 days',
            icon: 'dollar-sign',
            color: 'green'
          },
          {
            id: 'widget-customers',
            type: 'metric_card',
            title: 'Active Customers',
            value: '1,234',
            change: '+8.2%',
            change_type: 'positive',
            period_comparison: 'vs last 30 days',
            icon: 'users',
            color: 'blue'
          },
          {
            id: 'widget-orders',
            type: 'metric_card',
            title: 'Total Orders',
            value: '156',
            change: '-2.1%',
            change_type: 'negative',
            period_comparison: 'vs last 30 days',
            icon: 'shopping-cart',
            color: 'purple'
          },
          {
            id: 'widget-conversion',
            type: 'metric_card',
            title: 'Conversion Rate',
            value: '3.4%',
            change: '+0.5%',
            change_type: 'positive',
            period_comparison: 'vs last 30 days',
            icon: 'trending-up',
            color: 'orange'
          },
          {
            id: 'widget-revenue-chart',
            type: 'line_chart',
            title: 'Revenue Trend (Last 30 Days)',
            data: {
              labels: [
                '2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05',
                '2024-01-06', '2024-01-07', '2024-01-08', '2024-01-09', '2024-01-10',
                '2024-01-11', '2024-01-12', '2024-01-13', '2024-01-14', '2024-01-15',
                '2024-01-16'
              ],
              datasets: [
                {
                  label: 'Daily Revenue',
                  data: [1200, 1350, 1100, 1450, 1600, 1400, 1750, 1500, 1650, 1800, 1950, 1700, 1850, 2000, 1900, 2100],
                  color: '#10B981'
                }
              ]
            },
            height: 300
          },
          {
            id: 'widget-traffic-sources',
            type: 'pie_chart',
            title: 'Traffic Sources',
            data: {
              labels: ['Organic Search', 'Direct', 'Social Media', 'Email', 'Referrals', 'Paid Ads'],
              datasets: [
                {
                  data: [35, 25, 15, 12, 8, 5],
                  colors: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4']
                }
              ]
            },
            height: 300
          },
          {
            id: 'widget-top-products',
            type: 'table',
            title: 'Top Selling Products',
            data: {
              headers: ['Product', 'Sales', 'Revenue', 'Growth'],
              rows: [
                ['Premium Plan', '45 sales', '$4,500', '+15%'],
                ['Professional Plan', '89 sales', '$7,120', '+8%'],
                ['Starter Plan', '156 sales', '$4,680', '+22%'],
                ['Enterprise Plan', '12 sales', '$12,000', '+5%'],
                ['Add-on Services', '78 sales', '$3,900', '+18%']
              ]
            },
            height: 250
          },
          {
            id: 'widget-customer-growth',
            type: 'area_chart',
            title: 'Customer Growth',
            data: {
              labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
              datasets: [
                {
                  label: 'New Customers',
                  data: [65, 75, 85, 95, 110, 125, 135, 145, 160, 175, 185, 200],
                  color: '#3B82F6'
                },
                {
                  label: 'Total Customers',
                  data: [250, 325, 410, 505, 615, 740, 875, 1020, 1180, 1355, 1540, 1740],
                  color: '#10B981'
                }
              ]
            },
            height: 300
          }
        ]
      },
      filters: {
        available_periods: ['7d', '30d', '90d', '1y', 'custom'],
        available_metrics: ['revenue', 'customers', 'orders', 'conversion', 'traffic', 'engagement'],
        available_breakdowns: ['daily', 'weekly', 'monthly', 'quarterly']
      },
      metadata: {
        last_updated: new Date().toISOString(),
        data_freshness: '5 minutes ago',
        total_records: 15234,
        data_sources: ['CRM', 'E-commerce', 'Marketing', 'Billing']
      },
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 200 })
  }
}

// POST /api/brain/analytics/dashboards - Create custom dashboard
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Validate required fields
    const { name, widgets } = body
    if (!name || !widgets) {
      return NextResponse.json(
        { error: 'Missing required fields: name, widgets' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/analytics/dashboards`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify({
        dashboard: {
          name: name,
          description: body.description || '',
          widgets: widgets,
          layout: body.layout || 'grid',
          permissions: body.permissions || 'private',
          tags: body.tags || []
        },
        actions: {
          auto_refresh: body.auto_refresh || false,
          sharing_enabled: body.sharing_enabled || false,
          export_enabled: body.export_enabled || true
        }
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`FastAPI AI Central Hub responded with status: ${response.status}, ${JSON.stringify(errorData)}`)
    }

    const data = await response.json()
    return NextResponse.json({
      success: true,
      message: 'Dashboard created successfully',
      dashboard: data.dashboard
    })
  } catch (error) {
    console.error('Error creating dashboard via Analytics API:', error)
    
    // Return development fallback
    const body = await request.json()
    const fallbackData = {
      success: true,
      dashboard: {
        id: 'dashboard-new-' + Date.now(),
        name: body.name || 'New Dashboard',
        description: body.description || '',
        widgets: body.widgets || [],
        created_at: new Date().toISOString()
      },
      message: 'Dashboard created successfully (Development mode)',
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 201 })
  }
}

// PUT /api/brain/analytics/dashboards - Update dashboard
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    const { dashboard_id } = body
    
    if (!dashboard_id) {
      return NextResponse.json(
        { error: 'Dashboard ID is required' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/analytics/dashboards/${dashboard_id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify({
        updates: {
          name: body.name,
          description: body.description,
          widgets: body.widgets,
          layout: body.layout,
          permissions: body.permissions,
          tags: body.tags
        },
        actions: {
          refresh_data: body.refresh_data || false,
          notify_subscribers: body.notify_subscribers || false
        }
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`FastAPI AI Central Hub responded with status: ${response.status}, ${JSON.stringify(errorData)}`)
    }

    const data = await response.json()
    return NextResponse.json({
      success: true,
      message: 'Dashboard updated successfully',
      dashboard: data.dashboard
    })
  } catch (error) {
    console.error('Error updating dashboard via Analytics API:', error)
    
    return NextResponse.json({
      success: true,
      message: 'Dashboard updated successfully (Development mode)',
      source: "fallback"
    }, { status: 200 })
  }
}

// DELETE /api/brain/analytics/dashboards - Delete dashboard
export async function DELETE(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const dashboardId = searchParams.get('dashboardId')
    
    if (!dashboardId) {
      return NextResponse.json(
        { error: 'Dashboard ID is required' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/analytics/dashboards/${dashboardId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`FastAPI AI Central Hub responded with status: ${response.status}, ${JSON.stringify(errorData)}`)
    }

    return NextResponse.json({
      success: true,
      message: 'Dashboard deleted successfully'
    })
  } catch (error) {
    console.error('Error deleting dashboard via Analytics API:', error)
    
    return NextResponse.json({
      success: true,
      message: 'Dashboard deleted successfully (Development mode)',
      source: "fallback"
    }, { status: 200 })
  }
}