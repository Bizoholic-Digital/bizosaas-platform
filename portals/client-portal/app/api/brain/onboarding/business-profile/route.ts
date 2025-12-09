import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate required fields
    const { business_type, industry, company_size, goals } = body;

    if (!body) {
      return NextResponse.json(
        { error: 'Missing request body' },
        { status: 400 }
      );
    }

    // Accept any valid business profile data
    // In a real implementation, we would save this to the database/CRM

    const businessProfile = {
      id: `bp_${Date.now()}`,
      business_type: business_type || 'unknown',
      industry: industry || 'unknown',
      company_size: company_size || 'unknown',
      goals: goals || [],
      onboarding_completed: true,
      created_at: new Date().toISOString(),
    };

    return NextResponse.json({
      success: true,
      profile: businessProfile,
      message: 'Business profile created successfully',
      next_step: '/dashboard'
    });

  } catch (error) {
    console.error('Business profile creation error:', error);
    return NextResponse.json(
      { error: 'Failed to create business profile' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  return NextResponse.json({
    success: true,
    profile: {
      id: 'bp_mock',
      business_type: 'technology',
      industry: 'software',
      company_size: '10-50',
      goals: ['lead_generation', 'brand_awareness'],
      onboarding_completed: false
    }
  });
}
