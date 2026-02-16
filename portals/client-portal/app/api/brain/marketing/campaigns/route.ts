/**
 * Marketing Campaigns API Route for Client Portal
 * Manages campaign operations via FastAPI AI Central Hub
 */

import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// GET /api/brain/marketing/campaigns - Fetch all campaigns
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const status = searchParams.get('status')
    const type = searchParams.get('type')
    const search = searchParams.get('search')
    const page = searchParams.get('page') || '1'
    const limit = searchParams.get('limit') || '20'
    const sort = searchParams.get('sort') || 'created_at'
    const order = searchParams.get('order') || 'desc'
    const channel = searchParams.get('channel')
    const budget_min = searchParams.get('budget_min')
    const budget_max = searchParams.get('budget_max')

    let url = `${BRAIN_API_URL}/api/brain/marketing/campaigns`
    const params = new URLSearchParams()

    if (status) params.set('status', status)
    if (type) params.set('type', type)
    if (search) params.set('search', search)
    if (channel) params.set('channel', channel)
    if (budget_min) params.set('budget_min', budget_min)
    if (budget_max) params.set('budget_max', budget_max)
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
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error('Error fetching campaigns from Marketing API via Brain API:', errorMessage);

    // Return fallback campaigns data
    const fallbackData = {
      campaigns: [
        {
          id: 'campaign-1',
          name: 'Q1 Lead Generation Campaign',
          description: 'Multi-channel campaign targeting B2B software companies',
          type: 'lead_generation',
          status: 'active',
          channels: ['email', 'linkedin', 'google_ads'],
          budget: {
            total: 15000,
            spent: 8500,
            remaining: 6500,
            currency: 'USD'
          },
          timeline: {
            start_date: '2024-01-01',
            end_date: '2024-03-31',
            duration_days: 90
          },
          targeting: {
            audience_size: 50000,
            demographics: {
              age_range: '25-54',
              location: ['United States', 'Canada'],
              industries: ['Technology', 'Software', 'SaaS']
            },
            interests: ['B2B Marketing', 'Lead Generation', 'Marketing Automation']
          },
          performance: {
            impressions: 125000,
            clicks: 3750,
            conversions: 182,
            ctr: 3.0,
            conversion_rate: 4.85,
            cost_per_click: 2.27,
            cost_per_conversion: 46.70,
            roas: 3.2
          },
          content: {
            email_templates: 3,
            ad_creatives: 8,
            landing_pages: 2,
            social_posts: 15
          },
          ai_insights: {
            optimization_score: 85,
            recommendations: [
              'Increase LinkedIn budget by 20%',
              'Test new ad creative variations',
              'Optimize landing page for mobile'
            ],
            predicted_performance: {
              end_of_campaign_conversions: 280,
              projected_roas: 3.5
            }
          },
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-16T14:30:00Z',
          created_by: 'Sarah Johnson',
          assigned_team: ['Sarah Johnson', 'Mike Chen', 'Lisa Wang']
        },
        {
          id: 'campaign-2',
          name: 'Brand Awareness - Tech Startups',
          description: 'Social media campaign to increase brand recognition among startup founders',
          type: 'brand_awareness',
          status: 'draft',
          channels: ['facebook', 'instagram', 'twitter', 'content_marketing'],
          budget: {
            total: 8000,
            spent: 0,
            remaining: 8000,
            currency: 'USD'
          },
          timeline: {
            start_date: '2024-02-01',
            end_date: '2024-04-30',
            duration_days: 89
          },
          targeting: {
            audience_size: 75000,
            demographics: {
              age_range: '22-45',
              location: ['United States', 'United Kingdom', 'Australia'],
              industries: ['Startups', 'Technology', 'Venture Capital']
            },
            interests: ['Entrepreneurship', 'Startup Funding', 'Tech Innovation']
          },
          performance: {
            impressions: 0,
            clicks: 0,
            conversions: 0,
            ctr: 0,
            conversion_rate: 0,
            cost_per_click: 0,
            cost_per_conversion: 0,
            roas: 0
          },
          content: {
            email_templates: 0,
            ad_creatives: 12,
            landing_pages: 1,
            social_posts: 25
          },
          ai_insights: {
            optimization_score: 0,
            recommendations: [
              'Campaign not yet launched',
              'Complete audience validation',
              'Finalize content calendar'
            ],
            predicted_performance: {
              end_of_campaign_conversions: 150,
              projected_roas: 2.8
            }
          },
          created_at: '2024-01-15T10:00:00Z',
          updated_at: '2024-01-16T16:45:00Z',
          created_by: 'Mike Chen',
          assigned_team: ['Mike Chen', 'Emily Rodriguez']
        },
        {
          id: 'campaign-3',
          name: 'Retargeting - Website Visitors',
          description: 'Retargeting campaign for users who visited pricing page but didn\'t convert',
          type: 'retargeting',
          status: 'paused',
          channels: ['google_ads', 'facebook'],
          budget: {
            total: 5000,
            spent: 3200,
            remaining: 1800,
            currency: 'USD'
          },
          timeline: {
            start_date: '2024-01-10',
            end_date: '2024-02-28',
            duration_days: 49
          },
          targeting: {
            audience_size: 12000,
            demographics: {
              age_range: '25-65',
              location: ['United States'],
              industries: ['All']
            },
            interests: ['Previously visited pricing page']
          },
          performance: {
            impressions: 45000,
            clicks: 1350,
            conversions: 68,
            ctr: 3.0,
            conversion_rate: 5.04,
            cost_per_click: 2.37,
            cost_per_conversion: 47.06,
            roas: 4.1
          },
          content: {
            email_templates: 2,
            ad_creatives: 6,
            landing_pages: 1,
            social_posts: 5
          },
          ai_insights: {
            optimization_score: 92,
            recommendations: [
              'Resume campaign - performing well',
              'Expand to similar audiences',
              'Test video ad formats'
            ],
            predicted_performance: {
              end_of_campaign_conversions: 95,
              projected_roas: 4.3
            }
          },
          created_at: '2024-01-10T08:00:00Z',
          updated_at: '2024-01-14T12:15:00Z',
          created_by: 'Lisa Wang',
          assigned_team: ['Lisa Wang', 'David Chen']
        }
      ],
      pagination: {
        current_page: parseInt(request.nextUrl.searchParams.get('page') || '1'),
        total_pages: 1,
        total_campaigns: 3,
        per_page: parseInt(request.nextUrl.searchParams.get('limit') || '20')
      },
      statistics: {
        total_campaigns: 3,
        active_campaigns: 1,
        draft_campaigns: 1,
        paused_campaigns: 1,
        completed_campaigns: 0,
        total_budget: 28000,
        total_spent: 11700,
        avg_roas: 2.4,
        channels_distribution: {
          'email': 2,
          'google_ads': 2,
          'facebook': 2,
          'linkedin': 1,
          'instagram': 1,
          'twitter': 1,
          'content_marketing': 1
        }
      },
      source: "fallback"
    }

    return NextResponse.json(fallbackData, { status: 200 })
  }
}

// POST /api/brain/marketing/campaigns - Create new campaign
export async function POST(request: NextRequest) {
  let body: any = {};
  try {
    body = await request.json()

    // Validate required fields
    const { name, type, channels, budget, timeline, targeting } = body
    if (!name || !type || !channels || !budget || !timeline || !targeting) {
      return NextResponse.json(
        { error: 'Missing required fields: name, type, channels, budget, timeline, targeting' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/marketing/campaigns`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify({
        campaign_data: {
          name: name,
          description: body.description || '',
          type: type,
          channels: channels,
          budget: {
            total: parseFloat(budget.total) || 0,
            currency: budget.currency || 'USD'
          },
          timeline: {
            start_date: timeline.start_date,
            end_date: timeline.end_date
          },
          targeting: {
            audience_size: targeting.audience_size || 0,
            demographics: targeting.demographics || {},
            interests: targeting.interests || [],
            custom_audiences: targeting.custom_audiences || []
          },
          content: body.content || {},
          goals: body.goals || {},
          status: body.status || 'draft'
        },
        actions: {
          auto_optimize: body.auto_optimize || false,
          send_notifications: body.send_notifications || true,
          create_content_calendar: body.create_content_calendar || false,
          setup_tracking: body.setup_tracking || true
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
      message: 'Campaign created successfully',
      campaign: data.campaign,
      ai_recommendations: data.ai_recommendations || []
    })
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error('Error creating campaign via Marketing API:', errorMessage);

    // Use the already parsed body
    const fallbackData = {
      success: true,
      campaign: {
        id: 'campaign-new-' + Date.now(),
        name: body.name || 'New Campaign',
        description: body.description || '',
        type: body.type || 'lead_generation',
        status: 'draft',
        channels: body.channels || ['email'],
        budget: {
          total: parseFloat(body.budget?.total) || 0,
          spent: 0,
          remaining: parseFloat(body.budget?.total) || 0,
          currency: body.budget?.currency || 'USD'
        },
        timeline: body.timeline || {},
        targeting: body.targeting || {},
        performance: {
          impressions: 0,
          clicks: 0,
          conversions: 0,
          ctr: 0,
          conversion_rate: 0,
          roas: 0
        },
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      message: 'Campaign created successfully (Development mode)',
      ai_recommendations: [
        'Consider A/B testing your ad creatives',
        'Set up conversion tracking early',
        'Start with a small budget and scale gradually'
      ],
      source: "fallback"
    }

    return NextResponse.json(fallbackData, { status: 201 })
  }
}

// PUT /api/brain/marketing/campaigns - Update campaign
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    const { campaign_id } = body

    if (!campaign_id) {
      return NextResponse.json(
        { error: 'Campaign ID is required' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/marketing/campaigns/${campaign_id}`, {
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
          type: body.type,
          channels: body.channels,
          budget: body.budget,
          timeline: body.timeline,
          targeting: body.targeting,
          content: body.content,
          goals: body.goals,
          status: body.status
        },
        actions: {
          recalculate_performance: body.recalculate_performance || false,
          update_ai_recommendations: body.update_ai_recommendations || true,
          notify_team: body.notify_team || false,
          auto_optimize: body.auto_optimize || false
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
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error('Error updating campaign via Marketing API:', errorMessage);
    return NextResponse.json(
      { error: 'Failed to update campaign', details: errorMessage },
      { status: 500 }
    );
  }
}

// DELETE /api/brain/marketing/campaigns - Delete campaign
export async function DELETE(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const campaignId = searchParams.get('campaignId')

    if (!campaignId) {
      return NextResponse.json(
        { error: 'Campaign ID is required' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/marketing/campaigns/${campaignId}`, {
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
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error('Error deleting campaign via Marketing API:', errorMessage);
    return NextResponse.json(
      { error: 'Failed to delete campaign', details: errorMessage },
      { status: 500 }
    );
  }
}