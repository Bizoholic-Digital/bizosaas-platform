import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_BASE = process.env.BRAIN_API_URL || 'http://host.docker.internal:8001'

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const endpoint = searchParams.get('endpoint') || 'leads'
    const tenant_id = searchParams.get('tenant_id') || 'demo'
    
    let url = ''
    
    switch (endpoint) {
      case 'leads':
        const status = searchParams.get('status')
        const assigned_to = searchParams.get('assigned_to')
        const limit = searchParams.get('limit')
        
        url = `${BRAIN_API_BASE}/api/crm/leads?tenant_id=${tenant_id}`
        if (status) url += `&status=${status}`
        if (assigned_to) url += `&assigned_to=${assigned_to}`
        if (limit) url += `&limit=${limit}`
        break
        
      case 'dashboard':
        url = `${BRAIN_API_BASE}/api/crm/dashboard/stats?tenant_id=${tenant_id}`
        break
        
      default:
        return NextResponse.json(
          { success: false, error: 'Invalid endpoint' },
          { status: 400 }
        )
    }
    
    const response = await fetch(url)
    const data = await response.json()
    
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching CRM data:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to fetch CRM data' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { endpoint = 'leads', ...requestData } = body
    
    let url = ''
    
    switch (endpoint) {
      case 'leads':
        url = `${BRAIN_API_BASE}/api/crm/leads`
        break
        
      case 'activities':
        const leadId = requestData.lead_id
        if (!leadId) {
          return NextResponse.json(
            { success: false, error: 'Lead ID required for activities' },
            { status: 400 }
          )
        }
        url = `${BRAIN_API_BASE}/api/crm/leads/${leadId}/activities`
        break
        
      case 'recalculate-score':
        const scoreLeadId = requestData.lead_id
        if (!scoreLeadId) {
          return NextResponse.json(
            { success: false, error: 'Lead ID required for score recalculation' },
            { status: 400 }
          )
        }
        url = `${BRAIN_API_BASE}/api/crm/leads/${scoreLeadId}/score/recalculate`
        break
        
      default:
        return NextResponse.json(
          { success: false, error: 'Invalid endpoint' },
          { status: 400 }
        )
    }
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData)
    })
    
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error creating CRM data:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to create CRM data' },
      { status: 500 }
    )
  }
}