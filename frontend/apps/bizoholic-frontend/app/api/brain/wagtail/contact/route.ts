/**
 * Wagtail Contact Form API Route
 * Handles contact form submissions and sends them to Wagtail CMS via FastAPI Brain Gateway
 */

import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.BRAIN_API_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Validate required fields
    const { name, email, service, message } = body
    if (!name || !email || !service || !message) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    // Forward to Brain API Gateway which handles Wagtail CMS integration
    const response = await fetch(`${BRAIN_API_URL}/wagtail/contact-forms`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.BRAIN_API_KEY || 'dev-token'}`,
      },
      body: JSON.stringify({
        form_type: 'bizoholic_contact',
        data: {
          full_name: name,
          email_address: email,
          company_name: body.company || '',
          phone_number: body.phone || '',
          service_interest: service,
          budget_range: body.budget || '',
          project_details: message,
          source: 'bizoholic_website',
          submitted_at: body.submitted_at || new Date().toISOString(),
          ip_address: request.ip || 'unknown',
          user_agent: request.headers.get('user-agent') || 'unknown'
        }
      })
    })

    if (!response.ok) {
      console.error('Brain API error:', response.status, await response.text())
      return NextResponse.json(
        { error: 'Failed to submit contact form' },
        { status: 500 }
      )
    }

    const result = await response.json()
    
    return NextResponse.json({
      success: true,
      message: 'Contact form submitted successfully',
      data: result
    })

  } catch (error) {
    console.error('Contact form API error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Bizoholic Contact API',
    endpoints: {
      'POST /api/brain/wagtail/contact': 'Submit contact form to Wagtail CMS'
    }
  })
}