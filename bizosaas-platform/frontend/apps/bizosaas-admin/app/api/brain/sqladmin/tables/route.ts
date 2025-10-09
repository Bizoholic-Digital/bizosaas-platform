import { NextRequest, NextResponse } from 'next/server';

// Backend API configuration - connects to SQLAdmin backend service
const BACKEND_API_URL = 'http://localhost:8005';

export async function GET(request: NextRequest) {
  try {
    console.log(`[SQLADMIN] Fetching tables: ${BACKEND_API_URL}/admin/tables`);

    // Try to fetch from backend service
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);
      
      const backendResponse = await fetch(`${BACKEND_API_URL}/admin/tables`, {
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
        console.log(`[SQLADMIN] Backend response successful: ${backendData.tables?.length || 0} tables`);
        
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
      console.log('[SQLADMIN] Using fallback mock data for tables');
      
      const fallbackData = {
        tables: [
          {
            name: "tenants",
            rows: 5,
            size: "64 KB",
            last_updated: "2025-09-22"
          },
          {
            name: "users", 
            rows: 25,
            size: "128 KB",
            last_updated: "2025-09-22"
          },
          {
            name: "leads",
            rows: 150,
            size: "512 KB", 
            last_updated: "2025-09-22"
          },
          {
            name: "campaigns",
            rows: 45,
            size: "256 KB",
            last_updated: "2025-09-22"
          }
        ],
        total_tables: 4,
        database: "bizosaas",
        source: 'fallback',
        warning: 'Backend service unavailable, using mock data'
      };

      return NextResponse.json(fallbackData);
    }
  } catch (error) {
    console.error('SQLAdmin Tables API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : String(error) },
      { status: 500 }
    );
  }
}