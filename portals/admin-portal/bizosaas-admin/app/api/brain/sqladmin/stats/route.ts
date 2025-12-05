import { NextRequest, NextResponse } from 'next/server';

// Backend API configuration - connects to SQLAdmin backend service
const BACKEND_API_URL = 'http://localhost:8005';

export async function GET(request: NextRequest) {
  try {
    console.log(`[SQLADMIN] Fetching stats: ${BACKEND_API_URL}/admin/stats`);

    // Try to fetch from backend service
    try {
      const backendResponse = await fetch(`${BACKEND_API_URL}/admin/stats`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'BizOSaaS-Admin-Frontend/1.0.0'
        }
      });

      if (backendResponse.ok) {
        const backendData = await backendResponse.json();
        console.log(`[SQLADMIN] Backend stats response successful`);
        
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
      console.log('[SQLADMIN] Using fallback mock data for stats');
      
      const fallbackData = {
        database_size: "2.1 MB",
        total_tables: 15,
        total_rows: 1250,
        active_connections: 3,
        uptime: "2 days, 5 hours",
        last_backup: "2025-09-21 23:00:00",
        performance: {
          avg_query_time: "12ms",
          cache_hit_ratio: "95.2%",
          disk_usage: "12.5%"
        },
        source: 'fallback',
        warning: 'Backend service unavailable, using mock data'
      };

      return NextResponse.json(fallbackData);
    }
  } catch (error) {
    console.error('SQLAdmin Stats API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}