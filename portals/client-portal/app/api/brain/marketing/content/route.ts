/**
 * Marketing Content API Route for Client Portal
 * Manages content templates and AI-generated content via FastAPI AI Central Hub
 */

import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000'

// GET /api/brain/marketing/content - Fetch content templates and suggestions
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const type = searchParams.get('type') // 'email', 'ad', 'social', 'landing_page'
    const campaign_type = searchParams.get('campaign_type')
    const industry = searchParams.get('industry')
    const audience = searchParams.get('audience')
    const tone = searchParams.get('tone')

    let url = `${BRAIN_API_URL}/api/brain/marketing/content`
    const params = new URLSearchParams()

    if (type) params.set('type', type)
    if (campaign_type) params.set('campaign_type', campaign_type)
    if (industry) params.set('industry', industry)
    if (audience) params.set('audience', audience)
    if (tone) params.set('tone', tone)

    url += `?${params.toString()}`

    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
      cache: 'no-store',
    })

    if (!response.ok) {
      console.error(`FastAPI AI Central Hub responded with status: ${response.status}`);
      return NextResponse.json(
        { error: 'Failed to fetch marketing content' },
        { status: response.status }
      );
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching content from Marketing API via Brain API:', error)
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

// POST /api/brain/marketing/content - Generate AI content
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // Validate required fields
    const { content_type, prompt, target_audience } = body
    if (!content_type || !prompt || !target_audience) {
      return NextResponse.json(
        { error: 'Missing required fields: content_type, prompt, target_audience' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/marketing/content/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
      body: JSON.stringify({
        generation_request: {
          content_type: content_type,
          prompt: prompt,
          target_audience: target_audience,
          tone: body.tone || 'professional',
          length: body.length || 'medium',
          industry: body.industry || 'technology',
          platform: body.platform || 'email',
          campaign_goal: body.campaign_goal || 'lead_generation'
        },
        options: {
          include_variations: body.include_variations || true,
          optimize_for_engagement: body.optimize_for_engagement || true,
          include_hashtags: body.include_hashtags || false,
          personalization_level: body.personalization_level || 'medium'
        }
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      console.error(`FastAPI AI Central Hub responded with status: ${response.status}`, errorData);
      return NextResponse.json(
        { error: 'Failed to generate content', details: errorData },
        { status: response.status }
      );
    }

    const data = await response.json()
    return NextResponse.json({
      success: true,
      message: 'Content generated successfully',
      content: data.content,
      variations: data.variations || [],
      ai_insights: data.ai_insights || []
    })
  } catch (error) {
    console.error('Error generating content via Marketing API:', error)
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}