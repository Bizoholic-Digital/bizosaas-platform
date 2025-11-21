import { NextRequest, NextResponse } from 'next/server';

const BRAIN_HUB_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://bizosaas-brain-unified:8001';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const queryString = searchParams.toString();
    const url = `${BRAIN_HUB_URL}/api/crm/leads${queryString ? `?${queryString}` : ''}`;

    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      throw new Error(`Brain Hub responded with status: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error('CRM Leads API Error:', error);
    
    // Return fallback data for development
    const fallbackData = {
      success: true,
      leads: [
        {
          id: 'lead_001',
          first_name: 'Demo',
          last_name: 'Client',
          email: 'demo@client.com',
          company: 'Demo Company',
          status: 'qualified',
          score: 85
        }
      ],
      total_count: 1,
      message: 'Using fallback data - Brain Hub connection failed'
    };
    
    return NextResponse.json(fallbackData);
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const url = `${BRAIN_HUB_URL}/api/crm/leads`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
    
  } catch (error) {
    console.error('CRM Leads POST Error:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to create lead' },
      { status: 500 }
    );
  }
}