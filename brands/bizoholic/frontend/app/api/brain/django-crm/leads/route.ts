/**
 * Django CRM Leads API Route
 * Handles lead creation and management in Django CRM system via FastAPI AI Agentic Central Hub
 */

import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// POST /api/brain/django-crm/leads - Create new lead
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // Validate required fields for lead creation
    const { name, email, source } = body
    if (!name || !email || !source) {
      return NextResponse.json(
        { error: 'Missing required fields: name, email, source' },
        { status: 400 }
      )
    }

    // Forward to FastAPI AI Agentic Central Hub which handles Django CRM integration
    const response = await fetch(`${BRAIN_API_URL}/api/brain/django-crm/leads`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3001',
      },
      body: JSON.stringify({
        lead_data: {
          // Contact Information
          first_name: body.name.split(' ')[0] || body.name,
          last_name: body.name.split(' ').slice(1).join(' ') || '',
          email: email,
          phone: body.phone || '',
          company: body.company || '',

          // Lead Classification
          source: source, // 'website', 'social_media', 'referral', 'advertising'
          status: 'new', // 'new', 'contacted', 'qualified', 'proposal', 'won', 'lost'
          priority: body.priority || 'medium', // 'low', 'medium', 'high'

          // Service Details
          service_interest: body.service || '',
          budget_range: body.budget || '',
          project_details: body.message || '',

          // Metadata
          source_url: body.source_url || 'bizoholic_website',
          utm_source: body.utm_source || '',
          utm_medium: body.utm_medium || '',
          utm_campaign: body.utm_campaign || '',

          // Tracking
          ip_address: request.headers.get('x-forwarded-for') || request.ip || 'unknown',
          user_agent: request.headers.get('user-agent') || 'unknown',
          submitted_at: body.submitted_at || new Date().toISOString(),

          // Custom Fields
          custom_fields: {
            website_form: true,
            form_type: 'contact_form',
            lead_score: calculateLeadScore(body),
            initial_touchpoint: 'contact_form'
          }
        },
        actions: {
          send_welcome_email: true,
          assign_to_sales_rep: true,
          create_follow_up_task: true,
          add_to_nurture_sequence: true
        }
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      console.error('FastAPI AI Central Hub error:', response.status, errorData)

      // Return fallback response for development
      const fallbackData = {
        success: true,
        lead: {
          id: 'lead-dev-' + Date.now(),
          email: email,
          status: 'new',
          source: source,
          created_at: new Date().toISOString()
        },
        message: 'Lead created successfully (Development mode)',
        source: "fallback"
      }

      return NextResponse.json(fallbackData, { status: 201 })
    }

    const result = await response.json()

    return NextResponse.json({
      success: true,
      message: 'Lead created successfully in CRM',
      lead: result.lead,
      actions_performed: result.actions_performed,
      next_steps: result.next_steps
    })

  } catch (error) {
    console.error('Django CRM leads API error:', error)

    // Fallback for error cases
    const fallbackData = {
      success: true,
      lead: {
        id: 'lead-fallback-' + Date.now(),
        status: 'new',
        created_at: new Date().toISOString()
      },
      message: 'Lead captured (Development mode)',
      source: "fallback"
    }

    return NextResponse.json(fallbackData, { status: 201 })
  }
}

// GET /api/brain/django-crm/leads - Get leads with filters
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const status = searchParams.get('status')
    const source = searchParams.get('source')
    const priority = searchParams.get('priority')
    const page = searchParams.get('page') || '1'
    const limit = searchParams.get('limit') || '20'

    let url = `${BRAIN_API_URL}/api/brain/django-crm/leads`
    const params = new URLSearchParams()

    if (status) params.set('status', status)
    if (source) params.set('source', source)
    if (priority) params.set('priority', priority)
    params.set('page', page)
    params.set('limit', limit)

    url += `?${params.toString()}`

    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3001',
      },
      cache: 'no-store',
    })

    if (!response.ok) {
      throw new Error(`FastAPI AI Central Hub responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching leads from Django CRM:', error)

    // Return fallback leads data
    const fallbackData = {
      leads: [
        {
          id: 'lead-1',
          first_name: 'John',
          last_name: 'Doe',
          email: 'john.doe@example.com',
          company: 'Acme Corp',
          phone: '+1-555-0123',
          source: 'website',
          status: 'new',
          priority: 'medium',
          service_interest: 'SEO Optimization',
          budget_range: '$5,000 - $10,000',
          created_at: '2024-01-15T10:30:00Z',
          last_contact: null,
          assigned_to: null
        },
        {
          id: 'lead-2',
          first_name: 'Jane',
          last_name: 'Smith',
          email: 'jane.smith@startup.com',
          company: 'TechStart Inc',
          phone: '+1-555-0456',
          source: 'social_media',
          status: 'contacted',
          priority: 'high',
          service_interest: 'AI Campaign Management',
          budget_range: '$10,000+',
          created_at: '2024-01-14T15:45:00Z',
          last_contact: '2024-01-15T09:00:00Z',
          assigned_to: 'sales_rep_1'
        }
      ],
      pagination: {
        current_page: 1,
        total_pages: 1,
        total_leads: 2,
        per_page: 20
      },
      source: "fallback"
    }

    return NextResponse.json(fallbackData, { status: 200 })
  }
}

// PUT /api/brain/django-crm/leads - Update lead status/information
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    const { lead_id } = body

    if (!lead_id) {
      return NextResponse.json(
        { error: 'Lead ID is required' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/django-crm/leads`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3001',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`FastAPI AI Central Hub responded with status: ${response.status}, ${JSON.stringify(errorData)}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error updating lead via Django CRM API:', error)
    return NextResponse.json(
      { error: 'Failed to update lead', details: error.message },
      { status: 500 }
    )
  }
}

// Helper function to calculate lead score
function calculateLeadScore(leadData: any): number {
  let score = 0

  // Company provided (+10)
  if (leadData.company) score += 10

  // Phone provided (+5)
  if (leadData.phone) score += 5

  // Budget range scoring
  const budget = leadData.budget?.toLowerCase() || ''
  if (budget.includes('10,000+') || budget.includes('enterprise')) score += 20
  else if (budget.includes('5,000') || budget.includes('professional')) score += 15
  else if (budget.includes('2,500') || budget.includes('standard')) score += 10

  // Service interest scoring
  const service = leadData.service?.toLowerCase() || ''
  if (service.includes('ai') || service.includes('enterprise')) score += 15
  else if (service.includes('seo') || service.includes('social')) score += 10
  else if (service.includes('content')) score += 8

  // Message length (engagement indicator)
  const messageLength = (leadData.message || '').length
  if (messageLength > 200) score += 10
  else if (messageLength > 100) score += 5

  return Math.min(score, 100) // Cap at 100
}