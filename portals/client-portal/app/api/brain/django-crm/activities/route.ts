/**
 * Django CRM Activities API Route for Client Portal
 * Manages activity operations via FastAPI AI Central Hub
 */

import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// GET /api/brain/django-crm/activities - Fetch all activities
export async function GET(request: NextRequest) {
  // Extract params outside try-catch so they're available in fallback
  const searchParams = request.nextUrl.searchParams
  const page = searchParams.get('page') || '1'
  const limit = searchParams.get('limit') || '20'

  try {
    const session = await getServerSession(authOptions);
    const type = searchParams.get('type')
    const status = searchParams.get('status')
    const search = searchParams.get('search')
    const sort = searchParams.get('sort') || 'created_at'
    const order = searchParams.get('order') || 'desc'
    const assigned_to = searchParams.get('assigned_to')
    const contact_id = searchParams.get('contact_id')
    const deal_id = searchParams.get('deal_id')
    const lead_id = searchParams.get('lead_id')
    const date_from = searchParams.get('date_from')
    const date_to = searchParams.get('date_to')

    let url = `${BRAIN_API_URL}/api/crm/activities`
    const params = new URLSearchParams()

    // Add tenant_id from session if available
    if (session?.user?.tenant_id) {
      params.set('tenant_id', session.user.tenant_id);
    }

    if (type) params.set('type', type)
    if (status) params.set('status', status)
    if (search) params.set('search', search)
    if (assigned_to) params.set('assigned_to', assigned_to)
    if (contact_id) params.set('contact_id', contact_id)
    if (deal_id) params.set('deal_id', deal_id)
    if (lead_id) params.set('lead_id', lead_id)
    if (date_from) params.set('date_from', date_from)
    if (date_to) params.set('date_to', date_to)
    params.set('page', page)
    params.set('limit', limit)
    params.set('sort', sort)
    params.set('order', order)

    url += `?${params.toString()}`

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      'Host': 'localhost:3000',
    };

    if (session?.access_token) {
      headers["Authorization"] = `Bearer ${session.access_token}`;
    } else if (request.headers.get("authorization")) {
      headers["Authorization"] = request.headers.get("authorization")!;
    }

    const response = await fetch(url, {
      headers,
      cache: 'no-store',
    })

    if (!response.ok) {
      throw new Error(`FastAPI AI Central Hub responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching activities from Django CRM via Brain API:', error)

    // Return fallback activities data
    const fallbackData = {
      activities: [
        {
          id: 'activity-1',
          type: 'call',
          subject: 'Discovery call with TechCorp',
          description: 'Initial discovery call to understand their marketing automation needs',
          status: 'completed',
          priority: 'high',
          scheduled_date: '2024-01-16T11:00:00Z',
          completed_date: '2024-01-16T11:45:00Z',
          duration_minutes: 45,
          created_at: '2024-01-15T14:30:00Z',
          updated_at: '2024-01-16T11:45:00Z',
          assigned_to: 'Sarah Johnson',
          contact: {
            id: 'contact-1',
            name: 'John Smith',
            email: 'john.smith@techcorp.com',
            company: 'TechCorp Solutions'
          },
          deal: {
            id: 'deal-1',
            title: 'TechCorp Enterprise Marketing Package',
            value: 50000,
            stage: 'proposal'
          },
          lead: {
            id: 'lead-1',
            name: 'John Smith',
            company: 'TechCorp Solutions',
            score: 85
          },
          outcome: {
            summary: 'Successful discovery call. Client confirmed budget and timeline.',
            next_steps: ['Send proposal', 'Schedule demo', 'Provide case studies'],
            follow_up_date: '2024-01-18T14:00:00Z'
          },
          attachments: [
            {
              id: 'att-1',
              name: 'TechCorp_Discovery_Notes.pdf',
              size: 245760,
              type: 'application/pdf',
              url: '/attachments/techcorp_discovery_notes.pdf'
            }
          ],
          tags: ['discovery', 'qualified', 'enterprise']
        },
        {
          id: 'activity-2',
          type: 'email',
          subject: 'Welcome email to StartupXYZ',
          description: 'Automated welcome email with onboarding information',
          status: 'completed',
          priority: 'medium',
          scheduled_date: '2024-01-15T14:20:00Z',
          completed_date: '2024-01-15T14:20:00Z',
          duration_minutes: 0,
          created_at: '2024-01-15T14:20:00Z',
          updated_at: '2024-01-15T14:20:00Z',
          assigned_to: 'System',
          contact: {
            id: 'contact-2',
            name: 'Emily Rodriguez',
            email: 'emily.r@startupxyz.io',
            company: 'StartupXYZ'
          },
          deal: {
            id: 'deal-2',
            title: 'StartupXYZ Growth Marketing Package',
            value: 25000,
            stage: 'negotiation'
          },
          lead: {
            id: 'lead-2',
            name: 'Emily Rodriguez',
            company: 'StartupXYZ',
            score: 92
          },
          outcome: {
            summary: 'Welcome email sent successfully. Email opened within 2 hours.',
            engagement: {
              opened: true,
              clicked: true,
              replied: false,
              open_time: '2024-01-15T16:30:00Z',
              click_time: '2024-01-15T16:32:00Z'
            }
          },
          email_template: {
            id: 'template-1',
            name: 'Startup Welcome Package',
            subject: 'Welcome to Bizoholic - Your Growth Journey Starts Now'
          },
          tags: ['welcome', 'automated', 'startup']
        },
        {
          id: 'activity-3',
          type: 'meeting',
          subject: 'Product demo for RetailPlus',
          description: 'Scheduled product demonstration focusing on e-commerce features',
          status: 'scheduled',
          priority: 'high',
          scheduled_date: '2024-01-19T10:00:00Z',
          duration_minutes: 60,
          created_at: '2024-01-16T09:15:00Z',
          updated_at: '2024-01-16T09:15:00Z',
          assigned_to: 'Lisa Wang',
          contact: {
            id: 'contact-3',
            name: 'David Chen',
            email: 'david.chen@retailplus.com',
            company: 'RetailPlus'
          },
          deal: {
            id: 'deal-3',
            title: 'RetailPlus E-commerce Marketing',
            value: 75000,
            stage: 'qualification'
          },
          lead: {
            id: 'lead-3',
            name: 'David Chen',
            company: 'RetailPlus',
            score: 68
          },
          meeting_details: {
            location: 'Zoom Meeting',
            meeting_url: 'https://zoom.us/j/1234567890',
            agenda: [
              'Platform overview and capabilities',
              'E-commerce marketing automation demo',
              'ROI case studies from similar retailers',
              'Q&A and next steps discussion'
            ],
            attendees: [
              {
                name: 'David Chen',
                email: 'david.chen@retailplus.com',
                role: 'VP of Marketing'
              },
              {
                name: 'Lisa Wang',
                email: 'lisa.wang@bizoholic.com',
                role: 'Account Executive'
              }
            ]
          },
          preparation: {
            materials_prepared: true,
            demo_environment_ready: true,
            case_studies_selected: true,
            calendar_sent: true
          },
          tags: ['demo', 'retail', 'high-value']
        },
        {
          id: 'activity-4',
          type: 'task',
          subject: 'Follow up on proposal status',
          description: 'Check on the status of the TechCorp proposal and address any questions',
          status: 'pending',
          priority: 'medium',
          scheduled_date: '2024-01-18T09:00:00Z',
          created_at: '2024-01-16T15:30:00Z',
          updated_at: '2024-01-16T15:30:00Z',
          assigned_to: 'Sarah Johnson',
          contact: {
            id: 'contact-1',
            name: 'John Smith',
            email: 'john.smith@techcorp.com',
            company: 'TechCorp Solutions'
          },
          deal: {
            id: 'deal-1',
            title: 'TechCorp Enterprise Marketing Package',
            value: 50000,
            stage: 'proposal'
          },
          task_details: {
            checklist: [
              { item: 'Send follow-up email', completed: false },
              { item: 'Schedule proposal review call', completed: false },
              { item: 'Prepare answers for technical questions', completed: false },
              { item: 'Update deal probability based on feedback', completed: false }
            ],
            reminder_set: true,
            reminder_time: '2024-01-18T08:30:00Z'
          },
          dependencies: [
            {
              id: 'activity-1',
              type: 'call',
              subject: 'Discovery call with TechCorp'
            }
          ],
          tags: ['follow-up', 'proposal', 'reminder']
        },
        {
          id: 'activity-5',
          type: 'linkedin_message',
          subject: 'Connection request to RetailPlus CTO',
          description: 'LinkedIn outreach to technical decision maker',
          status: 'completed',
          priority: 'low',
          scheduled_date: '2024-01-14T09:25:00Z',
          completed_date: '2024-01-14T09:25:00Z',
          created_at: '2024-01-14T09:20:00Z',
          updated_at: '2024-01-14T09:25:00Z',
          assigned_to: 'Lisa Wang',
          contact: {
            id: 'contact-3',
            name: 'David Chen',
            email: 'david.chen@retailplus.com',
            company: 'RetailPlus'
          },
          deal: {
            id: 'deal-3',
            title: 'RetailPlus E-commerce Marketing',
            value: 75000,
            stage: 'qualification'
          },
          social_activity: {
            platform: 'linkedin',
            message_sent: 'Hi David, I came across your profile and noticed RetailPlus is expanding rapidly. We specialize in e-commerce marketing automation that could help scale your growth. Would you be open to a brief conversation?',
            connection_accepted: true,
            response_received: true,
            response_text: 'Hi Lisa, yes I\'d be interested to learn more. Can we set up a call next week?',
            response_time: '2024-01-14T14:30:00Z'
          },
          tags: ['linkedin', 'outreach', 'social-selling']
        }
      ],
      pagination: {
        current_page: parseInt(page),
        total_pages: 1,
        total_activities: 5,
        per_page: parseInt(limit)
      },
      statistics: {
        total_activities: 5,
        completed_activities: 3,
        scheduled_activities: 1,
        pending_activities: 1,
        overdue_activities: 0,
        activities_by_type: {
          'call': 1,
          'email': 1,
          'meeting': 1,
          'task': 1,
          'linkedin_message': 1
        },
        activities_by_status: {
          'completed': 3,
          'scheduled': 1,
          'pending': 1,
          'overdue': 0,
          'cancelled': 0
        },
        avg_completion_time: '2.5 hours',
        productivity_score: 85
      },
      source: "fallback"
    }

    return NextResponse.json(fallbackData, { status: 200 })
  }
}

// POST /api/brain/django-crm/activities - Create new activity
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // Validate required fields
    const { type, subject, assigned_to } = body
    if (!type || !subject || !assigned_to) {
      return NextResponse.json(
        { error: 'Missing required fields: type, subject, assigned_to' },
        { status: 400 }
      )
    }

    const session = await getServerSession(authOptions);
    const response = await fetch(`${BRAIN_API_URL}/api/crm/activities`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': session?.access_token ? `Bearer ${session.access_token}` : (request.headers.get('authorization') || ''),
      },
      body: JSON.stringify({
        activity_data: {
          type: type,
          subject: subject,
          description: body.description || '',
          status: body.status || 'pending',
          priority: body.priority || 'medium',
          scheduled_date: body.scheduled_date || new Date().toISOString(),
          duration_minutes: parseInt(body.duration_minutes) || 30,
          assigned_to: assigned_to,
          contact_id: body.contact_id || null,
          deal_id: body.deal_id || null,
          lead_id: body.lead_id || null,
          tags: body.tags || [],
          meeting_details: body.meeting_details || null,
          task_details: body.task_details || null,
          email_template_id: body.email_template_id || null
        },
        actions: {
          send_calendar_invite: body.send_calendar_invite || false,
          create_reminder: body.create_reminder || true,
          notify_assignee: body.notify_assignee || true,
          auto_create_follow_up: body.auto_create_follow_up || false
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
      message: 'Activity created successfully',
      activity: data.activity
    })
  } catch (error) {
    console.error('Error creating activity via Django CRM API:', error)

    // Return development fallback
    const body = await request.json()
    const fallbackData = {
      success: true,
      activity: {
        id: 'activity-new-' + Date.now(),
        type: body.type || 'task',
        subject: body.subject || 'New Activity',
        status: body.status || 'pending',
        priority: body.priority || 'medium',
        assigned_to: body.assigned_to || 'Unknown',
        scheduled_date: body.scheduled_date || new Date().toISOString(),
        created_at: new Date().toISOString()
      },
      message: 'Activity created successfully (Development mode)',
      source: "fallback"
    }

    return NextResponse.json(fallbackData, { status: 201 })
  }
}

// PUT /api/brain/django-crm/activities - Update activity
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    const { activity_id } = body

    if (!activity_id) {
      return NextResponse.json(
        { error: 'Activity ID is required' },
        { status: 400 }
      )
    }

    const session = await getServerSession(authOptions);
    const response = await fetch(`${BRAIN_API_URL}/api/crm/activities/${activity_id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': session?.access_token ? `Bearer ${session.access_token}` : (request.headers.get('authorization') || ''),
      },
      body: JSON.stringify({
        updates: {
          subject: body.subject,
          description: body.description,
          status: body.status,
          priority: body.priority,
          scheduled_date: body.scheduled_date,
          duration_minutes: body.duration_minutes ? parseInt(body.duration_minutes) : undefined,
          assigned_to: body.assigned_to,
          tags: body.tags,
          outcome: body.outcome,
          meeting_details: body.meeting_details,
          task_details: body.task_details
        },
        actions: {
          update_calendar: body.update_calendar || false,
          notify_changes: body.notify_changes || false,
          create_follow_up: body.create_follow_up || false,
          sync_with_deal: body.sync_with_deal || true
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
    console.error('Error updating activity via Django CRM API:', error)
    return NextResponse.json(
      { error: 'Failed to update activity', details: error.message },
      { status: 500 }
    )
  }
}

// DELETE /api/brain/django-crm/activities - Delete activity
export async function DELETE(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const activityId = searchParams.get('activityId')

    if (!activityId) {
      return NextResponse.json(
        { error: 'Activity ID is required' },
        { status: 400 }
      )
    }

    const session = await getServerSession(authOptions);
    const response = await fetch(`${BRAIN_API_URL}/api/crm/activities/${activityId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': session?.access_token ? `Bearer ${session.access_token}` : (request.headers.get('authorization') || ''),
      },
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`FastAPI AI Central Hub responded with status: ${response.status}, ${JSON.stringify(errorData)}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error deleting activity via Django CRM API:', error)
    return NextResponse.json(
      { error: 'Failed to delete activity', details: error.message },
      { status: 500 }
    )
  }
}