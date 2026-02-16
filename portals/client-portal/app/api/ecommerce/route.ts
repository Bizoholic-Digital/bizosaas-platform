/**
 * E-commerce API Route for Client Portal
 * Manages e-commerce dashboard data and operations
 */

import { NextRequest, NextResponse } from 'next/server'

// Mock e-commerce data for demo
const mockEcommerceData = {
  overview: {
    total_sales: 45678.90,
    sales_today: 1234.56,
    orders_count: 127,
    orders_today: 8,
    average_order_value: 359.68,
    conversion_rate: 3.2,
    abandoned_carts: 23,
    refunds: 890.45,
    profit_margin: 24.5,
    top_selling_product: 'Marketing Automation Pro'
  },
  recent_orders: [
    {
      id: 'order_001',
      order_number: 'BZO-2024-001',
      customer: {
        name: 'John Smith',
        email: 'john.smith@techcorp.com'
      },
      status: 'completed',
      payment_status: 'paid',
      total: 599.00,
      currency: 'USD',
      items_count: 2,
      created_at: '2024-09-25T14:20:00Z',
      products: [
        {
          name: 'Marketing Automation Pro',
          quantity: 1,
          price: 499.00
        },
        {
          name: 'SEO Optimization Add-on',
          quantity: 1,
          price: 100.00
        }
      ]
    },
    {
      id: 'order_002',
      order_number: 'BZO-2024-002',
      customer: {
        name: 'Emily Rodriguez',
        email: 'emily.r@startupxyz.io'
      },
      status: 'processing',
      payment_status: 'paid',
      total: 299.00,
      currency: 'USD',
      items_count: 1,
      created_at: '2024-09-25T13:45:00Z',
      products: [
        {
          name: 'Startup Growth Package',
          quantity: 1,
          price: 299.00
        }
      ]
    },
    {
      id: 'order_003',
      order_number: 'BZO-2024-003',
      customer: {
        name: 'David Chen',
        email: 'david.chen@retailplus.com'
      },
      status: 'pending',
      payment_status: 'pending',
      total: 899.00,
      currency: 'USD',
      items_count: 3,
      created_at: '2024-09-25T12:30:00Z',
      products: [
        {
          name: 'E-commerce Marketing Suite',
          quantity: 1,
          price: 699.00
        },
        {
          name: 'Analytics Dashboard Pro',
          quantity: 1,
          price: 149.00
        },
        {
          name: 'Custom Integration Setup',
          quantity: 1,
          price: 51.00
        }
      ]
    }
  ],
  products: [
    {
      id: 'product_001',
      name: 'Marketing Automation Pro',
      description: 'Complete marketing automation suite with AI-powered insights',
      price: 499.00,
      compare_at_price: 699.00,
      currency: 'USD',
      sku: 'MAP-PRO-001',
      stock_quantity: 0, // Digital product - unlimited
      status: 'active',
      category: 'Software',
      tags: ['marketing', 'automation', 'pro'],
      sales_count: 45,
      revenue: 22455.00,
      rating: 4.8,
      reviews_count: 23,
      created_at: '2024-08-01T10:00:00Z',
      updated_at: '2024-09-20T15:30:00Z'
    },
    {
      id: 'product_002',
      name: 'Startup Growth Package',
      description: 'Essential marketing tools for growing startups',
      price: 299.00,
      compare_at_price: 399.00,
      currency: 'USD',
      sku: 'SGP-BASIC-001',
      stock_quantity: 0, // Digital product - unlimited
      status: 'active',
      category: 'Software',
      tags: ['startup', 'growth', 'basic'],
      sales_count: 67,
      revenue: 20033.00,
      rating: 4.6,
      reviews_count: 34,
      created_at: '2024-08-15T12:00:00Z',
      updated_at: '2024-09-18T14:20:00Z'
    },
    {
      id: 'product_003',
      name: 'E-commerce Marketing Suite',
      description: 'Specialized marketing tools for e-commerce businesses',
      price: 699.00,
      compare_at_price: 899.00,
      currency: 'USD',
      sku: 'EMS-ECOM-001',
      stock_quantity: 0, // Digital product - unlimited
      status: 'active',
      category: 'Software',
      tags: ['ecommerce', 'marketing', 'suite'],
      sales_count: 23,
      revenue: 16077.00,
      rating: 4.9,
      reviews_count: 18,
      created_at: '2024-09-01T09:30:00Z',
      updated_at: '2024-09-22T11:45:00Z'
    },
    {
      id: 'product_004',
      name: 'SEO Optimization Add-on',
      description: 'Advanced SEO tools and optimization services',
      price: 100.00,
      compare_at_price: 150.00,
      currency: 'USD',
      sku: 'SEO-ADDON-001',
      stock_quantity: 0, // Digital service - unlimited
      status: 'active',
      category: 'Services',
      tags: ['seo', 'optimization', 'addon'],
      sales_count: 89,
      revenue: 8900.00,
      rating: 4.7,
      reviews_count: 45,
      created_at: '2024-07-20T14:15:00Z',
      updated_at: '2024-09-23T16:10:00Z'
    }
  ],
  customers: [
    {
      id: 'customer_001',
      name: 'John Smith',
      email: 'john.smith@techcorp.com',
      phone: '+1-555-0123',
      company: 'TechCorp Solutions',
      orders_count: 3,
      total_spent: 1497.00,
      average_order_value: 499.00,
      status: 'active',
      created_at: '2024-08-15T10:30:00Z',
      last_order_date: '2024-09-25T14:20:00Z',
      lifetime_value: 1800.00,
      tags: ['enterprise', 'high-value']
    },
    {
      id: 'customer_002',
      name: 'Emily Rodriguez',
      email: 'emily.r@startupxyz.io',
      phone: '+1-555-0456',
      company: 'StartupXYZ',
      orders_count: 2,
      total_spent: 598.00,
      average_order_value: 299.00,
      status: 'active',
      created_at: '2024-09-10T14:20:00Z',
      last_order_date: '2024-09-25T13:45:00Z',
      lifetime_value: 750.00,
      tags: ['startup', 'growth-stage']
    }
  ],
  analytics: {
    sales_by_month: [
      { month: 'Jan', sales: 32500, orders: 89 },
      { month: 'Feb', sales: 28900, orders: 76 },
      { month: 'Mar', sales: 35600, orders: 98 },
      { month: 'Apr', sales: 42300, orders: 112 },
      { month: 'May', sales: 39800, orders: 105 },
      { month: 'Jun', sales: 45200, orders: 123 },
      { month: 'Jul', sales: 41600, orders: 117 },
      { month: 'Aug', sales: 48900, orders: 134 },
      { month: 'Sep', sales: 45678, orders: 127 }
    ],
    top_products_by_revenue: [
      { name: 'Marketing Automation Pro', revenue: 22455.00, sales: 45 },
      { name: 'Startup Growth Package', revenue: 20033.00, sales: 67 },
      { name: 'E-commerce Marketing Suite', revenue: 16077.00, sales: 23 },
      { name: 'SEO Optimization Add-on', revenue: 8900.00, sales: 89 }
    ],
    conversion_funnel: {
      visitors: 12456,
      product_views: 3421,
      cart_additions: 567,
      checkouts_started: 234,
      orders_completed: 127,
      conversion_rate: 1.02
    },
    payment_methods: {
      'Credit Card': 78.3,
      'PayPal': 15.7,
      'Bank Transfer': 4.2,
      'Other': 1.8
    }
  },
  integrations: {
    shopify: {
      enabled: true,
      status: 'connected',
      store_url: 'bizosaas-demo.myshopify.com',
      last_sync: '2024-09-25T14:00:00Z',
      products_synced: 24,
      orders_synced: 127
    },
    woocommerce: {
      enabled: false,
      status: 'disconnected',
      store_url: null,
      last_sync: null
    },
    stripe: {
      enabled: true,
      status: 'connected',
      account_id: 'acct_1234567890',
      last_sync: '2024-09-25T14:15:00Z',
      webhooks_active: true
    },
    paypal: {
      enabled: true,
      status: 'connected',
      merchant_id: 'PAYPAL123456',
      last_sync: '2024-09-25T14:10:00Z'
    }
  }
}

// GET /api/ecommerce - Fetch e-commerce dashboard data
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const section = searchParams.get('section') || 'overview'
    const dateRange = searchParams.get('dateRange') || '30d'
    const page = parseInt(searchParams.get('page') || '1')
    const limit = parseInt(searchParams.get('limit') || '20')

    console.log('[CLIENT-PORTAL] GET e-commerce data', { section, dateRange, page, limit })

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 300))

    let responseData: any = {}

    switch (section) {
      case 'overview':
        responseData = {
          overview: mockEcommerceData.overview,
          recent_orders: mockEcommerceData.recent_orders.slice(0, 5),
          analytics: mockEcommerceData.analytics
        }
        break

      case 'orders':
        const startIndex = (page - 1) * limit
        responseData = {
          orders: mockEcommerceData.recent_orders.slice(startIndex, startIndex + limit),
          pagination: {
            current_page: page,
            total_pages: Math.ceil(mockEcommerceData.recent_orders.length / limit),
            total_orders: mockEcommerceData.recent_orders.length,
            per_page: limit
          }
        }
        break

      case 'products':
        const productStartIndex = (page - 1) * limit
        responseData = {
          products: mockEcommerceData.products.slice(productStartIndex, productStartIndex + limit),
          pagination: {
            current_page: page,
            total_pages: Math.ceil(mockEcommerceData.products.length / limit),
            total_products: mockEcommerceData.products.length,
            per_page: limit
          }
        }
        break

      case 'customers':
        responseData = {
          customers: mockEcommerceData.customers,
          customer_stats: {
            total_customers: mockEcommerceData.customers.length,
            active_customers: mockEcommerceData.customers.filter(c => c.status === 'active').length,
            average_ltv: mockEcommerceData.customers.reduce((sum, c) => sum + c.lifetime_value, 0) / mockEcommerceData.customers.length
          }
        }
        break

      case 'integrations':
        responseData = {
          integrations: mockEcommerceData.integrations
        }
        break

      default:
        responseData = mockEcommerceData
    }

    return NextResponse.json({
      success: true,
      data: responseData,
      section,
      date_range: dateRange,
      last_updated: new Date().toISOString(),
      source: "fallback"
    })
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error('Error fetching e-commerce data:', errorMessage);
    return NextResponse.json(
      { error: 'Failed to fetch e-commerce data', details: errorMessage },
      { status: 500 }
    );
  }
}

// POST /api/ecommerce - Create new order or product
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { action, data } = body

    console.log(`[CLIENT-PORTAL] POST e-commerce action: ${action}`)

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 500))

    if (action === 'create_order') {
      const newOrder = {
        id: 'order_' + Date.now(),
        order_number: 'BZO-2024-' + String(Date.now()).slice(-3),
        customer: data.customer,
        status: 'pending',
        payment_status: 'pending',
        total: data.total || 0,
        currency: 'USD',
        items_count: data.products?.length || 0,
        created_at: new Date().toISOString(),
        products: data.products || []
      }

      return NextResponse.json({
        success: true,
        message: 'Order created successfully',
        order: newOrder,
        source: "fallback"
      })
    }

    if (action === 'create_product') {
      const newProduct = {
        id: 'product_' + Date.now(),
        name: data.name || 'New Product',
        description: data.description || '',
        price: parseFloat(data.price) || 0,
        currency: 'USD',
        sku: data.sku || 'SKU-' + Date.now(),
        status: 'draft',
        category: data.category || 'General',
        tags: data.tags || [],
        created_at: new Date().toISOString()
      }

      return NextResponse.json({
        success: true,
        message: 'Product created successfully',
        product: newProduct,
        source: "fallback"
      })
    }

    return NextResponse.json({
      success: true,
      message: 'Action completed successfully',
      source: "fallback"
    })
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error('Error creating e-commerce item:', errorMessage);
    return NextResponse.json(
      { error: 'Failed to create item', details: errorMessage },
      { status: 500 }
    );
  }
}

// PUT /api/ecommerce - Update order or product
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    const { type, id, updates } = body

    console.log(`[CLIENT-PORTAL] PUT update ${type}: ${id}`)

    if (!type || !id) {
      return NextResponse.json(
        { error: 'Type and ID are required' },
        { status: 400 }
      )
    }

    // Simulate update delay
    await new Promise(resolve => setTimeout(resolve, 400))

    return NextResponse.json({
      success: true,
      message: `${type} updated successfully`,
      id,
      updates_applied: Object.keys(updates),
      updated_at: new Date().toISOString(),
      source: "fallback"
    })
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error('Error updating e-commerce item:', errorMessage);
    return NextResponse.json(
      { error: 'Failed to update item', details: errorMessage },
      { status: 500 }
    );
  }
}

// DELETE /api/ecommerce - Delete order or product
export async function DELETE(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const type = searchParams.get('type')
    const id = searchParams.get('id')

    console.log(`[CLIENT-PORTAL] DELETE ${type}: ${id}`)

    if (!type || !id) {
      return NextResponse.json(
        { error: 'Type and ID are required' },
        { status: 400 }
      )
    }

    // Simulate deletion delay
    await new Promise(resolve => setTimeout(resolve, 350))

    return NextResponse.json({
      success: true,
      message: `${type} deleted successfully`,
      id,
      deleted_at: new Date().toISOString(),
      source: "fallback"
    })
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error('Error deleting e-commerce item:', errorMessage);
    return NextResponse.json(
      { error: 'Failed to delete item', details: errorMessage },
      { status: 500 }
    );
  }
}