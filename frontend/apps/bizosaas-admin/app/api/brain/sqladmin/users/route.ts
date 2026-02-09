import { NextRequest, NextResponse } from 'next/server';

// Backend API configuration - connects to SQLAdmin backend service
const BACKEND_API_URL = 'http://localhost:8005';

export async function GET(request: NextRequest) {
  try {
    console.log(`[SQLADMIN] Fetching users: ${BACKEND_API_URL}/admin/users`);

    // Try to fetch from backend service
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);

      const backendResponse = await fetch(`${BACKEND_API_URL}/admin/users`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'BizOSaaS-Admin-Frontend/1.0.0'
        },
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (backendResponse.ok) {
        const backendData = await backendResponse.json();
        console.log(`[SQLADMIN] Backend users response successful: ${backendData.users?.length || 0} users`);
        
        return NextResponse.json({
          ...backendData,
          source: 'backend'
        });
      } else {
        console.warn(`[SQLADMIN] Backend returned ${backendResponse.status}: ${backendResponse.statusText}`);
        throw new Error(`Backend API error: ${backendResponse.status}`);
      }
    } catch (backendError) {
      console.error('[SQLADMIN] Backend connection failed:', backendError);
      
      // Fallback to mock data
      console.log('[SQLADMIN] Using fallback mock data for users');
      
      const fallbackData = {
        users: [
          {
            id: 1,
            username: "admin",
            role: "Administrator",
            status: "active",
            last_login: "2025-09-22 14:30:00"
          },
          {
            id: 2,
            username: "manager",
            role: "Manager", 
            status: "active",
            last_login: "2025-09-22 12:15:00"
          },
          {
            id: 3,
            username: "user1",
            role: "User",
            status: "active", 
            last_login: "2025-09-22 09:45:00"
          }
        ],
        total_users: 3,
        active_sessions: 2,
        source: 'fallback',
        warning: 'Backend service unavailable, using mock data'
      };

      return NextResponse.json(fallbackData);
    }
  } catch (error) {
    console.error('SQLAdmin Users API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : String(error) },
      { status: 500 }
    );
  }
}