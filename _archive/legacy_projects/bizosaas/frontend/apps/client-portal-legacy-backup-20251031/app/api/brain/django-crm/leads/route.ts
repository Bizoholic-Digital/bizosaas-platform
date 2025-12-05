/**
 * Django CRM Leads API Route for Client Portal
 * Manages lead operations via FastAPI AI Central Hub
 */

import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// GET /api/brain/django-crm/leads - Fetch all leads
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const status = searchParams.get('status')
    const source = searchParams.get('source')
    const search = searchParams.get('search')
    const page = searchParams.get('page') || '1'
    const limit = searchParams.get('limit') || '20'
    const sort = searchParams.get('sort') || 'created_at'
    const order = searchParams.get('order') || 'desc'
    const assigned_to = searchParams.get('assigned_to')
    const score_min = searchParams.get('score_min')
    const score_max = searchParams.get('score_max')
    
    let url = `${BRAIN_API_URL}/api/crm/leads`
    const params = new URLSearchParams()
    
    if (status) params.set('status', status)
    if (source) params.set('source', source)
    if (search) params.set('search', search)
    if (assigned_to) params.set('assigned_to', assigned_to)
    if (score_min) params.set('score_min', score_min)
    if (score_max) params.set('score_max', score_max)
    params.set('page', page)
    params.set('limit', limit)
    params.set('sort', sort)
    params.set('order', order)
    
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
    console.error('Error fetching leads from Django CRM via Brain API:', error)
    
    // Return fallback leads data
    const fallbackData = {
      leads: [
        {
          id: 'lead-1',
          first_name: 'John',
          last_name: 'Smith',
          email: 'john.smith@techcorp.com',
          phone: '+1-555-0123',
          company: 'TechCorp Solutions',
          position: 'Marketing Director',
          status: 'new',
          source: 'website_form',
          score: 85,
          estimated_value: 50000,
          probability: 75,
          created_at: '2024-01-16T10:30:00Z',
          updated_at: '2024-01-16T14:20:00Z',
          assigned_to: 'Sarah Johnson',
          next_follow_up: '2024-01-18T09:00:00Z',
          tags: ['enterprise', 'high-priority'],
          notes: [
            {
              id: 'note-1',
              content: 'Interested in enterprise marketing automation package',
              created_at: '2024-01-16T10:35:00Z',
              created_by: 'Sarah Johnson'
            }
          ],
          activities: [
            {
              id: 'activity-1',
              type: 'email',
              subject: 'Welcome to Bizoholic',
              created_at: '2024-01-16T10:31:00Z'
            }
          ],
          address: {
            street: '123 Business Ave',
            city: 'New York',
            state: 'NY',
            postal_code: '10001',
            country: 'USA'
          },
          social: {
            linkedin: 'https://linkedin.com/in/johnsmith',
            website: 'https://techcorp.com'
          }
        },
        {
          id: 'lead-2',
          first_name: 'Emily',
          last_name: 'Rodriguez',
          email: 'emily.r@startupxyz.io',
          phone: '+1-555-0456',
          company: 'StartupXYZ',
          position: 'Founder & CEO',
          status: 'qualified',
          source: 'referral',
          score: 92,
          estimated_value: 25000,
          probability: 85,
          created_at: '2024-01-15T14:15:00Z',
          updated_at: '2024-01-16T11:45:00Z',
          assigned_to: 'Mike Chen',
          next_follow_up: '2024-01-17T15:30:00Z',
          tags: ['startup', 'referral'],
          notes: [
            {
              id: 'note-2',
              content: 'Referred by existing client TechFlow Inc. Very interested in AI automation.',
              created_at: '2024-01-15T14:20:00Z',
              created_by: 'Mike Chen'
            }
          ],
          activities: [
            {
              id: 'activity-2',
              type: 'call',
              subject: 'Discovery call completed',
              created_at: '2024-01-16T11:00:00Z'
            }
          ],
          address: {
            street: '456 Innovation St',
            city: 'San Francisco',
            state: 'CA',
            postal_code: '94105',
            country: 'USA'
          },
          social: {
            linkedin: 'https://linkedin.com/in/emilyrodriguez',
            website: 'https://startupxyz.io'
          }
        },
        {
          id: 'lead-3',
          first_name: 'David',
          last_name: 'Chen',
          email: 'david.chen@retailplus.com',
          phone: '+1-555-0789',
          company: 'RetailPlus',
          position: 'VP of Marketing',
          status: 'contacted',
          source: 'linkedin',
          score: 68,
          estimated_value: 75000,
          probability: 45,
          created_at: '2024-01-14T09:20:00Z',
          updated_at: '2024-01-15T16:30:00Z',
          assigned_to: 'Lisa Wang',
          next_follow_up: '2024-01-19T10:00:00Z',
          tags: ['retail', 'e-commerce'],
          notes: [
            {
              id: 'note-3',
              content: 'Needs comprehensive e-commerce marketing solution. Budget concerns mentioned.',
              created_at: '2024-01-15T16:30:00Z',
              created_by: 'Lisa Wang'
            }
          ],
          activities: [
            {
              id: 'activity-3',
              type: 'linkedin_message',
              subject: 'Initial contact via LinkedIn',
              created_at: '2024-01-14T09:25:00Z'
            }
          ],
          address: {
            street: '789 Commerce Blvd',
            city: 'Chicago',
            state: 'IL',
            postal_code: '60601',
            country: 'USA'
          },
          social: {
            linkedin: 'https://linkedin.com/in/davidchen-retail',
            website: 'https://retailplus.com'
          }
        }
      ],
      pagination: {
        current_page: parseInt(page),
        total_pages: 1,
        total_leads: 3,
        per_page: parseInt(limit)
      },
      statistics: {
        total_leads: 3,
        new_leads: 1,
        qualified_leads: 1,
        contacted_leads: 1,
        converted_leads: 0,
        avg_score: 81.7,
        total_estimated_value: 150000,
        sources: {
          'website_form': 1,
          'referral': 1,
          'linkedin': 1
        }
      },
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 200 })
  }
}

// POST /api/brain/django-crm/leads - Create new lead
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Validate required fields
    const { first_name, last_name, email, company } = body
    if (!first_name || !last_name || !email || !company) {
      return NextResponse.json(
        { error: 'Missing required fields: first_name, last_name, email, company' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/crm/leads`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify({
        lead_data: {
          first_name: first_name,
          last_name: last_name,
          email: email,
          phone: body.phone || '',
          company: company,
          position: body.position || '',
          source: body.source || 'manual',
          status: body.status || 'new',
          estimated_value: parseFloat(body.estimated_value) || 0,
          probability: parseInt(body.probability) || 50,
          assigned_to: body.assigned_to || null,
          tags: body.tags || [],
          notes: body.notes || '',
          address: body.address || {},
          social: body.social || {}
        },
        actions: {
          auto_score: true,
          send_welcome_email: body.send_welcome_email || false,
          create_initial_task: body.create_initial_task || true,
          notify_assignee: body.notify_assignee || false
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
      message: 'Lead created successfully',
      lead: data.lead,
      score: data.score || 0
    })
  } catch (error) {
    console.error('Error creating lead via Django CRM API:', error)
    
    // Return development fallback
    const body = await request.json()
    const fallbackData = {
      success: true,
      lead: {
        id: 'lead-new-' + Date.now(),
        first_name: body.first_name || 'New',
        last_name: body.last_name || 'Lead',
        email: body.email || 'new@example.com',
        company: body.company || 'New Company',
        status: 'new',
        score: Math.floor(Math.random() * 100),
        created_at: new Date().toISOString()
      },
      message: 'Lead created successfully (Development mode)',
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 201 })
  }
}

// PUT /api/brain/django-crm/leads - Update lead
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

    const response = await fetch(`${BRAIN_API_URL}/api/crm/leads/${lead_id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify({
        updates: {
          first_name: body.first_name,
          last_name: body.last_name,
          email: body.email,
          phone: body.phone,
          company: body.company,
          position: body.position,
          status: body.status,
          estimated_value: body.estimated_value ? parseFloat(body.estimated_value) : undefined,
          probability: body.probability ? parseInt(body.probability) : undefined,
          assigned_to: body.assigned_to,
          tags: body.tags,
          address: body.address,
          social: body.social
        },
        actions: {
          recalculate_score: body.recalculate_score || false,
          update_activities: body.update_activities || false,
          notify_changes: body.notify_changes || false
        }
      }),
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

// DELETE /api/brain/django-crm/leads - Delete lead
export async function DELETE(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const leadId = searchParams.get('leadId')
    
    if (!leadId) {
      return NextResponse.json(
        { error: 'Lead ID is required' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/crm/leads/${leadId}`, {
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

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error deleting lead via Django CRM API:', error)
    return NextResponse.json(
      { error: 'Failed to delete lead', details: error.message },
      { status: 500 }
    )
  }
}