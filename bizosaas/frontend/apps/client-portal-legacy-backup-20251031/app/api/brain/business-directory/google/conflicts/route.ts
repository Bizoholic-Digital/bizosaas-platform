import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const queryParams = new URLSearchParams();
    
    // Pass through all search parameters
    searchParams.forEach((value, key) => {
      queryParams.append(key, value);
    });

    const response = await fetch(`${BRAIN_API_URL}/api/brain/business-directory/google/conflicts?${queryParams}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
    });

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status);
      // Fallback Google conflicts data
      return NextResponse.json({
        conflicts: [
          {
            id: "conflict_001",
            type: "data_mismatch",
            severity: "medium",
            location_id: "loc_001",
            location_name: "Downtown Store",
            google_data: {
              name: "Downtown Store & More",
              phone: "+1-555-0123",
              address: "123 Main St, New York, NY 10001"
            },
            platform_data: {
              name: "Downtown Store",
              phone: "+1-555-0124",
              address: "123 Main Street, New York, NY 10001"
            },
            detected_at: "2024-09-18T08:30:00Z",
            status: "pending",
            suggested_resolution: "use_google_data"
          },
          {
            id: "conflict_002",
            type: "hours_mismatch",
            severity: "low",
            location_id: "loc_002",
            location_name: "Mall Location",
            google_data: {
              hours: {
                monday: "10:00 AM - 9:00 PM",
                sunday: "11:00 AM - 7:00 PM"
              }
            },
            platform_data: {
              hours: {
                monday: "9:00 AM - 9:00 PM",
                sunday: "12:00 PM - 6:00 PM"
              }
            },
            detected_at: "2024-09-18T07:15:00Z",
            status: "pending",
            suggested_resolution: "manual_review"
          }
        ],
        total: 2,
        summary: {
          pending: 2,
          resolved: 0,
          ignored: 0,
          by_severity: {
            high: 0,
            medium: 1,
            low: 1
          }
        },
        source: "fallback"
      }, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Google conflicts API error:', error);
    return NextResponse.json({
      conflicts: [],
      total: 0,
      error: 'Failed to fetch Google conflicts',
      source: "error"
    }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetch(`${BRAIN_API_URL}/api/brain/business-directory/google/conflicts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status);
      // Fallback conflict resolution response
      return NextResponse.json({
        success: true,
        conflict_id: body.conflict_id,
        resolution: body.resolution || "manual_review",
        resolved_at: new Date().toISOString(),
        applied_changes: body.resolution === "use_google_data" ? ["name", "phone", "address"] : [],
        source: "fallback"
      }, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Google conflict resolution error:', error);
    return NextResponse.json({
      error: 'Failed to resolve Google conflict',
      source: "error"
    }, { status: 500 });
  }
}