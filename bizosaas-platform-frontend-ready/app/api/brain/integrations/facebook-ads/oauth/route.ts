import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_BASE = process.env.BRAIN_API_URL || 'http://host.docker.internal:8001'

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const action = searchParams.get('action')
    const tenant_id = searchParams.get('tenant_id') || 'demo'
    
    let endpoint = ''
    
    if (action === 'callback') {
      const code = searchParams.get('code')
      const state = searchParams.get('state')
      const error = searchParams.get('error')
      const error_description = searchParams.get('error_description')
      
      const url = new URL(`${BRAIN_API_BASE}/api/integrations/facebook-ads/oauth/callback`)
      url.searchParams.set('tenant_id', tenant_id)
      if (code) url.searchParams.set('code', code)
      if (state) url.searchParams.set('state', state)
      if (error) url.searchParams.set('error', error)
      if (error_description) url.searchParams.set('error_description', error_description)
      
      endpoint = url.toString()
    } else {
      // Default to status check
      endpoint = `${BRAIN_API_BASE}/api/integrations/facebook-ads/oauth/status?tenant_id=${tenant_id}`
    }
    
    const response = await fetch(endpoint)
    const data = await response.json()
    
    // If this is a callback with success, redirect to close popup
    if (action === 'callback' && data.success) {
      return new Response(`
        <html>
          <body>
            <script>
              window.opener && window.opener.postMessage({ type: 'oauth_success', data: ${JSON.stringify(data)} }, '*');
              window.close();
            </script>
            <p>Authorization successful. This window will close automatically.</p>
          </body>
        </html>
      `, {
        headers: { 'Content-Type': 'text/html' }
      })
    }
    
    // If this is a callback with error, redirect to close popup
    if (action === 'callback' && data.error) {
      return new Response(`
        <html>
          <body>
            <script>
              window.opener && window.opener.postMessage({ type: 'oauth_error', error: '${data.error}' }, '*');
              window.close();
            </script>
            <p>Authorization failed: ${data.error}. This window will close automatically.</p>
          </body>
        </html>
      `, {
        headers: { 'Content-Type': 'text/html' }
      })
    }
    
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error with Facebook Ads OAuth:', error)
    return NextResponse.json(
      { success: false, error: 'OAuth operation failed' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const action = body.action || 'start'
    
    let endpoint = `${BRAIN_API_BASE}/api/integrations/facebook-ads/oauth/${action}`
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })
    
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error with Facebook Ads OAuth:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to process OAuth request' },
      { status: 500 }
    )
  }
}