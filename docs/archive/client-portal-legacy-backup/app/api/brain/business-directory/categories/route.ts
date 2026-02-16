import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const queryParams = new URLSearchParams();
    
    // Pass through all search parameters
    searchParams.forEach((value, key) => {
      queryParams.append(key, value);
    });

    const response = await fetch(`${BRAIN_API_URL}/api/brain/business-directory/categories?${queryParams}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
    });

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status);
      // Fallback categories data
      return NextResponse.json({
        categories: [
          {
            id: "cat_001",
            name: "Marketing & Advertising",
            slug: "marketing-advertising",
            description: "Digital marketing agencies, advertising firms, and promotional services",
            business_count: 45,
            featured: true,
            icon: "megaphone"
          },
          {
            id: "cat_002",
            name: "Technology Services",
            slug: "technology-services",
            description: "Software development, IT consulting, and tech support",
            business_count: 32,
            featured: true,
            icon: "computer"
          },
          {
            id: "cat_003",
            name: "Professional Services",
            slug: "professional-services",
            description: "Legal, accounting, consulting, and business services",
            business_count: 28,
            featured: true,
            icon: "briefcase"
          },
          {
            id: "cat_004",
            name: "Restaurants & Food",
            slug: "restaurants-food",
            description: "Restaurants, cafes, food delivery, and catering services",
            business_count: 67,
            featured: true,
            icon: "utensils"
          },
          {
            id: "cat_005",
            name: "Health & Wellness",
            slug: "health-wellness",
            description: "Healthcare providers, fitness centers, and wellness services",
            business_count: 41,
            featured: true,
            icon: "heart"
          },
          {
            id: "cat_006",
            name: "Retail & Shopping",
            slug: "retail-shopping",
            description: "Retail stores, e-commerce, and shopping centers",
            business_count: 39,
            featured: false,
            icon: "shopping-bag"
          },
          {
            id: "cat_007",
            name: "Real Estate",
            slug: "real-estate",
            description: "Real estate agents, property management, and construction",
            business_count: 24,
            featured: false,
            icon: "home"
          },
          {
            id: "cat_008",
            name: "Education & Training",
            slug: "education-training",
            description: "Schools, training centers, and educational services",
            business_count: 18,
            featured: false,
            icon: "graduation-cap"
          }
        ],
        total: 8,
        source: "fallback"
      }, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Business Directory Categories API error:', error);
    return NextResponse.json({
      categories: [],
      total: 0,
      error: 'Failed to fetch categories',
      source: "error"
    }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetch(`${BRAIN_API_URL}/api/brain/business-directory/categories`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status);
      // Fallback response for category creation
      return NextResponse.json({
        id: `cat_${Date.now()}`,
        name: body.name || "New Category",
        slug: body.slug || body.name?.toLowerCase().replace(/\s+/g, '-') || "new-category",
        status: "active",
        business_count: 0,
        created_at: new Date().toISOString(),
        source: "fallback"
      }, { status: 201 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Category creation error:', error);
    return NextResponse.json({
      error: 'Failed to create category',
      source: "error"
    }, { status: 500 });
  }
}