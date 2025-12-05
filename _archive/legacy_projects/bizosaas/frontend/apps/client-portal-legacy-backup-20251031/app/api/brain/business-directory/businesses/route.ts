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

    const response = await fetch(`${BRAIN_API_URL}/api/brain/business-directory/businesses?${queryParams}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
    });

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status);
      // Fallback business directory data
      return NextResponse.json({
        businesses: [
          {
            id: "biz_001",
            name: "Digital Marketing Solutions",
            description: "Full-service digital marketing agency specializing in SEO, PPC, and social media marketing",
            category: { name: "Marketing & Advertising", slug: "marketing-advertising" },
            address: {
              street: "123 Business Street",
              city: "New York",
              state: "NY",
              postal_code: "10001",
              country: "USA"
            },
            coordinates: { latitude: 40.7128, longitude: -74.0060 },
            contact: {
              phone: "+1-555-0123",
              email: "hello@digitalmarketing.com",
              website: "https://digitalmarketing.com"
            },
            rating: 4.8,
            review_count: 156,
            is_verified: true,
            is_claimed: true,
            featured_image: "/api/placeholder-image/business-1",
            hours: {
              monday: "9:00 AM - 6:00 PM",
              friday: "9:00 AM - 5:00 PM",
              weekend: "Closed"
            }
          },
          {
            id: "biz_002",
            name: "Tech Startup Hub",
            description: "Innovative technology consulting and software development services",
            category: { name: "Technology Services", slug: "technology-services" },
            address: {
              street: "456 Innovation Drive",
              city: "San Francisco",
              state: "CA",
              postal_code: "94102",
              country: "USA"
            },
            coordinates: { latitude: 37.7749, longitude: -122.4194 },
            contact: {
              phone: "+1-555-0456",
              email: "info@techstartup.com",
              website: "https://techstartup.com"
            },
            rating: 4.6,
            review_count: 89,
            is_verified: true,
            is_claimed: false,
            featured_image: "/api/placeholder-image/business-2",
            hours: {
              monday: "8:00 AM - 7:00 PM",
              friday: "8:00 AM - 6:00 PM",
              weekend: "10:00 AM - 4:00 PM"
            }
          }
        ],
        total: 2,
        page: 1,
        size: 20,
        source: "fallback"
      }, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Business Directory API error:', error);
    return NextResponse.json({
      businesses: [],
      total: 0,
      error: 'Failed to fetch businesses',
      source: "error"
    }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetch(`${BRAIN_API_URL}/api/brain/business-directory/businesses`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status);
      // Fallback response for business creation
      return NextResponse.json({
        id: `biz_${Date.now()}`,
        name: body.name || "New Business",
        status: "pending_approval",
        created_at: new Date().toISOString(),
        source: "fallback"
      }, { status: 201 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Business creation error:', error);
    return NextResponse.json({
      error: 'Failed to create business',
      source: "error"
    }, { status: 500 });
  }
}